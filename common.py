import os
import urllib.parse

import openai
import requests
import pandas as pd
from bs4 import BeautifulSoup
import re
from openai import OpenAI
import pickle

cache_file = 'api_cache.pkl'

client = OpenAI()
key = os.getenv("SCRAPE_API_KEY")

api_base_url = "https://scrape.abstractapi.com/v1"

headers = {
    "Content-Type": "application/json"
}


def load_cache():
    if os.path.exists(cache_file):
        with open(cache_file, 'rb') as f:
            return pickle.load(f)
    return {}


def save_cache(cache):
    with open(cache_file, 'wb') as f:
        pickle.dump(cache, f)
