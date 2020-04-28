# /etc/init.d/main.py
### BEGIN INIT INFO
# Provides:          sample.py
# Required-Start:    $remote_fs $syslog
# Required-Stop:     $remote_fs $syslog
# Default-Start:     2 3 4 5
# Default-Stop:      0 1 6
# Short-Description: Start daemon at boot time
# Description:       Enable service provided by daemon.
### END INIT INFO

import RPi.GPIO as GPIO # Import Raspberry Pi GPIO library
import time
import threading

led_pin = 22
buzzer_pin = 18
switch_pin = 12
bad_pin = 15
good_pin = 13

class ButtonHandler(threading.Thread):
    def __init__(self, pin, func, edge='both', bouncetime=200):
        super().__init__(daemon=True)

        self.edge = edge
        self.func = func
        self.pin = pin
        self.bouncetime = float(bouncetime)/1000

        self.lastpinval = GPIO.input(self.pin)
        self.lock = threading.Lock()

    def __call__(self, *args):
        if not self.lock.acquire(blocking=False):
            return

        t = threading.Timer(self.bouncetime, self.read, args=args)
        t.start()

    def read(self, *args):
        pinval = GPIO.input(self.pin)

        if (
                ((pinval == 0 and self.lastpinval == 1) and
                 (self.edge in ['falling', 'both'])) or
                ((pinval == 1 and self.lastpinval == 0) and
                 (self.edge in ['rising', 'both']))
        ):
            self.func()

        self.lastpinval = pinval
        self.lock.release()

def bad_button_callback():
    time.sleep(0.05)
    print("Bad button was pushed!")
            
    BUZZER_REPETITIONS = 75
    BUZZER_DELAY = 0.0007
        
    for _ in range(BUZZER_REPETITIONS):
        for value in [True, False]:
            GPIO.output(buzzer_pin, value)
            time.sleep(BUZZER_DELAY)
        time.sleep(BUZZER_DELAY)
        
    GPIO.output(switch_pin, 0)
    GPIO.output(led_pin, 0)

def good_button_callback():
    time.sleep(0.05)
    print("Good button was pushed!")
            
    BUZZER_REPETITIONS = 75
    BUZZER_DELAY = 0.0007
        
    for _ in range(BUZZER_REPETITIONS):
        for value in [True, False]:
            GPIO.output(buzzer_pin, value)
            time.sleep(BUZZER_DELAY)
        time.sleep(BUZZER_DELAY)
    if (GPIO.input(switch_pin) == True):
        GPIO.output(switch_pin, 0)
        GPIO.output(led_pin, 0)
    else:
        GPIO.output(switch_pin, 1)
        GPIO.output(led_pin, 1)
    
    
GPIO.setwarnings(False) # Ignore warning for now
GPIO.setmode(GPIO.BOARD) # Use physical pin numbering

GPIO.setup(good_pin, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)
GB = ButtonHandler(good_pin, good_button_callback, edge='rising', bouncetime=100)
GB.start()

GPIO.setup(bad_pin, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)
BB = ButtonHandler(bad_pin, bad_button_callback, edge='rising', bouncetime=100)
BB.start()

GPIO.add_event_detect(good_pin, GPIO.RISING, callback=GB)
GPIO.add_event_detect(bad_pin, GPIO.RISING, callback=BB)

GPIO.setup(led_pin, GPIO.OUT)
GPIO.setup(switch_pin, GPIO.OUT)
GPIO.setup(buzzer_pin, GPIO.OUT)



GPIO.output(switch_pin, 0)
GPIO.output(led_pin, 0)

message = input("Press enter to quit\n\n")
GPIO.cleanup() # Clean up
