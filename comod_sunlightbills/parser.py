"""
Must define three methods:

* answer_pattern(pattern, args)
* render_answer_html(answer_data)
* render_answer_json(answer_data)
"""
from .patterns import PATTERNS

import json
import os
import requests
from django.template import loader, Context


def search(topic):
    url = 'https://congress.api.sunlightfoundation.com/bills?apikey=%s&query=%s' % (os.environ['SUNLIGHT_API_KEY'], topic)
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
      return None
    if len(args) != 1:
      return None

    topic = args[0]

    results = search(topic)
    return results

############################################################
# Applicable module-wide
def render_answer_html(answer_data):
    template = loader.get_template('comod_sunlightbills/sunlightbills_search.html')
    return template.render(Context(answer_data))

def render_answer_json(answer_data):
    return json.dumps(answer_data)
