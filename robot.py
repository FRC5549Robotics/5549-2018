'''
    This is a demo program showing the use of the RobotDrive class,
    specifically it contains the code necessary to operate a robot with
    tank drive.
'''

import wpilib
from wpilib.drive import DifferentialDrive


class MyRobot(wpilib.IterativeRobot):

    def robotInit(self):
        '''Robot initialization function'''

        # object that handles basic drive operations
        self.frontLeftMotor = wpilib.Victor(0)
        self.rearLeftMotor = wpilib.Victor(1)
        self.frontRightMotor = wpilib.Victor(2)
        self.rearRightMotor = wpilib.Victor(3)

        self.left = wpilib.SpeedControllerGroup(self.frontLeftMotor, self.rearLeftMotor)
        self.right = wpilib.SpeedControllerGroup(self.frontRightMotor, self.rearRightMotor)

        self.myRobot = DifferentialDrive(self.left, self.right)
        self.myRobot.setExpiration(0.1)

        # joysticks 1 on the driver station
        self.stick = wpilib.Joystick(1)

    def teleopInit(self):
        '''Executed at the start of teleop mode'''
        self.myRobot.setSafetyEnabled(True)

    def teleopPeriodic(self):
        '''Runs the motors with tank steering'''
        self.myRobot.tankDrive(self.stick.getY(2) * -1, self.stick.getY(5) * -1)

if __name__ == '__main__':
    wpilib.run(MyRobot)