# TRasPI
Raspberry Pi code

Roadmap:
https://trello.com/b/GIqJAKub/gcse-computer-science-corsework

# Scripting Guide

### Main
All scripts **must** contain a *main* function as an entry point.  
* Optionally, it can take arguments (note: keyword arguments are not supported)  

#### core.std

### std.menu
Takes a list of items, callable objects and runs or returns the selected item

### std.error
Takes a message argument and displays it

### std.warning
Takes a message argument and displays it

### std.info
Takes a message argument and displays it

#### Config
The Config files can be read through *core.config*:  

* core.config.load(filename)  
	*returns the dictionary of the filename*  
	*default filename is core.cfg*
* core.config.cfg  
	*contains the dictionary of the last opened config file (note: this can be overridden my other modules)*  


### Storage
Scripts should be located in *programs* folder in the main directory.  


### Setting up the GFX-hat
The script on the pimoroni git hub page are bugged with dietpi and wont actually enable the SPI Bus this is paramount for the use of the LCD and must be enabled manually by editing the config file to avoid errors
