###Priority Bugs:

#1
Calling .finish() with no parent process causes error
```
Exception in thread Thread-1:
Traceback (most recent call last):
  File "/usr/local/lib/python3.8/site-packages/cap1xxx.py", line 464, in _trigger_handler
    self.handlers[event][channel](CapTouchEvent(channel, event, self.input_delta[channel]))
TypeError: handle() missing 1 required positional argument: 'event'

During handling of the above exception, another exception occurred:

Traceback (most recent call last):
  File "/usr/local/lib/python3.8/threading.py", line 932, in _bootstrap_inner
    self.run()
  File "/usr/local/lib/python3.8/site-packages/cap1xxx.py", line 231, in run
    if self.todo() == False:
  File "/usr/local/lib/python3.8/site-packages/cap1xxx.py", line 457, in _poll
    self._handle_alert()
  File "/usr/local/lib/python3.8/site-packages/cap1xxx.py", line 450, in _handle_alert
    self._trigger_handler(x, inputs[x])
  File "/usr/local/lib/python3.8/site-packages/cap1xxx.py", line 466, in _trigger_handler
    self.handlers[event][channel](channel, event)
  File "/home/traspi/core/render/screen.py", line 44, in handle
    result = func()
  File "/home/traspi/programs/weather/weather.py", line 50, in press
    self.window.finish()
  File "/home/traspi/core/render/window.py", line 45, in finish
    parent, generator = Screen().call_lost()
  File "/home/traspi/core/render/screen.py", line 28, in call_lost
    return self.callstack.pop()
IndexError: pop from empty list
```
#2
Frame 'Burn In Effect' when changing window focus
