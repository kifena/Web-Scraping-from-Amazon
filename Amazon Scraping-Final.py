#!/usr/bin/env python
# coding: utf-8

# In[8]:


import pandas as pd
from bs4 import BeautifulSoup 
from selenium import webdriver
import lxml
import lxml.html.soupparser
import re
import requests
import json
import random


# In[9]:


# identifying the variables
products = []
headers = {
        'accept-encoding': 'gzip, deflate, sdch, br',
        'accept-language': 'en-US,en;q=0.8,zh-CN;q=0.6,zh;q=0.4',
        'upgrade-insecure-requests': '1',
        'user-agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/56.0.2924.87 Safari/537.36',
        'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
        'cache-control': 'max-age=0',
    }
base_url = "https://www.amazon.com/s?k="


# In[10]:


# function to gather the links to the products' pages
def linkc(item):
    # put together the url to scrape from
    url = base_url + item
    # uncomment to watch the progress
    #print('begin scraping the data', url)
    
    # get the page data
    request = requests.get(url, headers=headers)
    soup = BeautifulSoup(request.text, 'lxml')
    body = soup.find('body')
    main_outlet = body.find('div',{'class':"s-main-slot s-result-list s-search-results sg-row"})
    links = main_outlet.find_all('a',{'class':'a-link-normal a-text-normal'})
    # get the links to pages
    for i in links:
        products.append('https://www.amazon.com' + i.get('href'))


# In[11]:


# lists to store the data
prices = []
review_nums = []
review_scores = []
stock = []
titles = []
imgs = []
k = 1
def pagec(products,prices,review_nums,review_scores,stock,titles,imgs,k):
    # begin scraping
    for page in products:
        # uncomment to watch the progress
        #print('begin scrapping the product page: ', page)
        #print('page number',k,'--- left:',len(products)-k)
        
        k = k + 1

        # get the page
        request = requests.get(page, headers=headers)
        soup1 = BeautifulSoup(request.text, 'lxml')

        # get the title of the item
        titles.append(soup1.find(id='productTitle').get_text().strip())

        # get the price
        try:
            prices.append(float(soup1.find('span',{'id':re.compile('^priceblock_')}).get_text().replace('$', '').replace(',', '.').strip()))
        except:
            try:
                prices.append(float(soup1.find('span',{'class':re.compile('^price')}).get_text().replace('$', '').replace(',', '.').strip()))
            except:
                prices.append('')

        # review score
        review_scores.append(float(soup1.find('span',{'class':'a-icon-alt'}).get_text().strip()[:3]))

        # how many reviews
        review_nums.append(int(soup1.select('#acrCustomerReviewText')[0].get_text().split(' ')[0].replace(".", "").replace(",","")))

        # whether it is available
        try:
            soup1.select('#availability .a-color-state')[0].get_text().strip()
            stock.append('Out of Stock')
        except:
            stock.append('Available')

         # get the link to the source image
        try:
            imgs.append(soup1.find('img',{'alt':titles[-1]}).get('data-old-hires').strip())
        except:
            imgs.append('')


# In[ ]:


# get the input
item = input()
# lowercase the input and format it
item = item.lower().strip().replace(' ','+')

# run the functions
linkc(item)
pagec(products,prices,review_nums,review_scores,stock,titles,imgs,k)

# json output
jj = json.dumps({'title':titles,'price':prices,'availability':stock,'score':review_scores,'number of reviews':review_nums,'image':imgs},indent=4)
print(jj)


# In[ ]:




