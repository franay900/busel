import psycopg2
conn = psycopg2.connect(dbname='busel', user='busel_admin', 
                        password='masterAdminBusel', host='localhost')
cursor = conn.cursor()