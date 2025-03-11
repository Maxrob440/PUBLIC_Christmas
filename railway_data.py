"""some yap so pylint is happy"""
import http.client
import json
from datetime import datetime, timedelta,date
from time import sleep
import traceback
import os
from random import randint
import urllib.parse
import logging

CURRENTLY_DISPLAYING = 'photos/currently_displaying.svg'

logger = logging.getLogger(__name__)
logging.basicConfig(filename='myapp.log', level=logging.INFO)

destination_crs = {
    'Exeter St Davids':'EXD',
    'Exeter Central':'EXC',
    'Okhampton':'OKE',
}
def days_since_june_15_2023():
    # Define the target date
    target_date = date(2023, 6, 15)
    # Get today's date
    today = date.today()
    # Calculate the difference in days
    days_difference = (today - target_date).days
    return days_difference

def display_cancelled_train(next_train_data):
    """Displays a cancelled train message"""
    print('Train cancelled!!!')
    avaliable_pictures = os.listdir('photos/portraits')
    random_picture = avaliable_pictures[randint(0,len(avaliable_pictures)-1)]
    with open(f'photos/portraits/{random_picture}', 'r', encoding='utf-8') as f:
        picture = f.read()
        picture = picture.replace('__days DAYS WELL SPENT', 'Next train is cancelled')

    with open(CURRENTLY_DISPLAYING, 'w', encoding='utf-8') as f:
        f.write(picture)
def display_new_error_message(error):
    """Displays an error message"""
    avaliable_pictures = os.listdir('photos/portraits')
    random_picture = avaliable_pictures[randint(0,len(avaliable_pictures)-1)]
    with open(f'photos/portraits/{random_picture}', 'r', encoding='utf-8') as f:
        picture = f.read()
        # picture = picture.replace('ERROR_CODE', error)
        picture = picture.replace('__days DAYS WELL SPENT', f'ERROR {error} :/')

    with open(CURRENTLY_DISPLAYING, 'w', encoding='utf-8') as f:
        f.write(picture)


def display_pictures():
    """Displays the pictures"""
    number = randint(0,10)
    if number == 0:
        edit_picture_landscape()
        return
    avaliable_pictures = os.listdir('photos/portraits')
    random_picture = avaliable_pictures[randint(0,len(avaliable_pictures)-1)]
    logger.info(f'Portrait picture displayed-{random_picture}')

    with open(f'photos/portraits/{random_picture}', 'r', encoding='utf-8') as f:
        picture = f.read()
        picture = picture.replace('__days', str(days_since_june_15_2023()))

        picture = picture.replace('photo1', f'photos/portraits/{random_picture}')
        # picture = picture.replace('photo2', 'photos/iCloud Photos (8)/iCloud Photos/IMG_6773.JPEG')
    with open(CURRENTLY_DISPLAYING, 'w', encoding='utf-8') as f:
        f.write(picture)

def edit_picture_landscape():
    avaliable_pictures = os.listdir('photos/landscapes')

    random_picture = avaliable_pictures[randint(0,len(avaliable_pictures)-1)]
    logger.info(f'Landscape picture displayed-{random_picture}')
    with open(f'photos/landscapes/{random_picture}', 'r', encoding='utf-8') as f:
        picture = f.read()

    with open(CURRENTLY_DISPLAYING, 'w', encoding='utf-8') as f:
        f.write(picture)

def edit_picture(next_train_data,drive_time,minutes_until_time,minutes_sub_ten=False) -> None:
    """
    Edit the picture takes inputs of depart time, arrival_time, on time,drive_time,minutes
    Times must be in format %H%M
    """
    with open('Example_trains.svg', 'r', encoding='utf-8') as f:
        picture = f.read()
        picture = picture.replace('depart_time', next_train_data.departure_time)
        picture = picture.replace('arrival_time', next_train_data.arrival_time)
        picture = picture.replace('status', next_train_data.delayed)
        picture = picture.replace('drive_time', str(drive_time))
        picture = picture.replace('minutes', str(minutes_until_time))
        picture = picture.replace('destination_station',next_train_data.destination)
        if minutes_sub_ten:
            picture = picture.replace("change_to_red","fill:#ff0000;fill-opacity:1;stroke-width:0.472494")
        else:
            picture = picture.replace("change_to_red","fill:#ffffff;fill-opacity:1;stroke-width:0.472494")
    with open(CURRENTLY_DISPLAYING, 'w', encoding='utf-8') as f:
        f.write(picture)

def get_data(station,destination) -> None:
    """Gets the data from the api and saves it to a json file"""
    conn = http.client.HTTPSConnection("api1.raildata.org.uk")
    payload = ''
    headers = {
    'x-apikey': 'Add API KEY HERE',
    'numRows':10,
    }
    api = f"/1010-live-departure-board-dep/LDBWS/api/20220120/GetDepBoardWithDetails/{station}?filterCRS={destination}"
    conn.request("GET", api, payload, headers)
    res = conn.getresponse()
    data_from_api = res.read()
    data_from_api = data_from_api.decode("utf-8")
    data_as_json = json.loads(data_from_api)

    with open('data.json', 'w', encoding='utf-8') as f:
        json.dump(data_as_json, f, ensure_ascii=False, indent=4)

def open_data():
    """Opens the data.json file and returns it as a json object"""
    with open('data.json', 'r', encoding='utf-8') as f:
        data_as_json = json.load(f)
    return data_as_json

def time_taken_to_get_to_station() -> int:
    """Returns the time taken to get to the station, currently just returns but will get smart"""

    return 1

def current_time():
    """Returns current time in %H:%M format"""
    time = datetime.now()
    return time.strftime("%H:%M")

def time_arrive_at_station(time_now,time_to_station):
    """Returns the time you will arrive at the station"""
    time_now = datetime.strptime(time_now, "%H:%M")
    time_arriving_at_station = time_now + timedelta(minutes=time_to_station)
    time_arriving_at_station = time_arriving_at_station.strftime("%H:%M")
    return time_arriving_at_station

class Queue():
    """Last in Last out Queue, operations - queue, dequeue"""
    def __init__(self):
        self.items = []
    def queue(self, item):
        """Adds an item to the queue"""
        self.items.append(item)
    def dequeue(self):
        """Removes the first item from the queue"""
        del self.items[0]
        return self.items
    def show_head(self):
        """Shows the first item in the queue"""
        return self.items[0]
    def __str__(self):
        return str(self.items)

class Train():
    """Train object, contains start location, destination, departure time and arrival time"""
    def __init__(self,start_location,destination,departure_time,arrival_time,delayed,cancelled):
        self.start_location=start_location
        self.destination=destination
        self.departure_time = departure_time
        self.arrival_time = arrival_time
        self.delayed = delayed
        self.cancelled = cancelled


def update_queue(data,all_train,time_at_station):
    """Updates the queue with the next trains"""
    for x in range(len(data['trainServices'])):
        train_time = str(data['trainServices'][x]['std'])
        if train_time not in all_train.items and data['trainServices'][x]['std'] > time_at_station:
            all_train.queue(data['trainServices'][x]['std'])
    while all_train.items[0] <= time_at_station:
        all_train.dequeue()
    return all_train

def get_train_data(data,numbers,destination):
    """Returns the train data"""
    for x in numbers:
        try:
            start_location = data['trainServices'][x]['origin'][0]['locationName']
            # destination = data['trainServices'][number]['destination'][0]['locationName']
            departure_time = data['trainServices'][x]['std']
            stations = data['trainServices'][x]['subsequentCallingPoints'][0]['callingPoint']
            index_station = [x for x in range(len(stations)) if stations[x]['locationName'] == destination]
            if index_station == []:
                print('Error, destination not found')
            arrival_time = stations[index_station[0]]['st']
            delayed = data['trainServices'][x]['etd']
            cancelled = data['trainServices'][x]['isCancelled']
            return Train(start_location,destination,departure_time,arrival_time,delayed,cancelled)
        except IndexError:
            print('This train not going there, trying next')
    return False



def get_next_train_info(station_name,destination,destination_crs,time_taken_to_get_to_station):
    all_train = Queue()

    while True:
        try:
            if destination not in destination_crs:
                print('Destination not found')
                return
            else:
                destination_crs_str = destination_crs[destination]

            get_data(station_name,destination_crs_str)
        except http.client.RemoteDisconnected:
            print('Error getting data, using old data')
        try:
            time_at_station = time_arrive_at_station(current_time(),time_taken_to_get_to_station)
            data = open_data()
            all_train = update_queue(data,all_train,time_at_station)
            next_train = all_train.show_head()
            numbers = [x for x in range(len(data['trainServices'])) if data['trainServices'][x]['std'] == next_train]
            next_train_data = get_train_data(data,numbers,destination)
            if next_train_data == False:
                print('Next trains not going to destination')
                display_new_error_message('24')
                return False,False
            departure_time_hours = int(all_train.show_head().split(':')[0])
            departure_time_minutes = int(all_train.show_head().split(':')[1])
            departure_time = timedelta(hours = departure_time_hours,minutes = departure_time_minutes)
            recommended_time = departure_time - timedelta(minutes=time_taken_to_get_to_station)
            time_hours = int(current_time().split(':')[0])
            time_minutes = int(current_time().split(':')[1])
            minutes_until_time = recommended_time - timedelta(hours=time_hours,minutes = time_minutes)
            print((f'1st {next_train_data.departure_time} {next_train_data.destination} {next_train_data.delayed} '))
            return next_train_data,minutes_until_time
        except (IndexError,KeyError):
            print('No trains found')
            # display_new_error_message('23')
            return False,False

def choose_what_to_display(setting,*args):
    """Chooses what to display"""
    minutes_until_time = args[0]
    next_train_data = args[1]
    minutes_sub_ten = False
    print(setting,'SETTING')
    if setting:
        return setting,minutes_sub_ten

    if minutes_until_time >= 20:
        return 'photos',minutes_sub_ten
    elif minutes_until_time < 20:
        if next_train_data.delayed == 'Cancelled':
            return 'train_cancelled',minutes_sub_ten
        if minutes_until_time < 10:
            minutes_sub_ten = True
        return 'minutes_until_train',minutes_sub_ten
    else:
        return 'error','100'
    
def change_display(to_display,minutes_sub_ten,*args):
    if args:
        next_train_data,minutes_to_station,minutes_until_time=args[0],args[1],args[2]
    if to_display == 'error':
        display_new_error_message(minutes_sub_ten) #this is error code
    elif to_display == 'photos':
        display_pictures()
    elif to_display == 'minutes_until_train':
        edit_picture(next_train_data,minutes_to_station,minutes_until_time,minutes_sub_ten)
    elif to_display == 'train_cancelled':
        print('Train cancelled')
        display_cancelled_train(next_train_data)



def adjust_minutes(minutes_until_time):
    minutes = str(time_taken_to_get_to_station())
    minutes_until_time = str(minutes_until_time)[2:4]
    minutes_until_time_int = int(minutes_until_time)
    if minutes_until_time_int == 1:
        minutes_until_time_text = '1 MINUTE'
    elif minutes_until_time == '00':
        minutes_until_time_text = '> AN HOUR'
    elif minutes_until_time_int < 10:
        minutes_until_time_text = f'{minutes_until_time_int} MINUTES'
    else:
        minutes_until_time_text = f'{minutes_until_time} MINUTES'


    return minutes,minutes_until_time_int,minutes_until_time_text


