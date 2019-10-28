import time  # Used for Sleep Function
import os  # For System Commands
import re  # For Splitting
import win10toast # For notifications
import spotipy # Spotify Python API
import spotipy.util as util # Util for Spotify API
import speech_recognition as sr  # Main SR API

from datetime import datetime # Check date
from keyboardVirtual import Keyboard  # Faked Key Presses (Different from normal module)
from googleapiclient.discovery import build # For Youtube API

r = sr.Recognizer()
notification = win10toast.ToastNotifier()

# Youtube Settings
youtube = build('youtube', 'v3', developerKey="AIzaSyDu5qoUXtLVam1LytJi26Z_Is48jq0zVyM")
# Spotify Client Settings
client_id = '8654953b081e4a93be3dc54a0bb94b76'
client_secret = 'ddf018ff1b3b4681878b036d6518ac29'
redirect_uri = 'http://google.com/'
# Username & Scope, and Prompt for user permission
# username = '21tsyxc5cuuvesyb6gfxa3nia'
username = ''
scope = 'user-read-private user-read-playback-state user-modify-playback-state'
token = util.prompt_for_user_token(username, scope, client_id, client_secret, redirect_uri)
# Create Spotify Object
spotifyObject = spotipy.Spotify(auth=token)

current_device = ''

MainKeys = [["open"],
            ["close", "exit", "quit"],
            ["date", "time"],
            ["search"],
            [["shut", "down"], ["turn", "off"], ["close", "down"], ["shutdown", "turnoff", "closedown"]],
            ["restart", "reinstate", "retard"],
            ["play", "lay"],
            ["set", "volume"],
            ["calculate", "evaluate"],
            ["next", "skip"],
            ["previous"],
            ["pause", "mouse"]]

explorer_list = ["explore", "explorer", "folder"]
taskview_list = ["task", "view", "taskview"]
mword_list = ["word", "words"]
mexcel_list = ["excel", "spreadsheet"]
mpowerpoint_list = ["powerpoint"]
spotify_list = ["spotify", "music"]
browser_list = ["browser", "google", "chrome"]
search_internet_list = ["google", "youtube"]
phone_list = ["phone", "smartphone", "iphone", "samsung", "android"]

text = ''

def get_audio():
    with sr.Microphone() as source:
        r.adjust_for_ambient_noise(source, duration=2)
        print("Speak Anything: ")
        audio = r.listen(source)
        # audio = r.record(source, duration=4)
        try:
            global text
            text = r.recognize_google(audio, language="EN-US")
            # print("You Said: {}".format(text))
        except:
            print("Sorry could not recognize your voice")
            return
    return text.lower()


def split_command(text):
    # If audio wasn't recognized
    try:
        input = text.split()
    except AttributeError:
        return
    # If multiple command
    if ("then" in input) or ("and" in input):
        input2 = re.split('then|and', text)
        for i in input2:
            parse_text(i.split())
            time.sleep(1)
    else:
        parse_text(input)


def parse_text(input):
    # If search and play
    if any(x in input for x in MainKeys[3]) or (any(x in input for x in MainKeys[6]) or any(x in input for x in MainKeys[11])):
        for word in input:
            if word in MainKeys[3]:
                internet_stuff(input)
                return
            if word in MainKeys[6] or word in MainKeys[11]:
                if "youtube" in input:
                    play_youtube(input)
                    return
                if "spotify" in input:
                    play_spotify(input, "Computer")
                    return
                if any(x in input for x in phone_list):
                    play_spotify(input, "Smartphone")
                    return
                media_pause_play()
    # Open Stuff
    if any(x in input for x in MainKeys[0]):
        open_stuff(input)
        return
    # Close Stuff
    if any(x in input for x in MainKeys[1]):
        close_stuff(input)
        return
    # Check Date
    if any(x in input for x in MainKeys[2]):
        check_date()
        return
    # Shutdown Computer
    if all(x in input for x in MainKeys[4][0]) or all(x in input for x in MainKeys[4][1]) or \
    all(x in input for x in MainKeys[4][2]) or any(x in input for x in MainKeys[4][3]):
        print("Are you sure?")
        if get_audio() == "yes":
            shutdown()
        return
    # Restart Computer
    if any(x in input for x in MainKeys[5]):
        print("Are you sure?")
        if get_audio() == "yes":
            restart()
        return
    # Set Volume
    if all(x in input for x in MainKeys[7]):
        for i in input:
            if '%' in i:
                set_volume(int(i.split('%')[0]))
        return
    # Next Media
    if any(x in input for x in MainKeys[9]):
        next_media()
        return
    # Prev Media
    if any(x in input for x in MainKeys[10]):
        prev_media()
        return
    # Evaluate/Calculate
    if any(x in input for x in MainKeys[8]):
        evaluator(input)
        return


def open_stuff(text):
    # Open Explorer
    if any(word in text for word in explorer_list):
        open_explorer()
        return
    # Open Task View
    if all(word in text for word in taskview_list[:2]) or (taskview_list[2] in text):
        open_taskview()
        return
    # Open Microsoft Applications (word, excel, powerpoint)
    if "microsoft" in text:
        if any(word in text for word in mword_list):
            microsoft_word()
            return
        if any(word in text for word in mexcel_list):
            microsoft_excel()
            return
        if any(word in text for word in mpowerpoint_list):
            microsoft_powerpoint()
            return
    # Open Spotify
    if any(word in text for word in spotify_list):
        open_spotify()
        return
    # Open Browser or Chrome
    if any(word in text for word in browser_list):
        open_chrome()
        return


def close_stuff(text):
    # Close Microsoft Applications (word, excel, powerpoint)
    if "microsoft" in text:
        if any(word in text for word in mword_list):
            close_word()
            return
        if any(word in text for word in mexcel_list):
            close_excel()
            return
        if any(word in text for word in mpowerpoint_list):
            close_powerpoint()
            return
    # Close Spotify
    if any(word in text for word in spotify_list):
        close_spotify()
        return
    # Close Browser or Chrome
    if any(word in text for word in browser_list):
        close_chrome()
        return


# Search on the internet
def internet_stuff(text):
    if "google" in text:
        search_options(text, 1)
        return
    if "youtube" in text:
        search_options(text, 2)
        return

# Searching (Google and Youtube)
def search_options(input, setting):
    # Getting search array
    search_array = get_SearchArray(input, setting, 1)
    seperator = "+"
    searchquery = seperator.join(search_array)
    if setting == 1:
        os.system("start www.google.com/search?q=" + searchquery)
    elif setting == 2:
        os.system("start www.youtube.com/results?search_query=" + searchquery)

# Getting Search Query
def get_SearchArray(input, setting, setting2):
    settingtype = ""
    settingtype2 = ""
    # Determines whether google/youtube search
    if setting == 1:
        settingtype = "google"
    elif setting == 2:
        settingtype = "youtube"
    elif setting == 3:
        settingtype = "spotify"
    elif setting == 4:
        for phone in phone_list:
            if phone in input:
                settingtype = phone
    # Determines whether search or directly click on line
    if setting2 == 1:
        settingtype2 = "search"
    elif setting2 == 2:
        settingtype2 = "play"
    # Assign settings
    startg = input.index(settingtype)
    starts = input.index(settingtype2)
    search_array = []
    if startg == (len(input) - 1):
        search_array = input[starts + 1:-2]
    elif startg > starts:
        search_array = input[startg + 1:]
    elif starts > startg:
        search_array = input[starts + 1:]
    return search_array

# Play query on Youtube
def play_youtube(text):
    # Getting search_query
    search_array = get_SearchArray(text, 2, 2)
    print(search_array)
    separator = " "
    searchquery = separator.join(search_array)
    # Getting VideoID and Playing it
    req = youtube.search().list(q=searchquery, part='snippet', type='video')
    res = req.execute()
    id = res['items'][0]['id']['videoId']
    command = "start https://youtube.com/watch?v=" + id
    os.system(command)

# Get Spotify Device ID
def get_device_id(device_type):
    device_id = ""
    # Get list of devices
    devices = spotifyObject._get('me/player/devices')['devices']
    if len(devices) == 0:
        return 1
    for device in devices:
        if device['type'] == device_type:
            return device['id']
    return 2

# Play song on spotify
def play_spotify(text, device_type):
    # Getting search_query
    search_array = []
    if device_type == "Computer":
        search_array = get_SearchArray(text, 3, 2)
    if device_type == "Smartphone":
        search_array = get_SearchArray(text, 4, 2)
    separator = " "
    search_query = separator.join(search_array)
    print(search_query)
    # Getting Track URI
    if search_query == "":
        notification.show_toast("Spotify Warning", "Nothing to search", duration=5, threaded=True)
        return
    current_market = spotifyObject.current_user()['country']
    searchResult = spotifyObject.search(search_query, type='track', limit=1, market=current_market)
    # print(json.dumps(searchResult, sort_keys=True, indent=4))
    try:
        track_uri = searchResult['tracks']['items'][0]['uri']
    except IndexError:
        notification.show_toast("Spotify Warning", "No result for the following query, please try again.", duration=5, threaded=True)
        return
    print(track_uri)
    # Getting Device ID
    device_id = get_device_id(device_type)
    if device_id == 1:
        notification.show_toast("Spotify Warning", "There are no devices available currently", duration=5, threaded=True)
        return
    if device_id == 2:
        notification.show_toast("Spotify Warning", "The type of device you're looking for aren't available now", duration=5, threaded=True)
        return
    # Playing track
    data = {
        'uris': [track_uri]
    }
    url = 'me/player/play?device_id=' + device_id
    spotifyObject._put(url, payload=data)
    # Stores current device id
    global current_device
    current_device = device_id


# Open Stuff Functions
def open_explorer():
    os.system('start explorer')
    notification.show_toast('Windows Explorer', 'Successfully opened', icon_path='icon/explorer.ico', duration=3, threaded=True)

def open_taskview():
    print("open taskview")
    Keyboard.keyDown(Keyboard.VK_LWIN)
    Keyboard.keyDown(Keyboard.VK_TAB)
    Keyboard.keyUp(Keyboard.VK_LWIN)
    Keyboard.keyUp(Keyboard.VK_TAB)
    notification.show_toast('Taskview', 'Successfully opened', duration=3, threaded=True)

def microsoft_word():
    os.system('start winword')
    time.sleep(1)
    notification.show_toast('Microsoft Word', 'Successfully opened', icon_path='icon/ms-word.ico', duration=3, threaded=True)

def microsoft_excel():
    os.system('start excel')
    time.sleep(1)
    notification.show_toast('Microsoft Excel', 'Successfully opened', icon_path='icon/ms-excel.ico', duration=3, threaded=True)

def microsoft_powerpoint():
    os.system('start powerpnt')
    time.sleep(1)
    notification.show_toast('Microsoft PowerPoint', 'Successfully opened', icon_path='icon/ms-powerpoint.ico',duration=3, threaded=True)

def open_spotify():
    os.system('start spotify')
    time.sleep(1)
    notification.show_toast('Spotify', 'Successfully opened', icon_path='icon/spotify.ico', duration=3, threaded=True)
    time.sleep(1)

def open_chrome():
    os.system('start chrome')
    time.sleep(1)
    notification.show_toast('Chrome', 'Successfully opened', icon_path='icon/chrome.ico', duration=3, threaded=True)
    time.sleep(1)


# Close Stuff Functions
def close_word():
    os.system('taskkill /im winword.exe /f')
    notification.show_toast('Microsoft Word', 'Successfully closed', icon_path='icon/ms-word.ico', duration=3, threaded=True)

def close_excel():
    os.system('taskkill /im excel.exe /f')
    notification.show_toast('Microsoft Excel', 'Successfully closed', icon_path='icon/ms-excel.ico', duration=3, threaded=True)

def close_powerpoint():
    os.system('taskkill /im powerpnt.exe /f')
    notification.show_toast('Microsoft PowerPoint', 'Successfully closed', icon_path='icon/ms-powerpoint.ico', duration=3, threaded=True)

def close_spotify():
    os.system('taskkill /im spotify.exe /f')
    notification.show_toast('Spotify', 'Successfully closed', icon_path='icon/spotify.ico', duration=3, threaded=True)

def close_chrome():
    os.system('taskkill /im chrome.exe /f')
    notification.show_toast('Chrome', 'Chrome closed', icon_path='icon/chrome.ico', duration=3, threaded=True)


# System Functions
def check_date():
    now = datetime.now()
    dt_string = now.strftime("%d/%m/%y %H:%M")
    notification.show_toast(dt_string, "Date & Time", duration=5, threaded=True)

def shutdown():
    # os.system('shutdown /s')
    print("computer shutdown")

def restart():
    # os.system('shutdown /r')
    print("computer restart")

def media_pause_play():
    Keyboard.key(Keyboard.VK_MEDIA_PLAY_PAUSE)
    time.sleep(1)
    notification.show_toast("Media", "Play/Pause", duration=3, threaded=True)
    

def set_volume(num):
    for i in range(50):
        Keyboard.key(Keyboard.VK_VOLUME_DOWN)
    for i in range(int(num / 2)):
        Keyboard.key(Keyboard.VK_VOLUME_UP)
        string = 'Volume set to ' + str(num) + '%'
        notification.show_toast("Media", string, duration=3, threaded=True)

def next_media():
    Keyboard.key(Keyboard.VK_MEDIA_NEXT_TRACK)
    time.sleep(1)
    notification.show_toast("Media", "Next Track", duration=3, threaded=True)

def prev_media():
    Keyboard.key(Keyboard.VK_MEDIA_PREV_TRACK)
    Keyboard.key(Keyboard.VK_MEDIA_PREV_TRACK)
    time.sleep(1)
    notification.show_toast("Media", "Previous Track", duration=3, threaded=True)

# Evaluate/Calculate Functions
def evaluator(exp, eval_regex=r'^(\d+|\+|-|\*|\/)$'):
    checked = []
    for i in range(len(exp)):
        if re.match(eval_regex, exp[i], re.M):
            checked.append(exp[i])
    try:
        result = str(eval("".join(checked)))
        notification.show_toast(result, "Result", icon_path='icon/calculator.ico', duration=3, threaded=True)
    except SyntaxError:
        notification.show_toast("Wrong Syntax", "Please try again", duration=3, threaded=True)