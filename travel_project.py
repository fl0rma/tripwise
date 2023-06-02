import streamlit as st
import pandas as pd
import numpy as np
import time
import warnings
from PIL import Image
import requests
import re

import time
import random
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from webdriver_manager.chrome import ChromeDriverManager
import googlemaps
import sklearn   
import gmaps
import gmaps.datasets

import warnings
warnings.filterwarnings('ignore')
from bs4 import BeautifulSoup

#To run the code: python -m streamlit run travel_project.py 
redy_to_run_flights = False
selected_place1 = False
selected_restaurant1 = False
ready_to_search = False

retreived_data = pd.DataFrame()
detailed_places_final = pd.DataFrame()
places_to_show = pd.DataFrame()
near_restaurants = pd.DataFrame()
hotels_to_show = pd.DataFrame()
top_3_prices = pd.DataFrame()
top_3_prices_return = pd.DataFrame()

# Image upload and text input section
image_path_1 = "./images/header.png"
image_1 = Image.open(image_path_1)

st.image(image_1)

st.title("Travel, because money returns. Time doesn’t!")
st.write(
  "Prepare to embark on a quest of data entry and watch as the magic of planning unfolds before your very eyes! Let's dive into the portal of inputs and shape your dream journey together!"
)

# Tabs section
st.subheader("Travel Insights Unleashed: Tell Us About Your Journey!")
tab1, tab2, tab3, tab4 = st.tabs(
  ["Intro", "When & Where to?", "Who is coming?", "How are you flying?"])

with tab1: #Intro
  st.write(
    ":warning:Warning: Side effects may include increased happiness, chronic wanderlust, and an inability to stay still!🌴🌞"
  )

  gif_url = "https://media.giphy.com/media/iKGV8COqlSUFbbl9KZ/giphy-downsized-large.gif"
  st.image(gif_url)

  # Load the city data from CSV
city_data = pd.read_csv('./data/worldcities.csv')

# Read the text file with the IATA codes (airport codes)
with open('./data/IATA_code.txt', 'r') as file:
  data = file.readlines()

# Create a list to store the data
rows = []

# Process each line of the text file
for line in data:
  # Split the line into individual values and remove escape characters
  values = line.strip().split('\t')
  rows.append(values)

# Create a pandas DataFrame from the data
IATA = pd.DataFrame(rows)
# Assign column names
new_column_names = ['IATA Code', 'City', 'Country']

# Update the column names of the DataFrame
IATA.columns = new_column_names

with tab2:
  city_choices = [""] + city_data['city_ascii'].unique()

  city_origin = st.selectbox(
        "🚀 Where are you blasting off from? Enter your city of origin: ",
        city_choices,
        index= 0,
        key='city_origin_' + str(len(city_choices))
    )
  
  # User input for the origin city name
  origin_city_name = city_origin

  # Convert the city name to lowercase and remove leading/trailing spaces
  origin_city_name = origin_city_name.lower().strip()
  matching_cities = IATA[IATA['City'].str.lower().str.contains(
    origin_city_name)]
  matched_city = matching_cities.iloc[0]
  iata_code = matched_city['IATA Code']
  origin_location_code = iata_code
  
  city_destination = st.selectbox(
    "🌍 Where do you want to land? Enter your desired destination city: ",
      city_choices,
      index= 0,
      key='city_destination' + str(len(city_choices))
    )
  
  destination_city_name = city_destination

   # Convert the city name to lowercase and remove leading/trailing spaces
  destination_city_name = destination_city_name.lower().strip()
  matching_cities = IATA[IATA['City'].str.lower().str.contains(
    destination_city_name)]
  matched_city = matching_cities.iloc[0]
  iata_code = matched_city['IATA Code']
  destination_location_code = iata_code

   # Function to validate the date format
  def validate_date_format(date):
    pattern = r'^\d{4}-\d{2}-\d{2}$'
    if not re.match(pattern, date):
      raise ValueError(
        "Invalid date format. Please enter a date in YYYY-MM-DD format.")
  
  departure_date = st.text_input(
    "📅 When do you want to take off? Enter your departure date (YYYY-MM-DD): ")
  
  # Validate departure date

  if departure_date:
    try:
      validate_date_format(departure_date)
    except ValueError as e:
      st.warning(str(e))
  
  return_date = st.text_input(
    "🏖️ When will you return from your amazing adventure? Enter your return date (YYYY-MM-DD): "
  )

  # Validate return date
  if return_date:
    try:
      validate_date_format(return_date)
      if return_date < departure_date:
        st.warning(
          "Return date should be after the departure date. Please enter a valid return date."
        )
    except ValueError as e:
      st.warning(str(e))


  st.write('Information completed?')
  agree = st.checkbox('Yes!.')
  disagree = st.checkbox("Not yet.")
  if agree:
    st.write(
      "Congrats! You've just unlocked a new level in the game of travel! Go to the next."
    )
    with st.spinner('Loading...'):
      time.sleep(3)
      st.success('Data successfully loaded!')
  if disagree:
    st.write("Oh no! The travel universe is eagerly awaiting your input!")

with tab3:

    def get_valid_integer_input(prompt):
        while True:
            try:
                value = int(st.text_input(prompt, value=0))
                if value==0:
                    return None
                else:
                    return value
            except ValueError:
                st.warning(
          "Oops! That's not a valid number. Please enter a number using only your toes!"
        )

    num_adults = get_valid_integer_input(
    "👥 How many fearless adults are embarking on this journey?")

    num_children = get_valid_integer_input(
    "🧒 Are you traveling with any daring children (under 16)? If yes, how many? "
  )

    num_infants = get_valid_integer_input(
    "👶 Are you bringing any adorable infants (under 2)? If yes, how many? ")

    st.write('Information completed?')
    agree = st.checkbox('All done.')
    disagree = st.checkbox("Nope.")
    if agree:
        st.write(
      "Congrats! You've just unlocked a new level in the game of travel! Go to the next."
    )
        with st.spinner('Loading...'):
            time.sleep(3)
            st.success('Data successfully loaded!')
    if disagree:
        st.write("Oh no! The travel universe is eagerly awaiting your input!")

with tab4:

  flight_classes = ['ECONOMY', 'PREMIUM_ECONOMY', 'BUSINESS', 'FIRST']
  selected_class = st.selectbox("🎩 What class of service would you like?",
                                flight_classes,
                                index=2)

  direct_flight = st.radio("✈️ Do you prefer a direct flight only?",
                           ('Yes', 'No'),
                           index=1)

  if direct_flight.lower() == 'yes':
    st.write("You're a jetsetter! Only direct flights for you! ✈️💨")
    non_stop = 'true'
  else:
    st.write(
      "You're an adventurous traveler! Layovers and connecting flights are your thing! ✈️🌍"
    )
    non_stop = 'false'
 
  budget_limit = get_valid_integer_input(
    "💰 Do you have a budget limit for this adventure? If so, please enter the amount in Euros: "
  )

  st.write('Information completed?')
  agree_ready = st.checkbox('Ready to fly!')
  disagree = st.checkbox("Need more time.")
  if agree_ready:
    st.write("Prepare yourself for an extraordinary journey!")
    with st.spinner('Loading...'):
      time.sleep(3)
      st.success('Data successfully loaded!')
      redy_to_run_flights = True
  if disagree:
    st.write("Oh no! The travel universe is eagerly awaiting your input!")

st.markdown('<hr style="border: 2px solid green;">', unsafe_allow_html=True)

if direct_flight.lower() == 'yes':
  non_stop = 'true'
else:
  non_stop = 'false'

###############___FLIGHTS CODE STARTS___###############

if redy_to_run_flights == True:
    api_key = open("./keys/key1.txt")
    for line in api_key:
        key = line

    secret = open("./keys/secret.txt")
    for line in secret:
        secret = line

    # Set your client ID and secret
    client_id = key  # Replace with your Amadeus client ID
    client_secret = secret  # Replace with your Amadeus client secret

    # Set the base URL and token endpoint
    base_url = "https://test.api.amadeus.com"
    token_endpoint = "/v1/security/oauth2/token"

    # Set the request payload to obtain the access token
    payload = {
        "grant_type": "client_credentials",
        "client_id": client_id,
        "client_secret": client_secret
    }

    return_flight_data = []
    departure_flight_data = []

    # Make a POST request to the token endpoint to get the access token
    response = requests.post(f"{base_url}{token_endpoint}", data=payload)

    # Check the response status code
    if response.status_code == 200:
        # Access token obtained successfully
        access_token = response.json()["access_token"]

        # Set the API base URL and endpoint
        api_base_url = "https://test.api.amadeus.com/v2/shopping"
        endpoint = "/flight-offers"
        # Set the query parameters for the departure trip
        departure_query_params = {
            "originLocationCode": origin_location_code,
            "destinationLocationCode": destination_location_code,
            "departureDate": departure_date,
            "adults": num_adults,
            "children": num_children,
            "infants": num_infants,
            "travelClass": flight_classes,
            "nonStop": non_stop,
            "currencyCode": "EUR",
            "maxPrice": budget_limit
        }

        # Set the query parameters for the return trip
        return_query_params = {
            "originLocationCode": destination_location_code,
            "destinationLocationCode": origin_location_code,
            "departureDate": return_date,
            "adults": num_adults,
            "children": num_children,
            "infants": num_infants,
            "travelClass": flight_classes,
            "nonStop": non_stop,
            "currencyCode": "EUR",
            "maxPrice": budget_limit
        }

        # Set the headers with the access token
        headers = {
            "Authorization": f"Bearer {access_token}",
            "Content-Type": "application/json"
        }

        # Make the GET request to retrieve flight offers for the departure trip
        departure_response = requests.get(f"{api_base_url}{endpoint}",
                                          params=departure_query_params,
                                          headers=headers)
        return_response = requests.get(f"{api_base_url}{endpoint}",
                                       params=return_query_params,
                                       headers=headers)

        # Check the response status code for the departure trip
        if departure_response.status_code == 200:
            # Request for departure trip successful
            departure_flight_offers = departure_response.json()
            # Create a list to store the departure flight offer details
            departure_flight_data = []

            # Process departure flight offers data
            for offer in departure_flight_offers["data"]:
                # Extract relevant information from each offer
                departure = offer["itineraries"][0]["segments"][0]["departure"]["iataCode"]
                arrival = offer["itineraries"][0]["segments"][-1]["arrival"]["iataCode"]
                airline = offer["validatingAirlineCodes"][0]
                price = offer["price"]["total"]
                departure_time = offer["itineraries"][0]["segments"][0]["departure"]["at"]
                arrival_time = offer["itineraries"][0]["segments"][-1]["arrival"]["at"]

                # Append the departure flight details to the list
                departure_flight_data.append({
                    "Departure": departure,
                    "Arrival": arrival,
                    "Airline": airline,
                    "Price (€)": price,
                    "Departure Time": departure_time,
                    "Arrival Time": arrival_time
                })

        if return_response.status_code == 200:
            # Request for return trip successful
            return_flight_offers = return_response.json()
            # Create a list to store the departure flight offer details
            return_flight_data = []

            # Process return flight offers data
            for offer in return_flight_offers["data"]:
                # Extract relevant information from each offer
                departure = offer["itineraries"][0]["segments"][0]["departure"]["iataCode"]
                arrival = offer["itineraries"][0]["segments"][-1]["arrival"]["iataCode"]
                airline = offer["validatingAirlineCodes"][0]
                price = offer["price"]["total"]
                departure_time = offer["itineraries"][0]["segments"][0]["departure"]["at"]
                arrival_time = offer["itineraries"][0]["segments"][-1]["arrival"]["at"]

                # Append the return flight details to the list
                return_flight_data.append({
                    "Departure": departure,
                    "Arrival": arrival,
                    "Airline": airline,
                    "Price (€)": price,
                    "Departure Time": departure_time,
                    "Arrival Time": arrival_time
                })

        departure_flights = pd.DataFrame(departure_flight_data)
        return_flights = pd.DataFrame(return_flight_data)

        if not departure_flights.empty:
            departure_flights['Departure Date'] = pd.to_datetime(
                departure_flights['Departure Time']).dt.date
            departure_flights['Departure Time'] = pd.to_datetime(
                departure_flights['Departure Time']).dt.time
            departure_flights['Arrival Date'] = pd.to_datetime(
                departure_flights['Arrival Time']).dt.date
            departure_flights['Arrival Time'] = pd.to_datetime(
                departure_flights['Arrival Time']).dt.time
            # Group the dataframe by "Airline" and sort the groups by price in ascending order
            grouped_departure_flights = departure_flights.groupby('Airline').apply(
                lambda x: x.sort_values('Price (€)'))
            # Reset the index of the grouped dataframe
            grouped_departure_flights = grouped_departure_flights.reset_index(drop=True)
            top_3_prices = grouped_departure_flights.groupby('Airline').head(3).reset_index(drop=True)
        else:
            top_3_prices = []

        if not return_flights.empty:
            # Convert Departure Time and Arrival Time columns to datetime type
            return_flights['Departure Date'] = pd.to_datetime(
                return_flights['Departure Time']).dt.date
            return_flights['Departure Time'] = pd.to_datetime(
                return_flights['Departure Time']).dt.time
            return_flights['Arrival Date'] = pd.to_datetime(
                return_flights['Arrival Time']).dt.date
            return_flights['Arrival Time'] = pd.to_datetime(
                return_flights['Arrival Time']).dt.time
            # Group the dataframe by "Airline" and sort the groups by price in ascending order
            grouped_return_flights = return_flights.groupby('Airline').apply(
                lambda x: x.sort_values('Price (€)'))
            # Reset the index of the grouped dataframe
            grouped_return_flights = grouped_return_flights.reset_index(drop=True)
            # Show the three lowest prices for each airline
            top_3_prices_return = grouped_return_flights.groupby('Airline').head(3).reset_index(drop=True)
        else:
            top_3_prices_return = []
else:
    st.write(':construction:')

###############___FLIGHTS CODE ENDS___###############

# Dataframe display section
st.subheader(
  'Behold, our top recommendation for your flight itinerary:'
)  #This dataframe will be coming from the code, this info is for testing, so we avoid making request while working on how the page looks

st.write("Top 3 choices for departure flight by airline:")


if len(top_3_prices) == 0:
    st.write(':construction:')
else:
    st.write(top_3_prices)

st.write("Top 3 choices for return flight by airline:")


if len(top_3_prices_return) == 0:
    st.write(':construction:')
else:
    st.write(top_3_prices_return)


# Image upload and text input section
image_path_2 = "./images/header2.png"
image_2 = Image.open(image_path_2)

st.image(image_2)

st.markdown('<hr style="border: 2px solid orange;">', unsafe_allow_html=True)
st.subheader("The Snore & More Inn is waiting for you...")

###############___HOTELS CODE STARTS___###############

input_city = city_destination 

if redy_to_run_flights == True:
    input_city = city_destination

    # First Step, using the Location Search to get the locationID number from the name of the city(INPUT)
    import requests

    url = "https://api.content.tripadvisor.com/api/v1/location/search"
    params = {
        "key": "A51D2E5910D046248A42E136AEE4C8A9",
        "searchQuery": input_city,
        "category": "attractions",
        "language": "en"
    }

    headers = {"accept": "application/json"}

    response = requests.get(url, params=params)
    results = response.json()

    df = pd.json_normalize(results['data'])

    city_value = df.loc[0, 'location_id']

    # finding the locationID from the Location Search to Location Details
    url = f"https://api.content.tripadvisor.com/api/v1/location/{city_value}/details"
    params = {
        "key": "A51D2E5910D046248A42E136AEE4C8A9",
        "language": "en",
        "currency": "USD"
    }
    headers = {"accept": "application/json"}

    response = requests.get(url, params=params, headers=headers)

    results = response.json()

    # with latLong we can find the hotels with Search Location Nearby
    latitude = results.get('latitude')
    longitude = results.get('longitude')

    url = "https://api.content.tripadvisor.com/api/v1/location/nearby_search"

    params = {
        "latLong": f"{latitude},{longitude}",
        "key": "A51D2E5910D046248A42E136AEE4C8A9",
        "category": "hotels",
        "language": "en"
    }

    headers = {"accept": "application/json"}

    response = requests.get(url, params=params, headers=headers)
    results = response.json()

    df = pd.json_normalize(results['data'])

    st.write("Stay just moments away from the city's main attractions at these 10 centrally-situated hotels we recommend for you:")

    hotels_to_show = df[['name', 'address_obj.street1']].copy()
    new_column_names = {'name': 'Hotel', 'address_obj.street1': 'Address'}
    hotels_to_show.rename(columns=new_column_names, inplace=True)
    hotels_to_show.reset_index(drop=True, inplace=True)
    hotels_to_show.index = hotels_to_show.index + 1

else:
    st.write(':construction:')


if len(hotels_to_show) == 0:
    st.write(':construction:')
else:
    st.dataframe(hotels_to_show)

###############___HOTELS CODE ENDS___###############

st.markdown('<hr style="border: 2px solid blue;">', unsafe_allow_html=True)

# Tabs section
st.subheader("Let's plan some activities")

image_path_3 = "./images/header3.png"
image_3 = Image.open(image_path_3)
st.image(image_3)

tab1, tab2, tab3, tab4, tab5 = st.tabs(["Intro", "Interesting places to visit", "Day plan", "Nearby restaurants", "Food Choices"])

with tab1: #Intro
    st.write("It's time to unlock a world of thrilling experiences in " + city_destination + "!")
    st.image("https://media.giphy.com/media/ToMjGpxInCZSzD3V82s/giphy.gif", width=400)

###############___PLACES CODE STARTS___###############

#    if st.button("Ready? Click here then!"):
#        driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()))

        # open the website
#        driver.get('https://www.tripadvisor.com/')
#        time.sleep(random.randint(2, 4))

        # Close cookies message
 #       remove_message = driver.find_element(By.XPATH, '/html/body/div[2]/div[2]/div/div[2]/div[1]/div/div[2]/div/div[1]/button')
 #       remove_message.click()
#        time.sleep(random.randint(2, 4))

        # Things to do icon
 #       things_to_do_icon = driver.find_element(By.XPATH, '/html/body/div[1]/main/div[1]/span/div/div/div/div[2]/a/span[1]/span')
 #       things_to_do_icon.click()
 #       time.sleep(random.randint(2, 4))

        # Search City
 #       search_city =  driver.find_element(By.XPATH, '/html/body/div[3]/div/form/input[1]')
 #       city = city_destination + " things to do"
 #       search_city.clear()
 #       search_city.send_keys(city)
 #       time.sleep(random.randint(2, 4))

        # click enter with the parameter keys.ENTER inside the method send_keys()
 #       search_city.send_keys(Keys.ENTER)
 #       time.sleep(random.randint(2, 4))

        # To get final url to do the scraping of the places
 #       html_source = driver.page_source
 #       time.sleep(random.randint(3, 4))

        # Close the website
 #       driver.quit()

        # Get all elements from the url as HTML and filter the class where we found the data is located
#        soup = BeautifulSoup(html_source, 'html.parser')
#        top_places = soup.find_all('div', class_='hZuqH')

        # Create a dataframe to show the places to visit according to the ranking showed on the page as well as locationID so we can get more information using TripAdvisor API
 #       data = []
 #       for top_place in top_places:
 #           name = top_place.find("a").text
 #           text = top_place.find("a")["href"]
 #           d_value = text.split('-')[2]
 #           data.append([name, d_value])

 #       places_to_visit = pd.DataFrame(data, columns=["Name", "locationID"])
 #       places_to_visit["locationID"] = places_to_visit["locationID"].str.replace("d", "")

        # Iterate in all the places to visit locationID to obtain detailed information with the API
 #       all_results = []
 #       for index, row in places_to_visit.iterrows():
 #           location_code = row['locationID']

#            if pd.notnull(location_code):  # Skip rows with null location ID values
#                url = f"https://api.content.tripadvisor.com/api/v1/location/{location_code}/details"
#                params = {
#                    "key": "A51D2E5910D046248A42E136AEE4C8A9",
#                    "language": "en",
#                    "currency": "EUR"
#                }
#                headers = {"accept": "application/json"}

#                response = requests.get(url, params=params, headers=headers)
#                time.sleep(random.randint(2, 4))

#                if response.status_code == 200:
#                    result = response.json()
#                    all_results.append(result)  # Append the result to the list
#                else:
#                    print(f"Error: {response.status_code} - {response.text}")

        # Convert the data
#        places_results = pd.DataFrame(all_results)

        #Save it
#        places_results.to_csv('saved_places_results.csv', index=False)
retreived_data = pd.read_csv('./places_to_show_Amsterdam.csv')




with tab2: # Places
    st.write("Unforgettable Destinations: A Guide to Must-Visit Places")

    

    if len(retreived_data) == 0:
        st.write(':construction:')   
    else:
      # Process the data to obtain only relevant information
      detailed_places = retreived_data[['name', 'description', 'address_obj', 'latitude', 'longitude']].copy()
      detailed_places['address_string'] = detailed_places['address_obj'].apply(lambda x: x.get('address_string', '') if isinstance(x, dict) else '')
      detailed_places.drop('address_obj', axis=1, inplace=True)
      detailed_places_final = detailed_places

      places_to_show = detailed_places_final[['name', 'description', 'address_string']].copy()
      new_column_names = {'name': 'Top Locations', 'description': 'Description', 'address_string': 'Address'}
      places_to_show.rename(columns=new_column_names, inplace=True)
      places_to_show.reset_index(drop=True, inplace=True)
      places_to_show.index = places_to_show.index + 1
      st.dataframe(places_to_show)
     

with tab3: #Places choice
  st.write("City Gems: Explore the Top Must-Visit Places")  
  
  if len(detailed_places_final) == 0:
     st.write(':construction:')
  else:
    places_list = detailed_places_final['name'].tolist()
    selected_place_day1 = st.selectbox("Where do you want to go today?", places_list, index=2)
    filtered_place = detailed_places_final.loc[detailed_places_final['name'] == selected_place_day1]
    latitude = filtered_place['latitude'].values[0]
    longitude = filtered_place['longitude'].values[0]

  # Expander section
  with st.expander("Check the selected place location here!"):
    if len(detailed_places_final) == 0:
       st.write(':construction:')
    else:
       data = pd.DataFrame({
          'name': [filtered_place],
          'latitude': [float(latitude)],
          'longitude': [float(longitude)]})
       st.map(data)

  
  st.write('Information completed?')
  agree_ready = st.checkbox("Yes! let's go.")
  disagree = st.checkbox("Nope, not yet.")
  if agree_ready:
    st.write("Have an amazing day!")
    with st.spinner('Loading...'):
      time.sleep(3)
      st.success('Data successfully loaded!')
      selected_place1 = True
  if disagree:
    st.write("Oh no! The travel universe is eagerly awaiting your input!")

with tab4: #Neraby restaurants
  st.write(
    "Bon appétit! These are our delicious restaurant recommendations."
  )  

 ###############___RESTAURANTS CODE STARTS___############### 
  
  if selected_place1 == True:
     
    #We filter the place from the data to obtain the values for latitude and longitude and define the point to do the search
    selected_row = detailed_places_final[detailed_places_final['name'] == selected_place_day1]
    location = f"{selected_row['latitude'].values[0]} , {selected_row['longitude'].values[0]}"

    #Key for API
    key_file2 = open("./keys/key2.txt")
    for line in key_file2:
      saved_key = line

    api_key = saved_key
    gmaps = googlemaps.Client(key=api_key)

    # Define the search radius in meters
    radius = 1000  
    place_type = 'restaurant'

    # Perform the search
    response = gmaps.places_nearby(location=location, radius=radius, type=place_type)

    #Get the list of all the the restaurants nearby 
    restaurants = []

    for result in response['results']:
       if 'restaurant' in result['types']:
            restaurants.append(result)

    near_restaurants = pd.DataFrame(restaurants)

    #Clean the data and normalize the rating so we can get the top 5 restaurants nearby
    clean_restaurants  = near_restaurants [((near_restaurants['business_status'] == "OPERATIONAL"))]
    clean_restaurants = clean_restaurants[['name','geometry','vicinity', 'rating','user_ratings_total','price_level','types']].copy()
    clean_restaurants['total_rating'] = (clean_restaurants['rating'] * clean_restaurants['user_ratings_total']) 

    from sklearn.preprocessing import MinMaxScaler

    scaler = MinMaxScaler()
    clean_restaurants['normalized_rating'] = ((scaler.fit_transform(clean_restaurants[['total_rating']]))*5).round(1)

    top_5_choices = (clean_restaurants.sort_values(by='normalized_rating', ascending=False)).head()

    def clean_geometry_column(df):
    # Extract latitude and longitude values from the "geometry" column
      df['latitude'] = df['geometry'].apply(lambda x: x['location']['lat'])
      df['longitude'] = df['geometry'].apply(lambda x: x['location']['lng'])
      df = df.drop('geometry', axis=1)

    clean_geometry_column(top_5_choices)

    Restaurants_1_to_show = top_5_choices[['name','vicinity', 'rating','user_ratings_total','normalized_rating','price_level']].copy()
    new_column_names = {'name': 'Restaurant', 'vicinity': 'Address', 'rating': 'Rating', 'user_ratings_total': 'Quantity ratings', 'normalized_rating': 'Adjusted ratings', 'price_level': 'Price level'}
    Restaurants_1_to_show.rename(columns=new_column_names, inplace=True)
    Restaurants_1_to_show.reset_index(drop=True, inplace=True)
    Restaurants_1_to_show.index = Restaurants_1_to_show.index + 1
    st.dataframe(Restaurants_1_to_show)
  else:
      st.write(':construction:')

 ###############___RESTAURANTS CODE ENDS___############### 
   
with tab5: #Food choices
  st.write("City Gems: Explore the Top Must-Visit Places")  
  
  if len(near_restaurants) == 0:
     st.write(':construction:')
  else:
    restaurants_list = top_5_choices['name'].tolist()
    selected_restaurant_day1 = st.selectbox("Where do you want to have lunch today?", restaurants_list, index=2)
    filtered_restaurant = top_5_choices.loc[top_5_choices['name'] == selected_restaurant_day1]
    latitude2 = filtered_restaurant['latitude'].values[0]
    longitude2 = filtered_restaurant['longitude'].values[0]

  # Expander section
  with st.expander("Check the selected restaurant location here!"):
    if len(near_restaurants) == 0:
       st.write(':construction:')
    else:
       data2 = pd.DataFrame({
          'name': [filtered_restaurant],
          'latitude': [float(latitude2)],
          'longitude': [float(longitude2)]})
       st.map(data2)

  
  st.write('Information completed?')
  agree_ready = st.checkbox("Yes, I'm Hungry!.")
  disagree = st.checkbox("Still thinking.")
  if agree_ready:
    st.write("Enjoy!")
    with st.spinner('Loading...'):
      time.sleep(3)
      st.success('Data successfully loaded!')
      selected_restaurant1 = True
  if disagree:
    st.write("Oh no! The travel universe is eagerly awaiting your input!")


# Sidebar section
with st.sidebar:
  st.subheader('Is everything ready?...')
  st.write("let's celebrate! 🎈")
  if st.button('Click me!✨'):
    st.balloons()
  else:
    st.write(' ')

###############___FINAL OUTPUT___############### 
