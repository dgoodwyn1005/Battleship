import pygame
import Constants as C

pygame.mixer.pre_init(44100, -16, 1, 512)
pygame.mixer.init()

sounds = {}
music = {}

class Sound:
    def __init__(self, m_vol = 100, s_vol = 100):
        #Initialize sounds
        self.play_music = True
        self.play_sound_effects = True
        self.music_volume = m_vol
        self.sound_effect_volume = s_vol

    def play_sound(self, sound_name):
        if self.play_sound_effects:
            if sound_name in sounds:
                sounds[sound_name].play()

    def play_song(self, song_name):
        if self.play_music:
            if song_name in music:
                music[song_name].play(-1)

    def stop_song(self, song_name):
        if song_name in music:
            music[song_name].stop()

    def toggle_music(self, choice):
        self.play_music = choice

    def toggle_sounds(self, choice):
        self.play_sound_effects = choice


def initialize_sounds():
    explosion_sound = pygame.mixer.Sound(C.AUDIO_FOLDER + "/explosion_sound.wav")
    water_sound = pygame.mixer.Sound(C.AUDIO_FOLDER + "/water_splash_sound.wav")
    buttonclick_sound = pygame.mixer.Sound(C.AUDIO_FOLDER + "/buttonclick.wav")

    menu = pygame.mixer.Sound(C.AUDIO_FOLDER + "/menu_ambience.mp3")
    conflict = pygame.mixer.Sound(C.AUDIO_FOLDER + "/conflict.ogg")
    victory = pygame.mixer.Sound(C.AUDIO_FOLDER + "/victory.wav")
    lose = pygame.mixer.Sound(C.AUDIO_FOLDER + "/lose.ogg")

    sounds.update({"explosion": explosion_sound})
    sounds.update({"splash" : water_sound})
    sounds.update({"click" : buttonclick_sound})

    music.update({"menu" : menu})
    music.update({"conflict" : conflict})
    music.update({"victory" : victory})
    music.update({"lose" : lose})