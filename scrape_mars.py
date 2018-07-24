
# coding: utf-8

# In[1]:


# Dependencies
from bs4 import BeautifulSoup
import requests
import pymongo
from splinter import Browser
import tweepy
import time
import pandas as pd
import json

def Scrape():

    print("COMMENCING SCRAPE")
    print("----------------------------------")

    # Empty dictionary
    mars_dict = {}

    url = "https://mars.nasa.gov/news/"


    # In[3]:


    #Request module to retrieve page
    html = requests.get(url)


    # In[4]:


    #Create BS object to parse with html.parser
    soup = BeautifulSoup(html.text, 'html.parser')


    # In[5]:


    # Retrieve title
    news_title_section = soup.find('div', 'content_title', 'a').text
    news_p_section = soup.find('div', 'rollover_description_inner').text


    # Adding to Dict
    mars_dict["news_title"] = news_title_section
    mars_dict["news_p"] = news_p_section


    #Print Results

    print(news_title_section)
    print(news_p_section)


    # In[7]:


    url_images = "https://www.jpl.nasa.gov/spaceimages/?search=&category=Mars"


    # In[8]:


    executable_path = {'executable_path': 'chromedriver.exe'}
    browser = Browser('chrome', **executable_path)
    browser.visit(url_images)

    # Click the 'Next' button on each page
    browser.click_link_by_partial_text('FULL IMAGE')


    # In[9]:


    for x in range(5):
        # HTML object
        html_image = browser.html
        # Parse HTML with Beautiful Soup
        soup = BeautifulSoup(html_image, 'html.parser')
        link = "https://www.jpl.nasa.gov"
        feat_img = soup.find('img', class_='fancybox-image')['src']
        featured_img_url = link + feat_img
    featured_img_url

    import requests
    import shutil
    response = requests.get(featured_img_url, stream=True)
    with open('img.jpg', 'wb') as out_file:
        shutil.copyfileobj(response.raw, out_file)
        
    # Display the image with IPython.display
    from IPython.display import Image
    Image(url='img.jpg')

    mars_dict["featured_image_url"] = featured_img_url

    # In[10]:


    url_weather = "https://twitter.com/marswxreport?lang=en"
    browser.visit(url_weather)


    # In[11]:


    html_weather = browser.html
    soup = BeautifulSoup(html_weather, "html.parser")
    mars_weather = soup.find("p", class_="TweetTextSize TweetTextSize--normal js-tweet-text tweet-text").text
    print(f"mars_weather = {mars_weather}")

    mars_dict["mars_weather"] = mars_weather

    # ## Mars Facts

    # In[12]:


    url_facts = "https://space-facts.com/mars/"


    # In[13]:


    table = pd.read_html(url_facts)
    table[0]


    # In[14]:


    df_mars_facts = table[0]
    df_mars_facts.columns = ["Parameter", "Values"]
    df_mars_facts.set_index(["Parameter"])


    # In[15]:


    mars_html_table = df_mars_facts.to_html()
    mars_html_table = mars_html_table.replace("\n", "")
    mars_html_table


    mars_dict["mars_html_table"] = mars_html_table
    # ## Mars Hemispheres

    # In[20]:


    url_hemisphere = "https://astrogeology.usgs.gov/search/results?q=hemisphere+enhanced&k1=target&v1=Mars"
    browser.visit(url_hemisphere)


    # In[21]:


    hemi_html = browser.html                        
    hemi_soup = BeautifulSoup(hemi_html, 'html.parser') 


    # In[22]:


    hemisphere_image_urls = []                                          

    products = hemi_soup.find('div', class_='result-list')              
    hemispheres = products.find_all('div', class_='item')           

    for hemisphere in hemispheres:                              
        title = hemisphere.find('div', class_='description')
        
        title_text = title.a.text                                           
        title_text = title_text.replace(' Enhanced', '')
        browser.click_link_by_partial_text(title_text)      
        
        hemi_html = browser.html                            
        hemi_soup = BeautifulSoup(hemi_html, 'html.parser')                 
        
        image = hemi_soup.find('div', class_='downloads').find('ul').find('li')
        img_url = image.a['href']
        
        hemisphere_image_urls.append({'title': title_text, 'img_url': img_url})
        
        browser.click_link_by_partial_text('Back')
    hemisphere_image_urls   

    mars_dict["hemisphere_image_urls"] = hemisphere_image_urls
  
    return mars_dict

