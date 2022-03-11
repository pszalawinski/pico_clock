'''
******************************************************************************
  * @file    Rotation Sensor.py
  * @author  Waveshare Team
  * @version 
  * @date    2021-02-08
  * @brief   Rotation Sensor
  ******************************************************************************
  * @attention
  *
  * THE PRESENT FIRMWARE WHICH IS FOR GUIDANCE ONLY AIMS AT PROVIDING CUSTOMERS
  * WITH CODING INFORMATION REGARDING THEIR PRODUCTS IN ORDER FOR THEM TO SAVE
  * TIME. AS A RESULT, WAVESHARE SHALL NOT BE HELD LIABLE FOR ANY
  * DIRECT, INDIRECT OR CONSEQUENTIAL DAMAGES WITH RESPECT TO ANY CLAIMS ARISING
  * FROM THE CONTENT OF SUCH FIRMWARE AND/OR THE USE MADE BY CUSTOMERS OF THE
  * CODING INFORMATION CONTAINED HEREIN IN CONNECTION WITH THEIR PRODUCTS.
  *
  ******************************************************************************
'''

from machine import Pin,ADC
import utime

#Define pins and their initialization
right = machine.Pin(27, machine.Pin.IN)
left = machine.Pin(26, machine.Pin.IN)
down = machine.Pin(22, machine.Pin.IN)


right_assist = 0
count = 0             #Rotate the value of the encoder


def right_handler(pin):
    global right_assist
    right.irq(handler=None)
    right_assist = 1


def down_handler(pin):
    global count
    down.irq(handler=None)
    count = 0
    print("down",count)
    down.irq(trigger=machine.Pin.IRQ_FALLING, handler=down_handler)


right.irq(trigger=machine.Pin.IRQ_FALLING, handler=right_handler)
down.irq(trigger=machine.Pin.IRQ_FALLING, handler=down_handler)


while True :
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
    
    
    
    
    
    
   
