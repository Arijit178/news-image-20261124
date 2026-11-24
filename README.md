# The World in One Day — Tuesday, 24 November 2026

[![make.fun](https://make.fun/badge/news-image-20261124.svg)](https://make.fun/bounty/news-image-20261124)
[![make.fun rank](https://make.fun/badge/news-image-20261124/Arijit178/news-image-20261124/rank.svg)](https://make.fun/bounty/news-image-20261124)
[![make.fun reward](https://make.fun/badge/news-image-20261124/Arijit178/news-image-20261124/reward.svg)](https://make.fun/bounty/news-image-20261124)

One 1024×1024 poster for the make.fun bounty
"Sum up 24 November's world news in one image"
(news-image-20261124). It is a front page for Tuesday
24 November 2026, with eight stories from that day.

## How it is made

`draw.py` renders `entry.png` with Python and Pillow, using only
DejaVu fonts and flat shapes drawn in the script — no photographs
and no copied artwork. `main.ts` runs on Node 22 with the standard
library only, and copies `entry.png` byte for byte into the output
directory the grader names in `$MAKEFUN_OUTPUT_DIR` (`/output`
by default), so two runs produce identical bytes.

```sh
python3 draw.py
mkdir -p out && MAKEFUN_OUTPUT_DIR=out node main.ts
```

## Stories in the picture

1. **Hormuz** — Iran says four tankers were hit by mines and the
   strait stays closed until Washington meets Tehran's conditions.
   (Daily Summary of World, 24 Nov 2026)
2. **The Hague** — The ICJ finds Myanmar guilty of genocide against
   the Rohingya in 2017, 9–6, the first time the UN's highest court
   has found a state responsible for genocide. (Daily Summary / ICJ,
   24 Nov 2026)
3. **Gaza** — Israel kills Hamas internal security chief Brig. Gen.
   Naeem Abu Nahel in a strike; six others are killed.
   (Reuters / Daily Summary, 24 Nov 2026)
4. **Space** — NATO chief Mark Rutte vows defence against a space
   threat, after reports Russia may launch a nuclear-armed satellite,
   dubbed Sputnik-S, within 60 days. (BBC / German media, 24 Nov 2026)
5. **Zaporizhzhia** — An overnight Russian attack kills 2 and wounds
   40, including four children, hitting an apartment building.
   (Just Security Early Edition / Kyiv Independent, 24 Nov 2026)
6. **Villavicencio, Colombia** — A car bomb outside regional
   government offices injures 23, on the eve of the 10th anniversary
   of the FARC peace deal. (Daily Summary, 24 Nov 2026)
7. **London** — The UK sanctions Yemen's Houthis and four senior
   officials, with asset freezes and travel bans.
   (Daily Summary, 24 Nov 2026)
8. **Nepal** — A magnitude 5.4 earthquake strikes Koshi Province;
   tremors are felt across India, Bhutan and Bangladesh.
   (The Statesman, 24 Nov 2026)

## Licence

MIT — see LICENSE.
