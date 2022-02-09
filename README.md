# rpi_locator
Attempts to gently scrape rpilocator for available Raspberry Pi 4s. By default runs continuously every 30 minutes. Hit q to quit.

## Options
_-n, --not-continuous_: only run once, then exit
_-i, --interval_: interval, in seconds, of when it will check the website
_-u, --usa-usa_: only check the US region

## To Do
- Spin out a thread to monitor keyboard for exit and proper teardown.