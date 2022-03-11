from machine import Pin,ADC
import utime

#Define pins and their initialization
right = machine.Pin(27, machine.Pin.IN)
left = machine.Pin(26, machine.Pin.IN)
down = machine.Pin(22, machine.Pin.IN)


right_assist = 0
count = 0
clicks = 0

hour = 0
minute = 0
second = 0


def right_handler(pin):
    global right_assist
    right.irq(handler=None)
    right_assist = 1


def down_handler(pin):
    global clicks
    global hour
    global minute
    global second
    print("click", clicks)
    global count
    down.irq(handler=None)
    
    if(clicks==2):
        hour = count
    if(clicks==4):
        minute = count
    if(clicks==6):
        second = count
    
    clicks = clicks + 1
    print("click added", clicks)
    print("time set to " + str(hour) + ":" + str(minute) + ":" + str(second))
    count = 0
    print("down",count)
    down.irq(trigger=machine.Pin.IRQ_FALLING, handler=down_handler)


right.irq(trigger=machine.Pin.IRQ_FALLING, handler=right_handler)
down.irq(trigger=machine.Pin.IRQ_FALLING, handler=down_handler)


if(clicks==5):
    print("clock set to" + + str(hour) + ":" + str(minute) + ":" + str(second))


while clicks < 6 :
    if (right_assist == 1 ):
        
        if (left.value() == 1 ):
            count = count - 1
            print("left",  count)

        elif (left.value() == 0 ):
            count = count + 1
            print("right",  count)
            
        while (left.value() == 0 ) | (right.value() == 0):
            utime.sleep_ms(1)
            
        right_assist = 0
        right.irq(trigger=machine.Pin.IRQ_FALLING, handler=right_handler)
    
    
    
    
    
    
   

