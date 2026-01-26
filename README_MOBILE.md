# 晨曦智能打卡 - 移动端构建指南

## 项目简介

晨曦智能打卡是一个基于 Kivy 的移动端打卡应用，支持位置验证、自动打卡、管理员补录等完整功能。

## 构建环境要求

- Python 3.8+
- Android SDK (API 31)
- Android NDK (25b)
- Java 8+
- Buildozer 1.4.0

## 快速开始

### 1. 环境准备

```bash
# 安装 Python 依赖
pip install -r requirements.txt

# 安装 Buildozer
pip install buildozer==1.4.0
```

### 2. 项目配置

```bash
# 运行配置脚本
python setup.py
```

### 3. 构建 APK

```bash
# 清理并构建发布版本
python build.py all

# 或者分步执行
python build.py clean    # 清理缓存
python build.py release  # 构建发布版本
```

## 项目结构

```
cswg/
├── buildozer.spec          # Buildozer 配置文件
├── mobile_launcher.py       # 移动端启动脚本
├── app_main.py             # 主应用文件
├── main.py                 # 核心功能模块
├── main_screen.py          # 主界面
├── admin_screen.py         # 管理员界面
├── settings_screen.py      # 设置界面
├── database.py             # 数据库模块
├── requirements.txt         # Python 依赖
├── setup.py               # 项目配置脚本
├── build.py               # 构建脚本
├── assets/                # 资源文件
│   ├── icon.png          # 应用图标
│   ├── presplash.png     # 启动画面
│   └── fonts/            # 字体文件
├── users.json            # 用户数据
├── attendance.json      # 打卡记录
└── settings.json         # 设置配置
```

## 功能特性

### 用户功能
- 用户注册/登录
- 指纹/面容识别（移动端）
- GPS 位置验证
- 智能打卡提醒
- 打卡记录查询
- 个人设置管理

### 管理员功能
- 用户管理
- 打卡记录审核
- 补卡操作
- 公告发布
- 数据统计

### 技术特性
- 跨平台支持 (Android/iOS)
- 离线数据存储
- 后台自动打卡
- 数据加密保护
- 响应式界面设计

## 权限说明

应用需要以下权限：

| 权限 | 用途 |
|------|------|
| INTERNET | 网络访问 |
| ACCESS_FINE_LOCATION | GPS 定位 |
| ACCESS_COARSE_LOCATION | 网络定位 |
| ACCESS_BACKGROUND_LOCATION | 后台定位 |
| WAKE_LOCK | 保持设备唤醒 |
| CAMERA | 摄像头权限 |
| WRITE_EXTERNAL_STORAGE | 写入存储 |
| READ_EXTERNAL_STORAGE | 读取存储 |
| VIBRATE | 振动提醒 |

## 构建配置

### buildozer.spec 关键配置

```ini
title = 智能打卡系统
package.name = attendanceapp
package.domain = com.chenxiAI.attendance

source.dir = .
source.main = mobile_launcher.py
source.include_exts = py,png,jpg,kv,atlas,json,ico,ttf

android.minapi = 21
android.targetSdkVersion = 31
android.api = 31
android.ndk = 25b
android.archs = arm64-v8a, armeabi-v7a

version = 1.1
version.name = 1.1.0

requirements = python3,kivy==2.1.0,kivymd==0.104.2,plyer==2.1.0,requests,sqlite3,android

android.permissions = INTERNET,ACCESS_FINE_LOCATION,ACCESS_COARSE_LOCATION,ACCESS_BACKGROUND_LOCATION,WAKE_LOCK,CAMERA,WRITE_EXTERNAL_STORAGE,READ_EXTERNAL_STORAGE,VIBRATE
android.features = android.hardware.location.gps
```

## 测试部署

### 1. 调试版本测试

```bash
# 构建调试版本
python build.py debug

# 安装到设备
adb install bin/attendanceapp-1.1-debug.apk
```

### 2. 发布版本部署

```bash
# 构建发布版本
python build.py release

# APK 签名（如果需要）
jarsigner -verbose -sigalg SHA1withRSA -digestalg SHA1 -keystore my-release-key.jks bin/attendanceapp-1.1-release-unsigned.apk chenxiweiguang

# 对齐 APK
zipalign -v 4 bin/attendanceapp-1.1-release-unsigned.apk bin/attendanceapp-1.1-release.apk
```

## 故障排除

### 常见问题

1. **构建失败: SDK/NDK 未找到**
   ```bash
   # 设置环境变量
   export ANDROID_HOME=/path/to/android-sdk
   export ANDROID_NDK_HOME=/path/to/android-ndk
   ```

2. **字体显示异常**
   - 确保 `assets/fonts/simhei.ttf` 文件存在
   - 检查字体文件权限

3. **位置权限问题**
   - 在 Android 设置中手动授予权限
   - 检查 GPS 是否开启

4. **应用崩溃**
   ```bash
   # 查看日志
   adb logcat | grep python
   ```

## 版本更新

### v1.1.0 (当前版本)
- 优化移动端性能
- 增强位置验证
- 改进用户界面
- 修复已知问题

### 即将发布
- iOS 版本支持
- 云数据同步
- 更多生物识别方式
- 高级统计分析

## 技术支持

如有问题，请检查：
1. 构建环境是否完整
2. 权限配置是否正确
3. 资源文件是否完整
4. 设备兼容性

## 版权信息

Copyright (C) [2026] [晨曦微光]

此软件受著作权法保护。未经明确书面许可，任何单位或个人不得复制、分发、修改或用于商业用途。