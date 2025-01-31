from dataclasses import dataclass

from textual.widgets import Select, Switch


@dataclass
class SettingRow:
    key: str
    label: str
    widget: Select | Switch
