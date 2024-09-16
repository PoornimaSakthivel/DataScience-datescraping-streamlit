import time
import os
import pandas as pd
from altair import value
import numpy as np
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
import tensorflow as tf
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.keys import Keys
from selenium.common.exceptions import NoSuchElementException
statedict={}
routename=[]
routelinks=[]
arr = np.array([])
# Function to load existing CSV data into a NumPy array
def load_existing_data(filename):
    if os.path.exists(filename):
        return np.loadtxt(filename, delimiter=',', dtype=str, skiprows=1)  # Skip header row
    return np.array([]).reshape(0, 11)  # Assuming 11 columns

# Load existing data
existing_data = load_existing_data('array.csv')      
def pageloadfun():
 WebDriverWait(driver, 1000).until(
        lambda d: d.execute_script('return document.readyState') == 'complete'
    )
 print("Page has fully loaded.")

#Clicking statetransport and 
def clickingstatetransport(s,n):
    elements = driver.find_elements(By.XPATH, s)
#driver.execute_script("arguments[0].scrollIntoView(true);", elements)
    pageloadfun
#time.sleep(15)
#driver.execute_script("window.scrollBy(0, 3000);")
    elements[n].click()
#printstategovt name
    stategovte=driver.find_element(By.XPATH, '//h1')
    stategovtname=stategovte.text
    print(stategovtname)
    return stategovtname

#Storing route name and corresponding state transport in dict
def retrievingroutesandroutelinks(elements,linkele):
    webelements=driver.find_elements(By.XPATH, elements)
    size =len(webelements)
    print(size)
#printing routenames
    webnametexts = [webname.text for webname in webelements]
    routeslink=driver.find_elements(By.XPATH, linkele)
    hrefs=[routelink.get_attribute('href') for routelink in routeslink]
    for text in webnametexts:
       
        print(text)
        routename.append(text)
        print("Enterted routes names ")
    for href in hrefs:
        print(href)
        routelinks.append(href)
        print("Enterted routes link ")
    if len(routename) == len(routelinks):
    # Combine lists into a dictionary
        statedict = dict(zip(routename, routelinks))
    else:
        print("Error: The number of webnames and hrefs do not match.")
    print(statedict)
    return statedict
def getstatetransport():
    
#printstategovt name
    stategovte=driver.find_element(By.XPATH, '//h1')
    stategovtname=stategovte.text
    print(stategovtname)
    return stategovtname

#getting the link and 
def retrievinglinks(linkele):
   #printing routeslink
    routeslink=driver.find_elements(By.XPATH, linkele)
    hrefs = [routelink.get_attribute('href') for routelink in routeslink]
    for href in hrefs:
        print(href)
        print("Enterted routes link ")
def retrievingwebnames(elements):
    webelements=driver.find_elements(By.XPATH, elements)
    size =len(webelements)
    print(size)
#printing routenames
    webnametexts = [webname.text for webname in webelements]
    for text in webnametexts:
        # Add your condition to select the specific element
        print(text)
        print("Enterted routes names ")
def routeclick(linkele1,n1):
    routeslinks=driver.find_elements(By.XPATH, linkele1)
    actions = webdriver.ActionChains(driver)
# Move to the element and click
    actions.move_to_element((routeslinks[n1])).click().perform()
def clickviewbuses():
    viewbuseselements=driver.find_elements(By.XPATH, '//*[text()="View Buses"]')
    viewbuseselements[1].click
    time.sleep(5)
    pageloadfun
def clickviewbus():
    viewbuseselement=driver.find_element(By.XPATH, '//*[text()="View Buses"]').click()
    time.sleep(5)
    pageloadfun
def pagescrolling():
    for i in range(150):  # Scroll and wait 5 times
        driver.execute_script("window.scrollBy(0, 1000);")
        WebDriverWait(driver, 100).until(
            EC.presence_of_element_located((By.XPATH,'//*[@class="box-info"]')))
    pageloadfun
def dyncpagescrolling(bussize):
    currentsize=checksize()
    print(currentsize)
    while currentsize==bussize:
    #for i in range(150):  # Scroll and wait 5 times
        #pagedown(3)
        pagescrolling()
        time.sleep(15)
        #driver.execute_script("window.scrollBy(0, 1000);")
        currentsize=checksize()
        print("In scrolling size "+str(currentsize))
        WebDriverWait(driver, 100).until(
            #sizeofelements==bussize)
            EC.presence_of_element_located((By.XPATH,'//*[@class="box-info"]')))
        
    pageloadfun
def checksize():
    rows=driver.find_elements(By.XPATH, '//*[contains(@class,"clearfix bus-item-details")]')
    print("In check sizeno of rows"+str(len(rows)))
    size=len(rows)
    return size
def pagescrolling1():
    for i in range(48):  # Scroll and wait 5 times
        driver.execute_script("window.scrollBy(0, 2200);")
        WebDriverWait(driver, 100).until(
            EC.presence_of_element_located((By.XPATH,'//*[contains(@class,"data_wrap")]')))
    pageloadfun
def clicktab(n):
    pageloadfun
    elementpath='//*[contains(@class,"paginationTable")]//div[' + str(n) + ']'
    print(elementpath)
    element1=driver.find_element(By.XPATH,elementpath)
    #driver.execute_script("window.scrollBy(0, 6000);")
    #pageloadfun
    #driver.execute_script("arguments[0].scrollIntoView(true);", element1)
    if element1.is_displayed():
        element1.click()
    else:
        print("Element is not visible.")
def pagedown(n2):
    for i in range(n2):
        driver.find_element(By.TAG_NAME, 'body').send_keys(Keys.PAGE_DOWN)
        time.sleep(8)
def dynamicscrolling():
    time.sleep(10)
    e1=driver.find_element(By.XPATH,'//*[contains(@class,"busFound")]')
    noofbus=e1.text
    bussize = int(noofbus.split()[0])
    
    print(noofbus)
    print("size of element")
    print(bussize)
    type(bussize)
    busdetailsrows=driver.find_elements(By.XPATH, '//*[contains(@class,"clearfix bus-item-details")]')
    print("sizeno of rows"+str(len(busdetailsrows)))
    size=len(busdetailsrows)
    while size < bussize:
        pagedown(4)
        time.sleep(15)
        #time.sleep(15)
        busdetailsrows=driver.find_elements(By.XPATH, '//*[contains(@class,"clearfix bus-item-details")]')
        print("sizeno of rowsloop"+str(len(busdetailsrows)))
        new_size=len(busdetailsrows)
        if new_size==size:
            break
        size=new_size


def retrievebusdetails(routename1,routelink1):

    time.sleep(3)
    #arr=np.append(routename1,routelink1)
    #print(arr)
    busrows=driver.find_elements(By.XPATH,'//*[contains(@class,"clearfix bus-item-details")]')
    noofbusrows=len(busrows)
    print(noofbusrows)
    data = []
    for i in range(noofbusrows):
        try:
            print(i)
            time.sleep(4)
            busname=driver.find_elements(By.XPATH,'//*[contains(@class,"travels")]')[i].text
            bustype=driver.find_elements(By.XPATH,'//*[contains(@class,"bus-type")]')[i].text
            depttime=driver.find_elements(By.XPATH,'//*[contains(@class,"dp-time")]')[i].text
            arrtime=driver.find_elements(By.XPATH,'//*[contains(@class,"bp-time")]')[i].text
            dur=driver.find_elements(By.XPATH,'//*[contains(@class,"dur")]')[i].text
            rating=driver.find_elements(By.XPATH,'//*[contains(@class,"rating")]//div[1]//span')[i].text
            price=driver.find_elements(By.XPATH,'//*[contains(@class,"fare")]//span[contains(@class,"f")]')[i].text
            seatav=driver.find_elements(By.XPATH,'//*[contains(@class,"column-eight")]//div[1]')[i].text
            values=[statetransportname,routename1,routelink1,busname,bustype,depttime,arrtime,dur,rating,price,seatav]
            #values=[routename1,routelink1,busname[i].text,bustype[i].text,depttime[i].text,arrtime[i].text,dur[i].text,rating[i].text,price[i].text,seatav[i].text]
            data.append(values)
            #arr=np.array(values)
            print(data)
            #arr=np.append(busname[i].text,bustype[i].text,depttime[i].text,arrtime[i].text,dur[i].text,rating[i].text,price[i].text,seatav[i].text,)
        except IndexError:
            # Handle the case where an index is out of range
            print(f"IndexError at bus {i}. Some details might be missing.")
            data.append([statetransportname, routename1, routelink1, "N/A", "N/A", "N/A", "N/A", "N/A", "N/A", "N/A", "N/A"])
            
        except Exception as e:
            # Handle any other exceptions
            print(f"An error occurred: {e}")
            data.append([statetransportname, routename1, routelink1, "N/A", "N/A", "N/A", "N/A", "N/A", "N/A", "N/A", "N/A"])
            #busname="value is not present"
            #arr=np.array(values)
            #np.savetxt('array.csv', arr, delimiter=',', fmt='%d')
            #print(arr)
        print(i)
    #print(arr)
    '''newarr = np.array(data)
    print(newarr)
    combined_array = np.concatenate((existing_data, newarr), axis=0) if existing_data.size else newarr'''

    # Save the combined NumPy array to CSV
    df = pd.DataFrame(data, columns=['State Transport Name', 'Routename', 'Route Link', 'Bus Name', 'Bus Type', 'Departure Time', 'Arrival Time', 'Duration', 'Rating', 'Price', 'Seat Availability'])
    file_exists = os.path.isfile('array.csv')

    if file_exists:
        # Load existing data
        existing_df = pd.read_csv('array.csv')
        # Append new data to existing data
        combined_df = pd.concat([existing_df, df], ignore_index=True)
    else:
        # If the file does not exist, use the new data as the DataFrame
        combined_df = df

    # Save the combined DataFrame to CSV
    combined_df.to_csv('array.csv', index=False)

    print("Data has been appended to 'array.csv'.")
    #df.to_csv('array.csv', index=False, header=True)
    #np.savetxt('array.csv', arr, delimiter=',', fmt='%s')
    
    '''arr = arr.astype(str)
    with open('array.csv', 'a') as file:
        np.savetxt('array.csv', arr, delimiter=',', fmt='%s')'''
    #print(arr)
    #print(values)

#print(arr)


     
    
      




#Launching chrome browser
driver=webdriver.Chrome()
#launching redbus
driver.get("https://www.redbus.in/online-booking/hrtc/?utm_source=rtchometile")
driver.maximize_window()
print("Chrome browser launched successfully with redbus")
time.sleep(5)
statetransportname=getstatetransport()

#retrieving route links and routes names
dict1=retrievingroutesandroutelinks('//*[@class="route_details"]//a','//*[@class="route_details"]//a')
print(dict1)
print(len(dict1))

pagedown(3)
pageloadfun

#clicking on the pagination
try:
    element1=driver.find_elements(By.XPATH,'//*[contains(@class,"paginationTable")]//div')
    sizeoftabs=len(element1)

    for i in range(1,sizeoftabs):
    
            element1[i].click()
            dict1=retrievingroutesandroutelinks('//*[@class="route_details"]//a','//*[@class="route_details"]//a')
   
    time.sleep(50)
    print(dict1)
    print(len(dict1))
except IndexError:
            # Handle the case where an index is out of range
            print(f"IndexError at bus {i}. Some details might be missing.")


for key, value in dict1.items():
    driver.get(value)
    
    time.sleep(20)
    try:
        clickviewbus()
        e1=driver.find_element(By.XPATH,'//*[contains(@class,"busFound")]')
        noofbus=e1.text
        bussize = int(noofbus.split()[0])

        print(noofbus)
        print("size of element")
        print(bussize)
        type(bussize)
        pageloadfun()
        time.sleep(15)
        dynamicscrolling()
        retrievebusdetails(key,value)
   
    except NoSuchElementException as e:
        print("noelement")
    time.sleep(2)
    