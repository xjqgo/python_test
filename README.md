# 音乐下载器项目

## 项目概述

这是一个基于 Python 的音乐下载工具，提供图形界面让用户可以方便地搜索和下载歌曲。该工具支持从指定的音乐平台获取歌曲信息，并将歌曲下载到本地。

## 功能特性

- **图形界面**：提供直观的用户界面，支持鼠标和键盘操作。
- **搜索功能**：
  - 通过输入歌手名称快速搜索歌曲
  - 支持回车键快速搜索
  - 实时显示搜索进度
  - 自动过滤 VIP 歌曲
  - 批量并发处理，加快搜索速度
  - 搜索完成后显示详细统计信息
- **下载管理**：
  - 支持选择性下载，可勾选需要的歌曲
  - 支持全选/取消全选
  - 可随时暂停/继续下载
  - 实时显示下载状态和进度
  - 支持一键打开下载目录
  - 按序号顺序下载，保证文件名序号与列表一致
  - 支持清空下载目录
- **智能处理**：
  - 自动过滤无法下载的 VIP 歌曲
  - 显示详细的统计信息（可下载数量、VIP 数量等）
  - 记录下载耗时和成功率
  - 批量处理提升性能
- **用户友好**：
  - 界面布局清晰
  - 操作反馈及时
  - 错误提示友好
  - 支持日志查看和清理
  - 搜索进度弹窗提示
  - 文件序号保持一致性

## 使用方法

1. 运行程序，界面会自动在屏幕中央显示。
2. 在搜索框输入歌手名称（默认：胡彦斌）。
3. 点击搜索按钮或按回车键开始搜索。
4. 在搜索结果列表中勾选要下载的歌曲。
5. 设置最大下载数量（默认：50）。
6. 点击"开始下载"按钮开始下载。
7. 可以随时：
   - 点击"停止下载"暂停下载
   - 点击"打开下载目录"查看下载的文件
   - 点击"清空目录"删除所有下载的文件
   - 查看日志了解详细信息
   - 点击"清除日志"清空日志记录

## 技术细节

- **界面框架**：使用 Tkinter 构建图形界面
- **多线程处理**：
  - 搜索和下载过程使用独立线程
  - 使用线程池进行并发搜索
  - 批量处理提升性能
- **请求接口**：使用 HTTP GET 请求获取歌曲信息
- **签名生成**：通过 MD5 加密生成请求签名
- **文件管理**：
  - 自动创建并管理下载目录
  - 文件名序号与列表保持一致
  - 支持批量清理文件

## 环境要求

- Python 3.x
- 需要安装的库：
  - `requests`：`pip install requests`
  - `tkinter`：Python 标准库（通常默认安装）

## 贡献

欢迎对本项目提出建议或贡献代码。请在提交 Pull Request 前确保代码风格一致，并通过所有测试。

## 许可证

MIT License