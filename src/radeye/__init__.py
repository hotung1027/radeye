""" ComPort Format
| SPI communication     | Channel   | Phase     | Atten + Gain      | Ex-Gain |
-------------------------------------------------------
| 1-4 -   Address       | 1-4       | 0-127     | 0x80 + 0-127      | 0-127   |
| 5 - LED Blink         | -         | -         | -                 | -       |
| 6 - Polarization      | -         | -         | -                 | -       |
"""
FILTER_KEYWORDS = "STMicroelectronics"
DATA_FORMAT = [
     "spi",
     "channel",
     "phase",
     "gain",
     "exgain"
     
]
TERMINATOR = "\r"