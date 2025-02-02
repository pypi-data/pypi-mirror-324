from enum import Enum
import matplotlib as mpl
import matplotlib.colors as mcolors


class ColorPicker:
    COLORS = mcolors.CSS4_COLORS

    @staticmethod
    def rgb2hex(r, g, b):
        return "#" + "".join(f"{i:02X}" for i in (r, g, b))

    @staticmethod
    def pastel():
        return ColorPicker._get_colormap_list("Pastel2")

    @staticmethod
    def accent():
        return ColorPicker._get_colormap_list("Accent")

    @staticmethod
    def set():
        return ColorPicker._get_colormap_list("Set2")

    @staticmethod
    def tab():
        return ColorPicker._get_colormap_list("tab20")

    @staticmethod
    def _get_colormap_list(name: str) -> list:
        cmap = mpl.colormaps.get_cmap(name)
        return [mpl.colors.to_hex(cmap(i)) for i in range(8)]


class Palette(Enum):
    Pastel = ColorPicker.pastel()
    Accent = ColorPicker.accent()
    Set = ColorPicker.set()
    Tab = ColorPicker.tab()

    @staticmethod
    def available_palettes() -> list:
        return [Palette.Accent, Palette.Pastel, Palette.Set, Palette.Tab]

    def __str__(self):
        if self.value == Palette.Pastel.value:
            return "Pastel"
        elif self.value == Palette.Accent.value:
            return "Accent"
        elif self.value == Palette.Set.value:
            return "Set"
        else:
            return "Tab"
