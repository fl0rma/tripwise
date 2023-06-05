<img src="https://bit.ly/2VnXWr2" alt="Ironhack Logo" width="100"/>

# TripWise

Effortless Itineraries for Unforgettable Escapes


## Introduction to the project.

## Content

- [Introduction](#Introduction)
- [Description](#description)
- [Technical Developments](#Technical-Developments)
- [Main Challanges and Strenghts](#requirements)
- [Product ShowCase](#deliverables)
- [Main Insights](#mentoring)
- [Conclusions](#schedule)
- [Resources](#resources)

<a name="description"></a>

## Description
Introducing TripWise, a comprehensive travel app and website designed to simplify and enhance your trip planning experience. With just a few simple inputs, TripWise empowers you to create personalized itineraries and discover the best options for your dream vacation in a matter of minutes.

Whether you're a budget-conscious traveler or seeking a luxurious getaway, TripWise leverages its advanced algorithms to swiftly curate and present the most enticing offers tailored to your preferences. By specifying your desired city of interest and budget, TripWise instantly showcases a range of options that meet your criteria.

Flight Prices: TripWise scours through a vast network of airlines and travel agencies to deliver the lowest airfares available, ensuring you can maximize your travel budget and secure the best deals on flights.

Accommodation Recommendations: We understand the importance of a comfortable and enjoyable stay. TripWise handpicks the top 5 hotels in your chosen city, carefully considering factors such as location, amenities, customer reviews, and affordability. Rest assured that you'll find the perfect accommodation to suit your needs and preferences.

Must-Do Activities: Discover the essence of your destination with TripWise's curated list of the top 10 things to do. From iconic landmarks to hidden gems, we provide a diverse selection of attractions and experiences to ensure you make the most of your trip and create unforgettable memories.

Fine Dining Experiences: Enhance your journey with culinary delights by exploring TripWise's selection of highly-rated restaurants near your chosen activities. Indulge in a variety of cuisines and savor the local flavors, all conveniently located within close proximity to your planned adventures.

TripWise is dedicated to making the act of planning your trip effortless and enjoyable. Our mission is to provide you with the tools and resources needed to curate personalized itineraries that cater to your unique travel preferences and constraints. Say goodbye to time-consuming research and let TripWise take care of the intricate details, so you can focus on creating unforgettable experiences during your well-planned escape.

With TripWise, embark on your next adventure with confidence, knowing that your travel arrangements have been expertly tailored to suit your desires and budget. Welcome to a new era of stress-free trip planning, where personalized itineraries are just a few clicks away. Let TripWise be your trusted companion on your journey to unforgettable destinations.


<a name="Technical Developments"></a>

## Technical Developments

Our team utilized cutting-edge technologies and APIs to deliver a robust and efficient platform that caters to all your travel planning needs.

The app's design and implementation were built using Streamlit, a powerful framework that allows for intuitive user interfaces and seamless user experiences. With Streamlit, we were able to create a visually appealing and user-friendly interface that simplifies the entire trip planning process.

To gather the necessary data for flights, hotels, and restaurants, TripWise integrates three main APIs:

TripAdvisor API: We leverage the TripAdvisor API to retrieve extensive data on hotels by proximity. This integration enables us to present you with the top 5 hotels in your chosen city, taking into account factors such as location, ratings, and reviews. This ensures that you have access to the best accommodations that suit your preferences and budget.

Amadeus API: The Amadeus API is an invaluable resource for accessing up-to-date flight information. By utilizing this API, TripWise provides you with the lowest flight prices available, allowing you to secure the best deals and make informed decisions when booking your flights.

Google Maps API: Our integration with the Google Maps API enables us to retrieve data on nearby restaurants based on the selected activities. This feature ensures that you have access to highly-rated dining options conveniently located near the attractions and experiences you plan to enjoy during your trip.

In addition to these API integrations, we utilized Selenium, a powerful web scraping tool, to extract data from TripAdvisor. This allowed us to gather information on the top 10 Things To Do at your chosen destination. By combining both API data and web scraping techniques, we ensure that TripWise presents you with a comprehensive list of must-visit attractions and activities for an enriching travel experience.

These technical developments showcase our commitment to providing you with a reliable, feature-rich, and comprehensive travel planning tool. We continually strive to leverage the latest technologies and APIs to enhance the accuracy, convenience, and efficiency of TripWise, enabling you to plan your dream vacation with confidence and ease.



<a name="Main Challanges and Strenghts"></a>

## Main Challanges and Strenghts

Integration of APIs: Handling authentication, data formatting, error handling, and staying up to date with API changes.


Data management and storage: Handling customer information, booking details, and itineraries. Designing an efficient database schema, implementing data validation and normalization, and ensuring data integrity. Specially moving the code to replit, the code was overheating the CPU and RAM.

User authentication and authorization: Building secure authentication and authorization system to protect sensitive user information and restrict access to certain features or data. Implementing secure login mechanisms, password encryption.

User interface design and user experience: Creating an intuitive and visually appealing user interface that provides a seamless user experience.

Performance optimization:  efficient database queries, caching strategies, asynchronous processing, and minimizing latency.

Error handling and exception management: such as network failures, invalid responses, or rate limiting. 



<a name="How to Use it"></a>

## How to Use it

For the project to run, the user will need the API Authetincation from TripAdvisor autorized by IP, if your IP adress is not authorized, you wont be able to see it. 
For the other Api's they will just need the keys and tokens. 

The first step is, under the "Tells Us About Your Journey!" to click on 'When&Where to?' here the user need to select the City of Origin, The Destination City, The departure Date (it needs to be written as (YYYY-MM-DD)otherwise it won't work), the same happens for the Date of Return. At the end the user need to select 'Yes!' for the information completed task. 

The Second thing is to Click on 'Who is Coming?' and select at least the number of Adults, the other responses are optional.Then select 'All done'

The Third part its optional as well, you can select the class f service and if you want a direct flight.The user can even set a budget limit, it need to be added in Euros. 
Now they click in 'Ready to Fly'

Now the user will be able to see the 3 top flights for 3 airlines companies and the top 10 Hotels choosen for you by proximity. 

Last part, you provide the Top 10 Activities for you to do in the selected City and the best restaurants near the chosen activity. The user just need to clickon 'Ready? Click Here!"

Check this video to see how it works https://vimeo.com/833319706?share=copy






