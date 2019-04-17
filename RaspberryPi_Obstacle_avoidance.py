
# coding: utf-8

# # IMPORTING LIBRARIES


# GPIO library
import RPi.GPIO as GPIO

# Time library
import time


# # SETTING GPIO PINS


# Set the GPIO modes
GPIO.setmode(GPIO.BCM)
GPIO.setwarnings(False)

# Set GPIO pins for the ultrasonic sensor
pinTrigger = 17         # Signal emitter
pinEcho = 18            # Signal receiver

# Set GPIO pins as output and input for the ultrasonic sensor
GPIO.setup(pinTrigger, GPIO.OUT)
GPIO.setup(pinEcho, GPIO.IN)

# Set the Variables for the GPIO pins for the motors (For the LinuxFriends Robots only two pins are needed.)
# Their robot has only two motors.
pinMotorAForwards = 10
pinMotorABackwards = 9
pinMotorBForwards = 8
pinMotorBBackwards = 7

# Set the GPIO pins mode as output because the motors are actuators 
GPIO.setup(pinMotorAForwards, GPIO.OUT)
GPIO.setup(pinMotorABackwards, GPIO.OUT)
GPIO.setup(pinMotorBForwards, GPIO.OUT)
GPIO.setup(pinMotorBBackwards, GPIO.OUT)




# # SPEED CONTROL WITH PWM SIGNAL


def ForwardsPwm():
    '''This function sets the value of the motors pins to 1. This turns on these motors and the 
        robot moves forward.'''
    
    # Using 75% of the motors speed
    pwm_motor1.ChangeDutyCycle(75) # Left motor
    pwm_motor2.ChangeDutyCycle(75) # Right motor


def LeftPwm():
    '''This function sets the value of the motors pins on the left of the robot to 0 while that
    of the motor on the right is set to 1. This turns off the motor on the left and the right motor is
    turned on, which makes the robot turn left.'''
    
    # Using 50% of the right motor speed and 10% of the left motor speed when turning
    pwm_motor1.ChangeDutyCycle(10)
    pwm_motor2.ChangeDutyCycle(50)

def BackwardsPwm():      # Depends on the board capacity to allow that functionnality.
    
    # Using 20% of the motors speed when moving backward
    pwm_motor1.ChangeDutyCycle(20)
    pwm_motor2.ChangeDutyCycle(20)

def StopMotors():
    '''This function sets the value of the motors pins to 0. This turns off these motors and the 
        robot stops.'''
    
    # Using 0% of the motors speed when moving backward
    pwm_motor1.ChangeDutyCycle(0)
    pwm_motor2.ChangeDutyCycle(0)


def RightPwm():
    '''This function sets the value of the motors pins on the rightt of the robot to 0 while that
    of the motor on the leftt is set to 1. This turns off the motor on the rightt and the leftt motor is
    turned on, which makes the robot turn right.'''
    
    # Using 50% of the left motor speed and 10% of the right motor speed when turning
    pwm_motor1.ChangeDutyCycle(50)
    pwm_motor2.ChangeDutyCycle(10)



def AvoidObstaclePwm():
    '''This function defines a strategy for the robot to avoid obstacles. If the robot faces an obstacle, 
    it will move backward a little bit, stop and then turn right.'''
    
    # Back off a little
    print("Backwards")
    BackwardsPwm()
    time.sleep(1)
    StopMotors()

    # Turn right
    print("Right")
    RightPwm()
    time.sleep(1)
    StopMotors()


def Measure():
    '''This function measures the distance between the robot and the obstacle
       To do so, the time between the emission and the reception of the signal from
       the ultrasonic sensor is computed and mutiplied by the value 34326 divided by 2.'''
    
    # Emission of the signal
    GPIO.output(pinTrigger, True)
    time.sleep(0.00001)           # Measure the distance every 0.01ms
    GPIO.output(pinTrigger, False)
    
    # Initialization of the times
    StartTime = time.time()
    StopTime = StartTime     
    
    # Measure of the time until the signal emitted is received back
    while GPIO.input(pinEcho)==0:
        StartTime = time.time()

    while GPIO.input(pinEcho)==1:
        StopTime = time.time()
        # If the sensor is too close to an object, the Pi cannot
        # see the echo quickly enough, so it has to detect that
        # problem and say what has happened
        if StopTime-StartTime >= 0.04:
            print("Hold on there! You're too close for me to see.")
            StopTime = StartTime
            break

    ElapsedTime = StopTime - StartTime
    Distance = (ElapsedTime * 34326)/2   # 34326 is the sonic speed in cm/s
    return Distance


def IsNearObstacle(localHowNear):
    '''Given a minimal distance as reference, this function measures if the robot is near an obstacle or not'''

    Distance = Measure()

    print("There is an Obstacle "+str(Distance)+" cm ahead")
    if Distance >= localHowNear:       # Safe to move forward
        return True              
    else:
        return False

# ######################################### MAIN PROGRAM ##########################################


# Defining the PWM Frequency
pwm_motor1 = GPIO.PWM(pinMotorAForwards, 500) # Left motor
pwm_motor2 = GPIO.PWM(pinMotorBForwards, 500) # Right motor

# Initializing the duty cycle at 100 (Maximum speed)
pwm_motor1.start(100)
pwm_motor2.start(100)

# Collecting the distance to the closest obstacle
HowNear = Measure()

# Defining the minimal distance between the robot and the nearest obstacle.
limit = 30.0

while True:
    if IsNearObstacle(limit):  # While the robot is free to move forward
        ForwardsPwm()             # Move forward
        time.sleep(0.005)
    else:
        AvoidObstaclePwm()
GPIO.cleanup()
