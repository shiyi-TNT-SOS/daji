---
name: daji
description: AI驱动的双语视频分析与拆解工具。自动检测镜头切换，提取关键帧，生成HTML可视化报告。支持抖音/小红书/B站/YouTube等多平台视频。
---

# 妲己拉片 — 视频参考片结构化拆解

> Version: v1.5 (2026-06-18)  
> Author: 妲己（AI助手）

上传视频 → ffmpeg 截帧 → AI 视觉分析 → 生成暗黑仪表盘 HTML 报告 + ZIP 图片包。

功能对子牙拉片，但独立实现，不依赖 aitoearn 体系。

## 触发词

- 拉片
- 视频分析
- 拆解视频
- 妲己拉片
- 视频拆解

## 硬规则

- 只使用原始视频帧作为视觉来源，不调用图片生成工具，不编造替代画面。
- 如果用户说"AI 生图"或模板里提到，一律解释为"从视频中截取/筛选关键帧"。
- 每张总览图和分镜图必须可追溯到原视频，文件名尽量带时间戳。
- 按场景、机位、动作、主体或情绪变化自然切分分镜，不强制固定分镜数。
- 视频提示词基于实际截帧编写，可以描述如何复刻视频，但不能声称生成图是源帧。
- 默认交付三件套：消息摘要、自包含 HTML 报告、ZIP 图片包。

## 快速流程

1. 创建输出目录 `{视频名}_分析/`
2. 截帧 + 场景检测：

```bash
python ~/./skills/video-lapian/scripts/extract_frames.py "video.mp4" --out "{视频名}_分析"
```

3. 生成总览图：

```bash
python ~/./skills/video-lapian/scripts/generate_overview.py "{视频名}_分析/关键帧" --out "{视频名}_分析/视频总览图.jpg" --title "视频总览"
python ~/./skills/video-lapian/scripts/generate_overview.py "{视频名}_分析/分镜详解" --out "{视频名}_分析/分镜总览图.jpg" --title "分镜总览"
```

4. 用视觉能力查看关键帧和分镜，基于实际截帧写分析报告。
5. 按 `assets/report_template.md` 写 `{视频名}_分析/完整分析报告.md`。
6. Markdown 转离线 HTML：

```bash
python ~/./skills/video-lapian/scripts/generate_html.py "{视频名}_分析/完整分析报告.md" --out "{视频名}_分析/完整分析报告.html"
```

7. 打包图片：

```bash
python ~/./skills/video-lapian/scripts/generate_zip.py "{视频名}_分析" --out "{视频名}_分析/分析图片.zip"
```

8. 用 `present_files` 把 HTML 报告呈现给用户查看。

## 报告结构（12 模块按序）

1. 基础信息
2. 视频总结
3. 视频总览
4. 分镜总览
5. 内容结构
6. 剧本拆解
7. 有效分镜清单
8. 分镜详细拆解
9. AI 视频平台提交版
10. 单镜头官方提示
11. 分段秒脚本
12. 最终全片串联提示

## 截帧标准

- 全片时间轴用均匀关键帧，短视频约每秒 1 帧，长视频降低采样率。
- 分镜清单用场景切换帧，默认阈值 `0.25`；分镜太少降到 `0.20`，太多升到 `0.30`。
- 分镜顺序首帧必须是原视频真实首帧、末帧必须是真实末帧（对 15 秒以上一镜到底尤其重要）。
- 始终在报告根目录导出 `首帧.jpg` 和 `尾帧.jpg`，并包含在 ZIP 中。
- 对一镜到底或低运动视频补充分镜采样帧时，保持每秒采样。
- 每个有意义的片段至少保留一张代表帧。
- 帧文件名带时间戳：`frame_0001_12.50s.jpg`、`shot_0003_08.20s.jpg`。

## 聊天消息输出

只展示精简摘要：

```markdown
## 视频分析

### 基础信息
| 属性 | 值 |
|---|---|
| 时长 | XX秒 |
| 分辨率 | XXXX x XXXX |
| 帧率 | XX fps |
| 分镜数 | X |

### 视频总结
**整体内容概括**：...
**核心卖点/信息点**：...
**情绪基调**：...

### 视频总览
[视频总览图]({路径}/视频总览图.jpg)

### 交付文件
- HTML报告：`完整分析报告.html`
- ZIP图片包：`分析图片.zip`
```

## 分镜分析字段

每个有效分镜包含：

- 截帧图片
- 时间码范围或代表帧时间点
- 画面描述
- 主体/产品/人物
- 动作
- 运镜方式
- 景别与构图
- 光线与色彩
- 情绪
- 复刻要点

详细字段说明见 `references/field_descriptions.md`。

## 输出目录结构

```text
{视频名}_分析/
|-- 视频总览图.jpg
|-- 分镜总览图.jpg
|-- 关键帧/
|   |-- frame_0001_0.00s.jpg
|-- 分镜详解/
|   |-- shot_0001_0.00s.jpg
|-- 首帧.jpg
|-- 尾帧.jpg
|-- 完整分析报告.md
|-- 完整分析报告.html
|-- metadata.json
|-- frames_manifest.csv
|-- shots_manifest.csv
`-- 分析图片.zip
```

## 报告视觉风格

暗黑仪表盘：`--bg: #05090d; --cyan: #52e8ff; --lime: #b9ff35`
截帧 base64 内联，单文件自包含，适配桌面和移动端。

## 视觉纯分镜模式

当用户明确只要干净分镜总览，不要文字标注、时间戳、分镜号或分析报告时：

- 仍只使用原始截帧。
- 不在总览图上放置标题、标注、分镜号、时间戳、描述、水印等文字。
- 如果用户说不需要，跳过 HTML/Markdown 分析报告。
- 优先输出单张网格图 `完整分镜总览图_无标注.jpg`。
- 按时间顺序排列帧，保持原视频宽高比。
- manifest 文件仅用于内部溯源，主交付物应为纯视觉分镜图。

## 质量检查清单

- 消息包含基础信息、总结和时间轴总览。
- HTML 可离线打开，所有图片 base64 内联。
- ZIP 包含时间轴总览、分镜总览、关键帧、分镜帧、首帧、尾帧。
- 报告包含全部 12 个模块且按序排列。
- 每个分镜都有真实视频帧。
- 分镜/故事板总览以真实首帧开始、真实末帧结束。
- 没有 AI 生成图伪造成帧。
- 路径和链接指向实际存在的文件。
- 分镜数基于自然变化，不按预设数量。

## 故障排除

- 缺少 `ffmpeg`：停止并告知用户安装 `imageio-ffmpeg`（`pip install imageio-ffmpeg`）或系统 ffmpeg，不要用 AI 生成图替代缺失帧。
- 场景检测分镜太少：用 `--scene-threshold 0.20` 重跑 `extract_frames.py`。
- 场景检测分镜太多：用 `--scene-threshold 0.30` 重跑 `extract_frames.py`。
- HTML 图片不显示：检查 Markdown 中图片路径是否相对于报告文件正确。

## 工具链

| 脚本 | 依赖 | 输入 | 输出 |
|------|------|------|------|
| `scripts/extract_frames.py` | ffmpeg, Python 3.10+ | 视频文件 | 关键帧/分镜/元数据/manifest |
| `scripts/generate_overview.py` | Pillow | 帧图片目录 | 视频总览图 / 分镜总览图 |
| `scripts/generate_html.py` | Pillow | Markdown 报告 | 单文件离线 HTML |
| `scripts/generate_zip.py` | Python stdlib | 分析目录 | 分析图片.zip |

### 依赖安装

推荐用 `imageio-ffmpeg` 提供 ffmpeg 二进制，无需额外安装系统 ffmpeg：

```bash
pip install imageio-ffmpeg Pillow
```

## 示例调用

```
用户: 妲己拉片，分析这个视频 C:/videos/ad.mp4
  → 自动走完 截帧 → 分析 → 生成 → 呈现 全流程
```
