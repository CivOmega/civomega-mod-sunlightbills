"""
Must define three methods:

* answer_pattern(pattern, args)
* render_answer_html(answer_data)
* render_answer_json(answer_data)
"""
from .patterns import PATTERNS, BILL_PATTERNS, PERSON_PATTERNS

import json
import os
import re
import requests
from django.template import loader, Context
from django.conf import settings


PATTERN_ARGS_RE = re.compile(r'{([A-Za-z0-9_]+)}')


def get_api_key():
    key = None
    try:
        key = settings.SUNLIGHT_API_KEY
    except:
        pass
    if 'SUNLIGHT_API_KEY' in os.environ:
        key = os.environ['SUNLIGHT_API_KEY']
    if key == None:
        raise Exception("To use this module, you must have a Sunlight API Key. See the readme here: https://github.com/CivOmega/civomega-mod-sunlightbills/")
    else:
        return key

def bill_search(topic):
    url = 'https://congress.api.sunlightfoundation.com/bills?apikey=%s&query=%s' % (get_api_key(), topic)
    resp = requests.get(url)
    return resp.json()

def person_search_by_zip(zipcode):
    url = 'https://congress.api.sunlightfoundation.com/legislators/locate?apikey=%s&zip=%s' % (get_api_key(), zipcode)
    resp = requests.get(url)
    return resp.json()

def person_search_by_party(party):
    party = party[0].upper()
    if party not in "DR":
      # party is D or R or I
      party = "I"
    url = 'https://congress.api.sunlightfoundation.com/legislators?apikey=%s&party=%s' % (get_api_key(), party)
    resp = requests.get(url)
    return resp.json()





############################################################
# Pattern-dependent behavior
def answer_pattern(pattern, args):
    """
    Returns a `dict` representing the answer to the given
    pattern & pattern args.
    """
    if pattern not in PATTERNS:
      # not one of our patterns
      return None
    if len(args) != 1:
      # we didn't actually search anything. (if this is a slow API, you can
      # change this to "len(args) < 5" to wait until a certain # of letters
      # are typed in before firing off your search to the API.)
      return None

    if pattern in BILL_PATTERNS:
      # Currently, our BILL_PATTERNS all only have one argument: the topic
      topic = args[0]
      return {
        'type': 'bill',
        'data': bill_search(topic)
      }
    elif pattern in PERSON_PATTERNS:
      # We might be looking up via zip code or text search, so see what
      # pattern the user used
      args_keys = PATTERN_ARGS_RE.findall(pattern)
      kwargs = dict(zip(args_keys,args))

      if "zipcode" in kwargs:
        # a zipcode search
        zipcode = kwargs['zipcode']
        return {
          'type': 'person',
          'data': person_search_by_zip(zipcode)
        }
      elif "party" in kwargs:
        # a search for legislators, by party
        party = kwargs['party']
        return {
          'type': 'person',
          'data': person_search_by_party(party)
        }

    return None




############################################################
# Applicable module-wide
def render_answer_html(answer_data):
    # This receives what we got in `answer_pattern` and returns HTML.

    if answer_data.get('type', None) == "bill":
      data = answer_data['data']
      template = loader.get_template('comod_sunlightbills/sunlightbills_bill_results.html')
      return template.render(Context(data))
    elif answer_data.get('type', None) == "person":
      data = answer_data['data']
      template = loader.get_template('comod_sunlightbills/sunlightbills_person_results.html')
      return template.render(Context(data))
    else:
      # TODO: render a template for "we don't know how to handle this search
      raise Exception

def render_answer_json(answer_data):
    return json.dumps(answer_data)
