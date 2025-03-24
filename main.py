import os
import asyncio
from google.cloud import speech
from microphone_stream import MicrophoneStream
from dotenv import load_dotenv  # Import dotenv to load .env variables

# Load environment variables from .env
load_dotenv()

# Get the API credentials from the environment
GOOGLE_CREDENTIALS = os.getenv("GOOGLE_APPLICATION_CREDENTIALS")

# Ensure credentials are set
if not GOOGLE_CREDENTIALS:
    raise ValueError("GOOGLE_APPLICATION_CREDENTIALS is not set in .env file!")

# Set Google Cloud credentials for authentication
os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = "C:\\Users\\NiaRa\\OneDrive\\Documents\\mykey.json"


async def listen_print_loop(responses):
    for response in responses:
        if not response.results:
            continue
        for result in response.results:
            if result.is_final:
                print(f"Final transcript: {result.alternatives[0].transcript}")

async def main():
    client = speech.SpeechClient()
    config = speech.RecognitionConfig(
        encoding=speech.RecognitionConfig.AudioEncoding.LINEAR16,
        sample_rate_hertz=16000,
        language_code="en-US",
    )
    streaming_config = speech.StreamingRecognitionConfig(config=config, interim_results=True)

    with MicrophoneStream(16000, 1600) as stream:
        audio_generator = stream.generator()
        requests = (speech.StreamingRecognizeRequest(audio_content=chunk) for chunk in audio_generator)
        responses = client.streaming_recognize(streaming_config, requests)

        await listen_print_loop(responses)

if __name__ == "__main__":
    asyncio.run(main())
