import psycopg2
conn = psycopg2.connect(dbname='busel', user='busel_admin', 
                        password='masterAdminBusel#345', host='localhost')
cursor = conn.cursor()
print(cursor)
