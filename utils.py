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

# utils.py
# contains the utility functions used in the main application.

import numpy as np
import cv2
import gi
import os
import pyscreenshot

gi.require_version("Gtk", "3.0")
gi.require_version("GdkPixbuf", "2.0")
from gi.repository import Gtk, GdkPixbuf, Gdk


def live_colors(self):
    if not self.is_live_colors:
        return
    x, y = self.cursor_pos
    r, g, b = 1 - self.img[y][x] / 255
    self.line_color = (r, g, b)
    self.line_text_color = (r, g, b)
    x, y = self.stats_pos
    r, g, b = 1 - self.img[y][x] / 255
    self.stats_text_color = (r, g, b)


def update_edges_and_pixbuf(self):
    # Convert the image to grayscale & Enhance contrast using histogram equalization
    self.gray = cv2.equalizeHist(cv2.cvtColor(self.img, cv2.COLOR_RGB2GRAY))
    # Detect edges using Canny
    self.edges = cv2.Canny(self.gray, self.lower_threshold, self.upper_threshold)
    # Convert OpenCV image to GdkPixbuf
    height, width, channels = self.img.shape
    self.pixbuf = GdkPixbuf.Pixbuf.new_from_data(
        self.img.tobytes(),
        GdkPixbuf.Colorspace.RGB,
        False,
        8,
        width,
        height,
        width * channels,
        None,
        None,
    )


def prepare_image(self, img):
    geometry = Gdk.Monitor.get_geometry(Gdk.Display.get_default().get_monitor(0))
    screen_width = geometry.width
    screen_height = geometry.height
    self.img = cv2.imread(img)
    self.img = cv2.resize(self.img, (screen_width, screen_height))
    self.img = cv2.cvtColor(self.img, cv2.COLOR_BGR2RGB)


def adjust_value(value, step, increase=True, min_value=None, max_value=None):
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
    self.line_endpoints = [
        (self.cursor_pos[0], 0),  # Line from cursor to top border
        # Line from cursor to bottom border
        (self.cursor_pos[0], self.img.shape[0] - 1),
        (0, self.cursor_pos[1]),  # Line from cursor to left border
        (self.img.shape[1] - 1, self.cursor_pos[1]),
    ]  # Line from cursor to right border

    # Update line lengths based on edge detection
    for i, (start, end) in enumerate(zip([self.cursor_pos] * 4, self.line_endpoints)):
        has_edge, new_end = detect_edge_along_line(start, end, self.edges)
        if has_edge:
            self.line_endpoints[i] = new_end


def detect_edge_along_line(start, end, edges):
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


def save_screenshot():
    base_filename = "screenshot.png"
    count = 0
    while True:
        # Check if the file exists
        if os.path.exists(base_filename):
            count += 1
            base_filename = f"screenshot_{count:02}.png"  # Padded count
        else:
            # Save the screenshot with the unique filename
            pyscreenshot.grab().save(base_filename)
            break
