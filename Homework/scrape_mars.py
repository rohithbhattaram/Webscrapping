from splinter import Browser
from bs4 import BeautifulSoup
import pandas as pd
import datetime as dt
import time 
import random


def scrape_all():

    try : 
        # Initiate headless driver for deployment
        browser = Browser("chrome", executable_path="chromedriver", headless=True)
        x=random.randint(1,4)
        news_title,href_link, news_paragraph = nasa_articles(browser)
        a=news_title[x]
        b=news_paragraph[x]
        c=nasa_images(browser)[x]
        d=mars_hemispheres(browser)
        e=mars_twitter(browser)[x]
        f=mars_info_table(browser)
        g=dt.datetime.now()

        print(a)
        print(b)
        print(c)
        print(d)
        print(e)
        print(f)
        print(g)
        print("Random Number"+str(x))
        # Run all scraping functions and store in dictionary.
    except  Exception as T: 
        print(T)
    except  BaseException as T: 
        print(T)

    

    data = {
            "news_title": a,
            "news_paragraph": b,
            "featured_image": c,
            "hemispheres": d,
            "weather": e,
            "facts": f,
            "last_modified": g
    }

    # Stop webdriver and return data
    browser.quit()
    return data


def nasa_articles(browser):
    url ='https://mars.nasa.gov/news/?page=0&per_page=40&order=publish_date+desc%2Ccreated_at+desc&search=&category=19%2C165%2C184%2C204&blank_scope=Latest'
    browser.visit(url)
    news_title = []
    href_link =[]
    news_p = []
    for x in range(10):
        # HTML object
        html = browser.html
        # Parse HTML with Beautiful Soup
        soup = BeautifulSoup(html, 'lxml')
    #   list_footer more_button
        buttons = browser.find_link_by_text('More')
        buttons_length = len(buttons)
        buttons[1].click()
    # Retrieve all elements that contain book information
    articles = soup.find('ul', class_='item_list')
    # Iterate through each book
    for article in articles:
        # Use Beautiful Soup's find() method to navigate and retrieve attributes
        title = article.find("div", {"class" : "content_title"}).find('a').get_text()
        href = article.find("div", {"class" : "content_title"}).a['href']
        teaser = article.find("div", {"class" : "article_teaser_body"}).get_text()
        news_title.append(title)
        href_link.append(href)
        news_p.append(teaser)
        
    return news_title,href_link,news_p


    
def nasa_images(browser):
    url ='https://www.jpl.nasa.gov/spaceimages/?search=&category=Mars'
    browser.visit(url)
    featured_image_url=[]

    for y in range(4) : # HTML object
        try:
            html = browser.html
            soup = BeautifulSoup(html, 'lxml')
            x = soup.find("div", {"class" : "more_button"}).find('a').get_text()
            browser.click_link_by_text(x)
            links = soup.find_all("a",{"class":"fancybox"})
            time.sleep(3)
        except AttributeError:
            print("Error..")


    for link in links : 
        href = link.get('data-fancybox-href')
        y ="https://www.jpl.nasa.gov"+str(href)
        featured_image_url.append(y)
    return featured_image_url




def mars_twitter(browser):
    url ='https://twitter.com/marswxreport?lang=en'
    browser.visit(url)
    mars_tweets=[]
    tweets = " "
    time.sleep(2)
    for y in range(5) : # HTML object
            html = browser.html
            soup = BeautifulSoup(html, 'lxml')
            browser.execute_script("window.scrollTo(0, document.body.scrollHeight);")
            time.sleep(2)
            tweets = soup.find_all("li", {"class" : "js-stream-item stream-item stream-item "})


    for tweet in tweets : 
        x= tweet. find("div", {"class" : "content"}).find('p').get_text()
        mars_tweets.append(x)


    return mars_tweets


def mars_hemispheres(browser) : 

    base_url='https://astrogeology.usgs.gov/search/results?q=hemisphere+enhanced&k1=target&v1=Mars'
    url=base_url

    browser.visit(url)
    hemisphere_info= []


    def read_base_page():
        links = browser.find_by_css("a.product-item h3")
        return links 

    links = read_base_page()

    def read_html():
        html = browser.html
        soup = BeautifulSoup(html, 'lxml')
        return soup



    for x in range(len(links)) : 
        hemisphere = {}
        links= read_base_page()
        links[x].click()
        soup = read_html()
        title = soup.find("h2", {"class" : "title"}).get_text()
        href = soup.find("div", {"class" : "downloads"}).a['href']
        hemisphere['img_url'] = href
        hemisphere['title']= title 
        hemisphere_info.append(hemisphere)
        browser.back()
        time.sleep(2)

    return hemisphere_info


def mars_info_table(browser):
    column_name=[]
    column_value =[]

    url ='https://space-facts.com/mars/'
    browser.visit(url)
    time.sleep(2)
    html = browser.html
    soup = BeautifulSoup(html, 'lxml')  
    table = soup.find("table", { "class" : "tablepress tablepress-id-mars" }).findAll("tr")
    for row in table:
        column_name.append(row.find("td", { "class" : "column-1" }).get_text())
        column_value.append(row.find("td", { "class" : "column-2" }).get_text())


    mars_info_df = pd.DataFrame({'Category' : column_name,
                                    'Value' : column_value, }, 
                                    columns=['Category','Value'])


    return mars_info_df.to_html(classes="table table-striped")



if __name__ == "__main__":

    # If running as script, print scraped data
    scrape_all()
