from gui.layout import create_main_window
import dearpygui.dearpygui as dpg

def main():
    create_main_window()
    dpg.start_dearpygui()

if __name__ == "__main__":
    main()
