import dearpygui.dearpygui as dpg
from gui.callbacks import save_api_keys, save_script_callback, search_youtube, select_video, toggle_display, download_script
from gui.styles import set_theme

def create_main_window():
    dpg.create_context()
    dpg.create_viewport(title='YouLog :: YouTube Script', width=800, height=600)
    set_theme()

    with dpg.window(label="Main Window", tag="main_window"):
        dpg.add_text("Welcome to the YouTube Script to Blog Converter!")
        dpg.add_input_text(label="YouTube API Key", tag="youtube_api_key", password=True)
        dpg.add_input_text(label="AI API Key (Optional)", tag="ai_api_key", password=True)
        dpg.add_button(label="Save API Keys", callback=save_api_keys)

        dpg.add_separator()
        dpg.add_input_text(label="Search YouTube", tag="search_query")
        dpg.add_button(label="Search", callback=search_youtube)
        dpg.add_listbox(items=[], label="Video List", tag="video_list", num_items=10, callback=select_video)

        dpg.add_separator()
        dpg.add_button(label="Download Script", callback=download_script, tag="download_script_button")
        dpg.disable_item("download_script_button")  # Initially disabled

        dpg.add_separator()
        dpg.add_text("Content Display")
        dpg.add_radio_button(items=["Script", "Blog Post"], label="Display Mode", tag="display_mode", default_value="Script", callback=toggle_display)
        dpg.add_input_text(multiline=True, label="", tag="content_display", height=200, width=750)

    with dpg.file_dialog(
        directory_selector=False,
        show=False,
        callback=save_script_callback,
        tag="save_file_dialog",
        file_count=1,
        width=700,
        height=400,
        default_filename=""
    ):
        dpg.add_file_extension("Text Files (*.txt){.txt}", color=(0, 255, 0, 255))
        dpg.add_file_extension("All Files (*.*){.*}")
        
    dpg.setup_dearpygui()
    dpg.show_viewport()
