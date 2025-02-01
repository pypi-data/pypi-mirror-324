## Setup
A simple method for using whisper to transcribe audio in real-time.

## Install
```
pip install whisper-worker
```

## Prerequisites

### MacOS
1. Install `brew install portaudio`

## Sources
- https://github.com/davabase/whisper_real_time/tree/master
- https://github.com/openai/whisper/discussions/608

## Examples
```python
from whisper_worker import Settings,RecordingDevice,WhisperWorker

def transcription_callback(text: str, result: dict) -> None:
    print(result)

args = Settings.load("settings.yaml")
logging.info("Using settings: ")
logging.info(args)

# Important for linux users.
# Prevents permanent application hang and crash by using the wrong Microphone
print(args)
recording_device = RecordingDevice(args.mic_settings)
whisper_worker = WhisperWorker(
    args.whisper_worker,
    recording_device,
)

# Cue the user that we're ready to go.
print("Model loaded.\n")
whisper_worker.listen(transcription_callback)

```

The `transcription_callback` function is called when a transcription is completed. 

## Settings

```yml

mic_settings:
  mic_name: "Jabra SPEAK 410 USB: Audio (hw:3,0)" # Linux only
  sample_rate: 16000
  energy_threshold: 3000 # 0-4000

whisper_worker:
  record_timeout: 2 # 0-10
  phrase_timeout: 3 # 0-10
  in_memory: True
  transcribe_settings:
    #  'tiny.en', 'tiny', 'base.en', 'base', 'small.en', 'small', 'medium.en', 'medium', 'large-v1', 'large-v2', 'large-v3', 'large', 'large-v3-turbo', 'turbo'
    model: medium.en

    # Whether to display the text being decoded to the console.
    # If True, displays all the details, If False, displays
    # minimal details. If None, does not display anything
    verbose: True

    # Temperature for sampling. It can be a tuple of temperatures,
    # which will be successively used upon failures according to
    # either compression_ratio_threshold or logprob_threshold.
    temperature: "(0.0, 0.2, 0.4, 0.6, 0.8, 1.0)" # "(0.0, 0.2, 0.4, 0.6, 0.8, 1.0)"

    # If the gzip compression ratio is above this value,
    # treat as failed
    compression_ratio_threshold: 2.4 # 2.4

    # If the average log probability over sampled tokens is below this value, treat as failed
    logprob_threshold: -1.0 # -1.0

    # If the no_speech probability is higher than this value AND
    # the average log probability over sampled tokens is below
    # logprob_threshold, consider the segment as silent
    no_speech_threshold: 0.6 # 0.6

    # if True, the previous output of the model is provided as a
    # prompt for the next window; disabling may make the text
    # inconsistent across windows, but the model becomes less
    # prone to getting stuck in a failure loop, such as repetition
    # looping or timestamps going out of sync.
    condition_on_previous_text: True # True

    # Extract word-level timestamps using the cross-attention
    # pattern and dynamic time warping, and include the timestamps
    # for each word in each segment.
    # NOTE: Setting this to true also adds word level data to the
    # output, which can be useful for downstream processing.  E.g.,
    # {
    #   'word': 'test',
    #   'start': np.float64(1.0),
    #   'end': np.float64(1.6),
    #   'probability': np.float64(0.8470910787582397)
    # }
    word_timestamps: True # False

    # If word_timestamps is True, merge these punctuation symbols
    # with the next word

    prepend_punctuations: '"''“¿([{-'

    # If word_timestamps is True, merge these punctuation symbols with the previous word
    append_punctuations: '"''.。,，!！?？:：”)]}、'

    # Optional text to provide as a prompt for the first window.
    # This can be used to provide, or "prompt-engineer" a context
    # for transcription, e.g. custom vocabularies or proper nouns
    # to make it more likely to predict those word correctly.
    initial_prompt: "" # ""

    # Comma-separated list start,end,start,end,... timestamps
    # (in seconds) of clips to process. The last end timestamp
    # defaults to the end of the file.
    clip_timestamps: "0" # "0"

    # When word_timestamps is True, skip silent periods longer
    # than this threshold (in seconds) when a possible
    # hallucination is detected
    hallucination_silence_threshold: None # float | None

    # Keyword arguments to construct DecodingOptions instances
    # TODO: How can DecodingOptions work?

logging_config:
  level: INFO # DEBUG, INFO, WARNING, ERROR, CRITICAL
  filepath: "talking.log"
  log_entry_format: "%(asctime)s - %(levelname)s - %(message)s"
  date_format: "%Y-%m-%d %H:%M:%S"
```
