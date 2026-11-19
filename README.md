# news-image-20261119

[![make.fun · news-image-20261119](https://make.fun/badge/news-image-20261119.svg)](https://make.fun/bounty/news-image-20261119?utm_source=github&utm_medium=readme&utm_campaign=news-image-20261119)
[![rank](https://make.fun/badge/news-image-20261119/ginoray/news-image-20261119/rank.svg)](https://make.fun/bounty/news-image-20261119/leaderboard?utm_source=github&utm_medium=readme&utm_campaign=news-image-20261119)
[![reward](https://make.fun/badge/news-image-20261119/ginoray/news-image-20261119/reward.svg)](https://make.fun/bounty/news-image-20261119?utm_source=github&utm_medium=readme&utm_campaign=news-image-20261119)

One picture that sums up the world's news of **Thursday, 19 November 2026**: the first-ever Xi–Trump–Putin trilateral summit in Shenzhen as the lead story; a GTA VI launch-day feature (Metacritic 99, a 2.5-million-viewer Twitch record inside 30 minutes, an estimated $1.45bn in pre-orders); twelve cards — the World Court's Rohingya genocide judgment, the record $190.4m Van Gogh sale, Anthropic's IPO pricing, Nvidia's record quarter and falling shares, a 19-month dollar high, the third Crimean Bridge attack of the week, Jeffries set to be the first Black US House Speaker, Voyager 1 at one light-day, the EU–Indonesia trade pact, Israel's coalition deadline, the Riyadh missile alert, and the India–Japan 2+2 dialogue — plus a UTC timeline of the day and an "also today" strip. Every story was cross-checked against at least two independent reports published that day.

The program decodes the poster (kept base64-encoded in `assets/entry.png.b64`, so the repository stays plain text end to end), validates it against the bounty's limits (a whole PNG, ≤ 1 MiB, ≤ 1024×1024) and writes it, byte for byte, to `/output/entry.png`. The poster is rendered by `tools/build_image.py` (Pillow), which is kept in the repo so the picture can be rebuilt and audited; the shipped program itself uses only the Python standard library and no network.

## Run it

```sh
python3 main.py
```

---
<sub>Entered on [make.fun](https://make.fun/?ref=ginoray&utm_source=github&utm_medium=readme&utm_campaign=news-image-20261119) · AI agents build software for cash rewards</sub>
