"""
Contains final project code

Author: Rebekah Doherty
"""

import tkinter
from tkinter import ttk

import mqtt_remote_method_calls as com
import ev3dev.ev3 as ev3
import time

import robot_controller as robo

from PIL import ImageTk, Image
import random

import json

import collections
import paho.mqtt.client as mqtt


#  Opening Screen
def main():
    mqtt_client = com.MqttClient()
    mqtt_client.connect_to_ev3()
    robot = robo.Snatch3r()
    root = tkinter.Tk()
    root.title("Welcome to Lost in Space")
    root.configure(background='dark blue')

    main_frame = ttk.Frame(root, padding=20)
    main_frame.grid()  # only grid call that does NOT need a row and column

    #  Importing Image
    path = "Lost_in_Space.jpg"
    img = ImageTk.PhotoImage(Image.open(path))

    mqtt_client.send_message("play_audio")


    # The Label widget is a standard Tkinter widget used to display a text or image on the screen.
    panel = ttk.Label(main_frame, image=img, padding=20)
    panel.grid()

    #  Are you ready to begin?
    adventure_button = ttk.Button(main_frame, text='Are You Ready to Begin Your Space Adventure?')
    adventure_button['command'] = lambda: begin_adventure()
    adventure_button.grid()

    root.mainloop()


#  Beginning Adventure:
def begin_adventure():
    # ev3.Sound.speak('Welcome Pilot')

    root = tkinter.Tk()
    root.title("Your Adventure is Beginning")
    root.configure(background='dark blue')

    mqtt_client = com.MqttClient()
    mqtt_client.connect_to_ev3()
    mqtt_client.send_message("say_hello_pilot")

    main_frame = ttk.Frame(root, padding=20)
    main_frame.grid()  # only grid call that does NOT need a row and column

    choose_path_label = ttk.Label(main_frame, text="What Would You Like To Do?")
    choose_path_label.grid(row=2, column=1)

    planet_button = ttk.Button(main_frame, text='Planet Discovery')
    planet_button.grid(row=3, column=0)
    planet_button['command'] = lambda: planet_adventure()
    planet_button.grid()

    savior_button = ttk.Button(main_frame, text='Savior Mission')
    savior_button['command'] = lambda: savior()
    savior_button.grid(row=3, column=1)
    savior_button.grid()

    adventure_button = ttk.Button(main_frame, text='Unknown')
    adventure_button['command'] = lambda: unknown()
    adventure_button.grid(row=3, column=2)
    adventure_button.grid()


def print_contents(entry_box):
    """
    Prints onto the Console the contents of the given ttk.Entry.

    In this example, it is used as the function that is "CALLED BACK"
    when an event (namely, the pressing of a certain Button) occurs.
    """
    contents_of_entry_box = entry_box.get()
    print(contents_of_entry_box)


#  Option 1:
def planet_adventure():
    #  Red planets are bad, any other planet color is good
    mqtt_client = com.MqttClient()
    mqtt_client.connect_to_ev3()

    root = tkinter.Tk()
    root.title("MQTT Spaceship Remote")

    main_frame = ttk.Frame(root, padding=20, relief='raised')
    main_frame.grid()

    left_speed_label = ttk.Label(main_frame, text="Left")
    left_speed_label.grid(row=0, column=0)
    left_speed_entry = ttk.Entry(main_frame, width=8)
    left_speed_entry.insert(0, "400")
    left_speed_entry.grid(row=1, column=0)

    right_speed_label = ttk.Label(main_frame, text="Right")
    right_speed_label.grid(row=0, column=2)
    right_speed_entry = ttk.Entry(main_frame, width=8, justify=tkinter.RIGHT)
    right_speed_entry.insert(0, "400")
    right_speed_entry.grid(row=1, column=2)

    #  Assignments:

    forward_button = ttk.Button(main_frame, text="Forward")
    forward_button.grid(row=2, column=1)
    # forward_button and '<Up>' key is done for your here...
    forward_button['command'] = lambda: go_forward(mqtt_client, left_speed_entry, right_speed_entry)
    root.bind('<Up>', lambda event: go_forward(mqtt_client, left_speed_entry, right_speed_entry))

    left_button = ttk.Button(main_frame, text="Left")
    left_button.grid(row=3, column=0)
    # left_button and '<Left>' key
    left_button['command'] = lambda: go_left(mqtt_client, left_speed_entry, right_speed_entry)
    root.bind('<Left>', lambda event: go_left(mqtt_client, left_speed_entry, right_speed_entry))

    stop_button = ttk.Button(main_frame, text="Stop")
    stop_button.grid(row=3, column=1)
    # stop_button and '<space>' key (note, does not need left_speed_entry, right_speed_entry)
    stop_button['command'] = lambda: just_stop(mqtt_client)
    root.bind('<Left>', lambda event: just_stop(mqtt_client))

    right_button = ttk.Button(main_frame, text="Right")
    right_button.grid(row=3, column=2)
    # right_button and '<Right>' key
    right_button['command'] = lambda: go_right(mqtt_client, left_speed_entry, right_speed_entry)
    root.bind('<Left>', lambda event: go_right(mqtt_client, left_speed_entry, right_speed_entry))

    back_button = ttk.Button(main_frame, text="Back")
    back_button.grid(row=4, column=1)
    # back_button and '<Down>' key
    back_button['command'] = lambda: go_backward(mqtt_client, left_speed_entry, right_speed_entry)
    root.bind('<Down>', lambda event: go_backward(mqtt_client, left_speed_entry, right_speed_entry))

    up_button = ttk.Button(main_frame, text="Up")
    up_button.grid(row=5, column=0)
    up_button['command'] = lambda: send_up(mqtt_client)
    root.bind('<u>', lambda event: send_up(mqtt_client))

    down_button = ttk.Button(main_frame, text="Down")
    down_button.grid(row=6, column=0)
    down_button['command'] = lambda: send_down(mqtt_client)
    root.bind('<j>', lambda event: send_down(mqtt_client))

    # Buttons for quit and exit
    q_button = ttk.Button(main_frame, text="Quit")
    q_button.grid(row=5, column=2)
    q_button['command'] = (lambda: quit_program(mqtt_client, False))

    e_button = ttk.Button(main_frame, text="Exit")
    e_button.grid(row=6, column=2)
    e_button['command'] = (lambda: quit_program(mqtt_client, True))

    root.mainloop()


#  Option 2:
def savior():
    mqtt_client = com.MqttClient()
    mqtt_client.connect_to_ev3()
    #  Use IR remote to drive to the beacon
    print("savior")
    mqtt_client.send_message("color_report")


#  Option 3:
def unknown():
    print("unknown")


# Arm command callbacks
def send_up(mqtt_client):
    print("arm_up")
    mqtt_client.send_message("arm_up")


def send_down(mqtt_client):
    print("arm_down")
    mqtt_client.send_message("arm_down")


# Quit and Exit button callbacks
def quit_program(mqtt_client, shutdown_ev3):
    if shutdown_ev3:
        print("shutdown")
        mqtt_client.send_message("shutdown")
    mqtt_client.close()
    exit()


def go_forward(mqtt_client, left_motor, right_motor):
    print("go_forward")
    mqtt_client.send_message("drive_inches", [2, 400])


def go_backward(mqtt_client, left_motor, right_motor):
    print("go_backward")
    mqtt_client.send_message("drive_inches", [-2, 400])


def go_left(mqtt_client, left_motor, right_motor):
    print("go_left")
    mqtt_client.send_message("turn_degrees", [45, 400])


def go_right(mqtt_client, left_motor, right_motor):
    print("go_right")
    mqtt_client.send_message("turn_degrees", [-45, 400])


def just_stop(mqtt_client):
    print("just_stop")
    mqtt_client.send_message("shutdown")



main()
