from bs4 import BeautifulSoup
import re
import requests

from database import DataBase

def get_url(page):
    """genera url"""     
    return 'https://boardgamegeek.com/geeklist/297643/math-trade-argentina-abril-2022/page/{}'.format(page)    

#def main():
# conexion a base
database = DataBase()

# vacio tabla games
#database.delete_games()

# ultima pagina
web = requests.get(get_url(1))
soup = BeautifulSoup(web.content, 'html.parser', multi_valued_attributes=None)
last_page = soup.find('a', attrs={'title':'last page'}).text
m = re.search('\[(.\d+)\]', last_page)
last_page = int(m.group(1))

if last_page > 0:
    for page in range(1,last_page+1):
        print('Page: ', page)

        url = get_url(page)
        web = requests.get(url)
        soup = BeautifulSoup(web.content, 'html.parser', multi_valued_attributes=None)

        items = soup.find_all('div', attrs={'class':re.compile('^js-rollable article')})

        for item in items:

            temp = item.find('div', class_='fl')

            # url_geeklist
            url_geeklist = temp.a['href']

            # url
            url = item.a.next_sibling.next_sibling['href']
            # name
            name = temp.a.next_sibling.next_sibling.text
            # type
            type = temp.text
            type = type[type.find('.')+1:type.find(':')].strip()
            # id
            id = int(temp.a.text.replace('.',''))
            
            temp2 = item.find('span', class_='sf')

            # rating
            rating = temp2.text
            m = re.search('Rating.(.+?)[Overall|Unranked]', rating)
            rating = float(m.group(1).strip())
            
            # rank
            try:
                rank = temp2.a.text            
            except AttributeError:
                #print('Rank-AttributeError: ', id)
                rank = 0  
            rank = int(rank)

            # username
            username = item.find('div', class_='username').text
            username = username[1:username.find(')')]

            # description
            dd = item.find('dd', class_='doubleright')
            description = dd.encode(formatter="html5").strip()

            #url_image
            url_image = item.find('dd', class_='doubleleft').img['src']

            # bbgid
            m = re.search('\/.*\/(.*?)\/', url)
            
            bggid = int(m.group(1).strip())

            game = (id,type,name,rank,rating,username,description,url,url_image,bggid,url_geeklist)
            
            #database.insert_game(game)
    
    database.insert_update()

database.close()

#main()
