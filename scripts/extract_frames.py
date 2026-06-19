#!/usr/bin/env python3
"""视频截帧 + 场景检测分镜 — 妲己拉片工具链"""

import subprocess
import json
import os
import sys
import re
import argparse
from pathlib import Path

try:
    from imageio_ffmpeg import get_ffmpeg_exe
    IMAGEIO_FFMPEG = True
except ImportError:
    IMAGEIO_FFMPEG = False


def get_ffmpeg_cmd():
    """获取 ffmpeg 可执行文件路径，优先用 imageio-ffmpeg 捆绑版"""
    if IMAGEIO_FFMPEG:
        return get_ffmpeg_exe()
    # 回退 PATH
    for name in ["ffmpeg.exe", "ffmpeg"]:
        for p in os.environ.get("PATH", "").split(os.pathsep):
            candidate = os.path.join(p, name)
            if os.path.exists(candidate):
                return candidate
    raise FileNotFoundError("未找到 ffmpeg，请安装 imageio-ffmpeg 或系统 ffmpeg")


def run_ffmpeg(*args, **kwargs):
    """运行 ffmpeg 命令"""
    cmd = [get_ffmpeg_cmd()] + list(args)
    return subprocess.run(cmd, **kwargs)


def get_video_metadata(video_path):
    """用 ffmpeg 输出解析视频元数据（无需 ffprobe）"""
    cmd = [
        get_ffmpeg_cmd(), "-hide_banner", "-i", video_path
    ]
    result = subprocess.run(cmd, capture_output=True, text=True)
    output = result.stderr + result.stdout
    
    lines = output.split("\n")
    video_line = None
    duration = 0.0
    width, height = 0, 0
    fps = 0.0
    codec = "unknown"
    fmt = "unknown"
    bitrate = "0"
    
    for line in lines:
        line = line.strip()
        
        # 输入格式行
        if line.startswith("Input #"):
            fmt_match = re.search(r"Input #\d+,\s+([^,]+),", line)
            if fmt_match:
                fmt = fmt_match.group(1).strip()
        
        # 时长和比特率
        if "Duration:" in line and "bitrate:" in line:
            dur_match = re.search(r"Duration:\s+(\d+):(\d+):(\d+\.\d+)", line)
            if dur_match:
                h, m, s = dur_match.groups()
                duration = float(h) * 3600 + float(m) * 60 + float(s)
            bitrate_match = re.search(r"bitrate:\s+([\d\s]+)\s+kb/s", line)
            if bitrate_match:
                bitrate = bitrate_match.group(1).replace(" ", "")
        
        # 视频流信息
        if "Stream" in line and "Video:" in line:
            video_line = line
            # 编码格式
            codec_match = re.search(r"Video:\s+([^\s,(]+)", line)
            if codec_match:
                codec = codec_match.group(1)
            
            # 分辨率，跳过 [0x1] 这种流标识
            res_match = re.search(r",\s+(\d{2,})x(\d{2,})", line)
            if res_match:
                width, height = int(res_match.group(1)), int(res_match.group(2))
            
            # 帧率
            fps_match = re.search(r"([\d.]+)\s+fps", line)
            if fps_match:
                fps = float(fps_match.group(1))
            
            # 如果没找到 fps，尝试 tbr
            if fps == 0:
                tbr_match = re.search(r"([\d.]+)\s+tbr", line)
                if tbr_match:
                    fps = float(tbr_match.group(1))
    
    if not video_line:
        print("[ERROR] 未找到视频流信息")
        sys.exit(1)
    
    return {
        "duration": duration,
        "width": width,
        "height": height,
        "fps": round(fps, 2),
        "codec": codec,
        "format": fmt,
        "bitrate": bitrate,
    }


def extract_keyframes(video_path, output_dir, interval=1.0):
    """均匀采样关键帧，默认每秒1帧"""
    os.makedirs(output_dir, exist_ok=True)
    
    cmd = [
        get_ffmpeg_cmd(), "-y", "-i", video_path,
        "-vf", f"fps=1/{interval}",
        "-q:v", "2",
        "-frame_pts", "1",
        os.path.join(output_dir, "frame_%04d.jpg")
    ]
    subprocess.run(cmd, capture_output=True, text=True)
    
    # 重命名为带时间戳的格式
    files = sorted(Path(output_dir).glob("frame_*.jpg"))
    renamed = []
    for f in files:
        pts = float(f.stem.replace("frame_", ""))
        timestamp = pts  # approx
        new_name = f"frame_{f.stem.replace('frame_', '').zfill(4)}_{timestamp:.2f}s.jpg"
        new_path = f.parent / new_name
        f.rename(new_path)
        renamed.append(new_path)
    
    return renamed


def detect_scenes(video_path, output_dir, threshold=0.25):
    """场景检测切分镜"""
    os.makedirs(output_dir, exist_ok=True)
    
    # 先获取场景切换时间点
    cmd_detect = [
        get_ffmpeg_cmd(), "-y", "-i", video_path,
        "-vf", f"select='gt(scene\\,{threshold})',showinfo",
        "-vsync", "vfr", "-f", "null", "-"
    ]
    result = subprocess.run(cmd_detect, capture_output=True, text=True)
    
    # 从 stderr 提取场景切换时间点
    scene_times = [0.0]
    for line in result.stderr.split("\n"):
        match = re.search(r"pts_time:([\d.]+)", line)
        if match:
            t = float(match.group(1))
            if scene_times and t - scene_times[-1] < 0.1:
                continue  # 跳过太近的
            scene_times.append(t)
    
    # 如果场景切换太少，降低阈值重试
    if len(scene_times) <= 2 and threshold > 0.15:
        return detect_scenes(video_path, output_dir, threshold - 0.05)
    
    # 截取每个分镜的代表帧
    shot_files = []
    for i, t in enumerate(scene_times):
        out_name = os.path.join(output_dir, f"shot_{i+1:04d}_{t:.2f}s.jpg")
        cmd = [
            get_ffmpeg_cmd(), "-y", "-ss", str(t), "-i", video_path,
            "-vframes", "1", "-q:v", "2", out_name
        ]
        subprocess.run(cmd, capture_output=True, text=True)
        shot_files.append(Path(out_name))
    
    return shot_files, scene_times


def extract_sample_frames(video_path, output_dir, interval=1.0, prefix="shot_sample"):
    """对一镜到底或场景少的视频，每秒采样补充分镜"""
    os.makedirs(output_dir, exist_ok=True)
    
    cmd = [
        get_ffmpeg_cmd(), "-y", "-i", video_path,
        "-vf", f"fps=1/{interval}",
        "-q:v", "2",
        os.path.join(output_dir, f"{prefix}_%04d.jpg")
    ]
    subprocess.run(cmd, capture_output=True, text=True)
    
    files = sorted(Path(output_dir).glob(f"{prefix}_*.jpg"))
    return files


def main():
    parser = argparse.ArgumentParser(description="视频截帧 + 场景检测分镜")
    parser.add_argument("video", help="视频文件路径")
    parser.add_argument("--out", default=None, help="输出目录（默认：视频名_分析）")
    parser.add_argument("--scene-threshold", type=float, default=0.25, help="场景检测阈值（默认0.25）")
    parser.add_argument("--shot-sample-interval", type=float, default=1.0, help="分镜采样间隔秒数（默认1.0）")
    args = parser.parse_args()
    
    video_path = Path(args.video)
    if not video_path.exists():
        print(f"[ERROR] 视频文件不存在: {args.video}")
        sys.exit(1)
    
    if args.out:
        base_dir = Path(args.out)
    else:
        base_dir = Path(f"{video_path.stem}_分析")
    
    base_dir.mkdir(parents=True, exist_ok=True)
    
    # 1. 提取元数据
    print("[1/5] 提取视频元数据...")
    meta = get_video_metadata(str(video_path))
    meta_path = base_dir / "metadata.json"
    with open(meta_path, "w", encoding="utf-8") as f:
        json.dump(meta, f, ensure_ascii=False, indent=2)
    print(f"  时长: {meta['duration']:.1f}s | 分辨率: {meta['width']}x{meta['height']} | 帧率: {meta['fps']}fps")
    
    # 2. 提取关键帧
    print("[2/5] 提取关键帧（均匀采样）...")
    keyframe_dir = base_dir / "关键帧"
    keyframes = extract_keyframes(str(video_path), str(keyframe_dir), interval=1.0)
    print(f"  关键帧: {len(keyframes)} 帧")
    
    # 3. 场景检测
    print(f"[3/5] 场景检测（阈值={args.scene_threshold}）...")
    shot_dir = base_dir / "分镜详解"
    shots, scene_times = detect_scenes(str(video_path), str(shot_dir), threshold=args.scene_threshold)
    print(f"  分镜: {len(shots)} 个")
    
    # 4. 补充分镜（对一镜到底）
    if len(shots) <= 2 and meta["duration"] >= 15:
        print("[4/5] 一镜到底/场景少，补充分镜采样帧...")
        frames = extract_sample_frames(str(video_path), str(shot_dir), interval=args.shot_sample_interval, prefix="shot_sample")
        # 把补充分镜加入列表
        for f in frames:
            if f not in shots:
                shots.append(f)
        print(f"  补充后分镜: {len(shots)} 帧")
    else:
        print("[4/5] 分镜数量充足，跳过补充")
    
    # 5. 首帧/尾帧
    print("[5/5] 提取首帧/尾帧...")
    first_frame = base_dir / "首帧.jpg"
    last_frame = base_dir / "尾帧.jpg"
    
    subprocess.run([get_ffmpeg_cmd(), "-y", "-ss", "0", "-i", str(video_path), "-vframes", "1", "-q:v", "2", str(first_frame)], capture_output=True)
    duration_safe = max(0.1, meta["duration"] - 0.1)
    subprocess.run([get_ffmpeg_cmd(), "-y", "-ss", str(duration_safe), "-i", str(video_path), "-vframes", "1", "-q:v", "2", str(last_frame)], capture_output=True)
    
    # 写入 manifest
    manifest_path = base_dir / "frames_manifest.csv"
    with open(manifest_path, "w", encoding="utf-8") as f:
        f.write("type,filename\n")
        for kf in keyframes:
            f.write(f"keyframe,{kf.name}\n")
        for sf in shots:
            f.write(f"shot,{sf.name}\n")
    
    shots_manifest_path = base_dir / "shots_manifest.csv"
    with open(shots_manifest_path, "w", encoding="utf-8") as f:
        f.write("index,filename,time\n")
        for i, (sf, t) in enumerate(zip(shots, scene_times)):
            f.write(f"{i+1},{sf.name},{t:.2f}\n")
    
    print(f"\n✅ 完成！输出目录: {base_dir}")
    print(f"   关键帧: {len(keyframes)} | 分镜: {len(shots)}")
    print(f"   metadata.json | frames_manifest.csv | shots_manifest.csv")


if __name__ == "__main__":
    main()
