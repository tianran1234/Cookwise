# Capstone 1-Cookwise website

This website can help people look up recipes by dish names, by area or by main ingredients. If people create their own accounts, they will be able to add their favorite recipes to their own collections.


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

Go to the designated local host porter once the server is running.
Here is a screen shot of the homepage:
 

A user will be able to look up recipes by various filter using the dropdown search box. 

A user will be able to sign up/login their own account using the Sign up/ Log in button, and edit/delete their profile any time from the user’s account page.
On the search result page, a user will have be presented with the list of the filtered recipes organized by name, and an image of the dish. 
Click on each dish, a user will be directed to the page with the detailed ingredients and instructions of that dish, along with a button to favorite the dish.

Logged in users will be able to favorite/unfavorite that dish and access their favorite recipe list on their account page.


## Testing

To run the tests:

```bash
python -m unittest test_file_name.py
