# GC Minimal Zine Poster

**English** · [简体中文](README.zh-CN.md) · [日本語](README.ja.md)


A Codex skill for turning a theme, sentence, object, mood, article idea, photo, or content brief into a quiet minimal zine-style editorial poster prompt and a generated raster image.

The callable skill name is `gc-minimal-zine-poster-v0-1`.

## Visual Direction

The skill compiles each request into a sparse vertical paper poster with:

- a 3:5 aged-paper canvas
- 70%-90% negative space
- one small imageable subject or visual cluster
- serif, typewriter, or monospaced typography
- one clearly visible high-chroma color anchor
- xerox, risograph, halftone, letterpress, or scanned-paper defects
- a quiet Japanese/Korean indie-zine or minimal editorial mood

It avoids commercial advertising layouts, glossy mockups, cinematic lighting, 3D rendering, neon, dense scrapbooks, and long clean text blocks.

## Examples

| Night Door | Yellow Step |
| --- | --- |
| ![Night Door](examples/night-door.jpeg) | ![Yellow Step](examples/yellow-step.jpeg) |

| Shore Pause | Pause Map |
| --- | --- |
| ![Shore Pause](examples/shore-pause.jpeg) | ![Pause Map](examples/pause-map.jpeg) |

| Typhoon Memory | Moon Tide |
| --- | --- |
| ![Typhoon Memory](examples/typhoon-memory.jpeg) | ![Moon Tide](examples/moon-tide.jpeg) |

## Album

A growing album of sheets generated with this skill lives in [`posters/`](posters/README.md) —
45 posters so far, each with its full final prompt, variation recipe, and source note in
[`posters/index.json`](posters/index.json). Sheets `01–27` are one-offs; `28–45` are the
**Seasons** album — four covers and fourteen interior pages.

| | | | | |
|:--:|:--:|:--:|:--:|:--:|
| <img src="posters/img/04-someone-wired-the-sky.jpeg" width="120"> | <img src="posters/img/09-the-edge-of-the-day.jpeg" width="120"> | <img src="posters/img/14-tiao-jin-ran-gang.jpeg" width="120"> | <img src="posters/img/17-there-is-another-world.jpeg" width="120"> | <img src="posters/img/20-you-ren-tiao-hai.jpeg" width="120"> |
| <img src="posters/img/21-the-cloud-ate-the-fire.jpeg" width="120"> | <img src="posters/img/22-we-stood-under-the-sign.jpeg" width="120"> | <img src="posters/img/23-someone-put-a-hat-on-the-lion.jpeg" width="120"> | <img src="posters/img/25-one-cloud-stayed.jpeg" width="120"> | <img src="posters/img/26-the-day-drained-into-the-pool.jpeg" width="120"> |

### Series — Seasons

An eighteen-sheet album in four chapters. Each season opens with a cover, then runs its
interior pages. Read it in order at [`/album/?series=seasons`](album/?series=seasons).

**Covers `28–31`** — one tree, photographed four times in a year.

| | | | |
|:--:|:--:|:--:|:--:|
| <img src="posters/img/28-seasons-spring.jpeg" width="120"> | <img src="posters/img/29-seasons-summer.jpeg" width="120"> | <img src="posters/img/30-seasons-autumn.jpeg" width="120"> | <img src="posters/img/31-seasons-winter.jpeg" width="120"> |

**Interior `32–45`** — fourteen photographs, one Variation Engine recipe each.
Captioned versions of all eighteen live in [`posters/plates/`](posters/plates);
the viewer can switch to them with the `题注版` toggle, or open
[`album/?series=seasons&plates=1`](album/?series=seasons&plates=1).

| | | | | | | |
|:--:|:--:|:--:|:--:|:--:|:--:|:--:|
| <img src="posters/img/32-spring-it-happened-without-us.jpeg" width="92"> | <img src="posters/img/33-spring-the-tree-turned-into-weather.jpeg" width="92"> | <img src="posters/img/34-spring-almost-nothing-for-a-week.jpeg" width="92"> | <img src="posters/img/35-spring-the-field-kept-the-small-ones.jpeg" width="92"> | <img src="posters/img/36-summer-the-water-never-stopped-to-look.jpeg" width="92"> | <img src="posters/img/37-summer-still-going-nobody-near.jpeg" width="92"> | <img src="posters/img/38-summer-one-tree-stayed-green-longer.jpeg" width="92"> |
| <img src="posters/img/39-summer-the-sky-pressed-down.jpeg" width="92"> | <img src="posters/img/40-autumn-it-was-already-leaving.jpeg" width="92"> | <img src="posters/img/41-autumn-the-colour-started-to-rust.jpeg" width="92"> | <img src="posters/img/42-autumn-too-much-of-it-at-once.jpeg" width="92"> | <img src="posters/img/43-winter-the-fog-took-the-garden.jpeg" width="92"> | <img src="posters/img/44-winter-it-looked-like-frost.jpeg" width="92"> | <img src="posters/img/45-winter-someone-stood-very-still.jpeg" width="92"> |

The covers need the opposite of the Variation Engine: the recipe is locked and only one
variable moves. Text-to-image cannot hold a layout still across four runs, so the model
only renders the square photographic plate — paper, plate position, type, rule and colour
chop are placed by [`tools/seasons_compose.py`](tools/seasons_compose.py) from a single
shared geometry table. The four sheets are pixel-identical apart from the photograph and
the accent. Rebuild them with `python3 tools/seasons_compose.py`.

The interior pages need the opposite again: every layout different, but every sheet on the
same paper. So the layout goes back to the model ([`tools/seasons_pages.py`](tools/seasons_pages.py)
holds the fourteen recipes and compiles the prompts), and the paper goes to code:
[`tools/paper_normalize.py`](tools/paper_normalize.py) estimates each generated sheet's own
paper white point, divides it out to recover pure ink density, and re-prints that ink onto
the covers' stock. Blank paper lands on the shared sheet; ink hue and saturation survive,
because it is a per-channel ratio and not a colour cast. All eighteen sheets now measure
229–230 / 221–222 / 203–204.

Each of the eighteen sheets also exists as a **captioned plate** in
[`posters/plates/`](posters/plates), with its title, Chinese title and note
printed on the paper below the image, so a set can be handed to someone without
this repository around it. The image is mounted at full size on a larger sheet
with a mat on all four sides rather than being overprinted: the negative space
on each poster is part of a composition that passed the Quality Gate, and every
sheet carries the printing vignette the skill asks for, which leaves its bottom
edge about 13 levels darker than bare paper. Surrounded, that edge reads as what
it is. Build them with `python3 tools/caption_plates.py`, and package the whole
album for sending with `python3 tools/seasons_pack.py` — the ZIP numbers its
files in reading order and carries a plain-text contents file, because a set of
files handed to someone has to be legible without this page next to it. The ZIP
also carries an A4 print PDF (`tools/seasons_pdf.py`) that imposes each plate at
its native 300 dpi rather than scaling it to fill the page.

The Chinese setting is done properly: type is positioned from the printed face
rather than the em box, full-width stops are squeezed back by 0.26em with the
same advance feeding line measurement, punctuation is kept off the start of a
line, ASCII runs like `88%` stay whole, all eighteen pages share one page size,
and the folio is pinned to the foot of the page so it lands on the same line
throughout. Glyph coverage is checked against the font's cmap, not by eye.

To browse it as a book, serve the repository root and open `/album/`:

```bash
python3 -m http.server 8080   # then visit http://localhost:8080/album/
```

The album viewer supports filtering by series / layout / mood / accent colour, arrow-key paging,
one-click prompt copying, and printing one poster per page to PDF.

## Installation

Clone the public repository directly into the Codex skills directory:

```bash
git clone https://github.com/LiamGvchi/gc-minimal-zine-poster.git \
  ~/.codex/skills/gc-minimal-zine-poster-v0-1
```

Restart Codex if the skill does not appear immediately.

## Usage

Invoke the skill by name and provide a theme or brief:

```text
用 $gc-minimal-zine-poster-v0-1 做一张关于雨天旧书店的海报
```

You can also provide a sentence, article idea, object, mood, or reference image.

## Output

For every generation request, the skill returns:

1. the generated raster poster image
2. the final image-generation prompt
3. the selected variation recipe and a short interpretation note

The workflow uses Standard Mode and generates the image by default. It only stops at prompt-only output when the user explicitly asks for that.

## Repository Structure

- `SKILL.md`: the complete Codex skill instructions
- `README.md`: public overview and installation instructions
- `LICENSE`: MIT license
- `examples/`: selected generated posters
- `posters/`: album archive — generated sheets plus `index.json` metadata (recipe + final prompt per sheet)
- `album/`: static album viewer for `posters/`

This repository publishes one standalone skill. A separate private vault may aggregate backups of multiple local skills, but private backup automation and unrelated skills are intentionally excluded here.

## License

MIT. See `LICENSE`.

`46–51` are a second series, **Colorful Journey**: six travel photographs run through the same skill on a deliberately whiter stock (measured 250–253, R−B 4–6) with a deliberately larger surviving colour area (1.4%–7.9% of the sheet, four of them above the skill's 2.5% ceiling). Both departures were asked for; see `posters/README.md` for the measurements and the rework log.
