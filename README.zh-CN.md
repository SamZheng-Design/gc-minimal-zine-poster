# GC Minimal Zine Poster

[English](README.md) · **简体中文** · [日本語](README.ja.md)

这是一个 Codex 技能：它会把主题、句子、物件、情绪、文章构想、照片或内容简报，转化为一张安静、极简的 ZINE 风格编辑海报所需的提示词，并生成对应的位图图像。

调用名称为 `gc-minimal-zine-poster-v0-1`。

## 视觉方向

这个技能会把每个请求编排成一张留白充足的竖版纸张海报，具有以下特征：

- 3:5 比例的仿旧纸张画布
- 70%–90% 的留白
- 一个小型、可被清楚表现的主体或视觉组合
- 衬线、打字机或等宽字体
- 一个清晰可见的高饱和度色彩锚点
- 复印、孔版印刷、网点、凸版印刷或扫描纸张的瑕疵与质感
- 安静的日式／韩式独立 ZINE 或极简编辑设计氛围

它会避开商业广告式布局、光亮样机、电影感布光、3D 渲染、霓虹、密集拼贴簿，以及大段整齐的文字。

## 示例

| Night Door | Yellow Step |
| --- | --- |
| ![Night Door](examples/night-door.jpeg) | ![Yellow Step](examples/yellow-step.jpeg) |

| Shore Pause | Pause Map |
| --- | --- |
| ![Shore Pause](examples/shore-pause.jpeg) | ![Pause Map](examples/pause-map.jpeg) |

| Typhoon Memory | Moon Tide |
| --- | --- |
| ![Typhoon Memory](examples/typhoon-memory.jpeg) | ![Moon Tide](examples/moon-tide.jpeg) |

## 图册

用这个技能生成的海报归档在 [`posters/`](posters/README.md)，目前 45 张：`01–27` 是单张，
`28–45` 是 **Seasons 四季影集**（四张封面 + 十四张内页）。
每张的**完整最终 prompt、变化配方和来源说明**都记录在 [`posters/index.json`](posters/index.json)。

| | | | | |
|:--:|:--:|:--:|:--:|:--:|
| <img src="posters/img/04-someone-wired-the-sky.jpeg" width="120"> | <img src="posters/img/09-the-edge-of-the-day.jpeg" width="120"> | <img src="posters/img/14-tiao-jin-ran-gang.jpeg" width="120"> | <img src="posters/img/17-there-is-another-world.jpeg" width="120"> | <img src="posters/img/20-you-ren-tiao-hai.jpeg" width="120"> |
| <img src="posters/img/21-the-cloud-ate-the-fire.jpeg" width="120"> | <img src="posters/img/22-we-stood-under-the-sign.jpeg" width="120"> | <img src="posters/img/23-someone-put-a-hat-on-the-lion.jpeg" width="120"> | <img src="posters/img/25-one-cloud-stayed.jpeg" width="120"> | <img src="posters/img/26-the-day-drained-into-the-pool.jpeg" width="120"> |

### 系列 — Seasons（四季）

十八张一册，分四章。每一季先是一张封面，然后是这一季的内页。
按顺序读：[`/album/?series=seasons`](album/?series=seasons)。

**封面 `28–31`** —— 同一棵树，一年拍四次。

| | | | |
|:--:|:--:|:--:|:--:|
| <img src="posters/img/28-seasons-spring.jpeg" width="120"> | <img src="posters/img/29-seasons-summer.jpeg" width="120"> | <img src="posters/img/30-seasons-autumn.jpeg" width="120"> | <img src="posters/img/31-seasons-winter.jpeg" width="120"> |

**内页 `32–45`** —— 十四张照片，一张一个 Variation Engine 配方。
带标题与介绍的题注版在 [`posters/plates/`](posters/plates)，图册里用 `题注版` 开关切换，
或直接打开 [`album/?series=seasons&plates=1`](album/?series=seasons&plates=1)。

| | | | | | | |
|:--:|:--:|:--:|:--:|:--:|:--:|:--:|
| <img src="posters/img/32-spring-it-happened-without-us.jpeg" width="92"> | <img src="posters/img/33-spring-the-tree-turned-into-weather.jpeg" width="92"> | <img src="posters/img/34-spring-almost-nothing-for-a-week.jpeg" width="92"> | <img src="posters/img/35-spring-the-field-kept-the-small-ones.jpeg" width="92"> | <img src="posters/img/36-summer-the-water-never-stopped-to-look.jpeg" width="92"> | <img src="posters/img/37-summer-still-going-nobody-near.jpeg" width="92"> | <img src="posters/img/38-summer-one-tree-stayed-green-longer.jpeg" width="92"> |
| <img src="posters/img/39-summer-the-sky-pressed-down.jpeg" width="92"> | <img src="posters/img/40-autumn-it-was-already-leaving.jpeg" width="92"> | <img src="posters/img/41-autumn-the-colour-started-to-rust.jpeg" width="92"> | <img src="posters/img/42-autumn-too-much-of-it-at-once.jpeg" width="92"> | <img src="posters/img/43-winter-the-fog-took-the-garden.jpeg" width="92"> | <img src="posters/img/44-winter-it-looked-like-frost.jpeg" width="92"> | <img src="posters/img/45-winter-someone-stood-very-still.jpeg" width="92"> |

做封面要把 Variation Engine 反过来：配方锁死，只留一个变量。
而文生图守不住版式——同一段提示词跑四次就是四个版面。
所以模型只负责方形照片，纸、图版位置、文字、细线和色块都由
[`tools/seasons_compose.py`](tools/seasons_compose.py) 按同一张几何表排。
四张除了照片和色块之外逐像素相同。重跑：`python3 tools/seasons_compose.py`。

内页反过来又反了一次：版式每张都要不一样，但纸必须是同一张。
所以版式交回模型（[`tools/seasons_pages.py`](tools/seasons_pages.py) 存着十四个配方并编译 prompt），
纸交给代码：[`tools/paper_normalize.py`](tools/paper_normalize.py) 先估出每张自己的纸白点，
把它除掉，只留下纯墨密度，再把这层墨重新印到封面那张纸上。
空白处正好落在共用纸上；因为是逐通道的比值而不是加一层色，墨的色相和饱和度不受影响。
十八张现在实测都是 229–230 / 221–222 / 203–204。
重跑：`python3 tools/paper_normalize.py 原图... --outdir 输出目录`。

十八张还各有一个**题注版**，在 [`posters/plates/`](posters/plates)：
标题、中文标题、介绍直接印在纸上，一套图递给别人时不需要旁边有这个仓库。
图版是**原尺寸装裱**而不是直接压字：那些负空间是过了 Quality Gate 的构图的一部分，
而且每张都带 skill 要求的印刷暗角，底边比空纸暗 13 级 —— 四边包上纸以后，
那条暗边就回到了它本来的身份：图版自己的边缘。
生成：`python3 tools/caption_plates.py`。整本打包发人：`python3 tools/seasons_pack.py`
—— ZIP 里文件名按阅读顺序编号，并附一份纯文本目录，因为一套文件交到别人手上时，
旁边不会有这个页面。包内还有一份 A4 打印版 PDF（`tools/seasons_pdf.py`），
图版按原生 300 dpi 摆放，而不是拉满页面。

色块大小不再靠目测：`tools/accent_audit.py` 在 CIELAB 里按色相 ±30° 卡出真正的彩墨，
量出每张占画布与占视觉簇的比例，并用代码合成的封面（已知 1.6%）校准过。

中文排版是认真做的：按字面而不是 `font.size` 定位、全角标点挤压 0.26em
（折行宽度用同一套 advance）、避头尾、`88%` 这类拉丁不拆、十八张同开本、
页脚钉底不随介绍长度浮动。缺字是用 fontTools 查 cmap 逐字确认的，不是肘眼看。

> 十四张照片全是春夏拍的，所以秋、冬两章是**诗意读法**——按气氛归的，不是按拍摄时间。
> 季节只是 `index.json` 里的一个 `season` 字段，随时可以改。

想像翻书一样浏览，在仓库根目录起一个静态服务，然后打开 `/album/`：

```bash
python3 -m http.server 8080   # 然后访问 http://localhost:8080/album/
```

图册支持按系列 / layout / mood / 强调色筛选、方向键翻页、一键复制 prompt，以及打印成每页一张的 PDF。
选 **Seasons 影集**时会换成分章阅读顶序：每季先封面、再内页，打印时每一章从新的一页开始。

## 安装

把公开仓库直接克隆到 Codex 的技能目录：

```bash
git clone https://github.com/LiamGvchi/gc-minimal-zine-poster.git \  ~/.codex/skills/gc-minimal-zine-poster-v0-1
```

如果技能没有立即出现，请重启 Codex。

## 使用方法

按名称调用技能，并提供主题或简报：

```text
用 $gc-minimal-zine-poster-v0-1 制作一张“雨天旧书店”主题的海报
```

也可以提供一句话、文章构想、物件、情绪或参考图片。

## 输出

每次生成时，这个技能会返回：

1. 生成的位图海报图像
2. 最终的图像生成提示词
3. 所选变化方案，以及一段简短的诠释说明

工作流默认采用 Standard Mode，并会直接生成图片。只有在你明确要求“只要提示词”时，它才会停在仅输出提示词的阶段。

## 仓库结构

- `SKILL.md`：完整的 Codex 技能说明
- `README.md`：英文概览与安装说明
- `LICENSE`：MIT 许可证
- `examples/`：精选的已生成海报
- `posters/`：图册归档——生成的海报，以及记录配方与完整 prompt 的 `index.json`
- `album/`：`posters/` 的静态图册浏览器

这个仓库只发布这一个独立技能。其他私有仓库可能会集中备份多个本地技能，但私有备份自动化和无关技能不会放在这里。

## 许可证

MIT。详见 `LICENSE`。

`46–51` 是第二个系列 **Colorful Journey（旅程留色）**：六张旅行照片，同一个 skill，但纸底刻意做白（实测 250–253，R−B 4–6），保留的彩色面积刻意放大（占版面 1.4%–7.9%，其中四张高于 skill 2.5% 的上限）。两处偏离都是按要求做的，实测数据和返工记录见 `posters/README.md`。
