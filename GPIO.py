"""1- sudo apt update
2- sudo apt install python3-libgpiod
3- sudo apt install libretech-gpio libretech-dtoverlay
sudo pip3 uninstall gpiod #remove it if you have it
lgpio info PIN#
sudo apt show python3-libgpiod
sudo lgpio set 8=1
sudo lgpio set 8=0"""

import gpiod
import time
import sys 

chipzero = gpiod.Chip('0')
chipone = gpiod.Chip('1')
chiptwo = gpiod.Chip('2')
chipthree = gpiod.Chip('3') 

# Define Pins
one = "3.3v supply"
two = "5v supply"
three = chiptwo.get_lines([25])
four = "5v supply"
five = chiptwo.get_lines([24]) 
six = "Ground"
seven = chipone.get_lines([28])
eight = chipthree.get_lines([4])
nine = "Ground"
ten = chipthree.get_lines([6])
eleven = chiptwo.get_lines([20])
twelve = chiptwo.get_lines([6])
thirteen = chiptwo.get_lines([21])
fourteen = "Ground"
fifteen = chiptwo.get_lines([22]) 
sixteen = chipthree.get_lines([7])
seventeen = "Ground"
eighteen = chipthree.get_lines([5])
nineteen = chipthree.get_lines([1])
twenty = "Ground"
twentyone = chipthree.get_lines([2])
twentytwo = chipzero.get_lines([2])
twentythree = chipthree.get_lines([0]) 
twentyfour = chipthree.get_lines([8])
twentyfive = "Ground"
twentysix = chiptwo.get_lines([12])
twentyseven = "Do Not Use"
twentyeight = "Do Not Use"
twentynine = chiptwo.get_lines([19])
thirty = "Ground"
thirtyone = chiptwo.get_lines([23])
thirtytwo = chipzero.get_lines([0])
thirtythree = chiptwo.get_lines([16])
thirtyfour = "Ground"
thirtyfive = chiptwo.get_lines([18])
thirtysix = chiptwo.get_lines([0])
thirtyseven = chiptwo.get_lines([15])
thirtyeight = chiptwo.get_lines([1])
thirtynine = "Ground"
fourty = chipzero.get_lines([27])

#Set output pins
five.request(consumer=sys.argv[0], type=gpiod.LINE_REQ_DIR_OUT)
seven.request(consumer=sys.argv[0], type=gpiod.LINE_REQ_DIR_OUT)
eleven.request(consumer=sys.argv[0], type=gpiod.LINE_REQ_DIR_OUT)
thirteen.request(consumer=sys.argv[0], type=gpiod.LINE_REQ_DIR_OUT)
fifteen.request(consumer=sys.argv[0], type=gpiod.LINE_REQ_DIR_OUT)
nineteen.request(consumer=sys.argv[0], type=gpiod.LINE_REQ_DIR_OUT)
twentyone.request(consumer=sys.argv[0], type=gpiod.LINE_REQ_DIR_OUT)
twentynine.request(consumer=sys.argv[0], type=gpiod.LINE_REQ_DIR_OUT)
thirtyone.request(consumer=sys.argv[0], type=gpiod.LINE_REQ_DIR_OUT)
thirtythree.request(consumer=sys.argv[0], type=gpiod.LINE_REQ_DIR_OUT)

#Set input pins 
three.request(consumer=sys.argv[0], type=gpiod.LINE_REQ_DIR_IN)
thirtyfive.request(consumer=sys.argv[0], type=gpiod.LINE_REQ_DIR_IN)
thirtyseven.request(consumer=sys.argv[0], type=gpiod.LINE_REQ_DIR_IN)

#Break statement for E-Stop

def homeZ():
    ishomeZ = 0
    nineteen.set_values([1])
    delaytime = 60 / (100000 * 200)
    twentynine.set_values([1])
    thirtyone.set_values([1])
    thirtythree.set_values([1])
    
    # Initialize counter for consecutive [1] values
    consecutive_ones_count = 0

    # Turn until five consecutive [1] values are detected
    while consecutive_ones_count < 10:
        # Check if the current value is [1]
        if thirtyseven.get_values() == [0]:
            consecutive_ones_count += 1
        else:
            # Reset the counter if the value is not [1]
            consecutive_ones_count = 0
        
        # Move the motor
        twentyone.set_values([1])
        time.sleep(.000001)
        twentyone.set_values([0])
        time.sleep(delaytime)

    # Back off by a quarter rotation to protect the limit switch from over-actuation
    nineteen.set_values([0])
    delaytime = 60 / (200 * 50)
    for n in range(6400):
        twentyone.set_values([1])
        time.sleep(.000001)
        twentyone.set_values([0])
        time.sleep(.0001)
    # The motor is zeroed at this point


# Here is a function to home the horizontal motor
def homeX():
    five.set_values([1])
    delaytime = 60 / (200 * 200)
    eleven.set_values([1])
    thirteen.set_values([1])
    fifteen.set_values([1])
    
    # Initialize counter for consecutive [1] values
    consecutive_ones_count = 0

    # Turn until five consecutive [1] values are detected
    while consecutive_ones_count < 5:
        # Check if the current value is [1]
        print(consecutive_ones_count)
        if thirtyfive.get_values() == [0]:
            consecutive_ones_count += 1
        else:
            # Reset the counter if the value is not [1]
            consecutive_ones_count = 0
        
        # Move the motor
        seven.set_values([1])
        time.sleep(.000001)
        seven.set_values([0])
        time.sleep(.0005)
   
    # Back off by a quarter rotation to protect the limit switch from over-actuation
    five.set_values([0])
    delaytime = 60 / (200 * 50)
    for n in range(200):
        seven.set_values([1])
        time.sleep(.000001)
        seven.set_values([0])
        time.sleep(delaytime)
    # The motor is zeroed at this point


# Lets test moving one of the motors 
# the vertical motor is controlled by the folowing DIR-5 Step-7 MS3-11 MS2-13 MS1=15
# We will make this a functions so that we can make controling motors easier in the future 
def moveIt (motor, direction, steps, speed=100, microstep="sixteenth"):
    delaytime=60/(speed*200)
    steps=int(steps)
    if motor == 1 :
            if direction == "R":
                  five.set_values([1])
            if direction == "L":
                  five.set_values([0])

            if microstep == "full":
                
                 fifteen.set_values([0])

            elif microstep == "half":
                  
                  fifteen.set_values([1])

            elif microstep == "quarter":
                  eleven.set_values([0])
                  thirteen.set_values([1])
                  fifteen.set_values([0])

            elif microstep == "eighth":
                  
                  fifteen.set_values([1])

            elif microstep == "sixteenth":
                  
                  fifteen.set_values([1])
                  
            for x in range (steps):
                seven.set_values([1])
                time.sleep(.000001)
                seven.set_values([0])
                time.sleep(delaytime)

    if motor == 2 :
            if direction == "U":
                  nineteen.set_values([1])
            if direction == "D":
                  nineteen.set_values([0])

            if microstep == "full":
                 twentynine.set_values([0])
                 thirtyone.set_values([0])
                 thirtythree.set_values([0])

            elif microstep == "half":
                 twentynine.set_values([0])
                 thirtyone.set_values([0])
                 thirtythree.set_values([1])

            elif microstep == "quarter":
                 twentynine.set_values([0])
                 thirtyone.set_values([1])
                 thirtythree.set_values([0])

            elif microstep == "eighth":
                 twentynine.set_values([0])
                 thirtyone.set_values([1])
                 thirtythree.set_values([1])

            elif microstep == "sixteenth":
                 twentynine.set_values([1])
                 thirtyone.set_values([1])
                 thirtythree.set_values([1])

            for n in range (steps):
                twentyone.set_values([1])
                time.sleep(.000001)
                twentyone.set_values([0])
                time.sleep(delaytime)
        

"""
moveIt(1,"L",16000,600,"sixteenth")
moveIt(2,"D",60000,10000,"sixteenth")
moveIt(2,"U",60000,10000,"sixteenth")
moveIt(1,"L",5000,600,"sixteenth")
moveIt(2,"D",60000,10000,"sixteenth")
moveIt(2,"U",60000,10000,"sixteenth")
moveIt(1,"R",21000,600,"sixteenth")
"""

#moveIt(1,"R",10000,500,"sixteenth")
#moveIt(1,"",10000,500,"sixteenth")
homeZ()
homeX()
