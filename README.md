# This is a simple ETL pipeline from Spotify API.
This pipeline extract recently played songs from the users, transform the data a bit to have more concise and readable, then load the transformed data to an SQL database.

Tech used: SQLite, Python


# Spotify API Extract, Transform, and Load using Python and SQLite

This project is extracting user's recently played songs, transform the data to make it more concise and readable, then load them to SQL database.

## How to Run
1. ```git clone``` this repository or download it as zip. (Recommended) Fork this repository, then clone it from your own github.
2. Download [PYTHON](https://www.python.org/downloads/windows/) and install it on your PC.
3. Open the folder on your IDE. (Recommended) Download [Visual Studio Code](https://code.visualstudio.com/).
4. Run ```pip install requirement.txt``` to automatically install any necessary package from Python.
5. Open ```app.py``` and run ```get_access_token()``` by executing ```python app.py```. The program will return a link you can click and it will open Spotify Authentication Page. Then, if you see on the URL, you will see something like this ```open.spotify.com/access_token=%%%..%%%&token_type%%%```.
6. Copy and insert that Access Token on ```TOKEN``` variable.
7. Run the program by executing ```python app.py``` on CMD/Terminal. The program will extract the data from Spotify API.
8. The program then will save the data on a simple database with extension ```.sqlite``` located on the same directory of the ```app.py```
9. You can use [SQLite Viewer Web](https://sqliteviewer.app/) and upload the ```.sqlite``` file.