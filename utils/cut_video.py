import tkinter as tk
from tkinter import filedialog, ttk
import cv2
import os

from moviepy.video.io.VideoFileClip import VideoFileClip


def update_progress(value, bar):
    bar['value'] = value
    root.update_idletasks()


def on_convert_start(bar):
    convert_button.config(state="disabled")  # 禁用按钮
    status_label.config(text="转换中，请稍候...")
    update_progress(0, bar)  # 初始化进度条


def convert_video_to_images():
    global video_path, output_folder, cap, frame_count, progress_bar

    # 选择视频文件
    video_path = filedialog.askopenfilename(title="Select a video file",
                                            filetypes=[("Video files", "*.mp4 *.avi *.mov")])

    if not os.path.exists(video_path):
        raise ValueError(f"Video file not found: {video_path}")

    output_folder = filedialog.askdirectory(title="Select an output directory")

    base_name = os.path.basename(video_path)
    base_name_without_ext, _ = os.path.splitext(base_name)

    output_path = os.path.join(output_folder, base_name_without_ext)
    os.makedirs(output_path, exist_ok=True)
    if not output_path:
        return

    # 创建进度条
    progress_bar = ttk.Progressbar(root, orient='horizontal', length=280, mode='determinate')
    progress_bar.pack(pady=10)
    on_convert_start(progress_bar)  # 初始化状态和进度条

    # 打开视频文件
    cap = cv2.VideoCapture(video_path)
    if not cap.isOpened():
        print("Error: Could not open video.")
        progress_bar.pack_forget()  # 隐藏进度条
        return

    # 获取视频的帧率和总帧数
    fps = cap.get(cv2.CAP_PROP_FPS)
    total_frames = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))
    interval = int(fps/3)
    frame_count = 0
    save_count = 0  # 用于记录保存的图片数量
    while True:
        ret, frame = cap.read()
        if not ret:
            break

        # 每interval帧保存一张图片
        if frame_count % interval == 0:
            filename = os.path.join(output_path, f'frame_{save_count:04d}.jpg')
            cv2.imwrite(filename, frame)
            save_count += 1

        # 更新进度条
        if save_count > 0:
            progress_value = int((save_count / (total_frames / interval)) * 100)
            update_progress(progress_value, progress_bar)

        frame_count += 1

    cap.release()
    print("Video processing completed.")
    update_progress(100, progress_bar)  # 完成进度
    status_label.config(text="转换完成")
    convert_button.config(state="normal", text="选择新的视频")  # 启用按钮
    progress_bar.pack_forget()  # 隐藏进度条


def convert_video_to_mp4():
    global video_path

    # 选择视频文件
    video_path = filedialog.askopenfilename(title="Select a video file",
                                            filetypes=[("Video files", "*.mp4 *.avi *.mov")])
    if not video_path:
        return

    # 从视频文件路径中提取文件名
    base_name = os.path.basename(video_path)
    base_name_without_ext, _ = os.path.splitext(base_name)

    # 让用户选择保存路径，使用原始文件名作为默认值
    output_path = filedialog.asksaveasfilename(title="Save as MP4",
                                               defaultextension=".mp4",
                                               filetypes=[("MP4 files", "*.mp4")],
                                               initialfile=base_name_without_ext)
    if not output_path:
        return

    # 使用moviepy转换视频格式，并显示进度条
    video_clip = VideoFileClip(video_path)
    bar = ttk.Progressbar(root, orient='horizontal', length=280, mode='determinate')

    bar.pack(pady=10)
    on_convert_start(bar)  # 初始化状态和进度条
    video_clip.write_videofile(output_path, codec='libx264', audio_codec='aac', fps=video_clip.fps,
                               # logger=update_progress
                               )
    print(f"{base_name_without_ext} Video conversion completed.")
    status_label.config(text="转换完成")
    video_clip.close()
    bar.pack_forget()  # 隐藏进度条


if __name__ == '__main__':
    # 创建主窗口
    root = tk.Tk()
    screen_width = root.winfo_screenwidth()
    screen_height = root.winfo_screenheight()
    x = (screen_width // 2) - 250  # 窗口宽度设为500，因此这里用250
    y = (screen_height // 2) - 100  # 窗口高度设为200

    root.geometry(f"500x300+{x}+{y}")
    root.title("Video Processing Tool")

    # 使用Frame来组织控件
    frame = tk.Frame(root)
    frame.pack(fill=tk.BOTH, expand=True)

    # 创建状态标签
    status_label = tk.Label(frame, text="Ready", anchor='w')
    status_label.pack(side=tk.TOP, fill=tk.X, padx=10, pady=10)

    # 创建进度条
    progress = ttk.Progressbar(frame, orient='horizontal', length=280, mode='determinate')
    progress.pack(side=tk.TOP, fill=tk.X, expand=True, padx=10)

    # 按钮的尺寸可以设置为更大的值，例如width=20
    convert_button = tk.Button(frame, text="Convert Video to Images", command=convert_video_to_images, width=20)
    convert_button.pack(side=tk.LEFT, padx=10, pady=10)

    convert_to_mp4_button = tk.Button(frame, text="Convert to MP4", command=convert_video_to_mp4, width=20)
    convert_to_mp4_button.pack(side=tk.RIGHT, padx=10, pady=10)

    # 运行主循环
    root.mainloop()
