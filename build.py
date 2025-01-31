import PyInstaller.__main__
import os
import re

def get_version_from_file():
    with open('version.txt', 'r', encoding='utf-8') as file:
        content = file.read()
        # 使用正则表达式从 FileVersion 行提取版本号
        version_match = re.search(r"FileVersion', u'([\d.]+)'", content)
        if version_match:
            return version_match.group(1)
        return "1.0.0"  # 默认版本号

def build_exe():
    # 确保当前目录是项目根目录
    project_root = os.path.dirname(os.path.abspath(__file__))
    os.chdir(project_root)
    
    # 从 version.txt 获取版本号
    version = get_version_from_file()
    
    # PyInstaller 打包参数
    params = [
        'test/music_manager.py',  # 主程序文件
        f'--name=音乐下载器_v{version}',  # 生成的 exe 文件名，包含版本号
        '--onefile',  # 打包成单个 exe 文件
        '--console',  # 显示控制台窗口，方便查看输出和错误信息
        '--add-data=README.md;.',  # 添加说明文档
        '--version-file=version.txt',  # 添加版本信息文件
        '--clean',  # 清理临时文件
        '--workpath=build',  # 指定工作目录
        '--distpath=dist',  # 指定输出目录
    ]
    
    # 执行打包
    PyInstaller.__main__.run(params)

if __name__ == "__main__":
    build_exe() 