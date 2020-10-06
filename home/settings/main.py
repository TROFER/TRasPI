import core
from .app import App

class Setting(core.std.Menu):

    def __init__(self, config: core.type.Config, settings: list):
        super().__init__(*(self.create_item(setting, config) for setting in settings[1:]), title=settings[0])
        self.config = config

    def create_item(self, setting: core.sys.Setting, config: core.type.Config) -> core.std.Menu.elm:
        if isinstance(setting, core.sys.Setting):
            return self.elm(
                core.element.Text(core.Vector(0, 0), setting.name, justify="L"),
                # core.element.Image(),
                data=setting,
                func=self.edit_value,
            )
        else: # list
            return self.elm(
                core.element.Text(core.Vector(0, 0), setting[0], justify="L"),
                # core.element.Image(),
                data=(config, setting),
                func=self.sub_wrapper,
            )

    async def sub_wrapper(self, data: tuple):
        return await Setting(*data)

    async def edit_value(self, setting: core.sys.Setting):
        if setting.data_type == bool:
            value = await core.std.Query(
                setting.data_kwargs.get("msg", "Set Value"),
                setting.name,
                cancel=True,
            )
        elif setting.data_type == int:
            value = await core.std.Numpad(
                setting.data_kwargs.get("min", -1000),
                setting.data_kwargs.get("max", 1000),
                getattr(self.config, setting.attr),
                setting.name,
            )
        else:
            await core.std.Info("Data Type not Supported")

        if value is not None:
            setattr(self.config, setting.attr, value)

class SettingHome(Setting):

    def __init__(self):
        self.config = core.sys.var
        super(Setting, self).__init__(*(self.create_item(setting, config) for config, setting in self.scan_settings()), title="Settings")

    def scan_settings(self) -> (core.type.Config, core.sys.Setting):
        for name, value in self.config:
            yield (self.config, core.sys.Setting(name, data=type(value)))
        for program in core.interface.application().applications:
            # All open programs - Add closed Programs
            yield (program.application.var, program.application.settings)

class Settings(core.std.Menu):

    def __init__(self, settings):
        self.items = []
        for _setting in settings:
            elements = [Text(core.Vector(0, 0), _setting["name"], justify='L')]
            if isinstance(_setting, list):
                elements.append(Text(core.Vector(128, 0), ">", justify="R"))
                self.items.append(core.std.Menu.elm(*elements, data=_setting["settings"], func=self.NewMenu))
            else:
                self.items.append(core.std.Menu.elm(*elements, data="Value, min max ect ect", func=self.EditValue)) # Add func=numpad or true false ect. 
        super().__init__(*self.items, title="Settings")

    async def NewMenu(self, item):
        await Settings(item)

    async def EditValue(self, item):
        if settting.type == bool:
            res = await core.std.Query()

App.window = SettingHome
main = App