import yt_dlp

video_url = "https://www.youtube.com/watch?v=y4lbxocj0Cg"  # replace with your video URL

with yt_dlp.YoutubeDL({'quiet': True}) as ydl:
    info = ydl.extract_info(video_url, download=False)
    #print(info)
    related = info.get("related", None)
    if related:
        print("Related videos:")
        for item in related:
            print(f"- {item.get('title')} (ID: {item.get('id')})")
    else:
        print("No related videos found.")
