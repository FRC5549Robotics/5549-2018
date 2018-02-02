'''
    This is a demo program showing the use of the RobotDrive class,
    specifically it contains the code necessary to operate a robot with
    tank drive.
'''

import wpilib
from wpilib.drive import DifferentialDrive
from wpilib.doublesolenoid import DoubleSolenoid


class MyRobot(wpilib.IterativeRobot):

    def robotInit(self):
        '''Robot initialization function'''

        # object that handles basic drive operations
        self.frontLeftMotor = wpilib.Talon(1)
        self.rearLeftMotor = wpilib.Talon(2)
        self.frontRightMotor = wpilib.Talon(3)
        self.rearRightMotor = wpilib.Talon(4)

        self.left = wpilib.SpeedControllerGroup(self.frontLeftMotor, self.rearLeftMotor)
        self.right = wpilib.SpeedControllerGroup(self.frontRightMotor, self.rearRightMotor)

        self.drive = DifferentialDrive(self.left, self.right)
        self.drive.setExpiration(0.1)
        self.timer = wpilib.Timer()

        # joystick 1 on the driver station
        self.stick = wpilib.Joystick(1)

        # Initialization of the pneumatic system
        self.Compressor = wpilib.Compressor(0)
        self.Compressor.setClosedLoopControl(True)
        self.enabled = self.Compressor.enabled()
        self.PSV = self.Compressor.getPressureSwitchValue()
        self.DS = wpilib.DoubleSolenoid(0, 1)
        self.Compressor.start()

        # Initialization of the camera server
        wpilib.CameraServer.launch()

    def autonomousInit(self):
        """This function is run once each time the robot enters autonomous mode."""
        self.timer.stop()
        self.timer.start()

    def autonomousPeriodic(self):
        """This function is called periodically during autonomous."""
        if self.timer < 4.0:
            self.drive.tankDrive(0.5, 0.5)
        else:
            self.drive.tankDrive(0, 0)

    def teleopInit(self):
        '''Executed at the start of teleop mode'''
        self.drive.setSafetyEnabled(True)

    def teleopPeriodic(self):
        '''Runs the motors with tank steering'''
        left_stick = self.stick.getRawAxis(1)/1.5
        right_stick = self.stick.getRawAxis(5)/1.5
        '''if right_stick < 0:
            divisor = 2
        else:
            divisor = 2.3'''

        #adjusted_right_stick = right_stick/divisor

        self.drive.tankDrive(-left_stick, -right_stick)

        # Basic pneumatic operations using joystick
        if self.stick.getRawButton(5):
            self.DS.set(DoubleSolenoid.Value.kForward)
        elif self.stick.getRawButton(6):
            self.DS.set(DoubleSolenoid.Value.kReverse)
        elif self.stick.getRawButton(1):
            self.Compressor.stop()
        elif self.stick.getRawButton(4):
            self.Compressor.start()


if __name__ == '__main__':
    wpilib.run(MyRobot)
