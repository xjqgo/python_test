# 音乐下载器实现要点

## 一、基础结构
1. 类名：`MusicManager`
2. 主要功能：搜索歌曲、获取下载链接、下载MP3文件
3. 运行环境：支持打包为exe，兼容命令行和GUI环境
4. 文件结构：
   ```
   project/
   ├── mp3/                # 下载文件保存目录
   ├── music_manager.py    # 主实现文件
   └── requirements.txt    # 项目依赖
   ```

## 二、关键接口
### 1. 搜索接口
- URL: `https://music.91q.com/v1/search`
- 请求方法: GET
- 请求头:
  ```python
  headers = {
      "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36",
      "Accept": "application/json, text/plain, */*",
      "Origin": "https://music.91q.com"
  }
  ```
- 关键参数:
  ```python
  params = {
      "appid": "16073360",
      "pageNo": page_no,
      "pageSize": "20",
      "timestamp": timestamp,
      "type": "1",
      "word": keyword,  # 需要URL编码
      "sign": sign      # MD5签名
  }
  ```
- 签名生成规则：
  ```python
  sign_str = f"appid=16073360&pageNo={page_no}&pageSize=20&timestamp={timestamp}&type=1&word={keyword}0b50b02fd0d73a9c4c8c3a781c30845f"
  sign = hashlib.md5(sign_str.encode()).hexdigest()
  ```
- 响应示例：
  ```json
  {
    "data": {
      "typeTrack": [
        {
          "id": "song_id",
          "title": "歌曲名称",
          "artist": [
            {
              "name": "歌手名称"
            }
          ]
        }
      ]
    }
  }
  ```

### 2. 下载链接获取接口
- URL: `https://music.91q.com/v1/song/tracklink`
- 请求方法: GET
- 请求头：与搜索接口相同
- 关键参数:
  ```python
  params = {
      "appid": "16073360",
      "timestamp": timestamp,
      "TSID": tsid,
      "sign": sign
  }
  ```
- 签名生成规则：
  ```python
  sign_str = f"TSID={tsid}&appid=16073360&timestamp={timestamp}0b50b02fd0d73a9c4c8c3a781c30845f"
  sign = hashlib.md5(sign_str.encode()).hexdigest()
  ```
- 响应示例：
  ```json
  {
    "data": {
      "path": "下载链接URL",
      "title": "歌曲名称",
      "artist": [
        {
          "name": "歌手名称"
        }
      ]
    }
  }
  ```

## 三、核心功能实现
1. 搜索歌曲
   - 支持分页搜索（默认每页20条）
   - 自动处理中文关键词编码（使用 requests.utils.quote）
   - 提取歌曲信息：
     ```python
     title = song.get('title', '未知')
     song_id = song.get('id', '未知')
     artists = song.get('artist', [])
     artist_names = [artist.get('name', '未知') for artist in artists]
     artist_names_str = " / ".join(artist_names)
     ```
   - 支持设置最大搜索页数（避免过多请求）

2. 获取下载链接
   - 处理签名验证（使用MD5加密）
   - 解析JSON响应获取MP3地址
   - 提取完整歌曲信息（标题、歌手、下载地址）
   - 错误处理和重试机制

3. 下载管理
   - 自动创建下载目录：
     ```python
     if not os.path.exists(self.mp3_dir):
         os.makedirs(self.mp3_dir)
     ```
   - 文件命名格式：`序号. 歌名 - 歌手.mp3`
   - 文件名处理：
     ```python
     file_name = "".join(c for c in file_name if c not in r'\/:*?"<>|')
     ```
   - 支持批量下载
   - 支持限制下载数量
   - 下载进度显示

4. 错误处理
   - 网络请求异常：
     ```python
     try:
         response = requests.get(url, headers=headers)
         response.raise_for_status()
     except Exception as e:
         print(f"请求失败: {e}")
     ```
   - VIP歌曲检测（通过响应数据判断）
   - JSON解析错误处理
   - 文件操作异常处理
   - 请求延迟处理（避免频繁请求）：
     ```python
     time.sleep(1)  # 请求间隔1秒
     ```

## 四、使用统计
1. 下载统计
   - 记录总歌曲数
   - 统计下载成功数
   - 统计VIP无法下载数
   - 计算总下载时间：
     ```python
     start_time = time.time()
     # 下载过程
     total_time = time.time() - start_time
     ```

2. 输出信息
   - 显示搜索结果：
     ```
     歌曲名: xxx, ID: xxx, 歌手: xxx
     ```
   - 显示下载进度
   - 显示保存路径：
     ```python
     save_dir = os.path.abspath(self.mp3_dir)
     print(f"文件保存目录: {save_dir}")
     ```
   - 显示统计结果：
     ```
     共有: xxx 首歌曲
     下载完成: xxx 首歌曲
     VIP无法下载: xxx 首歌曲
     总下载时间: xxx 秒
     ```

## 五、打包发布
1. exe打包支持
   ```python
   def is_running_in_exe():
       return getattr(sys, 'frozen', False)
   ```

2. 资源路径处理
   ```python
   def get_resource_path(relative_path):
       if is_running_in_exe():
           base_path = getattr(sys, '_MEIPASS', os.path.abspath("."))
       else:
           base_path = os.path.abspath(".")
       return os.path.join(base_path, relative_path)
   ```

3. 打包命令
   ```bash
   pyinstaller --onefile --name music_downloader music_manager.py
   ```

## 六、注意事项
1. 请求频率限制
   - 搜索请求间隔1秒
   - 下载请求适当延迟

2. 文件命名规范
   - 去除非法字符
   - 添加序号便于管理
   - 包含歌手信息

3. 用户交互
   - 清晰的进度显示
   - 友好的错误提示
   - 完整的统计信息

4. 性能优化
   - 避免重复请求
   - 合理的请求间隔
   - 异常情况处理

## 七、用户输入处理
1. 命令行参数处理
   ```python
   def get_user_input():
       try:
           # 基础输入
           keyword = input("请输入要下载的歌手名（如：胡彦斌）：")
           if not keyword.strip():
               raise ValueError("歌手名不能为空")

           # 下载数量输入
           max_downloads_input = input("请输入最大下载数（留空表示全部下载）：")
           max_downloads = None
           if max_downloads_input.strip():
               try:
                   max_downloads = int(max_downloads_input)
                   if max_downloads <= 0:
                       raise ValueError("下载数量必须大于0")
               except ValueError:
                   raise ValueError("请输入有效的数字")

           return keyword, max_downloads

       except ValueError as e:
           print(f"输入错误: {e}")
           return None, None
   ```

2. 输入验证
   - 关键词验证：
     ```python
     def validate_keyword(keyword: str) -> bool:
         """验证搜索关键词"""
         if not keyword or len(keyword.strip()) == 0:
             return False
         # 可以添加更多验证规则
         return True
     ```
   - 数量限制验证：
     ```python
     def validate_download_limit(limit: str) -> Optional[int]:
         """验证下载数量限制"""
         if not limit:
             return None
         try:
             num = int(limit)
             return num if num > 0 else None
         except ValueError:
             return None
     ```

3. 错误提示
   - 输入为空：
     ```
     请输入有效的歌手名！
     ```
   - 数字格式错误：
     ```
     下载数量必须是正整数！
     ```
   - 超出限制：
     ```
     下载数量不能超过100首！
     ```

4. 交互设计
   - 清晰的提示信息
   - 默认值处理
   - 重试机制：
     ```python
     def get_valid_input(prompt: str, validator, max_attempts: int = 3) -> Optional[str]:
         """获取有效输入"""
         for attempt in range(max_attempts):
             value = input(prompt)
             if validator(value):
                 return value
             print(f"输入无效，还有 {max_attempts - attempt - 1} 次尝试机会")
         return None
     ```

5. 输入处理最佳实践
   - 去除首尾空格
   - 特殊字符过滤
   - 长度限制
   - 编码处理：
     ```python
     def process_input(text: str) -> str:
         """处理用户输入"""
         # 去除首尾空格
         text = text.strip()
         # 限制长度
         text = text[:50]
         # 过滤特殊字符
         text = "".join(char for char in text if char.isprintable())
         return text
     ```

## 八、可扩展功能
1. 并发下载支持
2. 断点续传
3. 音质选择
4. 下载进度条
5. GUI界面
6. 播放列表导出
7. 歌词下载
8. 专辑封面下载 