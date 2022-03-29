import sqlite3

# inicia base de datos
class DataBaseMath:
    def __init__(self):
        self.connection = sqlite3.connect('math.db')    
        self.cursor = self.connection.cursor()      
        self.create_database()

    def create_database(self):
        sql = '''CREATE TABLE IF NOT EXISTS "games" (
                "id" INTEGER NOT NULL,
				"type" VARCHAR(20) NULL DEFAULT '',
				"name" VARCHAR(250) NULL DEFAULT '',
				"rank" INTEGER not null default 0,
				"rating" number not null default 0,
				"from" VARCHAR(50) NULL DEFAULT '',
				"designer"  VARCHAR(250) NULL DEFAULT '',
				"players"  VARCHAR(30) NULL DEFAULT '',
				"time"  VARCHAR(50)NULL DEFAULT '',
                "description" TEXT NULL DEFAULT '',                
                "url" TEXT NULL DEFAULT NULL,     
                "bggid"	INTEGER DEFAULT 0,
                PRIMARY KEY ("id"))'''
        self.cursor.execute(sql)
        self.connection.commit()
    
    def delete_games(self):
        sql = '''DELETE FROM "games"'''
        self.cursor.execute(sql)
        self.connection.commit()

    def insert_game(self, item):        
        sql = "INSERT INTO games (id,type,name,rank,rating,username,description,url,url_image,bggid,url_geeklist) values (?,?,?,?,?,?,?,?,?,?,?)"
        
        try:
            self.cursor.execute(sql, item)
            self.connection.commit()
        except Exception as e:
            raise
    
    def get_games(self):
        sql = 'SELECT * FROM vw_games WHERE rating > 6.5'

        try:
            self.cursor.execute(sql);            
            items = [list(item) for item in self.cursor.fetchall()]

            return items
        except Exception as e:
            raise

    def get_games_by_bggid(self,bggid):
        sql = "SELECT * FROM games WHERE bggid = {}".format(bggid)

        try:
            self.cursor.execute(sql);
            items = [list(item) for item in self.cursor.fetchall()]

            return items
        except Exception as e:
            raise
    def get_last(self):
        sql = 'SELECT max(id) last FROM games'
        try:
            self.cursor.execute(sql);            
            return self.cursor.fetchone()[0]

        except Exception as e:
            raise

    def close(self):
        self.cursor.close()
        self.connection.close()
# fin base de datos