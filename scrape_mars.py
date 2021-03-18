from os import link
import pandas as pd
import requests
from bs4 import BeautifulSoup as bs
import pymongo
from splinter import Browser

# Browser


def init_browser():
    executable_path = {'executable_path': '/Users/buckleyweglarz/Downloads/chromedriver'}
    return Browser('chrome', **executable_path, headless=False)


mars_info_dict = {}


def scrape_info():
    browser = init_browser()
    news_url = 'https://mars.nasa.gov/news/'
    browser.visit(news_url)
    html = browser.html
    soup = bs(html, 'html.parser')
    title = soup.find("ul", class_="item_list")
    first_item = title.find("li", class_="slide")
    news_title = first_item.find("div", class_="content_title").text
    news_p = soup.find("div", class_="article_teaser_body").text
    mars_info_dict["news_title"] = news_title
    mars_info_dict["paragraph"] = news_p
    # Featured Photo
    featured_url = "https://www.jpl.nasa.gov/spaceimages/?search=&category=Mars"
    browser.visit(featured_url)
    img_html = browser.html
    img_soup = bs(img_html, 'html.parser')
    # img_featured = img_soup.find('div',class_='carousel_container').article.footer.a['data-fancybox-href']
    link = "https:"+soup.find('div', class_='jpl_logo').a['href'].rstrip('/')
    img_url_main = link
    mars_info_dict["featured_img_url"] = featured_img_url
    # Mars Facts
    mars_url = 'https://space-facts.com/mars/'
    facts_table = pd.read_html(mars_url)
    facts_df = facts_table[0]
    facts_df.columns = ["Description", "Value"]
    facts_df = facts_df.set_index("Description")
    facts_html = facts_df.to_html()
    mars_info_dict["mars_table"] = mars_html_table
    # Mars Hemispheres
    hemispheres_img_urls = []
    hemispheres_url = "https://astrogeology.usgs.gov/search/results?q=hemisphere+enhanced&k1=target&v1=Mars"
    browser.visit(hemispheres_url)
    hemispheres_html = browser.html
    time.sleep(1)
    links = browser.find_by_css("a.product-item h3")
    for item in range(len(links)):
        hemisphere = {}
        browser.find_by_css("a.product-item h3")[item].click()
        time.sleep(1)
        hemisphere["title"] = browser.find_by_css("h2.title").text
        sample_element = browser.links.find_by_text("Sample").first
        hemisphere["img_url"] = sample_element["href"]
        hemisphere_img_urls.append(hemisphere)
        browser.back()
    mars_info_dict["hemisphere_imgs"] = hemisphere_img_urls
    browser.quit()
    return mars_info_dict





