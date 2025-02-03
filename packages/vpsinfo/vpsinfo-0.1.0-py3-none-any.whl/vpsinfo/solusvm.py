#!/usr/bin/env python
# -*- coding: utf-8 -*-
# vim: tabstop=4 shiftwidth=4 softtabstop=4

"""
The SolusVM Client API SDK for Python
"""

import re
import requests


class SolusVMClient:
    """
    SolusVM API client
    """

    def __init__(self, url, key, apihash, timeout=60):
        """
        init the SolusClient Object
        :param url: root URL, such as 'https://solusvm.com:5656'
        :param key: the API KEY, from cpanel
        :param apihash:  the API Hash, from cpanel
        :return: the new object
        """
        self.url = url
        self.key = key
        self.hash = apihash
        self.timeout = timeout

    @staticmethod
    def _xml2dict(xmlstr):
        """
        transfer XML to dict obj
        :param xmlstr:  the XML string
        :return: the dict obj
        """
        obj = {}
        # More robust XML parsing
        tag = re.compile("<(.*?)>([^<]+)<\/\\1>")
        matches = tag.finditer(xmlstr)
        for match in matches:
            tag_name, value = match.groups()
            obj[tag_name] = value.strip()  # Remove any whitespace

        if not obj:
            return {"error": "Failed to parse XML response"}

        return obj

    def _post(self, action, extra=None):
        """
        post data req to server
        :param action: the action that will do
        :return: the server's XML return
        """
        data = {"rdtype": "json", "hash": self.hash, "key": self.key, "action": action}

        if extra:
            data.update(extra)

        response = requests.post(
            self.url + "/api/client/command.php",
            params=data,
            timeout=self.timeout,
            verify=True,
        )
        if response.status_code != 200:
            return {"error": f"HTTP {response.status_code}: {response.text}"}

        # Always parse as XML since that's what the API returns
        result = self._xml2dict(response.text)

        # Debug output if needed
        # print("\nDebug: API Response:")
        # print(f"Status Code: {response.status_code}")
        # print(f"Content-Type: {response.headers.get('content-type', 'Not specified')}")
        # print(f"Raw Response: {response.text}")
        # print(f"Parsed Result: {result}\n")

        return result

    def info(self):
        """
        Retieve server information
        """
        extra = {
            "bw": "true",
            "hdd": "true",
            "mem": "true",
        }
        return self._post("info", extra)

    def status(self):
        """
        Retiev server status
        """
        return self._post("status")

    def reboot(self):
        """
        Reboot the server
        """
        return self._post("reboot")

    def boot(self):
        """
        Boot the server
        """
        return self._post("boot")

    def shutdown(self):
        """
        shutdown the server
        """
        return self._post("shutdown")

    def command(self, action):
        """
        run the command raw
        """
        return getattr(self, action)()
