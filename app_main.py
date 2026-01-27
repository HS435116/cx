# Copyright (C) [2026] [晨曦微光]
# 此软件受著作权法保护。未经明确书面许可，任何单位或个人不得复制、分发、修改或用于商业用途。
# APP名称：[晨曦智能打卡]
# 版本号：1.0.0

"""
应用主文件和配置
"""


import os
import time
import traceback
from datetime import datetime


from kivy.config import Config

from kivy.resources import resource_add_path

# 设置默认中文字体（必须在导入其他Kivy模块前设置）
_font_path = os.path.join(os.path.dirname(__file__), 'assets', 'fonts', 'simhei.ttf')
if os.path.exists(_font_path):
    Config.set('kivy', 'default_font', str(['Chinese', _font_path, _font_path, _font_path, _font_path]))
    resource_add_path(os.path.dirname(_font_path))

from kivy.app import App
from kivy.uix.screenmanager import ScreenManager
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.label import Label
from kivy.uix.button import Button
from kivy.uix.popup import Popup
from kivy.core.window import Window
from kivy.metrics import dp
from kivy.utils import platform as kivy_platform
from kivy.clock import Clock




# 导入所有屏幕
from main_screen import MainScreen
from settings_screen import SettingsScreen
from admin_screen import AdminScreen, AdManagerScreen, UserSearchScreen
from main import db



class AttendanceApp(App):
    """打卡应用主类"""

    def _log_exception(self, where: str):
        """把启动异常写入本地文件，方便在手机上定位“点开就回桌面/像进后台”的问题。"""
        try:
            log_dir = getattr(self, 'user_data_dir', None) or os.getcwd()
            log_path = os.path.join(log_dir, 'startup_error.log')
            with open(log_path, 'a', encoding='utf-8') as f:
                f.write(f"\n[{datetime.now().isoformat(timespec='seconds')}] {where}\n")
                f.write(traceback.format_exc())
                f.write("\n")
        except Exception:
            # 日志写入失败时忽略（避免二次异常）
            pass

    def build(self):
        """构建应用界面

        华为/鸿蒙部分机型上如果启动阶段抛异常，通常表现为“点开后立刻回到桌面/像进入后台”。
        这里做兜底：捕获异常并显示一个错误页，同时把 traceback 写入 startup_error.log。
        """
        self.title = "晨曦智能打卡"
        self.app_version = "1.1.0"

        try:
            # 创建屏幕管理器
            self.sm = ScreenManager()

            # 添加登录屏幕（从第一部分导入）
            from main import LoginScreen, RegisterScreen
            self.sm.add_widget(LoginScreen(name='login'))
            self.sm.add_widget(RegisterScreen(name='register'))

            # 添加主功能屏幕
            self.sm.add_widget(MainScreen(name='main'))
            self.sm.add_widget(SettingsScreen(name='settings'))
            self.sm.add_widget(AdminScreen(name='admin'))
            self.sm.add_widget(UserSearchScreen(name='user_search'))
            self.sm.add_widget(AdManagerScreen(name='ad_manager'))

            # 确保启动后首先显示登录页
            self.sm.current = 'login'

            return self.sm
        except Exception:
            self._log_exception('build() failed')

            # 极简错误页（尽量不依赖复杂组件）
            content = BoxLayout(orientation='vertical', spacing=dp(12), padding=dp(20))
            content.add_widget(Label(text='应用启动失败', font_size=dp(20), color=(1, 1, 1, 1)))
            content.add_widget(Label(
                text='请将手机连接电脑，用 adb logcat 查看错误，或在应用数据目录中查找 startup_error.log。',
                halign='left', valign='top', color=(0.9, 0.95, 1, 1)
            ))
            btn = Button(text='退出', size_hint=(1, None), height=dp(44), background_color=(0.8, 0.2, 0.2, 1))
            btn.bind(on_press=lambda *_: self.confirm_exit(None))
            content.add_widget(btn)
            return content

    
    def on_start(self):
        """应用启动时调用"""
        # 设置窗口背景色（#11264F）
        Window.clearcolor = (0.0667, 0.149, 0.3098, 1)

        # 记录启动时间：用于区分“启动阶段的短暂 pause”与“用户把应用切到后台”
        self._startup_ts = time.time()


        # 不允许后台运行：用户关闭/返回时提示并直接退出；应用进入后台时也不保持运行
        Window.bind(on_request_close=self.on_request_close)
        Window.bind(on_keyboard=self.on_keyboard)




        # 移动端：不强制全屏/不强制 Window.show。
        # 部分机型（如部分华为系统）在启动时强制全屏/强制 show 可能触发异常的 pause/resume，
        # 表现为“点击后立刻回到桌面/像进入后台”。
        from kivy.utils import platform as kivy_platform
        if kivy_platform not in ('android', 'ios'):
            Window.size = (360, 640)

        # 初始化默认管理员账号（仅开发环境）
        if os.environ.get('APP_DEV_MODE') == '1':
            try:
                from main import db
                db.add_user('admin', 'admin123', is_admin=True)
            except Exception:
                pass

        # 发布版不在运行时“清理文件”，避免误删导致异常
        # 如需清理，请在构建/发布流程中处理





    
    def _ensure_foreground_and_login(self, *args):
        # 兼容保留：只做界面切换，不做 Window.show/强制拉前台。
        # 如需在特定机型上拉前台，应通过 Android 端 Activity 处理。
        try:
            if getattr(self, 'sm', None):
                self.sm.current = 'login'
        except Exception:
            pass



    def on_keyboard(self, window, key, scancode, codepoint, modifiers):
        """拦截移动端返回键，避免系统默认行为把窗口直接送入后台"""
        # Android 返回键通常是 27 (ESC)
        if key in (27,):
            return self.on_request_close()
        return False

    def on_pause(self):
        """应用暂停时调用（移动端）

        目标：不允许长期后台运行。
        但华为/鸿蒙等机型在“刚启动”的几秒内可能会触发一次短暂 pause，
        如果直接 return False 会导致“点开就回桌面”。

        策略：启动后 5 秒内的 pause 视为系统抖动，允许（return True）；
        5 秒后如果进入后台，则直接结束应用（return False）。
        """
        try:
            if time.time() - getattr(self, '_startup_ts', 0) < 5:
                return True
        except Exception:
            return True
        return False



    
    def on_resume(self):
        """应用恢复时调用（移动端）"""
        try:
            main_screen = self.sm.get_screen('main')
            main_screen.evaluate_auto_mode()
        except Exception:
            pass



    def on_request_close(self, *args):
        if getattr(self, '_force_close', False):
            return False
        if getattr(self, '_exit_popup', None):
            return True

        current_screen = None
        try:
            current_screen = self.sm.current
        except Exception:
            current_screen = None

        # 登录/注册页：禁止“后台运行”，避免用户误触导致看起来像“进后台/闪退”
        if current_screen == 'register':
            # 注册页按返回键：返回上一级（登录页）
            try:
                self.sm.current = 'login'
            except Exception:
                pass
            return True

        if current_screen == 'login':
            # 登录页按返回键：只允许退出（可取消）
            content = BoxLayout(orientation='vertical', spacing=dp(12), padding=dp(20))
            content.add_widget(Label(text='确认退出应用？', color=(1, 1, 1, 1)))

            btn_layout = BoxLayout(size_hint=(1, None), height=dp(44), spacing=dp(10))
            cancel_btn = Button(text='取消', background_color=(0.2, 0.6, 0.8, 1))
            exit_btn = Button(text='退出系统', background_color=(0.8, 0.2, 0.2, 1))
            btn_layout.add_widget(cancel_btn)
            btn_layout.add_widget(exit_btn)
            content.add_widget(btn_layout)

            popup = Popup(title='退出提醒', content=content, size_hint=(0.86, 0.32), background_color=(0.0667, 0.149, 0.3098, 1), background='')
            self._exit_popup = popup

            cancel_btn.bind(on_press=lambda x: popup.dismiss())
            exit_btn.bind(on_press=lambda x: self.confirm_exit(popup))

            popup.bind(on_dismiss=lambda x: setattr(self, '_exit_popup', None))
            popup.open()
            return True

        # 其他页面：不提供后台运行，统一提示“确认退出”
        content = BoxLayout(orientation='vertical', spacing=dp(12), padding=dp(20))
        content.add_widget(Label(text='确认退出应用？', color=(1, 1, 1, 1)))

        btn_layout = BoxLayout(size_hint=(1, None), height=dp(44), spacing=dp(10))
        cancel_btn = Button(text='取消', background_color=(0.2, 0.6, 0.8, 1))
        exit_btn = Button(text='退出系统', background_color=(0.8, 0.2, 0.2, 1))
        btn_layout.add_widget(cancel_btn)
        btn_layout.add_widget(exit_btn)
        content.add_widget(btn_layout)

        popup = Popup(title='退出提醒', content=content, size_hint=(0.86, 0.32), background_color=(0.0667, 0.149, 0.3098, 1), background='')
        self._exit_popup = popup

        cancel_btn.bind(on_press=lambda x: popup.dismiss())
        exit_btn.bind(on_press=lambda x: self.confirm_exit(popup))

        popup.bind(on_dismiss=lambda x: setattr(self, '_exit_popup', None))
        popup.open()
        return True





    def confirm_exit(self, popup):

        if popup:
            popup.dismiss()
        self._force_close = True
        try:
            self.stop()
        finally:
            os._exit(0)



# 应用配置

if __name__ == '__main__':
    # 设置默认管理员账号（仅开发环境）
    print("初始化数据库...")
    
    # 确保所有屏幕类都已导入
    import sys
    sys.path.append('.')
    
    # 运行应用
    AttendanceApp().run()
