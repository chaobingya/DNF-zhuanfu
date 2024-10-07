import os
import subprocess


def start_scrcpy():
    """
    启动scrcpy，设置FPS和窗口标题，可自定义窗口大小。

    :param fps: 最大FPS值，默认为60。
    :param window_title: 窗口标题，默认为'My device'。
    :param width: 窗口宽度，默认为None，使用scrcpy默认值。
    :param height: 窗口高度，默认为None，使用scrcpy默认值。
    """
    # 获取当前脚本文件的目录

    current_dir = os.path.dirname(os.path.abspath(__file__))
    adb_path = os.path.join(current_dir, 'scrcpy-win64-v2.6.1', 'adb.exe')
    use_wifi = os.environ.get('ADB_WITH_WIFI')
    host = os.environ.get('ADB_WITH_WIFI_HOST')
    port = os.environ.get('ADB_WITH_WIFI_PORT')
    width = os.environ.get('ADB_WITH_WIFI_WIDTH', '640')
    height = str(round(int(width) * 0.45125))
    fps = os.environ.get('ADB_FPS')
    window_title = os.environ.get('ADB_WINDOW_TITLE')

    if use_wifi == 'true' and host and port:
        try:
            subprocess.Popen([adb_path, 'connect', host + ':' + port])
            print("adb started successfully ,addr:", host + ':' + port)
        except Exception as e:
            print(f"Failed to start adb: {e},try with usb")
            subprocess.Popen([adb_path, 'connect'])
    else:
        subprocess.Popen([adb_path, 'connect'])
    scrcpy_path = os.path.join(current_dir, 'scrcpy-win64-v2.6.1', 'scrcpy.exe')
    # 基础scrcpy命令
    command = [scrcpy_path, '--max-fps', str(fps), '--window-title', window_title,'--window-width', width, '--window-height', height]
    # 启动scrcpy进程，并捕获输出
    try:
        subprocess.Popen(command)
        print("scrcpy started successfully with max FPS of", fps)
    except Exception as e:
        print(f"Failed to start scrcpy: {e}")


if __name__ == '__main__':
    from dotenv import load_dotenv
    load_dotenv()
    start_scrcpy()
