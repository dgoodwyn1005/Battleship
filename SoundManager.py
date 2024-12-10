import pygame
import Constants as C


class Sound(object):
    sounds = {}  # Dictionary to hold all the sound effects
    music = {}  # Dictionary to hold all the music
    play_music = True   # Boolean to determine if music is enabled
    play_sound_effects = True  # Boolean to determine if sound effects are enabled

    def __init__(self, m_vol=100, s_vol=100):
        # Initialize sounds
        pygame.mixer.pre_init(44100, -16, 1, 512)
        pygame.mixer.init()
        self.music_volume = m_vol
        self.sound_effect_volume = s_vol

    def play_sound(self, sound_name):
        """Plays a sound effect by accepting the sound name as a parameter and searching for the sound in the sounds
        dictionary. If the sound is found and sound_effects are enabled, it plays the sound"""
        if Sound.play_sound_effects:
            if sound_name in Sound.sounds:
                Sound.sounds[sound_name].play()

    def play_song(self, song_name):
        """Plays a song by accepting the song name as a parameter and searching for the song in the music dictionary.
        If the song is found and music is enabled, it plays the song"""
        if Sound.play_music:
            if song_name in Sound.music:
                Sound.music[song_name].play(-1)

    def stop_song(self, song_name):
        """Stops the current song that is playing"""
        if song_name in Sound.music:
            Sound.music[song_name].stop()

    def toggle_music(self):
        """Toggle the music varible on and off which will enable or disable the music"""
        Sound.play_music = not Sound.play_music
        
    def toggle_sounds(self):
        """Toggle the sound effects variable on and off which will enable or disable the sound effects"""
        Sound.play_sound_effects = not Sound.play_sound_effects

    @classmethod
    def initialize_sounds(cls):
        """Initialize all the sounds and insert them into the sounds dictionary using the class method. This method
        using the @classmethod decorator in order to be called without creating an instance of the class, since the
        MainMenu Screen does not need to create an instance of the Sound class to initialize the sounds"""
        # Assign the sounds to the sound variables
        explosion_sound = pygame.mixer.Sound(C.AUDIO_FOLDER + "/explosion_sound.wav")
        water_sound = pygame.mixer.Sound(C.AUDIO_FOLDER + "/water_splash_sound.wav")
        button_click_sound = pygame.mixer.Sound(C.AUDIO_FOLDER + "/buttonclick.wav")
        menu = pygame.mixer.Sound(C.AUDIO_FOLDER + "/menu_ambience.mp3")
        conflict = pygame.mixer.Sound(C.AUDIO_FOLDER + "/conflict.ogg")
        victory = pygame.mixer.Sound(C.AUDIO_FOLDER + "/victory.wav")
        lose = pygame.mixer.Sound(C.AUDIO_FOLDER + "/lose.ogg")
        # Add the sounds to the sounds dictionary
        Sound.sounds.update({"explosion": explosion_sound})
        Sound.sounds.update({"splash": water_sound})
        Sound.sounds.update({"click": button_click_sound})
        Sound.music.update({"menu": menu})
        Sound.music.update({"conflict": conflict})
        Sound.music.update({"victory": victory})
        Sound.music.update({"lose": lose})
