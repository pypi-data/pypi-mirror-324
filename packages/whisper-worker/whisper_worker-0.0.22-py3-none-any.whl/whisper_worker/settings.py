from dataclasses import dataclass

import yaml
from .mic import MicSettings
from .logging_config import LoggingConfig
from .transcription import TranscribeSettings


@dataclass
class WhisperWorkerSettings:
    record_timeout: float
    phrase_timeout: float
    in_memory: bool
    transcribe_settings: TranscribeSettings

    @classmethod
    def load(cls, data):
        return cls(**data)

    def __post_init__(self):
        self.transcribe_settings = TranscribeSettings.load(self.transcribe_settings)


@dataclass
class Settings:
    whisper_worker: WhisperWorkerSettings
    mic_settings: MicSettings
    logging_config: LoggingConfig | None = None

    @classmethod
    def load(cls, path):
        with open(path, "r") as f:
            data = yaml.safe_load(f)
        return cls(**data)

    def __post_init__(self):
        self.whisper_worker = WhisperWorkerSettings.load(self.whisper_worker)
        self.mic_settings = MicSettings.load(self.mic_settings)
        if self.logging_config:
            self.logging_config = LoggingConfig(**self.logging_config)
