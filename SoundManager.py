import pygame
import Constants as C

class Sound:
    def __init__(self, m_vol = 100, s_vol = 100):
        #Initialize sounds
        pygame.mixer.init
        self.sounds = {}
        self.music = {}
        self.explosion_sound = pygame.mixer.Sound(C.AUDIO_FOLDER + "/explosion_sound.wav")
        self.water_sound = pygame.mixer.Sound(C.AUDIO_FOLDER + "/water_splash_sound.wav")

        self.conflict = pygame.mixer.Sound(C.AUDIO_FOLDER + "/conflict.ogg")

        self.sounds.update({"explosion": self.explosion_sound})
        self.sounds.update({"splash" : self.water_sound})

        self.music.update({"conflict" : self.conflict})

        self.play_music = True
        self.play_sound_effects = True
        self.music_volume = m_vol
        self.sound_effect_volume = s_vol

    def play_sound(self, sound_name):
        if sound_name in self.sounds:
            self.sounds[sound_name].play()

    def play_song(self, song_name):
        if song_name in self.music:
            self.music[song_name].play(-1)

    def stop_song(self, song_name):
        if song_name in self.music:
            self.music[song_name].stop()

    def toggle_music(self, choice):
        self.play_music = choice

    def toggle_sounds(self, choice):
        self.play_sound_effects = choice
