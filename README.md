# telnet-honeypot

This is a simple Telnet Honeypot. It is written in Python. Refer to  [my blog post](https://www.silicontrenches.com/post/telnet-honeypot)
for further details.

## Setup

A Python [Virtual Environment](https://www.pythonforbeginners.com/basics/how-to-use-python-virtualenv) is highly recommended.

Use pip3 to install the dependencies:

    cd telnet-honeypot
    pip3 install -r requirements.txt

Forward port 23 (Telnet) from you Router to port 2327 on the device running this
program.

Create the directory into which captured samples will be placed:

    mkdir samples

## To Run

The Python file should run directly from the command line:

    ./honey.py

Captured samples are renamed to their SHA1 Hash and placed in the "samples" directory.

## CAUTION

This program captures potential Malware sent from the Internet. These files could be
harmful to your computer. Extreme caution should be exercised when handling any
captured samples.

