import mysql.connector
from mysql.connector import Error
from sqlalchemy import create_engine
import pandas as pd
import re
from decimal import Decimal

def verify_connection(host, user, password,dbname) -> None:
    try:
        connection = mysql.connector.connect(
            host=host,
            user=user,
            password=password,
            database = dbname
        )

        if connection.is_connected():
            print(f"Successfully connected to MySQL server at {host} with user {user}")
            connection.close()
        else:
            print("Connection failed")

    except Error as e:
        print(f"Error: {e}")
        
def get(text):
    if isinstance(text, str):
    # Find all numbers in the text and return the first one
        match = re.search(r'\d+', text)
        if match:
         return match.group(0)
    return None

# Replace with your credentials
#DATABASE_URL = 'mysql+transport://root:Arudhra@1201@localhost/transport'
DATABASE_URL='mysql+pymysql://root:Arudhra%401201@localhost/redbustransport'

# Create the SQLAlchemy engine
engine = create_engine(DATABASE_URL, echo=True,pool_size=10, max_overflow=20)
print(engine)
#engine=verify_connection('localhost', 'root', 'Arudhra@1201','redbustransport')
df = pd.read_csv('array.csv')
print(df.dtypes)
df.columns = df.columns.str.strip()
df.rename(columns={
    'State Transport Name': 'statetransport',
    'Routename': 'route_name',
    'Route Link':'route_link',
    'Bus Name':'busname',
    'Bus Type':'bustype',
    'Departure Time':'departing_time',
    'Arrival Time':'reaching_time',
    'Duration':'duration',
    'Rating':'star_rating',
    'Price':'price',
    'Seat Availability':'seats_available'
    
}, inplace=True)
df['departing_time'] = pd.to_datetime(df['departing_time'], format='%H:%M', errors='coerce').dt.time
df['reaching_time'] = pd.to_datetime(df['reaching_time'], format='%H:%M', errors='coerce').dt.time

df['price'] = pd.to_numeric(df['price'], errors='coerce')
df['price'] = df['price'].apply(lambda x: Decimal(str(x)) if pd.notna(x) else None)
print("Columns in DataFrame:", df.columns)
print(df.head())

df['seats_available'] = df['seats_available'].apply(get)
df['seats_available'] = pd.to_numeric(df['seats_available'], errors='coerce')

#engine = verify_connection('localhost', 'root', 'Arudhra@1201','transport')
try:
    with engine.connect() as connection:
        result = connection.execute("SELECT 1")
        print(result.fetchone())
except Exception as e:
    print(f"Error connecting to the database: {e}")

df.to_sql('redbus_routes', engine, if_exists='append', index=False)

print("Data has been appended to 'bus_details' table in the MySQL database.")

# Close the engine
engine.dispose()