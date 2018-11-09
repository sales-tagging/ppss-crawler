from selenium import webdriver
from newspaper import Article
import pymysql

class Bot:
    def __init__(self):
        # Chrome WebDriver를 이용해 Chrome을 실행합니다.
        self.__driver = webdriver.Chrome('/Users/jungbohyuk/dev/store/chromedriver')
        self.__driver.implicitly_wait(3)
        self.__baseUrl = 'https://ppss.kr/'
        self.__dev = True
        self.__category = dict()
        
        self.__conn = pymysql.connect(host='localhost', user='root', password='qpqp1010',
                       db='testDB', charset='utf8')
 
        # Connection 으로부터 Cursor 생성
        self.__curs = self.__conn.cursor()
        
    def setDev(self, flag):
        self.__dev = flag

    def get_category(self):
        self.__driver.get('https://ppss.kr/')
        ul = self.__driver.find_element_by_xpath('//*[@id="menu-menu"]')

        lis = ul.find_elements_by_tag_name('li')
        cnt = len(lis)
        if(cnt == 0):
            print('lis size is 0')
            return
        
        bigCategories = ['business', 'current-affairs', 'culture', 'tech', 'life', 'special']
        cntBigCategories = len(bigCategories)
        categories = {bigCategories[i]: [] for i in range(0, len(bigCategories), 1)}

        ix_category = 0

        for index, li in enumerate(lis):
            if(index == 0 or index == cnt - 1 or index == cnt - 2) :
                continue    

            href = li.find_element_by_tag_name('a').get_attribute('href')

            if(cntBigCategories > ix_category and bigCategories[ix_category] in href):
                target = bigCategories[ix_category]
                ix_category = ix_category + 1

                continue
            
            categories[target].append(href)

        if(self.__dev):
            for big, sub in categories.items():    # for name, age in dictionary.iteritems():  (for Python 2.x)
                print('[', big, ']')
                for link in sub:
                    print(link)

        return categories

    def get_data_from_url(self, link):
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
        pageNumber = 1

        links = []

        while(True):
            self.__driver.get(link + '/page/' + str(pageNumber))
            articles = self.__driver.find_elements_by_tag_name('article')

            for article in articles:
                href = article.find_element_by_tag_name('a').get_attribute('href')
                links.append(href)
                
                if(self.__dev):
                    print(href)

            if(len(articles) < 10):
                break
            
            pageNumber = pageNumber + 1

            if(self.__dev):
                if(pageNumber > 3):
                    break

        return links
            
    def start(self):
        sql = """INSERT INTO ARTICLE(link_num, big_category, sub_category, title, content) VALUES(%s, %s, %s, %s, %s)"""
        # sql = "SELECT * FROM ARTICLE"
        # self.__curs.execute(sql)
        # rows = self.__curs.fetchall()
        # print(rows)     # 전체 rows

        # return
        try:
            categories = self.get_category()
            for bigCategoryName, subCategory in categories.items():    # for name, age in dictionary.iteritems():  (for Python 2.x)
                for subCategoryLink in subCategory:
                    arr = subCategoryLink.split('/')
                    subCategoryName = arr[len(arr)-1]
                    links = self.collect_article_link(subCategoryLink)
                    for link in links:
                        result = self.get_data_from_url(link)
                        linkArr = link.split('/')
                        linkNum = linkArr[len(linkArr) - 1]

                        if(self.__dev):
                            print('link num : ', linkNum)
                            print('title : ', result['title'])
                            print('text : ', result['text'])

                        try:
                            self.__curs.execute(sql, (linkNum, bigCategoryName, subCategoryName, result['title'], result['text']))
                            # self.__curs.execute(sql, (bigCategoryName, subCategoryName, '서울', '하이'))
                            self.__conn.commit()
                        except Exception as e:
                            print(e)
                            continue
                
            self.__driver.quit()
        except Exception as e:
            print(e)
            self.__driver.quit()

if __name__ == "__main__":
    Bot = Bot()
    # Dev mode is print log data and for simple test, using following this:
    # Bot.setDev(False)
    Bot.start()
    
    # Bot.get_data_from_url('https://ppss.kr/archives/178229')
    # Bot.collect_article_link('https://ppss.kr/archives/category/marketing')
