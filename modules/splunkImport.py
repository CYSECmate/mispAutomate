#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from private.splunkKeys import splunkUrl, splunkUser, splunkPass
import requests


''' Function which get the current splunk lookup indicators '''
def getSplunkContent(typeIntel, splunkUser, splunkPass):
  response = requests.get(splunkUrl+typeIntel, auth=(splunkUser, splunkPass), verify=False)
  return(response.text)


''' Function which delete the content of a splunk lookup '''
def deleteSplunkContent(typeIntel, splunkUser, splunkPass):
  response = requests.delete(splunkUrl+typeIntel, auth=(splunkUser, splunkPass), verify=False)
  return(response.status_code)


''' Function which push the misp exported indicators JSON to Splunk '''
def pushSplunkContent(typeIntel, splunkUser, splunkPass, param):
  response = requests.post(splunkUrl+typeIntel+"/batch_save", json = param, auth=(splunkUser, splunkPass), verify=False)
  return(response.status_code)
