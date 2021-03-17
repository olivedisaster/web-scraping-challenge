import pandas as pd
import requests
from bs4 import BeautifulSoup as bs
import pymongo
from splinter import Browser

#Browser
def init_browser():
    executable_path = {'executable_path': 'C:/Program Files/chromedriver_win32/chromedriver.exe'}
    return Browser('chrome', **executable_path, headless=False)

def scrape():
    browser = init_browser()

    #Mars News
    url = 'https://mars.nasa.gov/news/'
    browser.visit(url)
    html = browser.html
    soup = bs(html, 'lxml')

    title = soup.find('div', class_="content_title")
    title_text = title.a.text
    title_text = title_text.strip()
    news_p = soup.find("div", class_="rollover_description_inner")
    news_text = news_p.text
    news_text = news_text.strip()

    #Featured Photo
    url2 = "https://www.jpl.nasa.gov/spaceimages/?search=&category=Mars"
    browser.visit(url2)
    html2 = browser.html
    soup2 = bs(html2, 'html.parser')

    results = soup2.find("ul", class_="articles")
    href = results.find("a",class_='fancybox')['data-fancybox-href']
    featured_image_url = 'https://www.jpl.nasa.gov' + href

    #Mars Weather
    url3 = 'https://twitter.com/marswxreport?lang=en'
    browser.visit(url3)
    html3 = browser.html
    soup3 = bs(html3, 'html.parser')

    results2 = soup3.find('div', class_="js-tweet-text-container")
    tweet = results2.find("p", class_="TweetTextSize TweetTextSize--normal js-tweet-text tweet-text").text
    tweet_split = tweet.rsplit("pic")
    mars_weather = tweet_split[0]

    #Mars Facts
    url4 = 'https://space-facts.com/mars/'
    facts_table = pd.read_html(url4)
    facts_df = facts_table[0]
    facts_df.columns = ["Description", "Value"]
    facts_df = facts_df.set_index("Description")
    facts_html = facts_df.to_html()

    #Mars Hemispheres
    url5 = "https://astrogeology.usgs.gov/search/results?q=hemisphere+enhanced&k1=target&v1=Mars"
    browser.visit(url5)
    html4 = browser.html
    soup4 = bs(html4, 'html.parser')

    titles = soup4.find_all("h3")
    for title in titles:
        browser.click_link_by_partial_text("Hemisphere")

    results4 = soup4.find_all("div", class_="description")
    mars_dict={}
    hemisphere_image_urls=[]
    for result in results4:
        link = result.find('a')
        img_href = link['href']
        title_img = link.find('h3').text
        url6 = "https://astrogeology.usgs.gov" + img_href
        browser.visit(url6)
        html5 = browser.html
        soup5 = bs(html5, 'html.parser')
        pic = soup5.find("a", target="_blank")
        pic_href = pic['href']
        hemisphere_image_urls.append({"title":title_img,"img_url":pic_href})

    #Dictionary of all Mars Info Scraped
    mars_info_dict = {"news_title":title_text,"news_text":news_text,"featured_image":featured_image_url,
    "mars_weather":mars_weather,"facts_table":facts_html,"hemisphere_img":hemisphere_image_urls}

    browser.quit()

    return mars_info_dict