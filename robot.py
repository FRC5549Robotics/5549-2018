'''
    This is a demo program showing the use of the RobotDrive class,
    specifically it contains the code necessary to operate a robot with
    tank drive and basic autonomous procedures.
'''

import wpilib
from wpilib.drive import DifferentialDrive
from wpilib import DriverStation
from wpilib import adxrs450_gyro

class MyRobot(wpilib.IterativeRobot):

    def robotInit(self):
        '''Robot initialization function'''

        # object that handles basic drive operations
        self.frontRightMotor = wpilib.Victor(0)
        self.rearRightMotor = wpilib.Victor(1)
        self.frontLeftMotor = wpilib.Victor(2)
        self.rearLeftMotor = wpilib.Victor(3)

        # object that handles basic intake operations
        self.omnom = wpilib.Spark(7)    # make sure channels are correct

        # object that handles basic climb operations
        self.liftMotor = wpilib.Spark(4)    # make sure channel is correct

        # defining motor groups
        self.left = wpilib.SpeedControllerGroup(self.frontLeftMotor, self.rearLeftMotor)
        self.right = wpilib.SpeedControllerGroup(self.frontRightMotor, self.rearRightMotor)

        # setting up drive group for drive motors
        self.drive = DifferentialDrive(self.left, self.right)
        self.drive.setExpiration(0.1)

        # defines timer for autonomous
        self.timer = wpilib.Timer()

        # joystick 1 & 2 on the driver station
        self.stick = wpilib.Joystick(0)
        self.stick2 = wpilib.Joystick(1)

        # initialization of the camera server
        wpilib.CameraServer.launch()

        # initialization of the ultrasonic sensors
        self.AnalogInput_one = wpilib.AnalogInput(2)
        self.AnalogInput_two = wpilib.AnalogInput(3)

        # initialization of the hall-effect sensors
        self.DigitalInput = wpilib.DigitalInput(2)

        # initialization of the gyro
        #self.gyro = wpilib.ADXRS450_Gyro()

    def autonomousInit(self):
        '''This function is run once each time the robot enters autonomous mode.'''
        #self.gyro.reset()
        self.timer.reset()
        self.timer.start()


    def autonomousPeriodic(self):
        '''This function is called periodically during autonomous.'''

        # gets distance from ultrasonic sensor - voltage
        distance = self.AnalogInput_one.getVoltage()
        distance1 = self.AnalogInput_two.getVoltage()

        '''
        # Uses voltage to meter to determine the distance to obstacle
        if distance > 0.75:
            self.drive.tankDrive(0.575, 0.5)
        else:
            self.drive.tankDrive(0, 0)

        if distance1 > 0.75:
            self.drive.tankDrive(0.5, 0.5)
        else:
            self.drive.tankDrive(0, 0)
        '''


        # gets randomization of field elements
        gameData = DriverStation.getInstance().getGameSpecificMessage()
        # gets location of robot on the field
        position = DriverStation.getInstance().getLocation()

        # basic autonomous functions

        def stop_motor():
            self.drive.tankDrive(0, 0)

        def straight_speed():
            self.drive.tankDrive(0.5, 0.55)

        def left_turn_speed():
            self.drive.tankDrive(0.5, -0.5)

        def right_turn_speed():
            self.drive.tankDrive(-0.5, 0.5)

        ##################################################################################

        # Autonomous functions

        def left_switch():
            if self.timer.get() < 4.5:
                straight_speed()
            elif 4.5 < self.timer.get() < 5.25:
                left_turn_speed()
            elif self.timer.get() > 5.25:
                stop_motor()
            else:
                stop_motor()

        def right_switch():
            if self.timer.get() < 4.5:
                straight_speed()
            elif 4.5 < self.timer.get() < 5.25:
                right_turn_speed()
            # elif statement activating dropping mechanism after turn completion
            elif self.timer.get() > 5.25:
                stop_motor()
            else:
                stop_motor()

        def left_scale():
            if self.timer.get() < 7.30:
                straight_speed()
            elif 7.30 < self.timer.get() < 8.05:
                left_turn_speed()
            elif self.timer.get() > 8.05:
                stop_motor()
            else:
                stop_motor()

        def right_scale():
            if self.timer.get() < 7.30:
                straight_speed()
            elif 7.30 < self.timer.get() < 8.05:
                right_turn_speed()
            elif self.timer.get() > 8.05:
                stop_motor()
            else:
                stop_motor()

        def straight():
            if self.timer.get() < 5.0:
                straight_speed()
            elif self.timer.get() > 5.0:
                stop_motor()
            else:
                stop_motor()

        def center_straight():
            if self.timer.get() < 5.0:
                straight_speed()
            elif self.timer.get() > 4.0:
                stop_motor()
            else:
                stop_motor()

        ###############################################################

        # L-L-R
        if gameData == "LLR" and position == 1:
            left_switch()
        elif position == 2:
            center_straight()
        elif gameData == "LLR" and position == 3:
            straight()

        # L-R-L
        elif gameData == "LRL" and position == 1:
            left_switch()
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
            right_switch()

        # R-L-R
        elif gameData == "RLR" and position == 1:
            straight()
        elif gameData == "RLR" and position == 2:
            center_straight()
        elif gameData == "RLR" and position == 3:
            right_switch()



    def teleopInit(self):
        '''Executed at the start of teleop mode'''
        self.drive.setSafetyEnabled(True)

    def teleopPeriodic(self):
        '''Runs the motors with tank steering'''

        # gets value of hall-effect sensor - bool
        is_tall = self.DigitalInput.get()

        # controller mapping for tank steering
        left_stick = self.stick.getRawAxis(1)/2   # Slows down motors
        right_stick = self.stick.getRawAxis(5)/2

        # basic intake controller mapping with relative speed
        if self.stick2.getRawButton(5):
            self.omnom.set(-0.5)
        elif self.stick2.getRawButton(6):
            self.omnom.set(0.5)
        else:
            self.omnom.set(0)

        # basic lift controller mapping with relative speed
        def lift_control():
            if self.stick2.getRawAxis(2):
                self.liftMotor.set(self.stick2.getRawAxis(2))
            elif self.stick2.getRawAxis(3):
                self.liftMotor.set(-self.stick2.getRawAxis(3))

        # checks if one of these buttons is pressed
        if self.stick2.getRawAxis(2) or self.stick2.getRawAxis(3) or self.stick2.getRawButton(2):
            lift_control()
        elif self.stick2.getRawButton(1):
            self.liftMotor.set(-0.2)    # Operator loses control and this value takes over. ONLY USE TO HOLD OMNOM.


        '''
        if left_stick < 0:
            divisor = 2.3
        else:
            divisor = 2

        adjusted_left_stick = left_stick/divisor
        '''
        self.drive.tankDrive(-left_stick, -right_stick)



if __name__ == '__main__':
    wpilib.run(MyRobot)