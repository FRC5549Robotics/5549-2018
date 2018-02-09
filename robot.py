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
        self.frontLeftMotor = wpilib.Victor(1)
        self.rearLeftMotor = wpilib.Victor(2)
        self.frontRightMotor = wpilib.Victor(3)
        self.rearRightMotor = wpilib.Victor(4)

        self.left = wpilib.SpeedControllerGroup(self.frontLeftMotor, self.rearLeftMotor)
        self.right = wpilib.SpeedControllerGroup(self.frontRightMotor, self.rearRightMotor)

        self.drive = DifferentialDrive(self.left, self.right)
        self.drive.setExpiration(0.1)
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

        # Gets distance in the form of voltage from ultrasonic sensor.
        distance = self.AnalogInput.getVoltage()

        # Uses voltage to meter to determine the distance to obstacle
        if distance > 0.75:
            self.drive.tankDrive(0.55, 0.5)
        else:
            self.drive.tankDrive(0, 0)

        gameData = DriverStation.getGameSpecificMessage()
        position = DriverStation.getLocation()

        def l():
            if self.timer.get() < 5.0:
                self.drive.tankDrive(0.5, 0.5)  # Drive forwards for 5 seconds at half speed.
            elif 5.0 < self.timer.get() < 6.0:
                self.drive.tankDrive(0, 0.5)  # Turn right for 1 second at half speed.
            elif self.timer.get() > 6.0:
                self.drive.tankDrive(0, 0)  # Stop after 6 seconds.
            else:
                self.drive.tankDrive(0, 0)

        def r():
            if self.timer.get() < 5.0:
                self.drive.tankDrive(0.5, 0.5)  # Drive forwards for 5 seconds at half speed.
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
        left_stick = self.stick.getRawAxis(1)/1.5   # Slows down motors
        right_stick = self.stick.getRawAxis(5)/1.5
        '''if right_stick < 0:
            divisor = 2
        else:
            divisor = 2.3'''

        #adjusted_right_stick = right_stick/divisor

        self.drive.tankDrive(-left_stick, -right_stick)



if __name__ == '__main__':
    wpilib.run(MyRobot)