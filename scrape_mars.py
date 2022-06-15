# Automates browser actions
from splinter import Browser, browser

# Parses the HTML
from bs4 import BeautifulSoup as soup
import pandas as pd
import datetime as dt
# For scraping with Chrome
from webdriver_manager.chrome import ChromeDriverManager

# Headless driver initiation for deployment and Scrape ALL
def scrape_all():
    # Setup splinter
    # browser = init_browser()
    executable_path = {'executable_path': ChromeDriverManager().install()}
    browser = Browser('chrome', **executable_path, headless=False)

    # Set an empty dict for listings that we can save to Mongo// Automating our browser
    news_title, mars_p = mars_news(browser)
    # featured_image_url = mars_hemis(browser)
    # Running all scraping function to store the results in the dicitonary
    data = {
        'news_title' : news_title,
        'news_paragraph' : mars_p,
        'featured_image' : featured_image(browser),
        'facts' : mars_facts(),
        'hemispheres' : mars_hemis(browser),
        'last_modified' : dt.datetime.now()
    }
    browser.quit()
    return data
    #Stopping the webdriver and returning the data. 

#------------------- Mars News Section -------------------
# Scraping Mars News, visting the NASA Mars website. 
def mars_news(browser):
    url = 'https://mars.nasa.gov/news/'
    browser.visit(url)
    # Delay for loading the page
    browser.is_element_present_by_css('div.list_text', wait_time=1)
    # Converting the browser to soup object
    html = browser.html
    news_soup = soup(html, 'html.parser')
    # Error handling with try/except
    try:
        slide_elem = news_soup.select_one('div.list_text')
        news_title = slide_elem.find('div', class_='content_title').get_text()
        mars_p = slide_elem.find('div', class_='article_teaser_body').get_text()

    except AttributeError:
        return None, None

    return news_title, mars_p

#----------------- Mars Image Section ---------------------
# Scraping Mars Image wbsite and visiting url 
def featured_image(browser):
    url = 'https://spaceimages-mars.com'
    browser.visit(url)
    # Finding and click the Full Image Button
    full_image_elem = browser.find_by_tag('button')[1]
    full_image_elem.click()
    # Parsing the HTML with Soup
    html = browser.html
    img_soup = soup(html, 'html.parser')
    # Error handling with try/except
    try:
        relative_img_url = img_soup.find('img', class_='fancybox-image').get('src')
    except AttributeError:
        return None 
    # USing the base URL to create an absolute URL 
    featured_img_url = f'https://spaceimages-mars.com/{relative_img_url}'
    return featured_img_url

#---------------- Mars Facts Section ---------------------
def mars_facts():
    # Error handling with try/except, read_html scrapes facts table
    try:
        df = pd.read_html('https://galaxyfacts-mars.com')[0]
    except BaseException:
        return None
    # Setting the column names and index
    df.columns = ['Description','Mars','Earth']
    df.set_index('Description', inplace=True)
    # Dataframe to HTML format and bootstrapping 
    return df.to_html(classes=["table-bordered", "table-striped"])

# ---------------- Mars Hemisphere Section ----------------  
def mars_hemis(browser):
    # Visit URL using browser
    url = 'https://marshemispheres.com/'
    browser.visit(url)
    # Creating empty list to hold titles then looping through each hemisphere link
    hemisphere_urls = []
    for hemis in range(4):
        browser.links.find_by_partial_text('Hemisphere')[hemis].click()
        html = browser.html
        hemi_soup = soup(html, 'html.parser')
        title = hemi_soup.find('h2', class_='title').text
        img_url = hemi_soup.find('li').a.get('href')
        hemispheres = {}
        hemispheres['img_url'] = f'https://marshemispheres.com/{img_url}'
        hemispheres['title'] = title
        hemisphere_urls.append(hemispheres)
        browser.back()
    return hemisphere_urls
    #printing hemisphere_urls
if __name__ == "__main__":
# If running as script, print scraped data
    print(scrape_all())    
