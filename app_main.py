# Copyright (C) [2026] [晨曦微光]
# 此软件受著作权法保护。未经明确书面许可，任何单位或个人不得复制、分发、修改或用于商业用途。
# APP名称：[晨曦智能打卡]
# 版本号：1.0.0

"""
应用主文件和配置
"""


import os
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
    
    def build(self):
        """构建应用界面"""
        self.title = "晨曦智能打卡"
        self.app_version = "1.1.0"
        
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

        # 确保启动后首先显示登录页（尤其是移动端，避免启动后直接回到桌面）
        self.sm.current = 'login'

        return self.sm
    
    def on_start(self):
        """应用启动时调用"""
        # 设置窗口背景色（#11264F）
        Window.clearcolor = (0.0667, 0.149, 0.3098, 1)

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

        注意：部分机型在启动阶段可能会短暂触发 pause/resume。
        若这里返回 False，会导致应用被系统直接关闭，表现为“点击后立刻回到桌面/像进入后台”。

        因此这里返回 True，让系统允许暂停；真正的“退出”统一由返回键/关闭按钮的确认弹窗处理。
        """
        return True


    
    def on_resume(self):
        """应用恢复时调用（移动端）"""
        try:
            Window.show()
        except Exception:
            pass

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
