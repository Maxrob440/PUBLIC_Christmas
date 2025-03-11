import RPi.GPIO as GPIO
import time
GPIO.setwarnings(False)
GPIO.setmode(GPIO.BOARD)


GPIO.setup(10,GPIO.IN,pull_up_down=GPIO.PUD_DOWN)
GPIO.setup(12,GPIO.OUT)
def get_button_press():

    if GPIO.input(10) == GPIO.HIGH:
            GPIO.output(12,GPIO.HIGH)
            return True
    else:
            GPIO.output(12,GPIO.LOW)
            return False
