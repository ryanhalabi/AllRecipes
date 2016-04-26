import requests
import json
import pprint as pp
import matplotlib.pyplot as mp
import numpy as np
import matplotlib.patches as mpatches
from bs4 import BeautifulSoup
import re
from termcolor import colored

# MY ID 30967710



key = '8ef24472-a6cb-4922-926f-7094ce4e4e5f'
endpoint = 'https://na.api.pvp.net/'


# /observer-mode/rest/featured




parameters = {}
parameters['api_key'] = key




# endpoint = endpoint + 'observer-mode/rest/featured'
# response = requests.get(endpoint, params=parameters).json()
#
#
# # endpoint = endpoint + 'api/lol/na/v1.4/summoner/by-name/RiotSchmick'
# # response = requests.get( endpoint, parameters ).json()
#
#
# endpoint = endpoint + 'observer-mode/rest/featured'
# response = requests.get(endpoint, params=parameters).json()


# https://na.api.pvp.net/api/lol/na/v1.4/summoner/30967710?api_key=8ef24472-a6cb-4922-926f-7094ce4e4e5f


#SUMMONER INFO
# endpoint = endpoint + 'api/lol/na/v1.4/summoner/1,30967709,30967710'
# response1 = requests.get(endpoint, params=parameters).json()


#SUMMONER GAMES
# endpoint = endpoint + 'api/lol/na/v1.3/game/by-summoner/30967710/recent'
# response = requests.get(endpoint, params=parameters).json()




# BUILD LIST OF SUMMONERS


# endpoint = endpoint + 'api/lol/na/v1.4/summoner/'
#
# for i  in range (1,41,40):
#
#     search = ''
#     for j in range(i,i+40,1):
#         search = search  + str(j) + ','
#     search = search[:-1]
#
#     endpoint = endpoint + search
#     response = requests.get(endpoint, params=parameters).json()
#



# endpoint = endpoint + 'api/lol/na/v1.3/game/by-summoner/30967710/recent'
# response = requests.get(endpoint, params=parameters).json()

# /api/lol/{region}/v1.3/stats/by-summoner/{summonerId}/summary

# /api/lol/{region}/v1.3/stats/by-summoner/{summonerId}/ranked



# endpoint = endpoint + 'api/lol/na/v1.3/stats/by-summoner/50967711/summary'
# response = requests.get(endpoint, params=parameters).json()

# endpoint = endpoint + 'shards'
# response = requests.get(endpoint, params=parameters).json()

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













n= 2010
for i in range(n,n+1):

    URL = 'http://allrecipes.com/cook/' + str(i) + '/reviews/'

    URL = 'http://allrecipes.com/cook/2010/reviews/'
    response = requests.get(URL ).content
    soup = BeautifulSoup(response, 'html.parser')


    import pprint
    pp = pprint.PrettyPrinter(indent=2)
    pp.pprint(response)



    #TITLE
    X = soup.find_all('div', class_ = 'grid-profile-card'  )

    Y = soup.find_all('h4', class_ ='light' )[0].text



    # if len(title) > 0:
    #     title = title[0].text
    #     letters = soup.find_all("span", class_="recipe-ingred_txt added")
    #     print('\n\n')
    #     print(colored(title,'red'))
    #
    #     ingredients = {}
    #     for x in letters:
    #
    #         y = x.text
    #         y = y.replace('(','')
    #         y = y.replace(')','')
    #         print(y)
    #
    #         Q=[]
    #         # Q =   [int(s) for s in y.split() if s.isdigit()]
    #         text = y.split()
    #         temp = []
    #         #STRIP OUT QUANTITIES
    #         for z in text:
    #             if z.isdigit():
    #                 Q.append(int(z))
    #                 temp.append(z)
    #             elif '/' in z:
    #                 if z.split('/')[0].isdigit() and z.split('/')[1].isdigit():
    #                     Q.append( int(z.split('/')[0])/ int(z.split('/')[1]))
    #                     temp.append(z)
    #             elif '.' in z:
    #                 if z.split('.')[0].isdigit() and z.split('.')[1].isdigit():
    #                     Q.append( int(z.split('.')[0])+ (.1)**len(z.split('.')[1]) *int(z.split('.')[1]))
    #                     temp.append(z)
    #
    #         for x in temp:
    #             text.remove(x)
    #
    #         # print(text)
    #         #MULTIPLY QUANTITIES TO GET AMOUNT
    #         if len(Q) >0:
    #             q = np.prod(Q)
    #         else:
    #             q = 0
    #
    #         #PULL OUT UNIT
    #         for z in text:
    #             # print(z)
    #             if z in Volume.keys():
    #                 q = q*Volume[z]
    #                 text.remove(z)
    #                 unit = 'teaspoon'
    #                 break
    #             elif z in Mass.keys():
    #                 q = q*Mass[z]
    #                 text.remove(z)
    #                 unit = 'ounce'
    #                 break
    #             elif z in Length.keys():
    #                 q = q*Length[z]
    #                 text.remove(z)
    #                 unit = 'cm'
    #                 break
    #             else:
    #                 unit = 'none'
    #
    #         y = " ".join(text)
    #         # print(y)
    #         y = y.replace( 'can', '')
    #         y = y.replace( '  ', ' ')
    #         y = y.lstrip(' ').rstrip(' ')
    #
    #
    #
    #
    #         ingredients[ y ] = [q, unit]
    #         print(colored('type:','yellow'),y, '||' ,colored('quantity:','yellow'),q, unit, '\n')
    #         # print('unit:',u,'\n')
    #
    #
    #     Recipes[ title] = ingredients
    #
    #







        #
        #
        # import urllib.request, json
        #
        # response = urllib.request.urlopen(URL)
        # data = json.loads(str(response.read()))
        # print(data)



        # https://na.api.pvp.net
        # /api/lol/na/v1.3/game/by-summoner/30967710/recent?api_key=8ef24472-a6cb-4922-926f-7094ce4e4e5f

        #
        # import requests
        # import json
        # import pprint as pp
        # import matplotlib.pyplot as mp
        # import numpy as np
        # import matplotlib.patches as mpatches
        #
        #
        #
        #
        #
        # sunlight_key = '8afdfcd87c374103a98288c47cedd067'
        # secrets_key = 'b6f95391414454e2c04d85c7520d40ea'
        #
        # #http://transparencydata.com/api/:version/
        # #http://transparencydata.org/api/1.0/entities.json?apikey=YOUR_KEY&search=Barack+Obama&type=politician
        #
        #
        #
        #
        #
        # def top(parameters,n, key=sunlight_key):
        #     '''
        #     look up entity id
        #     '''
        #     parameters['apikey'] = key
        #     endpoint = 'http://transparencydata.com/api/1.0/aggregates/pols/top_%s.json?' %(n)
        #     response = requests.get(endpoint, params=parameters).json()
        #     return(response)
        #     pass
        #
        #
        #
        #
        #
        #
        # def entities(parameters, key=sunlight_key):
        #     '''
        #     look up entity id
        #     '''
        #     parameters['apikey'] = key
        #     endpoint = 'http://transparencydata.org/api/1.0/entities.json'
        #     response = requests.get(endpoint, params=parameters).json()
        #     return(response)
        #     pass
        #
        #
        #
        #
        #
        # #obama id = 4148b26f6f1c437cb50ea9ca4699417a
        #
        # def sector(parameters,id, key=sunlight_key):
        #     '''
        #     industry data
        #     '''
        #     parameters['apikey'] = key
        #
        #     endpoint = 'http://transparencydata.com/api/1.0/aggregates/pol/%s/contributors/sectors.json' %(id)
        #     response =  requests.get(endpoint, params=parameters).json()
        #
        #     return(response)
        #     pass
        #
        #
        #
        #
        #
        # def bio(parameters, key=sunlight_key):
        #     '''
        #     word count data
        #     '''
        #     parameters['apikey'] = key
        #
        #     endpoint = 'https://congress.api.sunlightfoundation.com/legislators'
        #     response =  requests.get(endpoint, params=parameters).json()
        #
        #     return(response)
        #     pass
        #
        #
        #
        #
        #
        #
        # def words(parameters, key=sunlight_key):
        #     '''
        #     word count data
        #     '''
        #     parameters['apikey'] = key
        #
        #     endpoint = 'http://capitolwords.org/api/1/text.json'
        #     response =  requests.get(endpoint, params=parameters).json()
        #
        #     return(response)
        #     pass
        #
        #
        #
        #
        # #find top earners
        # param = {'cycle':2012 }
        #
        #
        #            #set to 40
        # a = top(param,600)
        # id = []
        # for x in a:
        #     id.append( {  'id' : x['id'], 'name' : x['name'] , 'seat' : x['seat']  , 'party' : x['name'].split(' ')[-1] })
        #
        # id = [x for x in id if x['seat'] == 'federal:senate']
        # g=[]
        # #for each top earner now find sector donations
        # for x in id:
        #     f = {}
        #     b = {}
        #     d = sector(param,x['id'])
        #     for y in d:
        #         del y['count']
        #     for y1 in d:
        #         f[str(y1['sector'] )] = y1['amount']
        #     f['first'] = x['name']
        #     f['party'] = x['party']
        #     g.append(f)
        #
        # for x in g:
        #     x['first'] = x['first'].rstrip(' (R)')
        #     x['first'] = x['first'].rstrip(' (D)')
        #     z = x['first'].split(' ')
        #     x['last'] = z[ len(z)-1]
        #     x['first']=  z[0]
        #
        # #del g[0]
        # #del g[8]
        # #del g[13]
        # #del g[16]
        # #del g[18]
        # #del g[21]
        # #del g[26]
        # #del g[26]
        # #del g[26]
        # #del g[28]
        # #add in bio_ids
        #
        # #for x in g:
        # #    print(g.index(x))
        # #    print(x['last'])
        # #    z = bio({'query':x['last']})['results'][0]
        # #    pp.pprint(z['last_name'])
        # #    x['bio'] = z['bioguide_id']
        #
        # h = []
        # for x in g:
        #     print(g.index(x))
        #     z = bio({'query':x['last']})['results']
        #     if len(z) ==1 :
        #         z = z[0]
        #         pp.pprint(z['last_name'])
        #         x['bio'] = z['bioguide_id']
        #         h.append(x)
        # g = h
        #
        # final = []
        #
        # for x in g:
        #     print(g.index(x), ' out of ', len(g) )
        #     z={}
        #     for y in x:
        #         print(y)
        #         if y == 'A':
        #             c = 0
        #             c += words({'bioguide_id': x['bio'], 'phrase' : 'agriculture'   })['num_found']
        #             c += words({'bioguide_id': x['bio'], 'phrase' : 'food'   })['num_found']
        #             c += words({'bioguide_id': x['bio'], 'phrase' : 'farmer'   })['num_found']
        #             c += words({'bioguide_id': x['bio'], 'phrase' : 'water'   })['num_found']
        #             z['Ag'] = c
        #           #  pp.pprint(z['Ag'])
        #         elif y == 'B':
        #             c = 0
        #             c += words({'bioguide_id': x['bio'], 'phrase' : 'communication'   })['num_found']
        #             c += words({'bioguide_id': x['bio'], 'phrase' : 'internet'   })['num_found']
        #             c += words({'bioguide_id': x['bio'], 'phrase' : 'phone'   })['num_found']
        #             c += words({'bioguide_id': x['bio'], 'phrase' : 'infrastructure'   })['num_found']
        #             z['Comm/Elec'] = c
        #            # pp.pprint(z['Comm/Elec'])
        #         elif y == 'C':
        #             c = 0
        #             c += words({'bioguide_id': x['bio'], 'phrase' : 'construction'   })['num_found']
        #             c += words({'bioguide_id': x['bio'], 'phrase' : 'homes'   })['num_found']
        #             c += words({'bioguide_id': x['bio'], 'phrase' : 'development'   })['num_found']
        #             z['Const'] = c
        #            # pp.pprint(z['Const'])
        #         elif y == 'D':
        #             c = 0
        #             c += words({'bioguide_id': x['bio'], 'phrase' : 'military'   })['num_found']
        #             c += words({'bioguide_id': x['bio'], 'phrase' : 'navy'   })['num_found']
        #             c += words({'bioguide_id': x['bio'], 'phrase' : 'army'   })['num_found']
        #             c += words({'bioguide_id': x['bio'], 'phrase' : 'air force'   })['num_found']
        #             c += words({'bioguide_id': x['bio'], 'phrase' : 'defense'   })['num_found']
        #             z['Defense'] = c
        #           #  pp.pprint(z['Defense'])
        #         elif y == 'E':
        #             c = 0
        #             c += words({'bioguide_id': x['bio'], 'phrase' : 'oil'   })['num_found']
        #             c += words({'bioguide_id': x['bio'], 'phrase' : 'gas'   })['num_found']
        #             c += words({'bioguide_id': x['bio'], 'phrase' : 'solar'   })['num_found']
        #             c += words({'bioguide_id': x['bio'], 'phrase' : 'renewables'   })['num_found']
        #             c += words({'bioguide_id': x['bio'], 'phrase' : 'frack'   })['num_found']
        #             z['Energy'] = c
        #          #   pp.pprint(z['Energy'])
        #         elif y == 'F':
        #             c = 0
        #             c += words({'bioguide_id': x['bio'], 'phrase' : 'finance'   })['num_found']
        #             c += words({'bioguide_id': x['bio'], 'phrase' : 'stocks'   })['num_found']
        #             c += words({'bioguide_id': x['bio'], 'phrase' : 'stock market'   })['num_found']
        #             c += words({'bioguide_id': x['bio'], 'phrase' : 'bank'   })['num_found']
        #             z['Finance'] = c
        #           #  pp.pprint(z['Finance'])
        #         elif y == 'H':
        #             c = 0
        #             c += words({'bioguide_id': x['bio'], 'phrase' : 'insurance'   })['num_found']
        #             c += words({'bioguide_id': x['bio'], 'phrase' : 'health'   })['num_found']
        #             c += words({'bioguide_id': x['bio'], 'phrase' : 'hospital'   })['num_found']
        #             c += words({'bioguide_id': x['bio'], 'phrase' : 'healthcare'   })['num_found']
        #             c += words({'bioguide_id': x['bio'], 'phrase' : 'health care'   })['num_found']
        #             z['Health'] = c
        #           #  pp.pprint(z['Health'])
        #         elif y == 'K':
        #             c = 0
        #             c += words({'bioguide_id': x['bio'], 'phrase' : 'lawyer'   })['num_found']
        #             c += words({'bioguide_id': x['bio'], 'phrase' : 'law'   })['num_found']
        #             c += words({'bioguide_id': x['bio'], 'phrase' : 'judge'   })['num_found']
        #             c += words({'bioguide_id': x['bio'], 'phrase' : 'prosecutor'   })['num_found']
        #             c += words({'bioguide_id': x['bio'], 'phrase' : 'court'   })['num_found']
        #             z['Law'] = c
        #           #  pp.pprint(z['Law'])
        #         elif y == 'M':
        #             c = 0
        #             c += words({'bioguide_id': x['bio'], 'phrase' : 'transportation'   })['num_found']
        #             c += words({'bioguide_id': x['bio'], 'phrase' : 'automotive'   })['num_found']
        #             c += words({'bioguide_id': x['bio'], 'phrase' : 'factory'   })['num_found']
        #             c += words({'bioguide_id': x['bio'], 'phrase' : 'uaw'   })['num_found']
        #             c += words({'bioguide_id': x['bio'], 'phrase' : 'car'   })['num_found']
        #             z['Transport'] = c
        #           #  pp.pprint(z['Transport'])
        #         elif y == 'P':
        #             c = 0
        #             c += words({'bioguide_id': x['bio'], 'phrase' : 'union'   })['num_found']
        #             c += words({'bioguide_id': x['bio'], 'phrase' : 'minimum wage'   })['num_found']
        #             c += words({'bioguide_id': x['bio'], 'phrase' : 'unemployment'   })['num_found']
        #             z['Labor'] = c
        # #            pp.pprint(z['Labor'])
        #
        #     final.append(dict(x,**z))
        #
        #
        #
        #
        #
        #
        #
        #
        #
        # all = mp.figure(1)
        #
        #
        #
        #
        # for x in final:
        #     X=[]
        #     Y=[]
        #     for y in x:
        #         print(y)
        #         if y == 'A':
        #             X.append(x['A'])
        #             Y.append(x['Ag'])
        #         elif y == 'B':
        #             X.append(x['B'])
        #             Y.append(x['Comm/Elec'])
        #         elif y == 'C':
        #             X.append(x['C'])
        #             Y.append(x['Const'])
        #         elif y == 'D':
        #             X.append(x['D'])
        #             Y.append(x['Defense'])
        #         elif y == 'E':
        #             X.append(x['E'])
        #             Y.append(x['Energy'])
        #         elif y == 'F':
        #             X.append(x['F'])
        #             Y.append(x['Finance'])
        #         elif y == 'H':
        #             X.append(x['H'])
        #             Y.append(x['Health'])
        #         elif y == 'K':
        #             X.append(x['K'])
        #             Y.append(x['Law'])
        #         elif y == 'M':
        #             X.append(x['M'])
        #             Y.append(x['Transport'])
        #         elif y == 'P':
        #             X.append(x['P'])
        #             Y.append(x['Labor'])
        #
        #
        #
        #     mp.plot(X, Y, 'bo', c=np.random.rand(3,1))
        #
        #
        #
        # mp.axis([0, 3500000, 0, 500])
        #
        #
        #
        # R = {}
        # D = {}
        # R['count'] = 0
        # D['count'] = 0
        # R['A'] = 0
        # D['A'] = 0
        # R['B'] = 0
        # D['B'] = 0
        # R['C'] = 0
        # D['C'] = 0
        # R['D'] = 0
        # D['D'] = 0
        # R['E'] = 0
        # D['E'] = 0
        # R['F'] = 0
        # D['F'] = 0
        # R['H'] = 0
        # D['H'] = 0
        # R['K'] = 0
        # D['K'] = 0
        # R['M'] = 0
        # D['M'] = 0
        # R['P'] = 0
        # D['P'] = 0
        #
        # R['Ag'] = 0
        # D['Ag'] = 0
        # R['Comm/Elec'] = 0
        # D['Comm/Elec'] = 0
        # R['Const'] = 0
        # D['Const'] = 0
        # R['Defense'] = 0
        # D['Defense'] = 0
        # R['Energy'] = 0
        # D['Energy'] = 0
        # R['Finance'] = 0
        # D['Finance'] = 0
        # R['Health'] = 0
        # D['Health'] = 0
        # R['Law'] = 0
        # D['Law'] = 0
        # R['Transport'] = 0
        # D['Transport'] = 0
        # R['Labor'] = 0
        # D['Labor'] = 0
        #
        #
        #
        #
        #
        #
        # for x in final:
        #     if x['party'] == '(R)':
        #         R['count'] += 1
        #         for y in x:
        #             print(y)
        #             if y == 'A':
        #                 R['A'] += float(x['A'])
        #                 R['Ag'] += float(x['Ag'])
        #             elif y == 'B':
        #                 R['B'] += float(x['B'])
        #                 R['Comm/Elec'] += float(x['Comm/Elec'])
        #             elif y == 'C':
        #                 R['C'] += float(x['C'])
        #                 R['Const'] += float(x['Const'])
        #             elif y == 'D':
        #                 R['D'] +=float(x['D'])
        #                 R['Defense'] +=float(x['Defense'])
        #             elif y == 'E':
        #                 R['E'] += float(x['E'])
        #                 R['Energy'] += float(x['Energy'])
        #             elif y == 'F':
        #                 R['F'] += float(x['F'])
        #                 R['Finance'] += float(x['Finance'])
        #             elif y == 'H':
        #                 R['H'] += float(x['H'])
        #                 R['Health'] += float(x['Health'])
        #             elif y == 'K':
        #                 R['K'] += float(x['K'])
        #                 R['Law'] += float(x['Law'])
        #             elif y == 'M':
        #                 R['M'] += float(x['M'])
        #                 R['Transport'] += float(x['Transport'])
        #             elif y == 'P':
        #                 R['P'] += float(x['P'])
        #                 R['Labor'] += float(x['Labor'])
        #
        #
        #     if x['party'] == '(D)':
        #             D['count'] += 1
        #             for y in x:
        #                 print(y)
        #                 if y == 'A':
        #                     D['A'] +=float(x['A'])
        #                     D['Ag'] += float(x['Ag'])
        #                 elif y == 'B':
        #                     D['B'] += float(x['B'])
        #                     D['Comm/Elec'] += float(x['Comm/Elec'])
        #                 elif y == 'C':
        #                     D['C'] += float(x['C'])
        #                     D['Const'] += float(x['Const'])
        #                 elif y == 'D':
        #                     D['D'] += float(x['D'])
        #                     D['Defense'] += float(x['Defense'])
        #                 elif y == 'E':
        #                     D['E'] += float(x['E'])
        #                     D['Energy'] += float(x['Energy'])
        #                 elif y == 'F':
        #                     D['F'] += float(x['F'])
        #                     D['Finance'] += float(x['Finance'])
        #                 elif y == 'H':
        #                     D['H'] += float(x['H'])
        #                     D['Health'] += float(x['Health'])
        #                 elif y == 'K':
        #                     D['K'] += float(x['K'])
        #                     D['Law'] += float(x['Law'])
        #                 elif y == 'M':
        #                     D['M'] += float(x['M'])
        #                     D['Transport'] += float(x['Transport'])
        #                 elif y == 'P':
        #                     D['P'] += float(x['P'])
        #                     D['Labor'] += float(x['Labor'])
        #
        #
        #
        #
        # party = mp.figure(2)
        #
        #
        #
        # X=[]
        # Y=[]
        # for y in R:
        #     print(y)
        #     if y == 'A':
        #         X.append(R['A'])
        #         Y.append(R['Ag'])
        #     elif y == 'B':
        #         X.append(R['B'])
        #         Y.append(R['Comm/Elec'])
        #     elif y == 'C':
        #         X.append(R['C'])
        #         Y.append(R['Const'])
        #     elif y == 'D':
        #         X.append(R['D'])
        #         Y.append(R['Defense'])
        #     elif y == 'E':
        #         X.append(R['E'])
        #         Y.append(R['Energy'])
        #     elif y == 'F':
        #         X.append(R['F'])
        #         Y.append(R['Finance'])
        #     elif y == 'H':
        #         X.append(R['H'])
        #         Y.append(R['Health'])
        #     elif y == 'K':
        #         X.append(R['K'])
        #         Y.append(R['Law'])
        #     elif y == 'M':
        #         X.append(R['M'])
        #         Y.append(R['Transport'])
        #     elif y == 'P':
        #         X.append(R['P'])
        #         Y.append(R['Labor'])
        #
        #
        #
        # X = [x / R['count'] for x in X]
        # Y =[x / R['count'] for x in Y]
        # mp.plot(X, Y, 'bo', c= 'r')
        #
        #
        #
        #
        #
        #
        #
        #
        #
        # X=[]
        # Y=[]
        # for y in D:
        #     print(y)
        #     if y == 'A':
        #         X.append(D['A'])
        #         Y.append(D['Ag'])
        #     elif y == 'B':
        #         X.append(D['B'])
        #         Y.append(D['Comm/Elec'])
        #     elif y == 'C':
        #         X.append(D['C'])
        #         Y.append(D['Const'])
        #     elif y == 'D':
        #         X.append(D['D'])
        #         Y.append(D['Defense'])
        #     elif y == 'E':
        #         X.append(D['E'])
        #         Y.append(D['Energy'])
        #     elif y == 'F':
        #         X.append(D['F'])
        #         Y.append(D['Finance'])
        #     elif y == 'H':
        #         X.append(D['H'])
        #         Y.append(D['Health'])
        #     elif y == 'K':
        #         X.append(D['K'])
        #         Y.append(D['Law'])
        #     elif y == 'M':
        #         X.append(D['M'])
        #         Y.append(D['Transport'])
        #     elif y == 'P':
        #         X.append(D['P'])
        #         Y.append(D['Labor'])
        #
        #
        #
        # X = [x / D['count'] for x in X]
        # Y =[x / D['count'] for x in Y]
        # mp.plot(X, Y, 'bo', c= 'b')
        #
        #
        #
        # all.suptitle('Contributions vs Mentions by Senator', fontsize=16)
        # all.savefig('indiv.jpg')
        #
        #
        # party.suptitle('Contributions vs Mentions by Party', fontsize=16)
        # party.savefig('party.jpg')
        #
        # mp.figure(1)
        # mp.xlabel('Contributions')
        # mp.ylabel('# of Mentions')
        #
        # mp.figure(2)
        # mp.xlabel('Contributions')
        # mp.ylabel('# of Mentions')
        #
        #
        # red_patch = mpatches.Patch(color='red', label='Republican')
        # blue_patch = mpatches.Patch(color='blue', label='Democrat')
        # mp.legend(handles=[red_patch,blue_patch])