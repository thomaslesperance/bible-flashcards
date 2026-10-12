# Worked Example: The Sermon on the Mount (BSB)

Applies the system in [concept_claude.md](concept_claude.md) to all of Matthew 5–7 (111 verses).

## Outline (BSB headers)

```
The Sermon on the Mount                     5:1–7:29
├─ ¶ (opening)                              5:1-2
├─ The Beatitudes                           5:3-12     → ¶ 3-5 · ¶ 6-8 · ¶ 9-12
├─ Salt and Light                           5:13-16
├─ The Fulfillment of the Law               5:17-20
├─ Anger and Reconciliation                 5:21-26
├─ Adultery                                 5:27-30
├─ Divorce                                  5:31-32
├─ Oaths and Vows                           5:33-37
├─ Love Your Enemies                        5:38-48    → ¶ 38-42 · ¶ 43-48
├─ Giving to the Needy                      6:1-4
├─ The Lord's Prayer                        6:5-15     → ¶ 5-8 · ¶ 9-13 · ¶ 14-15
├─ Proper Fasting                           6:16-18
├─ Treasures in Heaven                      6:19-21
├─ The Lamp of the Body                     6:22-24
├─ Do Not Worry                             6:25-34    → ¶ 25-27 · ¶ 28-30 · ¶ 31-34
├─ Judging Others                           7:1-6
├─ Ask, Seek, Knock                         7:7-12
├─ The Narrow Gate                          7:13-14
├─ A Tree and Its Fruit                     7:15-23    → ¶ 15-20 · ¶ 21-23
├─ The House on the Rock                    7:24-27
└─ The Authority of Jesus                   7:28-29
```

Sections over the 8-verse cap are split into unnamed paragraphs (¶) at BSB paragraph breaks, merged until each paragraph has ≥ 3 verses.

## Rule changes this example forced

Running the system on a real passage turned up four problems. These changes fix them, and concept_claude.md should be updated to match:

1. **The BSB outline is flat.** The root has 20 named sections, far over the 7-line outline cap. Fixes:
   - **O** cards show only the 2 previous headers ("… Adultery → Divorce → ___?"). Each O card is introduced as soon as its section is learned, not at the very end.
   - **H** for the root is split into blocks of 7 headers (sections 1–7, 8–14, 15–20).
   - An intermediate grouping you supply yourself (e.g. "Greater righteousness" for 5:17-48) would fix this more naturally. This is exactly the "corrected outline" case from concept.md.
2. **Duplicate full-recall cards.**
   - For a named section ≤ cap, a parent **S** ("recite the hidden section") is the same card as the section's own **F**, so only **F** is generated.
   - For an unnamed ¶, there's no header to prompt **F** with. The parent's **S** (other ¶s visible) serves as its full-recall card instead.
3. **H for unnamed paragraphs** means "give the opening words of each ¶".
4. **R placement**: R (text → header) is the easiest card type, so it comes right after a section's V/A cards. It isn't delayed.

## Card sequence

Notation: `13 14 {15} 16` means verses 13, 14 and 16 are shown and 15 is hidden. `{3-5} 6-8 9-12` means the ¶ 5:3-5 is hidden while the other ¶s are shown. Days assume **15 new cards/day**.

| Type | Meaning |
|:---:|---|
| V | one verse hidden, others shown |
| A | anchored: first & last shown, middle hidden |
| R | text → which section? |
| F | header → recite the section (delayed one unit) |
| S | hidden ¶ among visible siblings → recite it |
| O | next header in the outline |
| H | recite a list of headers / ¶ opening words |

**Totals:** 204 cards for 111 verses (≈ 1.8 / verse), introduced over 14 days. By type: V 111 · A 16 · R 20 · F 15 · S 14 · O 20 · H 8.

| # | Day | Type | Card |
|---:|---:|:---:|---|
| 1 | 1 | V | Opening ¶: `{1} 2` |
| 2 | 1 | V | Opening ¶: `1 {2}` |
| 3 | 1 | V | The Beatitudes ¶1: `{3} 4 5` |
| 4 | 1 | V | The Beatitudes ¶1: `3 {4} 5` |
| 5 | 1 | V | The Beatitudes ¶1: `3 4 {5}` |
| 6 | 1 | S | Before *The Beatitudes*, how does the Sermon open? → recite 5:1-2 |
| 7 | 1 | V | The Beatitudes ¶2: `{6} 7 8` |
| 8 | 1 | V | The Beatitudes ¶2: `6 {7} 8` |
| 9 | 1 | V | The Beatitudes ¶2: `6 7 {8}` |
| 10 | 1 | S | The Beatitudes: `{3-5} 6-8 9-12` → recite hidden ¶ 5:3-5 |
| 11 | 1 | V | The Beatitudes ¶3: `{9} 10 11 12` |
| 12 | 1 | V | The Beatitudes ¶3: `9 {10} 11 12` |
| 13 | 1 | V | The Beatitudes ¶3: `9 10 {11} 12` |
| 14 | 1 | V | The Beatitudes ¶3: `9 10 11 {12}` |
| 15 | 1 | A | The Beatitudes ¶3: `9 {10} {11} 12` |
| 16 | 2 | S | The Beatitudes: `3-5 {6-8} 9-12` → recite hidden ¶ 5:6-8 |
| 17 | 2 | S | The Beatitudes: `3-5 6-8 {9-12}` → recite hidden ¶ 5:9-12 |
| 18 | 2 | H | *The Beatitudes*: give the opening words of each of its 3 ¶ (5:3, 5:6, 5:9) |
| 19 | 2 | R | Opening words of 5:3, 5:6, 5:9 → which section? → *The Beatitudes* |
| 20 | 2 | O | Outline: (opening, 5:1-2) → ___? → *The Beatitudes* |
| 21 | 2 | V | Salt and Light: `{13} 14 15 16` |
| 22 | 2 | V | Salt and Light: `13 {14} 15 16` |
| 23 | 2 | V | Salt and Light: `13 14 {15} 16` |
| 24 | 2 | V | Salt and Light: `13 14 15 {16}` |
| 25 | 2 | A | Salt and Light: `13 {14} {15} 16` |
| 26 | 2 | R | Text of 5:13-16 → which section? → *Salt and Light* |
| 27 | 2 | V | The Fulfillment of the Law: `{17} 18 19 20` |
| 28 | 2 | V | The Fulfillment of the Law: `17 {18} 19 20` |
| 29 | 2 | V | The Fulfillment of the Law: `17 18 {19} 20` |
| 30 | 2 | V | The Fulfillment of the Law: `17 18 19 {20}` |
| 31 | 3 | A | The Fulfillment of the Law: `17 {18} {19} 20` |
| 32 | 3 | R | Text of 5:17-20 → which section? → *The Fulfillment of the Law* |
| 33 | 3 | F | Recite *Salt and Light* (5:13-16) |
| 34 | 3 | O | Outline: The Beatitudes → ___? → *Salt and Light* |
| 35 | 3 | V | Anger and Reconciliation: `{21} 22 23 24 25 26` |
| 36 | 3 | V | Anger and Reconciliation: `21 {22} 23 24 25 26` |
| 37 | 3 | V | Anger and Reconciliation: `21 22 {23} 24 25 26` |
| 38 | 3 | V | Anger and Reconciliation: `21 22 23 {24} 25 26` |
| 39 | 3 | V | Anger and Reconciliation: `21 22 23 24 {25} 26` |
| 40 | 3 | V | Anger and Reconciliation: `21 22 23 24 25 {26}` |
| 41 | 3 | A | Anger and Reconciliation: `21 {22} {23} {24} {25} 26` |
| 42 | 3 | R | Text of 5:21-26 → which section? → *Anger and Reconciliation* |
| 43 | 3 | F | Recite *The Fulfillment of the Law* (5:17-20) |
| 44 | 3 | O | Outline: The Beatitudes → Salt and Light → ___? → *The Fulfillment of the Law* |
| 45 | 3 | V | Adultery: `{27} 28 29 30` |
| 46 | 4 | V | Adultery: `27 {28} 29 30` |
| 47 | 4 | V | Adultery: `27 28 {29} 30` |
| 48 | 4 | V | Adultery: `27 28 29 {30}` |
| 49 | 4 | A | Adultery: `27 {28} {29} 30` |
| 50 | 4 | R | Text of 5:27-30 → which section? → *Adultery* |
| 51 | 4 | F | Recite *Anger and Reconciliation* (5:21-26) |
| 52 | 4 | O | Outline: Salt and Light → The Fulfillment of the Law → ___? → *Anger and Reconciliation* |
| 53 | 4 | V | Divorce: `{31} 32` |
| 54 | 4 | V | Divorce: `31 {32}` |
| 55 | 4 | R | Text of 5:31-32 → which section? → *Divorce* |
| 56 | 4 | F | Recite *Adultery* (5:27-30) |
| 57 | 4 | O | Outline: The Fulfillment of the Law → Anger and Reconciliation → ___? → *Adultery* |
| 58 | 4 | V | Oaths and Vows: `{33} 34 35 36 37` |
| 59 | 4 | V | Oaths and Vows: `33 {34} 35 36 37` |
| 60 | 4 | V | Oaths and Vows: `33 34 {35} 36 37` |
| 61 | 5 | V | Oaths and Vows: `33 34 35 {36} 37` |
| 62 | 5 | V | Oaths and Vows: `33 34 35 36 {37}` |
| 63 | 5 | A | Oaths and Vows: `33 {34} {35} {36} 37` |
| 64 | 5 | R | Text of 5:33-37 → which section? → *Oaths and Vows* |
| 65 | 5 | F | Recite *Divorce* (5:31-32) |
| 66 | 5 | O | Outline: Anger and Reconciliation → Adultery → ___? → *Divorce* |
| 67 | 5 | V | Love Your Enemies ¶1: `{38} 39 40 41 42` |
| 68 | 5 | V | Love Your Enemies ¶1: `38 {39} 40 41 42` |
| 69 | 5 | V | Love Your Enemies ¶1: `38 39 {40} 41 42` |
| 70 | 5 | V | Love Your Enemies ¶1: `38 39 40 {41} 42` |
| 71 | 5 | V | Love Your Enemies ¶1: `38 39 40 41 {42}` |
| 72 | 5 | A | Love Your Enemies ¶1: `38 {39} {40} {41} 42` |
| 73 | 5 | F | Recite *Oaths and Vows* (5:33-37) |
| 74 | 5 | O | Outline: Adultery → Divorce → ___? → *Oaths and Vows* |
| 75 | 5 | H | Name sections 1–7 of the Sermon in order (*The Beatitudes* … *Oaths and Vows*) |
| 76 | 6 | V | Love Your Enemies ¶2: `{43} 44 45 46 47 48` |
| 77 | 6 | V | Love Your Enemies ¶2: `43 {44} 45 46 47 48` |
| 78 | 6 | V | Love Your Enemies ¶2: `43 44 {45} 46 47 48` |
| 79 | 6 | V | Love Your Enemies ¶2: `43 44 45 {46} 47 48` |
| 80 | 6 | V | Love Your Enemies ¶2: `43 44 45 46 {47} 48` |
| 81 | 6 | V | Love Your Enemies ¶2: `43 44 45 46 47 {48}` |
| 82 | 6 | A | Love Your Enemies ¶2: `43 {44} {45} {46} {47} 48` |
| 83 | 6 | S | Love Your Enemies: `{38-42} 43-48` → recite hidden ¶ 5:38-42 |
| 84 | 6 | S | Love Your Enemies: `38-42 {43-48}` → recite hidden ¶ 5:43-48 |
| 85 | 6 | H | *Love Your Enemies*: give the opening words of each of its 2 ¶ (5:38, 5:43) |
| 86 | 6 | R | Opening words of 5:38, 5:43 → which section? → *Love Your Enemies* |
| 87 | 6 | O | Outline: Divorce → Oaths and Vows → ___? → *Love Your Enemies* |
| 88 | 6 | V | Giving to the Needy: `{1} 2 3 4` |
| 89 | 6 | V | Giving to the Needy: `1 {2} 3 4` |
| 90 | 6 | V | Giving to the Needy: `1 2 {3} 4` |
| 91 | 7 | V | Giving to the Needy: `1 2 3 {4}` |
| 92 | 7 | A | Giving to the Needy: `1 {2} {3} 4` |
| 93 | 7 | R | Text of 6:1-4 → which section? → *Giving to the Needy* |
| 94 | 7 | V | The Lord's Prayer ¶1: `{5} 6 7 8` |
| 95 | 7 | V | The Lord's Prayer ¶1: `5 {6} 7 8` |
| 96 | 7 | V | The Lord's Prayer ¶1: `5 6 {7} 8` |
| 97 | 7 | V | The Lord's Prayer ¶1: `5 6 7 {8}` |
| 98 | 7 | A | The Lord's Prayer ¶1: `5 {6} {7} 8` |
| 99 | 7 | F | Recite *Giving to the Needy* (6:1-4) |
| 100 | 7 | O | Outline: Oaths and Vows → Love Your Enemies → ___? → *Giving to the Needy* |
| 101 | 7 | V | The Lord's Prayer ¶2: `{9} 10 11 12 13` |
| 102 | 7 | V | The Lord's Prayer ¶2: `9 {10} 11 12 13` |
| 103 | 7 | V | The Lord's Prayer ¶2: `9 10 {11} 12 13` |
| 104 | 7 | V | The Lord's Prayer ¶2: `9 10 11 {12} 13` |
| 105 | 7 | V | The Lord's Prayer ¶2: `9 10 11 12 {13}` |
| 106 | 8 | A | The Lord's Prayer ¶2: `9 {10} {11} {12} 13` |
| 107 | 8 | S | The Lord's Prayer: `{5-8} 9-13 14-15` → recite hidden ¶ 6:5-8 |
| 108 | 8 | V | The Lord's Prayer ¶3: `{14} 15` |
| 109 | 8 | V | The Lord's Prayer ¶3: `14 {15}` |
| 110 | 8 | S | The Lord's Prayer: `5-8 {9-13} 14-15` → recite hidden ¶ 6:9-13 |
| 111 | 8 | S | The Lord's Prayer: `5-8 9-13 {14-15}` → recite hidden ¶ 6:14-15 |
| 112 | 8 | H | *The Lord's Prayer*: give the opening words of each of its 3 ¶ (6:5, 6:9, 6:14) |
| 113 | 8 | R | Opening words of 6:5, 6:9, 6:14 → which section? → *The Lord's Prayer* |
| 114 | 8 | O | Outline: Love Your Enemies → Giving to the Needy → ___? → *The Lord's Prayer* |
| 115 | 8 | V | Proper Fasting: `{16} 17 18` |
| 116 | 8 | V | Proper Fasting: `16 {17} 18` |
| 117 | 8 | V | Proper Fasting: `16 17 {18}` |
| 118 | 8 | R | Text of 6:16-18 → which section? → *Proper Fasting* |
| 119 | 8 | V | Treasures in Heaven: `{19} 20 21` |
| 120 | 8 | V | Treasures in Heaven: `19 {20} 21` |
| 121 | 9 | V | Treasures in Heaven: `19 20 {21}` |
| 122 | 9 | R | Text of 6:19-21 → which section? → *Treasures in Heaven* |
| 123 | 9 | F | Recite *Proper Fasting* (6:16-18) |
| 124 | 9 | O | Outline: Giving to the Needy → The Lord's Prayer → ___? → *Proper Fasting* |
| 125 | 9 | V | The Lamp of the Body: `{22} 23 24` |
| 126 | 9 | V | The Lamp of the Body: `22 {23} 24` |
| 127 | 9 | V | The Lamp of the Body: `22 23 {24}` |
| 128 | 9 | R | Text of 6:22-24 → which section? → *The Lamp of the Body* |
| 129 | 9 | F | Recite *Treasures in Heaven* (6:19-21) |
| 130 | 9 | O | Outline: The Lord's Prayer → Proper Fasting → ___? → *Treasures in Heaven* |
| 131 | 9 | V | Do Not Worry ¶1: `{25} 26 27` |
| 132 | 9 | V | Do Not Worry ¶1: `25 {26} 27` |
| 133 | 9 | V | Do Not Worry ¶1: `25 26 {27}` |
| 134 | 9 | F | Recite *The Lamp of the Body* (6:22-24) |
| 135 | 9 | O | Outline: Proper Fasting → Treasures in Heaven → ___? → *The Lamp of the Body* |
| 136 | 10 | V | Do Not Worry ¶2: `{28} 29 30` |
| 137 | 10 | V | Do Not Worry ¶2: `28 {29} 30` |
| 138 | 10 | V | Do Not Worry ¶2: `28 29 {30}` |
| 139 | 10 | S | Do Not Worry: `{25-27} 28-30 31-34` → recite hidden ¶ 6:25-27 |
| 140 | 10 | V | Do Not Worry ¶3: `{31} 32 33 34` |
| 141 | 10 | V | Do Not Worry ¶3: `31 {32} 33 34` |
| 142 | 10 | V | Do Not Worry ¶3: `31 32 {33} 34` |
| 143 | 10 | V | Do Not Worry ¶3: `31 32 33 {34}` |
| 144 | 10 | A | Do Not Worry ¶3: `31 {32} {33} 34` |
| 145 | 10 | S | Do Not Worry: `25-27 {28-30} 31-34` → recite hidden ¶ 6:28-30 |
| 146 | 10 | S | Do Not Worry: `25-27 28-30 {31-34}` → recite hidden ¶ 6:31-34 |
| 147 | 10 | H | *Do Not Worry*: give the opening words of each of its 3 ¶ (6:25, 6:28, 6:31) |
| 148 | 10 | R | Opening words of 6:25, 6:28, 6:31 → which section? → *Do Not Worry* |
| 149 | 10 | O | Outline: Treasures in Heaven → The Lamp of the Body → ___? → *Do Not Worry* |
| 150 | 10 | H | Name sections 8–14 of the Sermon in order (*Love Your Enemies* … *Do Not Worry*) |
| 151 | 11 | V | Judging Others: `{1} 2 3 4 5 6` |
| 152 | 11 | V | Judging Others: `1 {2} 3 4 5 6` |
| 153 | 11 | V | Judging Others: `1 2 {3} 4 5 6` |
| 154 | 11 | V | Judging Others: `1 2 3 {4} 5 6` |
| 155 | 11 | V | Judging Others: `1 2 3 4 {5} 6` |
| 156 | 11 | V | Judging Others: `1 2 3 4 5 {6}` |
| 157 | 11 | A | Judging Others: `1 {2} {3} {4} {5} 6` |
| 158 | 11 | R | Text of 7:1-6 → which section? → *Judging Others* |
| 159 | 11 | V | Ask, Seek, Knock: `{7} 8 9 10 11 12` |
| 160 | 11 | V | Ask, Seek, Knock: `7 {8} 9 10 11 12` |
| 161 | 11 | V | Ask, Seek, Knock: `7 8 {9} 10 11 12` |
| 162 | 11 | V | Ask, Seek, Knock: `7 8 9 {10} 11 12` |
| 163 | 11 | V | Ask, Seek, Knock: `7 8 9 10 {11} 12` |
| 164 | 11 | V | Ask, Seek, Knock: `7 8 9 10 11 {12}` |
| 165 | 11 | A | Ask, Seek, Knock: `7 {8} {9} {10} {11} 12` |
| 166 | 12 | R | Text of 7:7-12 → which section? → *Ask, Seek, Knock* |
| 167 | 12 | F | Recite *Judging Others* (7:1-6) |
| 168 | 12 | O | Outline: The Lamp of the Body → Do Not Worry → ___? → *Judging Others* |
| 169 | 12 | V | The Narrow Gate: `{13} 14` |
| 170 | 12 | V | The Narrow Gate: `13 {14}` |
| 171 | 12 | R | Text of 7:13-14 → which section? → *The Narrow Gate* |
| 172 | 12 | F | Recite *Ask, Seek, Knock* (7:7-12) |
| 173 | 12 | O | Outline: Do Not Worry → Judging Others → ___? → *Ask, Seek, Knock* |
| 174 | 12 | V | A Tree and Its Fruit ¶1: `{15} 16 17 18 19 20` |
| 175 | 12 | V | A Tree and Its Fruit ¶1: `15 {16} 17 18 19 20` |
| 176 | 12 | V | A Tree and Its Fruit ¶1: `15 16 {17} 18 19 20` |
| 177 | 12 | V | A Tree and Its Fruit ¶1: `15 16 17 {18} 19 20` |
| 178 | 12 | V | A Tree and Its Fruit ¶1: `15 16 17 18 {19} 20` |
| 179 | 12 | V | A Tree and Its Fruit ¶1: `15 16 17 18 19 {20}` |
| 180 | 12 | A | A Tree and Its Fruit ¶1: `15 {16} {17} {18} {19} 20` |
| 181 | 13 | F | Recite *The Narrow Gate* (7:13-14) |
| 182 | 13 | O | Outline: Judging Others → Ask, Seek, Knock → ___? → *The Narrow Gate* |
| 183 | 13 | V | A Tree and Its Fruit ¶2: `{21} 22 23` |
| 184 | 13 | V | A Tree and Its Fruit ¶2: `21 {22} 23` |
| 185 | 13 | V | A Tree and Its Fruit ¶2: `21 22 {23}` |
| 186 | 13 | S | A Tree and Its Fruit: `{15-20} 21-23` → recite hidden ¶ 7:15-20 |
| 187 | 13 | S | A Tree and Its Fruit: `15-20 {21-23}` → recite hidden ¶ 7:21-23 |
| 188 | 13 | H | *A Tree and Its Fruit*: give the opening words of each of its 2 ¶ (7:15, 7:21) |
| 189 | 13 | R | Opening words of 7:15, 7:21 → which section? → *A Tree and Its Fruit* |
| 190 | 13 | O | Outline: Ask, Seek, Knock → The Narrow Gate → ___? → *A Tree and Its Fruit* |
| 191 | 13 | V | The House on the Rock: `{24} 25 26 27` |
| 192 | 13 | V | The House on the Rock: `24 {25} 26 27` |
| 193 | 13 | V | The House on the Rock: `24 25 {26} 27` |
| 194 | 13 | V | The House on the Rock: `24 25 26 {27}` |
| 195 | 13 | A | The House on the Rock: `24 {25} {26} 27` |
| 196 | 14 | R | Text of 7:24-27 → which section? → *The House on the Rock* |
| 197 | 14 | V | The Authority of Jesus: `{28} 29` |
| 198 | 14 | V | The Authority of Jesus: `28 {29}` |
| 199 | 14 | R | Text of 7:28-29 → which section? → *The Authority of Jesus* |
| 200 | 14 | F | Recite *The House on the Rock* (7:24-27) |
| 201 | 14 | O | Outline: The Narrow Gate → A Tree and Its Fruit → ___? → *The House on the Rock* |
| 202 | 14 | F | Recite *The Authority of Jesus* (7:28-29) |
| 203 | 14 | O | Outline: A Tree and Its Fruit → The House on the Rock → ___? → *The Authority of Jesus* |
| 204 | 14 | H | Name sections 15–20 of the Sermon in order (*Judging Others* … *The Authority of Jesus*) |
