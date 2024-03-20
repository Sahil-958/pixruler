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

from actions import *
from utils import *
import cairo
import sys
import numpy as np
import cv2
import pyscreenshot
import gi

gi.require_version("Gtk", "3.0")
gi.require_version("GdkPixbuf", "2.0")
from gi.repository import Gtk, GdkPixbuf, Gdk


class ScreenCaptureWindow(Gtk.Window):

    def __init__(self):
        Gtk.Window.__init__(self, title="PixRuler")
        self.connect(
            "realize",
            lambda widget: self.get_window().set_cursor(
                Gdk.Cursor.new_for_display(
                    Gdk.Display.get_default(), Gdk.CursorType.BLANK_CURSOR
                )
            ),
        )

        # Default values
        self.step_size = 1
        self.step_size_mp = 1
        self.font_size = 12
        self.stats_font_size = 12
        self.line_thickness = 1
        self.offset = [0, 0]
        self.TEXT_DISPLAY_THRESHOLD = 80
        self.colors = [
            (1, 0, 0),  # Red
            (0, 1, 0),  # Green
            (0, 1, 1),  # Cyan
            (1, 0, 1),  # Magenta
            (1, 1, 0),  # Yellow
        ]
        self.line_text_color = self.colors[1]
        self.stats_text_color = self.colors[1]
        self.line_color = self.colors[0]
        self.is_live_colors = False
        self.cursor_pos = [0, 0]
        self.text_pos = [0, 0]
        self.line_endpoints = []
        self.stats_pos = [100, 100]
        self.lower_threshold = 50
        self.upper_threshold = 70

        # Capture the screen
        if len(sys.argv) > 1:
            self.arg_count = len(sys.argv)
            self.current_arg_index = 1
            prepare_image(self, sys.argv[self.current_arg_index])
        else:
            self.img = pyscreenshot.grab()
            # Convert to OpenCV format
            self.img = np.array(self.img)

        update_edges_and_pixbuf(self)

        height, width, channels = self.img.shape
        # Center the starting cursor position
        self.cursor_pos = [width // 2, height // 2]
        # Drawing area for displaying the image
        self.drawing_area = Gtk.DrawingArea()
        self.drawing_area.connect("draw", self.on_draw)
        self.add(self.drawing_area)
        # Update cursor position
        self.connect("motion-notify-event", self.on_motion_notify)
        self.add_events(Gdk.EventMask.POINTER_MOTION_MASK)
        self.connect("scroll-event", self.on_scroll)
        self.add_events(Gdk.EventMask.SCROLL_MASK)
        self.connect("button-press-event", self.on_button_press)
        self.add_events(Gdk.EventMask.BUTTON_PRESS_MASK)
        self.connect("key-press-event", self.on_key_press)
        self.add_events(Gdk.EventMask.KEY_PRESS_MASK)
        # Set window properties
        self.fullscreen()
        self.set_keep_above(True)
        self.connect("destroy", Gtk.main_quit)
        self.show_all()
        update_lines(self)

    def on_draw(self, widget, cr):
        # Draw the GdkPixbuf
        Gdk.cairo_set_source_pixbuf(cr, self.pixbuf, 0, 0)
        cr.paint()
        cr.set_line_width(self.line_thickness)
        total_len_y = 0
        total_len_x = 0
        line_name = "INITIALIZE"
        for i, (start, end) in enumerate(
            zip([self.cursor_pos] * 4, self.line_endpoints)
        ):
            cr.set_source_rgb(*self.line_color)
            cr.move_to(start[0], start[1])
            cr.line_to(end[0], end[1])
            cr.stroke()
            length = cv2.norm(np.array(end) - np.array(start))
            self.text_pos[0] = (start[0] + end[0]) // 2 + self.offset[0]
            self.text_pos[1] = (start[1] + end[1]) // 2 + self.offset[1]
            if start[0] == end[0]:  # Vertical line
                line_name = "-y" if start[1] < end[1] else "y"
                total_len_y += length
            elif start[1] == end[1]:  # Horizontal line
                line_name = "x" if start[0] < end[0] else "-x"
                total_len_x += length

            cr.set_source_rgb(*self.line_text_color)
            cr.set_font_size(self.font_size)

            if length > self.TEXT_DISPLAY_THRESHOLD + self.font_size:
                cr.move_to(self.text_pos[0], self.text_pos[1])
                cr.show_text(f"{line_name} ({length:.0f}px)")

            cr.set_source_rgb(*self.stats_text_color)
            cr.set_font_size(self.stats_font_size)
            cr.move_to(
                self.stats_pos[0], self.stats_pos[1] + self.stats_font_size * i * 2
            )
            cr.show_text(f"{line_name} ({length:.0f}px)")

        cr.set_source_rgb(*self.stats_text_color)
        cr.set_font_size(self.stats_font_size)
        cr.move_to(self.stats_pos[0], self.stats_pos[1] + self.stats_font_size * 8)
        cr.show_text(f"Cursor Position: {self.cursor_pos}")
        cr.move_to(self.stats_pos[0], self.stats_pos[1] + self.stats_font_size * 10)
        cr.show_text(f"Total Length Y: {total_len_y:.0f}px")
        cr.move_to(self.stats_pos[0], self.stats_pos[1] + self.stats_font_size * 12)
        cr.show_text(f"Total Length X: {total_len_x:.0f}px")
        cr.move_to(self.stats_pos[0], self.stats_pos[1] + self.stats_font_size * 14)
        cr.show_text(f"Lower Threshold: {self.lower_threshold}")
        cr.move_to(self.stats_pos[0], self.stats_pos[1] + self.stats_font_size * 16)
        cr.show_text(f"Upper Threshold: {self.upper_threshold}")
        cr.move_to(self.stats_pos[0], self.stats_pos[1] + self.stats_font_size * 18)
        cr.show_text(f"Step Size: {self.step_size_mp}")
        cr.move_to(self.stats_pos[0], self.stats_pos[1] + self.stats_font_size * 20)
        cr.show_text(f"Step Size with Multiplier: {self.step_size}")
        cr.move_to(self.stats_pos[0], self.stats_pos[1] + self.stats_font_size * 22)
        cr.show_text(f"Live Color: {self.is_live_colors}")

    def on_motion_notify(self, widget, event):
        self.cursor_pos = [int(event.x), int(event.y)]
        live_colors(self)
        update_lines(self)
        self.queue_draw()

    def on_button_press(self, widget, event):
        action = button_actions.get((event.type, event.button))
        if action:
            action(self, event)
            self.queue_draw()
            return

        self.queue_draw()

    def on_key_press(self, widget, event):
        control_pressed = event.state & Gdk.ModifierType.CONTROL_MASK
        alt_pressed = event.state & Gdk.ModifierType.MOD1_MASK
        self.step_size = self.step_size_mp
        if alt_pressed and control_pressed:
            self.step_size *= 8
        elif control_pressed:
            self.step_size *= 4
        elif alt_pressed:
            self.step_size *= 2

        action = key_actions.get(event.keyval)
        # If no action found for single key value, check for key-value pairs
        if action is None:
            for key in key_actions.keys():
                if isinstance(key, tuple) and event.keyval in key:
                    action = key_actions[key]
                    break

        if action:
            action(self, event)
            self.queue_draw()
            return

    def on_scroll(self, widget, event):
        if event.direction == Gdk.ScrollDirection.SMOOTH:
            return

        action = scroll_actions.get((event.type, event.state))

        if action:
            action(self, event)
            self.queue_draw()
            return


if __name__ == "__main__":
    win = ScreenCaptureWindow()
    Gtk.main()
