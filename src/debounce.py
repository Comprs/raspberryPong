import rpi.GPIO as GPIO

channel = []

def add_channels(*args):
    global channels
    for arg in args:
        channel.append(arg)
    
def serv_player1(channel):
    print('player1 served')
    
def serv_player2(channel):
    print('player2 served')
    
def powerup_player1(channel):
    print('player1 used a powerup')
    
def powerup_player2(channel):
    print('player2 used a powerup')
    
    
    
def setup():
    for ch in range(len(channel)):
        GPIO.setup(channel[ch], GPIO.IN, pull_up_down=GPIO.PUD_UP)
        GPIO.add_event_detect(channel[ch], GPIO.RISING)
        if ch == 0 or ch == 2:
            GPIO.add_event_callback(channel[ch], if ch == 0: serv_player1 else: serv_player2, bouncetime = 200)
        elif ch == 1:
            GPIO.add_event_callback(channel[ch], powerup_player1, bouncetime = 200) 
        elif ch ==3:
            GPIO.add_event_callback(channel[ch], powerup_player2)


        
    
