"""Results views."""

import collections
import requests
import math

from bs4 import BeautifulSoup

from django.views.decorators.cache import cache_page
from django.shortcuts import render


# Create your views here.

@cache_page(60 * 10)
def index(request):
    response = requests.get('http://cvk.gov.ua/pls/vnd2014/wp039pt001f01=910.html#', timeout=600)
    # response = requests.get('http://localhost:5000/static/cvk.html')
    xml = BeautifulSoup(response.content)
    tds = xml.find_all(class_='td2')
    majorital = [td.text.split(',')[1].strip() for td in tds if len(td.text.split(',')) == 2]
    majorital = collections.Counter(majorital).most_common()

    response = requests.get('http://cvk.gov.ua/pls/vnd2014/wp510pt001f01=910.html', timeout=600)
    # response = requests.get('http://localhost:5000/static/cvk2.html')
    xml = BeautifulSoup(response.content)
    tds = xml.find_all(class_='tdbarv')
    proportional = [float(td.text.strip()[:-2]) + 5 for td in tds]
    titles = [title.text.strip() for title in xml.find_all('table', class_='t1')[-2].find_all(class_='td2')]
    proportional = [(title, math.floor(225 * res / 100)) for title, res in zip(titles, proportional)]
    dict_proportional = dict(proportional)
    cumulative = sorted(
        ((name, percent + dict_proportional.get(name, 0))for name, percent in dict(majorital).items()),
        key=lambda x: x[1], reverse=True)
    return render(request, 'index.html', {
        'proportional': proportional, 'majorital': majorital, 'cumulative': cumulative})
