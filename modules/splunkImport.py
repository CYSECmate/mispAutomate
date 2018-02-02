#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from private.splunkKeys import splunkUrl, splunkUser, splunkPass
import requests
from lib.logger import *
import sys

''' Function which get the current splunk lookup indicators '''
def getSplunkContent(typeIntel, splunkUser, splunkPass):
  response = requests.get(splunkUrl+typeIntel, auth=(splunkUser, splunkPass), verify=False)
  return(response.text)


''' Function which delete the content of a splunk lookup '''
def deleteSplunkContent(typeIntel, splunkUser, splunkPass):
  response = requests.delete(splunkUrl+typeIntel, auth=(splunkUser, splunkPass), verify=False)
  if str(response.status_code) != ("200" or "404"):
      logger.info("Error - Response code "+str(response.status_code)+" - Cannot delete Splunk "+typeIntel)
      logger.info("------- Script finished with error")
      sys.exit(0)
  return(str(response.status_code))


''' Function which push the misp exported indicators JSON to Splunk '''
def pushSplunkContent(typeIntel, splunkUser, splunkPass, param):
  response = requests.post(splunkUrl+typeIntel+"/batch_save", json = param, auth=(splunkUser, splunkPass), verify=False)
  if str(response.status_code) != "200":
      logger.info("Error - Response code "+str(response.status_code)+" - Cannot update Splunk "+typeIntel)
      logger.info("------- Script finished with error")
      sys.exit(0)
  return(str(response.status_code))
