# 妲己拉片 — 视频参考片结构化拆解

> **Video Reference Structured Disassembly**

Upload video → ffmpeg frame extraction → AI visual analysis → generate dark dashboard HTML report + ZIP image package.

Functionally equivalent to `aitoearn-lapian`, but independently implemented, not dependent on the `aitoearn` system.

---

## 🎯 What is this?

**妲己拉片 (Daji Lapian)** is an open-source video analysis tool designed for **content creators, short video operators, and advertising directors**.

It helps you:
- 📸 **Auto frame extraction** — split video into keyframes and shot frames
- 📊 **Generate overview images** — see the video's overall rhythm at a glance
- 📝 **12-module analysis report** — from basic info to AI prompts, fully covered
- 🌐 **HTML report** — dark dashboard style, single-file offline viewable
- 📦 **ZIP image package** — all keyframes + shot frames packaged for archival

---

## 🚀 Quick Start

### Step 1: Install dependencies

```bash
pip install imageio-ffmpeg Pillow
```

✅ **Recommended: `imageio-ffmpeg`** — no need to install system ffmpeg, automatically provides binary.

❌ If you use system ffmpeg, make sure it's installed and callable from the command line.

---

### Step 2: Place Skill files

Put the `video-lapian/` folder at:

```
~/./skills/video-lapian/
```

Directory structure:
```
video-lapian/
├── SKILL.md              ← Skill description (for AI)
├── requirements.txt       ← Dependencies
├── README.md             ← This file (English manual)
├── 使用说明.md          ← Chinese manual
├── assets/
│   └── report_template.md
├── references/
│   └── field_descriptions.md
└── scripts/
    ├── extract_frames.py      ← Frame extraction + scene detection
    ├── generate_overview.py   ← Generate overview images
    ├── generate_html.py       ← Markdown → HTML report
    └── generate_zip.py      ← Package images into ZIP
```

---

### Step 3: Usage

#### **Method A: Via AI conversation (Recommended)**

Say to AI:
```
妲己拉片，分析这个视频 C:/videos/ad.mp4
```

AI will automatically:
1. Extract frames → 2. Analyze → 3. Generate report → 4. Present results

---

#### **Method B: Run directly from command line**

```bash
# 1. Extract frames
python ~/./skills/video-lapian/scripts/extract_frames.py "video.mp4" --out "video_分析"

# 2. Generate overview images
python ~/./skills/video-lapian/scripts/generate_overview.py "video_分析/关键帧" --out "video_分析/视频总览图.jpg" --title "视频总览"
python ~/./skills/video-lapian/scripts/generate_overview.py "video_分析/分镜详解" --out "video_分析/分镜总览图.jpg" --title "分镜总览"

# 3. Let AI analyze and write report (see "Report Generation" below)

# 4. Markdown to HTML
python ~/./skills/video-lapian/scripts/generate_html.py "video_分析/完整分析报告.md" --out "video_分析/完整分析报告.html"

# 5. Package ZIP
python ~/./skills/video-lapian/scripts/generate_zip.py "video_分析" --out "video_分析/分析图片.zip"
```

---

## 📊 What do you get?

### 1. **Chat message summary** (quick preview)

```
## Video Analysis

### Basic Info
| Attribute | Value |
|---|---|
| Duration | 30s |
| Resolution | 1080 x 1920 |
| Frame rate | 30 fps |
| Number of shots | 8 |

### Video Summary
**Overall content**: Outfit sharing short video, showcasing 3 summer outfits
**Core selling points/info**:
- High cost-effectiveness (unit price <100 yuan)
- Suitable for petite women
- Can be daily or for dates

### Video Overview
[Video overview image](video_分析/视频总览图.jpg)

### Deliverables
- HTML report: `完整分析报告.html`
- ZIP image package: `分析图片.zip`
```

---

### 2. **HTML report** (full analysis)

**12 modules in order**:

| Module | Content |
|--------|---------|
| 1. Basic Info | Duration, resolution, frame rate, number of shots |
| 2. Video Summary | Overall summary, core selling points, emotional tone, target audience |
| 3. Video Overview | Keyframe grid image (uniform sampling) |
| 4. Shot Overview | Scene change representative frame grid image |
| 5. Content Structure | Paragraphs, timecodes, content positioning, functions |
| 6. Script Breakdown | Voiceover/copy, subtitle rhythm, BGM/SFX |
| 7. Valid Shots List | Serial number, timecode, visual keywords, shot size, camera movement, emotion |
| 8. Detailed Shot Breakdown | Each shot's frame + 8 analysis fields |
| 9. AI Video Platform Submission | Prompts suitable for Keling/Jimeng/Runway |
| 10. Single Shot Official Prompts | Independent prompts for each shot (text-to-image/image-to-video) |
| 11. Segmented Second Script | Time-axis script split by seconds |
| 12. Final Full Video Concatenation Prompt | Complete prompt to recreate the entire video |

**Visual style**: Dark dashboard (#05090d background + #52e8ff cyan highlight)

---

### 3. **ZIP image package** (for archival)

```
分析图片.zip
├── 视频总览图.jpg
├── 分镜总览图.jpg
├── 关键帧/
│   ├── frame_0001_0.00s.jpg
│   ├── frame_0002_1.00s.jpg
│   └── ...
├── 分镜详解/
│   ├── shot_0001_0.00s.jpg
│   ├── shot_0002_3.50s.jpg
│   └── ...
├── 首帧.jpg
└── 尾帧.jpg
```

---

## 🔧 Advanced Features

### 1. **Adjust shot detection sensitivity**

Scene detection default threshold `0.25` (between 0-1, smaller = more sensitive).

- **Too few shots** → Lower to `0.20`
- **Too many shots** → Raise to `0.30`

```bash
python extract_frames.py "video.mp4" --out "video_分析" --scene-threshold 0.20
```

---

### 2. **Pure shot overview mode** (only clean grid image)

Say to AI:
```
Only want shot overview image, no text annotations or timestamps
```

AI will output:
- `完整分镜总览图_无标注.jpg` (clean grid, arranged in chronological order)

---

### 3. **AI video platform prompts**

Report modules 9-12 are specifically generated for you:

| Module | Purpose |
|--------|---------|
| **AI Video Platform Submission** | Direct submission format for Keling/Jimeng/Runway/Pika etc. |
| **Single Shot Official Prompt** | Independent prompt for each shot (text-to-image/image-to-video) |
| **Segmented Second Script** | Time-axis script split by seconds (visual + voiceover + SFX) |
| **Full Video Concatenation Prompt** | Complete prompt to recreate the entire video |

---

## ⚠️ Important Notes

### 1. **Only use original video frames**

❌ **No AI-generated images** — All frame images are真实地 extracted from the video  
❌ **No fabricated alternative visuals** — If video quality is poor, frames will also be poor  
✅ **Traceable** — Each image filename includes timestamp (e.g., `frame_0001_12.50s.jpg`)

---

### 2. **Number of shots not forcibly fixed**

✅ Naturally split based on **changes in scene, camera position, action, subject, or emotion**  
❌ Will not forcibly produce "fixed 10 shots"  
✅ For long-take videos, will supplement shot sampling frames (maintain per-second sampling)

---

### 3. **First and last frames must be real**

✅ Shot overview image **must start with real first frame and end with real last frame**  
✅ Especially important for 15s+ long-take videos  
✅ Always export `首帧.jpg` and `尾帧.jpg` and include in ZIP

---

## 🔍 Troubleshooting

| Problem | Solution |
|---------|----------|
| **Missing ffmpeg** | Install `imageio-ffmpeg` (`pip install imageio-ffmpeg`) or system ffmpeg |
| **Scene detection too few shots** | Rerun `extract_frames.py` with `--scene-threshold 0.20` |
| **Scene detection too many shots** | Rerun `extract_frames.py` with `--scene-threshold 0.30` |
| **HTML images not displaying** | Check if image paths in Markdown are correct relative to the report file |
| **ZIP missing images** | Check if `分析目录/` has `关键帧/` and `分镜详解/` folders |

---

## 📝 Example: Complete Workflow

### Input
```
Dad: 妲己拉片，分析这个视频 C:/videos/summer_outfit.mp4
```

### AI automatically executes
```
1. Create output directory summer_outfit_分析/
2. Extract frames + scene detection
   → 关键帧/ (1 frame per second)
   → 分镜详解/ (scene change frames)
   → metadata.json
   → frames_manifest.csv
   → shots_manifest.csv
3. Generate overview images
   → 视频总览图.jpg
   → 分镜总览图.jpg
4. Use visual capability to view keyframes and shots, write analysis report
   → 完整分析报告.md (12 modules)
5. Markdown to offline HTML
   → 完整分析报告.html (base64 inline images)
6. Package images
   → 分析图片.zip
7. Present results
   → Chat message summary
   → HTML report (offline viewable)
   → ZIP image package (downloadable)
```

### Output
```
✅ Video analysis complete!

### Basic Info
| Attribute | Value |
|---|---|
| Duration | 30s |
| Resolution | 1080 x 1920 |
| Frame rate | 30 fps |
| Number of shots | 8 |

### Video Summary
**Overall content**: Outfit sharing short video, showcasing 3 summer outfits
...

### Deliverables
- HTML report: `summer_outfit_分析/完整分析报告.html`
- ZIP image package: `summer_outfit_分析/分析图片.zip`
```

---

## 💡 Usage Tips

### 1. **Choose appropriate videos**
- ✅ **Videos with shot changes** — ads, MVs, short videos  
- ⚠️ **Long-take videos** — will supplement shot sampling frames, but fewer shots  
- ❌ **Pure black screen or static image videos** — frame extraction meaningless  

### 2. **Use for competitor analysis**
1. Lapian → 2. View detailed shot breakdown → 3. Extract "recreation points" → 4. Use AI prompt module to generate your own version

### 3. **Use for AI video creation**
1. Lapian → 2. View modules 9-12 → 3. Copy prompts → 4. Submit to Keling/Jimeng/Runway

---

## 📞 Contact & Feedback

**Author**: 妲己 (AI Assistant)  
**Skill Version**: v1.0 (2026-06-18)  
**Feedback**: If you encounter problems or have improvement suggestions, please contact the creator

---

## 📜 License

This tool is an open-source project, free to use, modify, and share.  
**Hard rule**: Only use original video frames, do not call image generation tools, do not fabricate alternative visuals.

---

_❤️ Happy la pian! 🎬_
