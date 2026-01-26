#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# Copyright (C) [2026] [晨曦微光]
# 移动端优化启动脚本

import os
import sys

# 添加当前目录到Python路径
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

# 移动端环境变量设置
os.environ['KIVY_NO_CONSOLELOG'] = '1'
os.environ['KIVY_WINDOW'] = 'sdl2'
os.environ['KIVY_GRAPHICS'] = 'sdl2'

# 针对移动端的优化配置
os.environ['KIVY_DPI'] = '160'

# 禁用文件监控（移动端不需要）
os.environ['KIVY_NO_FILELOG'] = '1'

# 导入主应用
from app_main import AttendanceApp

if __name__ == '__main__':
    # 设置应用为移动端模式
    os.environ['APP_MOBILE_MODE'] = '1'
    
    # 启动应用
    app = AttendanceApp()
    app.run()