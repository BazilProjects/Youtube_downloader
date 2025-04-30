"""import requests

# Function to download a video
def download_video(url, save_path):
    try:
        # Send a GET request to the URL
        response = requests.get(url, stream=True)

        # Check if the request was successful (status code 200)
        if response.status_code == 200:
            # Open a file in write-binary mode
            with open(save_path, 'wb') as f:
                # Write the content in chunks to avoid memory overload
                for chunk in response.iter_content(chunk_size=8192):
                    if chunk:  # filter out keep-alive new chunks
                        f.write(chunk)
            print(f"Video downloaded successfully! Saved to: {save_path}")
        else:
            print(f"Failed to download video. HTTP Status code: {response.status_code}")

    except Exception as e:
        print(f"An error occurred: {e}")

# Example usage
video_url ="https://xhamster.com/videos/big-ass-stepmom-agrees-to-share-bed-with-stepson-angel-cruz-sarah-black-xhnQh7b"
save_path = "downloaded_video.mp4"
download_video(video_url, save_path)

import yt_dlp

video_url = "https://youtu.be/ba-HMvDn_vU?list=PLUl4u3cNGP60IKRN_pFptIBxeiMc0MCJP"

# Options for downloading
ydl_opts = {
    'format': 'best',  # Downloads the best available quality
    'outtmpl': '%(title)s.%(ext)s',  # Output filename format
}

# Download video
with yt_dlp.YoutubeDL(ydl_opts) as ydl:
    ydl.download([video_url])

print("Download complete!")

import yt_dlp

video_url = "https://youtu.be/ba-HMvDn_vU"

with yt_dlp.YoutubeDL({'listformats': True}) as ydl:
    ydl.extract_info(video_url, download=False)
"""
import yt_dlp

video_url ="https://www.youtube.com/watch?v=--6CdAypJsQ"#"https://www.youtube.com/watch?v=_waPvOwL9Z8"#"https://www.youtube.com/watch?v=90JWoR9MfYU&list=PLUl4u3cNGP61Q_RVDn6srWbLV_zFnd9n0"
#
# "https://www.youtube.com/watch?v=ba-HMvDn_vU&list=PLUl4u3cNGP60IKRN_pFptIBxeiMc0MCJP"
#"https://www.youtube.com/watch?v=HdHlfiOAJyE&list=PLUl4u3cNGP63B2lDhyKOsImI7FjCf6eDW"#
# This selects the best available MP4 format (video + audio)
ydl_opts = {
    'format': 'bv*+ba/b[ext=mp4]',  # Best MP4 video + best audio
    'outtmpl': '%(title)s.%(ext)s',  # Output filename
    'merge_output_format': 'mp4',  # Ensure MP4 format
    'postprocessors': [{
        'key': 'FFmpegVideoConvertor',
        'preferedformat': 'mp4',
    }]
}

with yt_dlp.YoutubeDL(ydl_opts) as ydl:
    ydl.download([video_url])

print("Download complete!")
