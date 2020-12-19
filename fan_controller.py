import os
from time import sleep
import RPi.GPIO as GPIO

FAN_CONTROL_PIN = 14    # GPIO14
THRESHOLD = 60          # 60°C
FAN_STATUS = True       # True = Active

def setup() -> None:
    GPIO.setmode(GPIO.BCM)
    GPIO.setup(FAN_CONTROL_PIN, GPIO.OUT)
    GPIO.setwarnings(False)


def set_status(new_status: bool = True):
    global FAN_STATUS
    
    GPIO.output(FAN_CONTROL_PIN, new_status)
    FAN_STATUS = new_status


def activate_fan() -> None:
    set_status(True) 


def deactivate_fan() -> None:
    set_status(False) 


def evalute_temperature(cpu_temp: float, hysteresis: float = 10.0) -> None:
    # If the CPU temperature is higher than the threshold we need to activate the fan
    if cpu_temp >= THRESHOLD:
        activate_fan()
    
    # We shutdown the fan only with a margin on the threshold
    elif cpu_temp < (THRESHOLD - hysteresis):
        deactivate_fan()
    
    else:
        return


def read_temperature() -> float: 
    raw_temp: str = os.popen('cat /sys/class/thermal/thermal_zone0/temp').readline()
    temp_in_celsius: float  = int(raw_temp)/1000
    return temp_in_celsius


def main() -> None:
    setup()
    while True:
        temperature: int = read_temperature()

        evalute_temperature(cpu_temp=temperature)

        sleep(30)


if __name__ == '__main__':
    try:
        main()
    except KeyboardInterrupt:
        GPIO.cleanup() 
