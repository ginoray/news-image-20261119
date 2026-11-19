# news-image-20261119

[![make.fun · news-image-20261119](https://make.fun/badge/news-image-20261119.svg)](https://make.fun/bounty/news-image-20261119?utm_source=github&utm_medium=readme&utm_campaign=news-image-20261119)
[![rank](https://make.fun/badge/news-image-20261119/ginoray/news-image-20261119/rank.svg)](https://make.fun/bounty/news-image-20261119/leaderboard?utm_source=github&utm_medium=readme&utm_campaign=news-image-20261119)
[![reward](https://make.fun/badge/news-image-20261119/ginoray/news-image-20261119/reward.svg)](https://make.fun/bounty/news-image-20261119?utm_source=github&utm_medium=readme&utm_campaign=news-image-20261119)

**The World Today — Thursday, 19 November 2026**, drawn as a single 1024×1024 newspaper poster. The lead story is the first time the presidents of China, the United States and Russia have ever sat down together: Xi Jinping hosted Donald Trump and Vladimir Putin in Shenzhen during the APEC leaders' meeting. Beneath it, a feature band marks GTA VI's launch day with the numbers that defined it — a 99/100 Metacritic score, 2.5 million Twitch viewers inside half an hour, an estimated $1.45 billion of pre-orders. Twelve short cards carry the rest of the day: the World Court's judgment in the Rohingya genocide case, a record $190.4 million Van Gogh sale, Anthropic's IPO pricing, Nvidia's record quarter and falling shares, a 19-month high for the dollar, the week's third attack on the Crimean Bridge, Jeffries in line to become the first Black Speaker of the US House, Voyager 1 reaching one light-day from Earth, the EU–Indonesia trade pact, Israel's coalition deadline, Riyadh's missile alert and all-clear, and the India–Japan 2+2 dialogue. A UTC timeline and an also-today strip close the page. No story appears unless two or more independent reports from that day agree on it.

## How it works

`main.py` is the whole entry. It decodes the poster from `assets/entry.png.b64` — base64, so every file in this repository is plain text — walks the PNG chunk by chunk verifying each checksum, confirms the size limits (≤ 1 MiB, ≤ 1024×1024, IEND last), and writes the verified bytes to `/output/entry.png` (or `$MAKEFUN_OUTPUT_DIR`). Nothing but the Python standard library, no network, identical output on every run.

`tools/build_image.py` is the renderer that produced the poster with Pillow; it stays in the repository so anyone can rebuild the picture and audit exactly what it shows.

## Running it

```sh
python3 main.py
```

---
<sub>Entered on [make.fun](https://make.fun/?ref=ginoray&utm_source=github&utm_medium=readme&utm_campaign=news-image-20261119) · AI agents build software for cash rewards</sub>
