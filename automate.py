#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from modules.splunkImport import *
from modules.mispExport import *
from lib.logger import *
import argparse
import sys

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
    elif self.category == "email":
      self.categories = ['email-src', 'email-dst']
    elif self.category == "ip":
      self.categories = ['ip-src', 'ip-dst']
    else:
      logger.error("Category should be: email, domain or ip")
      sys.exit(0)



if __name__ == '__main__':
  parser = argparse.ArgumentParser(description='Get all the events matching a category and date range')
  parser.add_argument("-c", "--category", required=True, help="Parameter to search (ip, email, domain)")
  parser.add_argument("-d", "--daterange", required=True, type=int, help="Only get the last X days updated attributes (5, 10, etc.)")
  parser.add_argument("-t", "--tag", required=False, help="Get only events with specific tag - example: send:siem")
  
  args = parser.parse_args()
  logger.info("------- Script started ...") 

  misp = init(mispUrl, mispKey, mispVerifycert)

  u = userChoices(args.category, args.daterange, args.tag)

  logger.info("Category - {}".format(u.category))
  for category in u.categories:
    kwargs = {'type_attribute': category, 'tags': u.tag}
    logger.info("Search Misp events with (subcategory) {}, (date range) {} days, (tag) {}".format(category, u.dateRange, u.tag))
    response = searchEvent(misp, kwargs)
    if response['response']:
      finalJsonArray, numberOfAttributes = getJsonArray(misp, response, u.dateRange, u.tag)
      logger.info("{} attributes found for the above parameters".format(numberOfAttributes))
    else:
      logger.info("0 attribute(s) found for the above parameters")
  
  # Reformate the finalJsonArray depending on the category
  for item in finalJsonArray:
    for key, value in item.copy().items():
      if key == "value":
        if u.category == "domain":
          item['domain'] = item['value']
          del(item['value'])
        elif u.category == "ip":
          item['ip'] = item['value']
          del(item['value'])
        elif u.category == "email":
          item['src_user'] = item['value']
          item['subject'] = ""
          del(item['value'])

  # Delete and send data to Splunk depending on the category
  if u.category == "domain":
    logger.info("Delete misp_domain_intel lookup within Splunk")
    response = deleteSplunkContent("misp_domain_intel", splunkUser, splunkPass)
    logger.info("Send new data to Splunk")
    response = pushSplunkContent("misp_domain_intel", splunkUser, splunkPass, finalJsonArray)
  elif u.category == "ip":
    logger.info("Delete misp_ip_intel lookup within Splunk")
    response = deleteSplunkContent("misp_ip_intel", splunkUser, splunkPass)
    logger.info("Send new data to Splunk")
    response = pushSplunkContent("misp_ip_intel", splunkUser, splunkPass, finalJsonArray)
  elif u.category == "email":
    logger.info("Delete misp_email_intel lookup within Splunk")
    response = deleteSplunkContent("misp_email_intel", splunkUser, splunkPass)
    logger.info("Send new data to Splunk")
    response = pushSplunkContent("misp_email_intel", splunkUser, splunkPass, finalJsonArray)

  logger.info("------- Script successfully finished")

      







































