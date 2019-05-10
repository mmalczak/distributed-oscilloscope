class Colors():

    def __init__(self):
        self.colors = [[255, 255, 0], [255, 0, 255], [0, 0, 255],
                       [0, 255, 0], [255, 0, 0], [0, 255, 255]]

    def get_color(self, idx):
        if idx <= 5:
            return self.colors[idx]
        else:
            color = [0, 0, 0]
            color[idx % 3] = 0
            color[(idx + 1) % 3] = (50 * idx) % 255
            color[(idx + 2) % 3] = (255 - 50 * idx) % 255
            return color
