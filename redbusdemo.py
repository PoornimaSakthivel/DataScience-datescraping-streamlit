#Library Imports
import streamlit as st
import pandas as pd
import numpy as np
from PIL import Image
import mysql.connector
from sqlalchemy import create_engine, text
from datetime import timedelta


#Streamlit Dropdown options
r = st.sidebar.radio('Menu',['Home','Route Information and Bus details','Data Analysis'])
ratings = ['1 to 3', '3 to 4', 'Above 4']
timings=['Morning','Afternoon','Night','Early Morning']
checkboxoptions = ['A/C', 'Non A/C']
checkboxoptions1 = ['Seater', 'Semi-Sleeper','Sleeper']
st.sidebar.selected_seat_types = []

#state transport List from scraped data
statetransport = ['Kerala RTC Online Ticket Booking', 'TSRTC Online Bus Ticket Booking', 'West bengal transport corporation','Bihar state road transport corporation (BSRTC)','NORTH BENGAL STATE TRANSPORT CORPORATION','PEPSU (Punjab)','Chandigarh Transport Undertaking (CTU)','JKSRTC','HRTC','Kadamba Transport Corporation Limited (KTCL)']
#DB connection
def get_connection():
 
        connection = mysql.connector.connect(
            host="localhost",
            user="root",
            password="Arudhra@1201",
            database="redbustransport"
        )
        print("DB Conn is success")
        return connection
#Getting routenames as per the state transport selection
def get_unique_values(column_name):
    query = f"SELECT DISTINCT {column_name} FROM redbus_routes where statetransport='{selected_state_transport}'"  
    connection = get_connection()
    try:
        cursor = connection.cursor()
        cursor.execute(query)
        values = [row[0] for row in cursor.fetchall()]
    finally:
        connection.close()
    return values
#Converting time(from DB) to HH:MM format
def format_timedelta_to_hhmm(td):
    if isinstance(td, str):
        
        try:
            td = pd.to_timedelta(td)
        except ValueError:
            return '00:00'  

    if isinstance(td, timedelta):
        total_seconds = td.total_seconds()
        hours, remainder = divmod(total_seconds, 3600)
        minutes, _ = divmod(remainder, 60)
        return f"{int(hours):02}:{int(minutes):02}"
    else:
        return '00:00'  

def format_time_to_hhmm(time_str):
    if pd.isna(time_str):
        return '00:00'
    if isinstance(time_str, str):
        try:
            return pd.to_datetime(time_str, format='%H:%M:%S').strftime('%H:%M')
        except ValueError:
            return time_str 
    else:
        return time_str  


def format_time_to_hhmm(time_str):
    if pd.isna(time_str):
        return '00:00'
    try:
        return pd.to_datetime(time_str, format='%H:%M:%S').strftime('%H:%M')
    except ValueError:
        return time_str

#Filter the results based on the inputs given by users
def get_route_data(route_name,start_fare_int,end_fare_int,selected_rating_set,selected_seat_type,selected_bustype_options,set_selected_departure_time):
    
    
    query = f"""
    SELECT busname, bustype, departing_time, reaching_time, duration, star_rating, price, seats_available
    FROM redbus_routes
    WHERE route_name = '{route_name}'
      AND price BETWEEN {start_fare_int} AND {end_fare_int}
      AND star_rating {selected_rating_set}
      AND ({selected_seat_type})
      AND ({selected_bustype_options})
      AND departing_time {set_selected_departure_time}
      
    """
    #st.write("Generated SQL Query:")
    #st.code(query)
    connection = get_connection()
    try:
        cursor = connection.cursor()
        cursor.execute(query)
        data = cursor.fetchall()
    finally:
        connection.close()
    
    
    df=pd.DataFrame(data, columns=['Bus_Name', 'Bus_type', 'Departing_Time', 'Reaching_Time','Duration','Rating','Price In Rs','Seats_available'])
    #df['Departing_Time'] = pd.to_datetime(df['Departing_Time'], format='%H:%M:%S', errors='coerce').dt.strftime('%H:%M%S')
    df['Departing_Time'] = df['Departing_Time'].apply(format_timedelta_to_hhmm)
    df['Reaching_Time'] = df['Reaching_Time'].apply(format_timedelta_to_hhmm)
    #df['Departing_Time'] = pd.to_datetime(df['Departing_Time'], format='%H:%M:%S', errors='coerce').dt.strftime('%H:%M')
    #df['Reaching_Time'] = pd.to_datetime(df['Reaching_Time'], format='%H:%M:%S', errors='coerce').dt.strftime('%H:%M')
    
    print("\nDataFrame after Conversion:")
    print(df)
    print("\nData Types after Conversion:")
    print(df.dtypes)
    df.fillna({'Departing_Time': '00:00', 'Reaching_Time': '00:00', 'Duration': '00:00'}, inplace=True)
    
    df['Departing_Time'] = df['Departing_Time'].apply(format_time_to_hhmm)
    df['Reaching_Time'] = df['Reaching_Time'].apply(format_time_to_hhmm)
    df['Duration'] = df['Duration'].apply(format_timedelta_to_hhmm)
    
    #df['Departing_time'] = pd.to_datetime(df['Departing_time'], format='%H:%M:%S').dt.time
    #df['Reaching_time'] = pd.to_datetime(df['Reaching_time'], format='%H:%M:%S').dt.time
    return df
    #return pd.DataFrame(data, columns=['Bus_Name', 'Bus_type', 'Departing_time', 'Reaching_time','Duration','Price','Seats_available'])

    #return pd.DataFrame(data, columns=['route_name', 'departure_time', 'fare', 'rating'])

#Data Analysis State Transport Vs No of Routes
def fetch_data():
    try:
        connection = get_connection()
        
        
        cursor = connection.cursor()
        
        
        query = """
        SELECT
        COUNT(DISTINCT CASE WHEN statetransport = 'HRTC' THEN route_name END) AS count_hrtc,
        COUNT(DISTINCT CASE WHEN statetransport = 'PEPSU (Punjab)' THEN route_name END) AS count_pepsu,
        COUNT(DISTINCT CASE WHEN statetransport = 'TSRTC Online Bus Ticket Booking' THEN route_name END) AS count_tsrtc,
        COUNT(DISTINCT CASE WHEN statetransport = 'Kerala RTC Online Ticket Booking' THEN route_name END) AS count_kerala,
        COUNT(DISTINCT CASE WHEN statetransport = 'JKSRTC' THEN route_name END) AS count_jksrtc,
        COUNT(DISTINCT CASE WHEN statetransport = 'West bengal transport corporation' THEN route_name END) AS count_westbengal,
        COUNT(DISTINCT CASE WHEN statetransport = 'Bihar state road transport corporation (BSRTC)' THEN route_name END) AS count_bihar,
        COUNT(DISTINCT CASE WHEN statetransport = 'NORTH BENGAL STATE TRANSPORT CORPORATION' THEN route_name END) AS count_northbengal,
        COUNT(DISTINCT CASE WHEN statetransport = 'Chandigarh Transport Undertaking (CTU)' THEN route_name END) AS count_ctu,
        COUNT(DISTINCT CASE WHEN statetransport = 'Kadamba Transport Corporation Limited (KTCL)' THEN route_name END) AS count_ktcl

        FROM redbus_routes;"""
        cursor.execute(query)
        results = cursor.fetchall()
        
       
        
    finally:
        connection.close()
        
        # Convert results to a DataFrame
    data1= {
            'State Transport': [
            'HRTC', 'PEPSU (Punjab)', 'TSRTC Online Bus Ticket Booking', 
            'Kerala RTC Online Ticket Booking', 'JKSRTC', 
            'West bengal transport corporation', 'Bihar state road transport corporation (BSRTC)',
            'NORTH BENGAL STATE TRANSPORT CORPORATION', 'Chandigarh Transport Undertaking (CTU)',
            'Kadamba Transport Corporation Limited (KTCL)'
        ],
        'Route Count': results[0] 
        }
    df1 = pd.DataFrame(data1)
    return df1
        
#Data Analysis State Transport Vs Max Fare
def fetch_data1():
    try:
        connection = get_connection()
        
        
        cursor = connection.cursor()
        
        
        query = """
        SELECT statetransport, MAX(price) AS MAX_fare
        FROM redbus_routes
        GROUP BY statetransport;"""
        cursor.execute(query)
        results1 = cursor.fetchall()
        
       
        
    finally:
        connection.close()
        
       
    df2 = pd.DataFrame(results1, columns=['State Transport', 'Max Fare'])
   
    return df2
        

       
#Streamlit Code for Menu and Menuoptions
#Home menu
if r =='Home':
    st.title('Redbus Data Scraping with Selenium & Dynamic Filtering using Streamlit')

    image = Image.open(r'C:\Users\POORNIMA\Desktop\bus.png')  
    # Display the image
    st.image(image, caption='Local Image', use_column_width=True)
#Route Information and Bus details Menu
elif r =='Route Information and Bus details':
    st.subheader("Route Information and Bus details filtering using Streamlit")

    #State Transport Dropdown
    selected_state_transport = st.sidebar.selectbox(
    'Select State Transport',
    statetransport)

    #Getting routename from DB
    column_name = 'route_name' 
    unique_values = get_unique_values(column_name)
    selected_route = st.sidebar.selectbox(
    'Select Route',
    unique_values)
    st.markdown("""
    <div style='text-align: left;'>
    </div>
    """, unsafe_allow_html=True)

    
    
    

    #Departure time Dropdown 
    selected_departure_time = st.sidebar.selectbox(
        'Select Departure Time',
        timings
    )

    #BusType-Multiselect
    bustypeoptions = st.sidebar.multiselect(
        "Select Bus Type",
     ["A/C", "NON A/C"],
    ["A/C"]
    )

   
    #SeatType-Multiselect
    seattypeoptions = st.sidebar.multiselect(
        "Select Seat Type",
     ["Seater", "Semi-Sleeper","Sleeper"],
    ["Seater", "Semi-Sleeper"]
    )

   



   

    #Select Fare-Slider
    start_fare, end_fare = st.sidebar.select_slider(
    "Select a range of bus fare",
        options=[
        "0",
        "500",
        "1000",
        "1500",
        "2000",
        "3000",
        "4000",
        "5000",
    ],
    value=("500", "1000"),
)
   
    




    #Rating Dropdown
    selected_rating = st.sidebar.selectbox(
        'Select Ratings',
        ratings
    )

    #Based on the user input storing the values 
    if st.sidebar.button('Get Bus Details'):
        st.write('Retrieving the Bus Results')
        #unique_routes = get_unique_values('route_name')
        #st.dataframe(pd.DataFrame(unique_routes, columns=['Route Name']))
        

        start_fare_int = int(start_fare)
        end_fare_int = int(end_fare)
        
     

       
        if selected_rating=='1 to 3':
            selected_rating_set='BETWEEN 1 AND 3'
        elif selected_rating=='3 to 4':
            selected_rating_set='BETWEEN 3 AND 4'
        elif selected_rating=='Above 4':
            selected_rating_set='>4'

        
        if selected_departure_time=='Morning':
            set_selected_departure_time="BETWEEN '06:00:00' AND '12:00:00'"
        elif selected_departure_time=='Afternoon':
            set_selected_departure_time="BETWEEN '12:00:00' AND '19:00:00'"
        elif selected_departure_time=='Night':
            set_selected_departure_time="BETWEEN '19:00:00' AND '24:00:00'"
        elif selected_departure_time=='Early Morning':
            set_selected_departure_time="BETWEEN '01:00:00' AND '06:00:00'"
      
        bustype_conditions = []
        if 'NON A/C' in bustypeoptions:
            bustype_conditions.append("bustype LIKE '%Non A/C%'")
            bustype_conditions.append("bustype LIKE '%Non AC%'")
        if 'A/C' in bustypeoptions:
            bustype_conditions.append("bustype LIKE 'A/C%'")
            bustype_conditions.append("bustype LIKE '%AC%' AND bustype NOT LIKE '%Non AC%' AND bustype NOT LIKE '%Non A/C%'")
        if bustype_conditions:
            selected_bustype_options = ' OR '.join(bustype_conditions)
        else:
            selected_bustype_options = "bustype LIKE '%'"   

      

        seat_conditions = []
        if 'Seater' in seattypeoptions:
            seat_conditions.append("bustype LIKE '%Seater%'")
        if 'Semi-Sleeper' in seattypeoptions:
            seat_conditions.append("bustype LIKE '%Semi-Sleeper%'")
        if 'Sleeper' in seattypeoptions:
             seat_conditions.append("bustype LIKE '%Sleeper%'")
        if seat_conditions:
            selected_seat_type = ' OR '.join(seat_conditions)
        else:
            selected_seat_type = "bustype LIKE '%'"
       

        
        

        data = get_route_data(selected_route,start_fare_int,end_fare_int,selected_rating_set,selected_seat_type,selected_bustype_options,set_selected_departure_time)

        st.dataframe(data)
        #st.write("Generated SQL Query:")
#Data Ananlysis
elif r =='Data Analysis':
    st.subheader("State Transport Vs No of Routes")
    data1 = fetch_data()
    data2=fetch_data1()
    #st.sidebar.write(data1)
    #st.sidebar.write(data2)
    #displaying charts
    st.bar_chart(data1.set_index('State Transport')['Route Count'])
    st.subheader("State Transport Vs Max Fare")
    st.line_chart(data2.set_index('State Transport')['Max Fare'])
    
        
       

   
        



        
            









