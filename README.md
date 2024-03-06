# xpt2046-touchcontroller-py

A simple touch controller compatible with the [fbcp-ili9341](https://github.com/juj/fbcp-ili9341) display driver, designed for Raspberry Pi and tested with the [4.0inch SPI Module ST7796](http://www.lcdwiki.com/4.0inch_SPI_Module_ST7796) and Raspberry Pi Zero W. This controller utilizes the auxiliary SPI wiring of the Raspberry Pi.
You will need a touch screen with a xpt2046 chipset.

## How to Use

1. Ensure `fbcp-ili9341` is set up and running with a compatible display.
2. Modify the screen size in `calibrate.py` (line 14) to match your display: `surfaceSize = (480, 320)`.
3. Modify the screen size in `demo.py` (line 18) to match your display: `surfaceSize = (480, 320)`.
4. Run the calibration script: `python3 calibrate.py`
   - Press each circle for two seconds to register the location.
5. Enjoy by running the demo script: `python3 demo.py`

## Wiring

Connect the Raspberry Pi to the XPT2046 as follows:

| Raspberry Pi      | XPT2046 |
| ----------------- | ------- |
| SCLK_1 (GPIO21)   | CLK     |
| CE_1 (GPIO17)     | CS      |
| MOSI_1 (GPIO20)   | DIN     |
| MISO_1 (GPIO19)   | DO      |
| GPIO26            | IRQ     |

## Missing Features

- A deadzone feature to exclude ghost touch at the border of the touchscreen.
- Clean code improvements are welcome.

Contributions to improve the project are highly appreciated. Please feel free to contribute and improve.
