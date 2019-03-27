
from colormath.color_objects import sRGBColor, LabColor
from colormath.color_conversions import convert_color


class Colors(object):

    @classmethod
    def lab_from_pygame_tuple(kls, color):
        rgb = sRGBColor(color[0], color[1], color[2], is_upscaled=True)
        return convert_color(rgb, LabColor)

    @classmethod
    def lighter(kls, color, pct):
        co = kls.lab_from_pygame_tuple(color)
        co.lab_l = co.lab_l * (1.0+pct)
        return convert_color(co, sRGBColor).get_upscaled_value_tuple()

    @classmethod
    def darker(kls, color, pct):
        co = kls.lab_from_pygame_tuple(color)
        co.lab_l = co.lab_l * (1.0-pct)
        return convert_color(co, sRGBColor).get_upscaled_value_tuple()
