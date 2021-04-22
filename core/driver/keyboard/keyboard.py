import keyboard

_map = {
    0: "up",
    1: "down",
    2: "nul",
    3: "left",
    4: "enter",
    5: "right"
}

_bindings = {
    0: None,
    1: None,
    2: None,
    3: None,
    4: None,
    5: None,
}

def bind(button, function):
    try:
        if _bindings[button] is not None:
            keyboard.remove_hotkey(_bindings[button])
        _bindings[button] = keyboard.add_hotkey(
        _map[button], function, args=(button, "press"), trigger_on_release=False)
    except ValueError:
        pass
    except KeyError:
        pass