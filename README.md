# What is this? #

Outsourced python code of [tvheadend](https://github.com/tvheadend/tvheadend) to create a reusable HTSP client library for python.

# Goals #

- some improvements regarding HTSP communication between a python HTSPClient and an TVHeadend instance
- understanding the powerful TVHeadend API
- example script files

# Installation #

Install from source:

    cd ~/src/
    git clone https://github.com/tvheadend/python-htspclient
    
Install virtualenv:

    virtualenv htsp
    cd htsp
    bin/activate
    source bin/activate
    pip install -e ~/src/python-htspclient/
    

# Setup #

Before you start, enter your server settings (hostname, username, password) in ```scripts/__init__.py``` file or
create a config.json file inside your venv folder to avoid changing the ```scripts/__init__.py``` file after each update:

```
import json
with open('config.json', 'w') as cfile:
    CONFIG = {'hostname': 'myhostname', 'username': 'mysuername', 'password': 'mypassword'}
    json.dump(CONFIG, cfile)
    cfile.close()
```

# Examples #

## scripts/merge_channels.py ##

A small demonstration of the api to create a merged channel:

- Lookup the channels by entering the name
- select the channels you want to merge
- enter the name and channel number of the new merged channel
- optional: disable old channels

### Usage ###

In your ```htsp``` virtualenv run:

    python ~/src/python-htspclient/scripts/merge_channels.py
    
## scripts/map_channelnumbers.py ##

Update channelnumbers based on a list:

- List item can be
  - a str with the channel name, i.e. "Channel 123" or
  - a list with 2 items ["channel query", "service query"]
  - use the "EXACT"-Flag to match exact names

### Usage ###

First, edit the channel list in ```map_channelnumbers.py```! 

*Your current settings will be overridden.*

In your ```htsp``` virtualenv run:

    python ~/src/python-htspclient/scripts/map_channelnumbers.py
