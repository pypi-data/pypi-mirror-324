# Part of the RoboticsWare project - https://roboticsware.uz
# Copyright (C) 2022 RoboticsWare (neopia.uz@gmail.com)
# 
# This library is free software; you can redistribute it and/or
# modify it under the terms of the GNU Lesser General Public
# License as published by the Free Software Foundation; either
# version 2.1 of the License, or (at your option) any later version.
# 
# This library is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the GNU
# Lesser General Public License for more details.
# 
# You should have received a copy of the GNU Lesser General
# Public License along with this library; if not, write to the
# Free Software Foundation, Inc., 59 Temple Place, Suite 330,
# Boston, MA  02111-1307  USA

import pygame
import sys, math
from pgzhelper.pgzhelper import Util
from pgzhelper.pgzhelper import Actor
from pgzhelper.pgzhelper import Collide
from pgzero import game
from pgzero.keyboard import keyboard
from pgzero.constants import keys
from pgzero.rect import Rect


__version__ = "1.0.0"

__all__ = [
    "Actor",
    "Collide",
    "Util",
    "set_fullscreen",
    "toggle_fullscreen",
    "hide_mouse",
    "show_mouse",
    "distance_to",
    "direction_to",
    "game",
    "keyboard",
    "keys",
    "Rect",
]

_fullscreen = False

def set_fullscreen():
  global _fullscreen
  mod = sys.modules['__main__']
  mod.screen.surface = pygame.display.set_mode((mod.WIDTH, mod.HEIGHT), pygame.FULLSCREEN)
  _fullscreen = True

def set_windowed():
  global _fullscreen
  mod = sys.modules['__main__']
  mod.screen.surface = pygame.display.set_mode((mod.WIDTH, mod.HEIGHT))
  _fullscreen = False

def toggle_fullscreen():
  if _fullscreen:
    set_windowed()
  else:
    set_fullscreen()

def hide_mouse():
  pygame.mouse.set_visible(False)

def show_mouse():
  pygame.mouse.set_visible(True)

def distance_to(from_x, from_y, to_x, to_y):
  dx = to_x - from_x
  dy = to_y - from_y
  return math.sqrt(dx**2 + dy**2)

def direction_to(from_x, from_y, to_x, to_y):
  dx = to_x - from_x
  dy = from_y - to_y

  angle = math.degrees(math.atan2(dy, dx))
  if angle > 0:
    return angle

  return 360 + angle