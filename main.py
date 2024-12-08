import MainMenu as MM
import SoundManager as SM


if __name__ == "__main__":
    SM.Sound.initialize_sounds()   # Initialize all sounds
    screen = MM.Main_Menu()    # Create the main menu screen
    screen.startDisplay(screen.main_loop)  # Start the main menu screen
