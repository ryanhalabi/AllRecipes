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



def cleanup(soup, Bad, Volume, Mass , Length, lingred,c,total):

    squant = []
    stype = []

    letters = soup.find_all("span", class_="recipe-ingred_txt added")
    for x in letters:
        y = x.text
        y = y.lower()
        # print(y)

        Q=[]
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



        #remove stuff in parantheses
        y = " ".join(text)
        y = re.sub(r'\(.*?\)', '', y)
        text = y.split()

        # remove bad words
        for x in text:
            if x in Bad:
               text.remove(x)

        y = " ".join(text)


        # remove ', drained' types.  Bad idea?
        if len(y.split(',')) >1:
            B = y.split(',')[-1]
            y = y.replace(B,'')

        # remove extra spaces and commmas
        y = y.replace(',','')
        y = y.replace(' ', '_')
        y = y.replace('-', '_')
        y = y.replace("'",'')
        y = ' '.join(y.split())
        # print(y)

        if q != 0:
            squant.append(q)
            stype.append(y)

            if y not in lingred:
                lingred.append(y)
                c.execute("ALTER TABLE recipes ADD COLUMN `" + y + "` real DEFAULT 0" )

            total = total + 1
            # print(colored('type:','yellow'),y, '||' ,colored('quantity:','yellow'),q, unit)

            # print('\n\n')
    return squant, stype

