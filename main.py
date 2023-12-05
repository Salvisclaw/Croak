import streamlit as st
from streamlit_option_menu import option_menu
import streamlit.components.v1 as components
import os
import time
import spotipy
from spotipy.oauth2 import SpotifyOAuth, SpotifyClientCredentials
import requests
from spotifysearch import *
from model import *


#Authentication - without user
#client_credentials_manager = SpotifyClientCredentials(client_id=Client_id, client_secret=client_secret)
#sp = spotipy.Spotify(client_credentials_manager = client_credentials_manager)

Client_id=os.environ['Client_ID']
client_secret=os.environ['Client_secret']
auth_manager = SpotifyClientCredentials(client_id=Client_id, client_secret=client_secret)
sp = spotipy.client.Spotify(auth_manager=auth_manager) 






if 'model' not in st.session_state:
    st.session_state.model = 'Model 1'
def update_radio2():
    st.session_state.model=st.session_state.radio2
if 'genre' not in st.session_state:
    st.session_state.genre=3
def update_num_genre():
    st.session_state.genre=st.session_state.num_genre
if 'artist' not in st.session_state:
    st.session_state.artist=5
def update_same_art():
    st.session_state.artist=st.session_state.same_art
if 'model2' not in st.session_state:
    st.session_state.model2= 'Spotify model'
def update_radio1():
    st.session_state.model2 =st.session_state.radio1

if 'Region' not in st.session_state:
    st.session_state.rg="US"
def update_Region():
    st.session_state.rg=st.session_state.Region
if 'radio' not in st.session_state:
    st.session_state.feature="Song"
def update_radio0():
    st.session_state.feature=st.session_state.radio

if 'p_url' not in st.session_state:
    st.session_state.p_url = 'Example: https://open.spotify.com/playlist/37i9dQZF1DX8FwnYE6PRvL?si=06ff6b38d4124af0'
def update_playlist_url():
    st.session_state.p_url = st.session_state.playlist_url

if 's_url' not in st.session_state:
    st.session_state.s_url = 'Example: https://open.spotify.com/track/5CQ30WqJwcep0pYcV4AMNc?si=ed4b04f153a24531'
def update_song_url():
    st.session_state.s_url = st.session_state.song_url

if 'sn_url' not in st.session_state:
    st.session_state.sn_url = 'In The End'
def update_song_name_url():
    st.session_state.sn_url = st.session_state.songname_url

if 'a_url' not in st.session_state:
    st.session_state.a_url = 'Example: https://open.spotify.com/artist/3RNrq3jvMZxD9ZyoOZbQOD?si=UNAsX20kRpG89bxOO8o7ew'
def update_artist_url():
    st.session_state.a_url = st.session_state.artist_url


def play_recomm():
    if 'rs' in st.session_state:
        del st.session_state.rs,st.session_state.err
    try:
        if len(pd.read_csv('Data/new_tracks.csv')) >= 200:
            with st.spinner('Updating the dataset...'):
                x=update_dataset()
                st.success('{} New tracks were added to the dataset.'.format(x))
    except:
        st.error("The dataset update failed. ")
    with st.spinner('Getting Recommendations...'):
        res,err = playlist_model(st.session_state.p_url,st.session_state.model,st.session_state.genre,st.session_state.artist)
        st.session_state.rs=res
        st.session_state.err=err
    if len(st.session_state.rs)>=1:
        if st.session_state.model == 'Model 1' or st.session_state.model == 'Model 2':
            st.success('Go to the Result page to view the top {} recommendations'.format(len(st.session_state.rs)))

        else:
            st.success('Go to the Result page to view the  Spotify recommendations')
    else:
        st.error('Model failed. Please try again')   

def art_recomm():
    if 'rs' in st.session_state:
        del st.session_state.rs,st.session_state.err
    with st.spinner('Getting Recommendations...'):
        res,err = top_tracks(st.session_state.a_url,st.session_state.rg)
        st.session_state.rs=res
        st.session_state.err=err
    if len(st.session_state.rs)>=1:
        st.success("Your results are ready! Go to the Result Page to see the recommendations")
    else:
        st.error('Model failed, please try again')

def song_recomm():
    if 'rs' in st.session_state:
        del st.session_state.rs,st.session_state.err
    with st.spinner('Getting Recommendations...'):
        res,err = song_model(st.session_state.s_url,st.session_state.model,st.session_state.genre,st.session_state.artist)
        st.session_state.rs=res
        st.session_state.err=err
    if len(st.session_state.rs)>=1:
        if st.session_state.model == 'Model 1' or st.session_state.model == 'Model 2':
            st.success('Go to the Result page to view the top {} recommendations'.format(len(st.session_state.rs)))
        else:
            st.success('Go to the Result page to view the  Spotify recommendations')
    else:
        st.error('Model failed. Please try again.')

def playlist_page():
    st.subheader("User Playlist")
    st.markdown('---')
    playlist_uri = (st.session_state.playlist_url).split('/')[-1].split('?')[0]
    uri_link = 'https://open.spotify.com/embed/playlist/' + playlist_uri
    components.iframe(uri_link, height=300)
    return

def song_page():
    st.subheader("User Song")
    st.markdown('---')
    song_uri = (st.session_state.song_url).split('/')[-1].split('?')[0]
    uri_link = 'https://open.spotify.com/embed/track/' + song_uri
    components.iframe(uri_link, height=100)

def artist_page():
    st.subheader("User Artist")
    st.markdown('---')
    artist_uri = (st.session_state.artist_url).split('/')[-1].split('?')[0]
    uri_link = 'https://open.spotify.com/embed/artist/' + artist_uri
    components.iframe(uri_link, height=80)


def spr_sidebar():
    menu=option_menu(
        menu_title=None,
        options=['Home','Result','About'],
        icons=['house','book','info-square','terminal'],
        menu_icon='cast',
        default_index=0,
        orientation='horizontal'
    )
    if menu=='Home':
        st.session_state.app_mode = 'Home'
    elif menu=='Result':
        st.session_state.app_mode = 'Result'
    elif menu=='About':
        st.session_state.app_mode = 'About'
    
def home_page():
    st.session_state.radio=st.session_state.feature
    st.session_state.radio2=st.session_state.model
    st.session_state.num_genre=st.session_state.genre
    st.session_state.same_art=st.session_state.artist
    st.session_state.Region=st.session_state.rg

    
    st.title('Helical Recommendation System')
    col,col2,col3=st.columns([2,2,3])
    radio=col.radio("Feature",options=("Playlist","Song","Artist Top Tracks"),key='radio',on_change=update_radio0)
    if radio =="Artist Top Tracks":
        radio1=col2.radio("Model",options=["Spotify model"],key='radio1',on_change=update_radio1)
        Region=col3.selectbox("Please Choose Region",index=58,key='Region',on_change=update_Region,options=('AD', 'AR', 'AU', 'AT', 'BE', 'BO', 'BR', 'BG', 'CA', 'CL', 'CO', 'CR', 'CY', 'CZ', 'DK', 'DO', 'EC', 'SV', 'EE', 'FI', 'FR', 'DE', 'GR', 'GT', 'HN', 'HK', 'HU', 'IS', 'ID', 'IE', 'IT', 'JP', 'LV', 'LI', 'LT', 'LU', 'MY', 'MT', 'MX', 'MC', 'NL', 'NZ', 'NI', 'NO', 'PA', 'PY', 'PE', 'PH', 'PL', 'PT', 'SG', 'ES', 'SK', 'SE', 'CH', 'TW', 'TR', 'GB', 'US', 'UY'))
    elif radio =="Playlist" or radio =="Song" :
        radio2=col2.radio("Model",options=("Model 1","Model 2","Spotify Model"),key='radio2',on_change=update_radio2)
        if st.session_state.radio2=="Model 1" or st.session_state.radio2=="Model 2":
            num_genre=col3.selectbox("choose a number of genres to focus on",options=(1,2,3,4,5,6,7),index=2,key='num_genre',on_change=update_num_genre)
            same_art=col3.selectbox("How many recommendations by the same artist",options=(1,2,3,4,5,7,10,15),index=3,key='same_art',on_change=update_same_art)


    st.markdown("<br>", unsafe_allow_html=True)
    
    if radio == "Playlist" :
        st.session_state.playlist_url = st.session_state.p_url
        Url = st.text_input(label="Playlist Url",key='playlist_url',on_change=update_playlist_url)
        playlist_page()
        state =st.button('Get Recommendations')
        with st.expander("Here's how to find any Playlist URL in Spotify"):
            st.write(""" 
                - Search for Playlist on the Spotify app
                - Right Click on the Playlist you like
                - Click "Share"
                - Choose "Copy link to playlist"
            """)
            st.markdown("<br>", unsafe_allow_html=True)
            st.image('spotify_get_playlist_url.png')
        if state:
            play_recomm()
    elif radio == "Song" :
        st.session_state.songname_url = st.session_state.sn_url
        Url_a = st.text_input(label="Type a songs name to get the url for",key='get_url',on_change=update_song_name_url)

        from spotifysearch.client import Client
        myclient = Client(Client_id, client_secret)
        results = myclient.search(Url_a)
        tracks = results.get_tracks()

        track = tracks
        
        result_length = len(tracks)

        track_song_list = []
        track_url_list = []
        track_actual_url_list = []
        anotherlist=[]


        genrec = st.radio(
            "Choose an option to search in:",
            ["5x4"])


        if genrec == "Full":
        
            for leupz in range(result_length):
                thetrack = tracks[leupz]
                st.write(thetrack.name)
                name_desu = thetrack.name
                track_song_list.append(name_desu)
            
                st.write(thetrack.url)            
                urlname_desu = thetrack.name           
                track_url_list.append(urlname_desu)      
            
                song_uri = (thetrack.url).split('/')[-1].split('?')[0]
                uri_link = 'https://open.spotify.com/embed/track/' + song_uri
                components.iframe(uri_link, height=100)


            st.write(result_length)

        elif genrec == "5x4":
            for leupz in range(result_length):
                thetrack = tracks[leupz]

                name_desu = thetrack.name
                track_song_list.append(name_desu)
            
       
                urlname_desu = thetrack.url          
                track_url_list.append(urlname_desu)      
            
                song_uri = (thetrack.url).split('/')[-1].split('?')[0]
                uri_link = 'https://open.spotify.com/embed/track/' + song_uri
                dem = uri_link

                track_actual_url_list.append(dem)
            notneeded_chkbox = st.checkbox('Click on this to see the results')

            if notneeded_chkbox:
########### WARNING: MAY CAUSE SOME TO FAINT :/
                
                st.write('Feature activated!')

                pages = st.radio("Page",["1","2","3","4",], horizontal=True)

                if pages == "1":
                    Le_songs = st.radio(
                        "Its time to choose...",
                        [track_song_list[0],track_song_list[1],track_song_list[2],track_song_list[3],track_song_list[4]])
                    
                    if Le_songs == track_song_list[0]:
                        st.session_state.s_url = track_actual_url_list[0]
                        
                    elif Le_songs == track_song_list[1]:
                        st.session_state.s_url = track_actual_url_list[1]
                        
                    elif Le_songs == track_song_list[2]:
                        st.session_state.s_url = track_actual_url_list[2]
                    
                    elif Le_songs == track_song_list[3]:
                        st.session_state.s_url = track_actual_url_list[3]
                        
                    elif Le_songs == track_song_list[4]:
                        st.session_state.s_url = track_actual_url_list[4]
                        
                        
                    st.write('Previews')
                
                    components.iframe(track_actual_url_list[0], height=100)
                    components.iframe(track_actual_url_list[1], height=100)
                    components.iframe(track_actual_url_list[2], height=100)
                    components.iframe(track_actual_url_list[3], height=100)
                    components.iframe(track_actual_url_list[4], height=100)
                    

                if pages == "2":
                    Le_songs = st.radio(
                        "Its time to choose...",
                        [track_song_list[5],track_song_list[6],track_song_list[7],track_song_list[8],track_song_list[9]])
                    if Le_songs == track_song_list[5]:
                        st.session_state.s_url = track_actual_url_list[5]
                        
                    elif Le_songs == track_song_list[6]:
                        st.session_state.s_url = track_actual_url_list[6]
                        
                    elif Le_songs == track_song_list[7]:
                        st.session_state.s_url = track_actual_url_list[7]
                    
                    elif Le_songs == track_song_list[8]:
                        st.session_state.s_url = track_actual_url_list[8]
                        
                    elif Le_songs == track_song_list[9]:
                        st.session_state.s_url = track_actual_url_list[9]
                        
                    st.write('Previews')
                
                    components.iframe(track_actual_url_list[5], height=100)
                    components.iframe(track_actual_url_list[6], height=100)
                    components.iframe(track_actual_url_list[7], height=100)
                    components.iframe(track_actual_url_list[8], height=100)
                    components.iframe(track_actual_url_list[9], height=100)
                if pages == "3":
                    Le_songs = st.radio(
                        "Its time to choose...",
                        [track_song_list[10],track_song_list[11],track_song_list[12],track_song_list[13],track_song_list[14]])

                    if Le_songs == track_song_list[10]:
                        st.session_state.s_url = track_actual_url_list[10]
                        
                    elif Le_songs == track_song_list[11]:
                        st.session_state.s_url = track_actual_url_list[11]
                        
                    elif Le_songs == track_song_list[12]:
                        st.session_state.s_url = track_actual_url_list[12]
                    
                    elif Le_songs == track_song_list[13]:
                        st.session_state.s_url = track_actual_url_list[13]
                        
                    elif Le_songs == track_song_list[14]:
                        st.session_state.s_url = track_actual_url_list[14]
                    
                    st.write('Previews')
                
                    components.iframe(track_actual_url_list[10], height=100)
                    components.iframe(track_actual_url_list[11], height=100)
                    components.iframe(track_actual_url_list[12], height=100)
                    components.iframe(track_actual_url_list[13], height=100)
                    components.iframe(track_actual_url_list[14], height=100)
                if pages == "4":
                    Le_songs = st.radio(
                        "Its time to choose...",
                        [track_song_list[15],track_song_list[16],track_song_list[17],track_song_list[18],track_song_list[19]])

                    if Le_songs == track_song_list[15]:
                        st.session_state.s_url = track_actual_url_list[15]
                        
                    elif Le_songs == track_song_list[16]:
                        st.session_state.s_url = track_actual_url_list[16]
                        
                    elif Le_songs == track_song_list[17]:
                        st.session_state.s_url = track_actual_url_list[17]
                    
                    elif Le_songs == track_song_list[18]:
                        st.session_state.s_url = track_actual_url_list[18]
                        
                    elif Le_songs == track_song_list[19]:
                        st.session_state.s_url = track_actual_url_list[19]
                    
                    st.write('Previews')
                
                    components.iframe(track_actual_url_list[15], height=100)
                    components.iframe(track_actual_url_list[16], height=100)
                    components.iframe(track_actual_url_list[17], height=100)
                    components.iframe(track_actual_url_list[18], height=100)
                    components.iframe(track_actual_url_list[19], height=100)
                    
                else:
                    st.write("""If you have clicked on an option, click on "Get recommendations" button to get recommendations""")

     
                st.write(result_length)
        
        st.session_state.song_url = st.session_state.s_url
        Url = st.text_input(label="Song Url ",key='song_url',on_change=update_song_url)
    
        song_page()
        state =st.button('Get Recommendations')
        with st.expander("Here's how to find any Song URL in Spotify"):
            st.write(""" 
                - Search for Song on the Spotify app
                - Right Click on the Song you like
                - Click "Share"
                - Choose "Copy link to Song"
            """)
            st.markdown("<br>", unsafe_allow_html=True)
            st.image('spotify_get_song_url.png')

            
        if state:
            song_recomm()
    elif radio == "Artist Top Tracks" :
        st.session_state.artist_url = st.session_state.a_url
        Url = st.text_input(label="Artist Url",key='artist_url',on_change=update_artist_url)
        artist_page()
        state =st.button('Get Recommendations')
        with st.expander("Here's how to find any Artist URL in Spotify"):
            st.write(""" 
                - Search for Artist on the Spotify app
                - Right Click on the Artist you like
                - Click "Share"
                - Choose "Copy link to Artist"
            """)
            st.markdown("<br>", unsafe_allow_html=True)
            st.image('spotify_get_artist_url.png')
        if state:
            art_recomm()
    
def result_page():
    if 'rs' not in st.session_state:
        st.error('Please select a model on the Home page and run Get Recommendations')
    else:
        st.success('Top {} recommendations'.format(len(st.session_state.rs)))
        i=0
        for uri in st.session_state.rs:
         uri_link = "https://open.spotify.com/embed/track/" + uri + "?utm_source=generator&theme=0"
         components.iframe(uri_link, height=80)
         i+=1
         if i%5==0:
            time.sleep(1)
def About_page():
    st.header('Development')
def main():
    spr_sidebar()        
    if st.session_state.app_mode == 'Home':
        home_page()
    if st.session_state.app_mode == 'Result':
        result_page()
    if st.session_state.app_mode == 'About' :
        About_page()
# Run main()
#if __name__ == '__main__': this doesnt allow reletive imports >:()
main()
