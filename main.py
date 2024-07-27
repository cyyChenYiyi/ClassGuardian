import datetime
import random
import sys
import os
from PyQt5.QtGui import QFont
import psutil
from PyQt5.QtCore import Qt, QUrl, QEvent, QTimer, QDateTime, QTime
from PyQt5.QtWidgets import QApplication, QHBoxLayout, QLabel, QMainWindow, QMessageBox, QLineEdit, QInputDialog, QDesktopWidget, QPushButton, QWidget
from PyQt5.QtWebEngineWidgets import QWebEngineView
from PyQt5.QtMultimedia import QMediaPlayer, QMediaContent
from PyQt5.QtMultimediaWidgets import QVideoWidget
import subprocess
from datetime import datetime

class BrowserWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        # 设置窗口标题和无边框风格
        self.setWindowTitle("ClassGuardian·课守护")
        self.setWindowFlags(Qt.FramelessWindowHint | Qt.WindowStaysOnTopHint | Qt.Tool)

        # 创建自定义标题栏
        self.titleBar = QWidget(self)
        self.titleBar.setStyleSheet("background-color: lightblue;")
        self.titleBar.setFixedHeight(50)  # 调整高度为50

        # 布局：标题和按钮放在标题栏中
        self.layout = QHBoxLayout(self.titleBar)
        self.layout.setContentsMargins(10, 0, 10, 0)  # 增加左侧边距以显示标题

        # 添加标题显示标签
        self.titleLabel = QLabel("ClassGuardian2·课守护", self.titleBar)
        self.titleLabel.setStyleSheet("color: black; background-color: transparent;")
        # 设置标签的字体为微软雅黑，字体大小为10
        font = QFont("微软雅黑", 11)
        self.titleLabel.setFont(font)
        self.layout.addWidget(self.titleLabel)
        self.layout.addStretch(1)  # 确保标题在左侧，按钮在右侧



        self.setMenuWidget(self.titleBar)




        # 初始化视频播放器
        self.videoPlayer = QMediaPlayer(None, QMediaPlayer.VideoSurface)
        self.videoWidget = QVideoWidget(self)
        self.setCentralWidget(self.videoWidget)
        self.videoPlayer.setVideoOutput(self.videoWidget)
        # 随机选择视频文件，确保文件扩展名正确
        self.video = random.choice(['D:/AD5(1).mp4', 'D:/AD5(1).mp4', 'D:/AD5(1).mp4', 'D:/AD5(1).mp4', 'D:/AD5(1).mp4'])
        self.videoPlayer.setMedia(QMediaContent(QUrl.fromLocalFile(self.video)))
        self.videoPlayer.play()
        self.videoPlayer.setMuted(True)  # type: ignore # 静音播放
        self.videoPlayer.mediaStatusChanged.connect(self.on_media_status_changed)

        # 初始化浏览器组件，但不显示直到视频播放完毕
        self.browser = QWebEngineView()
        self.browser.setZoomFactor(2.1)
        self.browser.loadFinished.connect(self.check_url_and_close)
        # 设置窗口全屏
        screen_geometry = QApplication.desktop().screenGeometry()
        self.resize(screen_geometry.width(), screen_geometry.height())
        self.setFixedSize(self.size())
        self.move(0, 0)

        # 定时器检查任务和USB插入
        self.timer = QTimer(self)
        self.timer.timeout.connect(self.check_task_manager_and_keep_on_top)
        self.timer.start(1000)
        self.usb_timer = QTimer(self)
        self.usb_timer.timeout.connect(self.check_usb_insertion)
        self.usb_timer.start(1000)

        # 日志文件路径
        self.log_file_path = os.path.join(os.environ['USERPROFILE'], 'Desktop', 'jilu.txt')
        if not os.path.exists(self.log_file_path):
            open(self.log_file_path, 'w').close()

    def on_media_status_changed(self, status):
        if status == QMediaPlayer.EndOfMedia:
            self.setCentralWidget(self.browser)
            self.browser.setHtml('''
<!DOCTYPE html>
<html lang="zh-CN">
<head>
    <meta charset="UTF-8">
    <title>网络状态检测</title>
    <script>
        // 当页面加载时立即检测网络状态
        function checkNetwork() {
            if (!navigator.onLine) {
                // 显示网络错误信息
                document.getElementById("networkStatus").style.display = 'block';
            } else {
                // 有网络时，延迟一秒后跳转，确保有足够的时间显示状态
                setTimeout(function() {
                    window.location.href = 'https://cyychenyiyi.github.io/ClassGuardian/2.0shouhu';
                }, 1000);
            }
        }

        document.addEventListener('DOMContentLoaded', checkNetwork);
        // 保持监听网络状态的变化
        window.addEventListener('online', checkNetwork);
        window.addEventListener('offline', function() {
            document.getElementById("networkStatus").style.display = 'block';
        });
    </script>
    <style>
        #networkStatus {
            display: none;
            margin: 20px;
            padding: 10px;
            border: 1px solid #f00;
            background-color: #fee;
            text-align: center;
        }
    </style>
</head>
<body>
    <div id="networkStatus">
        <h1>连接错误</h1>
        <p>请您检查网络连接。如果您的网络未出现问题，请联系ClassGuardian开发者。</p>
    </div>
</body>
</html>

            ''')

    def schedule_window_close(self, close_times):
        current_datetime = QDateTime.currentDateTime()
        for close_time in close_times:
            hour, minute = map(int, close_time.split(':'))
            close_datetime = QDateTime(current_datetime.date(), QTime(hour, minute))
            if close_datetime > current_datetime:
                delta_milliseconds = current_datetime.msecsTo(close_datetime)
                QTimer.singleShot(delta_milliseconds, self.close)
                break
    def check_url_and_close(self):
        url = self.browser.url().toString()
        if "https://cyychenyiyi.github.io/ClassGuardian/closeok" in url:
            self.close()

    def check_task_manager_and_keep_on_top(self):
        process_names_to_terminate = ['Taskmgr.exe', 'msedge.exe', '360chrome.exe']
        for process in psutil.process_iter(['pid', 'name']):
            if process.info['name'] in process_names_to_terminate:
                # 关闭所有实例
                for p in psutil.process_iter(['pid', 'name']):
                    if p.info['name'] == process.info['name']:
                        p.terminate()
                self.log_abnormal_behavior(process.info['name'])
                self.show_warning()
                break  # 避免重复警告
    def start_tianqi_mind(*args, **kwargs):
        import subprocess
        import os

        # 获取当前工作目录
        cwd = os.getcwd()
        # 定义程序的完整路径
        exe_path = os.path.join(cwd, "天启mind.exe")

        # 打印路径，确认路径是否正确
        print(f"尝试启动的程序路径：{exe_path}")

        # 检查文件是否存在
        if not os.path.exists(exe_path):
            print("错误：找不到文件。请检查路径是否正确。")
            return

        try:
            # 使用subprocess启动程序
            subprocess.Popen([exe_path])
            print("调试信息：程序已启动")
        except Exception as e:
            print(f"调试信息：启动程序时发生错误: {e}")

    def log_abnormal_behavior(self, process_name):
        with open(self.log_file_path, 'a') as log_file:
            log_file.write(f"{QDateTime.currentDateTime().toString()} - 关闭异常程序: {process_name}\n")

    def show_warning(self):
        QMessageBox.warning(self, '警告', '已记录异常行为到班主任后台')

    def check_usb_insertion(self):
        removable_drives = []
        for part in psutil.disk_partitions():
            if 'removable' in part.opts.lower():
                drive = part.device.split('\\')[0] + '\\'  # 获取驱动器的根路径
                if os.path.exists(drive) and drive not in ['C:\\', 'D:\\']:
                    removable_drives.append(drive)
        
        for drive in removable_drives:
            target_file = os.path.join(drive, 'Ukey.ClassGuardian')
            if os.path.exists(target_file):
                # 如果找到文件，则写入日志并关闭程序
                with open(self.log_file_path, 'a') as log_file:
                    log_file.write(f"{datetime.now().strftime('%Y-%m-%d %H:%M:%S')} - 检测到含有ClassGuardian-Ukey的U盘插入: {drive}\n")
                QMessageBox.warning(self, 'ClassGuardian', '检测到ClassGuardian-Ukey，点击确定关闭课间守护')
                self.close()  # 关闭窗口
            else:
                # 如果U盘中没有关键文件，记录U盘插入事件
                with open(self.log_file_path, 'a') as log_file:
                    log_file.write(f"{datetime.now().strftime('%Y-%m-%d %H:%M:%S')} - 检测到U盘插入: {drive}\n")












def main():
    app = QApplication(sys.argv)
    window = BrowserWindow()
    window.show()
    sys.exit(app.exec_())


if __name__ == '__main__':
    main()
