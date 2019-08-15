"""
  Library of EV3 robot functions that are useful in many different applications. For example things
  like arm_up, arm_down, driving around, or doing things with the Pixy camera.

  Add commands as needed to support the features you'd like to implement.  For organizational
  purposes try to only write methods into this library that are NOT specific to one tasks, but
  rather methods that would be useful regardless of the activity.  For example, don't make
  a connection to the remote control that sends the arm up if the ir remote control up button
  is pressed.  That's a specific input --> output task.  Maybe some other task would want to use
  the IR remote up button for something different.  Instead just make a method called arm_up that
  could be called.  That way it's a generic action that could be used in any task.
"""

import ev3dev.ev3 as ev3
import math
import time
from time   import sleep


class Snatch3r(object):
    """Commands for the Snatch3r robot that might be useful in many different programs."""
    def drive_inches(self, inches_to_drive, drive_speed_sp):
        left_motor = ev3.LargeMotor(ev3.OUTPUT_B)
        right_motor = ev3.LargeMotor(ev3.OUTPUT_C)

        # Check that the motors are actually connected
        assert left_motor.connected
        assert right_motor.connected


        touch_sensor = ev3.TouchSensor()
        assert touch_sensor

        cl = ev3.ColorSensor()
        assert cl

        btn = ev3.Button()
        led_colors = [ev3.Leds.BLACK,
                      ev3.Leds.GREEN,
                      ev3.Leds.RED,
                      ev3.Leds.AMBER]

        # Potential values of the color_sensor.color property
        #   ev3.ColorSensor.COLOR_NOCOLOR is the value 0
        #   ev3.ColorSensor.COLOR_BLACK   is the value 1
        #   ev3.ColorSensor.COLOR_BLUE    is the value 2
        #   ev3.ColorSensor.COLOR_GREEN   is the value 3
        #   ev3.ColorSensor.COLOR_YELLOW  is the value 4
        #   ev3.ColorSensor.COLOR_RED     is the value 5
        #   ev3.ColorSensor.COLOR_WHITE   is the value 6
        #   ev3.ColorSensor.COLOR_BROWN   is the value 7

        cl.mode = 'COL-COLOR'
        colors = ('unknown', 'black', 'blue', 'green', 'yellow', 'red', 'white', 'brown')

        degrees_per_inch = 90
        motor_turns_needed_in_degrees = inches_to_drive * degrees_per_inch
        left_motor.run_to_rel_pos(position_sp=motor_turns_needed_in_degrees, speed_sp=drive_speed_sp,
                                      stop_action='brake')
        right_motor.run_to_rel_pos(position_sp=motor_turns_needed_in_degrees, speed_sp=drive_speed_sp,
                                       stop_action='brake')

        left_motor.wait_while('running')
        right_motor.wait_while('running')

        if cl.color == 5:
            ev3.Sound.play("/home/robot/csse120/assets/sounds/danger_louder.wav")
            ev3.Leds.set_color(ev3.Leds.LEFT, ev3.Leds.RED)
            ev3.Leds.set_color(ev3.Leds.RIGHT, ev3.Leds.RED)
            motor_turns_needed_in_degrees = -6 * degrees_per_inch
            left_motor.run_to_rel_pos(position_sp=motor_turns_needed_in_degrees, speed_sp=drive_speed_sp,
                                      stop_action='brake')
            right_motor.run_to_rel_pos(position_sp=motor_turns_needed_in_degrees, speed_sp=drive_speed_sp,
                                       stop_action='brake')
            sleep(0.2)
            ev3.Leds.set_color(ev3.Leds.LEFT, ev3.Leds.BLACK)
            ev3.Leds.set_color(ev3.Leds.RIGHT, ev3.Leds.BLACK)
            print("red")
            sleep(5)
        if cl.color == 4:
            ev3.Sound.speak("We have discovered a safe planet")
            ev3.Leds.set_color(ev3.Leds.LEFT, ev3.Leds.GREEN)
            ev3.Leds.set_color(ev3.Leds.RIGHT, ev3.Leds.GREEN)
            print("green")
            sleep(5)
        if cl.color == 3:
            ev3.Sound.speak("We have discovered a safe planet")
            ev3.Leds.set_color(ev3.Leds.LEFT, ev3.Leds.GREEN)
            ev3.Leds.set_color(ev3.Leds.RIGHT, ev3.Leds.GREEN)
            sleep(5)
        if cl.color == 2:
            ev3.Sound.speak("We have discovered a safe planet")
            ev3.Leds.set_color(ev3.Leds.LEFT, ev3.Leds.GREEN)
            ev3.Leds.set_color(ev3.Leds.RIGHT, ev3.Leds.GREEN)
            print("blue")
            sleep(1)
        if cl.color == 0:
            ev3.Leds.set_color(ev3.Leds.LEFT, ev3.Leds.BLACK)
            ev3.Leds.set_color(ev3.Leds.RIGHT, ev3.Leds.BLACK)

    def turn_degrees(self, degrees_to_turn, turn_speed_sp):
        """ Turns a set number of degrees. Positive is a left turn. """
        left_motor = ev3.LargeMotor(ev3.OUTPUT_B)
        right_motor = ev3.LargeMotor(ev3.OUTPUT_C)

        # Check that the motors are actually connected
        assert left_motor.connected
        assert right_motor.connected

        if degrees_to_turn > 0: #  left turn
            left_motor.run_to_rel_pos(position_sp=-degrees_to_turn * 5, speed_sp=turn_speed_sp,stop_action='brake')
            right_motor.run_to_rel_pos(position_sp=degrees_to_turn * 5, speed_sp=turn_speed_sp,stop_action='brake')
        elif degrees_to_turn < 0: #  right turn
            left_motor.run_to_rel_pos(position_sp=-degrees_to_turn * 5, speed_sp=turn_speed_sp, stop_action='brake')
            right_motor.run_to_rel_pos(position_sp=degrees_to_turn * 5, speed_sp=turn_speed_sp, stop_action='brake')
        left_motor.wait_while('running')
        right_motor.wait_while('running')

    def arm_calibration(self, touch_sensor):
        arm_motor = ev3.MediumMotor(ev3.OUTPUT_A)
        arm_motor.run_forever(speed_sp=900)
        while not touch_sensor.is_pressed:
            time.sleep(0.01)
        arm_motor.stop(stop_action="brake")
        ev3.Sound.beep().wait()

        arm_revolutions_for_full_range = 14.2
        arm_motor.run_to_abs_pos(position_sp=-arm_revolutions_for_full_range)
        arm_motor.wait_while(ev3.Motor.STATE_RUNNING)
        ev3.Sound.beep().wait()
        arm_motor.position = 0

    def arm_up(self):
        touch_sensor = ev3.TouchSensor()
        assert touch_sensor
        arm_motor = ev3.MediumMotor(ev3.OUTPUT_A)
        arm_motor.run_forever(speed_sp=900)
        while not touch_sensor.is_pressed:
            time.sleep(0.01)
        arm_motor.stop(stop_action="brake")
        ev3.Sound.beep().wait()

    def arm_down(self):
        arm_motor = ev3.MediumMotor(ev3.OUTPUT_A)
        arm_revolutions_for_full_range = 14.2
        arm_motor.run_to_abs_pos(position_sp=-arm_revolutions_for_full_range)
        arm_motor.wait_while(ev3.Motor.STATE_RUNNING)
        ev3.Sound.beep().wait()
        arm_motor.position = 0

    def left_motor(self, degrees_to_turn, speed_sp):
        left_motor = ev3.LargeMotor(ev3.OUTPUT_B)
        right_motor = ev3.LargeMotor(ev3.OUTPUT_C)

        # Check that the motors are actually connected
        assert left_motor.connected
        assert right_motor.connected

        left_motor.run_to_rel_pos(position_sp=degrees_to_turn, speed_sp=speed_sp, stop_action='brake')
        left_motor.wait_while('running')
        right_motor.wait_while('running')


    def right_motor(self, degrees_to_turn, speed_sp):
        left_motor = ev3.LargeMotor(ev3.OUTPUT_B)
        right_motor = ev3.LargeMotor(ev3.OUTPUT_C)

        # Check that the motors are actually connected
        assert left_motor.connected
        assert right_motor.connected

        right_motor.run_to_rel_pos(position_sp=degrees_to_turn, speed_sp=speed_sp, stop_action='brake')
        left_motor.wait_while('running')
        right_motor.wait_while('running')


    def loop_forever(self):
        self.running = True
        while self.running:
            time.sleep(0.1)  # Do nothing until the robot does a shutdown.def loop_forever(self):
        # This is a convenience method that I don't really recommend for most programs other than m5.
        #   This method is only useful if the only input to the robot is coming via mqtt.
        #   MQTT messages will still call methods, but no other input or output happens.
        # This method is given here since the concept might be confusing.
        self.running = True
        while self.running:
            time.sleep(0.1)


    def shutdown(self):
        ev3.Sound.speak("Why did you ask me to stop").wait()
        self.running = False


    def beep(self):
        ev3.Sound.beep().wait()
        self.running = True

    def color_report(self):
        touch_sensor = ev3.TouchSensor()
        assert touch_sensor

        cl = ev3.ColorSensor()
        assert cl

        btn = ev3.Button()
        led_colors = [ev3.Leds.BLACK,
                      ev3.Leds.GREEN,
                      ev3.Leds.RED,
                      ev3.Leds.AMBER]

        # Potential values of the color_sensor.color property
        #   ev3.ColorSensor.COLOR_NOCOLOR is the value 0
        #   ev3.ColorSensor.COLOR_BLACK   is the value 1
        #   ev3.ColorSensor.COLOR_BLUE    is the value 2
        #   ev3.ColorSensor.COLOR_GREEN   is the value 3
        #   ev3.ColorSensor.COLOR_YELLOW  is the value 4
        #   ev3.ColorSensor.COLOR_RED     is the value 5
        #   ev3.ColorSensor.COLOR_WHITE   is the value 6
        #   ev3.ColorSensor.COLOR_BROWN   is the value 7

        cl.mode = 'COL-COLOR'
        colors = ('unknown', 'black', 'blue', 'green', 'yellow', 'red', 'white', 'brown')
        while not touch_sensor.value():
            if cl.color == 5:
                ev3.Sound.speak("Danger, Will Robinson")
                ev3.Leds.set_color(ev3.Leds.LEFT, ev3.Leds.RED)
                ev3.Leds.set_color(ev3.Leds.RIGHT, ev3.Leds.RED)
                print("red")
                sleep(5)
            if cl.color == 4:
                ev3.Sound.speak("We have discovered a safe planet")
                ev3.Leds.set_color(ev3.Leds.LEFT, ev3.Leds.GREEN)
                ev3.Leds.set_color(ev3.Leds.RIGHT, ev3.Leds.GREEN)
                print("green")
                sleep(5)
            if cl.color == 3:
                ev3.Sound.speak("We have discovered a safe planet")
                ev3.Leds.set_color(ev3.Leds.LEFT, ev3.Leds.GREEN)
                ev3.Leds.set_color(ev3.Leds.RIGHT, ev3.Leds.GREEN)
                sleep(5)
            if cl.color == 2:
                ev3.Sound.speak("We have discovered a safe planet")
                ev3.Leds.set_color(ev3.Leds.LEFT, ev3.Leds.GREEN)
                ev3.Leds.set_color(ev3.Leds.RIGHT, ev3.Leds.GREEN)
                print("blue")
                sleep(1)
            if cl.color == 0:
                ev3.Leds.set_color(ev3.Leds.LEFT, ev3.Leds.BLACK)
                ev3.Leds.set_color(ev3.Leds.RIGHT, ev3.Leds.BLACK)


    def say_hello_pilot(self):
        ev3.Sound.speak("Welcome, Pilot")


    def play_old_danger(self):
        ev3.Sound.play("/home/robot/csse120/assets/sounds/lost_in_space_danger.wav")

    def play_new_danger(self):
        ev3.Sound.play("/home/robot/csse120/assets/sounds/danger_will_robinson.wav")
