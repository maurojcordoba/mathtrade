from flask import Flask, render_template,request
from databasemath import DataBaseMath

app = Flask(__name__)

@app.route('/')
def home():
    title = 'Math Trade'

    url_template = 'https://boardgamegeek.com{}'

    databasemath = DataBaseMath()
    data = databasemath.get_games()
        
    return render_template('math.html', data=data ,title=title,url_template=url_template) 

@app.route('/games/')
def games():
    title = 'Math Trade'
    bggid = request.args.get('bggid')

    url_template = 'https://boardgamegeek.com{}'
    
    databasemath = DataBaseMath()
    data = databasemath.get_games_by_bggid(bggid)
        
    return render_template('games.html', data=data ,title=title,url_template=url_template) 


def query_string():
    print(request)
    print(request.args)
    print(request.args.get('p1'))
    return 'Ok'

def pagina_no_encontrada(error):    
    return render_template('404.html'), 404

if __name__ == '__main__':
    app.add_url_rule('/query_string',view_func=query_string)

    app.register_error_handler(404,pagina_no_encontrada)

    app.run(host='0.0.0.0', debug=True, port=5000)