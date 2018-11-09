# ppss-crawler
crawling 'ㅍㅍㅅㅅ' homepage with python

### install

0. install mysql server && chrome && chrome web-driver

1. install pypi packages
```
$ pip install -U selenium pymysql

# python 2
$ pip install -U newspaper

# python 3
$ pip install -U newspaper3k
```

2. create ```ppss``` database && create ```article``` table under ```ppss``` database.

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
db_info = {
    "host": "localhost",
    "user": "root",
    "password": "1111",
    "db": "ppss",
    "charset": "utf8",
}
```

driver info setting: input driver path
If you want to get off headless options, erase chrome_options part
```
Bot = Bot(driver_path="./", db_info=db_info, verbose=True)
```

If you wanna off verbose mode, uncomment commented line:159:
```
From: 
# Bot.set_dev(False)

To:
Bot.set_dev(False)
```

Now, Execute main.py!
```
$ python main.py
```