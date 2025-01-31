from sys import platform
from dataclasses import dataclass
import speech_recognition


@dataclass
class MicSettings:
    mic_name: str
    sample_rate: int
    energy_threshold: int

    @classmethod
    def load(cls, data):
        return cls(**data)


@dataclass
class Mic:
    settings: MicSettings
    source: speech_recognition.Microphone | None = None

    def __post_init__(self):
        if "linux" in platform:
            print("Available microphone devices are: ")
            for index, name in enumerate(
                speech_recognition.Microphone.list_microphone_names()
            ):
                print(f'Microphone with name "{name}" found')

            for index, name in enumerate(
                speech_recognition.Microphone.list_microphone_names()
            ):
                if self.settings.mic_name in name:
                    self.source = speech_recognition.Microphone(
                        sample_rate=self.settings.sample_rate, device_index=index
                    )
                    print(f"Found target mic: '{self.settings.mic_name}'")
                    break
                
                print(f"Target not found: {self.settings.mic_name}")

        else:
            self.source = speech_recognition.Microphone(
                sample_rate=self.settings.sample_rate
            )