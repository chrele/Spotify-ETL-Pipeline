# This is a simple ETL pipeline from Spotify API.
This pipeline extract recently played songs from the users, transform the data a bit to have more concise and readable, then load the transformed data to an SQL database.

Tech used: SQLite, Python

#HOW TO USE
You will need to run the get_access_token() function to get the access token. This will be updated in the future for ease of use.

The Access token then can be used in the TOKEN placeholder. That's it.

Finally, run it by executing python app.py
