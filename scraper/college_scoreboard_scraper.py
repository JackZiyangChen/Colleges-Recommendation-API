import requests
import json
import csv


API_KEY = "X6X0rbM1WVq8kJClxtF1Jgqd9G3LcE6bjFgr2upE"
BASE_URL = "https://api.data.gov/ed/collegescorecard/v1/schools?"


req_url = BASE_URL + "api_key=" + API_KEY