import requests
import hashlib
import time
from music_download import MusicDownloader

def generate_sign(page_no, timestamp, keyword):
    keyword = requests.utils.unquote(keyword)
    sign_str = f"appid=16073360&pageNo={page_no}&pageSize=20&timestamp={timestamp}&type=1&word={keyword}0b50b02fd0d73a9c4c8c3a781c30845f"
    sign = hashlib.md5(sign_str.encode()).hexdigest()
    return sign

def get_all_music_info(keyword="胡彦斌"):
    encoded_keyword = requests.utils.quote(keyword)
    page_no = 1
    all_songs = []

    while True:
        timestamp = str(int(time.time()))
        sign = generate_sign(page_no, timestamp, encoded_keyword)

        url = f"https://music.91q.com/v1/search?sign={sign}&word={encoded_keyword}&type=1&pageNo={page_no}&pageSize=20&appid=16073360&timestamp={timestamp}"
        headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"
        }

        response = requests.get(url, headers=headers)
        response.encoding = 'utf-8'
        data = response.json()

        # 提取歌曲信息
        songs = data.get('data', {}).get('typeTrack', [])
        if not songs:
            break

        for song in songs:
            title = song.get('title', '未知')
            song_id = song.get('id', '未知')
            artists = song.get('artist', [])
            artist_names = [artist.get('name', '未知') for artist in artists]
            artist_names_str = " / ".join(artist_names)

            print(f"歌曲名: {title}, ID: {song_id}, 歌手: {artist_names_str}")
            all_songs.append(song_id)

        page_no += 1
        time.sleep(1)  # 避免请求过于频繁

    # 输出歌曲总数
    print(f"\n共找到 {len(all_songs)} 首歌曲")
    return all_songs


if __name__ == "__main__":
    # 获取所有歌曲信息
    songs = get_all_music_info('胡彦斌')
    
    # 下载所有歌曲
    downloader = MusicDownloader()
    downloader.download(songs)