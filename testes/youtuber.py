from pytube import YouTube
import os

videoLink = "https://www.youtube.com/watch?v=UcCmyb8bST8"
            #https://youtu.be/rIcf_cToq5c
DEFAULT_PATH = os.path.dirname(__file__)

videoFile = YouTube(videoLink)
videoFile.streams.get_audio_only().download(DEFAULT_PATH)
