#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from modules.splunkImport import *
from modules.mispExport import *
import argparse
import os
import json


''' Variables '''
finalJsonArray = []


''' User choices Class '''
class userChoices:
  def __init__(self, category, dateRange, tag):
    self.category = category
    if tag:
      self.tag = tag
    else:
      self.tag = None
    self.dateRange = dateRange
    if self.category == "domain":
      self.categories = ['domain']
    if self.category == "email":
      self.categories = ['email-src', 'email-dst']
    if self.category == "ip":
      self.categories = ['ip-src', 'ip-dst']



if __name__ == '__main__':
  parser = argparse.ArgumentParser(description='Get all the events matching a category and date range')
  parser.add_argument("-c", "--category", required=True, help="Parameter to search (ip, email, domain, etc.)")
  parser.add_argument("-d", "--daterange", required=True, type=int, help="Only get the last X days updated attributes (5, 10, etc.)")
  parser.add_argument("-t", "--tag", required=False, help="Get only events with specific tag - example: send:siem")
  
  args = parser.parse_args()

  misp = init(mispUrl, mispKey, mispVerifycert)

  u = userChoices(args.category, args.daterange, args.tag)
  

  if u.category == 'domain':
    for category in u.categories:
      kwargs = {'type_attribute': category}
      response = searchEvent(misp, kwargs)
      if response:
        finalJsonArray = getJsonArray(misp, response, u.dateRange, u.tag)
    for item in finalJsonArray:
      for key, value in item.copy().items():
        if key == "value":
          item['domain'] = item['value']
          del(item['value'])
    response = deleteSplunkContent("misp_domain_intel", splunkUser, splunkPass)
    response = pushSplunkContent("misp_domain_intel", splunkUser, splunkPass, finalJsonArray)

  if u.category == 'ip':
    for category in u.categories:
      kwargs = {'type_attribute': category}
      response = searchEvent(misp, kwargs)
      if response:
        finalJsonArray = getJsonArray(misp, response, u.dateRange, u.tag)
    for item in finalJsonArray:
      for key, value in item.copy().items():
        if key == "value":
          item['ip'] = item['value']
          del(item['value'])
    response = deleteSplunkContent("misp_ip_intel", splunkUser, splunkPass)
    response = pushSplunkContent("misp_ip_intel", splunkUser, splunkPass, finalJsonArray)
  if u.category == 'email':
    for category in u.categories:
      kwargs = {'type_attribute': category}
      response = searchEvent(misp, kwargs)
      if response['response']:
        finalJsonArray = getJsonArray(misp, response, u.dateRange, u.tag)
    for item in finalJsonArray:
      for key, value in item.copy().items():
        if key == "value":
          item['src_user'] = item['value']
          item['subject'] = ""
          del(item['value'])
    response = deleteSplunkContent("misp_email_intel", splunkUser, splunkPass)
    response = pushSplunkContent("misp_email_intel", splunkUser, splunkPass, finalJsonArray)


  print(finalJsonArray)
      







































