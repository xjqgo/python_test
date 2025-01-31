import requests
import hashlib
import time
import json
import os
import sys

class MusicManager:
    def __init__(self):
        self.mp3_dir = 'mp3'
        if not os.path.exists(self.mp3_dir):
            os.makedirs(self.mp3_dir)

    def generate_search_sign(self, page_no, timestamp, keyword):
        """生成搜索接口签名"""
        keyword = requests.utils.unquote(keyword)
        sign_str = f"appid=16073360&pageNo={page_no}&pageSize=20&timestamp={timestamp}&type=1&word={keyword}0b50b02fd0d73a9c4c8c3a781c30845f"
        return hashlib.md5(sign_str.encode()).hexdigest()

    def generate_download_sign(self, tsid):
        """生成下载接口签名"""
        timestamp = str(int(time.time()))
        sign_str = f"TSID={tsid}&appid=16073360&timestamp={timestamp}0b50b02fd0d73a9c4c8c3a781c30845f"
        return hashlib.md5(sign_str.encode()).hexdigest(), timestamp

    def search_songs(self, keyword, max_pages=10):
        """搜索歌曲"""
        print(f"\n开始搜索歌手: {keyword}")
        encoded_keyword = requests.utils.quote(keyword)
        page_no = 1
        all_songs = []
        
        while page_no <= max_pages:
            timestamp = str(int(time.time()))
            sign = self.generate_search_sign(page_no, timestamp, encoded_keyword)

            url = f"https://music.91q.com/v1/search?sign={sign}&word={encoded_keyword}&type=1&pageNo={page_no}&pageSize=20&appid=16073360&timestamp={timestamp}"
            headers = {
                "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"
            }

            try:
                response = requests.get(url, headers=headers)
                response.encoding = 'utf-8'
                data = response.json()

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
            except Exception as e:
                print(f"搜索出错: {e}")
                break

        print(f"\n共找到 {len(all_songs)} 首歌曲")
        return all_songs

    def get_song_info(self, tsid):
        """获取歌曲下载信息"""
        url = "https://music.91q.com/v1/song/tracklink?"
        headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
            "Accept": "application/json, text/plain, */*",
            "Origin": "https://music.91q.com"
        }
        
        sign, timestamp = self.generate_download_sign(tsid)
        params = {
            "appid": "16073360",
            "timestamp": timestamp,
            "TSID": tsid,
            "sign": sign
        }
        
        try:
            response = requests.get(url, headers=headers, params=params)
            response.encoding = 'utf-8'
            
            if response.status_code != 200:
                return None, None, None
                
            data = response.json()
            mp3_url = data.get('data', {}).get('path')
            song_name = data['data']['title']
            artist_name = data['data'].get('artist', [{}])[0].get('name', '未知')
            
            return mp3_url, song_name, artist_name
            
        except Exception as e:
            print(f"获取歌曲信息出错: {e}")
            return None, None, None

    def download_song(self, mp3_url, song_name, artist_name, download_count):
        """下载单首歌曲"""
        try:
            response = requests.get(mp3_url)
            response.raise_for_status()
            
            file_name = f"{download_count:02d}. {song_name} - {artist_name}"
            file_name = "".join(c for c in file_name if c not in r'\/:*?"<>|')
            file_path = os.path.join(self.mp3_dir, f"{file_name}.mp3")
            
            with open(file_path, 'wb') as f:
                f.write(response.content)
            print(f"歌曲已保存到: {file_path}")
            return True
        except Exception as e:
            print(f"下载MP3时出错: {e}")
            return False

    def process(self, keyword, max_downloads=None):
        """主处理流程"""
        print(f"开始处理歌手 {keyword} 的音乐")
        start_time = time.time()  # 记录开始时间
        
        # 搜索歌曲
        song_ids = self.search_songs(keyword)
        
        # 下载歌曲
        download_count = 0
        failed_count = 0
        downloaded_songs = []
        
        for tsid in song_ids:
            if max_downloads is not None and download_count >= max_downloads:
                break
                
            mp3_url, song_name, artist_name = self.get_song_info(tsid)
            if mp3_url and song_name and artist_name:
                download_count += 1
                if self.download_song(mp3_url, song_name, artist_name, download_count):
                    downloaded_songs.append((download_count, song_name, artist_name))
            else:
                print(f"TSID {tsid}: VIP歌曲无法下载")
                failed_count += 1
        
        # 打印下载结果
        if downloaded_songs:
            print("\n下载成功的歌曲:")
            for index, song_name, artist_name in downloaded_songs:
                print(f"{index:02d}.{song_name} - {artist_name}")
            
            save_dir = os.path.abspath(self.mp3_dir)
            print(f"文件保存目录: {save_dir}")

        print(f"\n共有: {len(song_ids)} 首歌曲")
        print(f"下载完成: {download_count} 首歌曲")
        print(f"VIP无法下载: {failed_count} 首歌曲")
        
        # 计算并打印总下载时间
        total_time = time.time() - start_time
        print(f"总下载时间: {total_time:.2f} 秒")

def is_running_in_exe():
    """检查是否在exe环境中运行"""
    return getattr(sys, 'frozen', False)

def get_resource_path(relative_path):
    """获取资源文件的绝对路径"""
    if is_running_in_exe():
        # 如果是打包后的 exe，使用 sys._MEIPASS
        base_path = getattr(sys, '_MEIPASS', os.path.abspath("."))
    else:
        # 如果是开发环境，使用当前目录
        base_path = os.path.abspath(".")
    return os.path.join(base_path, relative_path)

if __name__ == "__main__":
    try:
        # 用户输入
        keyword = input("请输入要下载的歌手名（如：胡彦斌）：")
        max_downloads_input = input("请输入最大下载数（留空表示全部下载）：")
        max_downloads = int(max_downloads_input) if max_downloads_input else None

        # 创建管理器实例并开始处理
        manager = MusicManager()
        manager.process(keyword, max_downloads)
        
    except Exception as e:
        print(f"\n程序运行出错: {e}")
    finally:
        # 在exe环境中等待用户按键退出
        if is_running_in_exe():
            input("\n按回车键退出...")