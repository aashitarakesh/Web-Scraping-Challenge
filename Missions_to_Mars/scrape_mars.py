# Dependencies
from bs4 import BeautifulSoup
import requests
import os
from splinter import Browser
from webdriver_manager.chrome import ChromeDriverManager
import pandas as pd

def scrape():
    # Setup splinter
    executable_path = {'executable_path': ChromeDriverManager().install()}
    browser = Browser('chrome', **executable_path, headless=False)

##########################
#  NASA Mars News
##########################

    # Visit the NASA Mars News Site
    url = 'https://mars.nasa.gov/news/'
    browser.visit(url)
    # Parse HTML with Beautiful Soup
    html = browser.html
    soup = BeautifulSoup(html, 'html.parser')
    # Extract the latest news title and paragraph text and assign to variables
    news_title = soup.find('div', class_='list_text').find('a').text
    news_paragraph = soup.find('div', class_='article_teaser_body').text
    # print(f'Title: {news_title} \nText: {news_paragraph}')

#########################################
# JPL Mars Space Images - Featured Image
#########################################
    # Visit JPL Mars Space Images
    jurl = 'https://data-class-jpl-space.s3.amazonaws.com/JPL_Space/index.html'
    browser.visit(jurl)
    # Parse HTML with Beautiful Soup
    html = browser.html
    image_soup = BeautifulSoup(html, 'html.parser')
    # Scrape image URL
    image_url = image_soup.find('img', class_='headerimage').get("src")

    # Use Base URL to Create Complete URL
    featured_image_url = f'https://data-class-jpl-space.s3.amazonaws.com/JPL_Space/{image_url}'
    # print(featured_image_url)

##########################
#  Mars Facts
##########################
    # Visit Mars webpage
    facts_url ='https://space-facts.com/mars/'
    tables = pd.read_html(facts_url)

    # Required table stored at index 0
    mars_df = tables[0]

    # Rename columns
    mars_df.columns = ['Attribute', 'Value']

    # Convert Dataframe to HTML table string.
    mars_table = mars_df.to_html(index=False)

#########################################
# Mars Hemispheres
#########################################
    
    # Visit the USGS Astrogeology site
    astr_url ='https://astrogeology.usgs.gov/search/results?q=hemisphere+enhanced&k1=target&v1=Mars'
    browser.visit(astr_url)

    # Parse HTML with Beautiful Soup
    html = browser.html
    astr_soup = BeautifulSoup(html, 'html.parser')

    # Hemisphere title containing the hemisphere name
    titles = astr_soup.find_all('h3')
    for title in titles:
        browser.links.find_by_partial_text('Hemisphere')

    results = astr_soup.find_all('div', class_='description')
    hemisphere_image_urls=[]
    for result in results:
        link = result.find('a')
        href = link['href']
        title = link.find('h3').text
    
       # Find the image url to the full resolution image.
        image_url = 'https://astrogeology.usgs.gov' + href
        browser.visit(image_url)
    
      # Parse HTML with Beautiful Soup
        html = browser.html
        new_soup = BeautifulSoup(html, 'html.parser')
    
        img_link = new_soup.find('div', class_= 'downloads')('li')[1]
        img_href = img_link.find('a')['href']
    
        #Append the dictionary with the image url string and the hemisphere title to a list
        hemisphere_image_urls.append({"title":title,"img_url":img_href})

        # Store data in a dictionary
        mars_data = {
             "news_title":news_title,
             "text":news_paragraph,
             "featured_image":featured_image_url,
             "mars_table":mars_table,
             "hemisphere_img":hemisphere_image_urls
             }

    # Close the browser after scraping
    browser.quit()
    # Return results
    return mars_data



 