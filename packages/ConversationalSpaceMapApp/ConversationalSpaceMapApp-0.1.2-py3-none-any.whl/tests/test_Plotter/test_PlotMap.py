import unittest
import matplotlib
import matplotlib.pyplot as plt

matplotlib.use("Agg")

import utilities

import conversationalspacemapapp.Types.Data as Data
import conversationalspacemapapp.Plotter.PlotMap as PlotMap
import conversationalspacemapapp.App.AbstractApp as AbstractApp
import conversationalspacemapapp.Parser.TimestampParser as TranscriptParser


class TestPlotMap(unittest.TestCase):
    parser: TranscriptParser.AbstractParser
    fig: plt.figure()
    ax: plt.Axes
    app: AbstractApp.AbstractApp

    def setUp(self):
        TestPlotMap.parser = utilities.get_parser_mock()
        TestPlotMap.app = utilities.get_app_mock(parser=TestPlotMap.parser)
        TestPlotMap.fig, TestPlotMap.ax = plt.subplots()

    def tearDown(self):
        TestPlotMap.fig.show()

    def test_bar_plot(self):
        sut = PlotMap.MapBarPlot(
            fig=TestPlotMap.fig,
        )
        sut.plot(Data.PlotOptions(app=TestPlotMap.app))

    def test_bar_plot_no_axes(self):
        sut = PlotMap.MapBarPlot(
            fig=TestPlotMap.fig,
        )
        sut.plot(
            Data.PlotOptions(
                app=TestPlotMap.app,
                xaxis=False,
                yaxis=False,
            )
        )
