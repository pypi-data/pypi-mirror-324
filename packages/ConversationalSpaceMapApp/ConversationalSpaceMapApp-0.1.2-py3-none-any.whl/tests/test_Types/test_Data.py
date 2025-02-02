import unittest

import utilities

import conversationalspacemapapp.Types.Data as Data
import conversationalspacemapapp.App.AbstractApp as AbstractApp
import conversationalspacemapapp.Parser.TimestampParser as TranscriptParser


class TestPlotOptions(unittest.TestCase):
    parser: TranscriptParser.AbstractParser
    app: AbstractApp.AbstractApp

    def setUp(self):
        TestPlotOptions.parser = utilities.get_parser_mock()
        TestPlotOptions.app = utilities.get_app_mock(parser=TestPlotOptions.parser)

    def test_plot_options_setup(self):
        sut = Data.PlotOptions(
            app=TestPlotOptions.app,
        )
        speaker00 = sut.participants[0]
        speaker01 = sut.participants[1]
        self.assertEqual(2, len(sut.participants))
        self.assertEqual(utilities.speaker00_name, speaker00.name)
        self.assertEqual(utilities.speaker00_label, speaker00.label)
        self.assertEqual(utilities.speaker00_color, speaker00.color)
        self.assertEqual(utilities.speaker00_type, speaker00.type)
        self.assertEqual(utilities.speaker01_name, speaker01.name)
        self.assertEqual(utilities.speaker01_label, speaker01.label)
        self.assertEqual(utilities.speaker01_color, speaker01.color)
        self.assertEqual(utilities.speaker01_type, speaker01.type)
