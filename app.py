import sqlalchemy
import pandas as pd 
from sqlalchemy.orm import sessionmaker
import requests
import json
from datetime import datetime
import datetime
import sqlite3


DATABASE_LOCATION = "sqlite:///my_played_tracks.sqlite"
TOKEN = "BQB5TjPZkLd7fO9zmeMNjaom-_yPuKWG7RgeLvINy9HHDYXR6avTSusr6a36oDE2lB4Riug6MdlT-2j254E44MlM0_a1rVxSugLyixc17MYYOARdVXQRyqEf0BtpgTvqc8y-u4fd8FtwYs_scexcDGtst5J6lc3W380ucRH4f2WVqacd7aNdMwjhmpeZiYyLW4VC" # your Spotify API token

def get_access_token(): #Manual from browser
    ENDPOINT = 'https://accounts.spotify.com/authorize'

    ENDPOINT += '?response_type=' + 'token'
    ENDPOINT += '&client_id=' + '7e197e5eebd5448ba639ea2d61699101'
    ENDPOINT += '&redirect_uri=' + 'https://open.spotify.com/'
    ENDPOINT += '&scope=' + 'user-read-recently-played'

    #Scopes can be edited as needed. Check the others -> https://developer.spotify.com/documentation/web-api/concepts/scopes

    print(ENDPOINT)

def get_user_id():
    ENDPOINT = 'https://api.spotify.com/v1/me'

    headers = {
        "Authorization" : "Bearer {token}".format(token=TOKEN)
    }

    r = requests.get(ENDPOINT, headers=headers)
    data = r.json()

    return data['id']

def check_if_valid_data(df: pd.DataFrame) -> bool:
    if df.empty:
        print("No songs downloaded. Finishing execution")
        return False 

    # Primary Key Check
    if pd.Series(df['played_at']).is_unique:
        pass
    else:
        raise Exception("Primary Key check is violated")

    # Check for nulls
    if df.isnull().values.any():
        raise Exception("Null values found")

    return True

if __name__ == "__main__":

    # user_id = get_user_id()

    # Extract

    headers = {
        "Accept" : "application/json",
        "Content-Type" : "application/json",
        "Authorization" : "Bearer {token}".format(token=TOKEN)
    }
    
    # Convert time to Unix timestamp in miliseconds      
    date = datetime.datetime(2023, 1, 1)
    
    # GET all songs listened after set date    
    r = requests.get("https://api.spotify.com/v1/me/player/recently-played?after={time}"
                     .format(time=int(date.timestamp() * 1000))
                     , headers = headers)

    data = r.json()
    song_names = []
    artist_names = []
    played_at_list = []
    timestamps = []

    # Extracting some part from json
    for song in data["items"]:
        song_names.append(song["track"]["name"])
        artist_names.append(song["track"]["album"]["artists"][0]["name"])
        played_at_list.append(datetime.datetime.strptime(song["played_at"], '%Y-%m-%dT%H:%M:%S.%fZ').strftime('%a, %d %b %Y | %H:%M:%S'))
        timestamps.append(datetime.datetime.strptime(song["played_at"][0:10], '%Y-%m-%d').strftime('%a, %d %b %Y'))
        
    # Make pandas       
    song_dict = {
        "song_name" : song_names,
        "artist_name": artist_names,
        "played_at" : played_at_list,
        "timestamp" : timestamps
    }

    song_df = pd.DataFrame(song_dict, columns = ["song_name", "artist_name", "played_at", "timestamp"])
    
    # Validate
    if check_if_valid_data(song_df):
        print("Data valid, proceed to Load stage")

    # Load

    engine = sqlalchemy.create_engine(DATABASE_LOCATION)
    conn = sqlite3.connect('my_played_tracks.sqlite')
    cursor = conn.cursor()

    sql_query = """
    CREATE TABLE IF NOT EXISTS my_played_tracks(
        song_name VARCHAR(200),
        artist_name VARCHAR(200),
        played_at VARCHAR(200),
        timestamp VARCHAR(200),
        CONSTRAINT primary_key_constraint PRIMARY KEY (played_at)
    )
    """

    cursor.execute(sql_query)
    print("Opened database successfully")

    try:
        song_df.to_sql("my_played_tracks", engine, index=False, if_exists='append')
    except:
        print("Data already exists in the database")

    conn.close()
    print("Close database successfully")
    


    # Job scheduling 
    
    # For the scheduling in Airflow, refer to files in the dag folder 