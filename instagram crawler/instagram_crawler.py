import requests
from bs4 import BeautifulSoup
import json
from json import JSONDecodeError
import re
from pprint import pprint
import time
from browser import Browser
from time import sleep
from selenium.common.exceptions import NoSuchElementException
from selenium.common.exceptions import StaleElementReferenceException
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from collections import defaultdict
import collections
from operator import itemgetter
from collections import OrderedDict

locations = defaultdict(int)
taged_people_list = defaultdict(int)

post_id = 1976

num_locations = 50

userid = 31
userpath = "./user/user%d"%userid
user_file = open(userpath, 'w', encoding="utf-8")

imgpath = "./img/img%d"%userid
img_file = open(imgpath, 'w', encoding="utf-8")

loginpath = "./login"
login_file = open(loginpath, 'r', encoding="utf-8")

file = open("data", 'w', encoding="utf-8")

class InstagramUser:
    def __init__(self, user_id, username=None, bio=None, followers_count=None, following_count=None, is_private=False, user_picture=None):
        
        self.id = user_id
        self.username = username
        self.bio = bio
        self.followers_count = followers_count
        self.following_count = following_count
        self.is_private = is_private
        self.user_picture = user_picture

def extract_shared_data(doc):

    for script in doc.find_all("script"):
        if script.text.startswith("window._sharedData ="):
            shared_data = re.sub("^window\._sharedData = ", "", script.text)
            shared_data = re.sub(";$", "", shared_data)
            shared_data = json.loads(shared_data)
            shared_data = shared_data['entry_data']['ProfilePage'][0]['user']
            return shared_data

def get_profile_information(data):
    
    return InstagramUser(
        user_id = data['id'],
        username = data['full_name'],
        bio = data['biography'],
        followers_count = data['followed_by']['count'],
        following_count = data['follows']['count'],
        is_private = data['is_private'],
        user_picture = data['profile_pic_url']
    )

if __name__ == '__main__':
    
    '''login_data = login_file.read()
    print(login_data)
    login = []
    login = re.split(' ',login_data)
    username = login[0]
    password = login[1]'''
    tag = "enjoylifesun"
    img_file.write(tag)
    
    quote_page = "https://www.instagram.com/%s/"%tag
    base_url = "https://www.instagram.com"
    browser = Browser()
    '''
    browser.get(base_url+'/accounts/login/')
    sleep(2)
    username_input = WebDriverWait(browser.driver, 5).until(
        EC.presence_of_element_located((By.NAME, 'username'))
    )
    username_input.send_keys(username)
    # Input password
    password_input = WebDriverWait(browser.driver, 5).until(
        EC.presence_of_element_located((By.NAME, 'password'))
    )
    password_input.send_keys(password)
    # Submit
    password_input.submit()
    print("")
    WebDriverWait(browser.driver, 60).until(
        EC.presence_of_element_located((By.CSS_SELECTOR, "a[href='/explore/']"))
    )'''
    browser.get(quote_page)
    
    posts_list = defaultdict(int)
    while len(locations) < num_locations:
        pageSource = browser.driver.page_source
        response = BeautifulSoup(pageSource, "html.parser")
        ele_posts = response.select('._mck9w')
        for ele_post in ele_posts:
            print("locations: %d"%len(locations))
            
            pt = ele_post.find('a')
            
            link = pt.get('href')
            if posts_list[link] != 5:
                posts_list[link] = 1
        
            if posts_list[link] == 1:
                posts_list[link] = 5
                content = ele_post.find('img').get('alt')
                
                prize = 0
                if content.find('抽獎') >= 0:
                    prize = 1
                    print("======prize======")
                if prize == 0:
                    variable = re.sub(base_url, "", link)
                    browser.driver.find_element_by_xpath("//a[@href='%s']"%variable).click()
                    sleep(2)
                    
                    postSource = browser.driver.page_source
                    post_response = BeautifulSoup(postSource, "html.parser")
                    
                    location = post_response.find('a', class_='_6y8ij')
                    imgs = post_response.find_all('img', class_='_2di5p')
                    #file.write("\n%s"%imgs[len(imgs)-1].get('src'))
                    if location and imgs:
                        
                        postpath = "./post/post%d"%post_id
                        post_file = open(postpath, 'w', encoding="utf-8")
                        post_file.write("萌萌\n")
                        post_file.write("%s\n"%link)
                        
                        location_url = location.get('href')
                        locations[location_url]+=1
                        img_file.write("\n%s"%location_url)
                        post_file.write("%s\n"%location_url)
                        
                        img_url = imgs[len(imgs)-1].get('src')
                        img_file.write("\n%s"%img_url)
                        
                        taged_people = post_response.find_all('a', class_='_n1lhu')
                        if taged_people:
                            #taged_users_url = []
                            for p in taged_people:
                                taged_users_url=p.get('href')
                                taged_people_list[taged_users_url]+=1
                            #f.write("\ntaged_users_url: %s"%taged_users_url)
                        
                        post_file.write("%s"%content)
                        post_file.close()
                        post_id+=1
                        
                        if len(locations) >= num_locations:
                            break
                    browser.find_one('._dcj9f').click()
                    sleep(2)
        browser.scroll_down()
    for key in taged_people_list:
        taged_users = re.sub(base_url, "", key)
        taged_users = taged_users.replace("/", "")
        user_file.write("%s %s\n"%(tag, taged_users))

