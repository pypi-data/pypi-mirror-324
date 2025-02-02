from dataclasses import dataclass

import conversationalspacemapapp.Types.Constants as Constants


@dataclass
class ParticipantOptions:
    name: str
    type: Constants.Participant
    label: str
    color: str


@dataclass
class PlotOptions:
    def __init__(
        self,
        app,
        title="Conversational Map Space",
        show_title=True,
        labels=True,
        interviewer_label="Interviewer",
        interviewee_label="Interviewee",
        yaxis=True,
        xaxis=True,
        grid=True,
        legend=True,
    ):
        assert app.has_parser
        self.map = app.parser.map
        self.participants: list[ParticipantOptions] = self._get_participants(app)

        self.title = title
        self.show_title = show_title
        self.labels = labels
        self.interviewer_label = interviewer_label
        self.interviewee_label = interviewee_label
        self.yaxis = yaxis
        self.xaxis = xaxis
        self.grid = grid
        self.legend = legend

    def _get_participant(self, participant_name: str):
        for participant in self.participants:
            if participant.name == participant_name:
                return participant

    def get_participant_color(self, participant_name: str) -> str:
        return self._get_participant(participant_name).color

    def get_participant_label(self, participant_name: str) -> str:
        return self._get_participant(participant_name).label

    def get_participant_type(self, participant_name: str) -> Constants.Participant:
        return self._get_participant(participant_name).type

    @staticmethod
    def _get_participants(app) -> list[ParticipantOptions]:
        participants = app.parser.participants
        output = []
        for participant in participants:
            output.append(
                ParticipantOptions(
                    name=participant,
                    type=app._get_participant_role(participant),
                    label=app._get_participant_name(participant),
                    color=app._get_participant_color(participant),
                )
            )
        return output


@dataclass
class Utterance:
    number: int
    speaker: str
    words: int

    def __lt__(self, other):
        return self.number < other.number
