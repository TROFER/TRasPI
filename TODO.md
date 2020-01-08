## Bugs

Weird thing that happens when changing windows
/command centre button press twice
When power.py attempts to stop the renderer it stops but then resumes with no backlight and messed up version of the home screen
When the system encounters an error it will resume on home but with no backlight

## Features
New GUI for music player, includes scrolling text, volume controls (Being reworked)
Add message when os restarts after an error example message: "OS error"
General polish of menus and programs, add features not added initially:
  *Tweak graphics on program menu* -Improve visuals (Custom program icons?), Vertically centre programs to better fit page
  *backlight system changes* -Hoeme.py and Program menu should pull their colours from the system default in sys.cfg, pre-installed programs should use this too
  *Sorting and Length Indicators on program menu* -Similar to the menu single
  *Torch opens to torch by default* -Remove menu completely? Navigate with left/right buttons
  *weather service logs changes conditions*
  *System settings is useful* -Link to command centre and integrate contrast values into core settings, program start screen should have its own window design.

##High Priority
Freeze / Pause renderer to save power
Fix some threads not closing when renderer is ended
Fix performance worsening substantially when the OS has errored multiple times

#Low Priority
Make programs use a .cfg file which can be edited using settings
Move cursor image file from music player assets to system assets
Noticed slight drop in rendering performance??? - Might need to make a benchmarking script

# Feature Ideas, Please Ignore
Web interface
Camera
Clock Application, includes digital and analogue face(s), timer, alarm and stopwatch -Acts a Low power standby mode?
Pong? 

#Future changes
Make base branch of Traspi which has no pre installed programs
Include custom loadout for personal use #includes Programs
