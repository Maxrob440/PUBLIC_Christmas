from railway_data import get_next_train_info,choose_what_to_display,change_display,adjust_minutes,edit_picture_landscape,display_pictures
from time import sleep,strftime,gmtime
from  current_mode import mode
from buttonpress import get_button_press
import traceback
import subprocess
import logging

logger = logging.getLogger(__name__)
logging.basicConfig(filename='myapp.log', level=logging.INFO)


sleep(10)
def run_eog():
    subprocess.run(['killall','eog'])
    logger.info('Running eog')
    image_path = "photos/currently_displaying.svg"
    subprocess.Popen(['eog','--fullscreen', image_path])
    logger.info('eog ran')

UPDATE_FREQUENCY = 30
EOG_FREQUENCY = 700
current_mode = mode()
#self.mode = ['photos','minutes_until_train',None]

current_mode.set_mode(None)
# current_mode.change_mode()
# current_mode.change_mode()
minutes_to_station = 18
destination_crs = {
    'Exeter St Davids':'EXD',
    'Exeter Central':'EXC',
    'Okhampton':'OKE',
}

def act_on_buttonpress():
    result = get_button_press()
    if result == True:
        current_mode.set_mode('minutes_until_train')
        # print('button is pressed')
    else:
        current_mode.set_mode('photos')
        # print('button not pressed')
    return current_mode.get_mode()

def main(station,destination,destination_crs,setting=None):
    logger.info('Main function started at time {}'.format(strftime("%Y-%m-%d %H:%M:%S", gmtime())))
    minutes_sub_ten = False
    display_pictures()
    time_waiting = 0
    eog_timer = 0
    while time_waiting <= UPDATE_FREQUENCY:
        setting = act_on_buttonpress()
        # setting = 'photos'
        sleep(1)
        time_waiting+=1
        eog_timer+=1
    if eog_timer >= EOG_FREQUENCY:
        run_eog()
        eog_timer = 0
    if setting=='photos':
        change_display('photos',minutes_sub_ten)
    next_train_data,minutes_to_next_train = get_next_train_info(station,destination,destination_crs,minutes_to_station)
    # print(next_train_data.delayed)
    if next_train_data == False:
        print('No trains found')
        print('Displaying photos')
        to_display = 'photos'
        minutes_until_time_text = 'You shoulnt see this :)'
    else:
        minutes, minutes_until_time_int, minutes_until_time_text = adjust_minutes(minutes_to_next_train)
        to_display,minutes_sub_ten = choose_what_to_display(setting,minutes_until_time_int,next_train_data)
    change_display(to_display,minutes_sub_ten,next_train_data,minutes_to_station,minutes_until_time_text)

run_eog()
while True:
    try:
        main('OKE','Exeter St Davids',destination_crs,current_mode.get_mode())
    except Exception as e:
        run_eog()
        print(e)
        print('ERROR restarting in 120')
        logger.error(e)
        sleep(120)
        traceback.print_exc()
