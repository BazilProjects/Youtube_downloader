import threading
import requests
import webbrowser

from kivy.app import App
from kivy.lang import Builder
from kivy.clock import Clock
from kivy.uix.boxlayout import BoxLayout

KV = '''
<MainScreen>:
    orientation: 'vertical'
    padding: 10
    spacing: 10

    # Navigation Bar (simple header)
    BoxLayout:
        size_hint_y: None
        height: '40dp'
        spacing: 10
        canvas.before:
            Color:
                rgba: .2, .2, .2, 1
            Rectangle:
                pos: self.pos
                size: self.size
        Label:
            text: "YouTube Downloader"
            font_size: '20dp'
            color: 1,1,1,1

    # URL Input and Button
    BoxLayout:
        size_hint_y: None
        height: '50dp'
        spacing: 10
        TextInput:
            id: url_input
            hint_text: "Paste YouTube link"
            multiline: False
            size_hint_x: 0.75
            font_size: '16dp'
        Button:
            text: "Get Links"
            size_hint_x: 0.25
            on_press: root.get_download_links(url_input.text)

    # Video Preview
    Video:
        id: video_player
        source: ""
        state: "stop"
        options: {'eos': 'loop'}
        size_hint_y: 0.4
        opacity: 0  # initially hidden

    # Download Links Section
    ScrollView:
        size_hint_y: 0.3
        GridLayout:
            id: download_links_layout
            cols: 1
            size_hint_y: None
            height: self.minimum_height
            spacing: 5

    # Related Searches Section
    ScrollView:
        size_hint_y: 0.2
        GridLayout:
            id: related_layout
            cols: 1
            size_hint_y: None
            height: self.minimum_height
            spacing: 5

    # Footer
    Label:
        size_hint_y: None
        height: '30dp'
        text: "[ref=lecz]&copy; 2025 LECZ Ltd. All Rights Reserved.[/ref]"
        markup: True
        font_size: '14dp'
        halign: 'center'
'''

class MainScreen(BoxLayout):

    def get_download_links(self, url):
        self.ids.download_links_layout.clear_widgets()
        self.ids.related_layout.clear_widgets()
        self.ids.video_player.opacity = 0
        threading.Thread(target=self.fetch_links, args=(url,), daemon=True).start()

    def fetch_links(self, url):
        try:
            response = requests.post("http://localhost:5000/get_download_link", json={"url": url})
            data = response.json()
            Clock.schedule_once(lambda dt: self.update_ui(data))
        except Exception as e:
            Clock.schedule_once(lambda dt, err=str(e): self.update_ui({"error": err}))

    def update_ui(self, data):
        dl_layout = self.ids.download_links_layout
        rel_layout = self.ids.related_layout
        video_player = self.ids.video_player

        dl_layout.clear_widgets()
        rel_layout.clear_widgets()

        from kivy.uix.label import Label
        from kivy.uix.button import Button

        if "error" in data:
            dl_layout.add_widget(Label(text="Error: " + data["error"]))
            return

        if "playlist_title" in data and "entries" in data:
            dl_layout.add_widget(Label(text="[b]Playlist: " + data["playlist_title"] + "[/b]", markup=True))
            for entry in data["entries"]:
                dl_layout.add_widget(Label(text="[b]Video: " + entry["title"] + "[/b]", markup=True))
                for fmt in entry["formats"]:
                    size = fmt.get("filesize")
                    size_str = f"{(size / (1024*1024)):.2f} MB" if size else "unknown size"
                    btn = Button(text=f"Download ({fmt.get('resolution','unknown')} - {size_str})", size_hint_y=None, height="40dp")
                    btn.bind(on_press=lambda inst, url=fmt["url"]: self.play_video(url))
                    dl_layout.add_widget(btn)

        elif "title" in data and "formats" in data:
            dl_layout.add_widget(Label(text="[b]" + data["title"] + "[/b]", markup=True))
            for fmt in data["formats"]:
                size = fmt.get("filesize")
                size_str = f"{(size / (1024*1024)):.2f} MB" if size else "unknown size"
                btn = Button(text=f"Download ({fmt.get('resolution','unknown')} - {size_str})", size_hint_y=None, height="40dp")
                btn.bind(on_press=lambda inst, url=fmt["url"]: self.play_video(url))
                dl_layout.add_widget(btn)
        else:
            dl_layout.add_widget(Label(text="No downloadable formats found."))

        # Set video source
        if "player_url" in data:
            video_player.source = data["player_url"]
            video_player.state = "play"
            video_player.opacity = 1
        elif "formats" in data and data["formats"]:
            video_player.source = data["formats"][0]["url"]
            video_player.state = "play"
            video_player.opacity = 1
        elif "entries" in data and data["entries"] and data["entries"][0]["formats"]:
            video_player.source = data["entries"][0]["formats"][0]["url"]
            video_player.state = "play"
            video_player.opacity = 1

        if "related" in data and data["related"]:
            for item in data["related"]:
                btn = Button(text=item["title"], size_hint_y=None, height="40dp")
                btn.bind(on_press=lambda inst, url=item["url"]: self.open_related(url))
                rel_layout.add_widget(btn)

    def play_video(self, url):
        video_player = self.ids.video_player
        video_player.source = url
        video_player.state = "play"
        video_player.opacity = 1

    def open_related(self, url):
        webbrowser.open(url)

class MyApp(App):
    def build(self):
        Builder.load_string(KV)
        return MainScreen()

if __name__ == '__main__':
    MyApp().run()
