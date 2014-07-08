#!/usr/bin/env python3

from abc import ABCMeta, abstractmethod
from base import Cloneable

HANDLE = {'CMD_DIR_UP' : handle_cmd_dir_up,
          'CMD_DIR_DOWN' : handle_cmd_dir_down,
          'CMD_PLAY' : handle_cmd_play,
          'CMD_PREV' : handle_cmd_prev,
          'CMD_NEXT' : handle_cmd_next,
          'CMD_ESC' : handle_cmd_esc,
          'CMD_STOP' : handle_cmd_stop,
          'CMD_CHMOD' : handle_cmd_chmod
         }

class State(Cloneable, metaclass=ABCMeta):

    # def handle(self, cmd):
    #    self.locals()['handle_cmd_' + cmd]()

    def handle(self, cmd):
        HANDLE[cmd]()

    @abstractmethod
    def handle_cmd_dir_up(self):
        pass

    @abstractmethod
    def handle_cmd_dir_down(self):
        pass

    @abstractmethod
    def handle_cmd_play(self):
        pass

    @abstractmethod
    def handle_cmd_prev(self):
        pass

    @abstractmethod
    def handle_cmd_next(self):
        pass

    @abstractmethod
    def handle_cmd_esc(self):
        pass

    @abstractmethod
    def handle_cmd_stop(self):
        pass

    @abstractmethod
    def handle_cmd_chmod(self):
        pass


