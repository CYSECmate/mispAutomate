#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from private.splunkKeys import splunkUrl, splunkUser, splunkPass
import requests


''' Function which push the misp exported indicators JSON to Splunk '''
def getSplunkContent(typeIntel, splunkUser, splunkPass):
  response = requests.get(splunkUrl+typeIntel, auth=(splunkUser, splunkPass), verify=False)
  return(response.text)



