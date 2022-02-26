# rpi4_locator
Attempts to gently scrape rpilocator for available Raspberry Pi 4s. By default runs continuously every 30 minutes. *PLEASE* be nice when interacting with the rpilocator site and do not be overly aggressive.

## Options
_-n, --not-continuous_: only run once, then exit\
_-i, --interval_: interval, in seconds, of when it will check the website\
_-u, --usa-usa_: only check the US region, but will include other Raspberry Pi types other than the model 4B (see errata)

## To Do
- Spin out a thread to monitor keyboard for exit and proper teardown.

## Errata
- rpilocator.com renders rows after each "Support this site" message with an HTML error; specifically, it closes the table row 
then continues to create columns.

- While the scraper could filter down arbitrarily by interacting with the JS filter field, I'm not sure it's worth building out the necessary JavaScript interaction engine for scraping purposes in this particular case.
