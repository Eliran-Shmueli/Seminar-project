import winsound


def click_sound_valid():
    """
    play valid sound on click
    """
    winsound.PlaySound('sounds/mixkit-select-click-1109.wav', winsound.SND_FILENAME | winsound.SND_ASYNC)


def click_sound_exit():
    """
    play exit sound on click
    """
    winsound.PlaySound('sounds/sci-fi-voiceclip-894-sound-effect-goodbye.wav',
                       winsound.SND_FILENAME | winsound.SND_ASYNC)


def click_sound_error():
    """
    play error sound on click
    """
    winsound.PlaySound('sounds/mixkit-click-error-1110.wav', winsound.SND_FILENAME | winsound.SND_ASYNC)