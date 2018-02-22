import jieba
from jieba import analyse
import re
from collections import defaultdict
import collections
from operator import itemgetter
from collections import OrderedDict

import MySQLdb

# Open database connection
db = MySQLdb.connect("localhost","testuser","test123","testdb", charset = "utf8")

# prepare a cursor object using cursor() method
cursor = db.cursor()

cursor.execute("SET NAMES utf8")
db.commit()

jieba.suggest_freq("可愛", True)
jieba.suggest_freq("卡士達", True)
jieba.suggest_freq("販賣機", True)
jieba.suggest_freq("適合", True)
jieba.suggest_freq("快樂", True)

post_id = 0

while post_id <= 3:

    words = defaultdict(int)

    postpath = "post%d"%post_id

    f = open(postpath, 'r', encoding="utf-8")
    
    post_url = ""
    location = ""
    
    for i in range(0, 3):
        line = f.readline()
        if i == 1:
            post_url = line
        if i == 2:
            location = line
    #print(post_url)
    #print(location)
    content = f.read()
    f.close()
    #print(content)
    data = re.split('#',content)

    str = ""
    for n in re.findall(u'[\u4e00-\u9fff]+',content):
        str = str + n + "\n"
    #seg_list = jieba.cut(str)
    #print("Default Mode: " + "/ ".join(seg_list))

    for x, w in analyse.extract_tags(str, withWeight=True):
        #print('%s %s' % (x, w))
        if w > 0.1:
            words[x] += 1
    #print("-----------------------")
    for tag in re.findall("#[a-zA-Z0-9\u4e00-\u9fff]+", content):
        #print(tag)
        tag = re.sub("^#", "", tag)
        words[tag] += 1
    strr = ""
    for n in re.findall(u'[a-zA-Z]+',content):
        strr = strr + n + "\n"
        words[n] += 1
    #print("-----------------------")
    #print(strr)
    #print("-----------------------")
    post_content = ""
    for key in words:
        #print(key)
        post_content = post_content + key + ','
    #print(post_content)
    # Prepare SQL query to INSERT a record into the database.
    sql = "INSERT INTO POST VALUES ('%d', '%s', '%s', '%s')"%(post_id, post_url, location, post_content)
    try:
        # Execute the SQL command
        cursor.execute(sql)
        # Commit your changes in the database
        db.commit()
    except:
        print("--------------")
        # Rollback in case there is any error
        db.rollback()
    
    post_id += 1
# disconnect from server
db.close()