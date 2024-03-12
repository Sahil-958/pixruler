# This file is part of pixruler.
#
# Copyright (c) 2024 Sahil <118348625+Sahil-958@users.noreply.github.com>
# pixruler is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# pixruler is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with pixruler.  If not, see <https://www.gnu.org/licenses/>.

# actions.py
# contains the key actions for the image viewer. The key actions are
# the actions that are performed when a key is pressed. The key actions are
# defined in the key_actions dictionary. The dictionary maps the key to the
# action that should be performed when the key is pressed. The key_actions
# dictionary is used in the main.py file to connect the key press event to the
# action that should be performed.
from utils import *
import sys
import cv2
import gi
import pyscreenshot

gi.require_version("Gtk", "3.0")
gi.require_version("GdkPixbuf", "2.0")
from gi.repository import Gtk, GdkPixbuf, Gdk


key_actions = {
    Gdk.KEY_1: lambda self, _: setattr(self, "step_size_mp", 1),
    Gdk.KEY_2: lambda self, _: setattr(self, "step_size_mp", 2),
    Gdk.KEY_3: lambda self, _: setattr(self, "step_size_mp", 3),
    Gdk.KEY_4: lambda self, _: setattr(self, "step_size_mp", 4),
    Gdk.KEY_5: lambda self, _: setattr(self, "step_size_mp", 5),
    Gdk.KEY_6: lambda self, _: setattr(self, "step_size_mp", 6),
    Gdk.KEY_7: lambda self, _: setattr(self, "step_size_mp", 7),
    Gdk.KEY_8: lambda self, _: setattr(self, "step_size_mp", 8),
    Gdk.KEY_9: lambda self, _: setattr(self, "step_size_mp", 9),
    Gdk.KEY_0: lambda self, _: setattr(self, "step_size_mp", 10),
    Gdk.KEY_Return: lambda _, __: pyscreenshot.grab().save("screenshot.png"),
    (Gdk.KEY_h, Gdk.KEY_Left): lambda self, _: (
        setattr(
            self,
            "cursor_pos",
            [
                adjust_value(self.cursor_pos[0], self.step_size, False, 0),
                self.cursor_pos[1],
            ],
        ),
        live_colors(self),
        update_lines(self),
    ),
    (Gdk.KEY_l, Gdk.KEY_Right): lambda self, _: (
        setattr(
            self,
            "cursor_pos",
            [
                adjust_value(self.cursor_pos[0], self.step_size, True, 0),
                self.cursor_pos[1],
            ],
        ),
        live_colors(self),
        update_lines(self),
    ),
    (Gdk.KEY_j, Gdk.KEY_Down): lambda self, _: (
        setattr(
            self,
            "cursor_pos",
            [
                self.cursor_pos[0],
                adjust_value(
                    self.cursor_pos[1],
                    self.step_size,
                    True,
                    0,
                    self.img.shape[0] - 1,
                ),
            ],
        ),
        live_colors(self),
        update_lines(self),
    ),
    (Gdk.KEY_k, Gdk.KEY_Up): lambda self, _: (
        setattr(
            self,
            "cursor_pos",
            [
                self.cursor_pos[0],
                adjust_value(self.cursor_pos[1], self.step_size, False, 0),
            ],
        ),
        live_colors(self),
        update_lines(self),
    ),
    Gdk.KEY_H: lambda self, _: (
        setattr(
            self,
            "stats_pos",
            [
                adjust_value(self.stats_pos[0], self.step_size, False, 0),
                self.stats_pos[1],
            ],
        ),
        live_colors(self),
    ),
    Gdk.KEY_L: lambda self, _: (
        setattr(
            self,
            "stats_pos",
            [
                adjust_value(self.stats_pos[0], self.step_size, True, 0),
                self.stats_pos[1],
            ],
        ),
        live_colors(self),
    ),
    Gdk.KEY_J: lambda self, _: (
        setattr(
            self,
            "stats_pos",
            [
                self.stats_pos[0],
                adjust_value(self.stats_pos[1], self.step_size, True, 0),
            ],
        ),
        live_colors(self),
    ),
    Gdk.KEY_K: lambda self, _: (
        setattr(
            self,
            "stats_pos",
            [
                self.stats_pos[0],
                adjust_value(self.stats_pos[1], self.step_size, False, 0),
            ],
        ),
        live_colors(self),
    ),
    Gdk.KEY_t: lambda self, _: (
        setattr(
            self,
            "line_thickness",
            adjust_value(self.line_thickness, self.step_size / 3, True, 0.7, 10),
        ),
        update_lines(self),
    ),
    Gdk.KEY_T: lambda self, _: (
        setattr(
            self,
            "line_thickness",
            adjust_value(self.line_thickness, self.step_size / 3, False, 0.7),
        ),
        update_lines(self),
    ),
    Gdk.KEY_f: lambda self, _: (
        setattr(
            self,
            "font_size",
            adjust_value(self.font_size, self.step_size / 2, True, 0),
        )
    ),
    Gdk.KEY_F: lambda self, _: (
        setattr(
            self,
            "font_size",
            adjust_value(self.font_size, self.step_size / 2, False, 0),
        )
    ),
    Gdk.KEY_s: lambda self, _: (
        setattr(
            self,
            "stats_font_size",
            adjust_value(self.stats_font_size, self.step_size / 2, True, 0),
        )
    ),
    Gdk.KEY_S: lambda self, _: (
        setattr(
            self,
            "stats_font_size",
            adjust_value(self.stats_font_size, self.step_size / 2, False, 0),
        )
    ),
    Gdk.KEY_o: lambda self, _: (
        setattr(
            self,
            "offset",
            [
                adjust_value(self.offset[0], self.step_size, True),
                self.offset[1],
            ],
        )
    ),
    Gdk.KEY_O: lambda self, _: (
        setattr(
            self,
            "offset",
            [
                adjust_value(self.offset[0], self.step_size, False),
                self.offset[1],
            ],
        )
    ),
    Gdk.KEY_p: lambda self, _: (
        setattr(
            self,
            "offset",
            [
                self.offset[0],
                adjust_value(self.offset[1], self.step_size, True),
            ],
        )
    ),
    Gdk.KEY_P: lambda self, _: (
        setattr(
            self,
            "offset",
            [
                self.offset[0],
                adjust_value(self.offset[1], self.step_size, False),
            ],
        )
    ),
    Gdk.KEY_c: lambda self, _: (
        setattr(self, "colors", [self.colors[-1]] + self.colors[:-1]),
        setattr(self, "line_text_color", self.colors[1]),
        setattr(self, "stats_text_color", self.colors[1]),
        setattr(self, "line_color", self.colors[0]),
    ),
    Gdk.KEY_C: lambda self, _: (
        setattr(self, "is_live_colors", not self.is_live_colors)
    ),
    Gdk.KEY_r: lambda self, _: (
        setattr(
            self,
            "lower_threshold",
            adjust_value(
                self.lower_threshold,
                self.step_size,
                True,
                0,
                self.upper_threshold - 1,
            ),
        ),
        setattr(
            self,
            "edges",
            cv2.Canny(self.gray, self.lower_threshold, self.upper_threshold),
        ),
        update_lines(self),
    ),
    Gdk.KEY_R: lambda self, _: (
        setattr(
            self,
            "lower_threshold",
            adjust_value(
                self.lower_threshold,
                self.step_size,
                False,
                0,
                self.upper_threshold - 1,
            ),
        ),
        setattr(
            self,
            "edges",
            cv2.Canny(self.gray, self.lower_threshold, self.upper_threshold),
        ),
        update_lines(self),
    ),
    Gdk.KEY_u: lambda self, _: (
        setattr(
            self,
            "upper_threshold",
            adjust_value(self.upper_threshold, self.step_size, True),
        ),
        setattr(
            self,
            "edges",
            cv2.Canny(self.gray, self.lower_threshold, self.upper_threshold),
        ),
        update_lines(self),
    ),
    Gdk.KEY_U: lambda self, _: (
        setattr(
            self,
            "upper_threshold",
            adjust_value(
                self.upper_threshold,
                self.step_size,
                False,
                self.lower_threshold + 1,
            ),
        ),
        setattr(
            self,
            "edges",
            cv2.Canny(self.gray, self.lower_threshold, self.upper_threshold),
        ),
        update_lines(self),
    ),
    Gdk.KEY_n: lambda self, _: (
        setattr(
            self,
            "current_arg_index",
            adjust_value(self.current_arg_index, 1, True, None, self.arg_count - 2),
        ),
        prepare_image(self, sys.argv[self.current_arg_index]),
        update_edges_and_pixbuf(self),
        update_lines(self),
    ),
    Gdk.KEY_N: lambda self, _: (
        setattr(
            self,
            "current_arg_index",
            adjust_value(self.current_arg_index, 1, False, 1),
        ),
        prepare_image(self, sys.argv[self.current_arg_index]),
        update_edges_and_pixbuf(self),
        update_lines(self),
    ),
    Gdk.KEY_q: lambda self, _: Gtk.main_quit(),
}
# -------------------------------------------------------
# Mouse Button
# -------------------------------------------------------
button_actions = {
    (
        Gdk.EventType.BUTTON_PRESS,
        Gdk.BUTTON_PRIMARY,
    ): lambda self, _: (
        setattr(self, "colors", [self.colors[-1]] + self.colors[:-1]),
        setattr(self, "line_text_color", self.colors[1]),
        setattr(self, "stats_text_color", self.colors[1]),
        setattr(self, "line_color", self.colors[0]),
    ),
    (Gdk.EventType.BUTTON_PRESS, Gdk.BUTTON_SECONDARY): lambda self, event: (
        setattr(self, "stats_pos", [int(event.x), int(event.y)]),
        live_colors(self),
    ),
}
# -------------------------------------------------------
# Scroll events
# -------------------------------------------------------
scroll_actions = {
    (
        Gdk.EventType.SCROLL,
        (Gdk.ModifierType.MOD1_MASK | Gdk.ModifierType.LOCK_MASK),
    ): lambda self, event: (
        setattr(
            self,
            "font_size",
            adjust_value(
                self.font_size,
                self.step_size,
                event.direction == Gdk.ScrollDirection.UP,
                0,
            ),
        )
    ),
    (Gdk.EventType.SCROLL, Gdk.ModifierType.MOD1_MASK): lambda self, event: (
        setattr(
            self,
            "stats_font_size",
            adjust_value(
                self.stats_font_size,
                self.step_size,
                event.direction == Gdk.ScrollDirection.UP,
                0,
            ),
        )
    ),
    (
        Gdk.EventType.SCROLL,
        (Gdk.ModifierType.SHIFT_MASK | Gdk.ModifierType.LOCK_MASK),
    ): lambda self, event: (
        setattr(
            self,
            "offset",
            [
                adjust_value(
                    self.offset[0],
                    self.step_size,
                    event.direction == Gdk.ScrollDirection.UP,
                ),
                self.offset[1],
            ],
        )
    ),
    (Gdk.EventType.SCROLL, Gdk.ModifierType.SHIFT_MASK): lambda self, event: (
        setattr(
            self,
            "offset",
            [
                self.offset[0],
                adjust_value(
                    self.offset[1],
                    self.step_size,
                    event.direction == Gdk.ScrollDirection.UP,
                ),
            ],
        )
    ),
    (
        Gdk.EventType.SCROLL,
        (Gdk.ModifierType.CONTROL_MASK | Gdk.ModifierType.LOCK_MASK),
    ): lambda self, event: (
        setattr(
            self,
            "lower_threshold",
            adjust_value(
                self.lower_threshold,
                self.step_size,
                event.direction == Gdk.ScrollDirection.UP,
                0,
                self.upper_threshold - 1,
            ),
        ),
        setattr(
            self,
            "edges",
            cv2.Canny(self.gray, self.lower_threshold, self.upper_threshold),
        ),
        update_lines(self),
    ),
    (Gdk.EventType.SCROLL, Gdk.ModifierType.CONTROL_MASK): lambda self, event: (
        setattr(
            self,
            "upper_threshold",
            adjust_value(
                self.upper_threshold,
                self.step_size,
                event.direction == Gdk.ScrollDirection.UP,
                self.lower_threshold + 1,
            ),
        ),
        setattr(
            self,
            "edges",
            cv2.Canny(self.gray, self.lower_threshold, self.upper_threshold),
        ),
        update_lines(self),
    ),
}
