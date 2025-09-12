import mysql.connector

# Your config
config = {
    'user': 'root',
    'password': '',
    'host': '127.0.0.1',
    'database': 'kl_aanwezig',
    'raise_on_warnings': True
}

# Connect
conn = mysql.connector.connect(**config)
cursor = conn.cursor()

# Run query
cursor.execute("""
    SELECT table_name 
    FROM information_schema.tables 
    WHERE table_schema = 'kl_aanwezig';
""")

# Fetch results
tables = cursor.fetchall()

print("Tables in database 'kl_aanwezig':")
for t in tables:
    print(t[0])

# Cleanup
cursor.close()
conn.close()
