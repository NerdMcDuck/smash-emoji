"""A program to control Smash bros running in an emulator"""
import argparse
import threading
import time
from typing import List
import vgamepad as vg
from vgamepad import VX360Gamepad
import queue


def do_controls(xbox360pad: VX360Gamepad, emoji: str) -> None:
    """
    Takes a list of emojis and maps them to their corresponding control scheme
    :param xbox360pad:
    :param emoji: The list of emoji commands
    :return: a list of strings command to be passed to the controller
    """
    cmd: str = emoji.lower().strip()
    if cmd == "jump":
        xbox360pad.press_button(button=vg.XUSB_BUTTON.XUSB_GAMEPAD_X)

    if cmd == "rw":
        xbox360pad.left_joystick_float(x_value_float=1.0, y_value_float=0.0)
        xbox360pad.update()
        time.sleep(0.2)
        xbox360pad.left_joystick_float(x_value_float=0.0, y_value_float=0.0)

    if cmd == "lw":
        xbox360pad.left_joystick_float(x_value_float=-1.0, y_value_float=0.0)
        xbox360pad.update()
        time.sleep(0.5)
        xbox360pad.left_joystick_float(x_value_float=0.0, y_value_float=0.0)

    if cmd == "attack":
        xbox360pad.press_button(button=vg.XUSB_BUTTON.XUSB_GAMEPAD_A)

    if cmd == "special":
        xbox360pad.press_button(button=vg.XUSB_BUTTON.XUSB_GAMEPAD_B)

    if cmd == "smash":
        xbox360pad.right_joystick_float(x_value_float=0.0, y_value_float=-1.0)
        xbox360pad.update()
        time.sleep(1.0)
        xbox360pad.right_joystick_float(x_value_float=0.0, y_value_float=0.0)
        xbox360pad.update()

    else:
        xbox360pad.press_button(button=vg.XUSB_BUTTON.XUSB_GAMEPAD_DPAD_UP)

    xbox360pad.update()
    time.sleep(0.2)

    # reset
    xbox360pad.release_button(button=vg.XUSB_BUTTON.XUSB_GAMEPAD_X)
    xbox360pad.release_button(button=vg.XUSB_BUTTON.XUSB_GAMEPAD_A)
    xbox360pad.release_button(button=vg.XUSB_BUTTON.XUSB_GAMEPAD_B)
    xbox360pad.release_button(button=vg.XUSB_BUTTON.XUSB_GAMEPAD_DPAD_UP)
    xbox360pad.update()
    time.sleep(0.5)


def gamepad_smash(xbox360pad: VX360Gamepad):
    """Go through a set of pre-programmed commands"""
    # press a button to wake the device up
    xbox360pad.press_button(button=vg.XUSB_BUTTON.XUSB_GAMEPAD_A)
    xbox360pad.update()
    time.sleep(0.5)
    xbox360pad.release_button(button=vg.XUSB_BUTTON.XUSB_GAMEPAD_A)
    xbox360pad.update()
    time.sleep(0.5)

    # press buttons and things
    xbox360pad.press_button(button=vg.XUSB_BUTTON.XUSB_GAMEPAD_A)
    xbox360pad.press_button(button=vg.XUSB_BUTTON.XUSB_GAMEPAD_B)
    xbox360pad.press_button(button=vg.XUSB_BUTTON.XUSB_GAMEPAD_LEFT_SHOULDER)
    xbox360pad.press_button(button=vg.XUSB_BUTTON.XUSB_GAMEPAD_DPAD_DOWN)
    xbox360pad.press_button(button=vg.XUSB_BUTTON.XUSB_GAMEPAD_DPAD_LEFT)
    xbox360pad.left_trigger_float(value_float=0.5)
    xbox360pad.right_trigger_float(value_float=0.5)
    xbox360pad.left_joystick_float(x_value_float=0.0, y_value_float=0.2)
    xbox360pad.right_joystick_float(x_value_float=-1.0, y_value_float=1.0)

    xbox360pad.update()

    time.sleep(1.0)

    # release buttons and things
    xbox360pad.release_button(button=vg.XUSB_BUTTON.XUSB_GAMEPAD_A)
    xbox360pad.release_button(button=vg.XUSB_BUTTON.XUSB_GAMEPAD_DPAD_LEFT)
    xbox360pad.right_trigger_float(value_float=0.0)
    xbox360pad.right_joystick_float(x_value_float=0.0, y_value_float=0.0)

    xbox360pad.update()

    time.sleep(1.0)

    # reset gamepad to default state
    xbox360pad.reset()

    xbox360pad.update()

    time.sleep(1.0)


def main(xbox360pad: VX360Gamepad):
    """
      Given an VX360Gamepad object, send the button commands
      :param xbox360pad:
      :return:
    """
    # init player 2
    time.sleep(2)
    xbox360pad.press_button(button=vg.XUSB_BUTTON.XUSB_GAMEPAD_LEFT_SHOULDER)
    xbox360pad.press_button(button=vg.XUSB_BUTTON.XUSB_GAMEPAD_RIGHT_SHOULDER)
    xbox360pad.update()
    time.sleep(0.5)
    xbox360pad.release_button(button=vg.XUSB_BUTTON.XUSB_GAMEPAD_LEFT_SHOULDER)
    xbox360pad.release_button(button=vg.XUSB_BUTTON.XUSB_GAMEPAD_RIGHT_SHOULDER)
    xbox360pad.update()
    time.sleep(1.0)

    # select a random character
    xbox360pad.left_joystick_float(x_value_float=0.0, y_value_float=0.8)
    xbox360pad.update()
    time.sleep(0.5)
    xbox360pad.left_joystick_float(x_value_float=0.0, y_value_float=0.0)
    xbox360pad.update()
    time.sleep(1.0)

    xbox360pad.press_button(button=vg.XUSB_BUTTON.XUSB_GAMEPAD_B)
    xbox360pad.update()
    time.sleep(0.5)
    xbox360pad.release_button(button=vg.XUSB_BUTTON.XUSB_GAMEPAD_B)
    xbox360pad.update()
    time.sleep(2.5)

    # some inputs
    # while True:
    #     gamepad_smash(xbox360pad)


def process_input_worker(blocking_q: queue.Queue, gp: VX360Gamepad):
    print(f"{gp=}\n")

    while True:
        cmd: str = blocking_q.get()
        print(f'Working on {cmd}')

        if cmd.lower() != "start":
            do_controls(gp, cmd)

        print(f'Finished {cmd}')
        print(f"items remaining in queue {blocking_q.qsize()}")
        blocking_q.task_done()


if __name__ == '__main__':
    # parser = argparse.ArgumentParser(
    #     prog='Smash-Bot',
    #     description='Pass in a one or more of the defined emojis',
    #     epilog='Text at the bottom of help')
    # parser.add_argument('emoji', nargs='+')  # positional argument
    #
    # args = parser.parse_args()
    # nothing: str = do_controls(args.emoji)
    # print(f"{args.emoji=} and {nothing=}")

    # init virtual Xbox 360 controller
    gamepad: VX360Gamepad = vg.VX360Gamepad()

    # init blocking queue with a total of 5 items
    q = queue.Queue(maxsize=5)

    # Turn-on the worker thread.
    threading.Thread(
        target=process_input_worker, daemon=True, args=(q, gamepad)).start()

    while 1:

        user_input = input("Enter up to 5 space separated emoji commands: ")
        usr_input_lst: List[str] = user_input.split(" ")

        if "stop" in usr_input_lst:
            print("Thanks for playing!")
            break

        if "start" in usr_input_lst:
            main(gamepad)

        print(f"{user_input=}")

        # Send thirty task requests to the worker.
        for item in usr_input_lst:
            q.put(item, block=True)

        # Block until all tasks are done.
        q.join()
