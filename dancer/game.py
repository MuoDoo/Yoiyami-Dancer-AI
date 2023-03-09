from config import REWARD_IN_ENV, REWARD_ON_POWER, REWARD_ON_BE_SHOT
from .memory_reader import MemoryReader
from .process import find_process, image_grab, set_foreground
from pynput.keyboard import Key, Controller

import numpy as np
import time


def action(action_index):
    if action_index < 0:
        return

    keyboard = Controller()
    keyboard.press('z')
    keyboard.press('x')
    keyboard.release(Key.left)
    keyboard.release(Key.right)
    keyboard.release(Key.up)
    keyboard.release(Key.down)

    if action_index == 0:
        return
    elif action_index == 1:
        keyboard.press(Key.left)
    elif action_index == 2:
        keyboard.press(Key.right)
    elif action_index == 3:
        keyboard.press(Key.up)
    elif action_index == 4:
        keyboard.press(Key.down)
    elif action_index == 5:
        keyboard.press(Key.up)
        keyboard.press(Key.left)
    elif action_index == 6:
        keyboard.press(Key.up)
        keyboard.press(Key.right)
    elif action_index == 7:
        keyboard.press(Key.down)
        keyboard.press(Key.left)
    elif action_index == 8:
        keyboard.press(Key.down)
        keyboard.press(Key.right)
    elif action_index == 9:
        keyboard.press(Key.left)
        keyboard.press(Key.right)
    # elif action_index == 5:
    #     press_key(DIK_LEFT)
    #     press_key(DIK_UP)
    # elif action_index == 6:
    #     press_key(DIK_LEFT)
    #     press_key(DIK_DOWN)
    # elif action_index == 7:
    #     press_key(DIK_RIGHT)
    #     press_key(DIK_UP)
    # elif action_index == 8:
    #     press_key(DIK_RIGHT)
    #     press_key(DIK_DOWN)


class DANCER(object):

    def __init__(self):
        pid, hwnd = find_process('rumiaDDR.exe')
        self.hwnd = hwnd
        self.pid = pid
        self.memory_reader = MemoryReader(pid)
        self.player = self.memory_reader.player_info()

    def play(self, action_index):
        set_foreground(self.hwnd)
        action(action_index)
        # time.sleep(0.5)
        prev_power = self.player.power
        prev_health = self.player.health

        self.player = self.memory_reader.player_info()
        if self.player.health > 0:
            prev_health = prev_health if prev_health > 0 else 10  # 10 for reset game
            reward = self.calculate_reward(prev_power, prev_health)
            return image_grab(self.hwnd, (0, 0, 0, 0)), reward, False
        else:
            self.restart_on_end()
            self.player = self.memory_reader.player_info()
            return image_grab(self.hwnd, (0, 0, 0, 0)), 0, True
    #     (34, 36, -228, -18)

    def restart_on_end(self):
        print("END")
        keyboard = Controller()
        keyboard.release('z')
        keyboard.release('x')
        time.sleep(0.2)
        # press_key(DIK_Z)
        keyboard.press('z')
        time.sleep(0.2)
        keyboard.release('z')
        # release_key(DIK_Z)

    def calculate_reward(self, prev_power, prev_health):
        reward = REWARD_IN_ENV

        return reward + \
            REWARD_ON_BE_SHOT*( max(prev_health-self.player.health,0) )/1000


