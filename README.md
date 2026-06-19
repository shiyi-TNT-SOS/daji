# 妲己拉片 🎬

> AI驱动的双语视频分析与拆解工具

[![Version](https://img.shields.io/badge/version-v1.0-green.svg)](https://github.com/shiyi-TNT-SOS/daji/releases)
[![License](https://img.shields.io/badge/license-MIT-blue.svg)](LICENSE)
[![Python](https://img.shields.io/badge/python-3.8+-blue.svg)](https://www.python.org/)
[![Stars](https://img.shields.io/github/stars/shiyi-TNT-SOS/daji?style=social)](https://github.com/shiyi-TNT-SOS/daji)

---

## ✨ 项目简介

妲己拉片 是一个开源的AI视频分析工具，能够自动拆解视频的镜头语言，提取关键帧，并生成美观的可视化分析报告。

**名称来源**："拉片"是影视行业的专业术语，指逐帧分析视频的镜头运用、节奏把控和视觉语言。

---

## 🎯 核心功能

| 功能 | 描述 | 状态 |
|------|------|------|
| 🎬 **智能分镜拆解** | 自动检测镜头切换，提取关键帧和分镜帧 | ✅ 可用 |
| 📊 **数据可视化** | 生成美观的HTML报告（暗色仪表盘风格） | ✅ 可用 |
| 🌐 **多平台支持** | 抖音 / 小红书 / B站 / YouTube / 本地视频 | ✅ 可用 |
| 🤖 **AI增强分析** | 集成GPT-4V，自动生成分镜脚本（可选） | ✅ 可用 |
| 📦 **一键打包** | 自动生成ZIP压缩包 | ✅ 可用 |

---

## 🚀 快速开始

### 1. 安装依赖

```bash
pip install -r requirements.txt
```

**依赖项**：
- `imageio-ffmpeg>=0.4.0` - 视频处理
- `Pillow>=10.0.0` - 图像处理

---

### 2. 基础使用

```bash
# 步骤1：提取关键帧
python scripts/extract_frames.py --video <视频路径>

# 步骤2：生成HTML报告
python scripts/generate_html.py --frames <帧目录>

# 步骤3：生成总览图
python scripts/generate_overview.py --frames <帧目录>
```

---

### 3. 示例报告

#### 📊 示例：分镜总览图

![分镜总览图示例](https://raw.githubusercontent.com/shiyi-TNT-SOS/daji/main/example-overview.jpg)

*↑ 自动生成的分镜总览图，一目了然查看视频节奏*

#### 🌐 在线查看完整报告

📄 [点击查看示例HTML报告](https://github.com/shiyi-TNT-SOS/daji/blob/main/example-report.html)（GitHub上直接预览）

---

## 📂 项目结构

```
daji/
├── LICENSE                    # MIT开源协议
├── README.md                # 本文件
├── SKILL.md                # 工具定义文件
├── requirements.txt         # Python依赖
├── example-overview.jpg    # 分镜总览图示例
├── scripts/               # 核心脚本
│   ├── extract_frames.py      # 视频帧提取
│   ├── generate_html.py      # HTML报告生成
│   ├── generate_overview.py  # 总览图生成
│   └── generate_zip.py      # ZIP打包
└── example-report.html     # 完整示例报告（可选）
```

---

## 🎯 使用场景

| 场景 | 用途 | 输出 |
|------|------|------|
| 📱 **短视频分析** | 拆解爆款视频的节奏和镜头运用 | 分镜报告 + 关键帧 |
| 🎥 **影视研究** | 分析电影/广告的镜头语言 | 完整分镜脚本 |
| 📚 **教学演示** | 展示视频制作技巧 | 可视化报告 |
| 🔍 **竞品分析** | 研究同类视频的制作手法 | 数据化对比 |

---

## 🤖 AI集成（可选）

如需AI增强分析，在 `scripts/` 中配置API密钥：

```python
# config.py
OPENAI_API_KEY = "your-api-key"
```

**AI功能**：
- 自动分析关键帧内容
- 生成分镜脚本描述
- 智能内容理解

---

## 📝 更新日志

### v1.0 (2026-06-19)

- ✅ 初始版本发布
- ✅ 支持多平台视频分析
- ✅ AI驱动的分镜脚本生成
- ✅ HTML可视化报告
- ✅ 一键打包功能

---

## 📄 许可证

MIT License - 自由使用、修改和分发

---

## 🙏 致谢

**Made with 💖 by shiyi-TNT-SOS**  
**Powered by 🦊 妲己 (AI助手)**

---

## 📧 联系方式

- **GitHub**: [@shiyi-TNT-SOS](https://github.com/shiyi-TNT-SOS)
- **Issue**: [提交问题](https://github.com/shiyi-TNT-SOS/daji/issues)
- **Discussions**: [参与讨论](https://github.com/shiyi-TNT-SOS/daji/discussions)

---

## ⭐ Star History

如果你觉得这个项目有用，请给我们一个Star！

[![Star History Chart](https://api.star-history.com/svg?repos=shiyi-TNT-SOS/daji&type=Date)](https://star-history.com/#shiyi-TNT-SOS/daji&Date)

---

*最后更新：2026-06-19*
