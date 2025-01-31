## Setup

### MacOS
1. Install `brew install portaudio`

## Sources
- https://github.com/davabase/whisper_real_time/tree/master
- https://github.com/openai/whisper/discussions/608

## Examples
```python
from src import Settings
from src.recording_device import RecordingDevice
from src.whisper_worker import WhisperWorker

def transcription_callback(text: str, result: dict) -> None:
    print(result)

args = Settings.load("settings.yaml")
print("Using settings: ")
print(args)

recording_device = RecordingDevice(args.mic_settings)
whisper_worker = WhisperWorker(
    args.whisper_worker,
    recording_device,
)

print("Model loaded.\n")
whisper_worker.listen(transcription_callback)
```