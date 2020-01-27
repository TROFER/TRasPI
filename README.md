# TRasPi Operating System
Raspberry Pi code

For a list of future changes see TODO.odt 

# Scripting Guide

## Main
All programs **must** have a *main.py* file inside their folder, if this is not provided the program manager will not detect it an assume it to be a package.

## core.std...
Programs can use the inbuilt standard windows, these provide features such as data input as well as standardised error, warning and information windows.

All programs **must** *yield* to change the current window, the function must also call an *@core.render.Window.focus* when defined

### core.std.menu
Takes two arguments, elements and title


#### elements
elements *type: tuple*, must contain a render element in addition to a data and selection argument

`elements.append(core.std.Menu.Element(
                core.element.Text(core.Vector(0, 0), "Example Label", justify="L"),
                data = label_data,
                select = write_code))`

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


# Setup


