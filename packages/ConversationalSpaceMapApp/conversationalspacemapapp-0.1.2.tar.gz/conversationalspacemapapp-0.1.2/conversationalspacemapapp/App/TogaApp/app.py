import toga
import toga_chart
from toga.style import Pack
from toga.constants import COLUMN

import pathlib
import platform
from typing import Callable

import conversationalspacemapapp.Types.Data as Data
import conversationalspacemapapp.Plotter.PlotMap as PlotMap
import conversationalspacemapapp.Types.Constants as Constants
import conversationalspacemapapp.App.AbstractApp as AbstractApp
import conversationalspacemapapp.Plotter.StylePicker as StylePicker


class ConversationalSpaceMapAppToga(AbstractApp.AbstractApp, toga.App):
    default_padding = 5
    default_flex = 1

    def __init__(self, name, id):
        super(ConversationalSpaceMapAppToga, self).__init__(formal_name=name, app_id=id)

    @property
    def path(self) -> pathlib.Path | None:
        return self.path_input.value

    @property
    def has_path(self):
        return self.path is not None and self.path.is_file()

    @property
    def path_filename(self) -> str | None:
        return str(self.path.name) if self.has_path else None

    @property
    def has_parser(self):
        return self.parser is not None

    def startup(self):
        self._create_window()

    def _set_window(self, tab_menu):
        self.main_window = toga.MainWindow()
        self.main_window.content = tab_menu
        self.main_window.size = toga.Size(width=1300, height=1000)
        self.main_window.show()

    def _create_tab_menu(self, tabs):
        main = toga.OptionContainer(content=tabs)
        self._set_widget_style(main)
        self._set_transparent_background(main)
        return main

    def _create_about_layout(self):
        # Create app description page
        description = toga.WebView(
            url="https://manuelbieri.ch/ConversationalSpaceMapApp/"
        )
        self._set_widget_style(description)
        self._set_transparent_background(description)
        about = toga.Box(
            children=[description],
            style=Pack(direction=COLUMN),
        )
        return about

    def _create_transcript_layout(self):
        self.transcript = toga.MultilineTextInput()
        self._set_widget_style(self.transcript)
        if self.has_parser:
            self.transcript.value = self.parser.content
        else:
            self.transcript.enabled = False
        return self.transcript

    def _set_transcript(self, content: str):
        assert type(content) == str
        self.transcript.value = content

    def _set_home_window(self, plot_settings, participants, label, chart):
        assert plot_settings is not None
        assert participants is not None
        assert label is not None
        assert chart is not None
        return toga.Box(
            children=[plot_settings, participants, label, chart],
            style=Pack(direction=COLUMN),
        )

    def _create_plot_settings_layout(self):
        # Create selections
        self.file_format = toga.Selection(
            items=ConversationalSpaceMapAppToga.save_file_formats
        )
        self._set_widget_style(self.file_format, flex=0)
        self.path_input = toga.Selection(
            items=self._get_file_history(), on_change=self._set_parser
        )
        self._set_widget_style(self.path_input, flex=1)
        self.path_input.readonly = True

        # Create buttons
        self.button = self._button_factory("📄", on_press=self.open_handler)
        self._set_widget_style(self.button, flex=0)
        self.plot = self._button_factory(
            "🖌", on_press=self.plot_handler, enabled=self.has_path
        )
        self._set_widget_style(self.plot, flex=0)
        self.save = self._button_factory(
            "💾", on_press=self.save_handler, enabled=False
        )
        self._set_widget_style(self.save, flex=0)
        plot_settings = toga.Box(
            children=[
                self.path_input,
                self.button,
                self.plot,
                self.file_format,
                self.save,
            ]
        )
        return plot_settings

    def _create_initial_participants_layout(self):
        self.participants_layout = toga.OptionContainer(
            content=[("General", self._create_general_participants_layout())],
            style=Pack(
                padding=ConversationalSpaceMapAppToga.default_padding, height=60
            ),
        )
        return self.participants_layout

    def _create_general_participants_layout(self):
        self.color_palette = self._set_widget_style(
            toga.Selection(
                items=StylePicker.Palette.available_palettes(),
                on_change=self._set_participants_color_selection,
            ),
        )
        self.plot_title = self._set_widget_style(
            toga.Switch(text="Title", on_change=self.plot_handler, value=True), flex=0
        )
        self.plot_title_input = self._set_widget_style(
            toga.TextInput(placeholder="Title"), flex=2
        )
        self.interviewer_label_input = self._set_widget_style(
            toga.TextInput(
                value="Interviewer",
                placeholder="Interviewer label",
                on_change=self.plot_handler,
            )
        )
        self.interviewee_label_input = self._set_widget_style(
            toga.TextInput(
                value="Interviewee",
                placeholder="Interviewee label",
                on_change=self.plot_handler,
            )
        )
        self.plot_legend = self._set_widget_style(
            toga.Switch(text="Legend", on_change=self.plot_handler, value=True), flex=0
        )
        self.plot_labels = self._set_widget_style(
            toga.Switch(text="Labels", on_change=self.plot_handler, value=True), flex=0
        )
        self.plot_yaxis = self._set_widget_style(
            toga.Switch(text="Y-Axis", on_change=self.plot_handler, value=True), flex=0
        )
        self.plot_xaxis = self._set_widget_style(
            toga.Switch(text="X-Axis", on_change=self.plot_handler, value=True), flex=0
        )
        self.plot_grid = self._set_widget_style(
            toga.Switch(text="Grid", on_change=self.plot_handler, value=True), flex=0
        )
        self._general_participants_layout = toga.Box(
            children=[
                self.plot_title_input,
                self.plot_title,
                self.plot_labels,
                self.interviewer_label_input,
                self.interviewee_label_input,
                self.plot_yaxis,
                self.plot_xaxis,
                self.plot_legend,
                self.plot_grid,
                self.color_palette,
            ]
        )
        return self._general_participants_layout

    def _create_info_layout(self):
        self.label = toga.Label("")
        self._set_widget_style(self.label)
        return self.label

    def _set_info_layout(self):
        assert self.has_parser
        self.label.text = self._get_info_content()
        self.label.refresh()

    def _create_chart(self):
        self.chart = toga_chart.Chart(style=Pack(flex=1), on_draw=self.draw_chart)
        self._set_widget_style(self.chart)
        return self.chart

    def _create_participants_layout(self):
        assert self.has_path
        self._clear_participants_layout()
        for participant in self.parser.participants:
            self.participants_layout.content.append(
                participant, self._create_participant_layout(participant)
            )

    def _clear_participants_layout(self):
        self.participants_layout.current_tab = 0
        for _ in range(1, len(self.participants_layout.content)):
            self.participants_layout.content.remove(1)
        assert len(self.participants_layout.content) == 1

    def _create_participant_layout(self, participant: str) -> toga.Box:
        # Create participant role
        role = toga.Selection(
            items=Constants.Participant,
            id=participant + "_role",
            on_change=self.plot_handler,
        )
        self._set_widget_style(role)

        # Create participant name label
        name = toga.TextInput(
            value=participant,
            id=participant + "_name",
            on_change=self.plot_handler,
            placeholder="Speaker name",
        )
        self._set_widget_style(name)

        # Create color picker
        color = toga.TextInput(
            value=self.color_palette.value.value[0],
            id=participant + "_color",
            on_change=self.plot_handler,
            readonly=True,
        )
        self._set_widget_style(color, flex=0)

        widget_container = toga.Box(
            children=[
                role,
                name,
                color,
            ]
        )

        for i in range(8):
            button = self._set_widget_style(
                toga.Button(
                    "   ",
                    id=participant + "_color" + str(i),
                    style=Pack(background_color=self.color_palette.value.value[i]),
                    on_press=lambda e: self._set_participant_color(color, e),
                ),
                flex=0,
            )
            widget_container.add(button)

        return widget_container

    def _set_participants_color_selection(self, e):
        assert self.has_parser
        for participant in self.parser.participants:
            for i in range(8):
                color_button = self._get_widget_by_id(participant + "_color" + str(i))
                color_button.style.background_color = self.color_palette.value.value[i]

    def _set_participant_color(self, color_widget: toga.Widget, index) -> None:
        color_widget.value = StylePicker.ColorPicker.rgb2hex(
            index.style.background_color.r,
            index.style.background_color.g,
            index.style.background_color.b,
        )

    def draw_chart(self, chart: toga_chart.Chart, figure, *args, **kwargs):
        if self.has_parser:
            self.map = PlotMap.MapBarPlot(fig=figure)
            self.map.plot(
                options=Data.PlotOptions(
                    app=self,
                    title=self.plot_title_input.value,
                    show_title=self.plot_title.value,
                    labels=self.plot_labels.value,
                    interviewer_label=self.interviewer_label_input.value,
                    interviewee_label=self.interviewee_label_input.value,
                    yaxis=self.plot_yaxis.value,
                    xaxis=self.plot_xaxis.value,
                    legend=self.plot_legend.value,
                    grid=self.plot_grid.value,
                ),
            )
            figure.tight_layout()
        else:
            return

    def _button_factory(
        self,
        label: str,
        on_press: Callable,
        enabled: bool = True,
        padding: float = None,
        flex: float = None,
    ) -> toga.Button:
        button = toga.Button(label, on_press=on_press)
        button.enabled = enabled
        self._set_widget_style(button, padding=padding, flex=flex)
        return button

    @staticmethod
    def _set_default_widget_flex(widget: toga.Widget) -> toga.Widget:
        widget.style.flex = ConversationalSpaceMapAppToga.default_flex
        return widget

    @staticmethod
    def _set_default_widget_padding(widget: toga.Widget) -> toga.Widget:
        widget.style.padding = ConversationalSpaceMapAppToga.default_padding
        return widget

    @staticmethod
    def _set_widget_style(
        widget: toga.Widget,
        padding: float = None,
        flex: float = None,
    ) -> toga.Widget:
        if padding is None and flex is None:
            ConversationalSpaceMapAppToga._set_default_widget_flex(widget)
            ConversationalSpaceMapAppToga._set_default_widget_padding(widget)
        elif padding is None:
            ConversationalSpaceMapAppToga._set_default_widget_padding(widget)
            widget.style.flex = flex
        elif flex is None:
            ConversationalSpaceMapAppToga._set_default_widget_flex(widget)
            widget.style.padding = padding
        else:
            widget.style.padding = padding
            widget.style.flex = flex
        return widget

    @staticmethod
    def _set_transparent_background(widget):
        if "macOS" in platform.platform():
            widget.style.background_color = "transparent"

    async def _get_path(self):
        file = toga.OpenFileDialog("Open file", file_types=["txt"])
        return await self.main_window.dialog(file)

    def _set_path(self, path: pathlib.Path):
        assert path.is_file()
        try:
            self.path_input.value = path
        except ValueError:
            self.path_input.items.append(path)
            self.path_input.value = path
        self._set_parser()

    def _set_plot_title(self):
        assert self.has_path
        self.plot_title_input.value = "Conversational Space Map " + str(self.path.stem)

    def _update_plot(self):
        self.chart.redraw()
        self.save.enabled = True

    def _is_new_history_path(self) -> bool:
        if self.path in self._get_file_history():
            return False
        return True

    async def _get_save_path(self):
        assert self.has_path
        file = toga.SaveFileDialog(
            "Save file",
            suggested_filename=str(pathlib.Path(self.path).stem),
            file_types=ConversationalSpaceMapAppToga.save_file_formats,
        )
        return await self.main_window.dialog(file)

    def _get_widget_value_by_id(self, key: str, default_value=None):
        widget: toga.Widget = self._get_widget_by_id(key)
        if widget is None:
            return default_value
        return widget.value

    def _get_widget_by_id(self, key: str) -> toga.Widget | None:
        for tab in self.participants_layout.content:
            for child in tab.content.children:
                if child.id == key:
                    return child
        return None


def main():
    return ConversationalSpaceMapAppToga(
        "ConversationalSpaceMapApp", "ch.manuelbieri.conversationalspacemapapp"
    )
