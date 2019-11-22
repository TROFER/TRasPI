# TRasPI
Raspberry Pi code

Roadmap:
https://trello.com/b/19Trr3Vm/raspberry-pi-development

# Scripting Guide

### Main
All scripts **must** contain a *main* function as an entry point.  
* Optionally, it can take arguments (note: keyword arguments are not supported)  

### Modules
*gfx.cleanup()*:
This module clears the backlight or LCD or Both when called. It takes one string argument for specifying which to clear.
Current options: "all" *clears both backlight and LCD* "lcd" *Clears the LCD only* "backlight" *clears the backlight only*

*gfx.menu()*:
This module creates a menu on the GFX hat when called. It takes two arguments *subject to change*, one for identifying the selection and the other for the label text.
Both arguments must be lists and must be strings only

*gfx.image()*:
This module displays a *64x128* *monochrome* *PNG* image on the GFX Hat.
It has one string argument specifying file location.
*note: The path must be in full and include the filename and extension*

*gfx.backlight()*:
This module is pretty pointless at the moment it will eventually provide cool backlight effects.
However at this moment it serves little to no purpose as no code is saved by using it.
It will take one string argument specifying the effect type.
*Example of what it could be like* gfx-backlight("lime") or gfx-backlight("red_orange")

*gfx.touch_led()*:
This module is for turning on and off the LEDs without use of a for loop in your code.
It has one string argument which can be either *"on"* or *"off"*

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

### Example program
	import gfx
	from gfxhat import backlight
	from time import sleep
	print("A simple image selection and display program")

	backlight.set_all(100,100,100) #Sets the backlight to a dim white
	itemid = ["image1","image2","image3","image4","quit"] #These identify an item
	itemlabel = ["Dog","Cat","Mouse","Turtle","quit"] #These will be used as the menu labels

	while quit = False:
			result = gfx.menu(itemid,itemlabel)

			if result == "image1":
			     gfx.image("/os/program_data/cat.png") #This can be anything
					 sleep(5) #Waits 5 seconds before returning to the menu screen

			elif result == "image2":
					 gfx.image("/os/program_data/dog.png")
					 sleep(5)

			elif result == "image3":
					 gfx.image("/os/program_data/mouse.png")
					 sleep(5)

			elif result == "image4":
					 gfx.image("/os/program_data/turtle.png")
					 sleep(5)

			elif result == "quit":
					 quit = True

	gfx.cleanup("all") #Clears the lcd and the backlight
	quit()

### Storage
Scripts should be located in *programs* folder in the main directory.  

### Using the backlight on the GFX-halt
Warning: The RGB values sent to the backlight must be kept under 100 per colour
*Example 100,0,0 or 100,0,100*
Using values over 100 will cause some high pitched noise from the screen likely due to winey chokes on the board itself

### Setting up the GFX-hat
The script on the pimoroni git hub page are bugged with dietpi and wont actually enable the SPI Bus this is paramount for the use of the LCD and must be enabled manually by editing the config file to avoid errors
