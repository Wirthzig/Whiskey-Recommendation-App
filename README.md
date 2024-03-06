------------------------------------------------------------------------------------------------------------------------

This is a backup repo for the final project of the Course Python and Web Design - EBS2070 (Maastricht University).
It is a flask-web application with different functionalities for an online whiskey shop, including a recommendation system for whiskey brands.

------------------------------------------------------------------------------------------------------------------------

Run the application:
    Python version 3.7 is used
    In terminal run: pip install -r requirements.txt
    Run the app.py
    Access the following link in your browser: http://127.0.0.1:5000/

------------------------------------------------------------------------------------------------------------------------

Structure:
In order to maintain an object-orientated approach, we separated functionalities into different classes. This allows to
implement different methods and access constraints for employees compared to managers. Using this design, a solid
database structure can easily be implemented in further development.

------------------------------------------------------------------------------------------------------------------------

Datasets:

availability.csv:
    shop_id
    distillery names

customers.csv:
    customer_id
    num_of_purchases
    status
    favourite

purchases.csv:
    customer_id
    date
    distillery
    whiskey
    recommended

shops.csv:
    shop_id
    location
    type
    date
    discount

whiskey86.csv:
    Distillery
    Body
    Sweetness
    Smoky
    Medicinal
    Tobacco
    Honey
    Spicy
    Winey
    Nutty
    Malty
    Fruity
    Floral
    Postcode
    Latitude
    Longitude

whiskey_review2020.csv:
    id
    distillery
    name,category
    points
    price
    currency
    description

------------------------------------------------------------------------------------------------------------------------

Sources:

The CSS skeletons are free to use templates retrieved from http://getskeleton.com/

For the application we use a combination of provided and original datasets.
These provided ones can be found here:
https://www.kaggle.com/koki25ando/scotch-whisky-dataset
https://www.kaggle.com/koki25ando/22000-scotch-whisky-reviews

The provided datasets were adjusted for optimal implementation. Missing data was replaced using information from
https://www.whiskybase.com/ and manufactures of specific whiskeys.

------------------------------------------------------------------------------------------------------------------------