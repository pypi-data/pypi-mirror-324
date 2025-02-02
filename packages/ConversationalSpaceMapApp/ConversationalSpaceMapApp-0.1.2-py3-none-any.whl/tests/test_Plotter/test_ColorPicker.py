import unittest

import conversationalspacemapapp.Plotter.StylePicker as ColorPicker


class TestColorPicker(unittest.TestCase):
    def abstract_test(self, palette, palette_str, pallette_list):
        self.assertEqual(palette.value, pallette_list)
        self.assertEqual(str(palette), palette_str)

    def test_accent(self):
        self.abstract_test(
            ColorPicker.Palette.Accent,
            "Accent",
            [
                "#7fc97f",
                "#beaed4",
                "#fdc086",
                "#ffff99",
                "#386cb0",
                "#f0027f",
                "#bf5b17",
                "#666666",
            ],
        )

    def test_pastel(self):
        self.abstract_test(
            ColorPicker.Palette.Pastel,
            "Pastel",
            [
                "#b3e2cd",
                "#fdcdac",
                "#cbd5e8",
                "#f4cae4",
                "#e6f5c9",
                "#fff2ae",
                "#f1e2cc",
                "#cccccc",
            ],
        )

    def test_set(self):
        self.abstract_test(
            ColorPicker.Palette.Set,
            "Set",
            [
                "#66c2a5",
                "#fc8d62",
                "#8da0cb",
                "#e78ac3",
                "#a6d854",
                "#ffd92f",
                "#e5c494",
                "#b3b3b3",
            ],
        )

    def test_tab(self):
        self.abstract_test(
            ColorPicker.Palette.Tab,
            "Tab",
            [
                "#1f77b4",
                "#aec7e8",
                "#ff7f0e",
                "#ffbb78",
                "#2ca02c",
                "#98df8a",
                "#d62728",
                "#ff9896",
            ],
        )
