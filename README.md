# rpi4_locator
Attempts to gently scrape rpilocator for available Raspberry Pi 4s. By default runs continuously every 30 minutes. Be nice with this!

## Options
_-n, --not-continuous_: only run once, then exit\
_-i, --interval_: interval, in seconds, of when it will check the website\
_-u, --usa-usa_: only check the US region

## To Do
- Spin out a thread to monitor keyboard for exit and proper teardown.

## Errata
- Due to a bug in the way rpilocator.com renders rows after each "Support this site" message, the 
script will skip over the subsequent vendor row. There is a way around it, but it involves a complete  
overhaul in how the script scrapes the page.
