# -*- coding: utf-8 -*-

from . import State

global current_state

class State_A(State.State):
    def handle_cmd_dir_up(self):
        print("handle_cmd_dir_up from State_A")

    def handle_cmd_dir_down(self):
        print("handle_cmd_dir_down from State_A")

    def handle_cmd_play(self):
        print("handle_cmd_play from State_A")

    def handle_cmd_prev(self):
        print("handle_cmd_prev from State_A")

    def handle_cmd_next(self):
        print("handle_cmd_next from State_A")

    def handle_cmd_esc(self):
        print("handle_cmd_esc from State_A")

    def handle_cmd_stop(self):
        print("handle_cmd_stop from State_A")

    def handle_cmd_chmod(self):
        print("handle_cmd_chmod from State_A")
