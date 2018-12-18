# TRasPI
Raspberry Pi code

Roadmap:
https://trello.com/b/19Trr3Vm/raspberry-pi-development

# Scripting Guide

### Main
Alls scripts **must** contain a *main* function as an entry point.  
* Optionly, it can take arguments (note: keyword arguments are not supported)  

### Modules

#### Logging
The logging module can be accessed through *core.log*:  

* log = core.log.name("My Logger")  
	*creates a named logger*  
* log.err("My logging message")  
	*uses the named logger*  
* core.log.err("my log without the name")  
	*does not use a name*  
	
#### Config
The Config files can be read through *core.config*:  

* core.config.load(filename)  
	*returns the dictionary of the filename*  
* core.config.cfg  
	*contains the dictionary of the last opened config file (note: this can be overridden my other modules)*  

### Storage
Scripts should be located in *programs* folder in the main directory.  
