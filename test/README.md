# 音乐下载器说明文档

## 一、软件功能
这是一个音乐下载工具，可以通过歌手名称搜索并下载歌曲。

## 二、使用方法
1. 运行程序后，输入歌手名称（如：胡彦斌）
2. 输入要下载的歌曲数量（留空表示下载全部）
3. 程序会自动搜索并下载歌曲到 mp3 目录

## 三、技术实现细节

### 1. 搜索歌曲接口
- 请求URL: `https://music.91q.com/v1/search`
- 请求方法: GET
- 参数说明:
  ```
  appid: 16073360
  pageNo: 页码（从1开始）
  pageSize: 每页数量（固定为20）
  timestamp: 当前时间戳
  type: 1
  word: 搜索关键词
  sign: MD5签名
  ```

### 2. 分页请求示例
1. 第一页请求：
   ```python
   params = {
       "appid": "16073360",
       "pageNo": "1",
       "pageSize": "20",
       "timestamp": "1234567890",
       "type": "1",
       "word": "胡彦斌"  # 签名时使用解码后的文字
   }
   ```

2. 第二页请求：
   ```python
   params = {
       "appid": "16073360",
       "pageNo": "2",  # 修改页码
       "pageSize": "20",
       "timestamp": "1234567890",
       "type": "1",
       "word": "胡彦斌"
   }
   ```

3. URL编码示例：
   ```python
   # 关键词编码
   encoded_word = requests.utils.quote("胡彦斌")  # 结果：%E8%83%A1%E5%BD%A6%E6%96%8C
   
   # 实际请求URL
   url = f"https://music.91q.com/v1/search?sign={sign}&word={encoded_word}&type=1&pageNo=2&pageSize=20&appid=16073360&timestamp={timestamp}"
   ```

### 3. 签名生成过程
1. 准备参数：
   ```javascript
   const params = {
       appid: "16073360",
       pageNo: "1",
       pageSize: "20",
       timestamp: "1234567890",
       type: "1",
       word: "关键词"  // 需要先进行 URL 解码
   }
   ```

2. 构建签名字符串：
   - 将参数按照字母顺序排序
   - 使用 `key=value` 格式连接
   - 使用 `&` 连接多个参数
   - 最后添加密钥
   ```javascript
   // 最终的签名字符串形如：
   appid=16073360&pageNo=1&pageSize=20&timestamp=1234567890&type=1&word=关键词0b50b02fd0d73a9c4c8c3a781c30845f
   ```

3. 对构建的字符串进行 MD5 加密，得到最终的 sign

### 4. 获取下载链接接口
- 请求URL: `https://music.91q.com/v1/song/tracklink`
- 请求方法: GET
- 参数说明:
  ```
  appid: 16073360
  timestamp: 当前时间戳
  TSID: 歌曲ID
  sign: MD5签名
  ```

### 5. 下载链接签名生成
1. 准备参数：
   ```javascript
   const params = {
       TSID: "歌曲ID",
       appid: "16073360",
       timestamp: "1234567890"
   }
   ```

2. 构建签名字符串：
   - 将参数按照字母顺序排序
   - 使用 `key=value` 格式连接
   - 使用 `&` 连接多个参数
   - 最后添加密钥
   ```javascript
   // 最终的签名字符串形如：
   TSID=歌曲ID&appid=16073360&timestamp=12345678900b50b02fd0d73a9c4c8c3a781c30845f
   ```

3. 对构建的字符串进行 MD5 加密，得到最终的 sign

## 四、注意事项
1. VIP 歌曲无法获取下载链接
2. 下载的文件会按顺序命名：`序号. 歌名 - 歌手.mp3`
3. 文件保存在程序所在目录的 mp3 文件夹中
4. 每次请求间隔 1 秒，避免请求过于频繁
5. 最多获取 10 页数据（每页 20 首歌）
6. 签名生成时注意：
   - 参数必须按字母顺序排序
   - 关键词必须先进行 URL 解码
   - 密钥必须添加在最后
7. 分页请求注意：
   - 页码从1开始
   - 每页固定返回20条数据
   - 每次请求需要新的时间戳和签名
   - 关键词在签名时使用原文，请求时使用编码后的文字