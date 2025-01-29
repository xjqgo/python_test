import requests
from bs4 import BeautifulSoup
from music_download import MusicDownloader

def get_music_info(keyword="胡彦斌"):
    # 对搜索关键词进行URL编码
    encoded_keyword = requests.utils.quote(keyword)
    url = f"https://music.91q.com/search?word={encoded_keyword}"
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"
    }

    try:
        response = requests.get(url, headers=headers)
        response.encoding = 'utf-8'
        print(f"正在搜索: {keyword}")
        print(f"获取到的响应内容长度: {len(response.text)} 字符")
        # 检查响应状态
        if response.status_code != 200:
            print(f"请求失败，状态码: {response.status_code}")
            return

        # 创建一个列表存储歌曲信息
        songs = []

        # 使用BeautifulSoup解析HTML
        soup = BeautifulSoup(response.text, 'html.parser')

        # 提取歌曲信息
        song_items = soup.select("div.song.ellipsis.clearfix")

        # 检查是否找到歌曲数据
        if not song_items:
            print("未找到任何歌曲信息")
            print("页面内容：")
            print(response.text[:500])  # 打印前500个字符以便调试
            return

        # 提取歌曲信息
        for song in song_items:
            song_link = song.select_one("div > a")
            singer = song.find_next_sibling("div", class_="artist ellipsis")
            if song_link:
                # 处理歌手名称
                singer_text = singer.text.strip() if singer else '未知歌手'
                # 分割并过滤空字符串，然后用 " / " 连接
                singers = [s.strip() for s in singer_text.split('/') if s.strip()]
                singer_text = " / ".join(singers)

                # 提取歌曲ID
                song_id = song_link.get('href', '未找到链接').split('/')[-1]

                song_info = {
                    '歌曲名': song_link.text.strip(),
                    '链接': 'https://music.91q.com' + song_link.get('href', '未找到链接'),
                    '歌手': singer_text,
                    '歌曲ID': song_id
                }
                songs.append(song_info)

        print(f"\n共找到 {len(songs)} 首歌曲")
        # 打印歌曲信息
        for song in songs:
            print("\n歌曲信息:")
            for key, value in song.items():
                print(f"{key}: {value}")

        return songs

    except requests.exceptions.RequestException as e:
        print(f"请求错误: {e}")
    except Exception as e:
        print(f"发生错误: {e}")

if __name__ == "__main__":
    # 可以在这里输入要搜索的关键词
    songs = get_music_info('胡彦斌')

    # 创建下载器实例
    downloader = MusicDownloader()

    # 下载每首歌曲
    if songs:
        for song in songs:
            tsid = song['歌曲ID']
            print(f"\n正在下载: {song['歌曲名']} - {song['歌手']}")
            downloader.download(tsid)
