#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from pymisp import PyMISP
from private.mispKeys import mispUrl, mispKey, mispVerifycert
import datetime, time


''' Variables '''
finalJsonArray = []


''' Function which initialise the connection to MISP '''
def init(mispUrl, mispKey, mispVerifycert):
  return PyMISP(mispUrl, mispKey, mispVerifycert, 'json')


''' Function which convert timestamp into readable date '''
def convertTimestampIntoReadableDate(timestamp):
  return datetime.datetime.fromtimestamp(int(timestamp)).strftime('%Y-%m-%d %H:%M:%S')


''' Function which remove X days to the curent timestamp for the search - Last X days updated attributes '''
def is_AttributeTimestampWithinDeltaOfDays(timestamp, numberOfDays):
  currentTime = datetime.datetime.now()                              # Get Current Time
  delta = datetime.timedelta(days=int(numberOfDays))                 # Convert int(number) of days into datetime type
  deltaTime = currentTime - delta                                    # Get new time: current time - number of days
  timestampToCheck = datetime.datetime.fromtimestamp(int(timestamp)) # Convert the attribute timestamp into datetime type
  if timestampToCheck > deltaTime:                                   # Check if the attribute timestamp within the delta Time
    return True
  else:
    return False


''' Search Misp event of specific attribute type '''
def searchEvent(mispObject, kwargs):
  response = mispObject.search(controller='attributes', **kwargs)
  return(response)


''' Get event details from misp and return a dict '''
def getEventDetailsFromMisp(mispObject, eventId):
    event = mispObject.get_event(eventId)
    dictEvent = {}
    dictEvent['event_id'] = eventId
    dictEvent['published'] = event['Event']['published']
    dictEvent['event_info'] = event['Event']['info']
    dictEvent['event_tag'] = ""
    if "Tag" in event['Event']:
      for tag_in_event in event['Event']['Tag']:
        dictEvent['event_tag'] += tag_in_event['name']+","
      dictEvent['event_tag'] = dictEvent['event_tag'][:-1]
    return dictEvent


''' Return dict of the attribute details '''
def getAttributeDetails(attribute):
    dictAttribute = {}
    dictAttribute['event_id'] = attribute['event_id']
    dictAttribute['attribute_updatedDate'] = convertTimestampIntoReadableDate(attribute['timestamp'])
    dictAttribute['value'] = attribute['value']
    dictAttribute['description'] = attribute['comment']
    dictAttribute['weight'] = "1"
    dictAttribute['attribute_type'] = attribute['type']
    dictAttribute['attribute_id'] = attribute['id']
    dictAttribute['attribute_tag'] = ""
    if "Tag" in attribute:
      for tag_in_attribute in attribute['Tag']:
         dictAttribute['attribute_tag'] += tag_in_attribute['name']+","
      dictAttribute['attribute_tag'] = dictAttribute['attribute_tag'][:-1]
    return dictAttribute



''' Function which returns attributes as JSON Array '''
def getJsonArray(mispObject, response, dateRange, tag):
  eventIdSet = set()   # Contains dict of each event id
  events = []          # Contains Json array of each event
  attributes = []      # Contains Json array of each attribute

  for attribute_item in response['response']['Attribute']:
    if is_AttributeTimestampWithinDeltaOfDays(attribute_item['timestamp'], dateRange):
      eventIdSet.add(attribute_item['event_id'])
      attributes.append(getAttributeDetails(attribute_item))

  for event_item in eventIdSet:
    events.append(getEventDetailsFromMisp(mispObject, event_item))

  for event in events:
    for attribute in attributes:
      if event['event_id'] == attribute['event_id']:
        if tag:
          if tag in event['event_tag']:
            finalJsonArray.append({**event, **attribute})
          else:
            pass
        else:
          finalJsonArray.append({**event, **attribute})
  return finalJsonArray






