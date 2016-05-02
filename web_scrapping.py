import pprint as pp
import numpy as np
from bs4 import BeautifulSoup
from termcolor import colored
import requests
import re




# PULL RECIPE DATA

R = 'no'
if R == 'yes':
    Quantities = { 'cup', 'cups', 'teaspoon', 'teaspoons', 'tablespoon', 'tablespoons' ,
                   'pound', 'pounds', 'lbs', "lb's", 'lb', 'ounce', 'ounces', 'oz', 'ozs', "oz's"}


    Volume ={   'teaspoon':  1, 'teaspoons' :  1, 't' : 1 , 'tsp.' : 1 , 'tsp': 1 ,
                'tablespoon': 3 , 'tablespoons' : 3 ,'T': 3 , 'tbl.' : 3 , 'tbl' : 3 , 'tbs': 3 , 'tbsp': 3 ,
                'fluid ounce'  : 6 , 'fluid ounces' : 6 ,'fl oz': 6 ,
                'gill':  24,
                'cup': 48 , 'cups': 48 ,
                'pint': 96 , 'pints': 96 , 'p': 96 , 'pt': 96 , 'fl pt': 96 ,
                'quart': 192 , 'quarts': 192 , 'q': 192 , 'qt': 192 , 'fl qt': 192 ,
                'gallon': 768 , 'gallons': 768 , 'g': 768 , 'gal': 768 ,
                'ml': .2 , 'milliliter':  .2, 'milliliters': .2 , 'millittre': .2 , 'millittres': .2 , 'cc': .2 , 'mL': .2 ,
                'liter': 203 , 'liters': 203 , 'litre': 203 , 'litres': 203 , 'L': 203 ,
                'dl': 20 , 'decliter': 20 , 'decliters': 20 , 'declitre': 20 , 'declitres':20, 'dL':20}

    Mass = {    'pounds':16, 'pounds': 16 , 'pound':16,'lb': 16 , '#': 16 ,
                'ounce': 1 , 'ounces':1  , 'oz': 1 ,
                'mg': .000035 , 'milligram': .000035 , 'milligrams': .000035 , 'milligramme': .000035 , 'milligrammes': .000035 ,
                'gram': .035 , 'grams': .035 , 'g': .035 , 'gramme': .035 , 'grammes': .035,
                'kg': 35 , 'kilogram': 35 , 'kilograms': 35 , 'kilogramme' : 35 , 'kilogrammes' : 35}


    Length = {  'mm': 1 , 'millimeter': 1 , 'millimeters': 1 , 'millimetre': 1 , 'millimetres': 1 ,
                'cm': 10  , 'centimeter': 10 , 'centimeters': 10 , 'centimetre': 10 , 'centimetres': 10 ,
                'm':  1000, 'meter': 1000 , 'metere': 1000 , 'meters': 1000 , 'metres': 1000 ,
                'in': 25.4 , 'inch': 25.4 , 'inches': 25.4 , '"':25.4}



    Recipes = {}



    # p = re.compile( r'[\d\/]+')


    n= 1
    for i in range(n,n+1):

        URL = 'http://allrecipes.com/recipe/' + str(i)

        response = requests.get(URL ).content
        soup = BeautifulSoup(response, 'html.parser')


        #TITLE
        title = soup.find_all('h1', class_ ='recipe-summary__h1' )
        if len(title) > 0:
            title = title[0].text
            letters = soup.find_all("span", class_="recipe-ingred_txt added")
            print('\n\n')
            print(colored(title,'red'))

            ingredients = {}
            for x in letters:

                y = x.text
                y = y.replace('(','')
                y = y.replace(')','')
                print(y)

                Q=[]
                # Q =   [int(s) for s in y.split() if s.isdigit()]
                text = y.split()
                temp = []
                #STRIP OUT QUANTITIES
                for z in text:
                    if z.isdigit():
                        Q.append(int(z))
                        temp.append(z)
                    elif '/' in z:
                        if z.split('/')[0].isdigit() and z.split('/')[1].isdigit():
                            Q.append( int(z.split('/')[0])/ int(z.split('/')[1]))
                            temp.append(z)
                    elif '.' in z:
                        if z.split('.')[0].isdigit() and z.split('.')[1].isdigit():
                            Q.append( int(z.split('.')[0])+ (.1)**len(z.split('.')[1]) *int(z.split('.')[1]))
                            temp.append(z)

                for x in temp:
                    text.remove(x)

                # print(text)
                #MULTIPLY QUANTITIES TO GET AMOUNT
                if len(Q) >0:
                    q = np.prod(Q)
                else:
                    q = 0

                #PULL OUT UNIT
                for z in text:
                    # print(z)
                    if z in Volume.keys():
                        q = q*Volume[z]
                        text.remove(z)
                        unit = 'teaspoon'
                        break
                    elif z in Mass.keys():
                        q = q*Mass[z]
                        text.remove(z)
                        unit = 'ounce'
                        break
                    elif z in Length.keys():
                        q = q*Length[z]
                        text.remove(z)
                        unit = 'cm'
                        break
                    else:
                        unit = 'none'

                y = " ".join(text)
                # print(y)
                y = y.replace( 'can', '')
                y = y.replace( '  ', ' ')
                y = y.lstrip(' ').rstrip(' ')




                ingredients[ y ] = [q, unit]
                print(colored('type:','yellow'),y, '||' ,colored('quantity:','yellow'),q, unit, '\n')
                # print('unit:',u,'\n')


            Recipes[ title] = ingredients



#
# total = 0
# L = []
# for x in Recipes.values():
#     total = total +len(x)
#     for y in x.keys():
#         if y.lstrip().rstrip() not in L:
#             L.append(y.lstrip().rstrip())


#
# import pprint
# pp = pprint.PrettyPrinter(indent=2)
# pp.pprint(Recipes)






# PULL REVIEWER DATA

S = 'no'
if S == 'yes':

    from selenium import webdriver
    from selenium.webdriver.common.keys import Keys
    import os

    chromedriver = "/Users/ryan/Desktop/Programming/AllRecipes/chromedriver"
    os.environ["webdriver.chrome.driver"] = chromedriver
    driver = webdriver.Chrome(chromedriver)
    p = re.compile( r'[\d]+')



    n = 2010
    for i in range(n, n+1):
        URL = 'http://allrecipes.com/cook/' + str(i) + '/reviews/'
        driver.get(URL)

        print( '\n' + 'COOK: ' +str(i))

        elems = driver.find_elements_by_class_name("profile-review-card")
        for x in elems:
            z = x.find_element_by_class_name('ng-scope')
            link = z.get_attribute('href')

            if link.find('personal') == -1:
                link = link[29:].rstrip('/').split('/')

                recipenum = link[0]
                name = link[1]
                # recipenum = p.findall(z.get_attribute('href'))[0]

                zz = x.find_element_by_class_name('rated-review--stars')
                zz = zz.find_element_by_class_name('ng-scope')
                zz = zz.find_element_by_class_name('ng-isolate-scope')

                ranking = zz.get_attribute('data-rating')
                print( str(name) + ' '+ str(recipenum) , colored(ranking,'red'))






    driver.close()




#GHOST

#
#
# import ghost
# ghost = ghost.Ghost()
# session = ghost.start()
# session.wait_timeout = 999
#
#
# page, resources = session.open('http://allrecipes.com/cook/2010/reviews/')
#
#
# # page, resources = session.open('https://www.google.com')
#
# soup2 = BeautifulSoup(page.content, 'html.parser')
# soup = BeautifulSoup(page.content)
#
# reviews = soup.find_all('article', class_ ='profile-review-card' )
#
#
#
# reviews2 = soup2.find_all('article', class_ ='profile-review-card' )
#
#




#
# #PYQT4
import sys
from PyQt4.QtGui import *
from PyQt4.QtCore import *
from PyQt4.QtWebKit import *
from lxml import html



#Take this class for granted.Just use result of rendering.
class Render(QWebPage):
  def __init__(self, url):
    self.app = QApplication(sys.argv)
    QWebPage.__init__(self)
    self.loadFinished.connect(self._loadFinished)
    self.mainFrame().load(QUrl(url))
    self.app.exec_()

  def _loadFinished(self, result):
    self.frame = self.mainFrame()
    self.app.quit()



# app = QApplication(sys.argv)
#
# w = QWidget()
# w.resize(250, 150)
# w.move(300, 300)
# w.setWindowTitle('Simple')
# w.show()
#
# sys.exit(app.exec_())


# url = 'http://pycoders.com/archive/'
url = 'http://allrecipes.com/cook/2010/reviews/'

r = Render(url)
result = r.frame.toHtml()
#This step is important.Converting QString to Ascii for lxml to process
# archive_links = html.fromstring(str(result.toAscii()))
archive_links = html.fromstring(result)

# archive_links = html.fromstring(str(result.encode('ascii')))
print(archive_links)




# >>> b'a string'.decode('ascii')
# 'a string'









#
# g = ghost.Ghost()
# with g.start() as session:
#     page, extra_resources = session.open("https://www.debian.org")
#     if page.http_status == 200 and \
#             'The Universal Operating System' in page.content:
#         print("Good!")
# y = x.get_attribute('innerHTML')

# ghost = ghost.Ghost()
# page, extra_resources = ghost.open("http://jeanphi.fr")
# assert page.http_status==200 and 'jeanphix' in ghost.content
#
# n= 2010
# for i in range(n,n):
#
#     # URL = 'http://allrecipes.com/cook/' + str(i) + '/reviews/'
#     #
#     # URL = 'http://allrecipes.com/cook/2010/reviews/'
#     # response = requests.get(URL ).content
#
#     URL = 'http://allrecipes.com/cook/2010/reviews/'
#     headers = {'user-agent', 'Mozilla/5.0'}
#     response = requests.get(URL,headers=headers).content
#
#
#     soup = BeautifulSoup(response, 'html.parser')
#
#     #TITLE
#     X = soup.find_all('article', class_ = "profile-review-card"  )
