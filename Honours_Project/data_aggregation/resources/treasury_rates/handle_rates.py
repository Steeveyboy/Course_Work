import sqlite3, glob, csv
from datetime import datetime

def create_table(conn):
    cur = conn.cursor()
    cur.execute("DROP table if exists treasury_rates;")
    conn.commit()
    query ="""
        CREATE TABLE 'treasury_rates'(
        "date_of" DATE NOT NULL,
        '1Mo' float,
        '2Mo' float,
        '3Mo' float,
        '4Mo' float,
        '6Mo' float,
        '1Yr' float,
        '2Yr' float,
        '3Yr' float,
        '5Yr' float,
        '7Yr' float,
        '10Yr' float,
        '20Yr' float,
        '30Yr' float
    );"""
    cur.execute(query)
    conn.commit()

def insert_rates(cur, csvfile):
    # print(csvfile)
    headers = ["date_of"] + [f"'{h.replace(' ', '')}'" for h in csvfile[0][1:]]
    # "date_of," + ",".join(csvfile[0][1:])
    full_statement = f"""
        INSERT INTO treasury_rates({",".join(headers)})
        VALUES ({','.join(['?' for _ in range(len(csvfile[0]))])});
    """
    for row in csvfile[1:]:
        # print(full_statement)
        # print(tuple(row))
        dat = datetime.strptime(row[0], "%m/%d/%Y").strftime("%Y-%m-%d")
        rowtup = tuple([dat] + [float(i) if i != '' else None for i in row[1:]])
        # print(rowtup)
        cur.execute(full_statement, rowtup)

def read_rates(conn):
    files = glob.glob('daily-treasury-rates*')
    cursor = conn.cursor()
    for file in files:
        with open(file, 'r') as fhand:
            csvfile = list(csv.reader(fhand))
            insert_rates(cursor, csvfile)
            conn.commit()

if __name__ == '__main__':
    conn = sqlite3.connect("../../options_database.db")
    create_table(conn)
    read_rates(conn)
    conn.close()


