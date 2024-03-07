# This file is part of pixruler.
#
# Copyright (c) 2024 Sahil
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

import cairo
import sys
import numpy as np
import cv2
import pyscreenshot
import gi
gi.require_version('Gtk', '3.0')
gi.require_version('GdkPixbuf', '2.0')
from gi.repository import Gtk, GdkPixbuf, Gdk

class ScreenCaptureWindow(Gtk.Window):

    def __init__(self):
        Gtk.Window.__init__(self, title="PixRuler")
        self.connect('realize', lambda widget: self.get_window().set_cursor(
            Gdk.Cursor.new_for_display(
                Gdk.Display.get_default(), Gdk.CursorType.BLANK_CURSOR
            )
        ))
        # Default values
        self.STEP_SIZE_FOUR = 4    
        self.STEP_SIZE_ONE = 1
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
            (1, 1, 0)   # Yellow
        ]
        self.cursor_pos = [0, 0]
        self.text_pos = [0, 0]
        self.line_endpoints = []
        self.stats_pos = [100, 100]
        self.lower_threshold = 50
        self.upper_threshold = 70       

        # Capture the screen
        if len(sys.argv) > 1:
           self.current_arg_index = 1
           self.prepare_image(sys.argv[self.current_arg_index]) 
        else:
            self.img = pyscreenshot.grab()
            # Convert to OpenCV format
            self.img = np.array(self.img)

        self.update_edges_and_pixbuf()

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
        self.connect('scroll-event', self.on_scroll)
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
        self.update_lines()
  

    def on_draw(self, widget, cr):
        # Draw the GdkPixbuf
        Gdk.cairo_set_source_pixbuf(cr, self.pixbuf, 0, 0)
        cr.paint()
        cr.set_line_width(self.line_thickness)
        total_len_y=0
        total_len_x=0   
        line_name = 'INITIALIZE'
        line_clr = self.colors[0]
        text_clr = self.colors[1]
        for i, (start, end) in enumerate(zip([self.cursor_pos] * 4, self.line_endpoints)):
            cr.set_source_rgb(*line_clr)
            cr.move_to(start[0], start[1])
            cr.line_to(end[0], end[1])
            cr.stroke()
            length = cv2.norm(np.array(end) - np.array(start))
            self.text_pos[0] = (start[0] + end[0]) // 2 + self.offset[0]
            self.text_pos[1] = (start[1] + end[1]) // 2 + self.offset[1]
            if start[0] == end[0]:  # Vertical line
                line_name = '-y' if start[1] < end[1] else 'y'
                total_len_y += length
            elif start[1] == end[1]:  # Horizontal line
                line_name = 'x' if start[0] < end[0] else '-x'
                total_len_x += length

            cr.set_source_rgb(*text_clr)
            cr.set_font_size(self.font_size)

            if length > self.TEXT_DISPLAY_THRESHOLD + self.font_size :
                cr.move_to(self.text_pos[0], self.text_pos[1])
                cr.show_text(f'{line_name} ({length:.0f}px)')

            cr.set_font_size(self.stats_font_size)
            cr.move_to(self.stats_pos[0], self.stats_pos[1] + self.stats_font_size * i * 2)
            cr.show_text(f'{line_name} ({length:.0f}px)')

        cr.set_font_size(self.stats_font_size)
        cr.move_to(self.stats_pos[0], self.stats_pos[1] + self.stats_font_size * 8)
        cr.show_text(f'Cursor Position: {self.cursor_pos}')
        cr.move_to(self.stats_pos[0], self.stats_pos[1] + self.stats_font_size * 10)
        cr.show_text(f'Total Length Y: {total_len_y:.0f}px')
        cr.move_to(self.stats_pos[0], self.stats_pos[1] + self.stats_font_size * 12)   
        cr.show_text(f'Total Length X: {total_len_x:.0f}px')
        cr.move_to(self.stats_pos[0], self.stats_pos[1] + self.stats_font_size * 14)   
        cr.show_text(f'Lower Threshold: {self.lower_threshold}')
        cr.move_to(self.stats_pos[0], self.stats_pos[1] + self.stats_font_size * 16)
        cr.show_text(f'Upper Threshold: {self.upper_threshold}')

    
    def on_motion_notify(self, widget, event):
        self.cursor_pos = [int(event.x), int(event.y)]
        self.update_lines()
        self.queue_draw()


    def on_button_press(self, widget, event):  
        right_click_pressed = event.type == Gdk.EventType.BUTTON_PRESS and event.button == 3
        left_click_pressed = event.type == Gdk.EventType.BUTTON_PRESS and event.button == 1
        if right_click_pressed:   
            self.stats_pos[0] = int(event.x) 
            self.stats_pos[1] = int(event.y)
        if left_click_pressed:
            self.colors = [self.colors[-1]] + self.colors[:-1]
        self.queue_draw()


    def on_scroll(self, widget, event):
        if event.direction == Gdk.ScrollDirection.SMOOTH:
            return
        control_pressed = event.state & Gdk.ModifierType.CONTROL_MASK
        alt_pressed = event.state & Gdk.ModifierType.MOD1_MASK
        shift_pressed = event.state & Gdk.ModifierType.SHIFT_MASK
        caps_lock_pressed = event.state & Gdk.ModifierType.LOCK_MASK
        is_increase = event.direction == Gdk.ScrollDirection.UP
        if caps_lock_pressed:
            if alt_pressed:
                self.font_size = self.adjust_value(self.font_size, self.STEP_SIZE_ONE, is_increase, 0)
            elif shift_pressed:
                self.offset[0] = self.adjust_value(self.offset[0], self.STEP_SIZE_FOUR, is_increase)
            elif control_pressed:
                self.lower_threshold = self.adjust_value(self.lower_threshold,
                                                         self.STEP_SIZE_ONE,
                                                         is_increase, 0, self.upper_threshold - 1)
                self.edges = cv2.Canny(self.gray, self.lower_threshold, self.upper_threshold)
                self.update_lines()
            else:
                self.line_thickness = self.adjust_value(self.line_thickness, 0.2, is_increase, 0.7)
        else:
            if alt_pressed:
                self.stats_font_size = self.adjust_value(self.stats_font_size, 1, is_increase, 0)
            elif shift_pressed:
                self.offset[1] = self.adjust_value(self.offset[1], self.STEP_SIZE_FOUR, is_increase)
            elif control_pressed:
                self.upper_threshold = self.adjust_value(self.upper_threshold,
                                                         self.STEP_SIZE_ONE,
                                                         is_increase, self.lower_threshold + 1)
                self.edges = cv2.Canny(self.gray, self.lower_threshold, self.upper_threshold)
                self.update_lines()
        self.queue_draw()


    def on_key_press(self, widget, event):
        control_pressed = event.state & Gdk.ModifierType.CONTROL_MASK
        alt_pressed = event.state & Gdk.ModifierType.MOD1_MASK
        step_size = self.STEP_SIZE_FOUR
        if alt_pressed and control_pressed:
            step_size *= 24 
        elif control_pressed:
            step_size *= 16
        elif alt_pressed:
            step_size *= 8
        
        if event.keyval == Gdk.KEY_Return:
            screen = pyscreenshot.grab()
            screen.save("screenshot.png")
        elif event.keyval == Gdk.KEY_h:
            self.cursor_pos[0] = self.adjust_value(self.cursor_pos[0], step_size, False, 0)
            self.update_lines()
        elif event.keyval == Gdk. KEY_k:
            self.cursor_pos[1] = self.adjust_value(self.cursor_pos[1], step_size, False, 0)
            self.update_lines()
        elif event.keyval == Gdk.KEY_j:
            self.cursor_pos[1] = self.adjust_value(self.cursor_pos[1], step_size, True, 0, self.img.shape[0] - 1)
            self.update_lines()
        elif event.keyval == Gdk.KEY_l:
            self.cursor_pos[0] = self.adjust_value(self.cursor_pos[0], step_size, True, 0, self.img.shape[1] - 1)
            self.update_lines()
        elif event.keyval == Gdk.KEY_H:
            self.stats_pos[0] = self.adjust_value(self.stats_pos[0], step_size, False, 0)
        elif event.keyval == Gdk.KEY_K:
            self.stats_pos[1] = self.adjust_value(self.stats_pos[1], step_size, False, 0)
        elif event.keyval == Gdk.KEY_J:
            self.stats_pos[1] = self.adjust_value(self.stats_pos[1], step_size, True, 0)
        elif event.keyval == Gdk.KEY_L:
            self.stats_pos[0] = self.adjust_value(self.stats_pos[0], step_size, True, 0)
        elif event.keyval == Gdk.KEY_t:
            self.line_thickness = self.adjust_value(self.line_thickness, 0.2, True, 0.7)
        elif event.keyval == Gdk.KEY_T:
            self.line_thickness = self.adjust_value(self.line_thickness, 0.2, False, 0.7)
        elif event.keyval == Gdk.KEY_f:
            self.font_size = self.adjust_value(self.font_size, step_size, True, 0)
        elif event.keyval == Gdk.KEY_F:
            self.font_size = self.adjust_value(self.font_size, step_size, False, 0)
        elif event.keyval == Gdk.KEY_s:
            self.stats_font_size = self.adjust_value(self.stats_font_size, 1, True, 0)
        elif event.keyval == Gdk.KEY_S:
            self.stats_font_size = self.adjust_value(self.stats_font_size, 1, False, 0)
        elif event.keyval == Gdk.KEY_o:
            self.offset[0] = self.adjust_value(self.offset[0], step_size, True)
        elif event.keyval == Gdk.KEY_O:
            self.offset[0] = self.adjust_value(self.offset[0], step_size, False)
        elif event.keyval == Gdk.KEY_p:
            self.offset[1] = self.adjust_value(self.offset[1], step_size, True)
        elif event.keyval == Gdk.KEY_P:
            self.offset[1] = self.adjust_value(self.offset[1], step_size, False)
        elif event.keyval == Gdk.KEY_c:
            self.colors = [self.colors[-1]] + self.colors[:-1]
        elif event.keyval == Gdk.KEY_r:
            self.lower_threshold = self.adjust_value(self.lower_threshold,
                                                     step_size, True, 0, self.upper_threshold - 1)
            self.edges = cv2.Canny(self.gray, self.lower_threshold, self.upper_threshold)
            self.update_lines()
        elif event.keyval == Gdk.KEY_R:
            self.lower_threshold = self.adjust_value(self.lower_threshold,
                                                     step_size, False, 0, self.upper_threshold - 1)
            self.edges = cv2.Canny(self.gray, self.lower_threshold, self.upper_threshold)
            self.update_lines()
        elif event.keyval == Gdk.KEY_u:
            self.upper_threshold = self.adjust_value(self.upper_threshold, step_size, True)
            self.edges = cv2.Canny(self.gray, self.lower_threshold, self.upper_threshold)
            self.update_lines()
        elif event.keyval == Gdk.KEY_U:
            self.upper_threshold = self.adjust_value(self.upper_threshold,
                                                     step_size, False, self.lower_threshold + 1)
            self.edges = cv2.Canny(self.gray, self.lower_threshold, self.upper_threshold)
            self.update_lines()
        elif event.keyval == Gdk.KEY_n:
            if len(sys.argv) > 1:
               self.current_arg_index += 1
               if self.current_arg_index >= len(sys.argv):
                    self.current_arg_index = 1
               self.prepare_image(sys.argv[self.current_arg_index])
            self.update_edges_and_pixbuf()
        elif event.keyval == Gdk.KEY_N:
            if len(sys.argv) > 1:
               self.current_arg_index -= 1
               if self.current_arg_index < 1:
                    self.current_arg_index = len(sys.argv) - 1
               self.prepare_image(sys.argv[self.current_arg_index])
               self.update_edges_and_pixbuf()
        elif event.keyval == Gdk.KEY_q:
            Gtk.main_quit()
        self.queue_draw()


    def update_edges_and_pixbuf(self):
            # Convert the image to grayscale & Enhance contrast using histogram equalization
            self.gray = cv2.equalizeHist(cv2.cvtColor(self.img, cv2.COLOR_RGB2GRAY))
            # Detect edges using Canny
            self.edges = cv2.Canny(self.gray, self.lower_threshold, self.upper_threshold)
            # Convert OpenCV image to GdkPixbuf
            height, width, channels = self.img.shape
            self.pixbuf = GdkPixbuf.Pixbuf.new_from_data(self.img.tobytes(), GdkPixbuf.Colorspace.RGB,
                                                    False, 8, width, height, width * channels, None, None)
            self.update_lines()  


    def prepare_image(self, img):  
       geometry=Gdk.Monitor.get_geometry(Gdk.Display.get_default().get_monitor(0))
       self.screen_width = geometry.width
       self.screen_height = geometry.height 
       self.img = cv2.imread(img)   
       self.img = cv2.resize(self.img, (self.screen_width, self.screen_height))
       self.img = cv2.cvtColor(self.img, cv2.COLOR_BGR2RGB)


    def adjust_value(self, value, step, increase=True, min_value=None, max_value=None):
        if increase:
            value += step
        else:
            value -= step
        if min_value is not None:
            value = max(min_value, value)
        if max_value is not None:
            value = min(max_value, value)
        return value


    def update_lines(self):
       # Update line endpoints based on cursor position and detected border
       self.line_endpoints = [(self.cursor_pos[0], 0),  # Line from cursor to top border
                         # Line from cursor to bottom border
                         (self.cursor_pos[0], self.img.shape[0] - 1),
                         (0, self.cursor_pos[1]),  # Line from cursor to left border
                         (self.img.shape[1] - 1, self.cursor_pos[1])]  # Line from cursor to right border

       # Update line lengths based on edge detection
       for i, (start, end) in enumerate(zip([self.cursor_pos] * 4, self.line_endpoints)):
           has_edge, new_end = self.detect_edge_along_line(start, end, self.edges)
           if has_edge:
               self.line_endpoints[i] = new_end


    def detect_edge_along_line(self, start, end, edges):
        """Detect if an edge exists along the line."""
        # Calculate the distance between start and end points
        distance = cv2.norm(np.array(end) - np.array(start))

        # Generate points along the line
        points = np.linspace(start, end, int(distance))

        # Check for edge in the path
        for point in points:
            x, y = point.astype(int)
            if edges[y, x] > 0:
                return True, (x, y)  # Return True and the position of the edge
        return False, end  # Return False if no edge is detected


if __name__ == "__main__":
    win = ScreenCaptureWindow()
    Gtk.main()

