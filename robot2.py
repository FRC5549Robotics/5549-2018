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
        self.frontLeftMotor = wpilib.Victor(1)
        self.rearLeftMotor = wpilib.Victor(2)
        self.frontRightMotor = wpilib.Victor(3)
        self.rearRightMotor = wpilib.Victor(4)

        self.left = wpilib.SpeedControllerGroup(self.frontLeftMotor, self.rearLeftMotor)
        self.right = wpilib.SpeedControllerGroup(self.frontRightMotor, self.rearRightMotor)

        self.drive = DifferentialDrive(self.left, self.right)
        self.drive.setExpiration(0.1)

        # joysticks 1 on the driver station
        self.stick = wpilib.Joystick(1)

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

if __name__ == '__main__':
    wpilib.run(MyRobot)