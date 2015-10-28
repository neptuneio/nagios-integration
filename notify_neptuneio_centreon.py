#!/usr/bin/env python

"""
Script to send Nagios events to Neptune.io

This script is designed to work as a notification command for Nagios,
which reads the event details from environment and pushes that event
to Neptune.io whenever a notification is triggered. Please read the
integration guide for more details on how to use this script.
"""

from optparse import OptionParser

import os
import sys
import requests
import simplejson as json

API_BASE_URL = 'https://www.neptune.io/api/v1/trigger/channel/nagios/'


def send_to_neptune(key, e):
    try:
        response = requests.post(API_BASE_URL + key, data=json.dumps(e), verify=True)
        if response.status_code != 200:
            print("Failed to send the event to Neptune.io; status: %d, msg: %s", response.status_code, response.text)
    except Exception:
        _, e, _ = sys.exc_info()
        print("Failed to send the event to Neptune.io; Error: %s", repr(e))


if __name__ == "__main__":
    p = OptionParser()
    p.add_option('--api_key', '-k', type='string')
    p.add_option('--type', '-t', type='string')
    p.add_option('--event', '-e', type='string')
    (options, arguments) = p.parse_args()

    api_key = options.api_key
    if not api_key:
        print("Neptune.io API key is missing. Please specify it with --api_key option.")
        sys.exit(1)
    if not options.event:
        print("--event option is missing.")
        sys.exit(1)

    event = json.loads(options.event)

    if options.type:
        event['type'] = options.type
    print json.dumps(event)

    send_to_neptune(api_key, event)
