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
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from collections import defaultdict
import collections
from operator import itemgetter
from collections import OrderedDict

locations = defaultdict(int)
taged_people_list = defaultdict(int)

post_id = 0

userid = 0
userpath = "./user%d"%userid
user_file = open(userpath, 'w', encoding="utf-8")

imgpath = "./img%d"%userid
img_file = open(imgpath, 'w', encoding="utf-8")

loginpath = "./login"
login_file = open(loginpath, 'r', encoding="utf-8")

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
    
    login_data = login_file.read()
    print(login_data)
    login = []
    login = re.split(' ',login_data)
    username = login[0]
    password = login[1]
    tag = "jojoxdaily"
    img_file.write(tag)
    
    quote_page = "https://www.instagram.com/%s/"%tag
    base_url = "https://www.instagram.com"
    browser = Browser()
    '''
    browser.get(quote_page)
    signin_x_btn = browser.find_one('._5gt5u')
    if signin_x_btn:
        signin_x_btn.click()

    signin_x_btn = browser.find_one('._lilm5')
    if signin_x_btn:
        browser.scroll_down()
        browser.js_click(signin_x_btn)

    more_btn = browser.find_one('._l8p4s')
    
    more_btn.click()'''
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
    )
    browser.get(quote_page)

    ele_posts = []
    ele_posts = browser.find('._mck9w')
    
    while len(ele_posts) < 12:
        browser.scroll_down()
        ele_posts = browser.find('._mck9w')
        #print(len(ele_posts))
    
    '''pageSource = browser.driver.page_source
    #print(len(ele_posts))
    #f.write("%s"%pageSource)
    
    response = BeautifulSoup(pageSource, "html.parser")
    #f.write("%s"%response)
    shared_data = extract_shared_data(response)
    user_profile = get_profile_information(shared_data)
    pprint(vars(user_profile))
    #f.write("%s"%shared_data)'''
    
    #sleep(800)
    rows = browser.find('._6d3hm._mnav9')
    links = []
    for row in rows:
        posts = row.find_elements_by_tag_name('a')
        for pt in posts:
            links.append(pt.get_attribute('href'))
    
    print(len(links))
    
    for j in range(0, len(links)):
    #for j in range(0, 10):
        
        contents = browser.find('._4rbun')
        content = contents[j].find_element_by_tag_name('img').get_attribute('alt')
        prize = 0
        if content.find('抽獎') >= 0:
            prize = 1
            print("======prize======")
        if prize == 0:
            variable = re.sub(base_url, "", links[j])
            browser.driver.find_element_by_xpath("//a[@href='%s']"%variable).click()
            sleep(2)
            location = browser.find('._q8ysx._6y8ij')
            imgs = browser.find('._2di5p')
            if location and imgs:
                
                postpath = "./post%d"%post_id
                post_file = open(postpath, 'w', encoding="utf-8")
                post_file.write("萌萌\n")
                post_file.write("%s\n"%links[j])
                
                location_url = location[0].get_attribute('href')
                locations[location_url]+=1
                img_file.write("\n%s"%location_url)
                post_file.write("%s\n"%location_url)
                
                img_url = imgs[len(imgs)-1].get_attribute('src')
                img_file.write("\n%s"%img_url)
                
                taged_people = browser.find('._n1lhu._4dsc8')
                if taged_people:
                    #taged_users_url = []
                    for p in taged_people:
                        taged_users_url=p.get_attribute('href')
                        taged_people_list[taged_users_url]+=1
                    #f.write("\ntaged_users_url: %s"%taged_users_url)
                '''
                date_time = browser.find_one('._p29ma._6g6t5').get_attribute('datetime')
                f.write("\ndate_time: %s"%date_time)'''
                post_file.write("%s"%content)
                post_file.close()
                post_id+=1
                
            if len(locations) >= 100 or j == len(links)-1:
                for key in taged_people_list:
                    taged_users = re.sub(base_url, "", key)
                    taged_users = taged_users.replace("/", "")
                    user_file.write("%s %s\n"%(tag, taged_users))
                break
            #sleep(800)
            close_btn = browser.find_one('._dcj9f')
            close_btn.click()
            sleep(2)