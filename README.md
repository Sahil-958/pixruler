# PixRuler: A Simple Screen Ruler 

PixRuler is a Python application designed to capture the screen, detect edges in the captured image using the Canny edge detection algorithm, and display the detected edges along with some statistical information.



https://github.com/Sahil-958/pixruler/assets/118348625/e810f5d4-f6d7-442f-a45e-f57615b6a988



## Features

- **Edge Detection**: Applies the Canny edge detection algorithm to detect edges in the captured image.
- **Dynamic Parameter Adjustment**: Allows users to adjust parameters such as thresholds, line thickness, font size, etc., dynamically for better visualization.

## Installation

1. Clone the repository:

```bash
git clone https://github.com/your_username/pixruler.git
cd pixruler
```

2. Setting Up Virtual Environment (Optional):

```bash
python -m venv .
source ./bin/activate
```

3. Install the required dependencies using pip:

```bash
pip install -r requirements.txt
```

4. Run the PixRuler script:

```bash
./bin/python pixruler.py
```

## Usage

1. Run the PixRuler script:

```bash
python pixruler.py
```

2. The application will capture the screen and display the detected edges along with statistical information.

3. Use the mouse to interact with the application:
   - Move the cursor to select points on the screen.
   - Right-click to adjust the position of statistical information.
   - Left-click to cycle through different line colors.
   - Scroll to adjust parameters such as thresholds, line thickness, font size, etc.
      - If `Caps Lock` is on:
          - Scroll to adjust the line thickness.
          - Hold `Ctrl` while scrolling to adjust the lower threshold value. 
          - Hold `Shift` while scrolling to adjust the horizontal text offset.
          - Hold `Alt` while scrolling to adjust the line font size.
      - If `Caps Lock` is off:
          - Hold `Ctrl` while scrolling to adjust the upper threshold value. 
          - Hold `Shift` while scrolling to adjust the vertical text offset.
          - Hold `Alt` while scrolling to adjust the stats font size.


4. Vim-like Keybindings for Parameter Adjustments:

    - **Stats Movement:**
      - `H`: Move statistical information left.
      - `L`: Move statistical information right.
      - `J`: Move statistical information down.
      - `K`: Move statistical information up.

    - **Pointer Movement:**
      - `h`: Move pointer left.
      - `l`: Move pointer right.
      - `j`: Move pointer down.
      - `k`: Move pointer up.

    - **Text Offset:**
      - `o`: Offset text horizontally right.
      - `O`: Offset text horizontally left.
      - `p`: Offset text vertically down.
      - `P`: Offset text vertically up.

    - **Threshold Adjustment:**
      - `R`: Decrease lower threshold value.
      - `r`: Increase lower threshold value.
      - `U`: Decrease upper threshold value.
      - `u`: Increase upper threshold value.

    - **Line and Font Settings:**
      - `T`: Decrease line thickness.
      - `t`: Increase line thickness.
      - `F`: Decrease font size.
      - `f`: Increase font size.
      - `S`: Decrease stats font size.
      - `s`: Increase stats font size.

    - **Other Commands:**
      - `c`: Cycle through different line and text colors.
      - `C`: Toggle Live Color Mode (lines and stats are colored inverted to the
        color below them).
      - `q`: Quit the application.
      - `RETURN`: Takes screenshot and saves it in current directory with name `screenshot.png`.
      - `n`: Switch to next image from the list of images passed as input.
      - `N`: Switch to previous image from the list of images passed as input.

Use above keybinds with `Ctrl` and `Alt` to increase the step size for certain adjustments.

When `Ctrl` is hold the step size is default(4)*16 and when `Alt` is hold the step size is default(1)*8. When both `Ctrl` and `Alt` are hold the step size is default(4)*24.

IF you feel that the keybinds letter's doesn't reflect the action it does, feel free to open an issue to suggest better keybinds.

## Customization

You can customize the application by modifying the following parameters in the `ScreenCaptureWindow` class:

- `STEP_SIZE_FOUR`: Step size for certain adjustments.
- `STEP_SIZE_ONE`: Step size for certain adjustments.
- `font_size`: Default font size for text display.
- `stats_font_size`: Default font size for statistical information.
- `line_thickness`: Default thickness for drawn lines.
- `TEXT_DISPLAY_THRESHOLD`: Threshold for displaying text associated with lines.
- `lower_threshold`: Default lower threshold for Canny edge detection.
- `upper_threshold`: Default upper threshold for Canny edge detection.

## Future Roadmap

- [x] Add support for providing image files as input.
- [x] Add support for saving the detected edges as an image file.
- [x] Add vim-like keybindings for parameter adjustments.
- [x] Add keyboard only usage by removing the need for mouse interaction.
- [ ] Add intuitive GUI for parameter adjustments.
- [ ] Add support for customizing the color palette for detected edges.
- [ ] Add snap-to-shape feature for detected edges of geometric shapes.
- [x] Add support for switching between multiple images passed as input.
- [ ] Refactor the code to improve performance, efficiency, and readability.
- [ ] Refactor code ASAP before it goes out of hand.
- [ ] Add github workflows for releases

## License

This project is licensed under the [GPL-3.0 License](https://www.gnu.org/licenses/gpl-3.0.html).

### Disclaimer

I am relatively new to open-source and licensing and may not fully understand all aspects of licensing. I am not even sure to add a license or not (is this single script even wroth one). While I have made efforts to ensure compliance with the GPL-3.0 License for this project, there may be uncertainties or mistakes. If you have any concerns or notice any issues related to licensing, please feel free to reach out for assistance. Your feedback and guidance are greatly appreciated.

## Acknowledgments

This application was inspired by discussions within the community about the need for a tool to capture the screen and visualize edge detection results. The following sources provided valuable insights:

- [Ubuntu StackExchange Post Regarding Port of Window PowerToys Screen Ruler for Linux](https://askubuntu.com/questions/1435406/intelligent-screen-ruler-for-linux-with-image-edge-detection-alternatiave-for-m)  
- [linuxquestions.org Discussion on ideas for screen ruler on Wayland](https://www.linuxquestions.org/questions/programming-9/ideas-for-screen-ruler-on-wayland-4175704648) 
- [Reddit Post about image viewer with ruler features](https://www.reddit.com/r/software/comments/63ledv/image_viewer_with_ruler_features/) 

## More mature and feature-rich alternatives 

- [xScope](https://xscopeapp.com/) [MacOS] [Proprietary]: A powerful set of tools for measuring, aligning, and inspecting on-screen graphics and layouts.

- [PowerToys](https://github.com/microsoft/PowerToys) [Windows] [Open-Source]: Microsoft PowerToys is a set of utilities for power users to tune and streamline their Windows experience for greater productivity. For more info on [PowerToys overviews and how to use the utilities](https://aka.ms/powertyos-docs) or any other tools and resources for [Windows development environments](https://learn.microsoft.com/windows/dev-environment/overview), head over to [learn.microsoft.com](https://aka.ms/powertoys-docs)!

- [Rooler](https://github.com/peteblois/rooler) [Windows] [Open-Source]: Utilities for pixel-perfect analysis and measurement of graphics. Created for designers to aid common tasks such as redlining and analysis of layouts. Rooler uses the on-screen graphics and can be used for any graphics- from static images to HTML in your browser to the UI of a running application. Rooler was originally inspired by the excellent OSX application [xScope](http://xscopeapp.com/).
    
- [KRuler](https://apps.kde.org/kruler) [Linux] [Open-Source]: KRuler is an on-screen ruler for measuring pixels. Position the 0 at your starting point and measure the precise pixel distance between the starting point and your cursor.
