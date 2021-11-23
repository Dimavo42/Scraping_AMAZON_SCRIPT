from bs4 import BeautifulSoup as bs
from selenium import webdriver

class Info:
    def __init__(self,item):
        self.driver=webdriver.Chrome(executable_path=r"D:\first_python_serious_project\chromedriver.exe") ###dfine here the path
        self.item_path=self.__get_path(item)
        self.driver.get(self.item_path)

    def __get_path(self,name):
        template = "https://www.amazon.com/s?k={}&ref=nb_sb_noss_1"
        name = name.replace(' ', '+')
        return template.format(name)

    def __make_new_path(self,name):
        if (name):
            return "https://www.amazon.com/" + name
        else:
            return False

    def __next_page(self,soup):
        page = soup.find('ul', {'class': 'a-pagination'})### IT have 2 options or it have "next link" in NORNMAL scrap OPITION 2  the search looking for a book then amazon search style is diffient and have been treat differnt
        if(page==None):
            return False
        if not page.find('li', {'class': 'a-disabled a-last'}):
            next_link = page.find('li', {'class': 'a-last'}).find('a')
            return next_link.get('href')
        else:
            return False

    def __scrap_info(self,soup):
        index = 0
        dico = {}
        pages = soup.find_all('div', {'data-component-type': 's-search-result'})
        if (len(pages) > 0):
            for t in pages:                                                              ###the function is scraping all data from amazon page and yelid the infromation creating dict for it
                dico[index] = {'name': None, 'price': 0.0, 'link': None, 'stars': None, 'Shipping': None}
                if (t.find('span', {'class': 'a-size-base-plus a-color-base a-text-normal'})):
                    dico[index]['name'] = t.find('span', {'class': 'a-size-base-plus a-color-base a-text-normal'}).text
                elif (t.find('span', {'class': 'a-size-medium a-color-base a-text-normal'})):
                    dico[index]['name'] = t.find('span', {'class': 'a-size-medium a-color-base a-text-normal'}).text
                if (t.find('span', {'class': 'a-size-base-plus a-color-base a-text-normal'})):
                    dico[index]['link'] = t.find('a', {'class': 'a-link-normal a-text-normal'}).get('href')
                elif (t.find('a', {'class': 'a-link-normal a-text-normal'})):
                    dico[index]['link'] = dico[index]['link'] = t.find('a',
                                                                       {'class': 'a-link-normal a-text-normal'}).get(
                        'href')
                if (t.find('span', {'class': 'a-price'})):
                    if ',' not in ((t.find('span', {'class': 'a-price'}).text).split('$')[1]):  ### the number contines ',' in it and it string need to to make a double
                        dico[index]['price'] = dico[index]['price'] = \
                        (t.find('span', {'class': 'a-price'}).text).split('$')[1]
                    else:
                        splited_price = []
                        splited_price.append(((t.find('span', {'class': 'a-price'}).text).split('$')[1]).split(',')[0])
                        splited_price.append(((t.find('span', {'class': 'a-price'}).text).split('$')[1]).split(',')[1])
                        dico[index]['price'] = splited_price[0] + splited_price[1]
                if (t.find('div', {'class': 'a-row a-size-small'})):
                    dico[index]['stars'] = t.find('div', {'class': 'a-row a-size-small'}).find(
                        {'span': 'aria-label'}).text
                if (t.find('div', {'class': 'a-row a-size-base a-color-secondary s-align-children-center'})):
                    dico[index]['Shipping'] = t.find('div', {
                        'class': 'a-row a-size-base a-color-secondary s-align-children-center'}).text
                index += 1
            yield dico
        else:
            pages = soup.find_all('li', {
                'class': 'a-carousel-card acswidget-carousel__card'})  ### if searching for books differnet style of scrap
            for page in pages:
                dico[index] = {'name': None, 'price': 0.0, 'link': None, 'stars': None, 'Shipping': None}
                if (page.find('span', {'class': 'a-truncate-full a-offscreen'})):
                    dico[index]['name'] = page.find('span', {'class': 'a-truncate-full a-offscreen'}).text
                if (page.find('a', {'class': 'a-color-base a-link-normal'})):
                    dico[index]['link'] = page.find('a', {'class': 'a-color-base a-link-normal'}).get('href')
                if (page.find('span', {'class': 'a-price-whole'})):
                    dico[index]['price'] = (page.find('span', {'class': 'a-price-whole'}).text).split('.')[0]
                if (page.find({'i': 'class'})):
                    dico[index]['stars'] = page.find({'i': 'class'}).text
                yield dico


### Make running have 1 loop for a page its scraps all data with scraping info and sending it outside


    def make_running(self):
        soup = bs(self.driver.page_source, 'html.parser')   ###the function is makeing a loop at selenium so each time it gives new page to scrap when it doesnt have page its stops scraping
        for info in self.__scrap_info(soup):
            yield info
        url = self.__make_new_path(self.__next_page(soup))
        if(url==False):### IF the search is for a book Then the URL have a NONETYPE and theres no point to contiune beceasus therse no next page
            return
        self.driver.get(url)
        soup = bs(self.driver.page_source, 'html.parser')
        while (True):
            for info in self.__scrap_info(soup):
                yield info
            url = self.__make_new_path(self.__next_page(soup))
            if (isinstance(url, str) == False):### no more pages to scrap
                break
            self.driver.get(url)
            soup = bs(self.driver.page_source, 'html.parser')



