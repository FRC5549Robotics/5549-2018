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
Logitech Joysticks
    Joystick 0 --> left motors(red label)
    Joystick 3 --> right motors(green label)
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
        self.omnom_left_motor = wpilib.Spark(7)  # make sure channels are correct
        self.omnom_right_motor = wpilib.Spark(8)

        # object that handles basic lift operations
        self.liftMotor = wpilib.Spark(4)  # make sure channel is correct

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

        # joystick 0 & on the driver station
        self.leftStick = wpilib.Joystick(0)
        self.rightStick = wpilib.Joystick(1)
        self.stick = wpilib.Joystick(2)

        # initialization of the hall-effect sensors
        self.DigitalInput = wpilib.DigitalInput(1)

        # initialization of the FMS
        self.DS = DriverStation.getInstance()
        self.PS = DriverStation.getInstance()

        # initialization of the camera server
        wpilib.CameraServer.launch()

    def autonomousInit(self):
        '''This function is run once each time the robot enters autonomous mode.'''
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
            elif 4.35 < self.timer.get() < 5.0:
                lift_activate()
            elif 6.35 < self.timer.get() < 6.85:
                dispense_cube()
            elif 6.85 < self.timer.get() < 7.85:
                lift_lower()
            elif self.timer.get() > 7.85:
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
            elif 4.35 < self.timer.get() < 5.0:
                lift_activate()
            elif 6.35 < self.timer.get() < 6.85:
                dispense_cube()
            elif 6.85 < self.timer.get() < 7.85:
                lift_lower()
            elif self.timer.get() > 7.85:
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
            if self.timer.get() < 3.0:
                straight_slow_speed()
            elif self.timer.get() > 3.0:
                stop_motor()

        def straight():
            if self.timer.get() < 3.5:
                straight_slow_speed()
            elif self.timer.get() > 3.5:
                stop_motor()

        ###############################################

        # L-L-R
        if gameData == "LLR" and position == 1:
            straight()  # left switch
        elif gameData == "LLR" and position == 2:
            center_straight()
        elif gameData == "LLR" and position == 3:
            straight()

        # L-R-L
        elif gameData == "LRL" and position == 1:
            straight()  # left switch
        elif gameData == "LRL" and position == 2:
            center_straight()
        elif gameData == "LRL" and position == 3:
            straight()

        # R-L-L
        elif gameData == "RLL" and position == 1:
            straight()
        elif gameData == "RLL" and position == 2:
            center_straight()
        elif gameData == "RLL" and position == 3:
            straight()  # right switch

        # R-L-R
        elif gameData == "RLR" and position == 1:
            straight()
        elif gameData == "RLR" and position == 2:
            center_straight()
        elif gameData == "RLR" and position == 3:
            straight()  # right switch

        # R-R-R
        elif gameData == "RRR" and position == 1:
            straight()
        elif gameData == "RRR" and position == 2:
            center_straight()
        elif gameData == "RRR" and position == 3:
            straight()  # right switch

        # L-L-L
        elif gameData == "LLL" and position == 1:
            straight()  # left switch
        elif gameData == "LLL" and position == 2:
            center_straight()
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

        # toggles for speed control
        self.toggle = 0

        # divisors that divide robot speed
        self.divisor = 2.0

        # the previous state of the joystick button
        self.buttonWasHeld = False

    def teleopPeriodic(self):
        '''Runs the motors with tank steering'''

        # gets value of hall-effect sensor - bool
        is_tall = self.DigitalInput.get()

        # controller mapping for tank steering
        leftAxis = self.leftStick.getRawAxis(1)
        rightAxis = self.rightStick.getRawAxis(1)

        if self.leftStick.getRawButton(1) and self.buttonWasHeld == False:
            self.buttonWasHeld = True
            if self.toggle == 0:
                self.divisor = 1.25
                self.toggle = 1
                self.buttonWasHeld = False
            elif self.toggle == 1:
                self.divisor = 2.0
                self.toggle = 0
                self.buttonWasHeld = False

        # controller mapping for omnom operation
        left_omnom_stick = self.stick.getRawAxis(1) / 1.25
        right_omnom_stick = self.stick.getRawAxis(5) / 1.25

        # lift controller mapping with relative speed
        if self.stick.getRawAxis(3):
            self.liftMotor.set(self.stick.getRawAxis(3))
        elif self.stick.getRawAxis(2):
            self.liftMotor.set(-self.stick.getRawAxis(2))
        else:
            self.liftMotor.set(0)

        # climb controller mapping with relative speed
        if self.stick.getRawButton(4):
            self.winch1.set(0.75)
            self.winch2.set(0.75)
        elif self.stick.getRawButton(1):
            self.winch1.set(-0.75)
            self.winch2.set(-0.75)
        else:
            self.winch1.set(0)
            self.winch2.set(0)

        # drives intake system using tank steering
        self.omnom.tankDrive(-left_omnom_stick, -right_omnom_stick)

        # drives drive system using tank steering
        self.drive.tankDrive(-leftAxis / self.divisor, -rightAxis / self.divisor)


if __name__ == '__main__':
    wpilib.run(MyRobot)