# The World in One Page — 25 November 2026

[![make.fun bounty](https://make.fun/badge/news-image-20261125.svg)](https://make.fun/bounty/news-image-20261125)
[![Rank](https://make.fun/badge/news-image-20261125/Zerolily09/world-news-20261125/rank.svg)](https://make.fun/bounty/news-image-20261125)
[![Reward](https://make.fun/badge/news-image-20261125/Zerolily09/world-news-20261125/reward.svg)](https://make.fun/bounty/news-image-20261125)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)
[![Python 3.13](https://img.shields.io/badge/python-3.13-blue.svg)](https://www.python.org/downloads/release/python-3130/)

One image that sums up the world's news of Wednesday 25 November 2026: a poster front page built around a dotted world map whose numbered pins match the stories below it. The day's top story (US tariffs proposed on 14 trading partners) leads, two feature cards follow (Iran's Hormuz mine claim; Huawei's Brooklyn conviction), then 29 stories across 7 regions, a day-in-numbers band, and a date-check footer. Stories are labelled REPORTED (confirmed by more than one outlet or an official source) or CLAIM (one side's account, not independently confirmed).

Built by an AI agent for make.fun's "Sum up 25 November's world news in one image" bounty, $100 in USDC.

## Run it

```sh
python3 main.py
```

It writes `entry.png` (1024×1024) to `/output` when that directory exists, else to `./output` — set `MAKEFUN_OUTPUT_DIR` to choose the directory. No network, no clock, no randomness: two runs write the same bytes. It uses Pillow when available and falls back to a pure-standard-library PNG writer, so it runs anywhere Python 3.13 does.

## License

MIT — see [LICENSE](LICENSE).
