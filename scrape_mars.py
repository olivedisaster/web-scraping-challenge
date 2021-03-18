from os import link
import pandas as pd
import requests
from bs4 import BeautifulSoup as bs
import pymongo
from splinter import Browser

# Browser


def init_browser():
    executable_path = {
        'executable_path': 'C:/Program Files/chromedriver_win32/chromedriver.exe'}
    return Browser('chrome', **executable_path, headless=False)


mars_info_dict = {}


def scrape_info():
    browser = init_browser()

# Mars News

    news_url = 'https://mars.nasa.gov/news/'
    browser.visit(news_url)
    html = browser.html
    soup = bs(html, 'html.parser')

    title = soup.find('div', class_="content_title")
    title_text = title.a.text
    title_text = title_text.strip()
    news_p = soup.find("div", class_="article_teaser_body")
    news_text = news_p.text
    news_text = news_text.strip()

    # Featured Photo

    featured_url = "https://www.jpl.nasa.gov/spaceimages/?search=&category=Mars"
    browser.visit(featured_url)
    img_html = browser.html
    img_soup = bs(img_html, 'html.parser')

    img_featured = img_soup.find("ul", class_="articles")
    href = results.find("a", class_='fancybox')['data-fancybox-href']
    img_url_main = 'https://www.jpl.nasa.gov' + href

    featured_img_url = img_url_main + img_featured

    mars_info_dict["featured_img_url"] = featured_img_url

    # Mars Facts

    mars_url = 'https://space-facts.com/mars/'
    facts_table = pd.read_html(mars_url)
    facts_df = facts_table[0]
    facts_df.columns = ["Description", "Value"]
    facts_df = facts_df.set_index("Description")
    facts_html = facts_df.to_html()

    # Mars Hemispheres

    hemispheres_img_urls = []

    hemispheres_url = "https://astrogeology.usgs.gov/search/results?q=hemisphere+enhanced&k1=target&v1=Mars"
    browser.visit(hemispheres_url)

    hemispheres_html = browser.html
    hemispheres_soup = bs(hemispheres_html, 'html.parser')

    hemispheres = hemispheres_soup.find_all('div', class_='item')

    for h in hemispheres:
	    title = h.find("h3").text
        hem_img = h.find("a", class_="itemLink product-item")["href"]
        browser.visit(hemispheres_url + hem_img)
        
          
        hem_results = hemispheres_soup.find('img', class_='wide-image')
        hemispheres_url = 'https://astrogeology.usgs.gov/' + hem_results["src"]

        hemispheres_img_urls = []

        hemispheres_img_urls.append({"title":link, "img_url":hemispheres_url})
             


        mars_info_dict["hemispheres_info"] = hemispheres_img_urls

        return mars_info_dict
            
