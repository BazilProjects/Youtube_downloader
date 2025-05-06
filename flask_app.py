'''
from flask import Flask, request, jsonify, render_template
from flask import  url_for, redirect
import yt_dlp

app = Flask(__name__)


#app.config['SERVER_NAME'] = '*'



@app.route("/home")
def home():
    """Renders the informative homepage."""
    return render_template("home.html")

@app.route("/")
def index():
    error = request.args.get('error')
    return render_template("index.html",error=error)


@app.route("/second_trial")
def index2():
    return render_template("index2.html")


@app.route("/about")
def about():
    return render_template("about.html")

COOKIE_FILE = "cookies.txt"  # <— path to your cookies.txt

@app.route("/get_download_link", methods=["POST"])
def get_download_link():
    data = request.get_json()
    video_url = data.get("url")

    if not video_url:
        return jsonify({"error": "No URL provided"}), 400

    ydl_opts = {
        'cookiefile': COOKIE_FILE,      # ← added
        'listformats': True,
        'quiet': False,
        'skip_download': True,
    }

    try:
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            info = ydl.extract_info(video_url, download=False)
            formats = []
            for fmt in info.get("formats", []):
                if fmt.get("url") and fmt.get("ext") == "mp4" \
                   and "vcodec" in fmt and "acodec" in fmt and fmt.get("acodec") != "none":
                    formats.append({
                        "url": fmt.get("url"),
                        "resolution": fmt.get("format_note"),
                        "filesize": fmt.get("filesize"),
                        "ext": fmt.get("ext")
                    })

            return jsonify({
                "title": info.get("title"),
                "formats": formats
            })
    except Exception as e:
        return jsonify({"error": str(e)}), 500


@app.route("/get_download_link_2", methods=["POST"])
def get_download_link_2():
    data = request.get_json()
    video_url = data.get("url")

    if not video_url:
        return jsonify({"error": "No URL provided"}), 400

    ydl_opts = {
        'cookiefile': COOKIE_FILE,      # ← added
        'listformats': True,
        'quiet': False,
        'skip_download': True,
    }

    try:
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            info = ydl.extract_info(video_url, download=False)

            if "entries" in info:
                playlist_title = info.get("title", "Playlist")
                playlist_entries = []
                for entry in info["entries"]:
                    if entry is None:
                        continue
                    formats = []
                    for fmt in entry.get("formats", []):
                        if fmt.get("url") and fmt.get("ext") == "mp4":
                            formats.append({
                                "url": fmt.get("url"),
                                "resolution": fmt.get("format_note"),
                                "filesize": fmt.get("filesize"),
                                "ext": fmt.get("ext")
                            })
                    playlist_entries.append({
                        "title": entry.get("title"),
                        "formats": formats
                    })
                return jsonify({
                    "playlist_title": playlist_title,
                    "entries": playlist_entries
                })
            else:
                formats = []
                for fmt in info.get("formats", []):
                    if fmt.get("url") and fmt.get("ext") == "mp4":
                        formats.append({
                            "url": fmt.get("url"),
                            "resolution": fmt.get("format_note"),
                            "filesize": fmt.get("filesize"),
                            "ext": fmt.get("ext")
                        })
                return jsonify({
                    "title": info.get("title"),
                    "formats": formats
                })
    except Exception as e:
        return jsonify({"error": str(e)}), 500



@app.errorhandler(404)
def not_found(e):
    return redirect(url_for('index', error='404'))

@app.errorhandler(403)
def forbidden(e):
    return redirect(url_for('index', error='403'))

@app.errorhandler(500)
def server_error(e):
    return redirect(url_for('index', error='500'))

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
    #app.run(host='0.0.0.0')
    #app.run(host="0.0.0.0", port=5000)






















from flask import Flask, request, jsonify, render_template
from flask import  url_for, redirect
import yt_dlp

app = Flask(__name__)


#app.config['SERVER_NAME'] = '*'



@app.route("/home")
def home():
    #Renders the informative homepage.
    return render_template("home.html")

@app.route("/")
def index():
    error = request.args.get('error')
    return render_template("index.html",error=error)


@app.route("/second_trial")
def index2():
    return render_template("index2.html")


@app.route("/about")
def about():
    return render_template("about.html")


@app.route("/get_download_link", methods=["POST"])
def get_download_link():
    data = request.get_json()
    video_url = data.get("url")

    if not video_url:
        return jsonify({"error": "No URL provided"}), 400

    ydl_opts = {
        'listformats': True,
        'quiet': False,
        'skip_download': True,
    }

    try:
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            info = ydl.extract_info(video_url, download=False)
            formats = []
            for fmt in info.get("formats", []):
                # Exclude audio-only or video-only formats and ensure both video and audio are included
                if fmt.get("url"):
                    if fmt.get("ext") == "mp4" and "vcodec" in fmt and "acodec" in fmt and fmt.get("acodec") != "none":
                        formats.append({
                            "url": fmt.get("url"),
                            "resolution": fmt.get("format_note"),
                            "filesize": fmt.get("filesize"),
                            "ext": fmt.get("ext")
                        })

            return jsonify({
                "title": info.get("title"),
                "formats": formats
            })
    except Exception as e:
        return jsonify({"error": str(e)}), 500
        




@app.route("/get_download_link_2", methods=["POST"])
def get_download_link_2():
    data = request.get_json()
    video_url = data.get("url")
    
    if not video_url:
        return jsonify({"error": "No URL provided"}), 400

    ydl_opts = {
        'listformats': True,
        'quiet': False,
        'skip_download': True,
    }

    try:
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            info = ydl.extract_info(video_url, download=False)
            
            # Check if this is a playlist
            if "entries" in info:
                playlist_title = info.get("title", "Playlist")
                playlist_entries = []
                for entry in info["entries"]:
                    # Skip any None entries (in case extraction failed for a video)
                    if entry is None:
                        continue
                    video_title = entry.get("title")
                    formats = []
                    for fmt in entry.get("formats", []):
                        # Filter for mp4 that contains both video and audio
                        if fmt.get("url") and fmt.get("ext") == "mp4" and \
                           "vcodec" in fmt and "acodec" in fmt and fmt.get("acodec") != "none":
                            formats.append({
                                "url": fmt.get("url"),
                                "resolution": fmt.get("format_note"),
                                "filesize": fmt.get("filesize"),
                                "ext": fmt.get("ext")
                            })
                    playlist_entries.append({
                        "title": video_title,
                        "formats": formats
                    })
                    print(playlist_entries)
                return jsonify({
                    "playlist_title": playlist_title,
                    "entries": playlist_entries
                })
            else:
                # Single video handling
                formats = []
                for fmt in info.get("formats", []):
                    if fmt.get("url") and fmt.get("ext") == "mp4" :#and \
                       #"vcodec" in fmt and "acodec" in fmt and fmt.get("acodec") != "none":
                        formats.append({
                            "url": fmt.get("url"),
                            "resolution": fmt.get("format_note"),
                            "filesize": fmt.get("filesize"),
                            "ext": fmt.get("ext")
                        })
                return jsonify({
                    "title": info.get("title"),
                    "formats": formats
                })
    except Exception as e:
        return jsonify({"error": str(e)}), 500


@app.errorhandler(404)
def not_found(e):
    return redirect(url_for('index', error='404'))

@app.errorhandler(403)
def forbidden(e):
    return redirect(url_for('index', error='403'))

@app.errorhandler(500)
def server_error(e):
    return redirect(url_for('index', error='500'))

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
    #app.run(host='0.0.0.0')
    #app.run(host="0.0.0.0", port=5000)

'''

from flask import Flask, request, jsonify, render_template
from flask import url_for, redirect
import yt_dlp

app = Flask(__name__)

@app.route("/home")
def home():
    # Renders the informative homepage.
    return render_template("home.html")

@app.route("/")
def index():
    error = request.args.get('error')
    return render_template("index.html", error=error)

@app.route("/second_trial")
def index2():
    return render_template("index2.html")

@app.route("/about")
def about():
    return render_template("about.html")

@app.route("/get_download_link", methods=["POST"])
def get_download_link():
    data = request.get_json()
    video_url = data.get("url")

    if not video_url:
        return jsonify({"error": "No URL provided"}), 400

    ydl_opts = {
        'cookies_from_browser': 'chrome',   # ← exact API name
        'listformats': True,
        'quiet': False,
        'skip_download': True,
    }

    try:
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            info = ydl.extract_info(video_url, download=False)
            formats = []
            for fmt in info.get("formats", []):
                # Exclude audio-only or video-only formats and ensure both video and audio are included
                if fmt.get("url") and fmt.get("ext") == "mp4" \
                   and "vcodec" in fmt and "acodec" in fmt and fmt.get("acodec") != "none":
                    formats.append({
                        "url": fmt.get("url"),
                        "resolution": fmt.get("format_note"),
                        "filesize": fmt.get("filesize"),
                        "ext": fmt.get("ext")
                    })

            return jsonify({
                "title": info.get("title"),
                "formats": formats
            })
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route("/get_download_link_2", methods=["POST"])
def get_download_link_2():
    data = request.get_json()
    video_url = data.get("url")

    if not video_url:
        return jsonify({"error": "No URL provided"}), 400

    ydl_opts = {
        'cookies_from_browser': 'chrome',   # ← exact API name
        'listformats': True,
        'quiet': False,
        'skip_download': True,
    }

    try:
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            info = ydl.extract_info(video_url, download=False)

            # Check if this is a playlist
            if "entries" in info:
                playlist_title = info.get("title", "Playlist")
                playlist_entries = []
                for entry in info["entries"]:
                    if entry is None:
                        continue
                    formats = []
                    for fmt in entry.get("formats", []):
                        if fmt.get("url") and fmt.get("ext") == "mp4":
                            formats.append({
                                "url": fmt.get("url"),
                                "resolution": fmt.get("format_note"),
                                "filesize": fmt.get("filesize"),
                                "ext": fmt.get("ext")
                            })
                    playlist_entries.append({
                        "title": entry.get("title"),
                        "formats": formats
                    })
                return jsonify({
                    "playlist_title": playlist_title,
                    "entries": playlist_entries
                })
            else:
                formats = []
                for fmt in info.get("formats", []):
                    if fmt.get("url") and fmt.get("ext") == "mp4":
                        formats.append({
                            "url": fmt.get("url"),
                            "resolution": fmt.get("format_note"),
                            "filesize": fmt.get("filesize"),
                            "ext": fmt.get("ext")
                        })
                return jsonify({
                    "title": info.get("title"),
                    "formats": formats
                })
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.errorhandler(404)
def not_found(e):
    return redirect(url_for('index', error='404'))

@app.errorhandler(403)
def forbidden(e):
    return redirect(url_for('index', error='403'))

@app.errorhandler(500)
def server_error(e):
    return redirect(url_for('index', error='500'))

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
