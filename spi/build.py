import os
import sys
import shutil
from PyInstaller.__main__ import run as pyinstaller_run

# 获取当前脚本所在的目录
script_dir = os.path.dirname(os.path.abspath(__file__))
# 设置工作目录为脚本所在目录
os.chdir(script_dir)

# 清理之前的构建文件
def clean_build_files():
    for folder in ['build', 'dist']:
        if os.path.exists(folder):
            shutil.rmtree(folder)
            print(f'已清理 {folder} 文件夹')

# 打包参数
def build_exe():
    # 使用绝对路径确保能找到main.py
    main_py_path = os.path.join(script_dir, 'main.py')
    if not os.path.exists(main_py_path):
        print(f'错误: 找不到主程序文件 {main_py_path}')
        return
    
    # 使用绝对路径确保能找到jtool.dll
    dll_source_path = os.path.join(script_dir, 'spi', 'jtool.dll')
    if not os.path.exists(dll_source_path):
        print(f'错误: 找不到DLL文件 {dll_source_path}')
        return
    
    params = [
        main_py_path,           # 主程序入口（使用绝对路径）
        '--name=SPItool',       # 应用名称
        '--onefile',            # 打包成单个文件
        '--windowed',           # 不显示控制台窗口
        '--hidden-import=PySide6',
        '--hidden-import=PySide6.QtCore',
        '--hidden-import=PySide6.QtGui',
        '--hidden-import=PySide6.QtWidgets',
        '--hidden-import=yaml',
        f'--add-data={dll_source_path};spi',  # 使用绝对路径添加DLL文件
        '--clean',             
        '--noupx'              
    ]
    
    print('开始打包...')
    pyinstaller_run(params)
    print('打包完成！')

if __name__ == '__main__':
    clean_build_files()
    build_exe()