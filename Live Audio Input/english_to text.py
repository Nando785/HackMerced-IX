from time import sleep
from filter_dupes import filter_dupes

from deepgram import (
    DeepgramClient,
    DeepgramClientOptions,
    LiveTranscriptionEvents,
    LiveOptions,
    Microphone,
)

old_sentence: str = ""

DEEPGRAM_API_KEY='e3253007cc1e3ebb12bbfe496cc555443927cd99'
DEEPGRAM_PROJECT_ID='9b4268d0-d465-439b-a31f-b52582a1e562'

def main():
    try:
        deepgram: DeepgramClient = DeepgramClient(DEEPGRAM_API_KEY)

        dg_connection = deepgram.listen.live.v("1")

        def on_message(self, result, **kwargs):
            sentence = result.channel.alternatives[0].transcript
            if len(sentence) == 0:
                return
            global old_sentence
            filter_dupes(old_sentence, sentence)
            old_sentence = sentence

        dg_connection.on(LiveTranscriptionEvents.Transcript, on_message)

        options: LiveOptions = LiveOptions(
            model="nova-2",
            punctuate=True,
            language="es-US",
            encoding="linear16",
            channels=1,
            sample_rate=16000,
            # To get UtteranceEnd, the following must be set:
            interim_results=True,
            utterance_end_ms="1000",
            vad_events=True,
            diarize=True
        )
        dg_connection.start(options)

        # Open a microphone stream on the default input device
        microphone = Microphone(dg_connection.send)

        # start microphone
        microphone.start()

        # wait until finished
        input("Press Enter to stop recording...\n\n")

        # Wait for the microphone to close
        microphone.finish()

        # Indicate that we've finished
        dg_connection.finish()

        print("Finished")

    except Exception as e:
        print(f"Could not open socket: {e}")
        return


if __name__ == "__main__":
    main()
