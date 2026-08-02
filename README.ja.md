# GC Minimal Zine Poster

[English](README.md) · [简体中文](README.zh-CN.md) · **日本語**

テーマ、短い文章、物、雰囲気、記事のアイデア、写真、コンテンツの概要から、静かでミニマルな ZINE 風エディトリアルポスター用のプロンプトと、対応するラスター画像を生成する Codex スキルです。

呼び出し名は `gc-minimal-zine-poster-v0-1` です。

## ビジュアル方針

各リクエストを、余白を活かした縦長の紙のポスターとして構成します。

- 3:5 比率の古びた紙を思わせるキャンバス
- 70%〜90% のネガティブスペース
- 小さく、視覚的に明確な一つの主題またはビジュアルのまとまり
- セリフ、タイプライター、または等幅書体
- はっきり見える高彩度のカラーアクセント
- ゼロックス、リソグラフ、ハーフトーン、活版印刷、スキャン紙の欠けや質感
- 静かな日本／韓国のインディー ZINE、またはミニマルなエディトリアルデザインの空気感

商業広告のレイアウト、光沢のあるモックアップ、映画的な照明、3D レンダリング、ネオン、密集したスクラップブック、大量の整った文章は避けます。

## 作例

| Night Door | Yellow Step |
| --- | --- |
| ![Night Door](examples/night-door.jpeg) | ![Yellow Step](examples/yellow-step.jpeg) |

| Shore Pause | Pause Map |
| --- | --- |
| ![Shore Pause](examples/shore-pause.jpeg) | ![Pause Map](examples/pause-map.jpeg) |

| Typhoon Memory | Moon Tide |
| --- | --- |
| ![Typhoon Memory](examples/typhoon-memory.jpeg) | ![Moon Tide](examples/moon-tide.jpeg) |

## アルバム

このスキルで生成したポスターは [`posters/`](posters/README.md) に保管しています。現在 45 点。
`01–27` は単発、`28–45` は **Seasons 四季アルバム**（表紙 4 枚 + 本文 14 枚）です。
各シートの**最終プロンプト・バリエーション方針・出典メモ**は [`posters/index.json`](posters/index.json) に記録されています。

| | | | | |
|:--:|:--:|:--:|:--:|:--:|
| <img src="posters/img/04-someone-wired-the-sky.jpeg" width="120"> | <img src="posters/img/09-the-edge-of-the-day.jpeg" width="120"> | <img src="posters/img/14-tiao-jin-ran-gang.jpeg" width="120"> | <img src="posters/img/17-there-is-another-world.jpeg" width="120"> | <img src="posters/img/20-you-ren-tiao-hai.jpeg" width="120"> |
| <img src="posters/img/21-the-cloud-ate-the-fire.jpeg" width="120"> | <img src="posters/img/22-we-stood-under-the-sign.jpeg" width="120"> | <img src="posters/img/23-someone-put-a-hat-on-the-lion.jpeg" width="120"> | <img src="posters/img/25-one-cloud-stayed.jpeg" width="120"> | <img src="posters/img/26-the-day-drained-into-the-pool.jpeg" width="120"> |

### シリーズ — Seasons（四季）

18 枚を 4 章に分けたアルバム。各季はまず表紙があり、そのあとに本文が続きます。
順番に読むなら [`/album/?series=seasons`](album/?series=seasons)。

**表紙 `28–31`** —— 同じ一本の樹を、一年に四度撮る。

| | | | |
|:--:|:--:|:--:|:--:|
| <img src="posters/img/28-seasons-spring.jpeg" width="120"> | <img src="posters/img/29-seasons-summer.jpeg" width="120"> | <img src="posters/img/30-seasons-autumn.jpeg" width="120"> | <img src="posters/img/31-seasons-winter.jpeg" width="120"> |

**本文 `32–45`** —— 14 枚の写真、それぞれに Variation Engine のレシピを一つ。
キャプション版は [`posters/plates/`](posters/plates)。ビューアーの `题注版` トグル、
または [`album/?series=seasons&plates=1`](album/?series=seasons&plates=1) から。

| | | | | | | |
|:--:|:--:|:--:|:--:|:--:|:--:|:--:|
| <img src="posters/img/32-spring-it-happened-without-us.jpeg" width="92"> | <img src="posters/img/33-spring-the-tree-turned-into-weather.jpeg" width="92"> | <img src="posters/img/34-spring-almost-nothing-for-a-week.jpeg" width="92"> | <img src="posters/img/35-spring-the-field-kept-the-small-ones.jpeg" width="92"> | <img src="posters/img/36-summer-the-water-never-stopped-to-look.jpeg" width="92"> | <img src="posters/img/37-summer-still-going-nobody-near.jpeg" width="92"> | <img src="posters/img/38-summer-one-tree-stayed-green-longer.jpeg" width="92"> |
| <img src="posters/img/39-summer-the-sky-pressed-down.jpeg" width="92"> | <img src="posters/img/40-autumn-it-was-already-leaving.jpeg" width="92"> | <img src="posters/img/41-autumn-the-colour-started-to-rust.jpeg" width="92"> | <img src="posters/img/42-autumn-too-much-of-it-at-once.jpeg" width="92"> | <img src="posters/img/43-winter-the-fog-took-the-garden.jpeg" width="92"> | <img src="posters/img/44-winter-it-looked-like-frost.jpeg" width="92"> | <img src="posters/img/45-winter-someone-stood-very-still.jpeg" width="92"> |

表紙では Variation Engine を逆に使います。レシピを固定し、変数は一つだけ。
ただし text-to-image はレイアウトを 4 回同じに保てないため、モデルには正方形の
写真部分だけを描かせ、用紙・図版位置・文字・罫線・色面は
[`tools/seasons_compose.py`](tools/seasons_compose.py) が単一の幾何表から配置します。
4 枚は写真とアクセント以外、ピクセル単位で同一です。再生成は `python3 tools/seasons_compose.py`。

本文はもう一度逆になります。レイアウトは全枚違うけれど、用紙は全枚同じでなければならない。
だからレイアウトはモデルに戻し（[`tools/seasons_pages.py`](tools/seasons_pages.py) が 14 のレシピを保持して
プロンプトを組み立てます）、用紙はコードに任せます。
[`tools/paper_normalize.py`](tools/paper_normalize.py) が各枚の用紙ホワイトポイントを推定して割り除き、
純粋なインク濃度だけを取り出して、それを表紙と同じ用紙に刷り直します。
余白は共通の紙に乗り、チャンネルごとの比なので色かぶりにならず、インクの色相と彩度は残ります。
18 枚の実測値はすべて 229–230 / 221–222 / 203–204。
再実行は `python3 tools/paper_normalize.py 元画像... --outdir 出力先`。

18 枚にはそれぞれ**キャプション版**が [`posters/plates/`](posters/plates) にあります。
タイトル・中国語タイトル・解説を紙に直接刷ってあるので、このリポジトリなしで
一揃いを人に渡せます。図版は縮小せず原寸で台紙にマウントしています。余白は
Quality Gate を通った構成の一部であり、各枚が skill の求める刷りのビネットを
持つため下端が紙より 13 レベル暗い —— 四辺を紙で囲むと、その暗い緋は本来の
意味（図版の縁）に戻ります。生成は `python3 tools/caption_plates.py`、
一冊分のパッケージ化は `python3 tools/seasons_pack.py`。ZIP のファイル名は読む順に
番号を振り、テキストの目次を同梱します。人に渡す一揃いは、この README が隣に
ない状態で読めなければ意味がないからです。ZIP には A4 印刷用 PDF
（`tools/seasons_pdf.py`）も入っています。図版はページに合わせて拡大せず、
ネイティブの 300 dpi のまま配置します。

中国語組版は手を抜いていません。字面基準の配置、全角句読点の 0.26em 詰め
（行長測定も同じ advance）、禁則処理、`88%` のような欧文は分割しない、
18 枚同じ判型、ノンブルはページ下端に固定。グリフの有無は fontTools で
cmap を読んで確認しています。

> 14 枚の写真はすべて春と夏のものです。よって秋と冬の章は**詩的な読み替え**で、
> 撮影日でなく空気の色で分けています。季節は `index.json` の `season` フィールドなので、いつでも変えられます。

本のようにめくって見るには、リポジトリのルートで静的サーバーを起動し `/album/` を開きます。

```bash
python3 -m http.server 8080   # http://localhost:8080/album/ を開く
```

アルバムはシリーズ / layout / mood / アクセント色での絞り込み、矢印キーでのページ送り、
プロンプトのワンクリックコピー、1 ページ 1 枚での PDF 印刷に対応しています。
**Seasons アルバム**を選ぶと章分けの読み順に切り替わり（各季は表紙 → 本文）、
印刷時は章ごとに新しいページから始まります。

## インストール

公開リポジトリを Codex のスキルディレクトリへ直接クローンします。

```bash
git clone https://github.com/LiamGvchi/gc-minimal-zine-poster.git \  ~/.codex/skills/gc-minimal-zine-poster-v0-1
```

スキルがすぐに表示されない場合は、Codex を再起動してください。

## 使い方

スキル名を指定し、テーマまたは概要を渡します。

```text
$gc-minimal-zine-poster-v0-1 を使って、雨の日の古書店をテーマにしたポスターを作って
```

短い文章、記事のアイデア、物、雰囲気、参照画像を渡すこともできます。

## 出力

各回の生成では、次の内容が返されます。

1. 生成されたラスター形式のポスター画像
2. 最終的な画像生成プロンプト
3. 選んだバリエーションの方針と、短い解釈メモ

ワークフローは Standard Mode を使い、デフォルトで画像を生成します。明確に「プロンプトだけ」を求めた場合にだけ、画像を生成せずプロンプトのみを返します。

## リポジトリ構成

- `SKILL.md`：Codex スキルの完全な手順
- `README.md`：英語版の概要とインストール手順
- `LICENSE`：MIT ライセンス
- `examples/`：選定済みの生成ポスター
- `posters/`：アルバム保管庫——生成したシートと、方針・最終プロンプトを記録した `index.json`
- `album/`：`posters/` を閲覧する静的アルバムビューア

このリポジトリで公開しているのは、この単独スキルだけです。別の非公開リポジトリに複数のローカルスキルのバックアップを集約する場合がありますが、非公開バックアップの自動化や無関係なスキルはここには含めません。

## ライセンス

MIT。詳細は `LICENSE` を参照してください。

`46–51` は第二のシリーズ **Colorful Journey**。同じスキルで旅の写真 6 枚を刷り直したもので、紙はより白く（実測 250–253、R−B 4–6）、残す色の面積は意図的に広げてある（版面の 1.4%–7.9%、うち 4 枚はスキルの上限 2.5% を超える）。いずれも依頼による逸脱。計測値と再生成の記録は `posters/README.md` を参照。

`52–57` は第三のシリーズ **Plates（全面図版）**。`46–51` と一対一で対応し、写真も文言も色相も同じだが、写真をアンカーに縮めず全面の図版として刷っている。理由は構造的なもので、スキルの `Image Anchor` の語彙はちょうど 8 項目しかなく、そのすべてが元画像を縮小・平坦化・断片化する方向にしか働かない。「写真をきちんと見せる」という選択肢がそもそも語彙に存在しない。そこで本シリーズは Color Engine の「版面の 0.8%–2.5%」という寸法規則を明確に放棄した。図版は実測で版面の 27.9%–41.4% を占める。根拠はスキル自身の *Prefer a colored … image panel* という一文と、禁止事項が禁じているのは**裁ち落とし**であって寸法ではないという点。それ以外は踏襲している —— ほぼ白の紙、フラットスキャン、最小限の文字組み、印刷の粗、1 枚 1 色相。
