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

filepath = "./output"
f = open(filepath, 'w', encoding="utf-8")

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
    
    tag = "jojoxdaily"
    
    quote_page = "https://www.instagram.com/%s/"%tag
    
    browser = Browser()
    
    browser.get(quote_page)
    signin_x_btn = browser.find_one('._5gt5u')
    if signin_x_btn:
        signin_x_btn.click()

    signin_x_btn = browser.find_one('._lilm5')
    if signin_x_btn:
        browser.scroll_down()
        browser.js_click(signin_x_btn)

    more_btn = browser.find_one('._1cr2e._epyes')
    
    more_btn.click()

    ele_posts = []
    ele_posts = browser.find('._cmdpi ._mck9w')
    while len(ele_posts) < 36:
        browser.scroll_down()
        ele_posts = browser.find('._cmdpi ._mck9w')
        #print(len(ele_posts))
    pageSource = browser.driver.page_source
    #print(len(ele_posts))
    #f.write("%s"%pageSource)
    
    response = BeautifulSoup(pageSource, "html.parser")
    #f.write("%s"%response)
    shared_data = extract_shared_data(response)
    user_profile = get_profile_information(shared_data)
    pprint(vars(user_profile))
    #f.write("%s"%shared_data)
    
    
    rows = response.find_all('div', '_70iju')
    links = []
    for row in rows:
        posts = row.find_all('a')
        for pt in posts:
            links.append(pt.attrs['href'])
    
    #f.write("%s"%links)
    print(len(links))
    
    #print("//a[@href="+"'"+links[0]+"'"+"]")
    for j in range(0, len(links)):
    
        browser.driver.find_element_by_xpath("//a[@href="+"'"+links[j]+"'"+"]").click()
        sleep(2)
        location = browser.find('._q8ysx._6y8ij')
        if location:
            location_url = location[0].get_attribute('href')
            f.write("\nlocation_url: %s"%location_url)
            
            imgs = browser.find('._2di5p')
            if imgs:
                img_url = imgs[len(imgs)-1].get_attribute('src')
                f.write("img_url: %s"%img_url)
            
            taged_people = browser.find('._n1lhu._4dsc8')
            if taged_people:
                taged_users_url = []
                for p in taged_people:
                    taged_users_url.append(p.get_attribute('href'))
                f.write("\ntaged_users_url: %s"%taged_users_url)
            
            like = browser.find('._nzn1h')
            if like:
                likes = like[0].find_element_by_tag_name('span').text
                f.write("\nlikes: %s"%likes)
            
            ele_num_comments = browser.find_one('._m3m1c._1s3cd')
            num_comments = 0
            while ele_num_comments:
                obj = ele_num_comments
                try:
                    obj = obj.find_element_by_tag_name('span')
                except NoSuchElementException:
                    obj =  None
                if obj:
                    num_comments = obj.text
                    break
                else :
                    ele_num_comments.click()
                    ele_num_comments = browser.find_one('._m3m1c._1s3cd')
            
            comments = []
            ele_comments = browser.find('._ezgzd')
            for i in range(1, len(ele_comments)):
                comments.append(ele_comments[i].find_element_by_tag_name('span').text)
            f.write("\ncomments: %s"%comments)
            if num_comments == 0:
                num_comments = len(ele_comments)-1
            f.write("\nnum_comments: %s"%num_comments)
            
            date_time = browser.find_one('._p29ma._6g6t5').get_attribute('datetime')
            f.write("\ndate_time: %s"%date_time)
            
        #sleep(800)
        close_btn = browser.find_one('._dcj9f')
        close_btn.click()
        contents = browser.find('._4rbun')
        content = contents[j].find_element_by_tag_name('img').get_attribute('alt')
        f.write("\ncontent: %s"%content)
        f.write("\n\n")