#from spotipy import SpotifyOAuth
#from spotipy.oauth2 import SpotifyClientCredentials
from spotipy.oauth2 import SpotifyOAuth
import spotipy
import requests
from bs4 import BeautifulSoup as bs
#import re
#import string
import PySimpleGUI

sp = spotipy.Spotify(auth_manager=SpotifyOAuth(client_id="b4069979eb594b1f81d83d23e4ac05de",
                                               client_secret="7ced5914fae14c6cb4b5f8d3b8690206",
                                               redirect_uri="http://localhost:9090",
                                               scope="user-library-read playlist-modify-public"))

def playlistByPopularity(most_popular, num_liked_songs, num_desired_songs ) -> None:
    '''
    Creates playlist based on the popularity/unpopularity of the songs desired from your liked songs
    Parameters:
        most_popular: True indicates most popular tracks are desired and False indicates least popular tracks are desired
        num_liked_songs: number of most recent liked songs to parse through
        num_desired_songs: number of desired songs in the new playlist
    '''
    #accesses the current user saved tracks
    results = sp.current_user_saved_tracks(limit = num_liked_songs)
    playlist = []
    song_score = {}
    #parses throguh liked songs associated a popularity score with each track
    for item in results['items']:
        track = item['track']
        song_id = track['id']
        popularity = track['popularity']
        song_score[song_id] = popularity

    #if most popular songs are desired
    if most_popular == True:
        #name of playlist list
        name = "MostPopularList"
        #part of description 
        descrip = "most popular"
        #sort list  by popularity
        sorted_by_popularity = sorted(song_score.items(), key=lambda x: x[1], reverse = True)
        for i in range(num_desired_songs):
            #add to playlist list
            playlist.append(sorted_by_popularity[i][0])

    #if least popular songs are desired
    if most_popular == False:
        name = "LeastPopularList"
        descrip = "least popular"
        #sorted by least popular songs
        sorted_by_unpopularity = sorted(song_score.items(), key = lambda x: x[1])
        for i in range(num_desired_songs):
            #adds to playlist list
            playlist.append(sorted_by_unpopularity[i][0])

    #appends to new playlist in spotify
    makePlaylist = sp.user_playlist_create(sp.me()['id'],name , public=True, collaborative=False, description=f"A playlist of the {num_desired_songs} {descrip} from the {num_liked_songs} most recent liked songs in your library")

    sp.user_playlist_add_tracks(sp.me()['id'], makePlaylist['id'], playlist, position=None)

############################################################################################################################

def playlistByAge(num_songs: int, minAge: int, maxAge: int) -> None:
    '''
    Creates playlist based on the age of artists found in the users liked songs
    Parameters:
        minAge: The minimum desired age
        maxAge: the maximum desired age
    '''
    #initialize empty lists for later
    playlist = []
    artistAge = {}

    #gets user saved tracks
    results = sp.current_user_saved_tracks(limit=num_songs)

    #gets the artists name out of the track information to use in the Wikipedia link
    for item in results['items']:
        for artist in item['track']['artists']:
            artistName = artist['name']
            # Format the artist name for Wikipedia URL
            name_for_wiki = artistName.replace(" ", "_")

            #fetches artist age for each unique artist
            if artistName not in artistAge:
                try:
                    #getset the URL for the artist wikipedia page using requests
                    wikipedia = requests.get(f"https://en.wikipedia.org/wiki/{name_for_wiki}")
                    wikipedia.raise_for_status()

                    #parses the wikipedia page using BeautifulSoup
                    soup = bs(wikipedia.text, 'html.parser')

                    #find the infobox on the artist wikipedia page
                    about = soup.find('table', class_='infobox')
                    if about:
                        #finds the artist age within the infobox
                        listedAge = about.find('span', class_='noprint ForceAgeToShow')
                        if listedAge:
                            ageAsString = listedAge.text
                            #extracts the age number using a regular expression
                            age = re.findall(r'\b\d+\b', ageAsString)
                            #adds age to dictionary if age is found
                            if age:
                                artistAge[artistName] = int(age[0])
                            #adds None for artist age if no age is found
                            else:
                                artistAge[artistName] = None
                        #adds None for artist age if no span tag is found
                        else:
                            artistAge[artistName] = None
                    #adds None for artist age if no infobox is found
                    else:
                        artistAge[artistName] = None
                #adds None for artist age if no page exists
                except requests.exceptions.RequestException:
                    artistAge[artistName] = None

    # Loop through list of tracks and add their tracks to the playlist if the artist's age is within the given range
    for item in results['items']:
        for artist in item['track']['artists']:
            artistName = artist['name']
            artist_age = artistAge.get(artistName, None)

            if artist_age is not None and minAge <= artist_age <= maxAge:
                track_id = item['track']['id']
                playlist.append(track_id)

    if len(playlist) == 0:
        return False

    makePlaylist = sp.user_playlist_create(sp.me()['id'], 'AgeList', public=True, collaborative=False, description=f"A playlist of my liked artists whose ages range from {minAge} to {maxAge}")

    sp.user_playlist_add_tracks(sp.me()['id'], makePlaylist['id'], playlist, position=None)

############################################################################################################################

def playlistbyYear (start_year: int, end_year: int, num_liked_songs: int, num_desired_songs:int) -> None: 
    '''
    Creates playlist based on a range of release years input by the user
    Parameters:
        start_year: earliest desired year
        end_year: latest desired year
        num_liked_songs: number of most recent liked songs to parse through
        num_desired_songs: number of desired songs in the new playlist
    '''
    #retrive liked songs
    results = sp.current_user_saved_tracks(limit=num_liked_songs)
    playlist = []
    song_years= {}

    #looping through liked songs and extract release date
    for item in results['items']:
        track=item['track']
        song_id= track['id']
        release_date= track['album']['release_date']

        #retrieve year from full date
        release_year = int(release_date.split('-')[0])
        song_years[song_id] = release_year

    #filter the songs by release year 
    filtered_songs=[
        song_id for song_id, year in song_years.items()
        if start_year <= year <= end_year
    ]

    #wanted songs for the playlist organized by release year 
    playlist=filtered_songs[:num_desired_songs]

    #create playlist for above
    if playlist:
        makenewPlaylist = sp.user_playlist_create(
            sp.me()['id'],
            'ReleaseYearlist',
            public=True,
            description = f"Playlist of songs released between {start_year} and {end_year}"
        )
        sp.user_playlist_add_tracks(sp.me()['id'], makenewPlaylist['id'], playlist)
    else: 
        print(f"No songs between {start_year} and {end_year}.")

############################################################################################################################

def playlistByWord(num_liked_tracks, word) -> None:
    '''
    Creates playlist with songs containing inputted word in the lyrics
    Parameters:
        num_liked_tracks:number of most recent liked songs to parse through
        word: word to search for in lyrics
    '''
    #initializes playlist list
    playlist = []
    playlist_name = f"{word}List"

    #gets liked songs
    results = sp.current_user_saved_tracks(limit = num_liked_tracks)

    #parses through liked songs
    for item in results['items']:
        #track name
        track_name = item['track']['name']
        #track name in appropriate azlyrics.com format
        if "(" in track_name:
            track_name = track_name.split("(")[0].strip()
        track_name = re.sub(r"[^a-zA-Z0-9 ]", "", track_name)
        track_az = track_name.replace(" ","-").lower()

        #artist name
        artist_name = item['track']['artists'][0]['name']
        #artist name in appropriate azlyrics.com format
        artist_az = re.sub(r"[^a-zA-Z0-9 ]", "", artist_name)
        artist_az = artist_az.replace(" ","-").lower()
 
        #link to appropriate website
        artist_first = artist_name[0].lower()

        az_link = f"https://azlyrics.biz/{artist_first}/{artist_az}/{artist_az}-{track_az}-lyrics/"
        print(az_link)
        try:
            #requests to approriate link
            az = requests.get(az_link)
            #make sure link exists
            az.raise_for_status()
            #html parse
            soup = bs(az.text, 'html.parser')
            #find lyrics part of the code 
            lyrics = soup.find_all('p')

            #builds list of words in lyrics from lyrics within each tag
            lyrics_list = []
            for tag in lyrics:
                text = tag.get_text().strip()  
                lyrics_list.append(text)     
            lyrics_continuous = " ".join(lyrics_list)
            words = lyrics_continuous.split()

            #if the desired word is in the lyrics add song to playlist list
            if word in words:
                track_id = item['track'].get('id')
                if track_id:
                    playlist.append(track_id)

        #if there is no addresss skip to next song
        except requests.exceptions.HTTPError:
            print(az_link)
            print(f'failed to read {track_az}')
            continue

    if len(playlist) == 0:
        return False
    #create new public playlist
    makePlaylist = sp.user_playlist_create(sp.me()['id'],playlist_name , public=True, collaborative=False, description=f"A playlist of songs containing the word {word} from the {num_liked_tracks} most recent liked songs in your library")
    sp.user_playlist_add_tracks(sp.me()['id'], makePlaylist['id'], playlist, position=None)


############################################################################################################################
#GUI STUFF
############################################################################################################################

def main() -> None:
    import PySimpleGUI as sg

    #creates the layout of the initial GUI 
    layout = [[sg.Text("Create a Playlist:")], [sg.Button('By Age')], [sg.Button('By Song Popularity')],[sg.Button('By Release Year')],[sg.Button('Songs That Mention a Word (ie. love, time, etc.)')]]

    #makes a window object using the layout that was created
    window = sg.Window("DCS-211 Spotify Playlist Project", layout)

    #runs until break condition is met, in this case window is closed
    while True:
        event, values = window.read()
        if  event == sg.WIN_CLOSED:
            break

        #if the By Age button is pressed, creates a layout for a new GUI window 
        if event == 'By Age':
            age_layout = [
                [sg.Text("Generate from how many of your most recent liked songs?: Max 50"), sg.InputText(key = "num_liked_songs")],
                [sg.Text("Enter the minimum and maximum age for your desired artists:")],
                [sg.Text("From:"), sg.InputText(key="min_age"), sg.Text("To:"), sg.InputText(key="max_age")],
                [sg.Button('Generate'), sg.Button('Back')]
            ]
            
            #creates new window for age input and playlist generation
            age_window = sg.Window("Age Range Input", age_layout)

            #runs until new break condition is met
            while True:
                age_event, age_values = age_window.read()
                
                #new window is closed or back button is pressed
                if age_event == sg.WIN_CLOSED or age_event == 'Back':
                    age_window.close()
                    break
                
                #generates Age playlist using playlistByAge function
                if age_event == 'Generate':
                    min_age = int(age_values["min_age"])
                    max_age = int(age_values["max_age"])
                    num_songs = int(age_values["num_liked_songs"])
                    if num_songs < 1 or num_songs > 50:
                        sg.popup("Number of songs must be between 1 and 50.")
                        continue

                    result = playlistByAge(num_songs, min_age, max_age)

                    if result == False:
                        sg.popup("No songs fit criteria")
                    else:
                        sg.popup("Playlist created!")
                    #after submission, close the age input window
                    age_window.close()
                    break

        #if popularity is chosen as parameter
        if event == 'By Song Popularity':
            popularity_layout = [
                [sg.Text("Do you want to generate your playlist by:")],
                [sg.Radio("Most Popular", "POPULARITY", key="most_popular", default=True),
                 sg.Radio("Least Popular", "POPULARITY", key="least_popular")],
                [sg.Text("Generate from how many of your most recent liked songs?: Max 50"), sg.InputText(key = "num_liked_songs")],
                [sg.Text("Enter # of desired songs in new playlist")],
                [sg.InputText(key="num_desired_songs")],
                [sg.Button("Generate"), sg.Button("Back")]
            ]

            #new window for popularity
            popularity_window = sg.Window("Popularity Info Input", popularity_layout)

            while True:
                pop_event, pop_values = popularity_window.read()
                
                if pop_event == sg.WIN_CLOSED or pop_event == 'Back':
                    popularity_window.close()
                    break
                #if generate is clicked
                if pop_event == 'Generate':  
                    num_liked_songs = pop_values["num_liked_songs"]

                    #ensure  inputted number is integer
                    if not num_liked_songs.isdigit():
                        sg.popup("Please enter an integer")
                    else:
                        num_liked_songs = int(num_liked_songs)
                        if num_liked_songs > sp.current_user_saved_tracks()['total']:
                            #ensures not too many songs for playlist are selected
                            sg.popup("Number is higher than the total number of liked songs in the library")
                        #determines whether the playlist will be by most popular or least popular
                        else:
                            if pop_values.get("most_popular") == True:
                                most_popular = True
                            elif pop_values.get("least_popular") == True:
                                most_popular = False
                            else:
                                sg.popup("Please select either Most Popular or Least Popular")
                                continue 
                            num_desired_songs = pop_values.get("num_desired_songs")
                            #ensures desired number of songs is a digit
                            if not num_desired_songs.isdigit():
                                sg.popup("Please enter an for number of desired songs")
                            else:
                                num_desired_songs = int(num_desired_songs)
                                if num_desired_songs > num_liked_songs:
                                    sg.popup("Number is higher than the requested number of songs")
                    #runs function
                    playlistByPopularity(most_popular, num_liked_songs, num_desired_songs)
                    sg.popup("Playlist created!")
                    popularity_window.close()
                    break
        
        #Release Year
        if event == 'By Release Year':
            year_layout = [
                [sg.Text("Enter the range of release years for your desired songs:")],
                [sg.Text("From:"), sg.InputText(key="start_year"), sg.Text("To:"), sg.InputText(key="end_year")],
                [sg.Text("Generate from how many of your most recent liked songs?: Max 50"), sg.InputText(key="num_liked_songs")],
                [sg.Text("Maximum # of desired songs in new playlist:"), sg.InputText(key="num_desired_songs")],
                [sg.Button('Generate'), sg.Button('Back')]
            ]

            year_window = sg.Window("Release Year Input", year_layout)

            #new conditional for running year window
            while True:
                year_event, year_values = year_window.read()

                #conditions for breaking out of window
                if year_event == sg.WIN_CLOSED or year_event == 'Back':
                    year_window.close()
                    break
                
                #if the user presses the generate button then
                if year_event == 'Generate':
                    try:
                        start_year = int(year_values["start_year"])
                        end_year = int(year_values["end_year"])
                        num_liked_songs = int(year_values["num_liked_songs"])
                        num_desired_songs = int(year_values["num_desired_songs"])

                        #ensures that the years given are a valid range
                        if start_year > end_year:
                            sg.popup("Start year must be less than or equal to end year.")
                        else:
                            playlistbyYear(start_year, end_year, num_liked_songs, num_desired_songs)
                            sg.popup("Playlist created!")
                            year_window.close()
                            break
                    except ValueError:
                        sg.popup("Please enter valid numbers for all fields")

        #if the user presses the playlist by word button
        if event == "Songs That Mention a Word (ie. love, time, etc.)":
            word_layout = [
                [sg.Text("Generate from how many of your most recent liked songs? Max 50:"), sg.InputText(key = "num_liked_songs")],
                [sg.Text("Generate songs containing what specific word (ie. 'love', 'time', etc.)?"), sg.InputText(key = "word")],
                [sg.Button("Generate"), sg.Button("Back")]
            ]

            #new window
            word_window = sg.Window("Songs Mentioning Specific Word", word_layout)
            while True:
                word_event, word_values = word_window.read()
                
                #closes new window
                if word_event == sg.WIN_CLOSED or word_event == 'Back':
                    word_window.close()
                    break
            
                if word_event == 'Generate':
                    #assigns appr variable
                    num_liked_songs = word_values["num_liked_songs"]
                    if not num_liked_songs.isdigit():
                        #ensures that it is integer
                        sg.popup("Please enter an integer")
                    else:
                        #assigns variable
                        num_liked_songs = int(num_liked_songs)
                    word = word_values["word"].lower()
                    #runs function
                    result = playlistByWord(num_liked_songs, word)
                    if result == False:
                        sg.popup("No songs fit criteria")
                    else:
                        sg.popup("Playlist created!")
                    # After submission, close the word input window
                    word_window.close()
                    break
        

main()

