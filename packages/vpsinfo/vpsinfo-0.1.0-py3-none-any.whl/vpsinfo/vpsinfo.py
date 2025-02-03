#!/usr/bin/env python3
import click
import json
from concurrent.futures import ThreadPoolExecutor
from pathlib import Path
from tabulate import tabulate
from typing import List, Dict

from .solusvm import SolusVMClient


CONFIG_PATH = Path.home() / ".vpsinfo.json"


class EnhancedSolusClient(SolusVMClient):
    """Extended SolusVM client supporting concurrent requests"""

    @staticmethod
    def from_config(node: Dict) -> "EnhancedSolusClient":
        """Create client instance from configuration node"""
        return EnhancedSolusClient(
            url=node["url"], key=node["key"], apihash=node["hash"], timeout=15
        )

    def get_bw_info(self) -> Dict:
        """Get bandwidth information"""
        try:
            data = self.info()
            if data.get("status") != "success":
                return {"error": data.get("statusmsg", "Unknown error")}

            def parse_resource(value, split_count=4):
                """Parse comma-separated resource values"""
                if not value:
                    return None, None, None
                parts = value.split(",")
                if len(parts) >= split_count:
                    total = float(parts[0])
                    used = float(parts[1])
                    # For disk, return None for used and percent if used is 0
                    if value == data.get("hdd") and used == 0:
                        return None, total, None
                    # For other resources, return None for all if total is 0
                    elif total == 0:
                        return None, None, None

                    percent = (
                        float(parts[3])
                        if len(parts) > 3 and float(parts[3]) > 0
                        else (used / total * 100 if total > 0 else 0)
                    )
                    return used, total, percent
                return None, None, None

            # Parse bandwidth, memory and disk data
            bw_used, bw_total, bw_percent = parse_resource(data.get("bw"))
            mem_used, mem_total, mem_percent = parse_resource(data.get("mem"))
            disk_used, disk_total, disk_percent = parse_resource(data.get("hdd"))

            return {
                "hostname": data.get("hostname"),
                "ipaddress": data.get("ipaddress"),
                "bw_used": bw_used,
                "bw_total": bw_total,
                "bw_percent": bw_percent,
                "mem_used": mem_used,
                "mem_total": mem_total,
                "mem_percent": mem_percent,
                "disk_used": disk_used,
                "disk_total": disk_total,
                "disk_percent": disk_percent,
            }
        except Exception as e:
            return {"error": str(e)}


def load_config() -> List[Dict]:
    """Load configuration file"""
    if not CONFIG_PATH.exists():
        raise FileNotFoundError(f"Config file not found: {CONFIG_PATH}")

    with open(CONFIG_PATH) as f:
        config = json.load(f)

    required_fields = ["name", "url", "key", "hash"]
    for node in config:
        if any(field not in node for field in required_fields):
            raise ValueError(f"Invalid node config: {node}")

    return config


def human_readable(size: float) -> str:
    """Convert bytes to human readable format"""
    for unit in ["B", "KiB", "MiB", "GiB", "TiB"]:
        if size < 1024.0:
            return f"{size:.2f} {unit}"
        size /= 1024.0
    return f"{size:.2f} PiB"


def process_nodes(nodes: List[Dict], func: callable) -> List[List]:
    """Process node requests concurrently"""
    with ThreadPoolExecutor() as executor:
        futures = [
            executor.submit(func, EnhancedSolusClient.from_config(node))
            for node in nodes
        ]

        results = []
        for node, future in zip(nodes, futures):
            result = future.result()
            if "error" in result:
                results.append([node["name"], "Error", result["error"]])
            else:
                # Extract all values
                name = f"{node['name']} ({result.get('ipaddress', 'N/A')})"
                results.append(
                    [
                        name,
                        "Success",
                        result.get("bw_used"),
                        result.get("bw_total"),
                        result.get("bw_percent"),
                        result.get("mem_used"),
                        result.get("mem_total"),
                        result.get("mem_percent"),
                        result.get("disk_used"),
                        result.get("disk_total"),
                        result.get("disk_percent"),
                    ]
                )
        return results


@click.command()
@click.option("--verbose", "-v", is_flag=True, help="Enable debug output")
def cli(verbose):
    """VPS information monitoring tool"""
    try:
        nodes = load_config()
        results = process_nodes(nodes, lambda client: client.get_bw_info())

        if verbose:
            click.echo("Debug: Raw results from API:")
            for i, result in enumerate(results):
                click.echo(f"Row {i}: {result} (length: {len(result)})")

        # Convert data to readable format
        formatted_results = []
        for row in results:
            if verbose:
                click.echo(f"\nProcessing row: {row}")

            if row[1] == "Error":
                if verbose:
                    click.echo("Error case - adding N/A columns")
                formatted_results.append(
                    [
                        row[0],  # name
                        f"{row[1]} - {row[2]}",  # Error with message
                        "N/A",  # bw used
                        "N/A",  # bw total
                        "N/A",  # bw %
                        "N/A",  # mem used
                        "N/A",  # mem total
                        "N/A",  # mem %
                        "N/A",  # disk used
                        "N/A",  # disk total
                        "N/A",  # disk %
                    ]
                )
            else:
                if verbose:
                    click.echo("Success case - formatting values")
                # Format all values
                formatted_results.append(
                    [
                        row[0],  # name with IP
                        row[1],  # status
                        human_readable(float(row[2]))
                        if row[2] is not None
                        else "N/A",  # bw used
                        human_readable(float(row[3]))
                        if row[3] is not None
                        else "N/A",  # bw total
                        f"{row[4]:.1f}%" if row[4] is not None else "N/A",  # bw percent
                        human_readable(float(row[5]))
                        if row[5] is not None
                        else "N/A",  # mem used
                        human_readable(float(row[6]))
                        if row[6] is not None
                        else "N/A",  # mem total
                        f"{row[7]:.1f}%" if row[7] is not None else "N/A",  # mem %
                        human_readable(float(row[8]))
                        if row[8] is not None
                        else "N/A",  # disk used
                        human_readable(float(row[9]))
                        if row[9] is not None
                        else "N/A",  # disk total
                        f"{row[10]:.1f}%" if row[10] is not None else "N/A",  # disk %
                    ]
                )

        if verbose:
            click.echo("\nDebug: Final formatted results:")
            for row in formatted_results:
                click.echo(f"Formatted row: {row}")

            click.echo("\nGenerating table:")
        click.echo(
            tabulate(
                formatted_results,
                headers=[
                    "VPS Name",
                    "Status",
                    "BW Used",
                    "BW Total",
                    "BW %",
                    "Mem Used",
                    "Mem Total",
                    "Mem %",
                    "Disk Used",
                    "Disk Total",
                    "Disk %",
                ],
                tablefmt="fancy_grid",
            )
        )
    except Exception as e:
        click.secho(f"Error: {str(e)}", fg="red")


if __name__ == "__main__":
    cli()
