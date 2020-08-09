from urllib.parse import quote_plus
import requests

from . import models
from django.shortcuts import render
from bs4 import BeautifulSoup
from bs4.element import Tag

BASE_URL = "https://losangeles.craigslist.org/search/hhh?query={}"
IMAGE_URL = "https://images.craigslist.org/{}_300x300.jpg"


# Create your views here.
def home(request):
    return render(request, 'base.html')


def new_search(request):
    search = request.POST.get('search')

    models.Search.objects.create(search="khatri")

    final_url = BASE_URL.format(search)
    response = requests.get(final_url)

    data = response.text
    soup = BeautifulSoup(data, features='html.parser')

    post_listings = soup.find_all('li', {'class': 'result-row'})

    final_posting = []

    for post in post_listings:
        post_title = post.find(class_='result-title').text
        post_url = post.find('a').get('href')

        if post.find(class_='result-image').get('data-ids'):
            post_image_id = post.find(class_='result-image').get('data-ids').split(',')[0].split(':')[1]
            post_image_url = IMAGE_URL.format(post_image_id)
        else:
            post_image_url = "https://craigslist.org/images/peace.jpg"

        #print(post_image_url)

        if post.find(class_='result-price'):
            post_price = post.find(class_='result-price').text
        else:
            post_price = 'N/A'

        final_posting.append(((post_title, post_url, post_price, post_image_url)))

    search_content = {
        'search': search,
        'final_posting': final_posting
    }
    return render(request, 'my_app/new_search.html', search_content)
