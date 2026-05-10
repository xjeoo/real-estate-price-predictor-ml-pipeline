from .constants import USER_AGENTS
import random
import requests
from dotenv import load_dotenv
import os

load_dotenv()
def get_new_session():
    """Creates new HTTP session with randomly selected User-Agent"""
    session = requests.Session()
    session.headers.update({
        'User-Agent': random.choice(USER_AGENTS),
        'Accept-Language': 'ro-RO,ro;q=0.9,en-US;q=0.8,en;q=0.7',
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
        'Referer': os.getenv("REFERER", "https://www.google.com/")
    })
    return session