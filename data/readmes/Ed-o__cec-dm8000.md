HDMI-CEC allows you to control items linked up by HDMI cables using the same remote control.  
So for example if you have a DreamBox (TV / Satellite / Cable box) your TV remote could control the box when you switch to that HDMI port.

The DreamBox DM8000 is (was ?) a great box but as it had a DVI port rather than a HDMI port people have always said HDMI-CEC was not possible.
I have writen this guide and included my script to show with a USB interface like the Pulsa-Eight HDMI-USB plug you can make this work.

#How to setup HDMI CEC commands on a DreamBox DM8000



Set up :

Standard DM8000 (which only has a DVI port not a HDMI) running OpenPli 7.3

Sony Bravia TV (2019 model that does CEC HDMI)

Pulse-eight CEC HDMI usb plug



On the command line install the CEC utils:



opkg install libcec



The kernel driver that turns the HDMI CEC codes (via a fake serial port) into something you can read is not loaded.

you can see this by doing 



ls -l / dev / ttyACM *

You will see no devices



We need to load a module from the kernel. So look in:

ls -l /lib/modules/3.2-dm8000/kernel/drivers/usb/class/

And we see 

cdc-acm.ko



you can load this by doing 

modprobe cdc-acm

to start it on every boot add it to a modules file like :
/etc/modules-load.d/dreambox-dvb-modules-dm8000.conf
Just add a line to the bottom that says :
cdc-acm

now you should see a /dev/ttyACM0 (or similar)


running:
cec-client

will now find the device and show you the commands from the remote (example press the yellow key):

DEBUG: [ 41565] key pressed: F4 (yellow) (74) current(ff) duration(0)



Now a fairly easy script will find these lines and turn them into command in the DM8000.

I couldn't find a direct way of entering commands so I used the webif system.

It is already setup that if you are coming from 127.0.0.1 it will allow commands without logging in.

I ran the web pages through NetTools and caught the remote control codes and turned them into a script.



So as an example - you press 'yellow' and this happens :

"F4(yellow)")
      wget -O /dev/null 'http://127.0.0.1/api/remotecontrol?type=long&command=400'
      ;;


so now you can run it with a command like this :
cec-client | ./cec-dm8000.sh

This can be set to run automatically using a /etc/init.d/cec file
and run that on boot up with :
/etc/rc3.d
ln -s ../init.d/cec S80cec

Notes :
The idea and the layout of the script came from here :
https://raspberrypi.stackexchange.com/questions/82847/detect-tv-remote-buttons-being-pressed-with-cec-client
The libcec did all the rest of the work.  This project just connects the two :)
I use the Pulse-Eight HDMI-CEC to USB plug : https://www.pulse-eight.com/p/104/usb-hdmi-cec-adapter


