# ppss-crawler
crawling 'ㅍㅍㅅㅅ' homepage with pytohn

### instll

```
$ pip install -U Selenium
$ pip install PyMySQL

# python 3
$ pip install newspaper3k
```

mysql db query following this:
```
CREATE TABLE article (
	id INT(11) UNSIGNED NOT NULL AUTO_INCREMENT,
    link_num INT(11) UNIQUE,
	big_category VARCHAR(255),
	sub_category VARCHAR(255),
	title VARCHAR(255),
	content MEDIUMTEXT,
	PRIMARY KEY (id)
) charset=utf8;
```

### How to use?

db info setting: input your user, password, db name
```
self.__conn = pymysql.connect(host='localhost', user='user', password='password', db='testDB', charset='utf8')
```

driver info setting: input driver path
If you want to get off headless options, erase chrome_options part
```
self.__driver = webdriver.Chrome('/driver/path', chrome_options=options)
```

If you want to use real not dev, erase following this comment:
```
From: 
# Bot.setDev(False)

To:
Bot.setDev(False)
```

Now, Excute Main.py
```
$ python Main.py
```