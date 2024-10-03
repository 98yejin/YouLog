import string
import dearpygui.dearpygui as dpg
from tkinter import Tk, filedialog
from api.youtube_api import search_videos
from api.transcript_api import fetch_video_transcript
from api.ai_api import transform_script_to_blog
from utils.helpers import get_global_state, set_global_state

def sanitize_filename(filename):
    valid_chars = f"-_.() {string.ascii_letters}{string.digits}"
    return ''.join(c for c in filename if c in valid_chars)

def save_script_callback(sender, app_data, user_data):
    script = get_global_state('current_script')
    if not script:
        show_modal("Error", "No script available to download.")
        return

    file_path = app_data['file_path_name']
    if file_path:
        try:
            with open(file_path, 'w', encoding='utf-8') as file:
                file.write(script)
            show_modal("Success", f"Script saved successfully to:\n{file_path}")
        except Exception as e:
            print(f"Error saving script: {e}")
            show_modal("Error", "Failed to save the script.")

def download_script():
    script = get_global_state('current_script')
    video_title = get_global_state('current_video_title')

    if not script:
        show_modal("Error", "No script available to download.")
        return

    # Sanitize the video title for the file name
    sanitized_title = sanitize_filename(video_title)
    default_filename = f"{sanitized_title}_script" if video_title else "script.txt"

    # Configure the file dialog with the default filename
    dpg.configure_item("save_file_dialog", default_filename=default_filename)
    dpg.show_item("save_file_dialog")

def show_modal(title, message):
    with dpg.window(label=title, modal=True, no_title_bar=False, tag="modal_window"):
        dpg.add_text(message)
        dpg.add_separator()
        dpg.add_button(label="OK", width=75, callback=lambda: dpg.delete_item("modal_window"))

def save_api_keys():
    youtube_api_key = dpg.get_value("youtube_api_key")
    ai_api_key = dpg.get_value("ai_api_key")
    if not youtube_api_key:
        show_modal("Error", "Please enter your YouTube API key.")
        return
    set_global_state('youtube_api_key', youtube_api_key)
    set_global_state('ai_api_key', ai_api_key)
    show_modal("Success", "API keys saved successfully!")

def search_youtube():
    query = dpg.get_value("search_query")
    youtube_api_key = get_global_state('youtube_api_key')
    if not youtube_api_key:
        show_modal("Error", "YouTube API key not provided.")
        return

    # Show a loading modal or message
    show_modal("Searching", "Please wait while we search for videos with transcripts...")

    # Perform the search
    video_items = search_videos(query, youtube_api_key)

    # Close the loading modal
    if dpg.does_item_exist("modal_window"):
        dpg.delete_item("modal_window")

    if video_items:
        dpg.configure_item("video_list", items=video_items)
    else:
        show_modal("No Results", "No videos with transcripts were found for your search.")
        dpg.configure_item("video_list", items=[])

def select_video(sender, app_data):
    selected_video = app_data
    video_id = selected_video.split('(')[-1].rstrip(')')
    video_title = selected_video.rsplit('(', 1)[0].strip()
    set_global_state('current_video_title', video_title)

    script = fetch_video_transcript(video_id)
    if script:
        set_global_state('current_script', script)
        set_global_state('current_blog_post', None)  # Reset previous blog post
        update_content_display()
        dpg.enable_item("download_script_button")  # Enable the download button
    else:
        show_modal("Error", "Transcript not available for this video.")
        dpg.disable_item("download_script_button")  # Disable the download button

def toggle_display():
    update_content_display()

def update_content_display():
    display_mode = dpg.get_value("display_mode")
    script = get_global_state('current_script')
    ai_api_key = get_global_state('ai_api_key')
    if display_mode == "Script":
        dpg.set_value("content_display", script)
    elif display_mode == "Blog Post":
        if ai_api_key:
            blog_post = get_global_state('current_blog_post')
            if not blog_post:
                blog_post = transform_script_to_blog(script, ai_api_key)
                set_global_state('current_blog_post', blog_post)
            dpg.set_value("content_display", blog_post)
        else:
            dpg.set_value("content_display", "AI API key not provided. Cannot generate blog post.")
