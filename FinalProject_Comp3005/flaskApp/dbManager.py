import sqlite3

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

    def get_by_title(self, name):
        self.cur.execute(f"select * from Artwork where Title = '{name}';")
        data = self.cur.fetchone()
        dataMapped = {"Title": data[0], "Artist": data[1], "Image_Address": data[2],"Year": data[3], "Gallery": data[4], "Collection": data[5]}
        return dataMapped
    
    def get_many_by_attr(self, table, name):
        if table == "Gallery":
            self.cur.execute(f"select * from {table} where Gallery_Name LIKE '%{name}%' LIMIT 30;")
        else:
            self.cur.execute(f"select * from {table} where Title LIKE '%{name}%' LIMIT 30;")
        data = self.cur.fetchall()
        return data

    def get_gallery_art(self, name):
        self.cur.execute(f"with merged(Title, Year, Artist, Gallery, Location, Image_Address) AS (select Title, Year, Artist, Artwork.Gallery, Location, Image_Address from Artwork join Gallery on Artwork.Gallery = Gallery.Gallery_Name) select * from merged where Gallery = '{name}';")
        data = self.cur.fetchall()
        print(data)
        return data

    def get_owners(self, title):
        self.cur.execute(f"with contracts(Title, Patron_id, ContractId, percent_share) AS (select Artwork_Title, Patron_id, ContractId, percent_share from OwnershipContract where Artwork_Title = '{title}') select distinct Title, First_Name, Last_Name, Patron.Patron_ID from contracts join Patron on contracts.Patron_ID = Patron.Patron_ID;")
        data = self.cur.fetchall()
        return data

    def get_patron_collection(self, patron_ID):
        self.cur.execute(f"with contracts(Artwork_Title, Patron_ID, percent_share, ContractId, First_Name, Last_Name) AS (select Artwork_Title, Patron.Patron_ID, percent_share, ContractId, First_Name, Last_Name from OwnershipContract join Patron on OwnershipContract.Patron_ID = Patron.Patron_ID) Select * from contracts where Patron_ID = {patron_ID};")
        data = self.cur.fetchall()
        print(data)
        return data
        