import sqlite3, json


class dbManager(): 
    def __init__(self):
        self.conn = sqlite3.connect('data/artwork_db', check_same_thread=False)
        self.cur = self.conn.cursor()
        # self.cur.execute(".mode column")

    def get_art(self):
        self.cur.execute("select * from Artwork;")
        for art in self.cur:
            print(art)
    
    def get_random(self):
        self.cur.execute("select * from Artwork order by random() limit 1;")
        data = self.cur.fetchone()
        dataMapped = {"Title": data[0], "Artist": data[1], "Image_Address": data[2],"Year": data[3], "Gallery": data[4], "Collection": data[5]}
        return dataMapped

    
# dbm = dbManager()
# print(dbm.get_random())