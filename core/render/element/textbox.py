class TextBox(Text):  # ASK TOM

    def __init__(self, anchor, *args, line_col=0, fill=None, width=1, **kwargs):
        self.rect = Rectangle(
            pos-Vector(2, 0), Vector(1, 1), line_col, fill, width)
        super().__init__(anchor, *args, *kwargs)

        def render(self):
            super().render()
            ImageDraw.rectangle(*self.rect)

        def copy(self):
            return self.anchor, self.line_col, self.fill, self.width

        def _offset(self, value: Vector):
            value = super()._offset(value)
            self.rect.pos = value - Vector(2, 0)
            self.rect.pos_2 = self.font_size() + Vector(2, 0)
            return value
