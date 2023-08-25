# Capstone 1-Cookwise website (http://127.0.0.1:5000/)

This website is designed to help people look up recipes by dish names, by area or by main ingredients. If people create their own accounts, they will be able to add their favorite recipes to their own collections.


## technology stack used:
PostgreSQL, flask, Jinja, SQLAlchemy, Psycopg, Unittest


## Cookwise API
A third party API is used here from The MealDB:
https://www.themealdb.com/api.php


## Installation

```bash
pip install -r requirements.txt
```

To run the server:

Step 1: start postgresql 
```bash
sudo service postgresql start
```

Step 2. 
```bash
python3 seed.py
```
Step 3. 
```bash
flask run
```


## Usage

Go to the designated local host porter (http://127.0.0.1:5000) once the server is running.
Here is a screen shot of the homepage:
![Untitled](https://github.com/tianran1234/capstone-1/assets/115170399/dcd689e0-cc06-4cd3-b40b-1648623efc2a)

A user (without logging in or signing up) can look up recipes by various filter using the dropdown search box on the top right side of the homepage, as shown below: 
![searchbox](https://github.com/tianran1234/Cookwise/assets/115170399/7797aeb3-433c-4b81-98af-c145d017925c)

A user will be able to sign up/login their own account using the Sign up/ Log in button, and edit/delete their profile any time from the user’s account page.
On the search result page, a user will have be presented with the list of the filtered recipes organized by name, and an image of the dish. 
Click on each dish, a user will be directed to the page with the detailed ingredients and instructions of that dish, along with a button to favorite the dish.

Logged in users will be able to favorite/unfavorite that dish and access their favorite recipe list on their account page.


## Testing

To run the tests:

```bash
python -m unittest test_file_name.py
