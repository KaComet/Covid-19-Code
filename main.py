import RPi.GPIO as GPIO # Import Raspberry Pi GPIO library

led_pin = 22
buzzer_pin = 18
switch_pin = 12
bad_pin = 15
good_in = 13
switch_state = False;

def bad_button_callback(channel):
    time.sleep(0.05)
    print("Bad button was pushed!")
            
    BUZZER_REPETITIONS = 1
    BUZZER_DELAY = 0.001
    PAUSE_TIME = 1
        
    for _ in xrange(BUZZER_REPETITIONS):
        for value in [True, False]:
            GPIO.output(buzzer_pin, value)
            time.sleep(BUZZER_DELAY)
        time.sleep(PAUSE_TIME)
        
    GPIO.output(switch_pin, 0)
    GPIO.output(led_pin, 0)
    switch_state = False

def good_button_callback(channel):
    time.sleep(0.05)
    print("Good button was pushed!")
            
    BUZZER_REPETITIONS = 1
    BUZZER_DELAY = 0.001
    PAUSE_TIME = 1
        
    for _ in xrange(BUZZER_REPETITIONS):
        for value in [True, False]:
            GPIO.output(buzzer_pin, value)
            time.sleep(BUZZER_DELAY)
        time.sleep(PAUSE_TIME)
    if (switch_state == true):
        GPIO.output(switch_pin, 0)
        GPIO.output(led_pin, 0)
        switch_state = False
    else:
        GPIO.output(switch_pin, 1)
        GPIO.output(led_pin, 1)
        switch_state = True
    
    
GPIO.setwarnings(False) # Ignore warning for now
GPIO.setmode(GPIO.BOARD) # Use physical pin numbering
GPIO.setup(bad_pin, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)
GPIO.setup(good_in, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)
GPIO.setup(led_pin, GPIO.OUT)
GPIO.setup(switch_pin, GPIO.OUT)

GPIO.output(switch_pin, 0)
GPIO.output(led_pin, 0)

GPIO.add_event_detect(bad_pin,GPIO.RISING,callback=bad_button_callback)
GPIO.add_event_detect(good_in,GPIO.RISING,callback=good_button_callback)
message = input("Press enter to quit\n\n")
GPIO.cleanup() # Clean up
