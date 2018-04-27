import pandas as pd
from splinter import Browser
from bs4 import BeautifulSoup
import requests
import numpy as np
import time
import json

def scrape():
    # mars news
    scraped_data = []
    executable_path = {'executable_path': 'chromedriver.exe'}
    browser = Browser('chrome', **executable_path, headless = False)
    nasa_url = 'https://mars.nasa.gov/news/'
    browser.visit(nasa_url)
    time.sleep(10)
    nasa_html = browser.html
    nasa_soup = BeautifulSoup(nasa_html, 'html.parser')
    headlines = nasa_soup.find_all('div', class_='content_title')
    news_title = headlines[0].find('a').text
    paragraph = nasa_soup.find_all('div', class_="article_teaser_body")
    news_p = paragraph[0].text
    # print (news_title)
    # print (news_p)
    latest_news = {"latest_news": {"news_title": news_title, "news_paragraph": news_p}}
    scraped_data.append(latest_news)

    # mars image

    jpl_url = "https://www.jpl.nasa.gov/spaceimages/?search=&category=Mars"
    jpl_html = requests.get(jpl_url)
    jpl_soup = BeautifulSoup(jpl_html.content, 'html.parser')
    jpl_image = jpl_soup.find('article', class_='carousel_item').get("style")
    jpl_image_url = jpl_image.replace("background-image: url('", "https://www.jpl.nasa.gov/")
    featured_image_url = jpl_image_url.replace("');","")
    # print (featured_image_url)
    featured_image_dict = {"featured_image": featured_image_url}
    scraped_data.append(featured_image_dict)
    # mars weather
    twitter_url = "https://twitter.com/marswxreport"
    twitter_html = requests.get(twitter_url)
    twitter_soup = BeautifulSoup(twitter_html.content, 'html.parser')
    tweets = twitter_soup.find_all("p", class_="TweetTextSize TweetTextSize--normal js-tweet-text tweet-text")
    mars_weather = tweets[0].text
    # print (mars_weather)
    weather_dict = {"weather": mars_weather}
    scraped_data.append(weather_dict)
    # mars facts
    fact_url = "http://space-facts.com/mars/"
    fact_html = requests.get(fact_url)
    fact_soup = BeautifulSoup(fact_html.content, 'html.parser')
    fact_category = fact_soup.find_all("td", class_="column-1")
    fact_actual = fact_soup.find_all("td", class_="column-2")
    category_list = []
    for category in fact_category:
        c = category.text
        c = c.replace(":","")
        category_list.append(c)
    fact_list = []
    for fact in fact_actual:
        f = fact.text
        fact_list.append(f)
    mars_df = pd.DataFrame({"description": category_list, "fact":fact_list})
    mars_df = mars_df.set_index('description')
    mars_facts = mars_df.to_dict()
    scraped_data.append(mars_facts)
    # mars hemispheres
    astro_base = "https://astrogeology.usgs.gov"
    hemisphere_search = "/search/results?q=hemisphere+enhanced&k1=target&v1=Mars"
    h_url = astro_base + hemisphere_search
    h_html = requests.get(h_url)
    h_soup = BeautifulSoup(h_html.content, 'html.parser')
    h_a = h_soup.find_all("a", class_="itemLink product-item")
    links = []
    for a in h_a:
        h_href = a['href']
        hemisphere_url = astro_base + h_href
        links.append(hemisphere_url)
    #   Mars Hemisperes
    astro_base = "https://astrogeology.usgs.gov"
    hemisphere_search = "/search/results?q=hemisphere+enhanced&k1=target&v1=Mars"
    h_url = astro_base + hemisphere_search
    h_html = requests.get(h_url)
    h_soup = BeautifulSoup(h_html.content, 'html.parser')
    h_a = h_soup.find_all("a", class_="itemLink product-item")
    # print (h_a)
    links = []
    for a in h_a:
        h_href = a['href']
        hemisphere_url = astro_base + h_href
        links.append(hemisphere_url)
    # print (links)
    hemisphere_dictionary = []
    h_name = []
    h_img = []
    h_list = []
    for z in np.arange(len(links)):
        l_html = requests.get(links[z])
        l_soup = BeautifulSoup(l_html.content, 'html.parser')
        l_li = l_soup.find_all("a")
        for aa in l_li:
            aa_href = aa.get('href')
            if aa_href[-3:] == "jpg":
                h_jpg = aa_href
        l_heading = l_soup.find("h2", class_ = "title")
        name = l_heading.text
        name = name.replace(" Enhanced","")
        h_name.append(name)
        h_img.append(h_jpg)
    h_df = pd.DataFrame({'title': h_name, 'img_url': h_img})
    h_df = h_df.set_index('title')
    h_dict = h_df.to_dict()
    # print (h_dict)
    scraped_data.append(h_dict)

    # print (json.dumps(scraped_data, indent=3))
    return scraped_data