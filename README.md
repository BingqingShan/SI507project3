# Instructions
## What this app can do
By running the flask app (written in SI507_project3.py), you can indirectly input data to database and show details of some information in the database. The diagram.jpg represents the relationship of the database.


This app will allow you to go to the routes at the specific paths and show the relevent result on the HTML page. Remember, if you are going to a route which is not defined in the program, you may run into error. So limit your routes in the following options, unless you want to add more routes yourself:

1.  `/index` -> 'index.html' - shows numbers of movies saved in the app.
2. `/movie/new/<title>/<director>/<distributor>/<major_genre>/<us_gross>/<worldwide_gross>/<us_dvd_sales>/<production_budget>/` -> a new movie shall be saved in the database based on the input of url. The page will either show "New movie: ___ (title) directed by ___ (director), distributed by ___ (distributor), has been saved in the list. More info: Major Genre: ___ ; US Gross: ___ , Worldwide Gross: ___ , US DVD Sales: ___ , Production Budget: ___ ." or show "That movie already exists. Go back to the main app."
3. `/all_movies` -> 'all_movies.html' - shows a list of movies saved in the app.
4. `/all_directors` -> 'all_directors.html' - shows a list of directors saved in the app.



## Dependencies the project relies on
Thus, to guarantee everyone can run this program properly, you may install all the required packages which is written in requirements.txt.

How to install it:

once you set up your virtual environment, you can type in $ pip install -r requirements.txt to install all the required packages all at once.

## How to run this app
Once you download the folder, in your terminal, set up your virtual environment and install packages as said above. Once you are done with that, you can cd to the file SI507_project3.py, type in python SI507_project_3.py runserver in your terminal and then let it run. You will see a builtin server (eg. http://127.0.0.1:5000). copy paste it in your web browser and then you will see the homepage with numbers of movies recorded in the database. Now you can go ahead and start to play around with different routes now.
