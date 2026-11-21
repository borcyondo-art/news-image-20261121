# The World in One Picture — 21 November 2026

[![make.fun](https://img.shields.io/badge/make.fun-news--image--20261121-0f766e)](https://make.fun/bounty/news-image-20261121)
[![Python](https://img.shields.io/badge/python-3.13-blue)](https://www.python.org/)
[![image](https://img.shields.io/badge/image-1024%C3%971024-lightgrey)](https://make.fun/bounty/news-image-20261121)
[![deterministic](https://img.shields.io/badge/build-deterministic-green)](https://make.fun/bounty/news-image-20261121)

Entry for the make.fun bounty
[“Sum up 21 November’s world news in one image”](https://make.fun/bounty/news-image-20261121)
($100, top 50 paid; deadline 23 November 2026 00:00 UTC).

## What it is

`main.py` draws a newspaper front page — **“The World in One Picture —
21 Nov 2026”** — and writes it to `/output/entry.png` (1024×1024 PNG,
under 1 MiB). It uses only the Python standard library plus Pillow, needs
no network, and is fully deterministic: two runs write identical bytes.

## The day’s news

- **Lead — COP31 in overtime (Antalya, Türkiye):** fossil-fuel deadlock
  drags the climate talks past their deadline; a third draft is due on
  Saturday. Nearly 200 nations deadlocked over a draft deal that drops
  every mention of fossil fuels and a $120bn adaptation fund; the EU warns
  the summit risks becoming a “fossil summit”.
- **Markets:** Wall Street slides into correction — US stocks fell about
  3.7% on Friday as AI shares sold off.
- **Europe:** Estonia shuts its Russia border after suspected arson
  sabotage.
- **Asia:** Mongolia’s president resigns, setting the stage for a snap
  election.
- **Cyber:** JPMorgan, Visa and Mastercard report a cyberattack on
  third-party vendors; core payment networks unaffected.
- **Sport:** India fight back in the Wellington Test (159 for 1 at stumps,
  day two).
- **Motors:** Hyundai unveils the eighth-generation Elantra at the Los
  Angeles Auto Show.
- **Ticker:** Warsaw seeks more NATO forces after the missile incursion;
  Denmark alleges a Russian plot to kill a US-Ukrainian; Nikhil Gupta
  jailed 19+ years in the US; Panama threatens a COP31 walkout; Sensex
  rallies 898 points.

All stories were first reported on Saturday 21 November 2026 (UTC).

## Run it

```sh
python3 main.py   # writes /output/entry.png
```

## License

MIT — see `LICENSE`.
