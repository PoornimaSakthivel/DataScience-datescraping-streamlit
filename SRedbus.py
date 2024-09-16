import streamlit as st
import pandas as pd
import numpy as np
from PIL import Image
import mysql.connector
from sqlalchemy import create_engine, text
from datetime import timedelta



r = st.sidebar.radio('Navigation',['Home','Route Information and Bus details'])
ratings = ['1 to 3', '3 to 4', 'Above 4']
timings=['Morning','Afternoon','Night','Early Morning']
checkboxoptions = ['A/C', 'Non A/C']
checkboxoptions1 = ['Seater', 'Semi-Sleeper','Sleeper']
selected_options = []
selected_options1 = []
st.sidebar.selected_seat_types = []


statetransport = ['Kerala RTC Online Ticket Booking', 'TSRTC Online Bus Ticket Booking', 'West bengal transport corporation','Bihar state road transport corporation (BSRTC)','NORTH BENGAL STATE TRANSPORT CORPORATION','PEPSU (Punjab)','Chandigarh Transport Undertaking (CTU)','JKSRTC','HRTC','Kadamba Transport Corporation Limited (KTCL)']

def get_connection():
 
        connection = mysql.connector.connect(
            host="localhost",
            user="root",
            password="Arudhra@1201",
            database="redbustransport"
        )
        print("DB Conn is success")
        return connection
def get_unique_values(column_name):
    query = f"SELECT DISTINCT {column_name} FROM redbus_routes where statetransport='{selected_state_transport}'"  # Replace 'your_table' with your table name
    connection = get_connection()
    try:
        cursor = connection.cursor()
        cursor.execute(query)
        values = [row[0] for row in cursor.fetchall()]
    finally:
        connection.close()
    return values
def format_timedelta_to_hhmm(td):
    if isinstance(td, str):
        # Convert string to timedelta if needed
        try:
            td = pd.to_timedelta(td)
        except ValueError:
            return '00:00'  # or handle invalid string format

    if isinstance(td, timedelta):
        total_seconds = td.total_seconds()
        hours, remainder = divmod(total_seconds, 3600)
        minutes, _ = divmod(remainder, 60)
        return f"{int(hours):02}:{int(minutes):02}"
    else:
        return '00:00'  # Default for non-timedelta values

def format_time_to_hhmm(time_str):
    if pd.isna(time_str):
        return '00:00'
    if isinstance(time_str, str):
        try:
            return pd.to_datetime(time_str, format='%H:%M:%S').strftime('%H:%M')
        except ValueError:
            return time_str  # Return original string if it can't be converted
    else:
        return time_str  # If it's already a time object or other acceptable type

# Convert time from 'HH:MM:SS' to 'HH:MM'
def format_time_to_hhmm(time_str):
    if pd.isna(time_str):
        return '00:00'
    try:
        return pd.to_datetime(time_str, format='%H:%M:%S').strftime('%H:%M')
    except ValueError:
        return time_str

def get_route_data(route_name,start_fare_int,end_fare_int,selected_rating_set,selected_seat_type,selected_bustype_options,set_selected_departure_time):
    
    #query = f"SELECT busname,bustype,departing_time,reaching_time,duration,price,seats_available FROM redbus_routes WHERE route_name = '{route_name}'"
    #query = f"SELECT busname,bustype,departing_time,reaching_time,duration,star_rating,price,seats_available FROM redbus_routes WHERE route_name = '{route_name}' AND price BETWEEN {start_fare_int} AND {end_fare_int} AND star_rating {selected_rating_set} AND (bustype LIKE  '{selected_seat_type}') AND (bustype LIKE '{selected_bustype_options}')"
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
    st.write("Generated SQL Query:")
    st.code(query)
    connection = get_connection()
    try:
        cursor = connection.cursor()
        cursor.execute(query)
        data = cursor.fetchall()
    finally:
        connection.close()
    # Adjust columns as necessary based on your database schema
    #busname,bustype,departing_time,reaching_time,duration,price,seats_available
    
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



if r =='Home':
    st.title('Redbus Data Scraping with Selenium & Dynamic Filtering using Streamlit')

    image = Image.open(r'C:\Users\POORNIMA\Desktop\bus.png')  # Replace with your image file path
    # Display the image
    st.image(image, caption='Local Image', use_column_width=True)
elif r =='Route Information and Bus details':
    st.subheader("Route Information and Bus details filtering using Streamlit")
    selected_state_transport = st.sidebar.selectbox(
    'Select State Transport',
    statetransport)

    column_name = 'route_name'  
    
   
    unique_values = get_unique_values(column_name)
    selected_route = st.sidebar.selectbox(
    'Select Route',
    unique_values)
    st.markdown("""
    <div style='text-align: left;'>
    
    </div>
    """, unsafe_allow_html=True)

    
    
    

    
    selected_departure_time = st.sidebar.selectbox(
        'Select Departure Time',
        timings
    )

    bustypeoptions = st.sidebar.multiselect(
        "Select Bus Type",
     ["A/C", "NON A/C"],
    ["A/C"]
    )

   

    seattypeoptions = st.sidebar.multiselect(
        "Select Seat Type",
     ["Seater", "Semi-Sleeper","Sleeper"],
    ["Seater", "Semi-Sleeper"]
    )

   



   


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
   
    




    
    selected_rating = st.sidebar.selectbox(
        'Select Ratings',
        ratings
    )

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
            bustype_conditions.append("bustype LIKE '%AC%' AND bustype NOT LIKE '%Non AC%'")
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
        st.write("Generated SQL Query:")
        



        
            









