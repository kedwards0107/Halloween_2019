import gspread
from oauth2client.service_account import ServiceAccountCredentials
import time
import datetime
import RPi.GPIO as GPIO

# GPIO setup
def setup_gpio(pin, in_out, state=GPIO.HIGH, pull_up_down=None):
    GPIO.setmode(GPIO.BCM)
    if pull_up_down:
        GPIO.setup(pin, in_out, pull_up_down=pull_up_down)
    else:
        GPIO.setup(pin, in_out)
    GPIO.output(pin, state)

# Initialize GPIO pins
setup_gpio(17, GPIO.IN, pull_up_down=GPIO.PUD_UP)
setup_gpio(22, GPIO.OUT)

# Google Sheets setup
scope = ["https://spreadsheets.google.com/feeds", "https://www.googleapis.com/auth/spreadsheets",
         "https://www.googleapis.com/auth/drive.file", "https://www.googleapis.com/auth/drive"]
creds = ServiceAccountCredentials.from_json_keyfile_name("creds.json", scope) #creds.json not saved on github for security
client = gspread.authorize(creds)
sheet = client.open("Halloween").sheet1

# Blinking function
def blink(pin, sleep_time, cleanup=False):
    for _ in range(6):
        GPIO.output(pin, GPIO.LOW)
        time.sleep(sleep_time)
        GPIO.output(pin, GPIO.HIGH)
        time.sleep(sleep_time)
    if cleanup:
        GPIO.cleanup()

# Main loop
try:
    while True:
        now_format = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")

        for button_pin, led_pin, candy_name in [(17, 22, "sour patch kids"), 
                                                (18, 5, "nerds"),
                                                (19, 6, "reeses pieces"),
                                                (20, 13, "twix")]:
            setup_gpio(button_pin, GPIO.IN, pull_up_down=GPIO.PUD_UP)
            setup_gpio(led_pin, GPIO.OUT)
            if GPIO.input(button_pin) == False:
                insertRow = [now_format, candy_name] + [int(name == candy_name) for name in ["sour patch kids", "nerds", "reeses pieces", "twix"]]
                sheet.insert_row(insertRow, 2)
                blink(led_pin, SleepTimeL, cleanup=True)

except KeyboardInterrupt:
    GPIO.cleanup()
    print("Done")
