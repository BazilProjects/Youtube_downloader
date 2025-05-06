import browser_cookie3
from http.cookiejar import MozillaCookieJar
import yt_dlp
def dump_cookies(path):
    # Load Chrome cookies (auto-decrypts v11 cookies via your keyring)
    cj = browser_cookie3.chrome()
    # Convert to a netscape jar
    nc = MozillaCookieJar(path)
    for cookie in cj:
        nc.set_cookie(cookie)
    nc.save(ignore_discard=True, ignore_expires=True)

# In your download route, before calling yt-dlp:
dump_cookies('cookies.txt')

ydl_opts = {
    'cookiefile': 'cookies.txt',
    # …other options…
}
video_url='https://www.youtube.com/watch?v=DiGB5uAYKAg'
with yt_dlp.YoutubeDL(ydl_opts) as ydl:
    info = ydl.extract_info(video_url, download=False)
    # …
