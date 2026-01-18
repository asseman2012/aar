#!/usr/bin/env python3
"""
Extraire l'audio d'une vidéo et transcrire/traduire en français
"""
import subprocess
import sys

video_path = '/mnt/c/Users/asseman/Documents/web/chantier/renovation-site/assets/video/videoplayback.mp4'

# Essayer d'extraire l'audio
try:
    print("Extraction de l'audio...")
    # On va essayer avec moviepy
    from moviepy.editor import VideoFileClip
    
    video = VideoFileClip(video_path)
    duration = video.duration
    print(f"Durée vidéo: {int(duration)} secondes ({int(duration/60)} minutes)")
    
    # Extraire l'audio
    audio = video.audio
    audio_path = '/mnt/c/Users/asseman/Documents/web/chantier/renovation-site/assets/video/audio.wav'
    audio.write_audiofile(audio_path, verbose=False, logger=None)
    print(f"Audio extrait: {audio_path}")
    
except ImportError:
    print("moviepy n'est pas installé")
    print("On va essayer avec ffmpeg...")
    try:
        subprocess.run(['ffmpeg', '-i', video_path, '-q:a', '9', '-n', '-acodec', 'libmp3lame', '-ab', '192k', 
                       '/mnt/c/Users/asseman/Documents/web/chantier/renovation-site/assets/video/audio.mp3'],
                      check=True)
        print("Audio extrait avec ffmpeg")
    except:
        print("ffmpeg non disponible")
        sys.exit(1)
