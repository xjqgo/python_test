import requests
import json
import time
import hashlib
import os

class MusicDownloader:
    def __init__(self):
        self.mp3_dir = 'mp3'
        if not os.path.exists(self.mp3_dir):
            os.makedirs(self.mp3_dir)

    def generate_sign(self, tsid):
        # 生成时间戳
        timestamp = str(int(time.time()))
        # 构建签名字符串
        sign_str = f"TSID={tsid}&appid=16073360&timestamp={timestamp}0b50b02fd0d73a9c4c8c3a781c30845f"
        print("\n签名生成过程:")
        print("1. TSID:", tsid)
        print("2. 时间戳:", timestamp)
        print("3. 原始字符串:", sign_str)
        
        # MD5加密
        sign = hashlib.md5(sign_str.encode()).hexdigest()
        print("4. MD5加密后:", sign)
        return sign, timestamp

    def get_song_info(self, tsid):
        """获取歌曲信息"""
        url = "https://music.91q.com/v1/song/tracklink?"
        headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
            "Accept": "application/json, text/plain, */*",
            "Origin": "https://music.91q.com"
        }
        
        # 获取签名和时间戳
        sign, timestamp = self.generate_sign(tsid)
        
        # 构建请求参数
        params = {
            "appid": "16073360",
            "timestamp": timestamp,
            "TSID": tsid,
            "sign": sign
        }
        
        try:
            print(f"\n正在获取歌曲信息...")
            print(f"请求URL: {url}")
            print("请求头:", json.dumps(headers, indent=2, ensure_ascii=False))
            print("请求参数:", json.dumps(params, indent=2, ensure_ascii=False))
            
            response = requests.get(url, headers=headers, params=params)
            response.encoding = 'utf-8'
            
            # 检查响应状态
            print(f"\n响应状态码: {response.status_code}")
            print("响应头:", json.dumps(dict(response.headers), indent=2, ensure_ascii=False))
            print("完整URL:", response.url)
            
            if response.status_code != 200:
                print(f"请求失败，状态码: {response.status_code}")
                return None, None
                
            # 尝试解析JSON响应
            try:
                data = response.json()
                print("\n接口返回数据:")
                print(json.dumps(data, ensure_ascii=False, indent=2))
                
                # 提取MP3地址
                mp3_url = data.get('data', {}).get('path') 
                # 提取歌名
                song_name = data['data']['title']
                if mp3_url:
                    print("MP3地址:", mp3_url)
                    print("歌名:", song_name)
                else:
                    print("未找到MP3地址")
                
                return mp3_url, song_name
            except json.JSONDecodeError:
                print("返回数据不是有效的JSON格式")
                print("原始响应内容:")
                print(response.text)
                return None, None
                
        except requests.exceptions.RequestException as e:
            print(f"请求错误: {e}")
            return None, None
        except Exception as e:
            print(f"发生错误: {e}")
            return None, None

    def download_and_save_mp3(self, mp3_url, song_name, tsid):
        try:
            response = requests.get(mp3_url)
            response.raise_for_status()
            
            # 保存文件，文件名中包含TSID
            file_path = os.path.join(self.mp3_dir, f"{song_name}_{tsid}.mp3")
            with open(file_path, 'wb') as f:
                f.write(response.content)
            print(f"歌曲已保存到: {file_path}")
        except requests.exceptions.RequestException as e:
            print(f"下载MP3时出错: {e}")

    def download(self, tsids, max_downloads=None):
        if isinstance(tsids, str):
            tsids = [tsids]
        
        download_count = 0
        failed_count = 0
        
        for tsid in tsids:
            if max_downloads is not None and download_count >= max_downloads:
                break
            
            mp3_url, song_name = self.get_song_info(tsid)
            if mp3_url:
                self.download_and_save_mp3(mp3_url, song_name, tsid)
                download_count += 1
            else:
                print(f"TSID {tsid}: VIP歌曲无法下载")
                failed_count += 1
        
        print(f"\n下载完成: {download_count} 首歌曲")
        print(f"VIP无法下载: {failed_count} 首歌曲")

if __name__ == "__main__":
    # 创建下载器实例
    downloader = MusicDownloader()
    # 测试特定歌曲ID列表
    TSIDs = ["T10063942259", "T10063942260"]  # 示例ID列表
    downloader.download(TSIDs, max_downloads=5)    