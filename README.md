# ddg-tracker
Generate a tracker list based on DuckDuckGos web crawler: https://github.com/duckduckgo/tracker-radar/. Ported from https://github.com/ngrande/ddg-tracker.

# System requirements
1. Python 3.6 or above. Tested with Python 3.8.
2. Git

# Offline use
To use this script offline, pull the [tracker-radar repo](https://github.com/duckduckgo/tracker-radar/). point `path` to the domains dir. run `generate.py`.

# Cron job script
At ddg-cron.sh. An example command would be: `./ddg-cron.sh -g '/Users/abhishek/Documents/work/ddg-tracker/generate.py' -f '2' -o '/tmp/final_output.txt'`.

# Hosted list
You can also integrate a hosted flavour directly into piHole from here: https://scripts.deydasapps.com/ddg-tracker/ddg-tracker.txt. The list is updated daily.
