import pyqtgraph as pg
from colors import Colors

class Curve(pg.PlotCurveItem):
    def __init__(self, GUI_channel):
        super().__init__()
        color = Colors().get_color(GUI_channel)
        self.setPen(color=tuple(color), connect="finite", width=1)


class Trigger(pg.InfiniteLine):

    def __init__(self, GUI_channel):
        super().__init__()
        self.setAngle(0)
        color = Colors().get_color(GUI_channel)
        self.setPen(color=tuple(color))

    def set_value(self, value):
        try:
            self.setValue(value)
        except TypeError:
            pass
            """for external trigger there is not threshold, the value
            of threshold in that case is 'not_available'"""
        except Exception as e:
            print(type(e))


class PlotMine():

    def __init__(self, ui):
        self.curves = {}
        self.trigger = None
        self.graphics_view = ui.graphicsView
        font_size = 12
        label_style = {'color': '#FFF', 'font-size': str(font_size)+'px'}
        self.graphics_view.setLabel('left', units='V', **label_style)
        self.graphics_view.setLabel('bottom', units='s', **label_style)

        self.graphics_view.setRange(yRange=[-10, 10])

    def add_channel(self, GUI_channel):
        curve = Curve(GUI_channel)
        self.curves[GUI_channel] = curve
        self.graphics_view.addItem(curve)

    def remove_channel(self, GUI_channel):
        curve = self.curves[GUI_channel]
        self.graphics_view.removeItem(curve)
        del self.curves[GUI_channel]

    def add_trigger(self, GUI_channel):
        """y=[1,1,1,1,1]
        pg.plot(y, pen=pg.mkPen('b', width=5))"""
        self.trigger = Trigger(GUI_channel)
        self.graphics_view.addItem(self.trigger)

    def remove_trigger(self):
        try:
            self.graphics_view.removeItem(self.trigger)
            self.trigger = None
        except:
            print("Cannot remove trigger")
