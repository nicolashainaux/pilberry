# -*- coding: utf-8 -*-

# Pilberry runs a car radio based on Raspberry Pi
# Copyright 2014 Olivier Cecillon <ocecillon@users.sourceforge.net>
# and Nicolas Hainaux <nico_h@users.sourceforge.net>

# This file is part of Pilberry.

# Pilberry is free software; you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation; either version 3 of the License, or
# any later version.

# Pilberry is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.

# You should have received a copy of the GNU General Public License
# along with Pilberry; if not, write to the Free Software
# Foundation, Inc., 51 Franklin St, Fifth Floor, Boston, MA  02110-1301  USA


from .State import State

global current_state

class State_A(State):

    def __init__(self):
        pass

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
