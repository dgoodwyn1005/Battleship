import MainMenu as MM
import Display as D

if __name__ == "__main__":
    screen = MM.Main_Menu()
    D.Display.startDisplay(screen, screen.main_loop())
