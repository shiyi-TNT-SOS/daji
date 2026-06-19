#!/usr/bin/env python3
"""Markdown 报告 → 暗黑仪表盘离线 HTML（图片 base64 内联）"""

import argparse
import base64
import os
import re
import sys
from pathlib import Path


def encode_image_base64(image_path):
    """将图片编码为 base64 data URI"""
    try:
        ext = Path(image_path).suffix.lower()
        mime_map = {".jpg": "image/jpeg", ".jpeg": "image/jpeg", ".png": "image/png", ".gif": "image/gif", ".webp": "image/webp"}
        mime = mime_map.get(ext, "image/jpeg")
        
        with open(image_path, "rb") as f:
            data = base64.b64encode(f.read()).decode("utf-8")
        return f"data:{mime};base64,{data}"
    except Exception as e:
        print(f"[WARNING] 无法编码图片 {image_path}: {e}")
        return ""


def md_to_html(md_path, output_path):
    """将 Markdown 转为暗黑仪表盘 HTML"""
    md_path = Path(md_path)
    base_dir = md_path.parent
    
    with open(md_path, "r", encoding="utf-8") as f:
        md_content = f.read()
    
    # 替换图片引用为 base64
    def replace_img(match):
        alt = match.group(1)
        src = match.group(2)
        img_path = base_dir / src
        if img_path.exists():
            b64 = encode_image_base64(str(img_path))
            return f'<img src="{b64}" alt="{alt}" loading="lazy">'
        return match.group(0)
    
    md_content = re.sub(r'!\[([^\]]*)\]\(([^)]+)\)', replace_img, md_content)
    
    # 简单的 Markdown → HTML 转换
    html_body = md_to_html_body(md_content)
    
    # 暗黑仪表盘 HTML 模板
    html = f"""<!DOCTYPE html>
<html lang="zh-CN">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>视频拉片分析报告</title>
<style>
:root {{
  --bg: #05090d;
  --card: #0a1219;
  --border: #1a2a35;
  --text: #c8d6e5;
  --text-dim: #7a8a9a;
  --cyan: #52e8ff;
  --lime: #b9ff35;
  --orange: #ff8c42;
  --pink: #ff6b9d;
  --purple: #a78bfa;
}}
* {{ margin: 0; padding: 0; box-sizing: border-box; }}
body {{
  background: var(--bg);
  color: var(--text);
  font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", "PingFang SC", "Microsoft YaHei", sans-serif;
  line-height: 1.8;
  padding: 24px;
}}
.container {{
  max-width: 960px;
  margin: 0 auto;
}}
h1 {{
  font-size: 2em;
  color: var(--cyan);
  border-bottom: 2px solid var(--border);
  padding-bottom: 12px;
  margin: 32px 0 16px;
}}
h2 {{
  font-size: 1.5em;
  color: var(--lime);
  margin: 28px 0 12px;
  padding-left: 12px;
  border-left: 4px solid var(--lime);
}}
h3 {{
  font-size: 1.2em;
  color: var(--orange);
  margin: 20px 0 8px;
}}
h4 {{
  font-size: 1.05em;
  color: var(--pink);
  margin: 16px 0 6px;
}}
p {{ margin: 8px 0; }}
img {{
  max-width: 100%;
  border-radius: 8px;
  border: 1px solid var(--border);
  margin: 12px 0;
}}
table {{
  width: 100%;
  border-collapse: collapse;
  margin: 16px 0;
  background: var(--card);
  border-radius: 8px;
  overflow: hidden;
  border: 1px solid var(--border);
}}
th {{
  background: #0d1a24;
  color: var(--cyan);
  padding: 10px 14px;
  text-align: left;
  font-weight: 600;
  font-size: 0.9em;
}}
td {{
  padding: 10px 14px;
  border-top: 1px solid var(--border);
  font-size: 0.9em;
}}
tr:hover td {{ background: rgba(82, 232, 255, 0.03); }}
code {{
  background: #0d1a24;
  color: var(--lime);
  padding: 2px 6px;
  border-radius: 4px;
  font-family: "Fira Code", "Cascadia Code", "Consolas", monospace;
  font-size: 0.85em;
}}
pre {{
  background: #0d1a24;
  border: 1px solid var(--border);
  border-radius: 8px;
  padding: 16px;
  overflow-x: auto;
  margin: 12px 0;
}}
pre code {{
  background: none;
  padding: 0;
}}
ul, ol {{ margin: 8px 0; padding-left: 24px; }}
li {{ margin: 4px 0; }}
strong {{ color: var(--cyan); }}
em {{ color: var(--purple); }}
blockquote {{
  border-left: 3px solid var(--orange);
  margin: 12px 0;
  padding: 8px 16px;
  background: rgba(255, 140, 66, 0.05);
  border-radius: 0 8px 8px 0;
}}
hr {{
  border: none;
  border-top: 1px solid var(--border);
  margin: 24px 0;
}}
.card {{
  background: var(--card);
  border: 1px solid var(--border);
  border-radius: 12px;
  padding: 20px;
  margin: 16px 0;
}}
.badge {{
  display: inline-block;
  background: rgba(82, 232, 255, 0.1);
  color: var(--cyan);
  padding: 2px 10px;
  border-radius: 12px;
  font-size: 0.8em;
  margin: 0 4px;
}}
@media (max-width: 768px) {{
  body {{ padding: 12px; }}
  h1 {{ font-size: 1.5em; }}
  table {{ font-size: 0.8em; }}
  th, td {{ padding: 6px 8px; }}
}}
</style>
</head>
<body>
<div class="container">
{html_body}
</div>
</body>
</html>"""
    
    with open(output_path, "w", encoding="utf-8") as f:
        f.write(html)
    
    print(f"✅ HTML 报告已生成: {output_path}")


def md_to_html_body(md):
    """简易 Markdown → HTML"""
    lines = md.split("\n")
    result = []
    in_code_block = False
    in_table = False
    in_list = False
    
    for line in lines:
        # 代码块
        if line.startswith("```"):
            if in_code_block:
                result.append("</code></pre>")
                in_code_block = False
            else:
                result.append("<pre><code>")
                in_code_block = True
            continue
        
        if in_code_block:
            result.append(escape_html(line))
            continue
        
        # 表格
        if "|" in line and line.strip().startswith("|"):
            if not in_table:
                result.append("<table>")
                in_table = True
            
            cells = [c.strip() for c in line.strip().strip("|").split("|")]
            
            # 跳过分隔行
            if all(c.replace("-", "").replace(":", "").replace(" ", "") == "" for c in cells):
                continue
            
            is_header = in_table and len(result) > 0 and result[-1] == "<table>"
            tag = "th" if is_header else "td"
            
            row = "<tr>" + "".join(f"<{tag}>{escape_html(c)}</{tag}>" for c in cells) + "</tr>"
            result.append(row)
            continue
        elif in_table:
            result.append("</table>")
            in_table = False
        
        # 关闭列表
        if in_list and not line.strip().startswith(("- ", "* ", "+ ", "1. ")):
            result.append(f"</{in_list}>")
            in_list = False
        
        # 标题
        if line.startswith("# "):
            result.append(f"<h1>{escape_html(line[2:])}</h1>")
        elif line.startswith("## "):
            result.append(f"<h2>{escape_html(line[3:])}</h2>")
        elif line.startswith("### "):
            result.append(f"<h3>{escape_html(line[4:])}</h3>")
        elif line.startswith("#### "):
            result.append(f"<h4>{escape_html(line[5:])}</h4>")
        # 水平线
        elif line.strip() == "---" or line.strip() == "***":
            result.append("<hr>")
        # 无序列表
        elif line.strip().startswith(("- ", "* ", "+ ")):
            if not in_list:
                in_list = "ul"
                result.append("<ul>")
            content = line.strip()[2:]
            result.append(f"<li>{inline_md(content)}</li>")
        # 有序列表
        elif re.match(r"^\d+\.\s", line.strip()):
            if not in_list:
                in_list = "ol"
                result.append("<ol>")
            content = re.sub(r"^\d+\.\s", "", line.strip())
            result.append(f"<li>{inline_md(content)}</li>")
        # 引用
        elif line.startswith("> "):
            result.append(f"<blockquote>{inline_md(line[2:])}</blockquote>")
        # 空行
        elif not line.strip():
            result.append("<br>")
        # 普通段落
        else:
            result.append(f"<p>{inline_md(line)}</p>")
    
    if in_code_block:
        result.append("</code></pre>")
    if in_table:
        result.append("</table>")
    if in_list:
        result.append(f"</{in_list}>")
    
    return "\n".join(result)


def inline_md(text):
    """行内 Markdown 转换"""
    # 粗体
    text = re.sub(r'\*\*(.+?)\*\*', r'<strong>\1</strong>', text)
    # 斜体
    text = re.sub(r'\*(.+?)\*', r'<em>\1</em>', text)
    # 行内代码
    text = re.sub(r'`([^`]+)`', r'<code>\1</code>', text)
    return text


def escape_html(text):
    return text.replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;").replace('"', "&quot;")


def main():
    parser = argparse.ArgumentParser(description="Markdown → 暗黑仪表盘离线 HTML")
    parser.add_argument("md_path", help="Markdown 文件路径")
    parser.add_argument("--out", default=None, help="输出 HTML 路径")
    args = parser.parse_args()
    
    md_path = Path(args.md_path)
    if args.out:
        out_path = args.out
    else:
        out_path = md_path.with_suffix(".html")
    
    md_to_html(md_path, out_path)


if __name__ == "__main__":
    main()
