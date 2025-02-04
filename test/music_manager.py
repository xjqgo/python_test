import requests
import hashlib
import time
import json
import os
import sys
import tkinter as tk
from tkinter import ttk, scrolledtext, messagebox
import threading
from queue import Queue

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

class MusicManagerGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("音乐下载管理器")
        self.root.geometry("800x600")
        
        # 创建音乐管理器实例
        self.manager = MusicManager()
        
        # 创建主框架并配置列宽
        self.main_frame = ttk.Frame(self.root, padding="10")
        self.main_frame.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
        
        # 配置主窗口和主框架的列宽和行高
        self.root.columnconfigure(0, weight=1)
        self.root.rowconfigure(0, weight=1)
        self.main_frame.columnconfigure(0, weight=1)
        self.main_frame.rowconfigure(1, weight=2)  # 下载列表区域占比更大
        self.main_frame.rowconfigure(2, weight=1)  # 日志区域占比正常
        
        # 搜索区域
        self.create_search_area()
        
        # 下载列表区域
        self.create_download_list_area()
        
        # 日志区域
        self.create_log_area()
        
        # 状态栏
        self.create_status_bar()
        
        # 绑定关闭窗口事件
        self.root.protocol("WM_DELETE_WINDOW", self.on_closing)

        self.song_queue = Queue()  # 添加一个队列来存储歌曲信息
        self.download_thread = None
        self.is_downloading = False
        self.search_thread = None
        self.is_searching = False

        # 添加搜索提示对话框
        self.create_search_dialog()

    def create_search_area(self):
        # 搜索框架
        search_frame = ttk.LabelFrame(self.main_frame, text="搜索", padding="5")
        search_frame.grid(row=0, column=0, sticky=(tk.W, tk.E), pady=5)
        search_frame.columnconfigure(1, weight=1)  # 让搜索输入框可以扩展
        
        # 搜索输入
        ttk.Label(search_frame, text="歌手名:").grid(row=0, column=0, padx=5)
        self.search_var = tk.StringVar(value="胡彦斌")  # 设置默认歌手名
        self.search_entry = ttk.Entry(search_frame, textvariable=self.search_var, width=40)
        self.search_entry.grid(row=0, column=1, padx=5)
        # 绑定回车键
        self.search_entry.bind('<Return>', lambda e: self.search_songs())
        
        # 搜索按钮和进度提示
        self.search_frame = ttk.Frame(search_frame)
        self.search_frame.grid(row=0, column=2, padx=5)
        
        self.search_btn = ttk.Button(self.search_frame, text="搜索", command=self.search_songs)
        self.search_btn.pack(side=tk.LEFT)
        
        self.search_progress = ttk.Label(self.search_frame, text="")
        self.search_progress.pack(side=tk.LEFT, padx=5)
        
        # 最大下载数
        ttk.Label(search_frame, text="最大下载数:").grid(row=0, column=3, padx=5)
        self.max_downloads_var = tk.StringVar(value="50")
        self.max_downloads_entry = ttk.Entry(search_frame, textvariable=self.max_downloads_var, width=10)
        self.max_downloads_entry.grid(row=0, column=4, padx=5)
        
        # 清空目录按钮 - 移到这里
        self.clear_dir_btn = ttk.Button(search_frame, text="清空目录", command=self.clear_download_dir)
        self.clear_dir_btn.grid(row=0, column=5, padx=5)

    def create_download_list_area(self):
        # 下载列表框架
        list_frame = ttk.LabelFrame(self.main_frame, text="下载列表", padding="5")
        list_frame.grid(row=1, column=0, sticky=(tk.W, tk.E, tk.N, tk.S), pady=5)
        list_frame.columnconfigure(0, weight=1)
        list_frame.rowconfigure(0, weight=1)
        
        # 创建表格
        columns = ("选择", "序号", "歌曲名", "歌手", "状态")
        self.tree = ttk.Treeview(list_frame, columns=columns, show="headings", height=10)
        
        # 设置列标题和宽度
        self.tree.heading("选择", text="☐")
        self.tree.column("选择", width=50, anchor="center", stretch=False)  # 固定宽度
        self.tree.heading("序号", text="序号")
        self.tree.column("序号", width=50, anchor="center", stretch=False)  # 固定宽度
        self.tree.heading("歌曲名", text="歌曲名")
        self.tree.column("歌曲名", width=300, stretch=True)  # 可伸缩
        self.tree.heading("歌手", text="歌手")
        self.tree.column("歌手", width=150, stretch=True)  # 可伸缩
        self.tree.heading("状态", text="状态")
        self.tree.column("状态", width=100, stretch=False)  # 固定宽度
        
        # 添加滚动条
        scrollbar = ttk.Scrollbar(list_frame, orient=tk.VERTICAL, command=self.tree.yview)
        self.tree.configure(yscrollcommand=scrollbar.set)
        
        # 放置表格和滚动条
        self.tree.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
        scrollbar.grid(row=0, column=1, sticky=(tk.N, tk.S))
        
        # 下载按钮框架
        btn_frame = ttk.Frame(list_frame)
        btn_frame.grid(row=1, column=0, columnspan=2, sticky=(tk.W, tk.E), pady=5)
        
        # 全选/取消全选按钮
        self.select_all_btn = ttk.Button(btn_frame, text="全选", command=self.toggle_select_all)
        self.select_all_btn.pack(side=tk.LEFT, padx=5)
        
        # 下载按钮
        self.download_btn = ttk.Button(btn_frame, text="开始下载", command=self.start_download)
        self.download_btn.pack(side=tk.LEFT, padx=5)
        
        # 打开下载目录按钮
        self.open_dir_btn = ttk.Button(btn_frame, text="打开下载目录", command=self.open_download_dir)
        self.open_dir_btn.pack(side=tk.LEFT, padx=5)
        
        # 进度条
        self.progress_var = tk.DoubleVar()
        self.progress_bar = ttk.Progressbar(list_frame, 
                                          variable=self.progress_var,
                                          maximum=100,
                                          mode='determinate')
        self.progress_bar.grid(row=2, column=0, sticky=(tk.W, tk.E), padx=5, pady=5)
        
        # 进度标签
        self.progress_label = ttk.Label(list_frame, text="0%", width=6)
        self.progress_label.grid(row=2, column=1, padx=5, pady=5)
        
        # 绑定点击事件
        self.tree.bind('<Button-1>', self.on_click)

    def create_log_area(self):
        # 日志框架
        log_frame = ttk.LabelFrame(self.main_frame, text="日志", padding="5")
        log_frame.grid(row=2, column=0, sticky=(tk.W, tk.E, tk.N, tk.S), pady=5)
        log_frame.columnconfigure(0, weight=1)
        log_frame.rowconfigure(0, weight=1)
        
        # 日志文本框
        self.log_text = scrolledtext.ScrolledText(log_frame, height=10)  # 移除 width 参数
        self.log_text.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
        
        # 按钮框架
        btn_frame = ttk.Frame(log_frame)
        btn_frame.grid(row=1, column=0, sticky=(tk.W, tk.E), pady=(5, 0))  # 增加顶部间距，移除底部间距
        
        # 清除日志按钮
        self.clear_log_btn = ttk.Button(btn_frame, text="清除日志", command=self.clear_log)
        self.clear_log_btn.pack(side=tk.LEFT, padx=5)

    def create_status_bar(self):
        # 状态栏
        self.status_var = tk.StringVar()
        self.status_bar = ttk.Label(self.root, textvariable=self.status_var, relief=tk.SUNKEN)
        self.status_bar.grid(row=1, column=0, sticky=(tk.W, tk.E))  # 放在root的第二行
        self.status_var.set("就绪")

    def log(self, message):
        """添加日志信息"""
        self.log_text.insert(tk.END, f"{message}\n")
        self.log_text.see(tk.END)

    def clear_log(self):
        """清除日志"""
        self.log_text.delete(1.0, tk.END)

    def create_search_dialog(self):
        """创建搜索提示对话框"""
        self.search_dialog = tk.Toplevel(self.root)
        self.search_dialog.withdraw()  # 初始隐藏
        self.search_dialog.transient(self.root)  # 设置为主窗口的临时窗口
        self.search_dialog.overrideredirect(True)  # 无边框
        
        # 配置对话框大小和位置
        self.search_dialog.geometry("300x100")
        
        # 创建样式
        style = ttk.Style()
        style.configure("Search.TFrame", background='white')
        style.configure("Search.TLabel", background='white', font=("Arial", 12))
        
        # 创建主框架
        self.dialog_frame = ttk.Frame(self.search_dialog, style="Search.TFrame")
        self.dialog_frame.pack(expand=True, fill='both')
        
        # 进度提示标签
        self.dialog_label = ttk.Label(self.dialog_frame, text="", style="Search.TLabel")
        self.dialog_label.pack(expand=True, pady=20)
        
        # 设置窗口置顶
        self.search_dialog.lift()
        self.search_dialog.attributes('-topmost', True)

    def center_search_dialog(self):
        """居中显示搜索对话框"""
        if not hasattr(self, 'search_dialog'):
            return
            
        # 等待主窗口更新完成
        self.root.update_idletasks()
        
        # 获取主窗口位置和大小
        root_x = self.root.winfo_x()
        root_y = self.root.winfo_y()
        root_width = self.root.winfo_width()
        root_height = self.root.winfo_height()
        
        # 对话框大小
        dialog_width = 300
        dialog_height = 100
        
        # 计算居中位置
        x = root_x + (root_width - dialog_width) // 2
        y = root_y + (root_height - dialog_height) // 2
        
        # 设置位置
        self.search_dialog.geometry(f"{dialog_width}x{dialog_height}+{x}+{y}")

    def show_search_progress(self, text):
        """显示搜索进度"""
        if not hasattr(self, 'search_dialog'):
            return
            
        self.dialog_label.config(text=text)
        self.center_search_dialog()
        self.search_dialog.deiconify()
        self.search_dialog.lift()  # 确保窗口在最前
        self.search_dialog.attributes('-topmost', True)  # 保持窗口置顶
        self.root.update()

    def hide_search_progress(self):
        """隐藏搜索进度"""
        if hasattr(self, 'search_dialog'):
            self.search_dialog.withdraw()

    def update_search_result(self, i, song_id, mp3_url, song_name, artist_name):
        """在主线程中更新搜索结果"""
        if mp3_url and song_name and artist_name:
            self.tree.insert("", tk.END, values=("☐", i, song_name, artist_name, "等待下载"),
                           tags=(song_id, mp3_url))
            return True  # 返回True表示成功添加
        return False  # 返回False表示VIP歌曲

    def search_worker(self, keyword):
        """搜索工作线程"""
        try:
            self.search_btn.state(['disabled'])
            # 显示搜索进度
            self.root.after(0, lambda: self.show_search_progress("正在搜索..."))
            songs = self.manager.search_songs(keyword)
            
            # 使用after方法在主线程中更新UI
            if songs:
                valid_count = 0  # 记录有效歌曲数量
                vip_count = 0    # 记录VIP歌曲数量
                total_count = len(songs)  # 总歌曲数
                
                for i, song_id in enumerate(songs, 1):
                    if not self.is_searching:  # 检查是否被取消
                        break
                    # 更新搜索进度
                    progress_text = f"正在获取... ({i}/{total_count})\n已过滤 {vip_count} 首VIP歌曲"
                    self.root.after(0, lambda t=progress_text: self.show_search_progress(t))
                    
                    # 获取歌曲信息
                    mp3_url, song_name, artist_name = self.manager.get_song_info(song_id)
                    
                    # 使用after方法在主线程中更新UI，并检查是否为VIP歌曲
                    success = False
                    self.root.after(0, lambda: setattr(self, '_temp_result', 
                        self.update_search_result(valid_count + 1, song_id, mp3_url, song_name, artist_name)))
                    self.root.update()
                    if hasattr(self, '_temp_result'):
                        success = self._temp_result
                        delattr(self, '_temp_result')
                    
                    if success:
                        valid_count += 1
                    else:
                        vip_count += 1
                    
                    time.sleep(0.1)  # 添加小延迟，避免请求过快
                
                if valid_count > 0:
                    self.root.after(0, lambda: self.status_var.set(
                        f"找到 {valid_count} 首可下载歌曲 (共 {total_count} 首，{vip_count} 首VIP歌曲被过滤)"))
                else:
                    self.root.after(0, lambda: self.status_var.set(
                        f"未找到可下载歌曲 (共 {total_count} 首，全部为VIP歌曲)"))
            else:
                self.root.after(0, lambda: self.status_var.set("未找到歌曲"))
                
        except Exception as e:
            self.root.after(0, lambda: self.log(f"搜索出错: {str(e)}"))
            self.root.after(0, lambda: self.status_var.set("搜索失败"))
        finally:
            self.root.after(0, lambda: self.search_btn.state(['!disabled']))
            self.root.after(0, self.hide_search_progress)  # 隐藏进度提示
            self.is_searching = False

    def search_songs(self):
        """搜索歌曲"""
        if self.is_searching:
            # 如果正在搜索，则取消搜索
            self.is_searching = False
            self.search_btn.state(['!disabled'])
            self.hide_search_progress()  # 隐藏进度提示
            self.status_var.set("搜索已取消")
            return
            
        keyword = self.search_var.get().strip()
        if not keyword:
            messagebox.showwarning("警告", "请输入歌手名")
            return
            
        # 清空现有列表
        for item in self.tree.get_children():
            self.tree.delete(item)
            
        self.status_var.set("正在搜索...")
        self.log(f"开始搜索: {keyword}")
        
        # 启动搜索线程
        self.is_searching = True
        self.search_thread = threading.Thread(target=self.search_worker, args=(keyword,))
        self.search_thread.daemon = True
        self.search_thread.start()

    def download_worker(self):
        """下载工作线程"""
        start_time = time.time()
        total_downloads = self.song_queue.qsize()
        success_count = 0
        failed_count = 0
        
        # 重置进度条
        self.root.after(0, lambda: self.progress_var.set(0))
        self.root.after(0, lambda: self.progress_label.config(text="0%"))
        
        while not self.song_queue.empty() and self.is_downloading:
            try:
                item_id, song_info = self.song_queue.get()
                index, mp3_url, song_name, artist_name = song_info
                
                # 更新状态
                self.tree.set(item_id, "状态", "下载中...")
                self.root.update()
                
                try:
                    file_name = f"{index:02d}. {song_name} - {artist_name}"
                    file_name = "".join(c for c in file_name if c not in r'\/:*?"<>|')
                    file_path = os.path.join(self.manager.mp3_dir, f"{file_name}.mp3")
                    
                    # 下载文件并显示进度
                    response = requests.get(mp3_url, stream=True)
                    response.raise_for_status()
                    
                    # 获取文件大小
                    total_size = int(response.headers.get('content-length', 0))
                    block_size = 8192
                    downloaded = 0
                    
                    with open(file_path, 'wb') as f:
                        for chunk in response.iter_content(chunk_size=block_size):
                            if chunk and self.is_downloading:
                                f.write(chunk)
                                downloaded += len(chunk)
                                # 更新单个文件的下载进度
                                if total_size:
                                    file_progress = (downloaded / total_size) * 100
                                    # 计算总体进度
                                    total_progress = ((success_count + file_progress/100) / total_downloads) * 100
                                    self.root.after(0, lambda p=total_progress: self.update_progress(p))
                    
                    self.tree.set(item_id, "状态", "完成")
                    self.log(f"下载完成: {file_name}")
                    success_count += 1
                    # 更新总体进度
                    total_progress = (success_count / total_downloads) * 100
                    self.root.after(0, lambda p=total_progress: self.update_progress(p))
                    
                except Exception as e:
                    self.tree.set(item_id, "状态", "下载失败")
                    self.log(f"下载失败: {song_name} - {str(e)}")
                    failed_count += 1
                
                self.song_queue.task_done()
                
            except Exception as e:
                self.log(f"下载过程出错: {str(e)}")
                failed_count += 1
                continue
        
        # 计算总耗时
        total_time = time.time() - start_time
        
        # 下载完成后的处理
        if not self.song_queue.empty():
            self.status_var.set("下载已暂停")
            self.log("\n下载已暂停:")
        else:
            self.status_var.set("下载完成")
            self.log("\n下载任务完成:")
            
        # 打印统计信息
        self.log(f"总计划下载: {total_downloads} 首")
        self.log(f"成功下载: {success_count} 首")
        self.log(f"下载失败: {failed_count} 首")
        self.log(f"总耗时: {total_time:.2f} 秒")
        
        # 如果有成功下载的歌曲，显示保存目录
        if success_count > 0:
            save_dir = os.path.abspath(self.manager.mp3_dir)
            self.log(f"文件保存目录: {save_dir}")
        
        self.download_btn.config(text="开始下载")
        self.download_btn.state(['!disabled'])

    def start_download(self):
        """开始或暂停下载"""
        if self.is_downloading:
            # 如果正在下载，则暂停
            self.is_downloading = False
            self.status_var.set("正在停止下载...")
            self.download_btn.config(text="开始下载")
            return
            
        items = self.tree.get_children()
        if not items:
            messagebox.showwarning("警告", "下载列表为空")
            return
            
        # 获取选中的项目
        selected_items = [item for item in items if self.tree.set(item, "选择") == "☑"]
        if not selected_items:
            messagebox.showwarning("警告", "请点击歌曲前的☐选择要下载的歌曲")
            return
            
        try:
            max_downloads = int(self.max_downloads_var.get())
        except ValueError:
            messagebox.showerror("错误", "请输入有效的最大下载数")
            return
        
        # 准备下载队列
        self.song_queue = Queue()
        for i, item_id in enumerate(selected_items, 1):
            if i > max_downloads:
                break
            
            values = self.tree.item(item_id)['values']
            tags = self.tree.item(item_id)['tags']
            if len(tags) >= 2:  # 确保有足够的标签信息
                mp3_url = tags[1]
                if values[4] != "VIP无法下载" and values[4] != "完成":  # 注意：状态列的索引变为4
                    self.song_queue.put((item_id, (i, mp3_url, values[2], values[3])))  # 更新索引
        
        if self.song_queue.empty():
            messagebox.showinfo("提示", "没有可下载的歌曲")
            return
        
        # 开始下载
        self.is_downloading = True
        self.status_var.set("正在下载...")
        self.download_btn.config(text="停止下载")
        self.download_btn.state(['disabled'])
        
        # 启动下载线程
        self.download_thread = threading.Thread(target=self.download_worker)
        self.download_thread.daemon = True
        self.download_thread.start()

    def on_click(self, event):
        """处理表格点击事件"""
        region = self.tree.identify_region(event.x, event.y)
        item = self.tree.identify_row(event.y)
        if item:
            if region == "cell" or region == "tree":
                # 获取点击的列
                column = self.tree.identify_column(event.x)
                # 如果点击第一列或整行，切换选择状态
                if column == "#1" or region == "tree":
                    current_state = self.tree.set(item, "选择")
                    # 切换选择状态
                    new_state = "☑" if current_state in ("☐", "") else "☐"
                    self.tree.set(item, "选择", new_state)

    def toggle_select_all(self):
        """切换全选/取消全选状态"""
        items = self.tree.get_children()
        if not items:
            return
            
        # 检查当前是否全选
        all_selected = all(self.tree.set(item, "选择") == "☑" for item in items)
        
        # 切换状态
        new_state = "☐" if all_selected else "☑"
        for item in items:
            self.tree.set(item, "选择", new_state)
        
        # 更新按钮文本
        self.select_all_btn.config(text="取消全选" if new_state == "☑" else "全选")

    def on_closing(self):
        """关闭窗口时的处理"""
        if self.is_downloading or self.is_searching:
            if not messagebox.askokcancel("确认", "下载或搜索正在进行中，确定要退出吗？"):
                return
            self.is_downloading = False
            self.is_searching = False
        
        if messagebox.askokcancel("退出", "确定要退出吗?"):
            self.root.destroy()

    def open_download_dir(self):
        """打开下载目录"""
        download_path = os.path.abspath(self.manager.mp3_dir)
        try:
            if os.path.exists(download_path):
                # Windows
                if os.name == 'nt':
                    os.startfile(download_path)
                # macOS
                elif os.name == 'darwin':
                    os.system(f'open "{download_path}"')
                # Linux
                else:
                    os.system(f'xdg-open "{download_path}"')
                self.log(f"已打开下载目录: {download_path}")
            else:
                messagebox.showwarning("警告", "下载目录不存在")
        except Exception as e:
            self.log(f"打开下载目录失败: {str(e)}")
            messagebox.showerror("错误", f"无法打开下载目录: {str(e)}")

    def update_progress(self, progress):
        """更新进度条和标签"""
        self.progress_var.set(progress)
        self.progress_label.config(text=f"{progress:.1f}%")

    def delete_selected(self):
        """删除选中的文件"""
        # 获取选中的项目
        selected_items = [item for item in self.tree.get_children() if self.tree.set(item, "选择") == "☑"]
        
        if not selected_items:
            messagebox.showwarning("警告", "请选择要删除的文件")
            return
        
        # 确认删除
        if not messagebox.askyesno("确认", "确定要删除选中的文件吗？\n此操作将同时删除本地文件！"):
            return
        
        deleted_count = 0
        failed_count = 0
        
        for item in selected_items:
            try:
                # 获取文件信息
                values = self.tree.item(item)['values']
                if len(values) >= 4:  # 确保有足够的值
                    song_name = values[2]
                    artist_name = values[3]
                    index = values[1]
                    
                    # 构建文件名
                    file_name = f"{index:02d}. {song_name} - {artist_name}"
                    file_name = "".join(c for c in file_name if c not in r'\/:*?"<>|')
                    file_path = os.path.join(self.manager.mp3_dir, f"{file_name}.mp3")
                    
                    # 删除文件
                    if os.path.exists(file_path):
                        os.remove(file_path)
                        self.log(f"已删除文件: {file_name}")
                        deleted_count += 1
                    else:
                        self.log(f"文件不存在: {file_name}")
                        failed_count += 1
                    
                    # 从列表中移除
                    self.tree.delete(item)
                
            except Exception as e:
                self.log(f"删除失败: {str(e)}")
                failed_count += 1
        
        # 显示删除结果
        if deleted_count > 0 or failed_count > 0:
            result_message = f"删除完成\n成功: {deleted_count} 个\n失败: {failed_count} 个"
            messagebox.showinfo("删除结果", result_message)
            self.status_var.set(f"删除完成 - 成功: {deleted_count}, 失败: {failed_count}")

    def clear_download_dir(self):
        """清空下载目录"""
        # 获取下载目录路径
        download_path = os.path.abspath(self.manager.mp3_dir)
        
        # 检查目录是否存在
        if not os.path.exists(download_path):
            messagebox.showwarning("警告", "下载目录不存在")
            return
        
        # 获取目录中的所有MP3文件
        mp3_files = [f for f in os.listdir(download_path) if f.lower().endswith('.mp3')]
        
        if not mp3_files:
            messagebox.showinfo("提示", "下载目录已经是空的")
            return
        
        # 确认清空操作
        if not messagebox.askyesno("确认", f"确定要删除下载目录中的所有文件吗？\n共有 {len(mp3_files)} 个文件\n此操作不可恢复！"):
            return
        
        # 执行删除操作
        deleted_count = 0
        failed_count = 0
        
        for filename in mp3_files:
            try:
                file_path = os.path.join(download_path, filename)
                os.remove(file_path)
                self.log(f"已删除文件: {filename}")
                deleted_count += 1
            except Exception as e:
                self.log(f"删除失败 {filename}: {str(e)}")
                failed_count += 1
        
        # 清空下载列表
        for item in self.tree.get_children():
            if self.tree.set(item, "状态") == "完成":  # 只删除已下载完成的项目
                self.tree.delete(item)
        
        # 显示删除结果
        result_message = f"目录清空完成\n成功: {deleted_count} 个\n失败: {failed_count} 个"
        messagebox.showinfo("清空结果", result_message)
        self.status_var.set(f"目录清空完成 - 成功: {deleted_count}, 失败: {failed_count}")

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

def main():
    root = tk.Tk()
    app = MusicManagerGUI(root)
    
    # 获取屏幕尺寸
    screen_width = root.winfo_screenwidth()
    screen_height = root.winfo_screenheight()
    
    # 获取窗口尺寸
    window_width = 800
    window_height = 600
    
    # 计算窗口居中位置
    x = (screen_width - window_width) // 2
    y = (screen_height - window_height) // 2
    
    # 设置窗口位置
    root.geometry(f"{window_width}x{window_height}+{x}+{y}")
    
    # 设置最小窗口大小
    root.minsize(800, 600)
    
    root.mainloop()

if __name__ == "__main__":
    main()