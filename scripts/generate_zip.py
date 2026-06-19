#!/usr/bin/env python3
"""打包分析图片为 ZIP"""

import argparse
import zipfile
from pathlib import Path


def create_zip(source_dir, output_path):
    """将分析目录中的图片打包为 ZIP"""
    source = Path(source_dir)
    output = Path(output_path)
    
    image_exts = {".jpg", ".jpeg", ".png", ".gif", ".webp"}
    
    with zipfile.ZipFile(output, "w", zipfile.ZIP_DEFLATED) as zf:
        count = 0
        for f in sorted(source.rglob("*")):
            if f.suffix.lower() in image_exts and f.is_file():
                arcname = f.relative_to(source)
                zf.write(f, arcname)
                count += 1
                print(f"  + {arcname}")
    
    print(f"✅ ZIP 已生成: {output} ({count} 张图片)")
    return output


def main():
    parser = argparse.ArgumentParser(description="打包分析图片为 ZIP")
    parser.add_argument("source_dir", help="分析目录")
    parser.add_argument("--out", default="分析图片.zip", help="输出 ZIP 路径")
    args = parser.parse_args()
    
    if not Path(args.source_dir).exists():
        print(f"[ERROR] 目录不存在: {args.source_dir}")
        return
    
    create_zip(args.source_dir, args.out)


if __name__ == "__main__":
    main()
