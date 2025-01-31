from yta_api.dataclasses import Response
from yta_audio.voice.transcription import DefaultTimestampedAudioTranscriptor
from yta_audio.voice.generation import GoogleVoiceNarrator
from yta_general_utils.temp import create_temp_filename
from yta_general_utils.downloader import Downloader
from fastapi.responses import JSONResponse, FileResponse
from fastapi import APIRouter


PREFIX = 'audio'

router = APIRouter(
    prefix = f'/{PREFIX}'
)

@router.get('/narrate')
def route_narrate_text(text: str):
    voice_narration_filename = GoogleVoiceNarrator.narrate(text)

    return FileResponse(voice_narration_filename)

@router.get('/transcribe')
def route_transcribe_audio(audio_file_url: str):
    # TODO: Check this to receive files
    # https://fastapi.tiangolo.com/tutorial/request-files/#uploadfile
    # TODO: Check that 'url' is a valid audio path or audio url
    #transcription = get_transcription_text(url)

    transcription = DefaultTimestampedAudioTranscriptor.transcribe(
        Downloader.download_audio(
            audio_file_url,
            output_filename = create_temp_filename('audio.mp3')
        )
    )

    # TODO: Build an specific format to give to our responses
    # TODO: Store information about who made the requested
    # TODO: Limit the amount of requests per user
    # Maybe 'timestamp'

    return JSONResponse(
        content = Response(
            transcription
        )
    )