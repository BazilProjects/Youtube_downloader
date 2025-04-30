from flask import Flask, jsonify , render_template, request, redirect, url_for
import yt_dlp
import os

app = Flask(__name__, template_folder="template")
@app.route('/download', methods=['GET'])
def download_video():
    url = request.args.get('url')
    if not url:
        return jsonify({"success": False, "error": "No URL provided"}), 400

    try:
        # yt-dlp options for the download
        ydl_opts = {
            'format': 'best',  # Best quality
            'outtmpl': 'downloads/%(title)s.%(ext)s',  # Save the video with its title
            'quiet': True,  # Suppress unnecessary logs
        }

        # Create yt-dlp object
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            info_dict = ydl.extract_info(url, download=False)
            video_url = info_dict['url']  # Get the direct video URL
            title = info_dict.get('title', 'video')

        return jsonify({"success": True, "video_url": video_url, "title": title})

    except Exception as e:
        return jsonify({"success": False, "error": str(e)}), 500


@app.route('/', methods=['GET', 'POST'])
def home():
    if request.method == 'POST':
        url = request.form['url']
        if url:
            save_path = os.path.join(os.path.expanduser("~"), "Downloads", "Youtube")
            os.makedirs(save_path, exist_ok=True)  # Create the directory if it doesn't exist
            message = download_video(url, save_path)
            return render_template('index.html', message=message)
        else:
            return render_template('index.html', message="Please enter a valid YouTube URL.")
    
    return render_template('index.html')

if __name__ == "__main__":
    app.run(debug=True)
