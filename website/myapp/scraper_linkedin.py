import re
import csv
from getpass import getpass
import time
from time import sleep
import random
from selenium.webdriver.common.keys import Keys
from selenium.common.exceptions import NoSuchElementException, ElementClickInterceptedException
#from msedge.selenium_tools import Edge, EdgeOptions
import random
#pip install webdriver-manager
from selenium import webdriver
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.common.exceptions import TimeoutException, StaleElementReferenceException

from selenium.webdriver.common.by import By
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities

import pandas as pd
#print(ChromeDriverManager().install()) #checker la version de chromedriver

#driver = webdriver.Chrome(ChromeDriverManager().install()) 



# DOCKER MODE - Set up the remote WebDriver
options = webdriver.ChromeOptions()
options.set_capability('timeouts', {
    #'implicit': 10000,
    #'pageLoad': 30000,
    #'script': 30000
}) 

options.add_argument('--no-sandbox')
options.add_argument('--disable-dev-shm-usage')
#options.add_argument('--disable-gpu')
#options.add_argument('--headless')  # Remove if you need to see the browser

options.add_argument("--disable-blink-features=AutomationControlled")
options.add_experimental_option("excludeSwitches", ["enable-automation"])
options.add_experimental_option('useAutomationExtension', False)

class WebDriver:
    def __init__(self, options):
        self.driver = webdriver.Remote(
            #command_executor="https://standalone-chrome-flcy.onrender.com/wd/hub",
            #following works when local
            #command_executor="http://selenium:4444/wd/hub",
            
            #works:
            command_executor="https://selenium-954459957107.europe-west1.run.app/wd/hub",
            #command_executor="https://selenium-954459957107.europe-west1.run.app:4444/wd/hub",
            #command_executor="http://host.docker.internal:4444/wd/hub",
            options = options
        )
        #self.driver.set_window_size(1500, 1000)
        #sleep(15)
    def close(self):
        self.driver.quit()

#NO DOCKER MODE
#driver = webdriver.Chrome("D:\Media Scraper\chromedriver-win32(works)\chromedriver.exe")
#driver.set_window_size(1500, 1000)

def human_like_delay(min_seconds=1, max_seconds=3):
    sleep(random.uniform(min_seconds, max_seconds))


def run_script():
    print("RUNNING TEST")
    #driver.find_element_by_xpath('//button[@aria-label="Posts"]').click()
    #df_raw = scrape_linkedin("ingénieur")
    #header=['Username','Job','Date','Texte','Nb_reactions','Nb_commentaires','Nb_partages','Commentaires','Mot cle recherché']
    #df = pd.DataFrame(df_raw,columns=header)
    #df.head()

def scrape_linkedin(keywords):
    driver = WebDriver(options).driver
    
    if ('linkedin' not in str(driver.current_url)):
        connection(driver) 
    #one_search(keywords, driver)
    keywords_array = []
    keywords_array.append(keywords)
    df_raw = Scrape_Linkedin(keywords_array, driver)
    header=['Username','Job','Date','Text','Number of reactions','Number of comments','Number of shares','Comments','Keyword']
    df_raw_final = pd.DataFrame(df_raw,columns=header)
    df_raw_final['Date']=df_raw_final['Date'].str.split('\n').str[0]
    df = df_raw_final.replace('\n', '<br>', regex=True)
    driver.quit()
    
    #df.head()
    print("df is ready from scraper")
    return df


def connection(driver):
    driver.set_window_size(1920, 1080)
    #CONNECTION TO LINKEDIN
    print("Going to Linkedin")
    driver.get('https://www.linkedin.com/login')
    print("Linkedin reached")
    human_like_delay()
    username = driver.find_element(By.XPATH, '//input[@id="username"]')
    username.send_keys("alinemuller972@gmail.com")
    username.send_keys(Keys.RETURN)
    human_like_delay()
    password = driver.find_element(By.XPATH, '//input[@id="password"]')
    password.send_keys("alinemuller972alinemuller972")
    password.send_keys(Keys.RETURN)
    print("Connected to account")
    human_like_delay()
    

def one_search(keyword, driver):
    #driver.set_window_size(1920, 1080)
    
    try:
        print("Waiting for input button")
        wait = WebDriverWait(driver, 2)
        search = wait.until(EC.element_to_be_clickable((By.XPATH, "//input[contains(@class, 'search-global')]")))
    except Exception as str_error:
        print("Input button not selected")
        pass
    print("Input button selected")
    search.clear()
    search.send_keys(keyword)
    search.send_keys(Keys.RETURN)
    print("Search launched")
    # only get the posts
    #driver.find_element_by_xpath('//button[@aria-label="Posts"]').click()
    #driver.find_element_by_xpath('//button[value="Posts"]').click()
    for x in range(1, 5):  # try 4 times to click on "Posts"
        print("Try n°",x," to click on Posts")
        str_error = None
        try:
            driver.find_element(By.XPATH, "//button[text()='Posts']").click()
            
        except Exception as str_error:
            pass
        if str_error:
            sleep(2)  # wait for 2 seconds before trying to fetch the data again
        else:
            break

    print("Clicked on Posts")
    #get all the page
    #cards = driver.find_elements_by_xpath('//div[@class="search-results-container"]/div')
    #cards = driver.find_elements_by_xpath('//div[@class="search-results-container"]//div[contains(@class,"occludable-update ember-view")]'|'//div[@class="search-results-container"]//div[contains(@class,"feed-shared-update-v2 feed-shared-update-v2--minimal-padding full-height relative feed-shared-update-v2--e2e artdeco-card ember-view")]')
    cards = driver.find_elements(By.XPATH, '//div[@class="occludable-update ember-view"]|//div[@class="feed-shared-update-v2 feed-shared-update-v2--minimal-padding full-height relative feed-shared-update-v2--e2e artdeco-card ember-view"]')

    i=0
    for card in cards:
        print('\n','card numéro ',i,'\n')
        i+=1
        print(card.text)



import re
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.common.exceptions import TimeoutException, StaleElementReferenceException

def get_linkedin_post_data(driver,card,mot_cle):
    """Extract data from tweet card"""
    username=''
    try:
        username = card.find_element(By.XPATH, './/span[@dir="ltr"]').text.split('\n')[0]
        print("username:",username)
    except (NoSuchElementException, StaleElementReferenceException) as er:
        pass

    job=''
    try:
        job = card.find_element(By.XPATH, './/span[contains(@class,"update-components-actor__description")]').text.split('\n')[0]
        print("job:",job)
    except NoSuchElementException:
        pass

    date=''
    try:
        date = card.find_element(By.XPATH, './/span[contains(@class,"update-components-actor__sub-description text-body-xsmall")]').text
        print("date:",date)
    except NoSuchElementException:
        pass

    text1=''
    try:
        text1 = card.find_element(By.XPATH, './/span[contains(@class,"break-words")]').text
        print("text1:",text1)
    except NoSuchElementException:
        pass
    text2 = ''

    try:
        text2 = card.find_element(By.XPATH, './/h2/span[@dir="ltr"]').text
        print("text2:",text2)
    except NoSuchElementException:
        pass

    text = text1 + text2

    nb_reactions = 0
    nb_commentaires = 0
    nb_partages = 0

    try:
        nb_reactions = card.find_element(By.XPATH, './/span[contains(@class,"social-details-social-counts__reactions-count")]').text
    except NoSuchElementException:
        pass

    try:
        nb_commentaires = re.search('[0-9]+',card.find_element(By.XPATH, './/li[contains(@class,"social-details-social-counts__item social-details-social-counts__comments")]').text).group()
    except NoSuchElementException:
        pass
    try:
        nb_partages = re.search('[0-9]+',card.find_element(By.XPATH, './/li[contains(@aria-label,"partage")]').text).group()
    except NoSuchElementException:
        pass


    comments=''
    concat_comments= ''
    try:
        #sleep(2)
        #card.find_element_by_xpath('//button[@class="comments-comments-list__load-more-comments-button artdeco-button artdeco-button--muted artdeco-button--1 artdeco-button--tertiary ember-view"]').click()
        #card.find_elements_by_xpath('//button[contains(@aria-label="commentaire")]').click()
        #element = driver.find_element_by_xpath('div[class="comments-comments-list__load-more-comments-button artdeco-button artdeco-button--muted artdeco-button--1 artdeco-button--tertiary ember-view"]')
        #driver.execute_script("arguments[0].click();", element)
        #WebDriverWait(driver, 2).until(EC.element_to_be_clickable((By.XPATH, "//button[@class='comments-comments-list__load-more-comments-button artdeco-button artdeco-button--muted artdeco-button--1 artdeco-button--tertiary ember-view']"))).click()
        card.find_element(By.XPATH, './/button[contains(@class,"comment-button")]').click()
    except (NoSuchElementException, ElementClickInterceptedException, TimeoutException) as e:
        pass

    try:
        sleep(1)
        #comment = card.find_element_by_xpath('.//article[contains(@class,"comments")]/div[contains(@class,"break-words")]').text
        #comments = card.find_elements_by_xpath('.//div[contains(@class,"comments")]')
        concat_comments = '\n'.join([i.text for i in card.find_elements(By.XPATH, './/div[contains(@class,"text relative")]')][1:]) #[i.text for i in card.find_elements_by_xpath('.//div[contains(@class,"comments")]')][0]
        #text_comments = map(text,comments)
        #print(text_comments)
        #concat_comments = ' '.join(text_comments)
        #for comm in comments:
        #    concat_comments = concat_comments + comm.text
    except NoSuchElementException:
        pass


    linkedin_post = (username,job,date,text,nb_reactions,nb_commentaires,nb_partages,concat_comments,mot_cle)
    #print('CARD')
    #print('=====')
    #print(linkedin_post)
    #print('=====')
    return linkedin_post




def Scrape_Linkedin(mots_cles, driver):
    data = []
    linkedin_post_ids = set()
    driver.set_window_size(1920, 1080)
    for mot_cle in mots_cles:
        #print("DATA")
        #print("============")
        #print(data)
        #print("============")
        nb_of_scrolls=0

        #wait = WebDriverWait(driver, 10)
        #search = wait.until(
        #    EC.presence_of_element_located(
        #        (By.XPATH, "//div[contains(@class, 'earch') or contains(@class, 'echerche')]")))
        
        print("Trying to reach search button")
        try:
            wait = WebDriverWait(driver, 10)
            search = wait.until(EC.element_to_be_clickable((By.XPATH, "//input[contains(@class, 'search-global')]")))
            print("Search button reached")
            search.clear()
            print("Search cleared")
            search.send_keys(mot_cle)
            search.send_keys(Keys.RETURN)

        except Exception as str_error:
            print("Couldn't reach search button")
            print(driver.page_source)
            pass
        print("Search launched")
        # navigate to 'latest' tab
        #try:
        #    driver.find_element_by_xpath('//button[@aria-label="Posts"]').click()
        #except NoSuchElementException:
        #    pass
        #sleep(1)

        # get all posts of a page
        for x in range(1, 5):  # try 4 times to click on "Posts"
            print("Try n°",x," to click on Posts")
            str_error = None
            try:
                driver.find_element(By.XPATH, "//button[text()='Posts']").click()
                
            except Exception as str_error:
                pass
            if str_error:
                sleep(2)  # wait for 2 seconds before trying to fetch the data again
            else:
                break

        print("Clicked on Posts")


        last_position = driver.execute_script("return window.pageYOffset;")
        scrolling = True

        while scrolling:
            #page_cards = driver.find_elements_by_xpath('//div[@class="occludable-update ember-view"]|//div[@class="feed-shared-update-v2 feed-shared-update-v2--minimal-padding full-height relative feed-shared-update-v2--e2e artdeco-card ember-view"]')
            #page_cards = driver.find_elements_by_xpath('//div[@id="fie-impression-container"]')
            page_cards = driver.find_elements(By.XPATH, './/div[contains(@class,"feed-shared-update-v2--wrapped")]')
            for card in page_cards[-5:]:
                linkedin_post = get_linkedin_post_data(driver,card,mot_cle)
                if linkedin_post:
                    linkedin_post_id = ''.join(str(s) for s in linkedin_post)
                    if linkedin_post_id not in linkedin_post_ids:
                        linkedin_post_ids.add(linkedin_post_id)
                        data.append(linkedin_post)
                        print("Appending to data file")

            scroll_attempt = 0
            while True:
                # check scroll position
                driver.execute_script('window.scrollTo(0, document.body.scrollHeight);')
                #NB of scrolls before stopping the research
                if nb_of_scrolls > 1:
                    scrolling = False
                    break
                nb_of_scrolls+=1
                print('Scroll nb: ',nb_of_scrolls)
                sleep(random.randint(2,4))
                curr_position = driver.execute_script("return window.pageYOffset;")
                if last_position == curr_position:
                    scroll_attempt += 1
                    time.sleep(1)
                    print("scroll attempt : ",scroll_attempt)
                    # end of scroll region
                    if scroll_attempt >= 5:
                        scrolling = False
                        break
                    else:
                        sleep(2) # attempt another scroll
                else:
                    last_position = curr_position
                    break
            #Write data in a temp file at each word to avoid data loss if problem
            #with open('tmp_linkedin_posts_data.csv','w',newline='',encoding='utf-8') as f:
            #    header=['Username','Job','Date','Texte','Nb_reactions','Nb_commentaires','Nb_partages','Commentaires','Mot cle recherché']
            #    writer = csv.writer(f,delimiter=';')
            #    writer.writerow(header)
            #    writer.writerows(data)
    return data