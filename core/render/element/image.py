class Image(Primative):

    def __init__(self, anchor, just_w='C', just_h=None):
        super().__init__()
        self.image, self.just_w, self.just_h = image, just_w, just_h
        self.anchor = anchor
        self.pos = self._offset()

    def render(self):
        # ASK TOM

    def copy(self):
        return self.pos, self.just_w, self.just_h

    def _offset(self):
        img_w, img_h = self.image_size()
        pos = []
        if self.just_w == 'R':
            pos[0] = self.anchor[0] - img_w
        elif self.just_w == 'L':
            pos[0] = self.anchor[0]
        else:
            pos[0] = self.anchor[0] - (img_w // 2)

        if self.just_h == 'B':
            pos[1] = self.anchor[1] + img_h
        elif self.just_h == 'T':
            pos[1] = self.anchor[1]
        else:
            pos[1] = self.anchor[1] + (img_h // 2)
        return pos

    def image_size(self):
        return  # IMAGE SIZE
