'''
    2018 code for Team 5549 Gryphon Robotics. Used for Power Up season.
    This contains the necessary code to drive using tank-steering and
    enables the use of attachments (omnom, lift, climb) with basic
    autonomous procedures.
'''

# This robot dispenses the cubes. Compared to him, you are nothing.
import wpilib
from wpilib.drive import DifferentialDrive
from wpilib import DriverStation
from wpilib import CameraServer
from wpilib import ADXRS450_Gyro

'''
Xbox 360 Controller
    Joystick 1 --> drive train control
    Joystick 2 --> attachment control

AXIS MAPPING
    0 - X-Axis (left)   |   4 - X-Axis (right)
    1 - Y-Axis (left)   |   5 - Y-Axis (right)
    2 - Trigger (left)  |
    3 - Trigger (right) |
    
BUTTON MAPPING 
    1 - A   |   5 - Bumper (left)  
    2 - B   |   6 - Bumper (right)  
    3 - X   |   7 - Back            
    4 - Y   |   8 - Start           
'''


class MyRobot(wpilib.IterativeRobot):

    def robotInit(self):
        '''Robot initialization function'''

        # object that handles basic drive operations
        self.frontRightMotor = wpilib.Victor(0)
        self.rearRightMotor = wpilib.Victor(1)
        self.frontLeftMotor = wpilib.Victor(2)
        self.rearLeftMotor = wpilib.Victor(3)

        # object that handles basic intake operations
        self.omnom_left_motor = wpilib.Spark(7)
        self.omnom_right_motor = wpilib.Spark(8)

        # object that handles basic lift operations
        self.liftMotor = wpilib.Spark(4)

        # object that handles basic climb operations
        self.winch1 = wpilib.Spark(5)
        self.winch2 = wpilib.Spark(6)

        # defining motor groups
        self.left = wpilib.SpeedControllerGroup(self.frontLeftMotor, self.rearLeftMotor)
        self.right = wpilib.SpeedControllerGroup(self.frontRightMotor, self.rearRightMotor)

        # setting up drive group for drive motors
        self.drive = DifferentialDrive(self.left, self.right)
        self.drive.setExpiration(0.1)

        # defining omnom motor groups
        self.omnom_left = wpilib.SpeedControllerGroup(self.omnom_left_motor)
        self.omnom_right = wpilib.SpeedControllerGroup(self.omnom_right_motor)

        # setting up omnom group for omnom motors
        self.omnom = DifferentialDrive(self.omnom_left, self.omnom_right)
        self.omnom.setExpiration(0.1)

        # defines timer for autonomous
        self.timer = wpilib.Timer()

        # joystick 1 & 2 on the driver station
        self.stick = wpilib.Joystick(1)
        self.stick2 = wpilib.Joystick(2)

        # initialization of the ultrasonic sensors
        self.AnalogInput_one = wpilib.AnalogInput(2)
        self.AnalogInput_two = wpilib.AnalogInput(3)

        # initialization of the hall-effect sensors
        self.DigitalInput = wpilib.DigitalInput(1)

        # initialization of the FMS
        self.DS = DriverStation.getInstance()
        self.PS = DriverStation.getInstance()

        # initialization of the camera server
        wpilib.CameraServer.launch()

    def autonomousInit(self):
        '''This function is run once each time the robot enters autonomous mode.'''
        # self.gyro.reset()
        self.timer.reset()
        self.timer.start()

    def autonomousPeriodic(self):
        '''This function is called periodically during autonomous.'''

        # gets randomization of field elements
        gameData = self.DS.getGameSpecificMessage()
        # gets location of robot on the field
        position = self.PS.getLocation()
        # position = 4

        # basic autonomous functions

        def stop_motor():
            self.drive.tankDrive(0, 0)

        def straight_speed():
            self.drive.tankDrive(0.75, 0.80)
            self.omnom_left.set(-0.1)
            self.omnom_right.set(0.1)

        def straight_slow_speed():
            self.drive.tankDrive(0.5, 0.55)

        def reverse_speed():
            self.drive.tankDrive(-0.75, -0.75)

        def reverse_slow_speed():
            self.drive.tankDrive(-0.5, -0.5)

        def left_turn_speed():
            self.drive.tankDrive(-0.5, 0.5)
            self.omnom_left.set(-0.1)
            self.omnom_right.set(0.1)

        def right_turn_speed():
            self.drive.tankDrive(0.5, -0.5)
            self.omnom_left.set(-0.1)
            self.omnom_right.set(0.1)

        def lift_activate():
            self.liftMotor.set(0.75)

        def lift_lower():
            self.liftMotor.set(0.1)

        def dispense_cube():
            self.omnom_left.set(0.5)
            self.omnom_right.set(-0.5)

        def HansZeTransmissionBroke():
            self.drive.tankDrive(0, 0)

        ##################################################################################

        # Autonomous functions

        # (Below) Activate during tests
        # position = 4

        def left_switch():
            if self.timer.get() < 1.85:
                straight_speed()
            elif 1.85 < self.timer.get() < 2.6:
                right_turn_speed()
            elif 2.6 < self.timer.get() < 2.7:
                lift_activate()
            elif 2.8 < self.timer.get() < 3.1:
                lift_lower()
            elif 3.1 < self.timer.get() < 3.35:
                self.omnom_left.set(-0.5)
                self.omnom_right.set(0.5)
            elif 4.35 < self.timer.get() < 4.85:
                lift_activate()
            elif 4.85 < self.timer.get() < 5.35:
                straight_slow_speed()
            elif 5.35 < self.timer.get() < 5.85:
                dispense_cube()
            elif 5.85 < self.timer.get() < 6.85:
                lift_lower()
            elif self.timer.get() > 6.85:
                stop_motor()

        def right_switch():
            if self.timer.get() < 1.85:
                straight_speed()
            elif 1.85 < self.timer.get() < 2.6:
                left_turn_speed()
            elif 2.6 < self.timer.get() < 2.7:
                lift_activate()
            elif 2.8 < self.timer.get() < 3.1:
                lift_lower()
            elif 3.1 < self.timer.get() < 3.35:
                self.omnom_left.set(-0.5)
                self.omnom_right.set(0.5)
            elif 4.35 < self.timer.get() < 4.85:
                lift_activate()
            elif 4.85 < self.timer.get() < 5.35:
                straight_slow_speed()
            elif 5.35 < self.timer.get() < 5.85:
                dispense_cube()
            elif 5.85 < self.timer.get() < 6.85:
                lift_lower()
            elif self.timer.get() > 6.85:
                stop_motor()

        def left_scale():
            if self.timer.get() < 2:
                straight_speed()
            elif 2 < self.timer.get() < 3:
                left_turn_speed()
            elif self.timer.get() > 4:
                stop_motor()
            else:
                stop_motor()

        def right_scale():
            if self.timer.get() < 1.0:
                straight_slow_speed()
            elif 1.0 < self.timer.get() < 4.3:
                straight_speed()
            elif 4.3 < self.timer.get() < 5.15:
                left_turn_speed()
            elif 5.15 < self.timer.get() < 5.6:
                reverse_speed()
            elif 5.6 < self.timer.get() < 5.7:
                lift_activate()
            elif 5.8 < self.timer.get() < 6.1:
                lift_lower()
            elif 6.1 < self.timer.get() < 6.35:
                self.omnom_left.set(-0.5)
                self.omnom_right.set(0.5)
            elif 6.35 < self.timer.get() < 7.35:
                lift_activate()
            elif 7.35 < self.timer.get() < 7.85:
                straight_slow_speed()
            elif 7.85 < self.timer.get() < 8.35:
                dispense_cube()
            elif 8.35 < self.timer.get() < 8.85:
                reverse_slow_speed()
            elif 8.85 < self.timer.get() < 9.85:
                lift_lower()
            elif self.timer.get() > 9.85:
                stop_motor()

        def center_straight():
            if self.timer.get() < 0.2:
                lift_activate()
            elif 0.2 < self.timer.get() < 0.5:
                lift_lower()
            elif 0.5 < self.timer.get() < 0.75:
                self.omnom_left.set(-0.5)
                self.omnom_right.set(0.5)
            elif 0.75 < self.timer.get() < 1.5:
                lift_activate()
            elif 1.5 < self.timer.get() < 4.5:
                straight_slow_speed()
            elif 4.5 < self.timer.get() < 4.00:
                dispense_cube()

        def straight():
            if self.timer.get() < 3.5:
                straight_slow_speed()
            elif self.timer.get() > 3.5:
                stop_motor()

        ###############################################

        # L-L-R
        if gameData == "LLR" and position == 1:
            straight()                          # left switch
        elif gameData == "LLR" and position == 2:
            straight()
        elif gameData == "LLR" and position == 3:
            straight()

        # L-R-L
        elif gameData == "LRL" and position == 1:
            straight()                          # left switch
        elif gameData == "LRL" and position == 2:
            straight()
        elif gameData == "LRL" and position == 3:
            straight()

        # R-L-L
        elif gameData == "RLL" and position == 1:
            straight()
        elif gameData == "RLL" and position == 2:
            center_straight()
        elif gameData == "RLL" and position == 3:
            straight()                          # right switch

        # R-L-R
        elif gameData == "RLR" and position == 1:
            straight()
        elif gameData == "RLR" and position == 2:
            center_straight()
        elif gameData == "RLR" and position == 3:
            straight()                          # right switch

        # R-R-R
        elif gameData == "RRR" and position == 1:
            straight()
        elif gameData == "RRR" and position == 2:
            center_straight()
        elif gameData == "RRR" and position == 3:
            straight()                          # right switch

        # L-L-L
        elif gameData == "LLL" and position == 1:
            straight()                          # left switch
        elif gameData == "LLL" and position == 2:
            straight()
        elif gameData == "LLL" and position == 3:
            straight()

        # Other situations
        else:
            straight()

        ''' tests'''
        '''
        if position == 4:
            lift_test()
        '''
    def teleopInit(self):
        '''Executed at the start of teleop mode'''
        self.drive.setSafetyEnabled(True)
		
    def teleopPeriodic(self):
        '''Runs the motors with tank steering'''

		left_toggle = 0
    	right_toggle = 0

    	left_speed = 0.5
    	right_speed = 0.5
    
    	if self.stickLeft.getRawButton(1):
        	if left_toggle == 0:
            	left_speed = 0.25
            	left_toggle = 1
        	elif left_toggle == 1:
            	left_speed = 0.5
            	left_toggle = 0

    	if self.stickRight.getRawButton(1):
        	if right_toggle == 0:
            	right_speed = 0.25
            	right_toggle = 1
        	elif right_toggle == 1:
            	right_speed = 0.5
				right_toggle = 0
		
        # gets value of hall-effect sensor - bool
        is_tall = self.DigitalInput.get()

        # controller mapping for tank steering
        left_stick = self.stick.getRawAxis(1)
        right_stick = self.stick.getRawAxis(5)

        # controller mapping for omnom operation
        left_omnom_stick = self.stick2.getRawAxis(1)/1.15
        right_omnom_stick = self.stick2.getRawAxis(5)/1.15

        # lift controller mapping with relative speed
        if self.stick2.getRawAxis(3):
            self.liftMotor.set(self.stick2.getRawAxis(3))
            #if is_tall == True:
                #self.liftMotor.set(0.3)
        elif self.stick2.getRawAxis(2):
            self.liftMotor.set(-self.stick2.getRawAxis(2))
            #if is_tall == True:
                #self.liftMotor.set(0.3)
        else:
            self.liftMotor.set(0)

        # climb controller mapping with relative speed
        if self.stick2.getRawButton(4):
            self.winch1.set(0.75)
            self.winch2.set(0.75)
        elif self.stick2.getRawButton(1):
            self.winch1.set(-0.75)
            self.winch2.set(-0.75)
        else:
            self.winch1.set(0)
            self.winch2.set(0)

        '''
        if left_stick < 0:
            divisor = 2.3
        else:
            divisor = 2

        adjusted_left_stick = left_stick/divisor
        '''

        self.omnom.tankDrive(left_omnom_stick, right_omnom_stick)     # drives intake system using tank steering

        self.drive.tankDrive(-left_stick, -right_stick)                 # drives drive system using tank steering




if __name__ == '__main__':
    wpilib.run(MyRobot)
