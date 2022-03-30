import os
import pymysql
import json

# inicia base de datos


class DataBase:
    def __init__(self):
        db_user = os.environ.get('GCLOUD_DB_USERNAME')
        db_password = os.environ.get('GCLOUD_DB_PASS')
        db_host = os.environ.get('GCLOUD_DB_CONNECTION')
        db_name = os.environ.get('GCLOUD_DB_NAME')

        self.connection = pymysql.connect(host=db_host,
                                          user=db_user,
                                          password=db_password,
                                          database=db_name,
                                          cursorclass=pymysql.cursors.DictCursor)

        self.cursor = self.connection.cursor()
        self.create_database()

    def create_database(self):
        sql = '''CREATE TABLE IF NOT EXISTS `games` (
	`id`	INT(10) NOT NULL,
	`type`	VARCHAR(20) DEFAULT '',
	`name`	VARCHAR(250) DEFAULT '',
	`rank`	INT(10) NOT NULL DEFAULT 0,
	`rating`	INT(10) NOT NULL DEFAULT 0,
	`username`	VARCHAR(50) DEFAULT '',
	`description`	TEXT ,
	`url`	VARCHAR(150) DEFAULT '',
	`url_image`	VARCHAR(250) DEFAULT '',
	`bggid`	INT(10) DEFAULT 0,
	`url_geeklist`	varchar(100) DEFAULT '',
	PRIMARY KEY(`id`))'''
    
        self.cursor.execute(sql)
        self.connection.commit()

    def delete_games(self):        
        self.cursor.execute('DELETE FROM games')
        self.connection.commit()

    def insert_game(self, item):
        try:
            self.cursor.execute("INSERT INTO games VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)", item)
            self.connection.commit()
        except Exception as e:
            raise

    def insert_update(self):
        try:
            self.cursor.execute("INSERT INTO updates VALUES (NOW())")
            self.connection.commit()
        except Exception as e:
            raise

    def get_games(self):
        sql = '''SELECT `type`,`name`,`rank`,rating,max(url_image) url_image,bggid, COUNT(*) cantidad FROM games
                WHERE  `rank` <> 0 AND rating >6.5
                GROUP BY `type`,`name`,`rank`,rating,bggid
                ORDER BY `rank` asc, rating DESC'''

        try:
            self.cursor.execute(sql)
            return json.dumps(self.cursor.fetchall())
        except Exception as e:
            raise    

    def get_games_by_bggid(self, bggid):        
        try:
            self.cursor.execute("SELECT * FROM games WHERE bggid = %s", bggid)
            return json.dumps(self.cursor.fetchall())
        except Exception as e:
            raise

    def get_version(self):
        try:
            self.cursor.execute('SELECT VERSION()')
            data = self.cursor.fetchone()
            return data['VERSION()']

        except Exception as e:
            raise
    def get_last_update(self):
        try:
            self.cursor.execute('SELECT MAX(date) as last_update FROM updates')
            data = self.cursor.fetchone()
            return data

        except Exception as e:
            raise

    def close(self):
        self.cursor.close()
        self.connection.close()
# fin base de datos
