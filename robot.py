'''
    This is a demo program showing the use of the RobotDrive class,
    specifically it contains the code necessary to operate a robot with
    tank drive and basic autonomous procedures.
'''

import wpilib
from wpilib.drive import DifferentialDrive
from wpilib import DriverStation

class MyRobot(wpilib.IterativeRobot):

    def robotInit(self):
        '''Robot initialization function'''

        # object that handles basic drive operations
        self.frontRightMotor = wpilib.Victor(0)
        self.rearRightMotor = wpilib.Victor(1)
        self.frontLeftMotor = wpilib.Victor(2)
        self.rearLeftMotor = wpilib.Victor(3)

        # object that handles basic intake operations
        self.omnomLeft = wpilib.Spark(7)
        self.omnomRight = wpilib.Spark(8)

        # defining motor groups
        self.left = wpilib.SpeedControllerGroup(self.frontLeftMotor, self.rearLeftMotor)
        self.right = wpilib.SpeedControllerGroup(self.frontRightMotor, self.rearRightMotor)

        # defining intake/output motor groups
        self.omnom = wpilib.SpeedControllerGroup(self.omnomLeft, self.omnomRight)

        # setting up drive group for drive motors
        self.drive = DifferentialDrive(self.left, self.right)
        self.drive.setExpiration(0.1)

        # setting up drive group for intake motors
        self.omnomop = DifferentialDrive(self.omnom)
        self.omnom.setExpiration(0.1)

        # defines timer for autonomous
        self.timer = wpilib.Timer()

        # joystick 1 on the driver station
        self.stick = wpilib.Joystick(1)

        # Initialization of the camera server
        wpilib.CameraServer.launch()

        # Initialization of the ultrasonic sensor
        self.AnalogInput = wpilib.AnalogInput(2)


    def autonomousInit(self):
        '''This function is run once each time the robot enters autonomous mode.'''
        self.timer.reset()
        self.timer.start()


    def autonomousPeriodic(self):
        '''This function is called periodically during autonomous.'''

        # Gets distance in the form of voltage from ultrasonic sensor
        distance = self.AnalogInput.getVoltage()

        # Uses voltage to meter to determine the distance to obstacle
        if distance > 0.75:
            self.drive.tankDrive(0.55, 0.5)
        else:
            self.drive.tankDrive(0, 0)

        gameData = DriverStation.getInstance().getGameSpecificMessage() #Gets color of switches and scale in string form
        position = 3    # Change position based on need

        def l():
            if self.timer.get() < 3.0:
                self.drive.tankDrive(0.55, 0.5)  # Drive forwards for 5 seconds at half speed.
            elif 3.0 < self.timer.get() < 4.0:
                self.drive.tankDrive(0, 0.5)  # Turn left for 1 second at half speed.
            elif self.timer.get() > 4.0:
                self.drive.tankDrive(0, 0)  # Stop after 6 seconds.
            else:
                self.drive.tankDrive(0, 0)

        def r():
            if self.timer.get() < 5.0:
                self.drive.tankDrive(0.55, 0.5)  # Drive forwards for 5 seconds at half speed.
            elif 5.0 < self.timer.get() < 6.0:
                self.drive.tankDrive(0.5, 0)  # Turn right for 1 second at half speed.
            elif self.timer.get() > 6.0:
                self.drive.tankDrive(0, 0)  # Stop after 6 seconds.
            else:
                self.drive.tankDrive(0, 0)

        def s():
            if self.timer.get() < 5.0:
                self.drive.tankDrive(0.5, 0.5)  # Drive forwards for 5 seconds at half speed.
            elif self.timer.get() > 5.0:
                self.drive.tankDrive(0, 0)  # Stop after 6 seconds.
            else:
                self.drive.tankDrive(0, 0)

        def cs():
            if self.timer.get() < 4.0:
                self.drive.tankDrive(0.5, 0.5)  # Drive forwards for 5 seconds at half speed.
            elif self.timer.get() > 4.0:
                self.drive.tankDrive(0, 0)  # Stop after 6 seconds.
            else:
                self.drive.tankDrive(0, 0)

        if gameData == "LLR" and position == 1:
            l()
        elif gameData == "LLR" and position == 2:
            cs()
        elif gameData == "LLR" and position == 3:
            s()
        elif gameData == "LRL" and position == 1:
            l()
        elif gameData == "LRL" and position == 2:
            cs()
        elif gameData == "LRL" and position == 3:
            s()
        elif gameData == "RLL" and position == 1:
            s()
        elif gameData == "RLL" and position == 2:
            cs()
        elif gameData == "RLL" and position == 3:
            r()
        elif gameData == "RLR" and position == 1:
            s()
        elif gameData == "RLR" and position == 2:
            cs()
        elif gameData == "RLR" and position == 3:
            r()
        else:
            cs()


    def teleopInit(self):
        '''Executed at the start of teleop mode'''
        self.drive.setSafetyEnabled(True)

    def teleopPeriodic(self):
        '''Runs the motors with tank steering'''
        left_stick = self.stick.getRawAxis(1)/2   # Slows down motors
        right_stick = self.stick.getRawAxis(5)/2

        left_trigger = self.stick.getRawButton(2)
        right_trigger = self.stick.getRawButton(3)
        '''
        if right_stick < 0:
            divisor = 2
        else:
            divisor = 2.1

        adjusted_right_stick = right_stick/divisor
        '''
        self.drive.tankDrive(-left_stick, -right_stick)
        self.omnomop.arcadeDrive(-left_trigger, right_trigger)


if __name__ == '__main__':
    wpilib.run(MyRobot)