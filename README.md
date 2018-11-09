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