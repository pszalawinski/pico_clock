from machine import Pin, SoftSPI, ADC
import ssd1306
import time
import utime

button = Pin(16, Pin.IN, Pin.PULL_DOWN)

rtc = machine.RTC()
spi = SoftSPI(baudrate=500000, polarity=1, phase=0, sck=Pin(14), mosi=Pin(13), miso=Pin(12))

dc = Pin(4)   # data/command
rst = Pin(5)  # reset
cs = Pin(15)  # chip select, some modules do not have a pin for this

display = ssd1306.SSD1306_SPI(128, 64, spi, dc, rst, cs)


display.fill(0)


# print(timer)



#Define pins and their initialization
right = machine.Pin(27, machine.Pin.IN)
left = machine.Pin(26, machine.Pin.IN)
down = machine.Pin(22, machine.Pin.IN)


right_assist = 0
count = 0
clicks = 0

godzina = 0
minuta = 0
sekunda = 0


def right_handler(pin):
    global right_assist
    right.irq(handler=None)
    right_assist = 1


def down_handler(pin):
    global clicks
    global godzina
    global minuta
    global sekunda
    print("click", clicks)
    global count
    down.irq(handler=None)
    
    if(clicks==2):
        godzina = count
    if(clicks==4):
        minuta = count
    if(clicks==6):
        sekunda = count
    
    clicks = clicks + 1
    print("click added", clicks)
    print("time set to " + str(godzina) + ":" + str(minuta) + ":" + str(sekunda))
    count = 0
    print("down",count)
    down.irq(trigger=machine.Pin.IRQ_FALLING, handler=down_handler)


right.irq(trigger=machine.Pin.IRQ_FALLING, handler=right_handler)
down.irq(trigger=machine.Pin.IRQ_FALLING, handler=down_handler)


while clicks < 8 :
    if (right_assist == 1 ):
        
        if (left.value() == 1 ):
            count = count - 1
            display.fill(0)
            display.text("left "+ str(count),37,30,1)
    
            display.show()
            print("left",  count)

        elif (left.value() == 0 ):
            count = count + 1
            display.fill(0)
            display.text("right "+ str(count),37,30,1)
    
            display.show()
            print("right",  count)
            
        while (left.value() == 0 ) | (right.value() == 0):
            utime.sleep_ms(1)
            
        display.text("time " + str(godzina) + ":" + str(minuta) + ":" + str(sekunda),1,1,2)
        display.show()
        rtc.datetime((2022, 3, 10, 0, godzina, minuta, sekunda, 0))
            
        right_assist = 0
        right.irq(trigger=machine.Pin.IRQ_FALLING, handler=right_handler)





        
while True:
    display.fill(0)
    
    

    
    hour = str(godzina)
    minute = str(minuta)
    second = str(sekunda)
    
    
    timer = rtc.datetime()
    
    thour = str(timer[4])
    tminute = str(timer[5])
    tsecond = str(timer[6])
    
    timenow = thour+"."+tminute+"."+tsecond
    
    day = str(timer[2])
    month = str(timer[1])
    year = str(timer[0])
    datenow = day+":"+month+":"+year
    
    
    display.text(datenow,0,0,1)
    display.text(timenow,37,30,1)
    display.show()
    time.sleep_ms(20000)
    count = 0
    clicks = 0
    print(count, "count and clicks ", clicks)
    display.poweroff()
    time.sleep_ms(1000)
    display.poweron()
    

