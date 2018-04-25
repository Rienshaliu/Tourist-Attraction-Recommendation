    '''
    ele_posts = []
    ele_posts = browser.find('._havey ._mck9w')
    
    while len(ele_posts) < 36:
        browser.scroll_down()
        ele_posts = browser.find('._havey ._mck9w')
        print(len(ele_posts))'''
    
    '''pageSource = browser.driver.page_source
    #print(len(ele_posts))
    #f.write("%s"%pageSource)
    
    response = BeautifulSoup(pageSource, "html.parser")
    #f.write("%s"%response)
    shared_data = extract_shared_data(response)
    user_profile = get_profile_information(shared_data)
    pprint(vars(user_profile))
    #f.write("%s"%shared_data)'''
	
    posts_list = defaultdict(int)
    while len(locations) < num_locations:
        
        #rows = browser.find('._6d3hm._mnav9')
        ele_posts = browser.find('._havey ._mck9w')
        
        for ele_post in ele_posts:
            print("locations: %d"%len(locations))
            
            try:
                pt = ele_post.find_element_by_tag_name('a')
            except StaleElementReferenceException:
                break
            pt = ele_post.find_element_by_tag_name('a')
            
            link = pt.get_attribute('href')
            if posts_list[link] != 5:
                posts_list[link] = 1
        
            if posts_list[link] == 1:
                posts_list[link] = 5
                content = ele_post.find_element_by_tag_name('img').get_attribute('alt')
                prize = 0
                if content.find('抽獎') >= 0:
                    prize = 1
                    print("======prize======")
                if prize == 0:
                    variable = re.sub(base_url, "", link)
                    browser.driver.find_element_by_xpath("//a[@href='%s']"%variable).click()
                    sleep(2)
                    location = browser.find('._q8ysx._6y8ij')
                    imgs = browser.find('._2di5p')
                    if location and imgs:
                        
                        postpath = "./post/post%d"%post_id
                        post_file = open(postpath, 'w', encoding="utf-8")
                        post_file.write("萌萌\n")
                        post_file.write("%s\n"%link)
                        
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
                        
                        if len(locations) >= num_locations:
                            break
                    #sleep(800)
                    close_btn = browser.find_one('._dcj9f')
                    close_btn.click()
                    sleep(2)
        browser.scroll_down()
    for key in taged_people_list:
        taged_users = re.sub(base_url, "", key)
        taged_users = taged_users.replace("/", "")
        user_file.write("%s %s\n"%(tag, taged_users))