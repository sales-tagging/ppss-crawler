from selenium import webdriver
from newspaper import Article

import pymysql


class Bot:

    def __init__(self, driver_path, db_info, verbose=True):
        """ Execute Chrome browser with Chrome WebDriver """
        self.driver_path = driver_path
        self.db_info = db_info

        options = webdriver.ChromeOptions()
        options.add_argument('--disable-extensions')
        options.add_argument('--headless')
        options.add_argument('--disable-gpu')
        options.add_argument('--no-sandbox')

        # self.__driver = webdriver.PhantomJS('/Users/jungbohyuk/dev/store/phantomjs-2.1.1-macosx/bin/phantomjs')
        self.__driver = webdriver.Chrome(self.driver_path, chrome_options=options)
        self.__driver.implicitly_wait(3)
        self.__baseUrl = 'https://ppss.kr/'
        self.__dev = verbose
        self.__category = dict()

        self.__conn = pymysql.connect(**self.db_info)
 
        # Connection 으로부터 Cursor 생성
        self.__curs = self.__conn.cursor()
        
    def set_dev(self, flag):
        self.__dev = flag

    def get_category(self):
        self.__driver.get(self.__baseUrl)
        ul = self.__driver.find_element_by_xpath('//*[@id="menu-menu"]')

        lis = ul.find_elements_by_tag_name('li')
        cnt = len(lis)

        if cnt == 0:
            print('lis size is 0')
            return

        big_categories = ['business', 'current-affairs', 'culture', 'tech', 'life', 'special']
        cnt_big_categories = len(big_categories)
        categories = {big_categories[i]: [] for i in range(cnt_big_categories)}

        target = ''
        ix_category = 0
        for index, li in enumerate(lis):
            if index == 0 or index == cnt - 1 or index == cnt - 2:
                continue    

            href = li.find_element_by_tag_name('a').get_attribute('href')

            if cnt_big_categories > ix_category and big_categories[ix_category] in href:
                target = big_categories[ix_category]
                ix_category += 1
                continue

            categories[target].append(href)

        if self.__dev:
            for big, sub in categories.items():
                print('[', big, ']')
                for link in sub:
                    print(link)

        return categories

    @staticmethod
    def get_data_from_url(link):
        a = Article(link, language='ko')
        a.download()
        a.parse()

        print(a.title)
        print(a.text)

        d = dict()
        d['title'] = a.title
        d['text'] = a.text

        return d

    def collect_article_link(self, link):
        n_page = 1

        links = []

        while True:
            self.__driver.get(link + '/page/' + str(n_page))
            articles = self.__driver.find_elements_by_tag_name('article')

            for article in articles:
                href = article.find_element_by_tag_name('a').get_attribute('href')
                links.append(href)
                
                if self.__dev:
                    print(href)

            if len(articles) < 10:
                break

            n_page += 1

            if self.__dev:
                if n_page > 3:
                    break

        return links
            
    def start(self):
        sql = """INSERT INTO ARTICLE(link_num, big_category, sub_category, title, content) VALUES(%s, %s, %s, %s, %s)"""

        try:
            categories = self.get_category()
            for big_category_name, sub_category in categories.items():
                for sub_category_link in sub_category:
                    arr = sub_category_link.split('/')
                    sub_category_name = arr[-1]
                    links = self.collect_article_link(sub_category_link)
                    for link in links:
                        result = self.get_data_from_url(link)
                        link_arr = link.split('/')
                        link_num = link_arr[-1]

                        if self.__dev:
                            print('link num : ', link_num)
                            print('title    : ', result['title'])
                            print('text     : ', result['text'])

                        try:
                            self.__curs.execute(sql, (link_num, big_category_name, sub_category_name,
                                                      result['title'], result['text']))
                            self.__conn.commit()
                        except Exception as e:
                            print(e)
                            continue

            self.__driver.quit()
        except Exception as e:
            print(e)
            self.__driver.quit()


if __name__ == "__main__":
    db_info = {
        "host": "localhost",
        "user": "root",
        "password": "1111",
        "db": "ppss",
        "charset": "utf8",
    }

    Bot = Bot(driver_path="./", db_info=db_info, verbose=True)
    # Bot.set_dev(False) # turn off logging if you want

    Bot.start()

