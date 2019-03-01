# TRasPI
Raspberry Pi code

Roadmap:
https://trello.com/b/19Trr3Vm/raspberry-pi-development

#Code Versions
The development branch contains code that likely wont work, however if you want to see the latest additions and changes please do so.

# Scripting Guide

### Main
All scripts **must** contain a *main* function as an entry point.  
* Optionally, it can take arguments (note: keyword arguments are not supported)  

### Modules

#### Logging
The logging module can be accessed through *core.log*:  

* log = core.log.name("My Logger")  
	*creates a named logger*  
* log.err("My logging message")  
	*uses the named logger*  
* core.log.err("my log without the name")  
	*does not use a name*  
* core.log.level(_num **or** name_)  
	*the global  logging level (can be the name of the level or an int)*

#### Config
The Config files can be read through *core.config*:  

* core.config.load(filename)  
	*returns the dictionary of the filename*  
	*default filename is core.cfg*
* core.config.cfg  
	*contains the dictionary of the last opened config file (note: this can be overridden my other modules)*  

### Storage
Scripts should be located in *programs* folder in the main directory.  

### Using the backlight on the GFX-halt
Warning: The RGB values sent to the backlight must be kept under 100 per colour
*Example 100,0,0 or 100,0,100*
Using values over 100 will cause some high pitched noise from the screen likely due to winey chokes on the board itself

### Setting up the GFX-hat
The script on the pimoroni git hub page are bugged with dietpi and wont actually enable the SPI Bus this is paramount for the use of the LCD and must be enabled manually by editing the config file to avoid errors
