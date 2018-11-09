import time
from selenium import webdriver

class Bot:
    def __init__(self):
        # Chrome WebDriver를 이용해 Chrome을 실행합니다.
        self.__driver = webdriver.Chrome('/Users/jungbohyuk/dev/store/chromedriver')
        self.__driver.implicitly_wait(3)
        self.__baseUrl = 'https://ppss.kr/'

    def get_category(self):
        self.__driver.get('https://ppss.kr/')
        ul = self.__driver.find_element_by_xpath('//*[@id="menu-menu"]')

        lis = ul.find_elements_by_tag_name('li')
        cnt = len(lis)
        if(cnt == 0):
            print('lis size is 0')
            return
        
        links = []

        for index, li in enumerate(lis):
            if(index == 0 or index == cnt - 1 or index == cnt - 2) :
                continue
            href = li.find_element_by_tag_name('a').get_attribute('href')
            links.append(href)
            
        # for link in links:
        #     print(link)

    def start(self):
        try:
            self.get_category()
            self.__driver.quit()
        except Exception as e:
            print(e)
            self.__driver.quit()

if __name__ == "__main__":
    Bot = Bot()
    Bot.start()
    

