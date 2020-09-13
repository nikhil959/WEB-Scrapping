from urllib.request import urlopen, Request
from bs4 import BeautifulSoup
import re
import json
import pymongo
from pymongo import MongoClient
from datetime import datetime
from urllib.error import HTTPError
from urllib.error import URLError
import random
from fake_useragent import UserAgent
import time
import urllib
from PyPDF2 import PdfFileReader, PdfFileWriter
from io import StringIO
import os
import wget

cwd = os.path.dirname(__file__)

alphabets = ["A", "B", "C", "D", "E", "F", "G", "H", "I", "J", "K", "L", "M", "N", "O", "P", "Q", "R", "S", "T", "U", "V", "W", "X", "Y", "Z"]
    
for item in alphabets:
    req = urllib.request.Request(
    "https://www.annauniv.edu/cai/Affiliated%20Colleges%20list%20by%20Alphabetical/"+str(item)+".html", 
    data=None, 
    headers={
        'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_9_3) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/35.0.1916.47 Safari/537.36'
    }
    )
    try:
        html = urllib.request.urlopen(req)
        bs = BeautifulSoup(html.read(), 'html.parser')
        each_alphabet_result = [i.get("href") for i in bs.findAll('a') if re.search("^A.*html$",i.get("href")) is not None] 
        if each_alphabet_result:
            for each_link in each_alphabet_result:
                req = urllib.request.Request(
                "https://www.annauniv.edu/cai/Affiliated%20Colleges%20list%20by%20Alphabetical/"+ str(each_link), 
                data=None, 
                headers={
                    'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_9_3) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/35.0.1916.47 Safari/537.36'
                }
                )
                html = urllib.request.urlopen(req)
                each_bs = BeautifulSoup(html.read(), 'html.parser')
                pdf_url_list = [i.get("href") for i in each_bs.findAll('a') if re.search("pdf$",i.get("href")) is not None]
                for each_pdb in pdf_url_list:
                    pdf_url = "https://www.annauniv.edu/cai/Affiliated%20Colleges%20list%20by%20Alphabetical/"+ each_pdb
                    file_name = wget.download(pdf_url, out=cwd+ "pdf_files")
                    
                    # memoryFile = StringIO(pdf_file)
                    # pdfFile = PdfFileReader(memoryFile)
                    import pdb
                    pdb.set_trace()
                    os.remove(cwd+file_name) if os.path.exists(cwd+file_name) else None
    except urllib.error.HTTPError as e:
        print("failed "+ str(item))
        # print('HTTPError: {}'.format(e.code))
        continue
    except urllib.error.URLError as e:
        print("failed "+ str(item))
        # print('URLError: {}'.format(e.reason))
        continue