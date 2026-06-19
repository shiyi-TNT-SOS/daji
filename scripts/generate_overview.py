#!/usr/bin/env python3
"""生成视频总览图 & 分镜总览图 — 网格拼接"""

import argparse
import os
import sys
from pathlib import Path

try:
    from PIL import Image, ImageDraw, ImageFont
except ImportError:
    print("[ERROR] 需要 Pillow: pip install Pillow")
    sys.exit(1)


def find_font():
    """找系统中的中文字体"""
    candidates = [
        "C:/Windows/Fonts/msyh.ttc",
        "C:/Windows/Fonts/simhei.ttf",
        "C:/Windows/Fonts/simsun.ttc",
        "/System/Library/Fonts/PingFang.ttc",
        "/usr/share/fonts/truetype/droid/DroidSansFallbackFull.ttf",
        "/usr/share/fonts/opentype/noto/NotoSansCJK-Regular.ttc",
    ]
    for c in candidates:
        if os.path.exists(c):
            return c
    return None


def create_overview(image_dir, output_path, title="", max_cols=5, thumb_size=320):
    """创建帧网格总览图"""
    image_dir = Path(image_dir)
    images = sorted(image_dir.glob("*.jpg")) + sorted(image_dir.glob("*.png"))
    
    if not images:
        print(f"[WARNING] {image_dir} 中没有图片")
        return None
    
    # 限制最多50帧
    if len(images) > 50:
        step = len(images) // 50
        images = images[::step][:50]
    
    n = len(images)
    cols = min(max_cols, n)
    rows = (n + cols - 1) // cols
    
    # 加载第一张图获取尺寸比例
    first = Image.open(images[0])
    orig_w, orig_h = first.size
    ratio = orig_h / orig_w
    
    thumb_h = int(thumb_size * ratio)
    
    # 画布：暗黑仪表盘风格
    title_h = 60 if title else 0
    gap = 8
    canvas_w = cols * thumb_size + (cols + 1) * gap
    canvas_h = rows * thumb_h + (rows + 1) * gap + title_h
    
    # 背景
    bg_color = (5, 9, 13)  # #05090d
    canvas = Image.new("RGB", (canvas_w, canvas_h), bg_color)
    draw = ImageDraw.Draw(canvas)
    
    # 标题
    if title:
        font = None
        font_path = find_font()
        if font_path:
            try:
                font = ImageFont.truetype(font_path, 28)
            except Exception:
                font = ImageFont.load_default()
        else:
            font = ImageFont.load_default()
        
        draw.text((gap, gap), title, fill=(82, 232, 255), font=font)  # #52e8ff
    
    # 粘贴缩略图
    for idx, img_path in enumerate(images):
        col = idx % cols
        row = idx // cols
        
        x = gap + col * (thumb_size + gap)
        y = title_h + gap + row * (thumb_h + gap)
        
        try:
            img = Image.open(img_path)
            img.thumbnail((thumb_size, thumb_h), Image.LANCZOS)
            
            # 居中粘贴
            paste_x = x + (thumb_size - img.width) // 2
            paste_y = y + (thumb_h - img.height) // 2
            
            canvas.paste(img, (paste_x, paste_y))
        except Exception as e:
            print(f"[WARNING] 无法加载 {img_path}: {e}")
    
    canvas.save(output_path, quality=90)
    print(f"✅ 总览图已生成: {output_path} ({cols}x{rows})")
    return output_path


def main():
    parser = argparse.ArgumentParser(description="生成视频帧网格总览图")
    parser.add_argument("image_dir", help="图片目录")
    parser.add_argument("--out", default="overview.jpg", help="输出路径")
    parser.add_argument("--title", default="", help="标题")
    parser.add_argument("--cols", type=int, default=5, help="每行列数")
    parser.add_argument("--thumb-size", type=int, default=320, help="缩略图宽度")
    args = parser.parse_args()
    
    create_overview(args.image_dir, args.out, args.title, args.cols, args.thumb_size)


if __name__ == "__main__":
    main()
