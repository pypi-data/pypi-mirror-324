import abc
import pathlib
from typing import Callable

import conversationalspacemapapp.Types.Constants as Constants
import conversationalspacemapapp.Parser.TimestampParser as TranscriptParser


class AbstractApp(metaclass=abc.ABCMeta):
    """
    Generate conversational space maps for interview data.
    """

    save_file_formats = ["PDF", "PNG", "SVG"]

    def __init__(self, **kwargs):
        self.parser: TranscriptParser.AbstractParser = None
        self.map = None
        super(AbstractApp, self).__init__(**kwargs)

    @property
    def path(self) -> pathlib.Path | None:
        return pathlib.Path(__file__)

    def path_as_str(self):
        if self.has_path:
            return self.path.as_posix()
        else:
            return ""

    @property
    def has_path(self):
        return self.path is not None

    @property
    def has_parser(self):
        return self.parser is not None

    def _create_window(self):
        home = self._create_home_layout()
        transcript = self._create_transcript_layout()
        about = self._create_about_layout()
        tab_menu = self._create_tab_menu(
            tabs=[["Home", home], ["Transcript", transcript], ["About", about]]
        )
        self._set_window(tab_menu)

    @abc.abstractmethod
    def _set_window(self, tab_menu):
        raise NotImplementedError

    @abc.abstractmethod
    def _create_tab_menu(self, tabs):
        raise NotImplementedError

    def _create_home_layout(self):
        plot_settings = self._create_plot_settings_layout()
        participants = self._create_initial_participants_layout()
        label = self._create_info_layout()
        chart = self._create_chart()
        return self._set_home_window(plot_settings, participants, label, chart)

    @abc.abstractmethod
    def _set_home_window(self, plot_settings, participants, label, chart):
        raise NotImplementedError

    @abc.abstractmethod
    def _create_plot_settings_layout(self):
        raise NotImplementedError

    @abc.abstractmethod
    def _create_initial_participants_layout(self):
        raise NotImplementedError

    @abc.abstractmethod
    def _create_participants_layout(self):
        assert self.has_path

    @abc.abstractmethod
    def _create_participant_layout(self, participant: str):
        raise NotImplementedError

    @abc.abstractmethod
    def _create_info_layout(self):
        raise NotImplementedError

    @abc.abstractmethod
    def _set_info_layout(self):
        raise NotImplementedError

    @abc.abstractmethod
    def _create_chart(self):
        raise NotImplementedError

    @abc.abstractmethod
    def _create_transcript_layout(self):
        raise NotImplementedError

    @abc.abstractmethod
    def _set_transcript(self, content: str):
        raise NotImplementedError

    @abc.abstractmethod
    def _create_about_layout(self):
        raise NotImplementedError

    @abc.abstractmethod
    def draw_chart(self, chart, figure, *args, **kwargs):
        raise NotImplementedError

    @abc.abstractmethod
    def _button_factory(
        self,
        label: str,
        on_press: Callable,
        enabled: bool = True,
        padding: int = None,
        flex: int = None,
    ):
        raise NotImplementedError

    @abc.abstractmethod
    def _set_transparent_background(self):
        raise NotImplementedError

    async def open_handler(self, widget):
        path = await self._get_path()
        if path is not None and path.is_file():
            self._set_path(path)
        else:
            return

    @abc.abstractmethod
    async def _get_path(self) -> pathlib.Path | None:
        raise NotImplementedError

    @abc.abstractmethod
    def _set_path(self, path: pathlib.Path):
        raise NotImplementedError

    def _write_file_history(self):
        assert self.has_path
        history = pathlib.Path(__file__).parent / "assets" / "history.txt"
        content = self.path_as_str()
        if not self._is_new_history_path():
            return
        elif history.is_file():
            with open(history, "a") as f:
                f.write(content + "\n")
        else:
            history.parent.mkdir(exist_ok=True, parents=True)
            with open(history, "w") as f:
                f.write(content + "\n")

    def plot_handler(self, widget):
        assert self.has_parser
        self._update_plot()
        self._set_info_layout()

    @abc.abstractmethod
    def _update_plot(self):
        raise NotImplementedError

    async def save_handler(self, widget):
        assert self.has_parser
        path = await self._get_save_path()
        if path is not None:
            self.map.save(path)
        else:
            return

    @abc.abstractmethod
    async def _get_save_path(self) -> pathlib.Path | None:
        raise NotImplementedError

    def _get_info_content(self):
        assert self.has_parser
        total_words = sum(utterance.words for utterance in self.parser.map)
        text = f"Total words: {total_words} / "
        for participant in self.parser.participants:
            participant_words = sum(
                utterance.words if participant == utterance.speaker else 0
                for utterance in self.parser.map
            )
            text += f"Words {participant}: {participant_words} ({round(100 * participant_words / total_words, ndigits=1)}%) / "
        text += f"Total utterances: {len(self.parser.map)}"
        return text

    @abc.abstractmethod
    def _set_plot_title(self):
        raise NotImplementedError

    def _set_parser(self, widget=None):
        assert self.has_path
        self.parser = TranscriptParser.TimestampParser(self.path)
        self._create_participants_layout()
        self._set_plot_title()
        self._update_plot()
        self._set_info_layout()
        self._set_transcript(self.parser.content)
        self._write_file_history()

    @staticmethod
    def _get_file_history() -> [pathlib.Path]:
        history = pathlib.Path(__file__).parent / "assets" / "history.txt"
        if history.is_file():
            with open(history, "r") as f:
                output = []
                files = sorted(f.readlines())
                for file in files:
                    file = file.strip("\n")
                    file = pathlib.Path(file)
                    if file.is_file() and not file in output:
                        output.append(file)
                return output
        else:
            return []

    @abc.abstractmethod
    def _is_new_history_path(self) -> bool:
        raise NotImplementedError

    @abc.abstractmethod
    def _get_widget_value_by_id(self, key: str, default_value=None):
        raise NotImplementedError

    def _get_participant_role(self, speaker_name: str) -> Constants.Participant:
        role_key = speaker_name + "_role"
        if speaker_name in self.parser.participants:
            return self._get_widget_value_by_id(
                role_key, default_value=Constants.Participant.Undefined
            )
        return Constants.Participant.Undefined

    def _get_participant_color(self, speaker_name: str) -> str | None:
        color_key = speaker_name + "_color"
        if speaker_name in self.parser.participants:
            return self._get_widget_value_by_id(color_key)
        return None

    def _get_participant_name(self, speaker_name: str) -> str | None:
        name_key = speaker_name + "_name"
        if speaker_name in self.parser.participants:
            return self._get_widget_value_by_id(name_key)
        return None
