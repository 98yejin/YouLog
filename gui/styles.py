import dearpygui.dearpygui as dpg

def set_theme():
    # Create a new theme
    with dpg.theme() as global_theme:
        # Apply theme to all items
        with dpg.theme_component(dpg.mvAll):
            # Set the background color to light gray
            dpg.add_theme_color(dpg.mvThemeCol_WindowBg, (0, 0, 0, 255))

    # Apply the theme globally
    dpg.bind_theme(global_theme)
