# Capstone 1-Cookwise website (http://127.0.0.1:5000/)

This website is designed to help people look up recipes by dish names, by area or by main ingredients. If people create their own accounts, they will be able to add their favorite recipes to their own collections.


## technology stack used:
PostgreSQL, python, flask, Jinja, SQLAlchemy, Psycopg, Unittest


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

Go to the designated local host porter (http://127.0.0.1:5000) once the server is running. Here is a screen shot of the homepage:![homepage](https://github.com/tianran1234/Cookwise/assets/115170399/5478814d-0b2d-4276-bd80-b68986045659)

A user (without logging in or signing up) can look up recipes by various filter using the dropdown search box on the top right side of the homepage, as shown below: 
![searchbox](https://github.com/tianran1234/Cookwise/assets/115170399/7797aeb3-433c-4b81-98af-c145d017925c)

If one clicks on "Search by name", they will be prompted to the search page below:
![Searchbyname](https://github.com/tianran1234/Cookwise/assets/115170399/ad348ae8-460b-4864-b56f-eac53a38abd4)
One can type in the name of the dish that they are looking for and then click on the search icon. If the dish can't be found, the user will be prompted to put in a different name. Otherwise they will be directed to the receipe page of that dish, as illurstrated below:
![receipe](https://github.com/tianran1234/Cookwise/assets/115170399/86a168f6-f5b7-470a-a220-a570c7ff4854)
There will be the ingredients and instructions of the dish, as well as an example picture and a link to the cooking video (if there is any) on the top left of the page.

A user will be prompted to sign up/ log in to their own account in order to favorite the receipe that they look up. They may click on the "sign up" button below the picture of the dish, and will be directed to this page:
![signup](https://github.com/tianran1234/Cookwise/assets/115170399/76266e73-b553-4b1c-b562-d4fd9c2aeb2f)
Or they can click on the "log in" button and will be directed to here:
![login](https://github.com/tianran1234/Cookwise/assets/115170399/4b2b8238-6fb0-4734-844b-df155e153555)

Once one is signed up/logged in, they will be directed to the homepage again which now looks like the screenshot below:
![loggedin](https://github.com/tianran1234/Cookwise/assets/115170399/603635cd-673e-4414-82f4-2c85c9747e46)

If the user click on their profile image on the top right of the homepage, they will be led to their personal page:
![Loggedin (2)](https://github.com/tianran1234/Cookwise/assets/115170399/36949138-ad8a-4913-9883-b14ff5416d22)

Once click on the "Edit Profile" button on the personal page, they will be able to edit their personal profile:
![editprofile](https://github.com/tianran1234/Cookwise/assets/115170399/ffdf00f8-0502-46cc-9454-2789bfc93661)
Once they are done editing and click on the submit button, or if they click on the "cancel" button, they will be directed back to their personal page.

There is a "favrotie" tab on the right of the nav bar of any logged-in user. If the user hasn't favortied any receipe yet, there will be a message reminder to add receipe to your favorites first. Otherwise, once clicked on the tab, the user will see the list of the receipes that they have favorited like below:
![favorties](https://github.com/tianran1234/Cookwise/assets/115170399/e7674984-8976-48d4-a92c-d2976dc70aa9)
If one click on the "Unfavorite" button beside a receipe, the receipe will be removed from the list.
If they click on the name of the receipe, they will be taken to the detailed receipe page, except this time, instead of being prompt to log in/ sign up below the example picture of the dish, they will be provided with an "Unfavorite" button as shown below:
![Unfavorite](https://github.com/tianran1234/Cookwise/assets/115170399/ba0d903a-a674-45eb-950f-ba42ffff8e4a)
Once clicked on the "Unfavorite", the user will be taken back to the page of list of their favorited receipes.

One the top right of the nav bar of any logged-in user, there is a "Log out" tab. Once clicked, the user will be directed to the log in page with a confirmation message "You have successfully logged out" as shown below:
![image](https://github.com/tianran1234/Cookwise/assets/115170399/021954c5-e712-44ce-826a-b590e454acc8)


## Testing

To run the tests:

```bash
python -m unittest test_file_name.py
