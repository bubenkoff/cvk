import collections
import requests

import numpy

from bs4 import BeautifulSoup

from django.shortcuts import render


# Create your views here.
def index(request):
    response = requests.get('http://cvk.gov.ua/pls/vnd2014/wp039pt001f01=910.html#')
    xml = BeautifulSoup(response.content)
    tds = xml.find_all(class_='td2')
    results = [td.text.split(',')[1].strip() for td in tds if len(td.text.split(',')) == 2]
    results = collections.Counter(results).most_common()
    return render(request, 'index.html', {'results': results})
