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
    

# Examples #

## scripts/merge_channels.py ##

Before you start, enter your server settings (hostname, username, password) in ```scripts/__init__.py``` file.

A small demonstration of the api to create a merged channel:

- Lookup the channels by entering the name
- select the channels you want to merge
- enter the name and channel number of the new merged channel
- optional: disable old channels

### Usage ###

In your ```htsp``` virtualenv call:

    python ~/src/python-htspclient/scripts/merge_channels.py
    

