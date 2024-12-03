import MainMenu as MM
import SoundManager as SM

SM.initialize_sounds()

if __name__ == "__main__":
    screen = MM.Main_Menu()
    screen.startDisplay(screen.main_loop)
