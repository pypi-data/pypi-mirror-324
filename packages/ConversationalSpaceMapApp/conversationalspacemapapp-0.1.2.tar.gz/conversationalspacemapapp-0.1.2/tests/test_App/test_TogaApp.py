import unittest
import matplotlib

matplotlib.use("Agg")

import conversationalspacemapapp.App.TogaApp.app as TogaApp
import conversationalspacemapapp.App.AbstractApp as AbstractApp

import tests.TestResources as TestResources


class TestAbstractApp(unittest.TestCase):
    sut: AbstractApp.AbstractApp

    def setUp(self):
        TestAbstractApp.sut = TogaApp.main()
        TestAbstractApp.sut.startup()


class TestTogaApp(TestAbstractApp):
    def test_run(self):
        pass

    def test_plot(self):
        TestAbstractApp.sut._set_path(
            path=TestResources.path_multiple_speaker_transcript
        )
