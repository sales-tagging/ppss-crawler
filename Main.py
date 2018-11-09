from selenium import webdriver

class Bot:
    def __init__(self):
        # Chrome WebDriver를 이용해 Chrome을 실행합니다.
        self.__driver = webdriver.Chrome('/Users/jungbohyuk/dev/store/chromedriver')
        self.__driver.implicitly_wait(3)
        self.__baseUrl = 'https://ppss.kr/'
        self.__display = True

    def setDisplay(self, flag):
        self.__display = flag

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
        d = {bigCategories[i]: [] for i in range(0, len(bigCategories), 1)}

        ix_category = 0

        for index, li in enumerate(lis):
            if(index == 0 or index == cnt - 1 or index == cnt - 2) :
                continue    

            href = li.find_element_by_tag_name('a').get_attribute('href')

            if(cntBigCategories > ix_category and bigCategories[ix_category] in href):
                target = bigCategories[ix_category]
                ix_category = ix_category + 1

                continue
            
            d[target].append(href)

        if(self.__display):
            for big, sub in d.items():    # for name, age in dictionary.iteritems():  (for Python 2.x)
                print('[', big, ']')
                for link in sub:
                    print(link)

    def start(self):
        try:
            self.get_category()
            self.__driver.quit()
        except Exception as e:
            print(e)
            self.__driver.quit()

if __name__ == "__main__":
    Bot = Bot()
    # If you want to not display print data, using following this:
    # Bot.setDisplay(False)
    Bot.start()
    

