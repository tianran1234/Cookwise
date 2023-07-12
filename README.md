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

To run the tests:

```bash
python -m unittest test_file_name.py
```


## Usage

A user will be able to look up recipes by various filter on the homepage by the dropdown search box. 

They will be able to sign up/log in/log out to their accounts.

They will be able to edit/delete their profile any time.

Logged in users will be able to favorite/unfavorite recipes and access their favorite recipe list on their profile page.
