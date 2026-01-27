# 考勤系统 - Android APK 构建项目

## 项目简介
这是一个基于 Kivy/KivyMD 的智能考勤管理系统，支持签到、签退、数据统计等功能。

## 核心文件说明
- `app_main.py` - 应用程序入口点
- `main.py` - 主界面逻辑
- `main_screen.py` - 主屏幕功能
- `admin_screen.py` - 管理员功能
- `settings_screen.py` - 设置界面
- `database.py` - 数据库操作
- `mobile_launcher.py` - 移动端启动器
- `buildozer.spec` - Android 构建配置
- `requirements.txt` - Python 依赖列表

## 数据文件
- `attendance.json` - 考勤数据
- `users.json` - 用户数据
- `settings.json` - 系统设置

## 资源文件
- `assets/` - 应用图标、启动画面、字体等

## GitHub Actions 构建
项目已配置 GitHub Actions 自动构建，推送到 GitHub 后会自动构建发布产物（AAB/APK，具体以 workflow 为准）。

构建完成后，可在 Actions 页面下载构建产物。

## 本地构建（可选）
```bash
pip install buildozer
buildozer android debug
```

## 功能特性
- 用户注册/登录
- 签到/签退记录
- 数据统计与导出
- 管理员权限控制
- 移动端适配

