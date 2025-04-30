import threading
import webbrowser

from kivy.app import App
from kivy.lang import Builder
from kivy.clock import Clock
from kivy.uix.boxlayout import BoxLayout

from yt_dlp import YoutubeDL

KV = '''
<MainScreen>:
    orientation: 'vertical'
    padding: 10
    spacing: 10

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

    Video:
        id: video_player
        source: ""
        state: "stop"
        options: {'eos': 'loop'}
        size_hint_y: 0.4
        opacity: 0

    ScrollView:
        size_hint_y: 0.3
        GridLayout:
            id: download_links_layout
            cols: 1
            size_hint_y: None
            height: self.minimum_height
            spacing: 5

    ScrollView:
        size_hint_y: 0.2
        GridLayout:
            id: related_layout
            cols: 1
            size_hint_y: None
            height: self.minimum_height
            spacing: 5

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
        ydl_opts = {
            'quiet': True,
            'skip_download': True,
            'forcejson': True,
            'extract_flat': False,
        }

        try:
            with YoutubeDL(ydl_opts) as ydl:
                info = ydl.extract_info(url, download=False)
                Clock.schedule_once(lambda dt: self.update_ui(info))
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

        def make_button(fmt):
            size = fmt.get("filesize") or fmt.get("filesize_approx")
            size_str = f"{(size / (1024*1024)):.2f} MB" if size else "unknown size"
            res = fmt.get("format_note") or fmt.get("resolution") or fmt.get("ext")
            label = f"Download ({res} - {size_str})"
            btn = Button(text=label, size_hint_y=None, height="40dp")
            btn.bind(on_press=lambda inst, url=fmt["url"]: self.play_video(url))
            return btn

        if 'entries' in data:
            dl_layout.add_widget(Label(text=f"[b]Playlist: {data.get('title', 'Unnamed')}[/b]", markup=True))
            for entry in data['entries']:
                dl_layout.add_widget(Label(text=f"[b]Video: {entry.get('title', 'Untitled')}[/b]", markup=True))
                for fmt in entry.get("formats", []):
                    dl_layout.add_widget(make_button(fmt))
        else:
            dl_layout.add_widget(Label(text=f"[b]{data.get('title', 'No Title')}[/b]", markup=True))
            for fmt in data.get("formats", []):
                dl_layout.add_widget(make_button(fmt))

        # Play video preview
        video_url = None
        if data.get("formats"):
            for fmt in data["formats"]:
                if fmt.get("vcodec") != "none" and fmt.get("acodec") != "none":
                    video_url = fmt["url"]
                    break
            if not video_url:
                video_url = data["formats"][0]["url"]
            video_player.source = video_url
            video_player.state = "play"
            video_player.opacity = 1

        # Related section placeholder
        if "related" in data:
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
