import nltk
import pprint as pp
import numpy as np
from bs4 import BeautifulSoup
from termcolor import colored
import requests
import re
from PyDictionary import PyDictionary
import pandas as pd
import time
import sqlite3
import sqlalchemy as sa

from file import function

#step size
T = 1000

conn = sqlite3.connect('allrecipe.db')
c = conn.cursor()


#retrieve previous recipes
lingred = []
engine = sa.create_engine('sqlite:///allrecipe.db')
try:
    query = "SELECT * FROM recipes limit 1"
    data = pd.read_sql(query,engine)
    L = list(pd.read_sql(query,engine).columns )
    if len(L) > 2:
        lingred = L[2:]
    print('found old data')
except:
    c.execute("CREATE TABLE recipes (id integer(10), name text , type text) ")
    print('table doesnt exist')



#retrieve graph variables
try:
    query = "SELECT total_ingred FROM graph order by step desc limit 1"
    data = pd.read_sql(query,engine)
    total = data.iloc[0,0]
    print('found graph table')
except:
    c.execute("CREATE TABLE graph (step integer(10), total_ingred integer(10), unique_ingred integer(10) ) ")
    print('no graph table, create')
    total = 0


#retrieve meta variables
try:
    query = "SELECT * FROM meta where name == 'last'"
    data = pd.read_sql(query,engine)
    start = data.iloc[0,1]
    print('found max')
except:
    c.execute("CREATE TABLE meta (name text, val integer(10) ) ")
    # query = "insert into meta VALUES ('last', " + str(T) + ')'
    query = "insert into meta VALUES ('last',  6663)"
    start = 6663
    c.execute(query)
    print('no max, creat meta')



Bad =   [   'container', 'package','can', 'jar']

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

TYPES = ['Appetizers and Snacks', 'BBQ & Grilling', 'Bread','Breakfast and Brunch', 'Chicken', 'Desserts' ,
         'Dinner', 'Drinks', 'Holidays and Events', 'Main Dish', 'Vegetarian',
         'Everyday Cooking', 'Fruits and Vegetables', 'Healthy Recipes','Ingredients',
         'Lunch', 'Meat and Poultry', 'Pasta and Noodles', 'Salad','Seafood',
         'Side Dish', 'Soups, Stews and Chili', 'Trusted Brands: Recipes and Tips', 'U.S. Recipes', 'World Cuisine']


Recipes = {}

graph = np.zeros([T,2])
# p = re.compile( r'[\d\/]+')

n= start+1
# n = 6917
# n = 6663
for i in range(n,n+T):
    print(i)
    start = time.time()
    URL = 'http://allrecipes.com/recipe/' + str(i)

    response = requests.get(URL ).content
    soup = BeautifulSoup(response, 'html.parser')
    end = time.time()
    ret = end-start

    start = time.time()
    #TITLE
    title = soup.find_all('h1', class_ ='recipe-summary__h1' )
    if len(title) > 0:
        title = title[0].text
        title = title.replace(' ', '_')
        title = title.replace('-', '_')
        title = title.replace("'", '_')
        title = title.lower()
        # print('\n\n')
        print( str(i-n) + '/'+ str(T) + ' ' + colored(title,'red'))

        ingredients = {}
        stype = []
        squant = []

        type = 'null'


        recipe_type = soup.find_all("span", class_="toggle-similar__title")

        for xx in recipe_type:
            zz = xx.text.replace('\r','').replace('\n','').lstrip(' ').rstrip(' ')
            # print(zz)
            if zz in TYPES:
                type = zz
                break


        letters = soup.find_all("span", class_="recipe-ingred_txt added")
        for x in letters:
            y = x.text

            y = y.replace('(','')
            y = y.replace(')','')

            # print(y)

            Q=[]
            # Q =   [int(s) for s in y.split() if s.isdigit()]
            text = y.split()
            temp = []
            #STRIP OUT QUANTITIES
            for z in text:
                # print(z)
                if z.isdigit():
                    Q.append(int(z))
                    temp.append(z)
                elif '/' in z:
                    if z.split('/')[0].isdigit() and z.split('/')[1].isdigit():
                        Q.append( int(z.split('/')[0])/ int(z.split('/')[1]))
                        temp.append(z)
                elif '.' in z:
                    o, d = 0, 0
                    if z.split('.')[0].isdigit():
                        o = int(z.split('.')[0])
                    if z.split('.')[1].isdigit():
                        d = (.1)**len(z.split('.')[1]) *int(z.split('.')[1])
                    if z.split('.')[0].isdigit() or z.split('.')[1].isdigit():
                        Q.append( o + d)
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

            # remove bad words
            for x in Bad:
                if y.find(x) != -1:
                   y = y.replace( x, '')


            # remove ', drained' types.  Bad idea?
            if len(y.split(',')) >1:
                B = y.split(',')[-1]
                y = y.replace(B,'')

            # remove extra spaces and commmas
            y = y.replace(',','')
            y = y.replace( '  ', ' ')
            y = y.lstrip(' ').rstrip(' ')
            y = y.replace(' ', '_')
            y = y.replace('-', '_')
            y = y.replace("'",'')
            y = y.lower()
            # print(y)

            if q != 0:
                squant.append(q)
                stype.append(y)
                ingredients[ y ] = [q, unit]

                if y not in lingred:
                    lingred.append(y)
                    c.execute("ALTER TABLE recipes ADD COLUMN `" + y + "` real DEFAULT 0" )

                total = total + 1
                # print(colored('type:','yellow'),y, '||' ,colored('quantity:','yellow'),q, unit)

                # print('\n\n')

        Recipes[ title   ] = ingredients


        graph[i-n] = [total, len(lingred)]
        c.execute("INSERT INTO graph ( step , total_ingred, unique_ingred  ) VALUES ('" + str(i) + "' , '" + str(total) + "' , " + str(len(lingred)) + " )")


        col = "' , '".join(stype)
        col= "'" + col +"'"

        A = [ str(x) for x in squant ]
        values = " , ".join( A )
        c.execute("INSERT INTO recipes (id, name, type," + col + " ) VALUES ('" + str(i) + "' , '" + title + "' , '" + type + "' , "  + values + " )")
        # update last checked
        query = "UPDATE meta SET val = '" + str(i) +"' WHERE name = 'last'"
        c.execute(query)
        conn.commit()

        # from PyDictionary import PyDictionary
        # dictionary=PyDictionary()

        # x= dictionary.synonym("package")
        # print(lingred)
    end = time.time()
    print(  round(ret,2), 'vs',  round(end - start,2), '\n')




#delete duplicates

#store duplicate
query = 'SELECT * FROM recipes GROUP BY id HAVING Count(id)>1'
dups = c.execute(query).fetchall()
#delete duplicates
query = 'DELETE FROM recipes WHERE id IN( SELECT id FROM recipes GROUP BY id HAVING Count(id)>1)'
c.execute((query))
#add duplicates back in
for item in dups:
    c.execute('insert into recipes values (' + ('?,'*len(item)).rstrip(',')  +')', item)
    print('delete dups')


conn.commit()
# conn.close()








pd.set_option('display.max_columns', 4)
# pd.set_option('display.height', 1000)
pd.set_option('display.max_rows', 20)
# pd.set_option('display.max_columns', 500)
# pd.set_option('display.width', 1000)
#pd.set_option('display.max_rows', 2)
# pd.set_option('expand_frame_repr', True)



#csv files were transformed into .db files and then joined on common entries
engine = sa.create_engine('sqlite:///allrecipe.db')

query = "SELECT id, type FROM recipes order by id asc"
data = pd.read_sql(query,engine)
print(data , '\n\n')

query = "SELECT * FROM meta limit 10"
data = pd.read_sql(query,engine)
print(data, '\n\n')


pd.set_option('display.max_columns', 4)
query = "SELECT * FROM graph order by step desc limit 1"
data = pd.read_sql(query,engine)
print(data, '\n\n')



print('null types')
query = "SELECT id, type FROM recipes where type = 'null' order by id asc"
data = pd.read_sql(query,engine)
print(data , '\n\n')
