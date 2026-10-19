**➕ Claude:** Text marked ➕ was added by Claude on 2026-10-14. Thomas's original lines are unchanged, typos included. Claude's text runs from a ➕ line to the next heading without ➕.
- **Decided** means one of Thomas's decisions (1–12), one of Claude's research resolutions (R1–R16, which stand unless Thomas overrides them), or a verified fact. **Proposed** means Claude's extrapolation, for Thomas to confirm.
- **Sources.** The `research/` folder next to this file holds the research with its sources and confidence levels: `stt.md`, `stack.md`, `policy.md`, `content.md`, `product.md` and `backend.md`, all snapshots dated 2026-10-14. Citations such as "(research: policy.md)" point there.
- **Decisions.** The durable record is the "Decisions so far" table below and, from Phase 0 on, `docs/decisions.md`. Open questions are settled at the build gates listed under "Open decisions for Thomas".

# Conceptual Requirements

Free Bible memory app attempting to help untalented, non-tech savvy people memorize large portions of the Bible, such as the Sermon on the Mount.

It combines a speech-to-text (STT) recitation feedback concept with a unique outline-based flashcard system developed by iteration with custom Anki flashcard decks.

Other features of the app defined below support and motivate this journey. In short, I want to create an app I would want to use. And I want the least talented person in my church to be successful with it.

It uses open-source Bible text and study material at this time with limited support for other Bible translations as defined below.

**➕ Claude:**

## ➕ Product summary

**Seedling** is a free iPhone app (Android later) for memorizing whole passages of the Bible, such as the Sermon on the Mount, not just single verses. It teaches a passage's outline first, then the words in small steps that each remove a few cues. Then the user says the passage aloud while the phone listens on the device and grades the attempt. It is built for the least confident, least tech-savvy member of a congregation: large text, one obvious next step, a growing plant instead of points, and no streak guilt. Churches can form groups that grow a shared "tree of the whole Bible."

Voice scoring and "free" don't set Seedling apart on their own: Bread, ReciteWell, Recite, Versify and Remember Me already offer one or both. None of the roughly 10 apps surveyed teaches the outline first or is built for long passages (research: product.md). Seedling's edge is:
1. the outline-first method tested in trials 1 and 2 (`notes/sequence_v2_draft.md`, called "sequence v2" below);
2. gentle design for older and non-tech users;
3. church groups;
4. the public-domain BSB, with no ads and no tracking.

## ➕ Decisions so far

**Read R1 first: it corrects decision 3.**

| # | Decision | Source |
|---|---|---|
| 1 | Spec: edit this doc in place, keep Thomas's text verbatim, mark Claude's additions; long material goes in sibling files | Thomas |
| 2 | Donations go to a church / existing 501(c)(3) | Thomas |
| 3 | Developer accounts: Thomas's Individual accounts now, the church's Organization accounts later (**amended by R1**) | Thomas |
| 4 | Release path: personal dev build on Thomas's iPhone → church beta (TestFlight / Play closed testing) → public launch | Thomas |
| 5 | Speech-to-text: native on-device recognizers first, behind a swappable interface; open-source engine later | Thomas |
| 6 | Monorepo in bible-flashcards; the Python generator is the reference implementation and content pipeline | Thomas |
| 7 | Port the sequence-v2 ladder (each card its own FSRS item) behind a pluggable scheduler; the per-unit model is later R&D | Thomas |
| 8 | Devices: iPhone only, plus Mac simulators | Thomas |
| 9 | Accounts 13+ in v1; raw audio never leaves the device; kids mode later | Thomas |
| 10 | Backend: Cloud Run (TypeScript API) + Cloud SQL Postgres + Firebase Auth, managed with Terraform | Thomas |
| 11 | Pace: 5–10 hours a week | Thomas |
| 12 | Design: Claude designs in code (Expo + simulator screenshot loop); Figma optional | Thomas |
| R1 | **Correction to decision 3.** The church's Apple Organization team owns the production app from the *first TestFlight upload*, not from public launch. Thomas's Individual account builds only a separate dev bundle ID. Church paperwork starts now. Why: Technical Specifications → Apple Developer Setup | Claude (research: policy.md) |
| R2 | A "Give" button opens the church's giving page in Safari. It unlocks nothing and isn't pay-what-you-want. Stripe and the Chase account are dropped | Claude |
| R3 | Local-first: the app works fully with no account and makes no network calls until the user opts in. Accounts (Sign in with Apple + Google) add backup, more devices and groups. Neutral age screen; in-app deletion | Claude |
| R4 | Client: Expo SDK 57, then 58 before the beta; Uniwind + HeroUI Native in place of Bootstrap; Skia for the plant; ts-fsrs | Claude |
| R5 | Backend: Hono on Cloud Run, Postgres 18 db-f1-micro, Identity Platform, append-only sync log; about $10/month in prod, $0 in the personal phase | Claude |
| R6 | STT: expo-speech-recognition with a mandatory on-device check (voice off if it fails); SpeechAnalyzer in v1.5; sherpa-onnx later; tested on the iPhone | Claude |
| R7 | Grading: every recall step is graded automatically from voice, typed first letters or a self-check; one tap confirms or overrides | Claude |
| R8 | Engine: TS port of sequence v2 (compile, calendar release, FSRS, session, grade, mastery); Python emits golden JSON for parity tests | Claude |
| R9 | Content: the full BSB is bundled; 10-passage starter shelf; other translations and commentaries on demand; pasted text stays on the device | Claude |
| R10 | Names: "Seedling"; "Passages" and "Shelf" replace "journeys"; plain step names; never "card", "deck" or "FSRS" in the UI | Claude (Thomas decides) |
| R11 | Progress plant: one personal plant; passages are limbs shaped by their outlines; verses are leaves; "thirsty", never dead; a group tree with birds | Claude |
| R12 | Motivation: weekly rhythm with rest days and repair; no leaderboards; capped catch-up; one opt-in reminder | Claude |
| R13 | Accessibility: Dynamic Type 200%+, verse text ≥ 20 pt, 7:1 contrast, 56 pt buttons, colorblind-safe colors plus shapes, silence timeouts ≥ 6 s | Claude |
| R14 | Launch compliance: US-only, policy pages on the church site, honest age rating, a privacy label with no audio | Claude |
| R15 | User content in v1: group name plus leader-authored passage titles and outline headings only; no chat; report and block | Claude |
| R16 | Repo: `apps/mobile`, `apps/api`, `packages/{engine,recite,plant,shared}`, `infra/`; existing Python stays where it is | Claude |

## ➕ Open decisions for Thomas

Each open question is settled at a gate in Build Phases (a gate is a decision Thomas records before the steps that depend on it). This index is the single list; the sections below only point to it.

| Gate | When | What Thomas decides |
|---|---|---|
| 0.1 | Phase 0 | App name: confirm "Seedling" after the store and trademark checks (App Name Ideas) |
| 0.6 | Phase 0 | Public or private repo; confirm there's no web version |
| 0.9 | Phase 0, church meeting | Publish under the church's name; Apple and Google Account Holder; legal name and EIN; giving URL; long-term GCP billing owner |
| 2.1 | Phase 2 | "Passages" or another word; a custom-branded or platform-native look; import trial 2's Anki history |
| 3.1 | Phase 3 | Voice grading: may voice give Again without asking? Do "close" words count as correct? Show tentative words live? |
| 4.2 | Phase 4 | Plant art direction; stage thresholds (50 / 300 / 1,000 rooted verses) |
| 4.7 | Phase 4 | Leaf clusters by chapter for very large passages |
| 5.1 | Phase 5, with the church | Ten Commandments numbering; Farewell Discourse boundary; Teachings of Jesus scope; the lead commentary |
| 5.2 | Phase 5 | Default pace and rhythm; Psalm 23 as everyone's first passage; placing a known passage as rooted; the first-run flow; "Learn the outline only" in the beta; KJV and WEB timing; study-help downloads before sign-in; AI questions |
| 6.1 | Phase 6 | Email-link sign-in; GCP billing; a hosted dev backend; syncing trails; pasted-text backup; Texas testers |
| 7.1 | Phase 7, pastor and elders | Named sharing in groups; blossom threshold; default rest day; who handles reports; the domain for join links |
| 8.1 | Phase 8a | Give in the beta; tester list; a warm API instance |
| 8.15 | Phase 8b | When to start Android; the Android voice floor (on-device on Android 13+ only, or sherpa-onnx early) |
| 9.7 | Phase 9 | The per-unit memory model; whether a section's recite step becomes a verse's governing step |
| 10.1 | Phase 10 | Crash reporting; Give, Android and pasted text at launch |

The go/no-go gates are 5.19 (open the beta) and 9.16 (launch).

## App Name Ideas

- \*Seedling
- Planted
- Grow
- Seed
- Seeded
- Word
- Wordseed
- Seedgrow
- Vine
- Tree
- Branch
- Root
- Rooted

**➕ Claude:** **Proposed: Seedling.** Thomas starred it, and it works on several levels:
- It is the progress tracker: your plant starts as a seed and grows.
- It echoes Jesus' seed parables (the sower, Matt 13:3–23; the mustard seed, Matt 13:31–32), which also supply the group tree's birds.
- It sounds gentle. "Everyone starts as a seedling" is the message for the least confident user.
- It is short, easy to say and spell, and makes a clear icon.

The rest are weaker product names. "Word", "Tree", "Vine", "Root" and "Branch" are too generic to find in store search or to protect. "Rooted" is the strongest runner-up, but the vocabulary below uses it for a mastered verse, and Christian brands probably already use it (unverified).

**What Thomas checks before committing** (about an hour; gate 0.1):
1. **App Store and Google Play**: search the name and note look-alikes. Creating an app record reserves the name, so per R1 create that record in the church's team, not Thomas's. A subtitle such as "Bible Memory" can carry the description.
2. **USPTO trademark search** (the US Patent and Trademark Office's free search tool): look for live marks on "Seedling" for software and education, likely Nice classes 9 and 41 (a class is a category of goods or services). A trademark conflict is the real blocker; a store look-alike is only a nuisance.
3. **Domain**: the policy and support pages live on the church site (R14). Group join links need a site that can host Apple's link file (User Groups → Joining). The church site may do; otherwise a cheap descriptive domain such as `seedlingbible.org`. Decided at gate 7.1.

**Vocabulary** (Proposed). Metaphor for feedback, plain words for navigation.

| Word in the UI | Means | Replaces |
|---|---|---|
| **Passage** | A stretch of Scripture you're learning, curated or your own | journey, deck |
| **Shelf** | A series of passages (Teachings of Jesus, Psalms of Trust) | collection |
| **Step** | One prompt in a session, named plainly ("Fill in the blanks") | card |
| **Today** | The day's session, with its time estimate | study queue |
| Seed → seedling → sapling → young tree → tree | Your plant's overall stage, set by total rooted verses | level, XP |
| Bud → leaf → full leaf → **rooted** | One verse's strength; rooted = you'll likely still know it in 3 weeks | mastered, mature |
| Blossom, fruit | A section mastered; a whole passage rooted | badge |
| **Thirsty** / water | A verse due for review / reviewing it | overdue, due |

**Replacing "journies"** (gate 2.1): **Passages** (recommended: plain, and what a pastor already says: "Which passage are you learning?"), Plantings (on theme, but a new user has to learn it), Paths or Gardens.

# Features

**➕ Claude:**

## ➕ How the features fit together

**The daily loop** (Proposed). Martha, 72, opens Seedling. The Today tab shows her plant and one large button: **"Today · about 15 minutes."** She taps it. Thirsty leaves come first, then new steps for her current passage. Each step has a plain banner ("See the outline", "Fill in the blanks", "Say it from memory") and a map strip showing where she is in the passage. On recall steps she taps the microphone and recites. Her words appear behind a marker as she speaks, marked by how well they match. If voice isn't working (a noisy room, the microphone declined), she types first letters or checks herself. The app grades each step ("Well done. See you again in 3 days.") and moves on; she can tap "Grade it differently" if it got her wrong. When she taps "Stop for today" or the session ends, her plant animates: new buds, a leaf that perks up, maybe a blossom. A quiet line reads "4 of 5 days this week." Study helps are one tap away on any step. Groups and the Give button live outside the session.

How each feature serves that loop:
- The **learning algorithm** decides what's in Today and in what order (the sequence v2 ladder plus FSRS).
- **Recital matching** is how most recall steps are answered and graded.
- The **progress tracker** turns the scheduler's numbers into something a non-technical person can read at a glance.
- **Core passages and intro articles** remove a beginner's two hardest choices: what to learn, and why bother.
- **Custom passages, groups and study helps** extend the loop for people who outgrow the starter shelf.

**Time per day.** The button's estimate is due steps × average time per step. At the trial pace of 12 new steps a day, trial 2's FSRS simulation estimates 24 min/day on average while new text arrives (peak 35), then 11 min/day through day 90 and 6 after (`notes/sequence_v2_draft.md` §11). That's too much for many beginners, so the default pace is Gentle (Robust Learning Algorithm).

**Scope by release stage** (Proposed). Each feature is listed at the stage where people first get it. Build Phases is authoritative for timing: the personal alpha is Phases 1–4, the church beta Phases 5–8, public launch Phases 9–10, and Later is Phase 11.

| Feature | Personal alpha | Church beta | Public launch | Later |
|---|---|---|---|---|
| Learning engine | Sequence v2 port, FSRS-6 defaults, auto-grading | Pace picker with time estimates; thresholds checked against Thomas's logs | Thresholds and FSRS parameters tuned on beta data | Per-unit memory model |
| Passages | Ps 23, Sermon on the Mount, Isaiah 40–44 | 10-passage starter shelf | Next shelf, Psalms packs, Teachings of Jesus | More shelves |
| Recital matching | On-device voice, live trail, Recite freely, trail history | | SpeechAnalyzer engine (iOS 26+) | Open-source engine, Android ≤ 12 |
| Type and self-check | Yes | | | |
| Progress plant | Plant, growth animation, thirsty leaves | | Home-screen widget | Art packs |
| Custom passages | Thomas edits YAML | Picker, collections, outline editor | Other public-domain translations, pasted text | Half-verse parts |
| Intro articles | | The 5 behind in-context "Why?" links | All 11 | |
| Study helps | | Commentary + cross-references (online, cached) | Pre-cached per passage | People and places; AI questions? |
| Accounts and sync | None (local only) | Apple + Google sign-in, backup, a second device | | |
| Groups | | Join by code or QR, group tree, leader passages, report and block | | Kids or family mode |
| Rhythm and reminders | One opt-in daily reminder; "days this week"; capped catch-up | Weekly goal, rest days, repair, reminder downgrade | | |
| Help and accessibility | | First-run flow, step help, "Hear it", "Help someone set up" | | |
| Give | | Link to the church's page (gate 8.1) | Same | In-app Apple Pay |
| Android | | Play closed test once the church's Play account exists | Yes (gate 10.1) | |

## Progress Tracker

- Sapling growing out of the soil that gradually grows shoots and leaves as user masters material
- Governed by some algorithm in the background that dictates the pseudo-random character of the plant and how it develops given a magnitutde of content the user has mastered

**➕ Claude:** This section makes R11 concrete. Everything here is **Proposed** unless it cites research.

### ➕ One plant, shaped by what you learn

- **One personal plant.** A seed is planted when you start your first passage. Its overall stage comes from total rooted verses: seedling 1–49, sapling 50–299, young tree 300–999, tree 1,000+. The thresholds are a first guess sized to the content: one long passage (Sermon on the Mount, 107 verses) makes a sapling, the starter shelf (~620 verses) a young tree, and Teachings of Jesus (~1,955 verses) a tree.
- **Each passage is a limb** whose branching follows its outline: sections are branches, sub-sections sub-branches, units twigs, and verses leaves. The plant literally has the shape of what you know, which reinforces the outline-first method.
- **Structure only grows.** Branches and leaves never shrink, fall or die. Only vitality (below) changes.

**Growth mapping** (formula details in research: product.md)

| What you've done | What appears | Signal |
|---|---|---|
| Start a passage | A new limb buds from the trunk | Enrollment |
| "See the outline" for a section | Its branch grows to 35% of full length | Preview done |
| Outline steps strengthen | The branch grows to full length | Stability (days until recall odds fall to 90%) of "Fill in the heading" / "Name the parts" |
| First step on a verse | Bud | Any step covering it introduced |
| "Say it from memory" graduates | Small leaf | Governing step (below) graduated |
| Stability ≥ 7 days | Full leaf | |
| Stability ≥ 21 days | **Rooted** leaf (deeper color, small root mark) | Anki's "mature" threshold |
| A section's recite step ≥ 21 days | Blossom on that branch | |
| Whole passage rooted | Fruit at the limb's crown | |

**Governing step.** A leaf's state comes from one step only: its unit's "Say it from memory" (Header → text). A verse appears on six or more steps, and averaging them would make leaves flicker as scaffold steps come due (research: product.md).

**Thirsty, never dying.** For each leaf the app computes retrievability R, the FSRS estimate of the chance you'd recall it right now. When R < 0.9 the leaf droops gently, up to 30°, and loses up to 35% of its color saturation, and no further: no browning, no falling. A review "waters" it with a brief rain sparkle (a crossfade under Reduce Motion). Copy stays neutral: "6 leaves are thirsty: water them (about 4 min)." Never red numbers, never "overdue." Punishment mechanics backfired for every participant in a 45-person Habitica field study, while Finch-style growth without punishment works (research: product.md). The droop is tested with older church members at build step 5.17; if it feels shaming, it falls back to a color shift only.

**Deterministic character.** The plant is a pure function, `growPlant(PlantInput)` in `packages/plant` (App Architecture §6 has the contract). The same inputs always give the same plant. A 128-bit seed, created with the first passage and synced, gives each outline node its own random stream (a seeded PRNG, pseudo-random number generator), so editing one section reshapes only that branch. Seeded traits are branch angle, curve, leaf shape and blossom palette. A stored `renderVersion` means a later algorithm change never silently reshapes a user's tree.

**Rendering.** Skia (a 2D graphics engine) draws tapered branches whose growth animates, and all leaves in one batch. The Sermon on the Mount has about 107 leaves; all 150 Psalms would have 2,461, so very large passages may need chapter-level leaf clusters (gate 4.7).

**Art direction** (gate 4.2): leaf species per passage or genre (olive, fig, vine for John 15 and the Psalms, mustard), the palette, and the setting (soil and sky, or a pot on a sill). Default proposal: procedural branches plus a small set of drawn leaf and blossom sprites that Thomas approves.

**Accessibility label.** VoiceOver reads a summary instead of the drawing: "Your plant: seedling. Sermon on the Mount: 4 of 5 branches grown, 42 of 107 verses rooted, 6 leaves thirsty."

**Widget** (Public launch). An iOS home-screen widget shows a PNG snapshot of the plant plus one line ("6 thirsty · about 4 min"). Skia can't run inside a widget (expo-widgets is SwiftUI-only), so the app renders the image after each session and the widget displays it (research: stack.md, product.md).

**Group tree.** The same engine draws a church's shared tree of the whole Bible: 10 genre limbs → 66 books → 1,189 chapters, with members as birds (Matt 13:31–32), never a ranking. Details under User Groups.

### ➕ What the user sees over time

Illustrative, at the Steady pace (12 new steps a day), starting with Psalm 23 and then the Sermon on the Mount.

| When | Plant |
|---|---|
| Day 1 | A sprout breaks the soil. After "Read it aloud" and "See the outline," one small limb (Psalm 23) shows two branch stubs, "He Leads Me" and "You Are With Me," and a few buds. |
| Day 30 | A seedling. Psalm 23's leaves are full and the first may be rooted. The Sermon's limb has all 5 branches grown (outline learned in its first week), most of its ~107 verses budded or in small leaf, the Beatitudes in full leaf. A few leaves droop after a busy weekend and perk up in one session. |
| Day 365 | A young tree with several limbs (most of the starter shelf, ~600 verses), fruit on the finished passages, blossoms on the Beatitudes and the Lord's Prayer section. After a holiday week, a capped 10-minute catch-up waters the thirstiest leaves first. In the church's group tree, birds sit in Matthew and the Psalms. |

**Open questions:** gate 4.2 (art, stage thresholds) and gate 5.2 (placing an already-known passage, such as Psalm 23, as rooted after one good recitation).

## Core Journies and Intro Material

### Core Journies

Pre-defined sections of material the user can choose to begin learning right away. Not too jazzed about the term "journies" though.

- Sermon on the Mount
- Farewell Discourse
- All teachings of Jesus packaged somehow
- Ten commandments
- Book of Psalms

**➕ Claude:** **The starter shelf** (R9), ordered easy to hard. Sizes come from running the repo's sequence-v2 generator on draft outlines (research: content.md). "Steps" are cards. "Days" means days until every step has been introduced at 12 new steps a day; reviews continue after that. "~" marks estimates for collections the generator can't build yet.

| # | Passage | Reference | Verses | Steps | Days | Default outline |
|---|---|---|---:|---:|---:|---|
| 1 | Psalm 23 "First Steps" | Ps 23 | 6 | 23 | 2 | Hand: 2 stanzas |
| 2 | The Ten Commandments | Exod 20:1–17 | 17 | 81 | 7 | Hand: two tables |
| 3 | Lost and Found | Luke 15 | 32 | 94 | 8 | BSB headings (3) |
| 4 | "I Am" sayings | John 6:35; 8:12; 8:58; 10:9; 10:11; 11:25–26; 14:6; 15:5 | 9 | ~30 | ~3 | One part per saying |
| 5 | Psalms of Trust | Ps 1, 16, 23, 27, 46, 91, 121 | 72 | ~180 | ~15 | Hand stanza outlines |
| 6 | Parables of the Kingdom | Matt 13:1–52 | 52 | 168 | 14 | BSB headings (10) |
| 7 | Songs of Ascents | Ps 120–134 | 101 | 256 | 22 | Five triads of psalms |
| 8 | Olivet Discourse | Matt 24–25 | 97 | 276 | 23 | BSB headings (9) |
| 9 | Sermon on the Mount | Matt 5:3–7:27 | 107 | 356 | 30 | Trial 1 outline (BSB has 19 headings) |
| 10 | Farewell Discourse | John 13:31–17:26 | 125 | 376 | 32 | BSB book outline + headings |

**Next shelf**: Romans 8 (121 steps, 11 days), Isaiah 52:13–53:12, Psalm 139 (60 steps, 5 days), Isaiah 40–44 (436 steps, 37 days; Thomas's trial 2), Psalm 119 (~500 steps, ~42 days).

**"All teachings of Jesus" is a shelf, not a passage.** Jesus' words in the Gospels cover about 1,955 verses (42,600 BSB words, about 18 Sermons on the Mount, roughly 15 months at 12 steps a day). BSB has no red-letter flags, so they come from the public-domain WEB (ENGWEBP) as a table of verse references. Suggested order: Sermon on the Mount → Lost and Found → Parables of the Kingdom → Parables of Grace (Luke 10:25–37, 18:9–14; Matt 18:21–35, 20:1–16; 82 verses, ~250 steps) → "I Am" sayings → Good Shepherd (John 10:1–18) and Bread of Life (John 6:22–58) → Olivet → Farewell. The shelf shows progress against the whole: "312 of 1,955 verses of Jesus' words rooted."

**Psalms ship as themed packs, not all 150** (2,461 verses, about 550 days). About 10 packs, e.g. Trust (above), Praise (Ps 8, 19, 100, 103, 145, 150: 77 verses, ~190 steps, ~16 days) and Repentance (Ps 32, 51, 130, 139: 62 verses, ~150 steps, ~13 days), plus the Songs of Ascents as five triads. Every psalm needs a hand-written stanza outline, because BSB's paragraph breaks don't follow the stanzas (Psalm 46 breaks at verses 10 and 11, not at the Selahs). Psalm 119 needs its 22 Hebrew-letter titles (Aleph to Tav) written in.

**The Farewell Discourse comes whole or in three parts**, each its own passage, taken alone or in order: 13:31–14:31 "Where I Am Going, You Cannot Come" (39 verses), 15:1–16:33 "Instructions for the Disciples" (60 verses) and 17:1–26 "Jesus' Prayer" (26 verses, ~80 steps, ~7 days). On the plant the parts grow the branches of one Farewell limb.

**Overlapping passages never teach a step twice** (a requirement on the card keys; mechanism in App Architecture §4). The whole Farewell Discourse and its parts, and Psalms of Trust and Psalm 23, must compile to the same steps for the text they share. So a step's key is tied to the shared text and outline headings, not to the passage it was enrolled through. The release planner skips steps already introduced in another enrollment. Custom and group passages that overlap a curated one don't share steps; a verse in two passages shows its higher stability. Test: enrolling in Farewell part 1 and then the whole adds no duplicate step for the shared text, and Psalms of Trust re-introduces no Psalm 23 step.

**The Ten Commandments** use a hand outline, because BSB gives Exod 20 a single heading. It is shown without numbers, so it doesn't pick a numbering tradition:
- The LORD Who Rescued You (20:1–2)
- Love the LORD (20:3–11): No Other Gods (3) · No Idols (4–6) · Honor His Name (7) · Keep the Sabbath (8–11)
- Love Your Neighbor (20:12–17): Honor Your Parents (12) · Life, Marriage, Property, Truth (13–16) · Do Not Covet (17)

Traditions number them differently (Jewish, Catholic/Lutheran, Reformed/Orthodox), so the church can add its numbering as a setting (gate 5.1). Deuteronomy 5:6–21 is offered as a variant. Short passages like this one are outline-heavy: 20 of its 81 steps are outline steps.

**How curated passages are authored** (Proposed pipeline)
1. Claude drafts each passage as a YAML outline in `data/passages/`. It starts from the BSB section headings inside the range (the default outline) and BSB's book outlines (`data/outlines/outlines.yml`, which covers only Genesis, Isaiah, John, Acts, Romans and Revelation).
2. Hand outlines replace BSB headings where they fail: single headings (Ten Commandments), psalm stanzas, Psalm 119 and collections ("I Am" sayings). Code handles the builder quirks: merge back-to-back heading blocks (Heb 11:30), and rename a heading that repeats its parent, keeping the original as `bsb_heading` (as trial 2 did).
3. The Python content exporter (`src/content/`) validates the outline against the text, including the 19 verses BSB omits (e.g. Matt 18:11). It writes the passage bundle plus golden JSON for the TypeScript parity tests.
4. Thomas reviews and approves every hand outline before it ships.
5. A corrected heading resets only the steps that ask about that heading, never verse progress (App Architecture §4, Versioning).

**Open questions:** gate 5.1 (Ten Commandments numbering; Farewell boundary at 13:31 or 14:1; red-letter verses in Acts and Revelation, 31 + 69; de-duplicating Gospel parallels) and gate 5.2 (Psalm 23 first for everyone).

### Into Material

Simple, potent, and quickly digestible articles to orient and introduce the user to the circumstance.

- Why the BSB?
- Why open-source?
- Why memorize?
- Why the Bible?
- Why you?
- Why this app?

**➕ Claude:** **Format** (Proposed). Each article is 150–250 words (about a minute aloud) in plain language. It quotes one Scripture passage from the bundled BSB, so the quote is always exact, and describes 2–3 findings in plain words ("A 1969 study found…"), with full references in a "Sources" fold at the bottom. Articles are bundled with the app, work offline, and are versioned with the content. Each has a "Hear it" button (Beautiful UI). Claude drafts them; Thomas and a pastor review the voice and theology.

| Article | One-line thesis | Evidence (research: product.md, content.md) | Scripture |
|---|---|---|---|
| Why the BSB? | A modern, readable translation in the public domain since 2023-04-30, so the whole Bible can live in the app, offline and free, with no license needed. | BSB terms and licensing pages (content.md) | Prov 30:5 |
| Why open-source? | Free text and open tools mean no company can lock it, charge for it or take it away, and anyone can check the method. | BSB public domain; ts-fsrs and the Bible API are MIT-licensed | Matt 10:8 |
| **Why memorize?** | What you carry by heart is with you when the book isn't: in temptation, in counsel, at a bedside. | Jesus answering temptation from Deuteronomy | Ps 119:11; Matt 4:4 |
| Why the Bible? | It's God's word, the one text worth carrying everywhere. | | 2 Tim 3:16–17; Isa 40:8 |
| Why you? | You don't need a good memory, just a good method and a little time. | Adults 55–65 benefit from self-testing as much as students (Meyer & Logan 2013); adults 67–88 still benefit from saying words aloud (Lin & MacLeod 2012) | Col 3:16 |
| Why this app? | It teaches the shape before the words, listens and grades so you don't have to judge yourself, and never shames you. | Bower 1969; Karpicke & Roediger 2008; Silverman & Barasch 2023 (repairable streaks) | Ps 1:2–3 |
| **Why the outline first?** | Knowing the structure gives each verse a place to hang, so long passages become possible. | Hierarchy recalled 2–3× better than jumbled lists (Bower 1969); context before text raises recall (Bransford & Johnson 1972); actors learn lines through meaning (Noice & Noice 2006) | Neh 8:8 |
| **Why say it aloud?** | Saying words aloud fixes them better than reading silently, at any age. | Production effect (MacLeod 2010); lasting, works for text (Ozubko 2012); helps older adults (Lin & MacLeod 2012) | Josh 1:8; Deut 6:6–7 |
| **Why does the app grade for me?** | People judge their own recall poorly, so checking against the text is more accurate, and you can always override. | Predictions uncorrelated with recall (Karpicke & Roediger 2008); stability bias (Kornell & Bjork 2009); scoring against the answer improves accuracy (Dunlosky & Rawson 2012) | Ps 139:23–24 |
| **Why is it free, and where does a gift go?** | Public-domain text and a small cloud bill (about $10 a month) keep it free; a gift goes to the church for the Great Commission and unlocks nothing. | backend.md (cost), policy.md (donations) | Matt 28:19–20; 2 Cor 9:7 |
| Why a little each day? (optional) | Short spaced sessions beat cramming, and testing beats rereading. | Roediger & Karpicke 2006; Cepeda 2006, 2008; Dunlosky 2013 | Deut 6:7 |

The five **bold** articles ship in the church beta; the rest by public launch.

**Where they appear**
- **Not in the first run.** A new user goes straight to a first success (Beautiful UI → First run); reading comes later.
- **In context**: a small "Why?" link the first time a feature appears. The first "See the outline" step links to Why the outline first?, the first microphone prompt to Why say it aloud?, the first automatic grade to Why does the app grade for me?, the first session end to Why memorize?, and the Give screen to Why is it free?
- **Library**: all articles under More → Learn, next to the credits page.

## Custom Journies, Outlines, and Verse Text

- User can build their own custom journey:
- Collection of disparate verses, portions of books, collections of books, etc.
- Input their own outline to use instead of the default
- Depending on legality, user can paste in their own Bible text by verse

**➕ Claude:** All **Proposed** unless noted.

### ➕ Passage picker

- **Two ways in.** (1) Tap a book, then a chapter grid, then the first and last verse (large number grids, not small scroll wheels). (2) Type a reference ("Matt 18:1-11", "John 3:16–21"); the parser accepts common abbreviations, hyphens and en dashes.
- **Ranges** may cross chapters (Matt 5:3–7:27). The 19 verses BSB omits (e.g. Matt 18:11) are allowed inside a range and shown as a gap with a short note; today's generator crashes on them and must be fixed (R8).
- **Collections.** Add several ranges, even across books, to make one passage ("I Am" sayings, a funeral set). The engine needs a "collection" root whose children are independent passages, another generator gap (research: content.md).
- **Size preview before starting**, computed on the device: "107 verses · about 356 steps · about 60 days at Gentle pace." Above about 150 verses, the app suggests splitting into parts, as the Farewell Discourse does.

### ➕ The default outline

- Built from the BSB section headings inside the range (from `Chapter.json`), with BSB's book outlines above them where they exist. Those cover only 6 books, so most custom passages get headings only.
- A range that starts mid-section uses that section's heading. Back-to-back headings are merged, and a child heading that repeats its parent is renamed from its text (trial 2's rules).
- **No headings at all** (a single psalm, a short epistle passage): the passage is split into parts of about 80 words at paragraph breaks, each labeled by its first words ("Blessed is the man…"), so the outline steps still work. The user can rename them.
- This follows Thomas's principle in `notes/concept.md`: start from the publisher's outline, and change it once you understand the passage better.

### ➕ Outline editor (Church beta)

- **Tree view**: each heading is a row with its verse range. Actions are buttons, never drag- or swipe-only: rename, split here (pick a verse), merge with next, indent or outdent (make a sub-section), move a boundary.
- **Paste an outline**: a text box that accepts indented lines with references, e.g. `The Beatitudes 5:3-16` with `Triad 1 5:3-5` indented beneath it. Problems are reported in plain words: the parts must cover the passage in order, with no gaps or overlaps (the generator's rule).
- **Editing a passage in progress**: unchanged parts keep their progress (App Architecture §4). The app warns first: "Changed sections restart their outline steps. Your verse progress stays."

### ➕ Half-verse parts (Later)

`notes/concept.md` proposes references like Matt 4:12a. This matters for poetry, where a stanza or parallel line can begin mid-verse. Proposal: a boundary may fall at a poetry line break (from `Chapter.json`) or a word index, written `12a`/`12b`. Mastery stays per verse: a split verse is rooted only when both its parts are.

### ➕ Other translations and your own text

- **Other public-domain translations** (Public launch) download on demand from the helloao API: KJV, WEB, ASV, YLT and others among its 34 English public-domain texts. The KJV matters most, because many older church members learned verses in it. Seedling avoids the 7 non-commercial or no-derivatives texts (e.g. NET): blanking words can count as a derivative, and a donation link muddies "non-commercial." Edited text may not be called BSB or WEB (research: content.md).
- **Pasted text** (Public launch; **Decided** posture from R9): a per-verse "my own text" field labeled for personal use. It's stored on the device only and excluded from Seedling's sync, account backup and groups; the user's own iCloud device backup and a "Move my progress" export file they choose to make can still carry it. There are no named presets or one-tap imports for NIV, ESV and so on. Outlines and references still come from the app, so the plant and map work as usual. The risk is fairly low only while the text stays on the device. If a server ever holds copies, the church needs a DMCA agent (the contact registered with the US Copyright Office under the Digital Millennium Copyright Act) and a takedown process. This is not legal advice; church counsel reviews it before launch (build 10.5).
- **Licensed translations** (ESV, NIV, NLT, NASB, CSB) would need a written license held by the church, not Thomas (Crossway licenses only organizations). ESV's free API terms cap local storage at 500 verses, which a local-first app passes quickly.

### ➕ Group-created passages

Leaders create a passage for their group: title, references and outline headings. Under R15 this is the only user-authored content in v1 besides the group name. It appears on members' shelves and never carries pasted text. Moderation is under User Groups.

**Open questions:** gate 6.1 (pasted text kept out of Seedling's account backup, as proposed, or backed up end-to-end encrypted) and gate 5.2 (KJV and WEB already in the beta).

## Real-Time Recital Matching

Similar to a karaoke machine, user begins reciting Bible text and open-source STT models parse their input.
Their input forms a moving trail behind a middle marker with the answer text appearing behind the marker.
The level of match between input and answer text is indicated by color coding.
These trails are stored and can be compared later on to show progress as trails are spotty and then turn to green.

**➕ Claude:** Thomas's "middle marker and trail" works like a teleprompter. The design is **Proposed**; engine facts come from research: stt.md.

### ➕ What the user sees

```
 Doing Right by Others › Anger and Murder (1 of 2)        ← map strip
 ─────────────────────────────────────────────────
  ²¹ You have heard that it was said to the              ← trail: what you said,
  ancients, ‘Do not murder’ and ‘Anyone who                 marked by match
 ━━━━━━━━━━━━━━━━━━━━━━━ ● ━━━━━━━━━━━━━━━━━━━━━━━━━      ← the marker
  m░░░░░░ w░░░ b░ s░░░░░░ t░ j░░░░░░░.’ ²² B░░ I …         ← ahead: depends on the step
```

- **The marker** is a fixed line in the middle of the text area. The passage keeps its layout and scrolls up so the next expected word sits at the marker.
- **The trail**: words already spoken move above the marker, each marked by how well it matched (Thomas's "answer text appearing behind the marker").
- **Text ahead** depends on the step. On "Read it aloud" it is fully visible (karaoke). On "Fill in the blanks" and "First letters" it shows that step's cues, and your voice fills them in. On "Say it from memory" it is hidden; only the map strip and verse numbers remain.
- **The marker sits at the furthest confirmed word.** It moves back only when you repeat a phrase (no penalty). Skipping ahead marks the skipped words missed.
- **Pauses.** After 6 s of silence, a "Need a nudge?" button offers the next first letter; using it counts as a hint. Listening stops after about 15 s of silence; both times are adjustable and never below 6 s (R13). Older reciters often pause to remember, so the stop is generous (research: product.md). Nothing reveals itself automatically.
- **Reduce Motion**: no scrolling animation; the view jumps a line at a time.

**Word states.** Color is always paired with a shape, as WCAG 1.4.1 requires (the Web Content Accessibility Guidelines rule against color-only meaning), on a colorblind-safe blue/orange palette, never red/green.

| State | Look | Counts as |
|---|---|---|
| Pending | Hidden or cue, per step | |
| Tentative (recognizer still guessing) | Light tint | Not yet scored |
| Matched | Solid blue fill + check underline | Correct |
| Close (sound-alike, small slip) | Dotted underline | Correct for coloring; grading rule under Robust Learning Algorithm |
| Missed | Orange outline box | Miss |
| Hinted | Small letter badge | Hint (→ Again) |
| Extra words | Small caret between words | Ignored unless many |

### ➕ Which steps take voice

Every step whose answer is verse text: Read it aloud (tracking only; always graded Easy), Fill in the blanks, First letters, One verse hidden, Middle hidden, Say it from memory, Fill in the missing part, and a section's "Say it from memory." Outline steps (Fill in the heading, Name the parts) use tap-to-reveal self-check in v1. Voice can come later, since the same aligner can match headings.

### ➕ Recite freely

Sequence v2 Decision 4 caps in-schedule recitation at about 450 words (about 3 minutes); whole movements are practiced outside the schedule. **Recite freely** is that place (Personal alpha):
- Open any passage, pick a branch on its map (a section, a movement, the whole passage) and recite with the teleprompter. Sessions are chained at section boundaries, so long recitals stay manageable and the map advances as you go.
- It doesn't change the schedule. It is practice and a check-up, not a test.
- **Check-ups**: trial 2's checkpoints become a gentle prompt 30, 60 and 90 days after a passage's text is fully introduced: "Try the whole Sermon with only the outline."
- **Trails over time live here.** Each section keeps a history: one thin strip per attempt (one tick per word, colored by state), stacked by date. Spotty strips turning solid is Thomas's "spotty, then green" (in blue, for colorblind safety). A score line reads "94% of words · 1 nudge." Attempts from a different engine version are labeled, so an engine upgrade doesn't look like personal progress.

### ➕ When voice isn't the right tool

- **Type first letters**: forgives adjacent-key slips; a word counts as missed after 2 wrong letters (trial 2's rule); each error gives a haptic plus a visual cue.
- **Self-check**: recite aloud or silently, tap "Show," then tap what you missed. The targets are phrases or poetry lines of about 4–6 words, never single words like "a" or "to", so every target meets the 44 pt rule (R13). A tapped phrase counts as one missed word; tapping it again expands it to single words for a finer answer. The app computes the grade, which research shows is more accurate than asking how well you did (Dunlosky & Rawson 2012).
- **Order** is voice → type → self-check, switchable on every step, and the app remembers the choice.

### ➕ Privacy and turning voice on

- **Decided** (decision 9): audio is processed on the device, never recorded and never uploaded. Before each session the app checks that on-device recognition is supported. If it isn't, voice is off. Otherwise the library silently falls back to Apple's servers; this is the part people get wrong (research: stt.md).
- Each attempt stores only a per-word state string ("MMCMXM…"), the engine id and version, and the grades. Transcripts aren't kept, except Thomas's own text-only test fixtures.
- **Two system prompts.** The current iOS path asks for both microphone and speech-recognition permission (research: stt.md). One Seedling screen explains both before either appears: "Seedling listens while you recite so it can show which words you got right. Audio is processed on your device and never saved or uploaded."
- **Recovering voice.** After a "Don't Allow", iOS never asks again; the only way back is the app's page in Settings. So after a denial or a failed on-device check, the step shows a **"Turn on voice"** card with three things:
  - an **Open Settings** button (`Linking.openSettings()`, which opens Seedling's own page in Settings);
  - 3 illustrated steps for turning on Dictation (Settings > General > Keyboard > Enable Dictation; iOS has no direct link to that page);
  - an equally large **Use typing instead** button.

  Both recovery paths are in the voice device script (build 3.12) and in "Help someone set up".

### ➕ Accuracy caveats and how grading absorbs them

- Speech recognition makes more errors on older and slower voices (one corpus showed a 41% relative rise in word errors from ages 60–65 to 81–86) and on Bible names (Zebulun, Melchizedek). Correct recitation marked wrong is the top complaint about competitors' voice modes, such as Verses' "Speak Out" (research: product.md).
- **So:** sound-alikes and homophones count as correct, with a looser threshold for proper nouns. Only the passage's proper nouns are passed to the recognizer as hints (≤ 100); passing the whole verse would flatter the user. Long pauses can lower Good to Hard, never to Again. If most misses are proper nouns or recognition looks unreliable, the grade is capped at Hard and the app asks "Did you say it right?" The user can always override with one tap.

### ➕ Engines by stage

| Stage | Engine | Notes |
|---|---|---|
| v1 (personal, church beta) | expo-speech-recognition 57.x → Apple SFSpeechRecognizer, on-device only | Tested on the iPhone: STT is broken in iOS 26.4+ simulators. A "replay" engine feeds logged text to the aligner in unit tests |
| v1.5 (by public launch) | A small Swift Expo module for SpeechAnalyzer (iOS 26+) | Needs only microphone permission; the transcriber is chosen by A/B testing Thomas's recordings |
| Later | sherpa-onnx streaming model (~45 MB download, Apache-2.0) | For Android 12 and older, or for consistent behavior. Whisper-type models are avoided for grading, since they can invent words during pauses |

**Open questions:** gate 3.1 (voice grading, close words, tentative words) and gate 6.1 (sync trails or keep them on the device).

## Robust Learning Algorithm

Using open-source FSRS at the core of the material review loop.
Outline-based approach rather than reference-verse approach to enhance recall through greater understanding of text shape and logic.
Well-designed sequence of learning phases for tackling large portions of text.
Outline work, text work, vocal recitation work.
Graduated difficulty system.
Genre-adaptive, but generally applied to any selection of material.
\*Requires more R&D and is the core of the product.

**➕ Claude:** **Decided** (decision 7): the app ports sequence v2, with each step its own FSRS item, behind a pluggable scheduler. The rest is **Proposed** detail from R7, R8, R12 and research: product.md.

### ➕ Sequence v2 in the app

- **Phase 1, the outline**, top level first: Read it aloud → See the outline → Fill in the heading → (a day later) Name the parts → Whole outline. Outlines over 40 headings learn their top levels first and the rest just before each branch.
- **Phase 2, the text**, unit by unit (about 80 words, at most 130), in three waves at least a day apart, then section closing:

| Wave | Internal name | In the app |
|---|---|---|
| 1 | Text → header · Missing words · First letters | Where does this belong? · Fill in the blanks · First letters |
| 2 | Scaffolded cloze · Anchor cloze | One verse hidden · Middle hidden |
| 3 | Header → text | Say it from memory |
| Closing | Missing section · First lines · Section header → text | Fill in the missing part · How does each part begin? · Say it from memory (section) |

- **Waves by real days.** Anki forced "a day later" to mean "12 cards later." The app's release planner uses the calendar: a wave opens no earlier than the local day after the previous wave was introduced. At most 2 units are in waves 1–2 at once, and missed days don't pile up new material; it simply waits (App Architecture §4).
- **Today's session** = due reviews (lowest R first, i.e. thirstiest) + new steps up to the pace, in ladder order. A step graded Again returns later in the same session (sequence v2's 10-minute learning step). If reviews alone would exceed the day's time, new steps pause: "Catching up today."

### ➕ What changes from Anki

- **Automatic grading** (R7). Every recall step produces an Attempt (input mode; words matched, close and missed; hints; peeks; hesitations; duration) and the app turns it into a grade. **App Architecture §4 is the source of truth; this is a summary.** The rule ports trial 2's type mode (`notes/sequence_v2_draft.md` §11, `src/deck/assets/card.js`):

| Grade | When | Result line |
|---|---|---|
| Again | A hint, a peek or "Show me" was used, or 2+ words were missed | "This one needs another look. We'll come back to it in a few minutes." |
| Hard | Anything else | "Got it, with some effort. See you again {tomorrow}." |
| Good | No words missed, at most 1 close word, no hints, fewer than 2 hesitations | "Well done. See you again {in 3 days}." |
| Easy | Always for Read it aloud and See the outline; for Fill in the blanks and First letters at 100% with no hesitations | "That came easily. See you again {in 9 days}." |

  - {…} is the real next due date in plain words. A **hesitation** is a pause longer than 3 s or 3× the user's usual gap between words (research: product.md). Hesitations can lower Good to Hard, never to Again. A failed recall is never Hard (the classic FSRS misuse). Easy on perfect scaffolds retires them, as sequence v2 §6 intends.
  - The headline never says "wrong", "failed" or a miss count; the words below it are tinted by state instead. These lines join the no-guilt word-list check (build 5.9).
  - Under the line, a small **"Grade it differently"** link offers the other plain choices: "I needed a lot of help" (Again), "I got it with some effort" (Hard), "I got it" (Good), "It was easy" (Easy). Both the automatic and the final grade are logged for calibration. Anki's FSRS FAQ says mostly-Again/Good grading works fine (research: product.md).
- **No four buttons, no deck options, no vocabulary to learn.** FSRS-6 defaults with desired retention 0.90; Thomas's trial settings become fixed defaults.
- **Pace setting**, labeled by time, not steps:

| Pace | New steps/day | Sermon on the Mount introduced in | Daily time (estimate) |
|---|---:|---:|---|
| **Gentle (default)** | 6 | ~60 days | ~10–15 min |
| Steady (trial pace) | 12 | 30 days | ~20–25 min on average, peaks near 35 |
| Ambitious | 18 | ~20 days | ~30+ min |

The minute figures are extrapolated from trial 2's simulation (24 min average at 12/day). Build step 1.13 re-simulates them against the app's own release planner before they appear in the UI. The default is confirmed at gate 5.2.

### ➕ When is a verse "known"?

The governing step for a verse is its unit's "Say it from memory" (Header → text). A verse is **rooted** at stability ≥ 21 days (Anki's "mature"). A section blossoms when its section recite step (or all its "Fill in the missing part" steps) reaches 21 days. `verse_mastery` is computed on the device, and groups read only that, never raw reviews (R5).

### ➕ Weekly rhythm and reminders

R12 in practice (research: product.md). The point is to keep people coming back without guilt.
- **A weekly goal, not a daily streak.** The user picks 3–7 days a week (default 5) and optional rest days (default Sunday). Rest days never count against them. Shown as "4 of 5 days this week."
- **Repair.** A missed day is repaired by studying within the next 2 days: "Tuesday's done too: you caught up today." Repairable streaks soften the drop-off after a break (Silverman & Barasch 2023).
- **Welcome back.** After 3+ days away there's no backlog count. A catch-up session capped at 10 minutes waters the thirstiest leaves first and adds no new steps: "Welcome back. 10 minutes will water your thirstiest leaves."
- **Fresh starts.** Mondays and the 1st of the month get fresh-start wording ("A new week. Ready when you are."), because people take up goals after such landmarks (Dai, Milkman & Riis 2014).
- **One reminder, opt-in.** It comes at one time the user picks and shows a phrase from their current passage ("'The LORD is my shepherd…' · about 12 min today"). After 3 ignored in a row it switches to weekly and says so: "We'll remind you on Sundays instead. Change this in More."
- **Never:** guilt copy, crying mascots, leaderboards, points, paywalls, or donation asks in notifications.

### ➕ Genre adaptation

| Genre | Adaptation |
|---|---|
| Prose (discourses, epistles) | Defaults above |
| Poetry (Psalms, prophets) | Units are stanzas; the outline is hand-written stanza titles; one line per poetry line, using `Chapter.json` indents. Psalms average about 2.5 steps per verse because their verses are short |
| Lists and genealogies (the Twelve, the table of nations) | Mark a section `style: list` in the outline: extra First letters steps in waves 2–3 and items grouped in fives for "Name the parts" (concept.md's first-letter idea against interference) |
| Long narrative (Genesis, Kings) | **Learn the outline only**: Phase 1 plus "Read it aloud" per section, no verse drills. Thomas's `notes/ideas.md` calls outline mastery the realistic goal for large OT books. On the plant, branches grow without leaves |
| Very short passages | One-verse units skip wave 2; a passage with a single section skips the outline phase (fixes today's generator crash) |

### ➕ R&D agenda (after the church beta)

1. **Calibrate grading thresholds** against Thomas's trial 2 Anki log (exported when the trial ends) and beta logs of automatic vs final grades.
2. **Optimize FSRS parameters** offline in Python (py-fsrs optimizer), first on trial 2, then on pooled beta logs. The parameters ship to devices and are validated before use. Per-user optimization comes after a few hundred reviews.
3. **Track the "Again on first sight" rate** per step type. A high rate means that step is too steep (sequence v2 §6).
4. **Per-unit memory model** (sequence v2 §9): one memory state per unit picks the step (First letters when recall odds are low, Say it from memory when high). Adopt it only if it beats the ladder on trial 2 and beta data: fewer reviews for the same check-up scores.
5. **Check-up scores** (outline cold at the end of Phase 1; the whole text from the outline at days 30, 60 and 90) are the yardstick for every change above.

### ➕ "Graduated difficulty," end to end

Read it aloud → See the outline → Fill in the heading → Name the parts → Whole outline → Where does this belong? → Fill in the blanks → First letters → One verse hidden → Middle hidden → Say it from memory → Fill in the missing part → section Say it from memory → Recite freely (whole movements) → check-ups. Each step removes only some cues, so it can be answered from the one before ("vanishing cues"). The output moves from reading aloud with the text, to reciting with cues, to reciting from the map alone.

**Open questions:** gate 5.2 (default pace and rhythm; "Learn the outline only" in the beta) and gate 9.7 (whether a section's recite step overrides the unit step as a verse's governing step once it exists).

## Beautiful UI

Using AI's help with React Native and modern Bootstrap
Colorful and fun to look at
Cohesive aesthetic

**➕ Claude:**

### ➕ Design principles (Proposed)

- **Calm.** One primary action per screen, a visible way back on every screen, no red alerts, no badges or counters competing for attention.
- **Colorful garden palette.** Leaf greens, soil browns, sky blue and blossom accents. Each stage of the ladder (outline, text, section) gets its own banner hue, as on the trial cards.
- **Cohesive.** One token file defines colors, radii, spacing and the type scale. Every screen uses the tokens and nothing else.
- **Plain words.** Never "card", "deck", "cloze", "FSRS", "stability" or "retention" (R10).

### ➕ Why not Bootstrap

Bootstrap is CSS for web browsers, and React Native doesn't render CSS, so it can't be used directly. The equivalent pair (R4): **Uniwind** brings Tailwind v4 class names to React Native (Tailwind's utility classes resemble Bootstrap's: `p-4 text-lg bg-leaf-500`), and **HeroUI Native** supplies ready components (buttons, sheets, inputs) the way Bootstrap does. Brand tokens live in one `global.css` with light and dark variants. AI agents write Tailwind fluently, which suits the design loop below. Fallback: Unistyles 3.5 with a small hand-built component set. Avoid NativeWind v5 (still a release candidate) and Tamagui 3.0 (released days ago) (research: stack.md).

### ➕ Accessibility defaults (R13)

- Dynamic Type (the iOS text-size setting) up to 200% and beyond, tested at the largest size (AX5); verse text at least 20 pt by default.
- Contrast target 7:1 (WCAG AAA, the strictest level of the Web Content Accessibility Guidelines) for text in light and dark modes.
- Primary buttons full width and at least 56 pt tall; every target at least 44 pt with 8 pt spacing, including self-check phrases at the default text size; nothing swipe-only.
- Color always paired with shape; colorblind-safe blue/orange.
- Reduce Motion respected everywhere, including the plant and the trail.
- No time limits on recitation; silence timeouts of 6 s or more, adjustable.
- **"Hear it"** (Church beta): on-device text-to-speech (expo-speech, which uses iOS's built-in voice; free, offline, sends nothing) with a speed control. It's offered on Read it aloud, See the outline, a step's revealed answer and the intro articles. It never appears on a recall step before the answer is revealed. It helps slow readers and people with low vision or dyslexia.
- **"Help someone set up"**: a helper walks a friend through text size, turning on voice (including the recovery card), a first passage and joining a group by QR code.

### ➕ Key screens

Tabs: **Today**, **Passages**, **Groups**, **More** (App Architecture §11).

| Screen | What it does | Stage |
|---|---|---|
| First run | See below | Alpha (basic) → beta |
| Today | Plant, the "Today · about N minutes" button, this week's rhythm | Alpha |
| Step | Banner, map strip, text, mic / type / self-check controls, result line, "Stop for today" | Alpha |
| Session end | Plant growth animation, rhythm, "See you tomorrow" | Alpha |
| Passages | My passages with progress, the starter shelf with sizes and days, "Make your own" | Beta |
| Passage | Its map, progress per section, Recite freely, trail history, study helps; menu with Pause, Start over, Remove | Alpha → beta |
| Picker and outline editor | Choose verses, edit headings | Beta |
| Recite freely | Teleprompter over any branch | Alpha |
| Study helps | Sheet over the current step | Beta |
| Groups | Group tree, birds, join by code or QR, leader passages | Beta |
| More | Pace, rhythm, text size, input default, reminder, Learn (articles), Help, Give, account and backup, About and credits, privacy, delete account | Alpha → beta |

**First run** (the one canonical flow; Proposed, confirmed at gate 5.2). The aim is a first success within about two minutes, with no articles to read and no settings to choose.
1. **Welcome**: one sentence about Seedling, an optional 60–90 s video, and **Start**. A small "Choose another passage" link serves people who know what they want.
2. **"Is this text easy to read?"**: a verse at the current size with large **Bigger** and **Smaller** buttons.
3. **Straight into Psalm 23's first step**, on the defaults: Gentle pace, 5 days a week, Sunday rest.
4. **The microphone is explained at the first voice step**, on Seedling's own screen before the system prompts. "Not now" continues without voice.
5. **The reminder is offered after the first session ends**: "Want a nudge each day? Pick a time."

Pace, rhythm and reminder can all be changed later in More. Research recommends a single path, a short video and face-to-face onboarding for older adults (research: product.md); the in-person part is "Help someone set up".

### ➕ Help and recovery (Proposed; Church beta)

- **"How to do this step."** The first 2 times each step type appears, a one-line panel says what it wants ("Say the heading that goes in the gap"). A **How?** link reopens it later. It is separate from the study-helps **?**.
- **"Stop for today"** on every step saves progress and shows the plant's growth so far. Stopping early is never a failure.
- **Passage menu**: **Pause** (no new steps or reviews until resumed; leaves get thirsty but never die), **Start over** and **Remove** (its history stays in the log). Each asks for confirmation in plain words.
- **More → Help**: short how-to videos (Claude scripts them, Thomas records them on the iPhone) and "Ask {church contact}" with a phone number or email.
- **Send feedback** opens a mail draft (App Architecture §16). If no mail app can open it (`Linking.canOpenURL('mailto:')` is false, common for Gmail-only users), it shows the address with a **Copy** button instead of failing silently.

### ➕ Step design (sequence v2 §8, adapted to Dynamic Type)

- **Map strip** on every text step, front and result, except where position is the answer ("Where does this belong?"). At large text sizes it collapses to a one-line breadcrumb ("Sermon › Doing Right by Others › Anger (1 of 2)"); tapping it opens the full map in a sheet.
- **Stable layout.** A unit looks the same on every step *at a given text size*: blanks keep their word's width, first letters sit in place with the rest of the word blurred, verse numbers are small and raised, and poetry lines keep their indents. Changing the text size reflows it, which is expected (research: product.md).
- **Reveal in place.** "Show" reveals hidden words where they stood, tinted; there's no flip to a separate back.
- **One prompt banner** in large type, colored by stage.
- **"How this was graded" footer.** Thomas liked trial 2's rubric guide, especially when it matched the code. A small footer states the actual rule in plain words, e.g. "1 word close, no hints → Good." It is generated from the grader's own reasons, so it can't drift from the code.

### ➕ Dark mode, haptics, sound

- **Dark mode** follows the system. Every token has a dark value; verse contrast stays at 7:1; the plant gets an evening palette.
- **Haptics**: a soft tap when a step completes and a light warning on a wrong first letter. Vibration perception declines with age, so each haptic is paired with a visual cue and an optional gentle sound. Haptics and sounds each have a setting.

### ➕ How Claude designs in code, and what Thomas reviews

**Loop** (decision 12): Claude writes a screen → builds it in the iOS Simulator → captures light/dark × default/AX5 text → checks it against this section and R13 → fixes → repeats. Maestro flows (scripted UI tests) cover the first run, a session and a recitation. Tools and foot-guns: Development Workflow → Tools and build step 2.14.

**Thomas reviews**
1. A one-page style tile (palette, type scale, buttons, a plant sample) before any screens are built.
2. Each key screen's screenshot set in its pull request.
3. The feel on his iPhone: voice, haptics, plant animation.
4. A session with 3–5 church members aged 60+ before TestFlight (build 5.17): the first run, text size, the tone of thirsty leaves, voice leniency.

**Open question:** gate 2.1 (custom-branded components with native navigation, as proposed, or platform-native components).

## User Groups and Shared Content

- Group progress tracker that shows how much of the whole "tree" of the Bible the users collectively know by heart
- Groups can create custom Journies

**➕ Claude:** Proposed for the church beta, within R15's limits.

### ➕ How groups work

- **What a group is**: a small group, class or whole congregation. Creating or joining one needs an account (13+, R3); the rest of the app never does.
- **Joining.** The leader shows a QR code with the 6-character code printed beside it in large type ("ABC123").
  - Members scan it with the iPhone's own **Camera** app, which needs no new permission in Seedling. The QR is a link that opens Seedling straight to "Join the Tuesday Night Group?"
  - Opening the app from a link needs **Universal Links**: an apple-app-site-association file (a small JSON file on a website that tells iOS which app may open its links) on a domain, plus an Associated Domains setting in the app. The church site can host it if its web host allows that file; otherwise a cheap separate domain. Decided at gate 7.1.
  - **Without the app** (common during the TestFlight beta), the link opens a web page: "Get Seedling, then enter code ABC123," with the install steps.
  - Typing the code always works too.
  - This is the heart of "Help someone set up": a leader can take a member from install to joined in one sitting.
- **Roles** (App Architecture §9, `group_members.role`):

| Role | Can |
|---|---|
| Owner | Everything a leader can; rename or delete the group; make leaders |
| Leader | Create group passages; see the group tree; remove members; handle reports |
| Member | Learn group passages; appear as a bird; leave anytime |

- **Group passages**: a leader adds a passage (title, references, outline headings) and it appears on every member's shelf, e.g. "This fall: the Sermon on the Mount." The group tree shows that passage's combined progress as its own limb.

### ➕ The group tree

- Trunk → 10 genre limbs (Law, History, Wisdom, Major Prophets, Minor Prophets; Gospels, Acts, Pauline Letters, General Letters, Revelation) → 66 book branches (length grows with the square root of verse count, since 2 John has 13 verses and Psalms 2,461) → 1,189 chapter twigs.
- Leaf density on a chapter = the share of its verses that at least one counted member has rooted. A chapter blossoms when 3 or more members have it rooted (gate 7.1).
- **Members are small birds** in the branches (Matt 13:31–32: the mustard seed grows into a tree where birds nest), clustered near what they're learning. No names by default and no ranking anywhere. A summary line reads "Together we know 1,240 verses by heart."
- **Data**: each counted member uploads only a bitset (a compact yes/no list) of rooted verses: 31,086 bits, about 3.9 KB. The server keeps per-group counts per verse. No review logs, grades, trails or audio are shared (R5, research: product.md).

### ➕ Privacy defaults

Two separate per-member settings, both stored per group (App Architecture §9):
- **Count my verses in the group total** (R11: opt-in). The join screen asks with two equal buttons, "Join and count my verses" and "Join without counting," so nothing is pre-chosen. Only counted members send a bitset. It can be changed anytime.
- **Show my name on my bird** is off by default. Leaders see the aggregate, not individuals, unless a member turns this on.

### ➕ Moderation basics (Apple guideline 1.2)

- User content is limited to the group name and leader-authored passage titles and outline headings. There's no chat, which keeps the age rating and the moderation burden low (R15).
- A word filter on those fields; a **Report** button on group names and group passages; **block** (hide a user's content; leaders can also remove members); and published contact information on the church's support page.
- Reports go to Thomas and a church contact, with a response target written into the community guidelines.

### ➕ Pastoral considerations

- Memorization isn't a competition, hence no rankings or comparisons. Matt 6:1 warns against practicing righteousness to be seen.
- Birds can't be tapped to inspect someone's progress unless that person opted in, and nobody can see who has fallen behind.
- The leader can set the group's default rest day (e.g. Sunday); members can change their own.
- **Celebrate together, without new user content.** When a section blossoms on the group tree, the app shows a fixed line, "The group finished the Beatitudes," with a blossom animation. Members can't write or edit it (R15).
- **13+**: accounts and groups are 13+ in v1. Under-13 users stay local-only and can't join groups. A family or kids mode with parental consent comes later (decision 9).

**Open questions:** gate 7.1 (named sharing, blossom threshold, default rest day, report handling, join-link domain).

## Access to free Bible APIs to enhance card content

- Quick links to public domain commentaries on text being learned to mitigate context switching and promote understanding
- Quickly check to see if an answer is available to a hang up in understanding so that learning can resume

**➕ Claude:** Proposed; sources and licenses from research: content.md.

### ➕ The study-helps sheet

A sheet slides up over the current step or verse, with three parts:
1. **Commentary on this verse.** Jamieson-Fausset-Brown (JFB) first (verse by verse, compact), then Clarke and Matthew Henry (Henry writes in long sections), with Gill, Calvin and Keil-Delitzsch (Old Testament only) on request. All six are public domain.
2. **Cross-references**: the top 5 by OpenBible relevance score (CC BY 4.0). Tapping one shows that verse from the bundled BSB in the same sheet, without leaving the session.
3. **Later**: people, places and events from the API's datasets, and Tyndale's topic profiles (e.g. "Aaron").

**The Tyndale caveat.** Tyndale Open Study Notes are modern and readable but licensed CC BY-SA 4.0 (attribution + share-alike), and their headwords quote the NLT, so they won't match BSB wording. Show them unmodified, with the note "These notes quote the NLT," and never AI-summarize them: a summary is an adaptation that would have to be released under CC BY-SA. Fetching them at runtime rather than bundling them avoids an open question about whether app encryption counts as DRM (digital rights management, i.e. copy protection, which CC licenses forbid adding).

### ➕ The "hang-up" flow

Thomas's goal: check for an answer, then resume learning.
1. Tap **?** on a step. On non-recall steps (Read it aloud, See the outline) it's always there. On recall steps it appears on the result line, after grading, so study helps never become a peek at the answer.
2. The sheet opens over the step. The microphone and silence timer pause.
3. Read, follow a cross-reference, close.
4. The session resumes on the same step in the same state.

### ➕ Offline caching and consent

- Commentaries total about 162 MB, so they're never bundled. When a passage is started, its chapters' notes download on Wi-Fi and are cached in SQLite. Cross-references are fetched per chapter and cached the same way.
- Requests are anonymous GETs to bible.helloao.org with no account and no user data, though helloao sees the IP address and the chapter.
- **Consent is the R3 opt-in.** Nothing downloads until the user agrees, once per feature (study helps; other translations): "Study helps download free notes from an online Bible library. Nothing about you is sent. Download?"
- **Under 13.** Downloads stay off only when the app *knows* the user is under 13: they answered the age screen that way, or expo-age-range reports it. Everyone else, including local users who never saw the age screen, gets the consent prompt. Confirmed at gate 5.2.

### ➕ Attribution

The app keeps its own attribution table, because the local DB's license notices are empty. An About → Credits page lists: the BSB (a courtesy credit, not required); each commentary with "public domain"; "Tyndale Open Study Notes, CC BY-SA 4.0, unmodified, reformatted" with a license link; and "Cross references: OpenBible.info, CC BY 4.0." The same credit appears under each note.

### ➕ Optional later: ask about a verse

An "Ask about this verse" box answered by an AI model that may use **only** the public-domain commentaries on that verse, quoting them, labeled "AI-generated; check the sources." Tyndale is excluded (above). Thomas decides whether it belongs at all (gate 5.2):
- **Cost**: per-question model fees, paid by the church or Thomas, with a hard budget cap. It also needs a server endpoint (API keys can't live in the app) and an account for rate-limiting.
- **Privacy**: questions are user content sent to a third-party model provider, so the privacy policy and store labels change.
- **Pastoral risk**: a fluent wrong answer about Scripture. The pastor would need to review the prompt and answer style.

**Open questions:** gate 5.1 (lead with JFB, public domain and verse-level but older language, or Tyndale, modern but NLT-keyed) and gate 5.2 (AI questions).

## Donation Path / PWYW

Option to give with some kind of promise to dedicate the money to the Great Commission.

**➕ Claude:** **R2 in detail.** Decided: gifts go to the church (decision 2). The mechanism and wording are Proposed.

### ➕ How it works

- **One "Give" button** opens the church's existing giving page in Safari via `Linking.openURL`, not an in-app browser. Apple guideline 3.2.2(iv) allows a free app to collect charitable funds "outside of the app, such as via Safari" (research: policy.md). Google Play says its own billing must not be used for tax-exempt donations, so linking out works there too.
- **It unlocks nothing**: no supporter badge, no plant boost, no extra features, ever.
- **Placement.** Allowed: More → Give, the About page, and the end of the "Why is it free, and where does a gift go?" article. Never: sessions, session end, the plant, celebrations, groups, the first run, reminders or any notification. A paywall or payment prompt reached from a reminder is a top complaint about the market leader (research: product.md).

### ➕ Why "PWYW" is dropped

"Pay what you want" or "support the developer" is payment for the app or a tip, and Apple guideline 3.1.1 requires tips to use in-app purchase (Apple's billing, with its commission). Gifts to Thomas personally also aren't tax-deductible, so Google's donation exemption wouldn't apply, and Stripe plus a Chase account in his name would make them personal income. A gift **to the church, for the Great Commission** avoids all three problems, which is why Stripe and the Chase account leave the stack.

### ➕ Draft wording

> **Give**
> Seedling is free, with no ads and nothing to unlock. It is a ministry of {Church}.
> If you'd like to give, your gift goes to {Church}, a 501(c)(3), for the Great Commission: making disciples of all nations (Matt 28:19–20).
> Giving opens {Church}'s giving page in Safari. It doesn't change anything in the app.
> [ Open giving page ]

Add "Gifts are tax-deductible as allowed by law" only if the church confirms it receipts gifts that way.

### ➕ The church's role

- Owns the giving page and payment processor, issues receipts, and approves this wording in writing.
- Decides how gifts are designated (for example missions, or Seedling's costs: about $10 a month of cloud, plus Apple's $99/year unless the nonprofit fee waiver applies) and can say so publicly.
- Is the publisher (R1): its name appears as the seller, and its site hosts the privacy, terms, support and deletion pages (R14).

### ➕ Later: in-app Apple Pay

Only Apple-approved nonprofits may take donations inside the app, and only with Apple Pay (guideline 3.2.1(vi)). A US nonprofit qualifies by holding any Candid Seal of Transparency; the seal is free and Apple charges no fee. A church not in the IRS's list of exempt organizations must first send IRS documents to get listed. It also needs a payment provider and an Apple Pay build. Optional, and only if the link-out proves to be a real barrier.

**Open questions:** gate 0.9 (the giving URL, the church's approval of the wording, tax-deductible receipts) and gate 8.1 (Give in the beta or at launch).

# Technical Specifications and Requirements

**➕ Claude:** What changed from your lists. Each section below explains its change.

- **Developer accounts (a change to decision 3).** Your Individual Apple account builds only the dev version for your phone; the church's Organization team owns the production app from the first TestFlight upload. Why: Apple Developer Setup.
- **Donations.** Stripe and the separate Chase account are dropped. A "Give" button opens the church's existing giving page in Safari (R2).
- **Bootstrap.** Bootstrap only works in web browsers. Uniwind (Tailwind CSS for React Native) plus HeroUI Native components take its place.
- **Cloud cost.** $0 during personal use, because the app is local-first; about $10/month once the backend is live.
- **Claude's access.** Claude works only in the dev cloud project, under its own limited Google identity. Your owner login never stays on the Mac user Claude runs as, so prod stays yours (Development Workflow).

## Stack

- Cross-platform (Android and iOS)
- leverage as many iOS/Android SDKs as possible for widgets and UX friction reduction
- React Native
- Typescript
- Terraform
- Probably SQL of some kind
- Bootstrap
- STT
- FSRS
- Local Sqlite (and/or GCP db service)
- Bible api [https://bible.helloao.org/docs/]
- GCP for users and groups and related auth (equivalent of AWS Cognito)
- Stripe and separate Chase bank account for donations/PWYW
- Figma UI design
- Expo

**➕ Claude:** Each of your bullets mapped to a concrete choice. Status follows the legend at the top: the R-items are Decided unless you override them; **Proposed** marks my further recommendations. Versions are as of 2026-10-14 (research: stack.md, backend.md).

| Your bullet | Choice (version) | Status | Why |
|---|---|---|---|
| Cross-platform (Android and iOS) | One Expo codebase. iPhone first (personal use, then the church TestFlight beta); Android beta later, from the church's Play account | Decided (4, 8, R1) | You have only an iPhone. Until someone lends an Android phone, Android is tested on the Mac's emulator and on Firebase Test Lab (Google's hosted test devices) |
| leverage ... SDKs | See "Platform features" below | Proposed | |
| React Native | React Native 0.86.3 + React 19.2.3, pinned by Expo SDK 57. Only the New Architecture (RN's current native layer) and the Hermes V1 engine (Meta's JavaScript engine built for RN) are supported | Decided (R4) | Expo picks the RN version, so never bump RN by hand |
| Typescript | TypeScript ~6.0.3 | Decided (R4) | TypeScript 7.0 is npm "latest", but Expo's templates still pin 6.0. Don't let tooling bump it |
| Terraform | Terraform 1.16 with the hashicorp/google and google-beta providers ~> 8.7. State in a GCS (Google Cloud Storage) bucket per project; roots `infra/envs/dev` and `infra/envs/prod` | Decided (R5) | Firebase's own Terraform guide pins provider 6.0, which is out of date |
| Probably SQL of some kind | **SQLite on the device** (expo-sqlite ~57.0.4 + Drizzle ORM 0.45.4, a typed query layer) and **Postgres 18 on the server** (Cloud SQL db-f1-micro; Postgres.app 18.6 on your laptop) | Decided (R4, R5) | The phone's SQLite is the source of truth for study state. Postgres holds only what signed-in accounts sync. Postgres 18 has a built-in `uuidv7()` |
| Bootstrap | **Uniwind 1.12.2** (Tailwind CSS v4 classes for RN) + **HeroUI Native 1.0.10** (ready-made accessible components). Fallback: Unistyles 3.5 | Decided (R4) | Bootstrap needs a browser's DOM, so it can't run in a native app. This pair is the closest "modern Bootstrap": utility classes plus a component kit, and Claude writes Tailwind fluently. NativeWind v5 is still a release candidate; Tamagui 3.0 shipped days ago |
| STT | expo-speech-recognition 57.1.x (Apple's SFSpeechRecognizer), on-device only. v1.5 adds a small SpeechAnalyzer module (iOS 26+); an open-source engine (sherpa-onnx) comes later | Decided (5, R6) | Voice mode turns off when the phone can't recognize speech on-device, so audio never leaves it |
| FSRS | ts-fsrs ^5.4.2 (FSRS-6) on the device. Parameters are optimized offline in Python (py-fsrs optimizer) and shipped to devices | Decided (R8) | Pin ^5.4, because 6.0 is still beta. No optimizer runs on a phone today |
| Local Sqlite (and/or GCP db service) | Both. SQLite is always there. Cloud SQL serves only accounts (backup/sync, multiple devices, groups) through a custom append-only sync log | Decided (R3, R5) | Local-first: the app works fully with no account and no network |
| Bible api (helloao) | The full BSB ships inside the app as a SQLite asset built by the Python content exporter. The helloao API supplies other public-domain translations and commentaries on demand, cached on the device. The first download asks for consent, and that prompt is the R3 opt-in | Decided (R3, R9) | Works offline from day one; the API only adds extras |
| GCP for users and groups and related auth | Firebase Auth on Identity Platform (Google Cloud's Cognito equivalent; free under 50K monthly active users), with Sign in with Apple + Google. The API runs Hono 4.13 on Node 22/24 in Cloud Run and verifies tokens with firebase-admin 14.5 | Decided (10, R3, R5) | Apple guideline 4.8 requires Sign in with Apple whenever Google sign-in is offered |
| Stripe and separate Chase bank account | **Dropped** | Decided (R2) | Gifts go to the church through its giving page (see Apple Developer Setup) |
| Figma UI design | Optional | Decided (12) | Claude designs in code, using the simulator screenshot loop |
| Expo | Expo SDK 57 (expo ~57.0.28), development builds only, never Expo Go. Upgrade to SDK 58 2–4 weeks after it goes stable, before the church beta. iPhone dev builds compile on your Mac; EAS Free (Expo's cloud build service) handles Android and release builds | Decided (R4) | SDK 58 adopts the UIKit scene lifecycle (iOS's newer way for an app to manage its windows), which iOS 27 SDK builds require. Local builds cost nothing |

**Also in the stack (Decided: R4):**
- **Navigation:** expo-router ~57.0.26 (file-based routes, like Next.js pages).
- **State:** Zustand 5.0.15 for temporary UI state; TanStack Query 5.104 for API calls only; zod 4.6 for the schemas shared by app and API.
- **Plant:** @shopify/react-native-skia 2.6.2 + Reanimated 4.5.1 + react-native-worklets 0.10.1.
- **Tests:** Vitest 5.0.4 for the pure-TS packages; jest-expo ~57.0.6 + Jest 30 + React Native Testing Library 14.1 for components; Maestro CLI 2.11.0 for end-to-end flows; Python's `unittest` for the generator and exporter (run on the Mac, because they need the git-ignored `data/bible.eng.db`).
- **Monorepo:** pnpm workspaces on Node 22 or 24 LTS.
- **Foot-gun (the part people get wrong):** npm's "latest" Reanimated, Skia and TypeScript are newer than SDK 57 supports. Add native packages with `npx expo install <pkg>`, never `pnpm add`. `npx` runs a package's command-line tool without a global install; `expo install` picks the version that matches the project's SDK; `npx expo install --check` lists mismatches.

### ➕ Platform features ("leverage as many SDKs as possible")

Staging is Proposed and matches the Build Phases.

| Feature | Package | Stage | Note |
|---|---|---|---|
| On-device speech | expo-speech-recognition 57.1.x; SpeechAnalyzer module in v1.5 | Personal | Tested on the iPhone, because speech recognition is broken in iOS 26.4+ simulators |
| Local reminders | expo-notifications ~57.0.22 | Personal | One repeating daily notification, no push server. iOS keeps only 64 pending notifications, so the app reschedules on each open |
| Haptics | expo-haptics | Personal | A light tap when a grade lands; an error cue in first-letter typing |
| Dynamic Type (the iOS text-size setting) | Built into RN `Text`. Keep `allowFontScaling` on; cap `maxFontSizeMultiplier` no lower than 2.0 | Personal | Tested at the largest accessibility size (R13) |
| Share sheet | RN's built-in `Share` API | Church beta | Shares a group join link (QR codes in person) |
| Sign in with Apple | expo-apple-authentication ~57.0.2 (+ google-signin 16.1.5 for Google) | Church beta | Accounts arrive with the beta. Tested on the iPhone, because it always errors on the simulator |
| Age signals (Texas SB2420) | expo-age-range | Before teen accounts exist in Texas | See Apple Developer Setup step 16 |
| Home-screen widget | expo-widgets ~57.0.24 (iOS) | Public launch | A PNG snapshot of the plant plus today's due count. Widget code can't run Skia or read app state, so the app pushes data to it. An Android widget comes with expo-widgets in SDK 58 |
| App Intents / Siri ("Start my review") | @bacons/apple-targets 5.0.0 (a Swift target) | Later | Needs Swift |
| Live Activities (progress on the lock screen) | expo-widgets | Maybe | Only if sessions turn out long enough to matter |

**Open question for Thomas:** is a web version ever a goal? I've assumed not; yes would change the database and styling choices, because expo-sqlite's web support is alpha (gate 0.6).

## Cost Generators

- Apple Developer license for host on Apple App Store with (~$100 per year)
- Google Play Store developer license?
- GCP:
- api for backend
- database for users
- security/auth

**➕ Claude:** Verified prices from the research (policy.md, backend.md, stack.md). Items without a researched price say so.

| Item | One-time | Yearly | Monthly | Stage | Paid by |
|---|---|---|---|---|---|
| Apple Developer Program, your Individual account | | $99 | | Personal | Thomas |
| Apple Developer Program, church Organization | | $99, or $0 with Apple's nonprofit fee waiver | | Church beta on | Church |
| D-U-N-S number (the business ID Apple and Google require from organizations) | $0 | | | Now (paperwork) | Church |
| Google Play Console, church Organization | $25 | | | When the Android beta starts | Church |
| GCP in the personal phase | | | $0 | Personal | |
| GCP prod: Cloud SQL db-f1-micro ≈ $7.67 + 10 GiB SSD ≈ $1.70 + backups ≈ $0.10–0.30. Cloud Run, Identity Platform, Secret Manager, Artifact Registry and logging stay in their free tiers | | | ≈ $10 (10–100 users); ≈ $10.50–12 (1,000 users) | Church beta on | Open (gate 6.1) |
| Optional: a hosted dev database (a second Cloud SQL instance) | | | +≈ $9.50 | If wanted before the beta (gate 6.1) | Thomas |
| Optional: one always-warm Cloud Run instance (removes 1–3 s cold starts) | | | +≈ $9.86 (list price) | Held in reserve (gate 8.1) | |
| Later: a bigger database (db-g1-small) at about 1,000 daily users | | | ≈ $28 total | Later | |
| EAS Free: 15 iOS + 15 Android cloud builds a month; over-the-air updates capped at 1,000 monthly users | | | $0 (Starter $19 if the quota bites) | All | |
| Local Xcode builds on your Mac | | | $0 | All | |
| GitHub and GitHub Actions | | | $0 (public repos free; private repos get 2,000 free minutes a month, but lose branch protection on the Free plan: see Development Workflow) | All | |
| Firebase Test Lab, free Spark plan (10 virtual + 5 physical device runs a day) | | | $0 | Android beta | |
| Claude subscription (the simulator pane needs Pro, Max, Team or Enterprise) | | | Your existing plan | All | Thomas |
| Android phone for real-device QA | Borrow ($0) or buy (price not researched) | | | Before the Android beta | Thomas or church |
| DMCA designated agent (the copyright-takedown contact registered with the US Copyright Office) | $6 per 3 years | | | Only if the server ever stores user-pasted text, which v1 doesn't | Church |
| Attorney review (privacy policy, COPPA (the US children's online privacy law, under 13), Texas SB2420) | Price not researched | | | Optional, before teen accounts exist in Texas | Church |

**Totals by stage**
- **Personal:** $99/yr from you, or $0 with a free Personal Team, whose builds expire every 7 days.
- **Church beta (iOS):** the church pays $0–99/yr; the cloud costs about $10/mo.
- **Android beta:** the church adds $25 once, plus a phone if one is bought.
- **Public launch:** no new fees. The cloud stays around $10–12/mo up to about 1,000 users.
- **Gone from your list:** Stripe's fees (2.9% + 30¢ per gift) and the Chase account.

**Budget alerts (Proposed).** A $15 budget on `seedling-dev` and $25 on `seedling-prod`, emailing you at 50%, 90% and 100%. Budgets only alert, sometimes hours late; they never stop spending (foot-guns at build steps 6.3 and 6.5). Managing Identity Platform through Terraform needs Firebase's Blaze plan (pay-as-you-go with a linked billing account), so a billing account exists from the first `terraform apply`; usage at this scale stays free.

**Open question for Thomas:** who pays for GCP long term, your card or a church billing account (gates 0.9 and 6.1)?

## Apple Developer Setup

- tedious
- payments can go to your name because your EIN is just your SSN if you don't have an EIN
- best to have a separate account for your actual revenue
- Screenshots, permissions, privacy policy, terms of service

**➕ Claude:** Your notes as a checklist (research: policy.md). Tags match the Build Phases: **[Claude]**, **[Thomas]**, **[Claude → Thomas]** (Claude drafts, you review or act) and **[Thomas + church]**. Each step names the build step that carries it out; this list holds the detail, the build step holds the schedule.

**Change to decision 3 (R1). Read this first.** "Your Individual account now, the church's later" still holds, but "later" now means *before the first TestFlight upload*, not before public launch. Two Apple rules force it:
- **Transfers need a released app.** Apple's app-transfer tool only moves an app with at least one version released on the App Store. A TestFlight-only app can't move.
- **Bundle IDs are permanent.** Once any build is uploaded under a bundle ID (the app's unique ID, e.g. `org.<church>.seedling`), that ID can never be reused, even if the app record is deleted.

So your Individual team only ever builds a dev bundle ID for your own phone, and the church team owns the production bundle ID from day one. That also avoids migrating Sign in with Apple users later, because their IDs belong to one team. Google Play: no personal account; the church's Organization account opens when the Android beta starts. This is the part people get wrong: never upload a production-ID build from your own team.

**About "payments can go to your name... separate account for your actual revenue."** Right instinct for a paid app, but it doesn't apply here. Seedling is free with no in-app purchases, so Apple pays out nothing and you need no banking or tax setup. Gifts go straight to the church through its giving page. Gifts to you personally wouldn't be tax-deductible, and asking people to "support the developer" would fall under Apple's in-app purchase rules. No revenue account means the EIN question doesn't come up for you.

**Now: church paperwork (longest lead time)**
1. **[Claude → Thomas]** A letter to church leadership explaining the accounts, costs, D-U-N-S, the fee waiver and who signs (build 0.8). **[Thomas + church]** One meeting: approval to publish under the church's name, and the Account Holder, someone with legal signing authority such as the pastor or an administrator, not a volunteer developer. Apple may phone them (0.9).
2. **[Thomas + church]** Confirm the church is a legal entity (Apple doesn't accept DBAs, "doing business as" trade names) with an EIN (its federal tax ID), a public website and an email on its own domain (0.9).
3. **[Thomas + church]** Find the church's IRS determination letter or its denomination's group-exemption letter (0.9). **Foot-gun:** churches aren't required to have a determination letter, but Apple's fee waiver needs nonprofit status "officially recognized" by the IRS. One church reported a stalled waiver for exactly this reason. Without a letter, the church pays $99/yr.
4. **[Thomas + church]** Look up or request a D-U-N-S number with Apple's lookup tool: free, up to 5 business days, plus up to 2 more before Apple sees it (Google says up to 30 days). The name must match the legal entity name exactly (0.10).
5. **[Thomas]** Check that "Seedling" is free as an App Store and Play name and isn't trademarked (R10; build 0.1).

**Personal phase: your Individual account**
6. **[Thomas]** Enroll as an Individual ($99/yr; legal name, street address, an Apple Account with two-factor authentication). A free Personal Team also works, but its builds expire every 7 days (0.2).
7. **[Thomas]** Turn on Developer Mode on the iPhone and register it; Xcode does this on the first run, or use `eas device:create` (0.4).
8. **[Claude]** EAS profiles (EAS: Expo's build-and-submit service): `development` (dev bundle ID `com.<thomas>.seedling.dev`, your team), `beta` and `production` (both the church's `org.<church>.seedling`, on separate update channels), plus the `demo` variant on its own dev-team ID (2.3, 5.16, 8.5). Never upload a build with the production ID from your team.
9. **[Claude]** Data export/import before the switch (8.12). The production app counts as a different app, so the dev build's study data doesn't carry over by itself.

**Before the church beta: the church's Organization team**
10. **[Thomas + church]** Enroll as an Organization with the D-U-N-S, legal name, website and domain email, and take the verification call. Request the fee waiver during enrollment; the church re-confirms eligibility each year, and selling anything ends the waiver. Accept the agreements and invite you as Admin (0.10).
11. **[Thomas, as Admin]** Create the production bundle ID and the App Store Connect app record in the church team (8.3; the dev-team equivalent is 6.6). Turn on the Sign in with Apple capability, then create:
    - a **Services ID** (Apple's ID for the web-style sign-in flow Firebase uses), and
    - a **Sign in with Apple key** (a .p8 file). Paste it into Identity Platform yourself; Claude never handles it.
    - On Google's side, the **OAuth client IDs** (IDs that tell Google's sign-in page which app is asking) for iOS, Android and web.
12. **[Thomas]** App Information, from answer sheets Claude prepares (8.8):
    - **Availability:** United States only, which sidesteps the EU's and other countries' rules at first.
    - **DSA trader status** (the EU Digital Services Act asks every developer): "not a trader".
    - **Age rating questionnaire:** required on every submission since September 2026, including the new social-media questions. Answer honestly for Scripture content; expect 9+ or 13+ (YouVersion's Bible app is 13+). Don't choose the Kids category.
    - **App Privacy label** (the store's privacy "nutrition label"): Email Address, User ID, Other User Content, and Product Interaction if review history syncs. All linked to the user, for App Functionality, with no tracking. Audio isn't collected, because recognition is on-device.
    - **URLs and rights:** privacy policy and support URLs on the church site; content rights note that the BSB is public domain.
13. **[Claude]** Settings App Review checks, in `app.config.ts` (Expo's app config) (8.5; permission wording 3.6):
    - `ios.config.usesNonExemptEncryption: false`. Export compliance: the app's only encryption is the OS's HTTPS, so Apple stops asking on every upload.
    - Privacy manifests (`ios.privacyManifests`) with the "required reason" codes for APIs like UserDefaults, copied from each native package's PrivacyInfo file. Apple emails about missing codes within minutes of an upload.
    - Specific microphone and speech-recognition permission messages; the plugin's generic default risks rejection. **[Thomas]** approves the wording.
14. **[Claude]** Features App Review looks for:
    - The app works with no account (Phases 2–5).
    - In-app account deletion: re-authenticate, revoke the Apple token, delete the Firebase user, purge the server rows, backed by a public web deletion page (6.10).
    - In-app links to the privacy policy, terms and support (5.11; the pages themselves 8.6).
    - Report and block tools plus published contact info for group content (guideline 1.2; 7.7).
    - A Give button that opens Safari and unlocks nothing (8.7).
15. **[Claude → Thomas]** The privacy policy, terms/community guidelines, support page and deletion page as HTML pages (not PDFs) on the church site, under the same entity name as the store listing. **[Thomas + church]** publish them (8.6).
16. **[Claude → Thomas]** **Texas SB2420** (the App Store Accountability Act, enforced since about June 4, 2026): if any testers are in Texas, add expo-age-range before teen accounts exist. It wraps Apple's Declared Age Range and Google's Play Age Signals. **[Thomas + church]** decide; a short attorney review is optional (gate 6.1; 6.9).
17. **TestFlight** (Apple's beta distribution service) (8.11):
    - **Internal testers:** up to 100, no review, but each must be an App Store Connect user on the church team. For you and a co-leader.
    - **External testers:** up to 10,000, invited by email or public link. The first build added to an external group goes through **Beta App Review**, so allow time. Builds expire after 90 days. **[Claude → Thomas]** Claude drafts the Beta App Description, review notes and screenshots; you provide the feedback email and review contact, submit, and answer review messages.
    - Church members join as external testers. **Foot-gun:** don't use EAS "ad hoc" builds for the church; they're capped at 100 iPhones a year.

**Google Play: the church's Organization account, when the Android beta starts**
18. **[Thomas + church]** The church creates the Organization Play Console account and invites you: $25 once, with the D-U-N-S, website and phone. Google doesn't accept prepaid cards and doesn't refund the fee if verification fails. The public listing shows the church's legal name, address, email and phone (8.17).
    - **Why not a personal account:** new personal accounts must verify a physical Android 10+ phone, then run a closed test with at least 12 testers opted in for 14 days straight before going public. Organization accounts are widely reported to be exempt (medium confidence; confirm when creating the account).
19. **[Thomas]** Play forms (8.18): Data safety (mirror the Apple answers, with "encrypted in transit: yes" and "deletion: yes"); the IARC rating questionnaire (the shared international age-rating system); target audience 13+, which keeps the app out of the Families policy; app access (test credentials for reviewers); ads: none; the account-deletion URL.
20. **[Thomas]** Testers through Play internal testing (up to 100), then closed testing through a Google Group (testers need Google accounts). Read the automatic pre-launch report after each upload (8.20).
21. **[Claude]** Keep Play App Signing (EAS's default) and target Android API 36 (SDK 57 already does). Don't lose the upload key. **Foot-gun:** Play re-signs the app with its own certificate, so Google sign-in fails in Play builds until **[Thomas]** adds the Play App Signing SHA-1 (a fingerprint of the signing certificate, which Google checks before allowing sign-in) to the Android OAuth client (8.20).

**Open questions for Thomas:** the church's EIN, IRS letter and signer (gate 0.9); whether any beta testers are in Texas (gate 6.1).

## Development Workflow

_agent-first development_

- dev right in claude code
- determine infrastructure, architecture, scope; no need to be limited anymore because of the capability of AI
- leverage connectors and plugins, e.g.:
- project management tools
- github for PRs
- to whatever database you're using either local or cloud at that time
- Figma UI design
- should be fine to give it access to GCP console, control it with policies
- let it get out of code and look at and view things with specific instructions
    - view its own output, then iterate
- set up a stripe account (simple audit)
    - they have a sandbox you can test payments

**➕ Claude:** What "agent-first" means day to day (research: stack.md, backend.md). Everything here is **Proposed** unless marked otherwise.

**Who does what.** Claude writes the code, tests, infra and drafts, opens PRs and checks its own work. You make the decisions, review and merge PRs, and test on your iPhone. You also handle anything that needs your identity: store consoles, billing, prod and legal text.

### ➕ Tools

| Tool | What Claude does with it | Setup |
|---|---|---|
| Claude Code Desktop + its iOS Simulator pane (public beta) | Builds, launches, taps, types into and screenshots up to 4 simulators per session | **[Thomas]** Xcode 26.4+ with a simulator runtime; approve the one-time consent (build 0.3) |
| Expo MCP (MCP, Model Context Protocol: a standard way to plug tools into Claude) | Screenshots, taps by `testID`, app logs and the route map of the running app | **[Thomas]** the command below. **[Claude]** adds `expo-mcp` as a dev dependency and starts the dev server with `EXPO_UNSTABLE_MCP_SERVER=1`, which turns on the local tools. Simulator only; reconnect after each dev-server restart |
| Maestro MCP (Maestro runs end-to-end UI tests written in YAML) | Writes and runs committed flows (onboarding, a review session, a recitation) on the simulator and the Android emulator | **[Claude]** `maestro mcp` ships with the Maestro CLI 2.11 |
| GitHub CLI (`gh`) | Branches, PRs, issues, the project board and CI logs | **[Thomas]** creates Claude's own GitHub account (a machine user); Claude runs `gh auth login` as it (build 0.7) |
| gcloud, as the dev agent account | Deploys the dev API, reads dev logs, creates test users in dev auth | **[Thomas]** the one-time setup below |
| Terraform | `plan` in `infra/envs/dev` anytime; `apply` there only through the `tf-dev` account, per session | **[Thomas]** runs everything in prod |
| Databases | `sqlite3` on the simulator's `app.db` (path from `xcrun simctl get_app_container booted <bundle id> data`) and on the dev-menu export from your iPhone; `psql` against Postgres.app; dev Cloud SQL through the Cloud SQL Auth Proxy (a local tunnel that signs in with IAM) as the agent account. Never the prod database | No MCP connector needed: the CLIs cover it. Optional later: a read-only MCP for local Postgres |
| Local services | Postgres.app 18.6, the API on your laptop, Vitest, jest-expo and the Python venv | **[Thomas]** installs Postgres.app and Android Studio with an arm64 emulator image |

**One-time setup [Thomas]:**
```
claude mcp add --transport http expo https://mcp.expo.dev/mcp
```
`claude mcp add` registers an MCP server with Claude Code; `--transport http` says it's a remote server reached over HTTPS; `expo` is the name it appears under; the URL is Expo's server. Afterward, run `/mcp` inside Claude Code to sign in to your Expo account.

Simulator screenshots go to Anthropic, so agent-driven simulators hold only `seedling-dev` test accounts and test data (foot-gun at build 2.14). Claude can't drive a physical iPhone; the device loop below covers that.

### ➕ What Claude may and may not touch
Your note "give it access to GCP console, control it with policies", made concrete. Claude doesn't get the console, because a browser session would carry your all-powerful owner login.

**The real wall is which credentials Claude's shell can read.** Claude Code runs commands as your macOS user, so it can read every file your user can. If your owner login sits in gcloud's folder (`~/.config/gcloud`), Claude can use it: switch configurations, drop the impersonation setting, or print an owner token. IAM (Google Cloud's permission system) then sees *you*, the owner of both projects. Claude Code's deny rules are a second line only: they match command prefixes, so a script or `bash -c` slips past them. Google's IAM deny policies would help, but they need a Google Cloud Organization, which you don't have (research: backend.md). Three rules follow:
1. **Your owner login never stays on this Mac user.** Owner and prod work (the bootstrap, prod `plan`/`apply`, prod admin scripts) runs in Cloud Shell (Google's browser terminal, already signed in as you) or from a separate macOS user.
2. **Claude signs in as its own Google identity:** a dedicated Google account (e.g. a new free account named for the agent) that holds no project roles. Its only power is to borrow (impersonate) the two dev service accounts below.
3. **Broad dev rights are borrowed per session,** through a time-limited grant you add.

| Identity | Can do | How Claude gets it |
|---|---|---|
| You (owner of both projects) | Everything | Never available to Claude: Cloud Shell or another macOS user |
| Agent Google account | Nothing by itself; Token Creator (the right to borrow) on `claude-agent` | Signed in inside Claude's own gcloud folder (below) |
| `claude-agent@seedling-dev` (a service account: a non-human Google identity) | Deploy to dev Cloud Run, push images, connect to the dev DB, read logs, create test users | Always, by impersonation; no key file |
| `tf-dev@seedling-dev` | Broader dev roles, enough for `terraform apply` to create Firebase, Identity Platform and Cloud SQL. No prod roles and no IAM-admin role, so it can't grant itself more | Only while your time-limited grant lasts |
| Deployer and runtime accounts | CI deploys and the running API | Never Claude (App Architecture §13) |

| Area | Claude may | Claude may not |
|---|---|---|
| Repo | Create branches, commit, push branches, open PRs, run tests and CI | Merge, push to `main`, force-push, change branch protection, start workflows by hand |
| `seedling-dev` | Deploy the API, read logs, create test users, `terraform plan`; `terraform apply` in `envs/dev` through `tf-dev` during a granted session | Grant itself roles, read secret values |
| `seedling-prod` | Nothing: no roles, no access to the prod state bucket | Any gcloud or Terraform command. Prod deploys go through GitHub Actions after your approval; you run prod `terraform apply` |
| Releases | Dev builds; `eas build --profile beta` | `eas submit`, `eas update` on the `beta` or `production` channel, `eas build --profile production`. You publish what testers and users get |
| Data | Test data, fixtures, the Python generator's output | The prod database or real users' data. Beta logs for R&D arrive as an anonymized export you make |
| Store consoles, Apple portal, billing | Draft text, answers and screenshots | Sign in, submit, accept agreements, pay |
| Keys | Reference secrets by name in config | Handle .p8 or JSON key files, or commit any credential |

**Foot-gun: deny rules are a tripwire, not a wall.** On GitHub the wall is Claude's own machine-user account (build 0.7) plus branch protection that requires your approving review (0.14), so GitHub itself blocks Claude merging its own PRs (which needs a public repo or a paid plan: gate 0.6). EAS has no such wall while Claude shares your Expo login, so `eas submit` and `eas update` to `beta`/`production` rest on the deny rules (a separate Expo account with a limited role may work, but wasn't researched). Deny rules (build 0.12) cover at least: prod `gcloud`, `terraform -chdir=infra/envs/prod`, pushes to `main`, force-pushes, `gh pr merge`, `gh workflow run`, `eas submit`, `eas update --channel beta|production`, `eas build --profile production`, and reads of `~/.config/gcloud` (Claude Code's sandbox can block that folder).

**How the impersonation works (one-time, [Thomas]; scheduled at build 6.4).** Impersonation means one identity borrows a short-lived token for a service account, like a session token minted from a login; no key file exists to leak. In a terminal on the Mac:
```
export CLOUDSDK_CONFIG="$HOME/.config/gcloud-seedling-agent"
gcloud auth login
gcloud config set auth/impersonate_service_account claude-agent@seedling-dev.iam.gserviceaccount.com
gcloud config set project seedling-dev
gcloud auth application-default login --impersonate-service-account claude-agent@seedling-dev.iam.gserviceaccount.com
```
- `CLOUDSDK_CONFIG` points gcloud at a separate folder, like a separate home directory for its logins and settings. Claude's folder never holds your owner login.
- `gcloud auth login` opens a browser. **Sign in as the agent Google account, not yours** (use a private window; the browser tends to pick your main account).
- `auth/impersonate_service_account` makes every gcloud command borrow a `claude-agent` token instead of acting as the agent account itself.
- `project` points it at dev.
- `application-default login` writes ADC (Application Default Credentials: the credential file that libraries such as Terraform and firebase-admin read, separate from gcloud's own login), impersonating the same account.
- Claude Code's `.claude/settings.json` sets `CLOUDSDK_CONFIG` to that folder's full path and `GOOGLE_APPLICATION_CREDENTIALS` to the ADC file inside it (`application_default_credentials.json`), which tells every library exactly which credential file to use. Your own terminal keeps its normal settings.
- If your owner account was ever signed in on this Mac user, sign it out of the default folder: `gcloud auth revoke --all` removes gcloud's saved logins, and `gcloud auth application-default revoke` removes the default ADC file.

**A `tf-dev` session ([Thomas], in Cloud Shell, when a dev apply is planned):**
```
gcloud iam service-accounts add-iam-policy-binding tf-dev@seedling-dev.iam.gserviceaccount.com \
  --member=serviceAccount:claude-agent@seedling-dev.iam.gserviceaccount.com \
  --role=roles/iam.serviceAccountTokenCreator \
  --condition='expression=request.time < timestamp("2026-11-01T02:00:00Z"),title=tf-dev-session'
```
- `add-iam-policy-binding` grants a role on one service account (`tf-dev`) rather than on the whole project.
- `--member` is who receives it: the `claude-agent` service account, the identity Claude already acts as, so Claude borrows `tf-dev` through it (a chained impersonation).
- `--role` is Token Creator, the right to borrow.
- `--condition` is an IAM condition: the grant stops working at that UTC time, so it can't outlive the session. Set it a few hours out.

Claude then runs Terraform with `GOOGLE_IMPERSONATE_SERVICE_ACCOUNT=tf-dev@seedling-dev.iam.gserviceaccount.com`, which tells the Google provider to borrow `tf-dev`. Expired grants can be deleted later with `remove-iam-policy-binding`.

**Check (build 6.4's done-when).** From Claude's shell: `gcloud auth list` shows only the agent account; the ADC identity is `claude-agent`; and `gcloud projects describe seedling-prod` fails under every configuration.

### ➕ Local dev setup (your notes under "Optimize Claude cost")
- **Dev API on your laptop:** yes. The Hono API and Postgres.app 18 run locally once sync work starts, with ADC impersonating the agent account so firebase-admin works against `seedling-dev`. The personal phase needs no backend at all.
- **Dev mode on your phone:** yes, as a development build (your own app binary with Expo's dev menu), not Expo Go. JS changes reload over Wi-Fi; only native changes need a rebuild.
- **Auth:** real Firebase Auth from `seedling-dev`, not prod. Tokens verify the same way, so nothing is mocked, and test accounts never mix with church members' accounts.

### ➕ Branches, PRs and repo memory
- **Branches:** `main` is protected. Each issue gets its own branch (`<issue#>-<slug>`) and one PR that closes it. Claude never merges.
- **Foot-gun: GitHub plan limits** (from GitHub's documentation, not the research files). On the Free plan a private repo gets no branch protection, and an Environment's required reviewers (the prod-deploy approval below) on a private repo need GitHub Enterprise. A private repo on Free would silently have neither: no protected `main` and no approval gate before prod. Choose public, or a paid plan plus a prod path only you can trigger (gate 0.6). A required CI check can only be selected after it has run once, so protection is switched on after CI exists.
- **PRs:** small enough to review in one sitting. Each PR body says what changed and how Claude verified it (tests run, screenshots). If the change needs your iPhone, it includes a device test script.
- **CI (GitHub Actions) on every PR:** typecheck, lint, Vitest, jest-expo, the golden parity tests (the TS engine against the committed golden JSON from the Python generator) and a golden freshness check (each golden records a hash of the Python sources and passage files that made it, and CI fails if they changed without a re-export). CI can't run the Python itself, because `bible.eng.db` is git-ignored; Python tests run on the Mac. Prod deploys run only from `main`, through a GitHub Environment that waits for your approval, and authenticate with Workload Identity Federation (GitHub proves its identity to Google, so no stored keys).
- **Repo memory:** a short root `CLAUDE.md` holds what the project is, the commands, and the hard rules: `npx expo install`, TypeScript 6, no prod, a `testID` on every interactive element, never show users "card", "deck" or "FSRS". Each package (`apps/mobile`, `apps/api`, `packages/*`, `infra`) gets its own CLAUDE.md with its commands, invariants and tests. Claude Code loads a folder's CLAUDE.md only when it works in that folder.
- **Plans in the repo:** before each phase, Claude writes `docs/plans/phase-N.md` with the steps, "done when" checklists and gate options. Decisions go into `docs/decisions.md`. A new session reads the plan instead of rebuilding context from chat.

### ➕ Device-testing loop (your iPhone)
Some things only work on a real phone: speech recognition (broken in iOS 26.4+ simulators), Sign in with Apple (errors on the simulator), haptics, widgets, and microphone noise in a real room.
1. **[Claude]** Finishes the PR and writes a numbered device test script: the steps and what you should see.
2. **[Thomas]** Plugs in and unlocks the iPhone. **[Claude]** runs `npx expo run:ios --device`: `run:ios` compiles the native app with Xcode on your Mac, and `--device` installs it on the connected iPhone instead of a simulator. No EAS quota is used. After that, JS-only changes reload over Wi-Fi.
3. **[Thomas]** Reports pass or fail per step, with a screenshot or screen recording. For STT, export the text-only recognition log from the dev menu; audio is never saved.
4. **[Claude]** Turns each failure into an automated test (an STT log becomes a replay fixture), then fixes it.

Dictation must be on for on-device recognition (build 0.4).

### ➕ Self-check loops by work type
What "view its own output, then iterate" means for each kind of work. Every loop ends at a stop criterion: the work is done, or Claude asks you.

| Work | Loop | Done when | Stop and ask when |
|---|---|---|---|
| UI | Build → screenshot in the simulator pane at default and largest text size, light and dark → check against the plan's UI checklist (R13: verse text ≥ 20 pt, buttons ≥ 56 pt, contrast, no swipe-only actions, plain-language labels) → fix | The checklist and the Maestro flow pass | 3 iterations without passing, or a taste call (color, layout, tone) |
| Engine (`engine`, `recite`, `plant`) | Write a failing Vitest test from the spec or golden JSON → implement → run → check parity with the goldens | All tests and parity pass, and the plant is deterministic (same seed, same plant) | The spec is ambiguous, or 2 attempts on the same test fail |
| STT | Replay recorded text-only logs through the aligner → fix → hand off a device test script | The replay suite is green and your device run passes | Anything needs a real microphone |
| API | Integration tests against local Postgres → deploy to dev → smoke test with a dev test token | The tests and the smoke test pass | A schema migration would drop or rewrite data |
| Infra | `terraform fmt`, `validate`, `plan` in dev → read the plan → apply in dev (in a `tf-dev` session) → smoke test → open a PR for the prod change; you run the prod plan and paste only its summary, never the raw plan on a public repo (build 6.14) | Dev applies cleanly | A plan destroys or replaces a stateful resource (the database or a state bucket), or touches IAM or prod |

### ➕ Other notes on your list
- **Figma:** optional (decision 12). If you sketch something there, Claude works from an exported image, so no connector is needed.
- **Stripe sandbox:** not needed; Stripe is dropped (R2).
- **"No need to be limited anymore":** agreed on capability. At 5–10 hours a week, though, your review time is the bottleneck, so phases stay small and each ends in something you can use.

### ➕ Project management
- **GitHub Issues + a GitHub Project board** (Backlog → Ready → In progress → In review → Done). No extra tool, no cost.
- **The build phases are the backlog:** each phase is a milestone, each step an issue labeled `claude` or `thomas` and titled with its step ID. Claude creates them with `gh` and links PRs with "Closes #N".
- **Your queue** is the `thomas` label plus PRs waiting for review. A 15-minute weekly check-in picks the next issues.

**Open question for Thomas:** public or private repo (gate 0.6)? Public gets unlimited free Actions minutes and branch protection on the Free plan, but makes the trial notes and data files visible; private on Free gets 2,000 minutes a month and loses both safeguards above.

### Optimize Claude cost

Example optimizations:

- have opus plan the app and create a spec, pass it off to sonnet to build the pieces, then have opus 5.5 on high review
  ui specific task
- explicity define a reinforcement learning loop for agent to produce work and check its own output, such as designing a ui, then viewing the ui, then adjusting, etc.:
- e.g., expo -> review it's own work based on business specs for UI/UX:
- can create a dev API backend on your laptop
- have expo put it to dev mode on your phone
- might be too much local machine setup to mock auth for dev, so likely just use GCP prod auth

**➕ Claude:** Your plan holds: Opus plans and reviews, Sonnet builds. On a subscription, "cost" means how fast you hit usage limits. Sonnet uses noticeably less than Opus for the same work, and Haiku far less (exact API prices weren't part of this research). Your last three bullets (laptop API, dev mode on the phone, auth) are answered under Development Workflow → Local dev setup.

#### ➕ Model routing

| Work | Model | Why |
|---|---|---|
| Phase plans, architecture changes, spec questions | Opus 5.5, high effort | Mistakes here multiply |
| Phase-end review, and high-risk code (auth, account deletion, sync, IAM and Terraform, the scheduler, the aligner, the privacy gate) | Opus 5.5, high effort | Subtle bugs hide here |
| Stuck debugging, after 2 failed Sonnet attempts | Opus 5.5 | Cheaper than a third blind attempt |
| Building from a written plan: features, tests, UI iterations, Terraform modules | Sonnet 5.5 | Most tokens go here, and the plan already did the hard thinking |
| Mechanical chores: renames, formatting, fixes from `npx expo install --check`, issues from a plan, changelogs, log summaries, code search | Haiku 5.5 | Cheap and low risk; tests and CI catch mistakes |

`/model` switches a session's model. Subagents (helper agents defined in `.claude/agents/*.md`) can pin `model: haiku` or `model: sonnet`, so an Opus or Sonnet session can hand chores to a cheaper helper.

#### ➕ Multi-agent workflows only when warranted
- The default is one session, one issue, one branch.
- Use parallel agents only for independent pieces: a research fan-out (how this spec was researched), or the engine and the API once their shared zod schemas exist. Each agent re-reads context and needs coordinating, so parallel runs cost more in total.
- Never put two agents on the same files. Parallel agents work in separate git worktrees (extra checkouts of the same repo, each on its own branch).

#### ➕ Context hygiene
- Per-package CLAUDE.md files keep each session's standing instructions small; the root file stays short.
- A fresh session per issue. The plan file carries state between sessions, not a long chat.
- Point Claude at exact files and the plan step, not "look around the repo".
- The root CLAUDE.md tells Claude never to open bulky files whole (`data/`, `output/`, the BSB asset, golden JSON); it queries them with scripts or reads a line range.

#### ➕ Free checks before expensive review
Cheap checks first, in this order:
1. Typecheck and lint.
2. Vitest and jest-expo.
3. Golden parity and freshness.
4. Maestro flows and the simulator screenshot loop.
5. CI on the PR.
6. Only then, an Opus review.

A Claude Code hook (a command the harness runs automatically after each edit) can run the typecheck, so errors surface at once.

#### ➕ Self-check loops with stop criteria
Your "reinforcement learning loop" is a feedback loop: produce, check, adjust. Reinforcement learning proper trains a model, and nothing is trained here. Rules for every task:
- The plan step states "done when" before work starts.
- After at most 3 UI iterations, Claude stops and shows you the screenshots.
- After at most 2 failed fixes for the same failure, Claude writes up what it tried and escalates to Opus or asks you.
- Claude never weakens a test, deletes an assertion or edits golden files to make tests pass without asking.
- Claude stops at once for anything involving prod, secrets, money, store submissions, legal text or a destructive Terraform plan.

The per-work-type loops are in Development Workflow → Self-check loops by work type.

#### ➕ /code-review at phase end
- At the end of each phase, Opus 5.5 runs `/code-review high` over the phase's merged changes, plus `/security-review` for phases touching the privacy gate, auth, sync, deletion, user content or release config (Phases 3, 6, 7, 8a and 8b). Findings become issues for Sonnet to fix.
- You and CI review each PR. High-risk PRs (auth, deletion, sync, IAM, the privacy gate) also get an Opus review before merge.

## App Architecture

- How the app will be structured and function and how to codebase will be organized and and overview of what it will consist of

**➕ Claude:** Seedling is a local-first Expo app built on four pure-TypeScript packages, plus a small Cloud Run API for backup, sync and groups. The existing Python stays where it is: it becomes the content pipeline and the reference implementation that the TypeScript port is tested against. **Decided** means your decisions, the R-items (my resolutions from the research, which stand unless you override them) or verified facts; **Proposed** means my extrapolation for you to confirm. §§1–2 and §17 are the summary; §§3–16 are the detailed reference that Build Phases cites by number. Versions come from the 2026-10-14 research files.

### ➕ 1. Overview

```
 iPHONE / ANDROID: local-first, works offline, no account     GOOGLE CLOUD: only after sign-in
┌───────────────────────────────────────────────────────────┐  sign in  ┌───────────────────────┐
│ apps/mobile: expo-router screens · Skia plant · widget    │──────────►│ Identity Platform     │
│     │ live queries          │ session         │ renders   │◄──────────│ (Firebase Auth)       │
│     ▼                       ▼                 ▼           │  ID token └───────────────────────┘
│ engine                 recite             plant           │
│ compile · release ·    normalize ·        growPlant       │ HTTPS + ID token ┌──────────────┐
│ schedule (ts-fsrs) ·   align · grade      (PlantInput)    │─────────────────►│ Cloud Run    │
│ session · mastery         ▲                               │◄─────────────────│ apps/api     │
│     │                     │ text hypotheses only          │ /v1/sync/push    │ (Hono)       │
│     │           STT engine (on-device) ◄── mic            │ /v1/sync/pull    └──────┬───────┘
│     ▼                                                     │ /v1/me /v1/groups       │ IAM login
│ app.db (SQLite + Drizzle): review_events · cards ·        │                         ▼
│   attempts · outbox · plant · settings · pasted_text      │          ┌────────────────────────┐
│ bsb.sqlite: the whole BSB + red-letter table (read-only)  │          │ Cloud SQL Postgres 18  │
│ texts.db: downloaded translations and commentary          │          └────────────────────────┘
└───────┬────────────────────────────────────────┬──────────┘
        ▲ bundled into each build                └──► bible.helloao.org: anonymous GETs, each
        │                                             feature only after its consent prompt
 CONTENT PIPELINE (Python, this repo, runs on the Mac)
 data/bible.eng.db + data/passages/*.yml ─► src/content/ ─► bsb.sqlite · passage bundles (JSON)
                                                          · fixtures/golden/*.json (parity tests)
```

**Local-first** (the phone's own database is the source of truth; the cloud is only a backup and a meeting place for groups). Studying, grading, scheduling, recitation and the plant all work in airplane mode with no account. Signing in adds backup/sync, a second device and groups.

**Network rule** (Decided: R3): the app makes no network calls until the user opts in. Two kinds of opt-in exist (Proposed):
- **Account.** "Back up my progress" or "Join a group" (§10). Only this reaches Seedling's servers.
- **Per-feature consent.** Study helps and translation downloads are anonymous GETs to helloao (no account, no identifiers; helloao sees the IP address and the chapter). Each feature asks once on first use ("Study helps download free notes from an online Bible library. Nothing about you is sent. Download?"), and that answer is the R3 opt-in for that feature.
- **Known under-13 users get neither.** "Known" means the user answered the age screen as under 13, or expo-age-range reports it. The age screen appears only at account opt-in (§10), so a local-only user who never tries to sign up has no known age and sees the consent prompts like anyone else.

| Where | What lives there |
|---|---|
| Device | All study data and logic: passages, cards, review history, trails, plant, settings, pasted text, the BSB |
| Cloud Run API | A stateless check-the-token-then-read/write layer: sync log, account, groups. Holds no study logic |
| Postgres | Users, the append-only review-event log, small last-writer-wins records, groups, mastery bitsets |
| Identity Platform (Firebase Auth's upgraded tier) | Sign-in identities (Apple, Google) and ID tokens (short-lived signed proofs of who the user is) |
| Python on the Mac | Runs at build time only: exports bundles, `bsb.sqlite` and golden files (saved known-good outputs the TypeScript port must reproduce) |
| bible.helloao.org | Optional downloads of commentaries and other translations, after consent |

The personal phase needs no cloud at all ($0). The API and Postgres arrive with sync in Phase 6 (research: backend.md).

### ➕ 2. Repo layout

A **monorepo** (several apps and libraries in one git repo) using **pnpm workspaces** (pnpm links the local packages to each other, so the app imports `@seedling/engine` as if it came from npm). Decided: decision 6 and R16.

```
bible-flashcards/
├── CLAUDE.md               agent guide: commands, rules ("npx expo install", no prod access)
├── package.json            root scripts (typecheck, lint, test, parity) and engines (Node 22/24)
├── pnpm-workspace.yaml     workspace globs, nodeLinker, allowBuilds (pnpm 11+ settings live here)
├── tsconfig.base.json      shared strict settings; TypeScript ~6.0.3 (not 7)
├── .github/workflows/      ci.yml, api-deploy.yml, eas.yml
├── .claude/                app-requirements/ (this spec + research/), settings.json (agent env + deny rules)
├── apps/
│   ├── mobile/             the Expo app
│   │   ├── app/            expo-router screens (one file per route)
│   │   ├── src/            db/, sync/, stt/ (engine adapters), auth/, content/, session/, ui/
│   │   ├── modules/        local Expo modules in Swift/Kotlin (speech-analyzer in v1.5)
│   │   ├── assets/         bsb.sqlite, bundles/, fonts, leaf sprites
│   │   ├── drizzle/        generated SQLite migrations
│   │   ├── e2e/            Maestro flows
│   │   └── CLAUDE.md       app rules: testIDs, Dynamic Type, no secrets in app.config
│   └── api/                Cloud Run service: Hono, pg, firebase-admin, Dockerfile
│       └── CLAUDE.md       API rules: zod on every route, never log bodies, additive migrations
├── packages/               pure TypeScript, no React Native imports, Vitest
│   ├── engine/             compile, release, schedule, session, grade, mastery
│   ├── recite/             STT interface, normalizer, aligner, word states, replay
│   ├── plant/              seeded plant generator
│   ├── shared/             zod schemas: bundle format, card keys, API and sync types
│   └── CLAUDE.md           the purity rule
├── infra/                  Terraform: bootstrap/, modules/, envs/dev, envs/prod
│   └── CLAUDE.md           prod is Thomas-only; agent works in envs/dev
├── fixtures/               golden/ (Python → TS parity), stt/ (text-only hypothesis logs)
├── src/                    existing Python
│   ├── deck/               sequence-v2 generator and Anki export (the reference)
│   └── content/            NEW exporter: passage bundles, bsb.sqlite, goldens
├── scripts/  tests/        existing Python tools (simulate_fsrs.py …) and unittest
├── data/                   outlines/ (trials), passages/ (NEW curated passages), bible.eng.db, README.md
└── notes/  output/  docs/  design notes, trial output; docs/ holds decisions.md, plans/, runbooks/
```

`data/bible.eng.db` (2.6 GB) stays git-ignored. CI can't run the Python exporter, so its outputs (bundles, `bsb.sqlite`, goldens) are committed and CI tests against them. This is the part people get wrong: change Python, then forget to re-export and commit (§12's freshness check catches it).

### ➕ 3. Packages and contracts

| Package | Owns | Depends on |
|---|---|---|
| `shared` | zod schemas (runtime-checked types) for the bundle format, card keys, sync and API payloads; verse-id helpers | zod 4.6 |
| `engine` | compile, release planner, scheduler adapter, session builder, grader, mastery, recompile diff | shared, ts-fsrs ^5.4.2 |
| `recite` | `SttEngine` interface, privacy-gate policy, normalizer, aligner, word states, trail encoding, replay engine | shared, double-metaphone 2.0.1, fastest-levenshtein 1.0.16, to-words 7.1 |
| `plant` | `growPlant`, seeded PRNG and hash, renderVersions | shared |

```ts
type VerseId = number;      // book order×1,000,000 + chapter×1,000 + verse: Matt 5:3 = 40005003
type CardKey = string;      // "som:header-to-text:40005021-40005023" (§4)
type Rating = 1 | 2 | 3 | 4;   // Again, Hard, Good, Easy (ts-fsrs)

// engine
compile(bundle: PassageBundle, opts?: CompileOpts): Compiled   // nodes, units, cards, groups
planToday(c: Compiled, intro: IntroHistory, today: LocalDay, pace: number): Group[]
buildSession(due: CardState[], newGroups: Group[], opts: SessionOpts): SessionQueue
grade(kind: CardKind, a: Attempt): { auto: Rating; reasons: string[] }
mastery(c: Compiled, states: Map<CardKey, CardState>, now: Date): VerseMastery[]
diffCompiled(prev: Compiled, next: Compiled): Record<'keep' | 'reset' | 'retire' | 'add', CardKey[]>
interface Scheduler {
  review(s: CardState | null, r: Rating, at: Date): CardState;
  retrievability(s: CardState, at: Date): number;
}
// recite and plant
createAligner(tokens: Token[]): { push(h: Hyp): WordState[]; finish(): AlignResult }
growPlant(input: PlantInput): PlantGeometry
```

**Cards are data, not HTML** (Decided: R8). A `CardSpec` says what to show, hide, blank or dim, which map node to focus, and which verses the answer covers. React components draw it. The Python generator's HTML stays for Anki only.

**The purity rule** (Decided: R16). Nothing in `packages/` imports `react`, `react-native` or `expo-*`, reads the clock or calls `Math.random`. Time and seeds are passed in. An ESLint import rule enforces it, and Vitest 5 (a fast TypeScript test runner) runs the packages in plain Node in milliseconds. That is why Claude can test the hard logic (scheduling, alignment, plant geometry) without a phone.

**How the app consumes them** (Proposed). Each package is a workspace dependency (`"@seedling/engine": "workspace:*"`) that ships TypeScript source with no build step. Metro (the React Native bundler) compiles it with the app, Vitest runs it directly, and the API's esbuild bundle inlines `shared`. Native STT adapters live in `apps/mobile/src/stt/` and implement `recite`'s `SttEngine`.

### ➕ 4. Learning-engine pipeline

```
bundle ─compile─► Compiled (cards + release groups) ─planToday(today, pace)─► today's new groups
due card states + today's new groups ─buildSession─► queue ─► Attempt ─grade─► Rating
Rating ─ts-fsrs─► review_event ─► card states ─mastery─► verse_mastery ─► plant, group bitset
```

- **compile** (Decided: R8). A port of `src/deck/tree.py`, `cards.py` and `order.py`'s grouping: outline → nodes → units (80-word target, 130 max, cut at paragraph breaks, computed per outline leaf) → the 14 card kinds of sequence v2, with the Python slugs kept as `CardKind` (`read-through` … `section-header-to-text`). It also closes the generator gaps from R8: collections of several passages across books, BSB's 19 missing verses, passages with no outline (one leaf, no Phase 1 cards), and the `report()` crash. The fixes land in Python first, so the goldens cover them.
- **Release groups** keep the Python grouping: `intro` (Read-through + Preview + Outline clozes of one family), `list-parts`, `whole-outline`, `wave-1/2/3` of a unit, `closing` and `recite` of a section. Each group carries its wait: "the day after group X was introduced" (waves, List the parts, Whole outline, section recite) or "as soon as X is done" (section closing).
- **schedule.** One FSRS item per card behind the `Scheduler` interface, so the per-unit memory-state model (later R&D) can replace it without touching the UI (Decided: decision 7).
- **session** (Proposed). Due reviews first, lowest retrievability first, then today's new groups in plan order. A 10-minute learning step re-queues an Again within the session. After 3+ days away, a catch-up session is capped at 10 minutes, waters the thirstiest leaves first and adds no new groups (R12). Time estimates start from `simulate_fsrs.py`'s seconds per card kind, then use the user's own durations.
- **mastery** (Decided: R8, R11). The **governing card** for a verse is its unit's Header→text card; scaffold cards never move a leaf, so leaves don't flicker as scaffolds fall due. Stages: bud (any card for the verse introduced), leaf (Header→text graduated), full leaf (stability ≥ 7 days), rooted (stability ≥ 21 days). **Stability** is the number of days until recall odds fall to 90%; **retrievability** (R) is today's recall odds. A verse in two passages takes the higher stability.

**The grading rule** (Decided: R7; thresholds from trial 2's type mode, `notes/sequence_v2_draft.md` and `src/deck/assets/card.js`). This table is the single source of truth: Features' "How this was graded" footer and Build 1.12's table-driven tests both cite it. Every recall card yields an `Attempt` {mode: voice | type | selfcheck, wordsTotal, matched, close, missed, longestMissedRun, hintsUsed, peeks, hesitations, durationMs}.

| Suggested grade | When |
|---|---|
| **Again** | a hint was used, a peek was taken ("Show me" before finishing a voice or typed attempt), or 2+ words were missed |
| **Good** | 0 words missed, at most 1 close, no hints, fewer than 2 hesitations |
| **Hard** | everything else (e.g. 1 word missed, or 2+ close, or 2+ hesitations). A failed recall is never Hard |
| **Easy** | only Read-through and Preview (always), and Fill in the blanks / First letters at 100% (nothing missed or close, no hints, no hesitations) |

- **Close**: in voice mode, a sound-alike or near-spelling (§5); in type mode, a word typed right after one wrong letter (two wrong letters make it missed). In self-check mode the user taps the words they missed; there is no "close".
- **Hesitation**: a long pause before a word; the threshold is set in the Phase 1 plan and calibrated in Phase 5. Hesitations can lower Good to Hard, never to Again.
- For outline cards the "words" are the headers. `longestMissedRun` is logged for calibration only.
- The user confirms or overrides with one tap; both `autoRating` and `finalRating` are logged.

**Card keys that survive versions and shared passages** (Proposed). A key names *what is asked*, by verse range, never by position or outline version, under an **outline family** id rather than a passage id:
- A **family** is one outline tree that several curated passages can share. The Farewell Discourse whole and its three parts are one family (`farewell`); Psalm 23 and Psalms of Trust both use the `psalms` family, where each psalm is a node. A passage in a shared family references the family's nodes instead of carrying its own outline, so compile yields identical units and identical keys for the shared parts.
- Depth in a key is depth in the family tree, so Psalm 23 has the same keys alone or inside Psalms of Trust.
- A node that exists in only one passage (a collection's own root) is keyed under that passage's id.
- **Custom and group passages** each get their own family, so they never share cards with curated ones, even when they overlap. A verse in both still shows one leaf, using the higher stability (above).
- **The release planner skips any card whose key is already introduced** through another enrollment. Enrolling in Farewell part 1 and then the whole adds no duplicate cards for the shared units, and Psalms of Trust re-introduces no Psalm 23 card.

| Card is about | Key shape | Example |
|---|---|---|
| a header (node) | `family:kind:start-end.depth` | `som:outline-cloze:40005027-40005030.3` |
| a unit | `family:kind:start-end` | `som:header-to-text:40005021-40005023` |
| one verse of a unit | `…:unit-range:verse` | `som:scaffolded-cloze:40005021-40005023:40005022` |
| one part of a section | `…:node-anchor:part-range` | `som:missing-section:40005003-40005016.1:40005006-40005008` |

Siblings split their parent's range, so a range plus a depth is unique within a family. Python gets the same key function, so goldens compare key for key. Each card also stores a `contentHash` of its cue and answer: for text cards the verse text; for header cards the node's own title and its children's titles, never the surrounding map, so a shared node hashes the same in every passage. Keys become permanent once Thomas's review events exist (Phase 2), so this scheme is fixed in Build 1.1's plan.

**Calendar-day release replaces "N cards later"** (Decided: R8; details Proposed). Anki introduces exactly N new cards a day, so the generator had to fake "a day later" as "N cards later". The app knows real dates:
- A group becomes eligible on the local day after the group it waits on was *introduced*. The day rolls over at 4 a.m. local (Anki's default), so late-night study counts as that day.
- Each day the planner offers eligible groups in the Python priority order: released groups oldest first, then the next Phase 1 family, then the next unit's wave 1 if fewer than 2 units are in waves 1–2.
- Groups are introduced whole; the day stops once its new-card count reaches **pace**.
- The Python rule "if nothing is ready, pull a group forward" is dropped. A light day is better than a broken day gap.
- Missed days create no backlog of new cards: waves simply wait.

**Pace** = new cards per day. Presets Gentle 6 / Steady 12 / Ambitious 18; the default is gate 5.2 (Proposed: Gentle). The UI labels paces in days and minutes, never cards. Steady (12) is the trial pace (sequence v2 §5).

**Versioning** (Proposed). `generatorVersion` (e.g. `seq-v2.1`) names the ladder rules; `outlineVersion` is an integer per passage, and each version is immutable. An enrollment records both. When an outline changes mid-study (edited by the user or a group leader, or updated in an app release or OTA), the engine compiles the old and new versions and runs `diffCompiled`:
- **keep**: same key, same hash → history and schedule continue.
- **reset**: same key, new hash → a `reset` event; the card starts over as new. A renamed header resets only its header cards.
- **retire**: key gone → no longer scheduled; its events stay in the log.
- **add**: new keys → released by the planner as usual. Moving a unit boundary retires that unit's text cards and adds new ones.

A `generatorVersion` upgrade goes through the same diff, so old compile rules never need to stay runnable. Review events are never deleted.

**Content upgrade on launch** (Proposed). On every app start, including after an OTA, the app compares each enrollment's `outlineVersion` and `generatorVersion` with the bundled ones. For each newer one it runs the diff and writes the reset/retire events plus the enrollment bump in one exclusive transaction (§8). It also replaces `bsb.sqlite` when the hash in `index.json` changes. Without this step, an edited curated outline (e.g. Psalm 23 re-authored in Phase 5 while Thomas studies it) silently breaks progress.

**FSRS configuration** (Decided: R8 and sequence v2 §6):

```ts
const params = generatorParameters({
  request_retention: 0.9,          // desired retention
  learning_steps: ['10m'],         // one step: the ladder already repeats same-day
  relearning_steps: ['10m'],
  enable_short_term: true,
  enable_fuzz: true,               // spreads due dates; see the replay rule
});                                // w = FSRS-6 defaults (21 weights) until optimized
```

**Fuzz** (a small random shift in each due date that stops reviews bunching up) makes a replay non-reproducible. So each review event stores its post-review snapshot (due, stability, difficulty, state), and that snapshot is the truth. Replays use fuzz off. Optimized weights come later from py-fsrs's optimizer, run offline in Python on exported events; they reach the device through sync and are zod-validated before use (Decided: R8).

**Parity tests against Python goldens** (Decided: R8; scope Proposed). `python -m src.content goldens` writes `fixtures/golden/<passage>.json`: the bundle, every `CardSpec` (key, kind, phase, verses, hide/show pattern, hash) and the group order. Vitest checks:
- **compile:** exact match, card for card.
- **release:** invariants, not identical days, because the app never pulls a group forward: every wave at least a day after the previous one, at most 2 units in waves 1–2, all of Phase 1 released before Phase 2, sections closing after their units. Total days must be close to Python's.
- **FSRS:** fixed rating sequences replayed in ts-fsrs and py-fsrs (`enable_fuzzing=False`) must give the same stability, difficulty and due within a small tolerance.

### ➕ 5. Recitation pipeline

```
mic ─► SttEngine (on-device) ─Hyp─► normalize ─► align ─► word states ─► trail on screen
                                                           └─► finish() ─► Attempt ─► grade
```

- **Engine interface** (Decided: R6). `SttEngine { id; probe(locale); prepare(locale); start({locale, biasPhrases, sessionId}); stop(); abort(); onHypothesis(cb); onLevel(cb); onError(cb) }`. A hypothesis (`Hyp`) is `{sessionId, segmentId, text, isFinal, alts?, words?, at}`. Every adapter emits "replace segment N": a new partial replaces the last one, `isFinal` freezes it, and the next speech becomes N+1. That one rule absorbs each OS's quirks: the growing transcript, iOS 18's reset after a pause, Android's chunked sessions and SpeechAnalyzer's tentative-then-final results. Engines: `ios-sfspeech` (v1, expo-speech-recognition 57.1.x), `ios-analyzer` (v1.5, local Swift module, iOS 26+), `android-ondevice`, `sherpa` (later), `replay` (tests) (research: stt.md).
- **Privacy gate** (Decided: R6). `start()` refuses unless `probe()` reports on-device recognition. iOS: `supportsOnDeviceRecognition()` is true. Android: API 33+ and `getSupportedLocales()` lists the locale as installed; otherwise the app offers the model download or falls back to typing. Android 12 and older has no on-device path in this library, so voice is off there. This is the part people get wrong: the library otherwise ignores `requiresOnDeviceRecognition` silently and may send audio to a server. If the check fails, voice mode is off and the card offers typing or self-check. `recordingOptions.persist` is never set, so no audio file is ever written. Both adapters get the same refusal test.
- **Normalizer.** Each passage word becomes `{display, norm, phon, verseId, lineIdx, aliases}`, where `phon` holds two Double Metaphone codes (a sound-alike encoding, so "Zebulun" and "Zebulon" match). Rules: lowercase; strip punctuation; curly quotes to ASCII; split em-dashes and hyphens (keeping the hyphenated form as an alias); numerals to words ("46,500" → "forty six thousand five hundred", digits kept as an alias); "LORD" → "lord"; contractions expanded. Hypotheses go through the same function, with fillers ("um") dropped. Proper nouns (≤100, 1–2 words each) become `biasPhrases`. Never bias with the whole verse: that flatters the user.
- **Aligner** (pure TS). It keeps a `frontier` (the furthest confirmed word) and aligns the current segment against a window of the passage from 15 words behind to 40 ahead. Scoring: a weighted edit distance where exact, alias and sound-alike matches are free, near-spellings (Levenshtein ratio ≥ 0.8; 0.7 for proper nouns) cost 0.3, a skipped passage word 1.0 and an extra spoken word 0.6. Two spoken words may match one passage word, and the reverse ("Melchi zedek"). If under half the window matches, a whole-passage search on the last 6 spoken words finds where the user jumped: skipped words become missed, and a jump back counts as a repeat with no penalty.
- **Word states:** `pending | tentative | matched | close | missed | hinted`, plus an insertion count between words. A tentative word locks when its segment is final, or after 3 unchanged partials / 1.2 s. The marker sits at the furthest locked word. Engine confidence is never used for color: iOS reports 0 on partials and Android -1.
- **Silence** (Proposed, inside R13's ≥ 6 s rule). A first-letter hint is offered after 6 s of silence (adjustable); using it marks the word `hinted`. Listening stops on card change, on backgrounding, or after a longer adjustable silence (default about 15 s, generous because older reciters pause to remember). Stopping never records a grade by itself: the user always sees the result and confirms.
- **Grade:** `finish()` turns states into an `Attempt` and `engine.grade` suggests the rating (§4).
- **Trail storage** (Decided: R6). One row per attempt: `states` (one character per passage word, e.g. `MMCMXMH…`), `insertions` (`0,0,1,…`), `engineId`, `engineVersion`, suggested and final rating. The progress view compares trails only when the card hash and the engine match, so an engine upgrade doesn't fake improvement.
- **Replay engine.** It plays a logged `Hyp[]` (text only, with timings) through the same aligner. Thomas's recorded recitations become `fixtures/stt/*.json`. STT is broken in iOS 26.4+ simulators, so the live path is tested on the iPhone (research: stt.md).
- **Latency budget** (Proposed; measure on the iPhone): recognizer partial ~0.3–0.5 s (one informal SpeechAnalyzer report; SFSpeechRecognizer unmeasured) + align < 5 ms (about 60×55 cells per partial) + paint ≤ 1 frame (16 ms; only changed words re-render). Target: a spoken word is colored within ~0.7 s.

### ➕ 6. Plant pipeline

`growPlant(input: PlantInput)` is a pure function (Decided: R11). The engine turns FSRS states into plain numbers first, so the plant package never sees FSRS:

```ts
interface PlantInput {
  plantSeed: string;          // 128-bit hex, created once, synced
  renderVersion: number;      // which growth algorithm drew this plant
  totalRootedVerses: number;  // sets the overall stage
  limbs: Array<{              // one per passage family, in enrollment order
    familyId: string;
    outline: OutlineNode;                                   // anchors + word counts
    branchGrowth: Record<NodeAnchor, number>;               // 0–1, from Phase 1 card stability
    leaves: Array<{ verseId: VerseId; stage: LeafStage; r: number | null }>;
    blossoms: NodeAnchor[];   fruit: boolean;
  }>;
}
interface PlantGeometry {
  stage: 'seedling' | 'sapling' | 'young-tree' | 'tree';
  segments: Segment[];        // id, parent, start, control point, end, width, growth 0–1
  leaves: Leaf[];             // verseId, position, angle, size, stage, droop°, saturation, shape
  blossoms: Point[];  fruit: Point[];  bounds: Rect;
  a11yLabel: string;          // "Sermon on the Mount: 42 of 107 verses rooted, 6 thirsty"
}
```

- **Shape.** The outline is the topology: limb = passage family (so the Farewell parts grow one limb), branch = section, twig = unit, leaf = verse. Branch length = parent × 0.8 × √(subtree words / parent words); widths follow Leonardo's rule (parent width² = sum of child widths²); the base angle is drawn once per plant from 22–38° with ±6° per node; leaves sit at golden-angle (137.5°) positions (research: product.md).
- **Character stays put.** Each node's random stream is `sfc32(hash(plantSeed, nodeAnchor))`, a small seeded PRNG (pseudo-random number generator that always gives the same sequence for the same seed). Editing one section reshapes only that branch. The hash and PRNG are ~20 inline lines, no dependency.
- **Vitality.** Droop = 30° × min(1, (0.9 − R) / 0.3) below R = 0.9, with up to 35% less saturation, capped. No browning, falling or death; structure never shrinks (R11).
- **Overall stage** (Proposed placeholders, gate 4.2): sapling at 50 rooted verses, young tree at 300, tree at 1,000.
- **Caching** (Proposed). Topology geometry is cached per limb in `plant_cache`, keyed by hash(seed, renderVersion, outline anchors); it changes only on an outline edit. The growth/stage/droop overlay is cheap and recomputed at session end and on app open, not after every review.
- **Rendering.** Skia (`@shopify/react-native-skia` 2.6.2, the SDK 57 pin) with Reanimated 4.5.1 (the animation library): branches are tapered Paths whose `end` trim animates growth; all leaves are drawn in one Atlas call (Skia's batched sprite drawing). Reduce Motion swaps animation for a crossfade.
- **Widget snapshot.** After a session the app renders the plant offscreen to a PNG (Skia `makeImageSnapshot`) in the App Group folder (storage shared by the app and its widget) and calls expo-widgets `updateSnapshot` with the PNG and a line of text. Widgets can't run Skia or hooks. That Skia snapshots suit widgets is low confidence (research: stack.md); the fallback is a text-only widget.
- **renderVersion** (Proposed). `growPlant` dispatches on it. Old versions stay in the package, frozen and covered by determinism tests. A plant moves to a new version only through an explicit "new look" migration, never silently.
- **Very large passages** (all of Psalms is 2,461 verses): whether leaves group by chapter beyond about 500 verses is gate 4.7, decided from frame times on the iPhone.

### ➕ 7. Content format

**Passage bundle** (Proposed). A self-contained JSON file, so Python and TypeScript compile from byte-identical input:

```jsonc
{
  "schema": 1,
  "id": "som",                                  // stable passage id
  "family": "som",                              // outline family, used in card keys (§4)
  "title": "Sermon on the Mount", "shelf": "teachings-of-jesus",
  "translation": "BSB", "outlineVersion": 1, "generatorVersion": "seq-v2.1",
  "ranges": [[40005003, 40007027]],             // several ranges, across books, for collections
  "outline": {
    "anchor": "40005003-40007027.0", "title": "The Sermon on the Mount",
    "range": [40005003, 40007027],
    "children": [{ "anchor": "40005003-40005016.1", "title": "The Beatitudes",
                   "bsbHeading": null, "range": [40005003, 40005016], "children": [] }]
  },
  "verses": [{
    "id": 40005003, "ref": "Matthew 5:3",
    "lines": [{ "text": "“Blessed are the poor in spirit, …", "indent": 0 }],
    "paragraphStart": true, "headings": ["The Beatitudes"], "subtitle": null,
    "red": true, "notes": [{ "id": 12, "text": "…" }]
  }],
  "attribution": ["bsb"],
  "stats": { "verses": 107, "words": 2279, "cards": 356 }
}
```

- **Passage spec vs bundle.** Everything above except `verses` and `stats` is the **passage spec**. Curated bundles ship whole in the app. Custom and group passages are stored and synced as specs only; the device rebuilds the bundle from `bsb.sqlite` (or `texts.db`) whenever it compiles (§8).
- **BSB SQLite asset** (Decided: R9; schema Proposed). `bsb.sqlite`, read-only and replaced whole by each app update (never migrated). Tables: `book` (id, osis, usfm, name, order, chapters), `verse` (id = VerseId, book, chapter, verse, lines_json, paragraph_start, headings_json, subtitle), `footnote`, `red_letter`, and an FTS5 index (SQLite's built-in full-text search) for reference and phrase search. The source is 6.6 MB of chapter JSON (research: content.md).
- **Red-letter table** (Decided: R9). `red_letter(verse_id, share)`, from ENGWEBP's words-of-Jesus flags mapped to BSB refs: 1,955 Gospel verses; the 7 WEB verses BSB lacks are dropped. It drives the "teachings of Jesus" progress (x of 1,955).
- **Commentary cache** (Decided: R9). Fetched per chapter after the study-helps consent (§1) from `/api/c/{commentary}/{book}/{chapter}.json` and stored in `texts.db`. JFB, Clarke and Henry come first. Tyndale is shown unmodified, credited "CC BY-SA 4.0", with a note that it quotes the NLT, and is never AI-summarized (a summary would be an adaptation that must itself be CC BY-SA). OpenBible cross-references (CC BY 4.0) come the same way.
- **Translation downloads** (Decided: R9; filter Proposed). Other translations come chapter by chapter from `/api/{translation}/{book}/{chapter}.json`, after the same kind of consent. They are parsed with a TS port of `src/chapter.py`'s flattening (whose TypedDicts already mirror the API) into `texts.db`, which uses `bsb.sqlite`'s verse schema. The app offers only translations whose API `license.publicDomain` flag is true (34 of 51 English texts, e.g. KJV, WEB, ASV, YLT). It excludes the 7 non-commercial / no-derivatives texts (e.g. NET), because blanking words may count as a derivative, and in v1 also the 7 share-alike texts (e.g. LSV), whose attribution and share-alike duties nobody has reviewed (research: content.md).
- **Attribution table** (Decided: R9). `packages/shared/attribution.ts`, hand-written credit lines plus the live API's `license` flags, captured at export time. The DB's `licenseNotice` is empty for all 51 translations. Shown on About and wherever a text appears.
- **The Python exporter** (Proposed: `python -m src.content build`).
  1. Read `data/passages/*.yml`: id, family, title, shelf, ranges, and either an outline tree or the family nodes it covers (collections allowed).
  2. Load text with `src/chapter.py`.
  3. Validate: parts cover parents exactly, gaps where BSB omits a verse are allowed, and back-to-back headings (Heb 11:30) are merged. Fail if an outline differs from the last committed bundle without an `outlineVersion` bump.
  4. Attach red-letter flags.
  5. Write `apps/mobile/assets/bundles/*.json`, an `index.json` shelf manifest (with `bsb.sqlite`'s hash) and `bsb.sqlite`.
  6. Run `src/deck` to write the goldens and print stats.

  Output is byte-stable (sorted keys), so git diffs show only real changes. `bible.eng.db` is a download, not code: its source URL, download date and SHA-256 go in `data/README.md`, a fetch script verifies the hash, and every golden is stamped with it, so a re-download can't change exports unnoticed.

### ➕ 8. On-device data model

Three databases: `app.db` (read-write, Drizzle-managed), the read-only `bsb.sqlite`, and `texts.db` (downloaded translations and commentary). Drizzle ORM 0.45.4 (an ORM maps tables to typed TypeScript objects) on expo-sqlite ~57.0.4; stay on 0.45.x and don't mix in v1-RC docs (research: stack.md). Decided: R4; tables Proposed.

| Table | Holds | Synced? |
|---|---|---|
| `passages` | per (passage, outlineVersion): the passage spec (§7), or a pointer to the bundled curated file | custom/group: spec only, never `verses`, `notes` or pasted text |
| `enrollments` | passage, outlineVersion, generatorVersion, translation, pace, status, `version` | yes (LWW) |
| `cards` | key, family, kind, contentHash, status (unreleased/released/introduced/retired), dates, FSRS state | no: rebuilt from events |
| `review_events` | UUIDv7 id, card key, kind (review/undo/reset), autoRating, finalRating, reviewedAt, durationMs, mode, snapshot, `seq`, `syncedAt` | yes, **append-only** |
| `attempts` | attempt summary + trail (states, insertions, engineId, engineVersion), linked to its event | yes, inside the event (gate 6.1) |
| `outbox` | pending uploads: (entity, entityId, createdAt, tries, lastError) | — |
| `verse_mastery` | verseId, stability, rootedAt, governing card | bitset only, if counted in a group total |
| `plant`, `plant_cache` | seed, renderVersion; cached geometry | seed: yes |
| `settings` | key → JSON value with `version` (pace, reminder, rhythm goal, text size, consents) | yes (LWW) |
| `pasted_text` | (label, verseId) → text, the user's own wording | **never** |
| `sync_state`, `app_log` | deviceId, lastPulledSeq; capped error log (§16) | no |

- **UUIDv7** is a unique id that embeds its creation time, so ids made offline on two phones never collide and sort roughly by time. It uses uuid 14.0.3, with `react-native-get-random-values` imported first.
- **Append-only:** a mistake is fixed by an `undo` event, never an UPDATE or DELETE. Card states are a cache rebuilt from events.
- **LWW** (last-writer-wins): for small mutable records, the higher `version` wins on merge.
- **Bundled migrations.** `drizzle-kit generate` writes SQL files. They are inlined into the JS bundle (babel inline-import plugin + `sql` in Metro's sourceExts) and applied by `useMigrations` before the first screen renders. If that setup is missing, migrations silently don't load.
- **Exclusive transactions.** One review writes the event, the card state, the attempt and the outbox row in `withExclusiveTransactionAsync`. The plain `withTransactionAsync` lets unrelated queries slip in.
- **Live queries.** The database is opened with `enableChangeListener: true`, so Drizzle's `useLiveQuery` re-renders screens when rows change.
- **Device backups** (Proposed). iOS iCloud backup and Quick Start (the iPhone-to-iPhone setup transfer) copy `app.db` by default, so local-only progress, pasted text included, survives a new iPhone without any account. That copy is the user's own Apple backup, which Seedling never sees, so it doesn't break "pasted text never reaches the server". `bsb.sqlite` and `texts.db` can be rebuilt or re-downloaded, so they are marked `NSURLIsExcludedFromBackupKey` (a flag that tells iOS not to copy a file into backups), as Apple's storage guidelines expect. More → Account says plainly what survives where (§10).

### ➕ 9. Server

Hono 4.13 (a small TypeScript web framework) on Node 22/24, `pg` 8.23 through `@google-cloud/cloud-sql-connector` 1.12 (IAM login, no database password), firebase-admin 14.5, and zod validation from `shared` on every route. Decided: R5. Routes are Proposed, as is using Drizzle for the Postgres schema and migrations too (one ORM to learn).

| Endpoint | Purpose |
|---|---|
| `GET /v1/health` | no auth; for uptime checks |
| `POST /v1/me` · `GET /v1/me` | create the user on first sign-in (with the 13+ attestation) · account info and FSRS weights |
| `DELETE /v1/me` | full deletion (token checked with `checkRevoked`) |
| `POST /v1/sync/push` | upload up to 500 events and records; idempotent |
| `GET /v1/sync/pull?after=&limit=500` | everything with `seq > after`, plus `next` and `hasMore` |
| `PUT /v1/mastery` | the rooted-verse bitset, sent only while `count_in_total` is true in at least one group |
| `POST /v1/groups` · `POST /v1/groups/join` | create (name) · join by code or QR; the join body requires an explicit `countInTotal` answer |
| `GET /v1/groups/:id/tree` | per-chapter rooted counts and member birds, never a ranking; names only where `show_name` is on |
| `POST /v1/groups/:id/passages` | leader publishes a passage spec: title, references and outline headings, never text |
| `POST /v1/reports` · `POST /v1/blocks` | Apple 1.2 basics for group content (R15) |

**ID-token middleware.** Every route except health:

```ts
app.use('/v1/*', async (c, next) => {
  const token = c.req.header('Authorization')?.replace(/^Bearer /, '');
  if (!token) return c.json({ error: 'unauthenticated' }, 401);
  try {
    const { uid } = await getAuth().verifyIdToken(token);  // checks signature, audience, expiry
    c.set('uid', uid);
  } catch {
    return c.json({ error: 'unauthenticated' }, 401);
  }
  await next();
});
```

Cloud Run's own IAM check is off (`invoker_iam_disabled = true`): two credentials can't share one Authorization header, so the Firebase token does the authenticating.

**Postgres schema** (trimmed; PG18 has native `uuidv7()`):

```sql
users          (id uuid pk default uuidv7(), firebase_uid text unique not null,
                age_gate_ok_at timestamptz not null,  -- 13+ attestation, no birth date
                seq bigint not null default 0,        -- per-user sync counter
                fsrs_params jsonb, display_name text, created_at timestamptz)
review_events  (id uuid pk /* client UUIDv7 */, user_id uuid → users on delete cascade,
                seq bigint not null, device_id uuid, card_key text, kind text, auto_rating smallint,
                final_rating smallint, reviewed_at timestamptz,
                payload jsonb,                        -- snapshot, attempt, trail
                received_at timestamptz default now(), unique (user_id, seq))
user_records   (user_id → users cascade, entity text, entity_id text, version int, seq bigint,
                payload jsonb, deleted bool, pk (user_id, entity, entity_id))  -- LWW; passage specs here
groups         (id uuid pk, name text, join_code text unique, created_by → users)
group_members  (group_id → groups cascade, user_id → users cascade, role text,
                count_in_total bool not null,         -- explicit choice on the join screen, no default
                show_name bool not null default false,
                pk (group_id, user_id))
group_passages (id uuid pk, group_id → groups cascade, version int, title text,
                ranges jsonb, outline jsonb)          -- references and headings, never text
mastery_bits   (user_id pk → users cascade, bits bytea /* 31,086 bits ≈ 3.9 KB */, version int)
reports, blocks
```

**Group sharing** (Proposed, within R11's "each opted-in member shares a bitset"). Joining asks one explicit question: "Count my rooted verses in the group's total? No names, no ranking." Neither answer is preselected, and the answer is stored in `count_in_total`. `show_name` ("show my name and what I'm learning on my bird") is a separate switch, off by default. Both can be changed later. Gate 7.1 confirms this with the pastor and elders.

**Sync protocol** (Decided: R5, from research: backend.md):
- **Push.** In one transaction: `SELECT seq FROM users WHERE id = $1 FOR UPDATE` (locks the user's row, so two phones pushing at once are put in order), drop ids that already exist, insert the rest numbered `seq + 1, seq + 2, …`, bump `users.seq`. Events and LWW records share this one counter. Re-sending a batch is harmless (**idempotent**).
- **Pull.** By `seq`, never by timestamp. A timestamp cursor skips a late upload from a phone that was offline; even a global serial can commit out of order.
- **Client merge.** Insert pulled events with `ON CONFLICT DO NOTHING`; apply records whose `version` is newer. If a card's merged history came from one device, keep its stored snapshot. If two devices reviewed it, replay the merged list sorted by (reviewedAt, id) with ts-fsrs `reschedule()`, fuzz off.
- **When.** After each session, on app foreground (debounced) and right after sign-in. It never blocks the UI; the outbox just waits for the network.
- **Payload check.** Tests inspect every push payload and fail on verse text or any `pasted_text` field (Build 6.8, 9.12).

**What the server never stores:** audio, recognizer transcripts, pasted text, Bible text (passage specs carry references and headings only), commentary, birth dates, Apple or Google OAuth tokens, contacts, location or advertising IDs. It stores nothing at all for users who never sign in, including every under-13 user.

### ➕ 10. Auth and accounts flow

1. **Install → local-only** (Decided: R3). No account, no anonymous auth, no network calls until the user opts in (§1). A random `deviceId` stays in `sync_state`.
2. **Opt in.** From "Back up my progress" or "Join a group", a short screen says what syncing stores (§15).
3. **Age screen** (Decided: R3). It asks birth month and year neutrally, with no "13+" default. Under 13: "You can keep using everything on this phone", and a local flag stops back-button retries and turns off the helloao features (§1). 13 and over: the server records only `age_gate_ok_at`. Before teen accounts exist for Texas testers, expo-age-range handles SB2420 (Texas's app-store age law; research: policy.md).
4. **Sign in.** Sign in with Apple (with a nonce, a one-time random value that blocks replayed logins) or Google, then Firebase `signInWithCredential` returns the ID token. Apple's guideline 4.8 requires Apple's option whenever Google's is offered. Email-link sign-in is gate 6.1.
5. **First upload.** `POST /v1/me`, then the whole outbox since install is pushed in batches of 500, with progress shown ("Backing up 3,214 reviews…").
6. **Second device / new phone.** Sign in → pull everything → rebuild card states → the same plant regrows, because the seed and outline are synced. Pasted text doesn't come back through Seedling's sync, and the user is told so beforehand; an iCloud restore or Quick Start still carries it (§8). If both phones studied offline before signing in, events merge as a union: the keys are deterministic, so reviews of the same card interleave correctly.
7. **No account at all** (Proposed). More → Account explains in one line that an iCloud backup keeps the plant on a new iPhone, and that an account also covers a lost phone or a deleted app. Once, after about 2 weeks of study and never inside a session, the app asks "Keep your plant safe?" with "Back up" and "Not now". Known under-13 users never see it.
8. **Sign out.** Sync stops; local data stays. "Erase this phone" is separate and asks for confirmation on its own screen, stating what will be lost.
9. **Deletion** (Decided: R3; Apple 5.1.1(v)). More → Account → Delete: re-authenticate (for Apple, a fresh sign-in, then Firebase `revokeAccessToken`) → `DELETE /v1/me` → the server cascades every row, hands owned groups to another leader or deletes them, and deletes the Firebase user. For Google Play, a public deletion page on the church site takes requests from people without the app; Thomas runs an admin script for those.

### ➕ 11. App structure

expo-router (file-based routing: each file in `app/` is a screen). Native tabs come from `unstable-native-tabs` on SDK 57 and become stable in SDK 58. Four tabs, under the five-tab cap. Proposed.

| Route | Screen |
|---|---|
| `(tabs)/index` **Today** | the plant, the weekly rhythm ("4 of 5 days"), the "Today · about N minutes" button, thirsty count |
| `(tabs)/passages` **Passages** | my passages with progress, the starter shelf, "Make your own" |
| `(tabs)/groups` **Groups** | join by code or QR, the group tree; asks to sign in first |
| `(tabs)/more` **More** | settings (pace, text size, input, reminders), Learn (intro articles), Give, About and credits, Account |
| `session/[id]` | the study session, full screen (states below) |
| `passage/[id]` | outline view, per-section progress, pace, trail history |
| `passage/new` | custom passage: references → outline editor → optional pasted text → preview |
| `notes/[verseId]` | commentary and cross-references sheet |
| `trail/[cardKey]` | trails for one card compared over time ("spotty to solid") |
| `plant` | full-screen plant with its spoken summary |
| `onboarding/*` | the first-run flow defined in Features → Beautiful UI → Key screens; plus "help someone set up" mode |
| `account/*` | sign-in, age screen, delete, erase this phone |

```
idle ─Start─► loading ─► prompt ─► attempt (voice, type or self-check) ─► revealed
                           ▲                                                 │ confirm or override
                           └───────── next card ◄──── event saved ◄──────────┘ ─► summary at the end
app goes to the background at any point: stop the mic, keep the place ─► paused ─► prompt
```

**revealed** shows the answer in place and the suggested grade in plain words ("Well done. See you again in 3 days."), with a small "Grade it differently" link offering the four plain choices (R7; wording in Features → Robust Learning Algorithm).

**State split** (Decided: R4):
- **SQLite + Drizzle live queries** are the truth for everything that persists.
- **Zustand** (a tiny in-memory store) holds the active session: queue, current card, attempt in progress, live word states. A partial result repaints only the words that changed.
- **TanStack Query** handles only API reads (groups, `/me`, sync status), with caching and retries.
- Firebase's `onAuthStateChanged` feeds an auth store, and navigation waits for its first answer.

Background services in `apps/mobile/src`: sync (outbox pusher/puller), notifications (one daily repeating trigger, rescheduled on every app open because iOS keeps at most 64 pending, and switched to weekly after 3 ignored, R12), the content-upgrade check (§4) and the widget snapshot writer.

### ➕ 12. Environments and delivery

| | local | dev | prod |
|---|---|---|---|
| App | dev build on the simulator or Thomas's iPhone (`npx expo run:ios --device`) | same dev build | TestFlight / Play testing, then the stores |
| Bundle ID | `com.<thomas>.seedling.dev` (Thomas's Individual team) | same | `org.<church>.seedling` (church Organization team) |
| API + DB | `pnpm --filter api dev` on the Mac + Postgres.app 18 | Cloud Run + Cloud SQL in `seedling-dev`, only if gate 6.1 says so (+≈$9.50/mo) | `seedling-prod` |
| Auth | `seedling-dev` Identity Platform | same | `seedling-prod` |

- **Variants.** `app.config.ts` reads `APP_VARIANT` (development, demo, beta, production) to set the name, icon, bundle ID, App Group and widget IDs, Firebase config and API URL. The `demo` variant (Build 5.16) has its own ID in Thomas's team. Bundle IDs follow R1; Apple Developer Setup explains why, and Build 8.3 holds the foot-gun. Local dev uses `seedling-dev`'s real auth rather than prod auth or emulators, which refines your note.
- **EAS profiles** (EAS = Expo's build-and-submit service; Proposed): `development` (dev client, dev bundle ID, Thomas's team), and `beta` and `production` (both the church's prod bundle ID, prod backend, update channels `beta` and `production`). EAS Free covers 15 iOS + 15 Android builds a month with Submit included. iOS builds made locally on the Mac cost nothing.
- **CI** (GitHub Actions). `ci.yml` on each PR: install, typecheck, lint, Vitest (packages and API, with a Postgres 18 service container), jest-expo, and a golden freshness check (each golden records a hash of the Python sources and passage files that made it; CI fails if they changed without a re-export). `eas.yml` is started by hand. Auth uses Workload Identity Federation, so there are no key files (§13).
- **API deploys** (Proposed). `api-deploy.yml` on main: build → Artifact Registry (Google's container image store) → deploy to dev. Prod waits for Thomas's approval in a `production` GitHub Environment, then: an on-demand backup (`gcloud sql backups create`) → migrations as a Cloud Run job under the deployer account → shift traffic to the new revision. **Migrations are additive** (expand/contract: add the new column or table in one release, remove the old one a release later), so the previous revision still runs and a rollback is just `gcloud run services update-traffic --to-revisions=<previous>=100` (runbook in Build 6.15). Foot-gun: on GitHub Free, a private repo gets no branch protection and no required reviewers on Environments, so this approval gate needs a public repo or a paid plan (gate 0.6).
- **EAS Update (OTA).** An OTA (over-the-air) update swaps the JavaScript and assets without a store release. The free plan has a hard cap of 1,000 monthly active users receiving updates; beyond it, budget EAS Starter ($19/mo, 3,000) or ship through the stores (research: stack.md). Rule (Proposed): an OTA never carries a database migration, because a rollback would leave the schema ahead of the code. A curated outline update can ship by OTA, since the content-upgrade check (§4) runs on the device. Thomas publishes OTAs to `beta` and `production`, or a workflow behind the `production` Environment does; Claude never does.
- **Release flow.** Personal phase: a local Release build on the iPhone. Church beta: bump the version → `eas build --profile beta` (or `--local`) → `eas submit` → TestFlight internal, then an external group (the first build needs Beta App Review), with Play internal → closed testing for Android. JS-only fixes go out as OTAs on `beta`. Public launch: `production` → store review.

### ➕ 13. Infrastructure

Terraform 1.16.6 with `google` and `google-beta` `~> 8.7`; Firebase project and app resources still need `google-beta` (Decided: R5).

```
infra/
├── bootstrap/      Thomas runs as owner, once per project: versioned state buckets, the Workload
│                   Identity pool, every service account and every IAM grant, budgets
├── modules/
│   ├── auth/       Firebase project + apps, Identity Platform, Apple and Google providers
│   ├── db/         Cloud SQL POSTGRES_18, db-f1-micro, edition "ENTERPRISE", IAM auth, PITR
│   └── api/        Cloud Run v2, Artifact Registry (keep 3 images), secrets, uptime check, 5xx alert
└── envs/
    ├── dev/        seedling-dev; state in the dev bucket; Claude applies through tf-dev
    └── prod/       seedling-prod; state bucket inside prod, which no agent identity can read
```

All IAM lives in bootstrap (Proposed), so no account Claude can borrow needs an IAM-admin role, and none can grant itself more access.

- **Resources.** Cloud Run: request billing, min 0 / max 4 instances, 1 vCPU / 512 MiB, startup CPU boost, `invoker_iam_disabled`, image ignored by Terraform so CI deploys don't fight it. Cloud SQL: 10 GB SSD with autoresize, backups with 7-day point-in-time recovery (PITR: restore to any minute), `deletion_protection_enabled`, `connector_enforcement = "REQUIRED"`, public IP with no authorized networks. Pool max 5 × 4 instances stays under f1-micro's 25 connections. Foot-gun: without `edition = "ENTERPRISE"`, PG16+ defaults to Enterprise Plus and the f1-micro tier fails.
- **Change safety** (Proposed). `lifecycle { prevent_destroy = true }` on the Cloud SQL instance and the state buckets, so a bad plan can't delete them. A PITR restore drill (clone into a new instance, then repoint) runs in dev and once in prod before testers' data exists (Build 6.15, 8.10). Prod plans go into PRs as a summary only, never raw output on a public repo.

**Identities** (Decided: R5; the agent login, tf-dev and the GitHub machine user are Proposed):

| Who | Where | Can do | Signs in by |
|---|---|---|---|
| Thomas (owner) | both projects | everything; bootstrap, prod plan/apply, prod admin scripts | his Google login + 2FA, only from a separate macOS user account or Cloud Shell (Google's browser terminal), never the Mac user Claude runs as |
| Agent login (a dedicated Google account used only by Claude) | no project roles | borrow `claude-agent` (standing grant); through it, `tf-dev` while a time-limited grant lasts | its own gcloud config directory (`CLOUDSDK_CONFIG`, set in `.claude/settings.json`); ADC there impersonates `claude-agent` |
| `claude-agent@seedling-dev` (a service account: a non-human Google identity) | dev only | deploy to dev Cloud Run, push images, connect to the dev DB, read logs, create test users, use the dev state prefix | **impersonation** (borrowing a service account's short-lived token; the Token Creator role allows it); no key file |
| `tf-dev@seedling-dev` | dev only | create and change dev resources (Firebase, Identity Platform, Cloud SQL, Cloud Run) for `terraform apply` in `envs/dev`; no IAM-admin role | chained impersonation per session: Thomas grants `claude-agent` Token Creator on it with the IAM condition `request.time < timestamp("<session end>")`, so it expires by itself |
| deployer (per project) | GitHub Actions | deploy Cloud Run, run the migration job, push images, act as the runtime account | **WIF** (Workload Identity Federation: GitHub proves "this is repo X on main" and Google trusts that), pinned to the repo id and `main` |
| runtime (per project) | the Cloud Run service and migration job | Cloud SQL client + instance user, read its secrets | attached to the service |
| Claude on GitHub (a machine-user account) | the repo | push branches, open PRs; merging needs Thomas's approving review | its own `gh` token |

**Agent guardrails: the wall is whatever credentials Claude's shell can read.** This is the part people get wrong. Impersonation runs on the caller's own stored login. If Thomas's owner login sits in `~/.config/gcloud` on the Mac user Claude runs as, Claude can reach prod with it: by switching configs, passing `--impersonate-service-account`, or through ADC (Application Default Credentials, the separate credential file Terraform and client libraries read; gcloud configs don't affect it). Deny rules are prefix matches that a script or `bash -c` gets around. Web-dev analogy: give the contractor their own badge that opens only the dev door, rather than your master key with a note saying "dev only". So (Proposed; Build 6.4 carries the steps):
1. After bootstrap, Thomas runs `gcloud auth revoke` and `gcloud auth application-default revoke` for his owner login on this Mac user. Owner and prod work happen only in a separate macOS user account or Cloud Shell.
2. Claude's shell holds only the agent login, which has no roles of its own and can borrow only dev accounts. Claude Code's sandbox also denies reads of `~/.config/gcloud`.
3. tf-dev access expires through its IAM condition, so a forgotten grant can't linger.
4. Deny rules for prod `gcloud` and `terraform -chdir=infra/envs/prod` stay as a tripwire, not a wall.

The check: from Claude's shell, `gcloud auth list` shows only the agent login, ADC resolves to `claude-agent`, and `gcloud projects describe seedling-prod` fails under every configuration.

- **Secrets.** No database password (IAM login) and no JSON keys anywhere. Thomas pastes the Sign in with Apple key (.p8) into Identity Platform himself. Terraform's state (its record of everything it created) stores the Identity Platform API key in plain text, so the state buckets are treated as secrets.
- **Budgets.** $15 (dev) and $25 (prod), alerting at 50/90/100%; they alert but never cap spending (foot-gun in Build 6.5). Costs: Technical Specifications → Cost Generators (prod ≈ $10/month).

### ➕ 14. Testing strategy

| Layer | Tool | What it proves | Runs |
|---|---|---|---|
| `engine` | Vitest 5.0.4 | golden parity (compile exact, release invariants, FSRS vs py-fsrs); the §4 grade table; shared-family keys (no duplicates across Farewell parts and whole); recompile diff and content upgrade | CI |
| `recite` | Vitest | normalizer cases (numerals, LORD, dashes, quotes); aligner fixtures (skip, repeat, jump, "Melchi zedek"); replays of Thomas's logs; privacy-gate refusal | CI |
| `plant` | Vitest | determinism (same input → same geometry hash); editing one section leaves the others unchanged; never shrinks | CI |
| `apps/api` | Vitest + Postgres 18 | push idempotency, seq order under concurrent pushes, the token middleware, deletion cascade, no verse text or pasted text accepted | CI |
| `apps/mobile` | jest-expo ~57.0.6 + RNTL 14.1 (React Native Testing Library) | screens against an in-memory DB; the session state machine. RNTL 14's render is async | CI |
| End-to-end | Maestro 2.11 (scripted flows that tap through the real app) | onboarding, a full session in type and self-check modes, a custom passage | simulator + Android emulator, local |
| Python | unittest | generator, exporter, key function | Mac (needs `bible.eng.db`) |

- **Manual on the iPhone** before each beta build: STT (broken in iOS 26.4+ simulators), Sign in with Apple (`getCredentialStateAsync` throws on simulators), the widget, reminders, a 450-word recitation, battery and heat.
- **Android without a device:** the arm64 emulator on the Mac, Firebase Test Lab Robo runs (Robo is Google's automated crawler that taps through the app; Spark plan: 10 virtual + 5 physical a day) and Play pre-launch reports on every upload. The emulator can't prove on-device recognition, so a borrowed Android 13+ phone runs the voice script before the Play closed test.
- **Accessibility:** each beta at AX5 (the largest Dynamic Type size; Dynamic Type is iOS's user text-size setting), with VoiceOver, Reduce Motion and a contrast check of the color tokens against 7:1 (R13). Every interactive element has a stable `testID` shared by Maestro and the Expo MCP automation.

### ➕ 15. Privacy and security boundaries

| Data | Lives | Reaches Seedling's server? | Who sees it |
|---|---|---|---|
| Raw audio | the on-device recognizer's memory only | never; never stored | no one |
| Recognizer text (hypotheses) | memory during one card | never (Thomas's own logs as dev fixtures only) | — |
| Trails and attempt summaries | `app.db` | if signed in, to own account (gate 6.1) | the user |
| Review events, enrollments, settings, plant seed | `app.db` | if signed in | the user; Thomas as operator |
| Custom passage specs (references, outline) | `app.db` | if signed in; group ones go to the group | user; group members |
| Pasted text | `pasted_text` in `app.db` | **never** (not in Seedling's sync or groups; the user's own iCloud backup carries it, §8) | the user |
| Rooted-verse bitset | `app.db` → `mastery_bits` | only while `count_in_total` is on in a group | group: as leaves and birds; names only with `show_name` |
| Email, user ID, name | Identity Platform, `users` | at account creation | the user; Thomas |
| Age answer | local flag; server timestamp only | attestation only, no birth date | — |
| Commentary and translation downloads | `texts.db` | no; helloao only, after consent | helloao sees the IP and chapter |

- **Permission strings** (Decided: R14; wording Proposed). `NSMicrophoneUsageDescription`: "Seedling listens while you recite so it can show which words you got right. Audio is processed on your device and never saved or uploaded." `NSSpeechRecognitionUsageDescription` (SFSpeechRecognizer path only): "Seedling uses your iPhone's on-device speech recognition to follow along as you recite. Nothing you say leaves your phone." Android asks for `RECORD_AUDIO` only. Also `usesNonExemptEncryption: false` and privacy manifests copied from each native dependency.
- **Threat notes:**
  - The API is public by design: every route but health needs a valid token, bodies are zod-checked and size-capped, and max 4 instances caps abuse cost.
  - ID tokens last an hour; deletion re-checks revocation.
  - Group content is limited to names, titles and headings, with report and block (Apple 1.2).
  - The agent can't reach prod because its shell holds no credential that can (§13). Simulator screenshots go to Anthropic (Build 2.14), so the simulator holds only test data.
  - pnpm's `allowBuilds` list and 1-day minimum release age slow supply-chain surprises.
  - iOS file protection encrypts `app.db` at rest; SQLCipher (an encrypted SQLite) is available if ever needed (Proposed: not in v1).
  - App Check (Firebase's proof that a call comes from the real app) needs native Firebase modules: deferred.

### ➕ 16. Observability

- **No third-party analytics in v1** (Proposed; fits R3/R5). What Seedling learns about learning comes from review events: Thomas's own, and beta testers' only by explicit opt-in export.
- **Crash reporting** (Proposed; gate 10.1). Personal phase: Xcode's device logs. Church beta: TestFlight crash reports and tester feedback, plus Play Console's Android vitals. Both are built in, need no SDK and leave the privacy labels unchanged. A crash SDK comes before public launch only if those weren't enough; it is then declared as Diagnostics on both privacy forms and never starts for known under-13 users.
- **On-device log.** `app_log` is a ring buffer of about 500 rows: error codes, card keys, engine ids, never verse text or pasted text. It is attached to feedback only when the user chooses.
- **Server logs.** Cloud Run writes structured JSON to Cloud Logging (free to 50 GiB/month): request id, route, status, latency, user id, never request bodies. `modules/api` creates an uptime check on `/v1/health` and an alert on the 5xx (server error) rate.
- **Feedback channel.** More → "Send feedback" opens a mail draft to the church support address with app version, device and iOS version filled in. TestFlight's screenshot feedback works during the beta, and the support page on the church site is required for store listings anyway.

### ➕ 17. Key architecture decisions

| # | Decision | Status |
|---|---|---|
| 1 | Local-first: device SQLite is the source of truth; the cloud is backup, sync and groups | Decided (R3, R5) |
| 2 | No network calls until opt-in: an account for Seedling's servers, a per-feature consent for helloao; none for known under-13 users | Decided (R3); consent design Proposed |
| 3 | Monorepo with pnpm workspaces in this repo; Python is the reference and content pipeline | Decided (6, R16) |
| 4 | Expo SDK 57 dev builds (no Expo Go); upgrade to SDK 58 before the church beta | Decided (R4) |
| 5 | Pure-TS packages (`engine`, `recite`, `plant`, `shared`): no RN imports, no clock, Vitest | Decided (R16) |
| 6 | Every ladder card is its own FSRS item (ts-fsrs, FSRS-6 defaults, retention 0.90, 10-minute steps) behind a `Scheduler` interface | Decided (7, R8) |
| 7 | Cards are data (`CardSpec`), drawn by React components | Decided (R8) |
| 8 | Range-based card keys under an outline family, without the outline version; shared passages share cards; any recompile runs keep/reset/retire/add | Proposed |
| 9 | Calendar-day release planner; groups introduced whole; no pull-forward; already-introduced keys skipped | Proposed (on R8) |
| 10 | Grading table in §4 (trial 2's type-mode rule) is the single source of truth; suggest and confirm; log auto and final ratings | Decided (R7) |
| 11 | Governing card = the unit's Header→text; rooted at stability ≥ 21 days | Decided (R8, R11) |
| 12 | On-device STT only, privacy gate inside the engine interface; voice off when it fails | Decided (5, R6) |
| 13 | Pure-TS aligner with a replay engine; trails as state strings + engine id/version | Decided (R6) |
| 14 | Deterministic plant: per-node hashed seeds, sfc32, stored renderVersion; never dies | Decided (R11) |
| 15 | Self-contained passage bundles as the shared Python/TS compile input; custom and group passages sync as specs only | Proposed |
| 16 | Bundle the whole BSB as read-only SQLite; other public-domain translations on demand | Decided (R9) |
| 17 | Pasted text never reaches Seedling's server | Decided (R9) |
| 18 | Custom append-only event-log sync (UUIDv7, per-user seq), not PowerSync or Firestore | Decided (R5) |
| 19 | Hono on Cloud Run + Cloud SQL PG18 f1-micro + Identity Platform, IAM DB login | Decided (10, R5) |
| 20 | Sign in with Apple + Google, no anonymous auth, neutral 13+ age screen | Decided (R3) |
| 21 | Two GCP projects; CI via WIF; agent identities are dev-only and Thomas's owner login never sits where Claude's shell can read it | Decided (R5); credential isolation Proposed |
| 22 | Groups see only client-computed mastery bitsets; counting toward the total is an explicit choice, names off by default | Decided (R5, R11); join design Proposed |
| 23 | Uniwind + HeroUI Native, with Unistyles 3.5 as the fallback | Decided (R4) |
| 24 | No analytics or crash SDK in v1; store-provided crash reports first | Proposed |
| 25 | OTA updates never carry database migrations; server migrations are additive | Proposed |
| 26 | Packages ship TS source with no build step | Proposed |

**Still open** (each is a Build Phases gate, which is the single decision list): trails synced or device-only, a hosted dev backend, GCP billing owner (6.1); repo visibility (0.6); stage thresholds and art (4.2); large-passage leaf grouping (4.7); default pace (5.2); group privacy (7.1).

## Build Phases with Instructions

- Organized and itemized list detailing the phase-wise steps of building the app, marking steps clearly as Clause or Thomas to indicate which steps you can complete on your own versus one's that require my input
- this will be used later to direct you in actually performing the build, but you are not building anything yet.

**➕ Claude:** This section turns the App Architecture above and the release-stage scope in Features → "How the features fit together" into ordered, checkable steps. Phase order, hours and gates are **Proposed**; most of what the phases build is **Decided** (App Architecture §17). It opens with how to use the plan, the phase overview and the decision gates; the full steps for Phases 0–11 follow. A future Claude session can carry out any step from this spec, its sibling files (including `research/`) and the phase's plan file, without this conversation.

### ➕ How to use this section

**Owner tags**

| Tag | Who | Typical work |
|---|---|---|
| **[Claude]** | Claude alone. It verifies its own work (tests, screenshots, CI) before opening a PR | Code, tests, dev-only Terraform, scripts |
| **[Thomas]** | Only a human can do it | Accounts, payments, signatures, the physical iPhone, judgment calls |
| **[Claude → Thomas]** | Claude prepares; Thomas reviews, approves or acts | Drafts, answer sheets, option memos, device test scripts |
| **[Thomas + church]** | Needs church leadership, the pastor or the church's signer | Publishing, accounts in the church's name, theology, group policy |

**Model tags** on Claude steps (Optimize Claude cost → Model routing):
- **Opus** (Opus 5.5, high effort): phase plans, gate memos, design, theology-sensitive drafts and reviews.
- **Sonnet** (Sonnet 5.5): building and testing from a written plan. **Sonnet, Opus review** marks high-risk code that also gets an Opus review before merge: scheduler, aligner, privacy gates, auth, sync, backup and restore, deletion, database migrations and content upgrades, IAM and deploy wiring.
- **Haiku** (Haiku 5.5): mechanical chores, such as creating issues or applying `npx expo install --check` fixes.

**Step format.** `- N.k **[Owner · Model]** what to do — *Done when:* the check that proves it`. Details and **Foot-gun** notes (the part people get wrong) are indented below. When Thomas approves a phase plan, its tasks become GitHub issues in that phase's milestone, labeled `claude` or `thomas` and titled with the step ID ("2.9 Step renderers").

**Gates.** A step marked **Gate** is a decision Thomas makes before the steps that depend on it. Claude lays out the options and a recommendation in the phase plan. The answer goes into `docs/decisions.md`, the ADR file (architecture decision records: one dated entry per decision). The gate table below is the single list of open decisions.

**PR review tiers** (Proposed). Claude labels each PR with its tier.

| Tier | PRs | What Thomas reads | Time |
|---|---|---|---|
| A | "Sonnet, Opus review" steps, database migrations, infra and IAM | The PR summary and the Opus review; the diff only where the review points | ~20 min |
| B | UI | The screenshot set | ~5 min |
| C | Chores, tests, docs | Nothing; approves on green CI at the weekly check-in | ~1 min |

**How a phase runs**
1. **Plan (Opus).** A fresh session greps this spec (`.claude/app-requirements/CLAUDE.md`) for its `Phase N —` heading and the App Architecture § headings the phase names, and reads only those line ranges, plus the research files its steps cite. It writes `docs/plans/phase-N.md`: the steps split into PR-sized tasks, done-when checklists, gate options and risks. Thomas approves it; Haiku then creates the phase's issues.
2. **Build (Sonnet).** One issue, one branch, one small PR, with tests in the same PR. Each issue gets a fresh session, pointed at the exact plan step and files.
3. **Self-verify.** The cheap checks run first: typecheck, lint, Vitest and jest-expo, golden parity, Maestro and screenshots, then CI. The stop rules in Optimize Claude cost → Self-check loops apply: after 3 UI rounds or 2 failed fixes, Claude stops and asks.
4. **Review (Opus).** At phase end, `/code-review high` runs over the phase's merged changes. Phases 3, 6, 7, 8a and 8b also get `/security-review`. Findings become issues, and Sonnet fixes them.
5. **Device check (Thomas).** Claude writes a numbered device test script. Thomas runs it on the iPhone and reports pass or fail per step (Development Workflow → Device-testing loop).
6. **Status.** The GitHub board is the live tracker. At phase end Claude updates the phase's **Status** line in a PR, e.g. `**Status:** Done 2026-12-02 · docs/plans/phase-2.md · review #41` (Proposed; gate 0.6).

**Hours** are Thomas's time: decisions, PR reviews (shown separately), accounts and device checks. Claude's time is not the bottleneck, and Thomas's own daily study isn't counted. Calendar ranges assume 5–10 hours a week; waits on Apple, Google or the church are listed separately.

### ➕ Phase overview

| Phase | Goal | Release stage | Thomas hours (PR review) | Calendar at 5–10 h/wk | Key dependency |
|---|---|---|---:|---|---|
| 0 Groundwork | Accounts, tools, repo rules; spec committed; church paperwork started | Before alpha | 8–14 (≈1) | 1–3 wk (church track runs 2–8 wk alongside) | Thomas's Apple enrollment; one church meeting |
| 1 Engine + content | Python exporter and goldens; TS engine at parity with Python | Personal alpha | 8–15 (≈3) | 1–3 wk | `data/bible.eng.db` on the Mac |
| 2 Study loop | Thomas studies daily on his iPhone (typing and self-check) | Personal alpha | 15–25 (≈5) | 2–5 wk | Phase 1; iPhone registered |
| 3 Voice | On-device recitation with the live trail | Personal alpha | 10–18 (≈3) | 2–4 wk | The iPhone (STT doesn't work in current simulators) |
| 4 Plant | The growing plant on Today | Personal alpha | 4–8 (≈1) | 1–2 wk | Art-direction gate |
| 5 Personal-complete | Starter shelf, custom passages, study helps, rhythm, accessibility; beta go/no-go | Personal alpha → beta gate | 14–24 (≈4) | 2–5 wk, plus the dogfood gate | Church content decisions; 3–5 older testers |
| 6 Backend + accounts | GCP, API, sign-in, sync, deletion, rollback runbooks | Church beta prep | 14–22 (≈4) | 2–4 wk | GCP billing account; an admin macOS user |
| 7 Groups | Groups, join by code or QR, group tree, report and block; SDK 58 | Church beta prep | 8–14 (≈2) | 1–3 wk | Pastor and elders on group privacy; SDK 58 stable |
| 8a iOS church beta | TestFlight external beta from the church's Apple team | Church beta | 15–25 (≈3) | 2–5 wk, plus Beta App Review | Church Apple Organization team (0.10) |
| 8b Android closed test | Play closed test from the church's Play account | Church beta | 8–15 (≈2) | 2–4 wk, alongside Phase 9 | Gate 8.15; a borrowed Android phone |
| 9 Beta iteration + launch prep | Fixes, grading calibration, FSRS parameters, R&D; the public-launch features | Church beta | 30–55 (≈8) | 8–12 wk (time-boxed) | Testers and their opt-in log exports |
| 10 Public launch | Store listings, age signals, final legal review, release | Public launch | 10–20 (≈2) | 1–4 wk, plus store review | Gate 9.16 |
| 11 Later | SpeechAnalyzer, sherpa-onnx, kids mode, AI questions, … | Later | Per project | — | Launch feedback |

**Totals** (Proposed): about 145–255 Thomas hours to public launch, 95–165 of them before the church beta. At 5–10 hours a week, Thomas studies in the app daily about 1–3 months from now, the church beta opens about 4–8 months out, and public launch lands about 6–12 months out.

**Parallel tracks.** The church paperwork starts in Phase 0 and only has to finish by Phase 8a. Phases 3 and 4 can overlap. The Phase 6 bootstrap can start during Phase 5's dogfood weeks (dogfooding: using your own app daily as a real user). Phase 8b runs alongside Phase 9.

### ➕ Decision gates

Every open decision in this spec is answered at one of these gates. Other sections point here.

| Gate | Decides | Who | Blocks |
|---|---|---|---|
| 0.1 | App name ("Seedling" after store and trademark checks) | Thomas | Store records (8.3) |
| 0.6 | Repo visibility (and what it does to branch protection), web version, phase order (voice before plant), tracker | Thomas | 0.13–0.15 |
| 0.9 | Church: publish under its name, Account Holder, legal entity and EIN, giving URL, long-term GCP billing | Thomas + church | 0.10, 8a |
| 2.1 | "Passages" or another word; custom look or platform-native; import trial 2's Anki history | Thomas | Phase 2 UI |
| 3.1 | Voice grading: suggest-and-confirm or automatic Again; do "close" words count; tentative words live | Thomas | 3.10 |
| 4.2 | Plant art direction and stage thresholds | Thomas | 4.3–4.6 |
| 4.7 | Group leaves by chapter beyond about 500 verses | Thomas | Large passages |
| 5.1 | Content defaults: Ten Commandments numbering, Farewell boundary, Teachings of Jesus scope, lead commentary | Thomas + church | 5.4, 5.6 |
| 5.2 | Product defaults: pace, rhythm, first-run flow, first passage, place a known passage as rooted, outline-only mode, study-help downloads, AI questions | Thomas | 5.6–5.12 |
| 5.19 | Church beta go/no-go | Thomas | Phase 6 onward |
| 6.1 | Email-link sign-in, GCP billing, hosted dev backend, trail sync, pasted-text backup, Texas testers | Thomas | Phase 6 |
| 7.1 | Group privacy, blossom threshold, church rest day, who receives reports, join-link domain | Thomas + church | 7.2–7.7 |
| 8.1 | Beta scope: Give, tester list, Texas testers, always-warm API | Thomas | 8a |
| 8.15 | Start Android; Android voice floor | Thomas | 8b |
| 9.7 | Per-unit memory model; which step governs a leaf | Thomas | Phase 11 |
| 9.16 | Public launch go/no-go | Thomas | Phase 10 |
| 10.1 | Launch scope: crash reporting, Give, Android, pasted text | Thomas | Phase 10 |

### ➕ Phase 0 — Groundwork

**Status:** Not started · **Thomas time:** 8–14 h, about 1 h of it PR review

**Goal:** Every account, tool and repo rule the build needs exists, the spec and its research are in git, and the church paperwork, which has the longest lead time, has started.

**Why the church track starts now:** R1 (Apple Developer Setup → "Change to decision 3"). The church's Apple team must own the production app from the first TestFlight upload.

**Prerequisites:** None. Do 0.0 first; then Tracks A, B and C run in parallel.

- 0.0 **[Claude · Haiku]** Commit `.claude/app-requirements/` (this spec, its sibling files and `research/`) in one PR — *Done when:* `git ls-files .claude/app-requirements` lists CLAUDE.md and all six research files.
  - The research files are 2026-10-14 snapshots, cited throughout as "(research: X.md)". If `research/` is missing, stop and ask Thomas: the copies Claude worked from were temporary.

**Track A: Thomas's setup**
- 0.1 **[Thomas]** **Gate: the app name.** Check "Seedling" in the App Store, Google Play and the USPTO trademark search (Nice classes 9 and 41), then confirm it or pick another — *Done when:* the name is in `docs/decisions.md`.
  - The steps are in App Name Ideas → "What Thomas checks". Don't create an App Store record to reserve the name: it belongs in the church's team (8.3).
- 0.2 **[Thomas]** Enroll in the Apple Developer Program as an Individual ($99/yr; legal name, street address, an Apple Account with two-factor authentication) — *Done when:* the membership shows Active.
  - This team only ever builds the dev bundle ID `com.<thomas>.seedling.dev` (R1).
- 0.3 **[Thomas]** Install the tools: Xcode 26.4+ with an iOS simulator runtime, Node 22 or 24 LTS, pnpm, the GitHub CLI (`gh`) and eas-cli (`npm install -g eas-cli` puts the `eas` command on your PATH). Approve Claude Code Desktop's one-time iOS Simulator consent — *Done when:* a simulator boots from Claude Code's Simulator pane.
  - Android Studio waits for Phase 8b (8.16).
- 0.4 **[Thomas]** Prepare the iPhone: turn on Developer Mode, register it (Xcode does this on first run) and turn on Settings > General > Keyboard > Enable Dictation — *Done when:* the iPhone's model and iOS version are in `docs/decisions.md`.
  - The model matters: SpeechAnalyzer's stronger transcriber reportedly needs an iPhone 12 or newer (research: stt.md, low confidence).
- 0.5 **[Thomas]** Create a free Expo account and run `eas login`. Register Expo's MCP server with `claude mcp add --transport http expo https://mcp.expo.dev/mcp`, then sign in with `/mcp` (Development Workflow → Tools explains each part) — *Done when:* `/mcp` lists `expo` as connected.
- 0.6 **[Thomas]** **Gate: repo and workflow** — *Done when:* recorded in `docs/decisions.md`.
  - **Repo visibility.** Public: free Actions minutes, branch protection and Environment approvals all work; the trial notes and data files become visible (`bible.eng.db` stays git-ignored). Private: 2,000 Actions minutes a month.
  - **Foot-gun:** on GitHub Free, a private repo gets no branch protection or rulesets, and private repos get Environment required reviewers only on Enterprise. So on a private Free repo, "Claude never merges" and the prod-deploy approval (6.12) silently don't exist, and prod deploys on every merge. Choose public (recommended), or GitHub Pro (branch protection) plus a Thomas-only prod deploy path: the prod Workload Identity provider also requires `assertion.actor` to be Thomas's GitHub login.
  - **Web version:** none planned (assumed). A web target would change the database and styling choices.
  - **Phase order:** voice (Phase 3) before the plant (Phase 4), because voice is the riskier piece (Proposed), or the plant first for an earlier motivating win.
  - **Tracker:** the GitHub board is live; Status lines here change only at phase end (Proposed).
- 0.7 **[Thomas]** Give Claude its own GitHub account — *Done when:* `gh auth status` in Claude Code's terminal shows that account, and Thomas's own `gh` login isn't on this macOS user.
  - Create a second GitHub account (a "machine user"; GitHub's terms allow one free one per person) and add it to the repo with Write access. In Claude Code's terminal, run `gh auth login` as that account.
  - Thomas reviews and merges in the browser. If his own `gh` login exists on this macOS user, he runs `gh auth logout`.
  - Why: Claude's shell can use any credential the macOS user can read, the way any script can read your `.env`. With its own account, GitHub itself (0.14) stops Claude approving or merging its own PRs.

**Track B: the church (start now)**
- 0.8 **[Claude → Thomas · Opus]** Draft the letter to church leadership — *Done when:* Thomas has sent it.
  - Contents: what Seedling is; why the church should be the publisher (R1); costs (Apple $99/yr or $0 with the nonprofit fee waiver, Google Play $25 once, about $10/month of cloud from the beta on); the D-U-N-S number (a free business ID Apple and Google require); who must sign (someone with legal authority, not a volunteer developer; Apple may phone them); the Give framing (R2); the privacy posture; a timeline.
- 0.9 **[Thomas + church]** **Gate: one meeting with leadership** — *Done when:* the answers are in `docs/decisions.md`.
  - Agenda: approval to publish under the church's name; the Account Holder for Apple and Google; the legal entity name and EIN; the giving page URL; who owns GCP billing long term.
  - **Foot-gun:** churches aren't required to hold an IRS determination letter, but Apple's fee waiver needs IRS-recognized nonprofit status. Find the letter, or the denomination's group-exemption letter. Without one, the church pays $99/yr.
- 0.10 **[Thomas + church]** The signer gets the D-U-N-S, enrolls the church as an Apple Organization and invites Thomas as Admin — *Done when:* Thomas can switch to the church team in his Apple Developer account.
  - D-U-N-S: check Apple's lookup tool first. It takes up to 5 business days, plus 2 before Apple sees it (Google says up to 30 days). The name must match the legal entity exactly.
  - Enrollment needs the church website and an email on the church's domain. Request the fee waiver during enrollment and accept the agreements. This only has to finish before Phase 8a.

**Track C: the repo**
- 0.11 **[Claude · Sonnet]** Create `docs/decisions.md` seeded with decisions 1–12 and R1–R16 (dated, each linking back here) and an empty `docs/plans/` — *Done when:* merged.
  - This file, not Claude's per-machine project memory, is the durable record of decisions. A cloud session or a new Mac has no project memory.
- 0.12 **[Claude · Opus]** Write the root `CLAUDE.md`, short `CLAUDE.md` stubs for `apps/mobile`, `apps/api`, `packages` and `infra`, and `.claude/settings.json` deny rules — *Done when:* Thomas approves the PR.
  - The root file stays short. It points to this spec and the current `docs/plans/phase-N.md` rather than copying them.
  - Root rules: native packages only via `npx expo install`; TypeScript ~6.0.3; no prod access; a `testID` on every interactive element; never "card", "deck", "cloze" or "FSRS" in UI text; never open `data/`, `output/`, `local/`, `bsb.sqlite` or golden JSON whole; never weaken a test or edit a golden to make it pass.
  - Deny rules: any `gcloud` command naming `seedling-prod`, `terraform -chdir=infra/envs/prod`, pushes to `main`, force-pushes, `gh pr merge`, `gh workflow run`, `eas submit`, `eas update --channel beta` or `production`, and `eas build --profile production`.
  - **Foot-gun:** deny rules match command prefixes, so a script or `bash -c` gets around them. They're a speed bump. The walls are separate credentials: 0.7, 0.14 and 6.4.
- 0.13 **[Claude · Sonnet]** Scaffold the pnpm workspace — *Done when:* CI is green on a PR with one sample test per package, and a deliberate `Math.random()` in `packages/engine` fails lint.
  - Root `package.json` (scripts `typecheck`, `lint`, `test`, `parity`; engines Node 22/24), `pnpm-workspace.yaml`, a strict `tsconfig.base.json`, empty `packages/{shared,engine,recite,plant}` with Vitest 5.0.4, ESLint with the purity rule (no `react`, `react-native` or `expo-*` imports, no clock reads or `Math.random` in `packages/`), `.github/workflows/ci.yml` (install, typecheck, lint, Vitest), and `local/` in `.gitignore` for Thomas's database exports.
  - **Foot-gun:** pnpm 11+ reads `nodeLinker` and `allowBuilds` (the list of packages allowed to run install scripts) only from `pnpm-workspace.yaml`, not `.npmrc`. It also skips versions published less than a day ago by default.
  - **Foot-gun:** TypeScript 7.0 is npm "latest", but Expo pins ~6.0.3. Pin it and don't let tooling bump it.
- 0.14 **[Thomas]** Protect `main` (if 0.6 allows it): require a pull request with 1 approving review and the passing `ci` check, and block force-pushes — *Done when:* a test PR from Claude's account can't merge without Thomas's approval.
  - **Foot-gun:** GitHub lets you pick a required check only after it has run once, so this comes after 0.13.
- 0.15 **[Claude · Haiku]** Create the backlog with `gh`: a milestone per phase, issues for Phases 0 and 1 only, and a Project board (Backlog → Ready → In progress → In review → Done) — *Done when:* the Phase 0 and 1 issues match their steps.
  - Later phases get their issues when their plans are approved, because each plan re-splits its steps.

**Exit criteria:** spec and research committed; Apple membership active; iPhone registered with Dictation on; CI runs on every PR and `main` is protected; the church has the letter and the D-U-N-S is requested.

**Thomas checkpoint (≈1 h):** review the CLAUDE.md and decisions PRs and confirm gates 0.1 and 0.6.

### ➕ Phase 1 — Engine + content

**Status:** Not started · **Thomas time:** 8–15 h, about 3 h of it PR review

**Goal:** The learning engine runs as pure TypeScript and matches the Python reference card for card, and the Python exporter produces every content file the app will bundle.

**Prerequisites:** Phase 0's workspace; `data/bible.eng.db` on the Mac. It's git-ignored, so only the Mac can run the exporter.

- 1.1 **[Claude · Opus]** Plan `docs/plans/phase-1.md`: the passage YAML format, the bundle schema (App Architecture §7), the `CardSpec` shape, the card-key function and its namespace (§4), the golden-file format and the parity tolerances — *Done when:* Thomas approves the plan.
  - **Card-key namespace.** Keys are namespaced by a passage *family* (a shared outline subtree), not by passage id. Parts and containing passages (Farewell's three parts and the whole; Psalm 23 inside Psalms of Trust) reference the same outline anchors, so compile yields identical units and keys. Custom and group passages that overlap curated ones get their own namespace: no shared cards, and a verse's mastery takes the higher stability (§4). The release planner skips cards already introduced in another enrollment.
  - **Foot-gun:** keys are permanent once Thomas's review events exist (Phase 2) and sync to the server (Phase 6). Changing the scheme later means migrating the event log, the server and the goldens.
- 1.2 **[Claude · Sonnet]** Close the generator gaps in Python first, so the goldens cover them — *Done when:* `venv/bin/python -m unittest discover -s tests -t .` passes with new cases for Matt 18:1–11, a one-section Psalm 23 and the "I Am" collection, and trial 2's deck regenerates with the same cards.
  - A "collection" root of independent passages, across books, in `src/deck/tree.py` (it now unpacks exactly one book).
  - Gaps for BSB's 19 omitted verses: `verses_of()` raises on a range ending at one, e.g. Matt 18:11.
  - Passages with no outline: one leaf, no outline-phase cards. Fix the `report()` crash (`max()` over zero outline-phase cards).
  - Merge back-to-back heading blocks (Heb 11:30).
- 1.3 **[Claude · Sonnet]** Add the range-based card-key function and `contentHash` to Python (`src/deck/keys.py`, rules from 1.1 and App Architecture §4) — *Done when:* keys are unique across the Sermon on the Mount and Isaiah 40–44 decks; renaming one header changes only that header's card hashes; and with test outlines, enrolling in Farewell part 1 then the whole adds zero duplicate keys for shared units, and Psalms of Trust re-introduces no Psalm 23 card.
- 1.4 **[Claude · Sonnet]** Define `data/passages/*.yml` and build `python -m src.content build` — *Done when:* the alpha bundles validate, a second run produces no diff, and editing an outline without bumping its `outlineVersion` fails the build.
  - Format: id, family, title, shelf, ranges and an outline tree. Convert `data/outlines/sermon_on_the_mount.yml` and `isaiah_40_44.yml`, and draft Psalm 23 with two stanzas.
  - The exporter validates parts against the text, attaches red-letter flags, and writes `apps/mobile/assets/bundles/*.json` plus an `index.json` shelf manifest with sorted keys. Byte-stable output means git diffs show only real changes.
- 1.5 **[Claude · Sonnet]** Export `bsb.sqlite` (tables `book`, `verse`, `footnote`, `red_letter` and an FTS5 search index) and pin its source — *Done when:* tests confirm 31,086 verses, 1,955 Gospel red-letter verses and no Matt 18:11, and `scripts/fetch_bible_db.py` refuses a `bible.eng.db` whose SHA-256 doesn't match.
  - Red letters come from ENGWEBP's words-of-Jesus flags mapped to BSB references. Drop the 7 WEB-only verses. Never use `eng_our`, which also flags Old Testament passages.
  - Record the source URL, download date and SHA-256 of `bible.eng.db` in `data/README.md`. **Foot-gun:** it's an unpinned download from helloao, so a re-download can change every export with no code change.
  - `bsb.sqlite` is a binary: re-export it only when the BSB data or its schema changes. Its hash goes in `index.json`.
- 1.6 **[Claude · Sonnet]** Build the attribution table `packages/shared/attribution.ts` from the live API's `license` flags, fetched at export time, plus hand-written credit lines — *Done when:* BSB, the six public-domain commentaries, Tyndale (CC BY-SA 4.0) and OpenBible (CC BY 4.0) each have a credit line.
  - **Foot-gun:** `licenseNotice` in `bible.eng.db` is empty for all 51 translations. Don't trust it (research: content.md).
- 1.7 **[Claude · Sonnet]** `python -m src.content goldens` writes `fixtures/golden/<passage>.json` (the bundle, every `CardSpec` and the group order), stamped with a hash of the Python sources, the passage files and `bible.eng.db` that made it — *Done when:* editing a passage YAML without re-exporting fails CI.
  - **Foot-gun:** CI can't run the exporter (the database is git-ignored), so every Python change needs a re-export and a commit. The hash check catches the forgotten ones.
- 1.8 **[Claude · Sonnet]** `packages/shared`: zod 4 schemas for `PassageBundle`, `CardSpec`, `CardKey`, `Attempt`, `Rating`, `ReviewEvent` and settings, plus `VerseId` helpers (Matt 5:3 = 40005003) — *Done when:* every committed bundle and golden parses in Vitest.
- 1.9 **[Claude · Sonnet, Opus review]** `packages/engine` compile: port `tree.py`, `cards.py` and the grouping in `order.py` into `compile()`, which returns nodes, units, `CardSpec`s and release groups as data — *Done when:* every golden matches exactly, card for card.
- 1.10 **[Claude · Sonnet, Opus review]** The calendar release planner `planToday()` (App Architecture §4) — *Done when:* the release invariants pass on every golden and total days land within the plan's tolerance of Python's.
  - A group becomes eligible the local day after the group it waits on was *introduced*; the day rolls over at 4 a.m.; groups are introduced whole, up to the pace; at most 2 units are in waves 1–2; nothing is pulled forward; missed days add no backlog.
- 1.11 **[Claude · Sonnet, Opus review]** The `Scheduler` interface over ts-fsrs ^5.4.2 (FSRS-6 defaults, retention 0.90, one 10-minute step) — *Done when:* fixed rating sequences give the same stability, difficulty and due date as py-fsrs (`enable_fuzzing=False`, via a small Python export script) within tolerance.
  - **Foot-gun:** fuzz (a small random shift in due dates) makes replays non-reproducible. Every review stores its post-review snapshot as the truth, and replays run with fuzz off.
- 1.12 **[Claude · Sonnet, Opus review]** Grader, mastery, session builder and `diffCompiled` — *Done when:* table-driven tests cover every row of the grade table below and every mastery and session rule, and renaming a header or moving a unit boundary produces the expected keep/reset/retire/add lists.
  - **Grade table** (R7; App Architecture §4 is the source of truth, and the "How this was graded" footer quotes it). This is trial 2's type-mode rule (`src/deck/assets/card.js`).

    | Grade | When |
    |---|---|
    | Again | A hint, a peek or "Show me" was used, or 2+ words were missed |
    | Good | 0 words missed, at most 1 close, fewer than 2 hesitations |
    | Hard | Everything else (so 1 missed word is Hard). Hesitations lower Good to Hard, never to Again |
    | Easy | Only Read-through and Preview (always), and Fill in the blanks / First letters at 100% with no hesitations |

  - Mastery: the governing card is the unit's Header→text; bud, leaf, full leaf at 7 days, rooted at 21 days of stability; a verse in two families takes the higher stability.
  - Session: thirstiest due cards first, then today's new groups; Again returns within the session; a catch-up after 3+ days away is capped at 10 minutes and adds no new groups.
- 1.13 **[Claude · Sonnet]** Simulation parity: a TS script ports the simulated learner in `scripts/simulate_fsrs.py` (same rating odds and seconds per step kind, averaged over runs) — *Done when:* fed the Python card order, it matches the Python run's daily totals within the plan's tolerance, and run on the TS planner at paces 6, 12 and 18 (Gentle, Steady, Ambitious) it writes a per-pace minutes table to `docs/` (replacing the extrapolated minutes in Robust Learning Algorithm's pace table).
- 1.14 **[Thomas]** When trial 2 ends, export the Isaiah 40–44 deck from Anki with scheduling information included, into `output/isa_trial_2/` — *Done when:* the file is there. It feeds the import decision (2.1) and grading calibration (5.14, 9.4).
- 1.15 **[Claude · Opus]** Phase review (`/code-review high`), fixes and the Status update — *Done when:* no high findings remain open.

**Exit criteria:** `pnpm parity` is green in CI; the bundles, `bsb.sqlite`, goldens and attribution table are committed; each generator gap has a test; the card-key namespace is decided and tested.

**Thomas checkpoint (≈1–2 h):** read the parity report and the per-pace minutes table; spot-check Psalm 23's cards in a preview Claude renders from the `CardSpec`s.

### ➕ Phase 2 — Personal alpha: the study loop

**Status:** Not started · **Thomas time:** 15–25 h, about 5 h of it PR review

**Goal:** Thomas studies daily on his iPhone in a dev build, offline, with real passages, every step type, typed and self-check grading, and a daily reminder.

**Prerequisites:** Phase 1's exit criteria; the iPhone registered (0.4).

- 2.1 **[Thomas]** **Gate: words, look and history** — *Done when:* recorded in `docs/decisions.md`.
  - The word for journeys: "Passages" (recommended), Plantings, Paths or Gardens.
  - A custom-branded look on both platforms (recommended) or platform-native components.
  - Import the trial 2 Anki history so Isaiah 40–44 continues in the app? Claude sizes the work in the plan. Proposed: only if the 1.14 export maps cleanly onto card keys.
- 2.2 **[Claude · Opus]** Plan `docs/plans/phase-2.md`: routes (App Architecture §11), tables (§8), the session state machine, the first-run flow (Beautiful UI → Key screens), and the UI checklist from Beautiful UI and R13 — *Done when:* Thomas approves.
- 2.3 **[Claude → Thomas · Sonnet]** Create `apps/mobile` with `npx create-expo-app@latest` (SDK 57, expo ≥ 57.0.28) and `npx expo install expo-dev-client`. `app.config.ts` reads `APP_VARIANT` and sets the dev bundle ID — *Done when:* `npx expo run:ios` opens on the simulator and, with **[Thomas]** plugging in the iPhone, `npx expo run:ios --device` installs on it.
  - If SDK 58 has been stable for 2+ weeks by then, start on 58 and skip 7.10 (R4).
  - **Foot-gun:** add every native package with `npx expo install`, never `pnpm add`, and keep `npx expo install --check` clean. npm's "latest" Reanimated, Skia and TypeScript are newer than SDK 57 supports.
  - **Foot-gun:** no Expo Go; development builds only. Duplicate copies of `react` or `react-native` in the monorepo break the app (fallback: `nodeLinker: hoisted`).
- 2.4 **[Claude · Sonnet]** Design tokens and a style tile: Uniwind and HeroUI Native via `npx expo install`, one `global.css` with light and dark tokens (garden palette; type scale with verse text ≥ 20 pt; radii; spacing), and a script that checks every text/background pair for 7:1 contrast — *Done when:* the contrast script passes in CI and **[Thomas]** approves the tile's screenshots (light/dark × default/AX5).
- 2.5 **[Claude · Sonnet, Opus review]** The database: expo-sqlite with Drizzle 0.45.x, tables from App Architecture §8 (including `outbox` and the capped `app_log` from day one), opened with `enableChangeListener: true`; migrations applied by `useMigrations` before the first screen — *Done when:* jest-expo tests prove an atomic review write, that card states rebuilt from events match the cached ones, and that migration reaches head both from empty and from a populated snapshot of each earlier schema version, with identical rebuilt card states.
  - Snapshots are committed fixtures, one per schema version, seeded from Thomas's exports (his own study data; no one else's).
  - Before applying any migration, the app copies `app.db` to its Documents folder and keeps the last 3 copies.
  - One review writes the event, card state, attempt and outbox row inside `withExclusiveTransactionAsync`; the plain `withTransactionAsync` lets unrelated queries slip in. Ids are UUIDv7, with `react-native-get-random-values` imported first.
  - **Foot-gun:** Drizzle's Expo page now says to install the v1 release candidate. Stay on 0.45.x and don't mix the two versions' docs.
  - **Foot-gun:** without the babel inline-import plugin and `sql` in Metro's `sourceExts`, migrations silently don't load.
- 2.6 **[Claude · Sonnet]** Content: load `bsb.sqlite` from the app's assets as a read-only database that each app update replaces whole (never migrated), load the bundles, and enroll in the alpha passages (Psalm 23, Sermon on the Mount, Isaiah 40–44) — *Done when:* enrolling in each passage produces the same cards as its golden.
- 2.7 **[Claude · Sonnet, Opus review]** Content upgrade on launch — *Done when:* a test upgrades a populated database from Psalm 23 v1 to v2 and only the expected cards reset.
  - For each enrollment whose bundled `outlineVersion` or `generatorVersion` is newer, compile the old version (kept in the `passages` table, §8) and the new one, run `diffCompiled`, and write the reset and retire events plus the enrollment bump in one exclusive transaction.
  - Replace the on-device `bsb.sqlite` when the hash in `index.json` changes.
  - **Foot-gun:** without this step, any outline fix shipped in an update (5.4 revises outlines Thomas is already studying) silently breaks progress or crashes.
- 2.8 **[Claude · Sonnet]** The app shell: expo-router tabs Today, Passages and More (Groups arrives in Phase 7), `session/[id]` and `passage/[id]`, with a Zustand session store driving idle → prompt → attempt → revealed → next, and a pause on backgrounding — *Done when:* jest-expo tests cover every state transition, including "Stop for today" and each passage-menu action.
  - "Stop for today" on every step saves progress and goes to the session-end screen; stopping early is never a failure.
  - The passage menu: Pause (no new steps or reviews until resumed), Start over and Remove (history stays in the log), each confirmed in plain words (Features → Beautiful UI → Help and recovery).
  - **Foot-gun:** SDK 57's native tabs import from `expo-router/unstable-native-tabs`; the stable path arrives in SDK 58.
  - **Foot-gun:** React Native Testing Library 14 made `render`, `fireEvent` and `act` async. Tests copied from older examples fail; run RNTL's v14 codemods.
- 2.9 **[Claude · Sonnet]** Step renderers for all 14 `CardKind`s, drawn from `CardSpec` data — *Done when:* each kind has a screenshot set (light/dark × default/AX5) that passes the UI checklist, and every interactive element has a `testID`.
  - Plain step names (R10); a stage-colored banner; the map strip, which collapses to a one-line breadcrumb at large text sizes and opens the full map on tap; the same layout on every step at a given text size; answers revealed in place; the "How this was graded" footer quoting the 1.12 grade table.
  - "How to do this step": a one-line panel the first 2 times each step kind appears, and a **How?** link that reopens it (separate from the study-helps **?**).
- 2.10 **[Claude · Sonnet]** Attempts without voice — *Done when:* a Maestro flow completes a full session in each mode and the logged ratings match the 1.12 grade table.
  - Typed first letters: adjacent-key slips forgiven, a word counts as missed after 2 wrong letters, and each error gives a haptic plus a visual cue.
  - Self-check: show the text, then tap the words you missed.
  - The result line in the wording of Features → Robust Learning Algorithm ("Well done. See you again in 3 days."), with a small "Grade it differently" link offering the four plain choices. Both `autoRating` and `finalRating` are logged.
- 2.11 **[Claude · Sonnet]** Today and session end: the "Today · about N minutes" button from the session builder, the thirsty count, a "days studied this week" line and a static plant placeholder. A dev menu (dev variant only) offers a clock offset for testing the planner, database export and reset — *Done when:* the clock offset walks a passage through waves 1–3 on the simulator as the plan predicts.
  - Reset exports the database first and requires typing RESET, because Thomas's daily build is the dev variant.
- 2.12 **[Claude → Thomas · Sonnet]** Reminders: one opt-in repeating daily notification with expo-notifications ~57.0.22, a `setNotificationHandler` and an Android channel — *Done when:* **[Thomas]** reports the reminder arriving at the chosen time on 3 days in a row.
  - **Foot-gun:** iOS keeps only the 64 soonest pending local notifications. Reschedule on every app open, and never call `removeAllPendingNotificationRequests` anywhere else; it silently wipes the reminder.
- 2.13 **[Claude · Sonnet]** The first-run flow and a minimal More → Settings (pace, rhythm, reminder) — *Done when:* Maestro covers the first run, and if 2.1 said import, Isaiah's due counts after an import match Anki's within a day.
  - The flow from Beautiful UI → Key screens: Welcome; an "Is this text easy to read?" size preview; then straight into the first passage's first step on the defaults (Gentle pace; 5 days a week with Sunday rest; pending 5.2). The microphone is explained at the first voice step (Phase 3), and the reminder is offered after the first session ends. Thomas switches himself to Steady in More.
  - If 2.1 said yes: a Python script turns the Anki export into review events keyed by card key, imported through the dev menu with `mode: anki-import`.
- 2.14 **[Claude · Sonnet]** The UI self-review loop on every screen (Development Workflow → Self-check loops), through the Simulator pane or Expo MCP (`npx expo install expo-mcp --dev`, then `EXPO_UNSTABLE_MCP_SERVER=1 npx expo start`) — *Done when:* every screen passes the checklist, with screenshot sets in its PR.
  - **Foot-gun:** simulator screenshots go to Anthropic, so the simulator only ever holds test data and test accounts. Expo MCP allows one dev-server connection and must reconnect after each restart.
- 2.15 **[Claude → Thomas · Sonnet]** A Release build on the iPhone (`npx expo run:ios --device --configuration Release`, which runs without the Mac's dev server) and a device test script — *Done when:* Thomas has studied 3 days in a row without a blocking bug.
- 2.16 **[Claude · Opus]** Phase review, fixes and the Status update — *Done when:* no high findings remain open.

**Exit criteria:** Thomas studies daily on the Release build; the Maestro flows for the first run and both input modes pass; migration and content-upgrade tests run in CI; no data-loss bug is open.

**Thomas checkpoint (≈2 h):** run the device script; collect friction notes in one issue; confirm the 2.1 choices still feel right on the phone.

### ➕ Phase 3 — Voice

**Status:** Not started · **Thomas time:** 10–18 h, about 3 h of it PR review

**Goal:** Thomas recites into the iPhone and watches the live trail; the app grades voice attempts and keeps trail history; audio never leaves the phone.

**Prerequisites:** Phase 2's session screens; Dictation on (0.4).

- 3.1 **[Thomas]** **Gate: voice grading** — *Done when:* recorded.
  - May voice ever record Again without asking, or does it always suggest and wait for a confirm (recommended)?
  - Do "close" words count as correct for grading, or only for coloring?
  - Show tentative words (the recognizer's current guess) live, or only confirmed ones?
- 3.2 **[Claude · Opus]** Plan from App Architecture §5 and research: stt.md — *Done when:* Thomas approves.
- 3.3 **[Claude · Sonnet, Opus review]** The `packages/recite` normalizer — *Done when:* Vitest covers each rule on real BSB verses.
  - Lowercase; strip punctuation; curly quotes to ASCII; split dashes and hyphens (keeping the hyphenated form as an alias); numerals to words with the digits as an alias ("46,500" in Num 1:21); "LORD"; contractions; fillers dropped; Double Metaphone codes (a phonetic encoding, so sound-alike words match).
  - Bias list: the passage's proper nouns only (≤ 100, 1–2 words each). Never the whole verse, which pushes the recognizer toward the right answer and flatters the user.
- 3.4 **[Claude · Sonnet, Opus review]** The aligner, word states, trail encoding and the `replay` engine (App Architecture §5) — *Done when:* hand-written fixtures for skips, repeats, jumps, pauses and proper nouns ("Melchi zedek") pass, and a benchmark shows under 5 ms per partial result.
- 3.5 **[Claude · Sonnet, Opus review]** The `ios-sfspeech` adapter in `apps/mobile/src/stt/`, on expo-speech-recognition 57.1.x (`npx expo install`) — *Done when:* a unit test proves `start()` refuses when the probe fails, and the app then shows the "Turn on voice" card (Features → Real-Time Recital Matching → Privacy and turning voice on): an Open Settings button (`Linking.openSettings()`), 3 illustrated steps for turning on Dictation, and an equally large "Use typing instead".
  - Emits "replace segment N" events, which absorb iOS 18's reset after a pause. Stops on card change and on backgrounding. Restores the iOS audio session on stop. Keeps the screen awake only while listening.
  - **Foot-gun (the privacy gate):** `requiresOnDeviceRecognition` is silently ignored when the device can't recognize on-device, and audio may then go to Apple's servers. `probe()` must check `supportsOnDeviceRecognition()` and `start()` must refuse otherwise. Never set `recordingOptions.persist`.
- 3.6 **[Claude → Thomas · Sonnet]** Permissions and logs: one Seedling screen that explains both system prompts (microphone and speech recognition) before either appears, with "Not now" continuing without voice; the same "Turn on voice" card after a "Don't Allow"; specific `NSMicrophoneUsageDescription` and `NSSpeechRecognitionUsageDescription` strings (the plugin's default text is generic and risks rejection); a dev-menu export of a session's text-only hypothesis log, never audio — *Done when:* Thomas approves the wording.
- 3.7 **[Thomas]** Record fixture sessions on the iPhone from Claude's script (about 2 h), and export each log to `fixtures/stt/` — *Done when:* the logs are committed (text only).
  - Clean Psalm 23; a Sermon section with deliberate skips, repeats and a jump back; Isaiah's proper nouns; long pauses; a 450-word section recitation; a noisy room.
- 3.8 **[Claude · Sonnet]** A replay suite over Thomas's logs; tune the aligner against them — *Done when:* the suite is green and its grades match what Thomas says he actually did.
  - **Foot-gun:** speech recognition is broken in iOS 26.4+ simulators (expo-speech-recognition issue #145). The simulator runs the `replay` engine, and live voice is tested only on the iPhone.
- 3.9 **[Claude · Sonnet]** The karaoke trail UI (Real-Time Recital Matching → What the user sees) — *Done when:* replay-driven screenshots pass the UI checklist and VoiceOver reads the result.
  - A fixed marker; the trail above it; text ahead that depends on the step; word states as color plus shape on blue/orange; "Need a nudge?" after 6 s (adjustable); listening stops after about 15 s of silence (adjustable, never below 6 s; Proposed, generous because older reciters pause to remember); Reduce Motion jumps a line at a time.
- 3.10 **[Claude · Sonnet]** Voice attempts into the grader: `finish()` → `Attempt` → a suggested grade (1.12 table), capped at Hard with "Did you say it right?" when most misses are proper nouns. Trail rows store `states`, `insertions`, `engineId`, `engineVersion` and both ratings — *Done when:* replay tests produce the expected attempts and rows.
- 3.11 **[Claude · Sonnet]** Trail history (`trail/[cardKey]`: one strip per attempt, compared only when the card hash and engine match) and **Recite freely** (any branch of the map, chained at section boundaries, schedule untouched, check-up prompts at 30, 60 and 90 days) — *Done when:* Maestro flows on the replay engine cover both.
- 3.12 **[Claude → Thomas · Sonnet]** A device test script: the live trail on every recall step type, latency (target: a word colored within about 0.7 s), a 450-word recitation, battery and heat over 15 minutes, airplane mode — *Done when:* Thomas reports pass, with the measured numbers in the PR.
- 3.13 **[Claude · Sonnet, Opus review]** *(Optional)* A SpeechAnalyzer local module (`npx create-expo-module@latest --local` → `apps/mobile/modules/speech-analyzer`, Swift, iOS 26+) — *Done when:* it passes the same device script and the A/B result is in `docs/decisions.md`. If skipped, it moves to 9.15.
  - SpeechTranscriber with volatile results, falling back to DictationTranscriber where it's unavailable. This path needs only the microphone permission. Thomas picks the default by reciting the same scripts with each engine.
  - **Foot-gun:** SpeechTranscriber accepts no `contextualStrings`. The expo-speech-transcriber package looks like a shortcut, but it hasn't been published since Dec 2025 and hardcodes en_US.
- 3.14 **[Claude · Opus]** Phase review plus `/security-review` of the privacy gate, fixes and the Status update — *Done when:* no high findings remain open.

**Exit criteria:** Thomas recites daily on the iPhone; the replay suite runs in CI; a unit test proves the recording options never persist audio.

**Thomas checkpoint (≈1 h):** run the device script and judge how lenient the grading feels on his own voice.

### ➕ Phase 4 — Plant

**Status:** Not started · **Thomas time:** 4–8 h, about 1 h of it PR review

**Goal:** Thomas's real progress grows a deterministic plant on Today, with gentle "thirsty" leaves. The home-screen widget is public-launch scope (9.13).

**Prerequisites:** Phase 2 (mastery data from real study). It can overlap Phase 3.

- 4.0 **[Thomas]** Export the database from the dev menu and AirDrop it to the Mac into the git-ignored `local/` folder — *Done when:* the file is there.
- 4.1 **[Claude → Thomas · Opus]** Plan plus three art-direction options rendered from Thomas's real data (4.0): leaf species per passage or genre, palette, setting. The default proposal is procedural branches with a small set of drawn leaf and blossom sprites — *Done when:* Thomas approves the plan.
- 4.2 **[Thomas]** **Gate: art direction**, and the placeholder stage thresholds (sapling at 50 rooted verses, young tree at 300, tree at 1,000) — *Done when:* recorded.
- 4.3 **[Claude · Sonnet]** `growPlant(input: PlantInput)` in `packages/plant` (App Architecture §6) — *Done when:* Vitest proves determinism (same input → same geometry hash), that editing one section changes only that branch, and that structure never shrinks.
  - An inline hash and sfc32 PRNG per node; branch length by the square root of words; Leonardo widths; golden-angle leaves; branch growth from outline-step stability; leaf stages; droop capped at 30° and 35% desaturation; dispatch on `renderVersion`.
- 4.4 **[Claude · Sonnet]** The engine → `PlantInput` adapter (mastery, R per leaf, blossoms, fruit) and the `plant_cache` table — *Done when:* tests over a simulated 90-day history produce the expected stages.
- 4.5 **[Claude · Sonnet]** The Skia renderer: `@shopify/react-native-skia` 2.6.2 and Reanimated 4.5.1 via `npx expo install`; tapered Paths with an animated `end` trim; all leaves in one Atlas call; a crossfade under Reduce Motion; the VoiceOver summary — *Done when:* screenshots pass the checklist and the label reads correctly.
  - **Foot-gun:** Skia v3 ships under a new name, `react-native-skia`. Stay on the Expo-pinned `@shopify` package and never install both.
  - **Foot-gun:** interpolate colors with Skia's `interpolateColors`, not Reanimated's `interpolateColor`.
- 4.6 **[Claude · Sonnet]** The plant on Today, the growth animation at session end (a "watering" sparkle) and the full-screen `plant` route — *Done when:* a Maestro flow shows growth after a session.
- 4.7 **[Claude → Thomas · Sonnet]** **Gate: performance.** A 2,461-leaf stress plant (all of Psalms) on the iPhone, with frame times reported — *Done when:* Thomas decides from the numbers whether leaves group by chapter beyond about 500 verses, and it's recorded.
- 4.8 **[Claude · Opus]** Phase review, fixes and the Status update — *Done when:* no high findings remain open.

**Exit criteria:** the plant reflects real mastery; determinism tests run in CI.

**Thomas checkpoint (≈1 h):** live with the plant for a week. Do thirsty leaves feel gentle, or like a reproach?

### ➕ Phase 5 — Personal-complete

**Status:** Not started · **Thomas time:** 14–24 h, about 4 h of it PR review

**Goal:** Everything a church member needs in the beta works on one phone and suits older, less tech-savvy users. Other translations, pasted text, the widget and the remaining articles wait for Phase 9 (public-launch scope). The phase ends with a go/no-go for the church beta.

**Prerequisites:** Phases 2–4; the church's answers from 0.9.

- 5.1 **[Thomas + church]** **Gate: content defaults.** Claude prepares a one-page options memo — *Done when:* recorded.
  - Ten Commandments numbering tradition, and the Farewell Discourse boundary (13:31 or 14:1).
  - Teachings of Jesus: include the red-letter verses in Acts and Revelation? De-duplicate parallel passages?
  - Which commentary leads: JFB (public domain, verse by verse, older language) or Tyndale (modern, quotes the NLT)?
- 5.2 **[Thomas]** **Gate: product defaults** — *Done when:* recorded.
  - Default pace: Gentle (6 new steps a day; recommended) or Steady (12). Rhythm: 5 days with Sunday as a rest day (recommended), changeable in More.
  - Confirm the first-run flow (Features → Beautiful UI → Key screens → First run).
  - First passage: Psalm 23 for everyone (recommended), or choose? Let a known passage be placed as rooted after one good recitation? Label paces by minutes (recommended)?
  - "Learn the outline only" and list-style sections (`style: list`): beta or later (Proposed: later, Phase 11; if beta, the plan adds a step).
  - Confirm the study-help rule (Proposed): anonymous downloads from helloao start only after a first-use consent prompt, and that prompt is the R3 opt-in. Users known to be under 13 (they answered the age screen so, or expo-age-range reports it) never see the prompt; everyone else does.
  - Confirm: KJV/WEB and pasted text wait for public launch (9.12; Proposed).
  - AI questions about a verse: yes, no or later (Proposed: later, Phase 11).
- 5.3 **[Claude · Opus]** Plan — *Done when:* Thomas approves.
- 5.4 **[Claude → Thomas + church · Opus drafts, Sonnet converts]** Author the 10-passage starter shelf in `data/passages/` (Core Journies table), then re-export bundles and goldens — *Done when:* the outline lint is green; Thomas approves each review packet; the pastor approves the interpretive headings (Ten Commandments, Psalms); and for passages already in use (Psalm 23, the Sermon), `outlineVersion` is bumped and 2.7's upgrade test passes.
  - Hand outlines are theological judgments ("Love the LORD", stanza titles), so Opus drafts them and Sonnet does the YAML and re-export.
  - Hand outlines for Psalm 23, the Ten Commandments, the Psalms of Trust stanzas, the "I Am" sayings and the Ascents triads. The Farewell Discourse comes whole and as three parts in one family (1.1), and Psalms of Trust shares Psalm 23's anchors.
  - Exporter lint: headings ≤ 6 words, no heading repeats its parent, siblings distinct, units within 80/130 words, full verse coverage.
  - A review packet per passage: the outline beside the BSB text, card counts, days at each pace, and differences from BSB's headings.
- 5.5 **[Claude · Sonnet, Opus review]** Custom passages and the outline editor — *Done when:* a device-built bundle compiles to the same cards as the Python bundle for the same ranges, and a Maestro flow edits a passage mid-study and resets only the expected cards.
  - Picker: book → chapter → verse grids and a typed-reference parser (a TS port of `src/refs.py`); collections across books; omitted verses shown as a gap with a note; a size preview ("107 verses · about 356 steps · about 60 days at Gentle pace"); a split suggestion above about 150 verses. The device builds the bundle from `bsb.sqlite` in the curated shape.
  - Editor: tree rows with buttons (rename, split, merge, indent, move a boundary; nothing drag- or swipe-only); paste an indented outline; plain-word validation; the recompile diff behind "Changed sections restart their outline steps. Your verse progress stays."
- 5.6 **[Claude · Sonnet]** The study-helps sheet (`notes/[verseId]`) — *Done when:* a Maestro flow opens helps mid-session and resumes on the same step, and a test proves no request is made before consent or for a known under-13 user.
  - Commentary led per 5.1. Tyndale is shown unmodified with "These notes quote the NLT" and is never AI-summarized. The top 5 OpenBible cross-references open the BSB verse in place. Per-chapter caching; the first-use consent prompt (5.2); the mic and silence timer pause while the sheet is open; on recall steps "?" appears only after grading.
- 5.7 **[Claude → Thomas + church · Opus]** Draft the five beta articles (Into Material table: 150–250 words each, BSB quotes taken from the bundle, a Sources fold): Why memorize?, Why the outline first?, Why say it aloud?, Why does the app grade for me? and Why is it free? Also script an optional 60–90 s welcome video — *Done when:* Thomas and the pastor approve the voice and the theology. The other six articles come in 9.11.
- 5.8 **[Claude · Sonnet]** Article rendering, More → Learn (the library), the in-context "Why?" links, and the Welcome screen's optional video (bundled, so nothing loads before opt-in; Thomas records it if wanted) — *Done when:* a Maestro flow opens each "Why?" link and returns to the same step, and the screenshot sets pass the checklist.
- 5.9 **[Claude · Sonnet]** Motivation (R12) — *Done when:* clock-offset tests cover each rule and a no-guilt word list passes over all copy.
  - A weekly goal of 3–7 days; rest days; repair by studying within 2 days; a capped 10-minute catch-up after 3+ days away (thirstiest first, no new steps); fresh-start wording on Mondays and the 1st; a reminder that drops to weekly after 3 ignored, and says so.
- 5.10 **[Claude · Sonnet]** The accessibility pass (R13): every screen at AX5, VoiceOver order and labels, Reduce Motion, 56 pt primary buttons, 44 pt targets, adjustable silence timeouts, and the "Help someone set up" mode — *Done when:* every screen passes the checklist at AX5 with VoiceOver on, and a Maestro flow plays "Hear it" on a Read it aloud step.
  - **"Hear it"**: on-device text-to-speech with expo-speech (`npx expo install expo-speech`; iOS's built-in voice, offline, sends nothing) and a speed control, on Read it aloud, See the outline, revealed answers and the articles. Never on a recall step before its answer is revealed.
- 5.11 **[Claude · Sonnet]** More → Settings and About: input default, haptics and sound toggles, a text-size preview, pace, rhythm and reminder; About and Credits from the attribution table; in-app links to the privacy policy, terms and support pages (placeholders until 8.6 publishes them); More → Help with short how-to videos (Claude scripts them, **[Thomas]** records them on the iPhone) and "Ask {church contact}" — *Done when:* a Maestro flow reaches every setting and link, and the screenshots pass.
- 5.12 **[Claude · Sonnet]** Pace and time estimates from the 1.13 simulation shown in the UI (paces labeled by days and minutes, not cards) — *Done when:* the picker's estimates match the simulation table.
- 5.13 **[Thomas]** Export the database again, as in 4.0 — *Done when:* the file is in `local/`.
- 5.14 **[Claude · Sonnet]** First grading calibration from Thomas's own `autoRating` vs `finalRating` logs (5.13) and the trial 2 export (1.14) — *Done when:* a short report in `docs/rnd/` proposes threshold changes and Thomas accepts or declines each.
- 5.15 **[Claude → Thomas + church · Sonnet]** The app icon, splash screen and per-variant icons (the dev variant visibly marked), so no upload ever ships Expo's placeholder — *Done when:* the church approves the icon.
- 5.16 **[Claude → Thomas · Sonnet]** An informal-test kit: a `demo` app variant (its own bundle ID and empty data, so testers never touch Thomas's progress), a 20-minute task script and an observation sheet. Hypothesis logging is off in this variant — *Done when:* the demo build is on Thomas's iPhone.
- 5.17 **[Thomas]** Run the informal test with 3–5 church members aged 60+ on Thomas's iPhone: the first run, text size, one session by voice and by typing, the tone of thirsty leaves — *Done when:* the observation sheets are summarized in one issue and Claude has turned them into fixes or deferrals.
- 5.18 **[Claude · Opus]** Phase review, fixes and the Status update — *Done when:* no high findings remain open.
- 5.19 **[Thomas]** **Gate: beta go/no-go** — *Done when:* "go" is recorded.
  - Thomas has studied daily for at least 6 weeks since Phase 2 (Proposed), including 30+ days on one long passage.
  - No crash or data-loss bug for 2 weeks; findings from 5.17 fixed or deliberately deferred.
  - The church's Apple Organization team is active (0.10).

**Exit criteria:** the starter shelf, custom passages, study helps, the five articles and rhythm all work offline; the accessibility checklist passes; the beta is a "go".

**Thomas checkpoint (≈2 h):** the older-member test and the go/no-go itself.

### ➕ Phase 6 — Backend + accounts

**Status:** Not started · **Thomas time:** 14–22 h, about 4 h of it PR review

**Goal:** Opt-in accounts back up and sync study data across devices and can be deleted from the app, on Terraform-managed GCP that Claude's shell can reach only in dev, with tested rollback and restore.

**Prerequisites:** the 5.19 "go" (6.1–6.4 may start during Phase 5's dogfood weeks); a payment method for a GCP billing account.

- 6.1 **[Thomas]** **Gate: accounts and cloud** — *Done when:* recorded.
  - Sign-in: Apple + Google are decided (R3). Add email-link sign-in for less tech-savvy testers?
  - GCP billing: Thomas's card or a church billing account?
  - A hosted dev backend (+≈$9.50/month) or laptop-only dev? Laptop-only is enough for simulator work; testing sync on the iPhone away from home needs the hosted one.
  - Trails: sync inside review events (Proposed), or keep them on the device?
  - Pasted text: kept out of Seedling's account backup (Proposed; the user's own iCloud backup and the 8.12 export file still carry it), or backed up end-to-end encrypted?
  - Any testers in Texas? If yes, expo-age-range lands before the beta (Texas SB2420, the state's app-store age law).
- 6.2 **[Claude · Opus]** Plan, with a threat model from App Architecture §15 and the sync test matrix — *Done when:* Thomas approves.
- 6.3 **[Claude · Sonnet, Opus review]** Write the Terraform: `infra/bootstrap`, `infra/modules/{auth,db,api}` and `infra/envs/{dev,prod}`; all IAM lives in bootstrap with Terraform 1.16 and `google`/`google-beta ~> 8.7` (App Architecture §13) — *Done when:* `terraform fmt -check` and `terraform validate` pass for every root.
  - Bootstrap: versioned state buckets; the Workload Identity pool and provider (WIF: GitHub proves "this is repo X on main" and Google trusts it), with an attribute condition (a rule on GitHub's token claims) pinned to the repo's numeric id and `main`; the agent, `tf-dev`, deployer and runtime service accounts; the agent's Google account as Token Creator on the agent service account only; budgets of $15 (dev) and $25 (prod).
  - **`tf-dev`** is a second dev-only service account with the broader roles `terraform apply` needs in dev (creating Firebase, Identity Platform, Cloud SQL, Cloud Run and dev IAM bindings), which the agent account lacks. Nobody holds a standing grant on it; Thomas adds a grant that expires, per session (6.5). It has no roles in prod. App Architecture §13 lists it.
  - `lifecycle { prevent_destroy = true }` on the Cloud SQL instance and the state buckets, so Terraform refuses any plan that deletes them.
  - A Cloud Monitoring uptime check on `/v1/health` and an alert on the 5xx (server error) rate, emailing Thomas (§16).
  - **Foot-gun:** Firebase's own Terraform guide pins provider 6.0, which is stale, and Firebase project and app resources still need `google-beta`.
  - **Foot-gun:** Cloud SQL on Postgres 16+ defaults to Enterprise Plus, so db-f1-micro fails without `edition = "ENTERPRISE"`.
  - **Foot-gun:** Cloud Run needs `invoker_iam_disabled = true` (the Firebase token and a Cloud Run IAM token can't share one Authorization header) and `ignore_changes` on the image, so CI deploys and Terraform don't fight.
  - **Foot-gun:** a Workload Identity provider without an attribute condition lets any GitHub repo in.
- 6.4 **[Thomas]** Bootstrap and the credential wall (about 3 h; Claude guides in chat but doesn't run these) — *Done when:* from Claude's shell, `gcloud auth list` shows no owner account, the ADC identity is the agent service account, `gcloud projects describe seedling-prod` fails under every gcloud configuration, and Claude can list Cloud Run services in `seedling-dev`.
  - **Why (this is the part people get wrong):** Claude's shell runs as Thomas's macOS user, so it can use any credential that user can read. Impersonation borrows a token using the login stored in `~/.config/gcloud`; if that login is Thomas's owner account, Claude can reach prod with it, whatever the active configuration says. ADC (Application Default Credentials, the login that Terraform and other libraries read) is separate from gcloud's configurations, and deny rules are only prefix matches. So the wall is: no owner credential on the macOS user Claude runs as.
  - **Owner work happens elsewhere.** Create a separate macOS user (e.g. "Seedling Admin") with its own clone of the repo, or use Cloud Shell (Google's browser terminal). Bootstrap, prod `plan`/`apply` and prod admin scripts run only there. Like a separate Unix account, its home folder isn't readable from Claude's.
  - In that admin user: create the billing account (needed from the first apply: managing Identity Platform through Terraform requires Firebase's Blaze plan, although usage stays free); create `seedling-dev` and `seedling-prod`, link billing and accept the Firebase terms; run `gcloud auth login` and `gcloud auth application-default login` (your owner login, for gcloud and for Terraform), then `terraform -chdir=infra/bootstrap init` and `terraform -chdir=infra/bootstrap apply`. `-chdir` runs Terraform in that folder, `init` downloads the providers, and `apply` prints the plan and waits for "yes". Bootstrap starts with local state, because its bucket doesn't exist yet; Claude's plan moves that state into the bucket afterwards.
  - **The agent's identity.** Create a dedicated Google account for the agent (e.g. a new Gmail address) with no project roles; bootstrap grants it Token Creator on `claude-agent@seedling-dev` only. On Thomas's normal macOS user, run the five commands in Development Workflow → "How the impersonation works": they point gcloud at Claude's own folder (`CLOUDSDK_CONFIG=$HOME/.config/gcloud-seedling-agent`), sign in there as the agent account (not Thomas's), set impersonation of `claude-agent` and the dev project, and write ADC impersonating the same account. Claude then sets `CLOUDSDK_CONFIG` and `GOOGLE_APPLICATION_CREDENTIALS` (the ADC file inside that folder) in `.claude/settings.json`'s `env`.
  - If Thomas's owner login was ever used on the normal macOS user, remove it there: `gcloud auth revoke <owner email>` and `gcloud auth application-default revoke`. A browser signed in to the Cloud console as owner is also owner access; Claude never drives it.
  - On GitHub: a `production` Environment with Thomas as required reviewer (see 0.6), and the Workload Identity provider and deployer account as Actions variables.
- 6.5 **[Claude · Sonnet]** `terraform apply` in `infra/envs/dev` through `tf-dev`: the Firebase project and apps, Identity Platform, the dev-only test sign-in (6.9), plus Cloud SQL and Cloud Run only if 6.1 chose a hosted dev backend — *Done when:* the apply is clean and a second `plan` shows no changes.
  - Per session, **[Thomas]** in Cloud Shell or the admin user grants the `claude-agent` service account (the identity Claude already acts as) Token Creator on `tf-dev`, with an IAM condition that expires: `gcloud iam service-accounts add-iam-policy-binding tf-dev@seedling-dev.iam.gserviceaccount.com --member=serviceAccount:claude-agent@seedling-dev.iam.gserviceaccount.com --role=roles/iam.serviceAccountTokenCreator --condition='expression=request.time < timestamp("<session end, UTC>"),title=tf-session'`. The condition makes the grant lapse by itself at that time. Claude then runs Terraform with `GOOGLE_IMPERSONATE_SERVICE_ACCOUNT=tf-dev@seedling-dev.iam.gserviceaccount.com`, borrowing `tf-dev` through `claude-agent` (a chained impersonation).
  - **Foot-gun:** Terraform state stores the Identity Platform API key in plain text, so the state buckets are secrets.
  - **Foot-gun:** stopping a Cloud SQL instance saves almost nothing (its idle IP costs nearly as much); delete unused dev instances instead. Budgets only alert, sometimes hours late; they never stop spending.
- 6.6 **[Thomas]** Sign-in providers for dev — *Done when:* both providers show Enabled in `seedling-dev`.
  - Apple, in Thomas's team: turn on Sign in with Apple for the dev bundle ID; create a Services ID (Apple's ID for the web-style sign-in flow Firebase uses) and a Sign in with Apple key (.p8); paste the key into `seedling-dev`'s Apple provider yourself. Terraform doesn't manage that secret, so it never lands in state, and Claude never handles it.
  - Google: set up the OAuth consent screen (the page Google shows when an app asks to sign someone in) and the iOS and web OAuth client IDs (IDs that tell Google's sign-in page which app is asking).
- 6.7 **[Claude · Sonnet, Opus review]** `apps/api` — *Done when:* Vitest integration tests pass locally and in CI.
  - Hono 4.13 with `@hono/node-server` on Node 22/24; zod from `shared` on every route; the ID-token middleware (App Architecture §9); `/v1/health`; `GET` and `POST /v1/me`.
  - The Postgres schema and migrations with Drizzle (Proposed), on Postgres.app 18 locally (**[Thomas]** installs it, about 5 minutes). A `pg` pool of at most 5 through the Cloud SQL connector with IAM login (max 4 instances × 5 stays under f1-micro's 25 connections).
  - `apps/api/CLAUDE.md` gains the migration rule: migrations are additive (expand/contract: add the new column or table first, remove the old one a release later), so the previous Cloud Run revision still runs after a migration.
  - Structured logs that never include request bodies; a Dockerfile (Node slim image, esbuild bundle); CI gains a Postgres 18 service container.
- 6.8 **[Claude · Sonnet, Opus review]** Sync (App Architecture §9), server and client — *Done when:* tests prove that a re-sent batch adds nothing, two concurrent pushes get gap-free `seq`s, two offline phones merge to identical card states, and a late upload is still pulled.
  - Push in one transaction under `SELECT … FOR UPDATE` on the user's row; idempotent. Pull by per-user `seq`, never by timestamp.
  - Client: the outbox pusher and puller run after each session, on foreground (debounced) and after sign-in. Merge with `ON CONFLICT DO NOTHING`; LWW records by `version`; cards reviewed on two devices are replayed with ts-fsrs `reschedule()`, fuzz off. `pasted_text` is never read.
- 6.9 **[Claude → Thomas · Sonnet, Opus review]** Client accounts, the age screen and a dev-only test sign-in — *Done when:* **[Thomas]** signs in with Apple and with Google on the iPhone (device script), under-13 answers stay local-only, and a test proves the prod Terraform leaves test sign-in off.
  - Firebase JS SDK 12.19 (Auth only) with React Native persistence; expo-apple-authentication with a nonce; google-signin 16.1.5; navigation waits for the first `onAuthStateChanged`; the opt-in screen explains what syncs.
  - The neutral age screen asks birth month and year with no default. Under 13 stays local-only, with a local flag that blocks retries and the study-help prompt (5.6). The server stores only `age_gate_ok_at`. expo-age-range is added here only if 6.1 said Texas; 10.6 adds it for everyone before launch.
  - No anonymous auth: Apple counts guest accounts as accounts that must be deletable, and they start data collection.
  - **Test sign-in:** email/password, enabled in `seedling-dev` only and shown only in the `development` variant's dev menu, with accounts the agent creates. Maestro flows (6.11, Phase 7) use it, because Apple sign-in throws on the simulator and Google's web sheet can't be driven reliably.
  - **Foot-gun:** `getReactNativePersistence` shows a recurring TypeScript "no exported member" error even though it works.
- 6.10 **[Claude · Sonnet, Opus review]** Deletion: More → Account → Delete re-authenticates (for Apple, a fresh sign-in, then `revokeAccessToken`), then `DELETE /v1/me` with `checkRevoked` cascades every row, hands owned groups to another leader or deletes them, and deletes the Firebase user. Add an admin script for requests from the web deletion page, and "Erase this phone" — *Done when:* integration tests leave zero rows for the user and no Firebase user.
- 6.11 **[Claude · Sonnet, Opus review]** First backup and restore: push the whole outbox since install with progress ("Backing up 3,214 reviews…"); a second device pulls and regrows the same plant; signing out keeps local data — *Done when:* a Maestro flow on two simulators, using test sign-in accounts, restores identical card states and plant geometry.
- 6.12 **[Claude · Sonnet, Opus review]** `api-deploy.yml`: build → Artifact Registry → deploy to dev on merge to `main` (image build and push only if dev is laptop-only); the prod job waits for the `production` Environment approval; Workload Identity Federation, no key files — *Done when:* a merge deploys (or pushes) to dev, `/v1/health` answers where deployed, and the prod job runs backup → migrate → traffic shift in that order.
  - Each deploy runs `gcloud sql backups create`, then the migrations as a Cloud Run job (a container that runs once to completion) under the deployer account, then shifts traffic to the new revision.
  - **Foot-gun:** firebase-admin can't use direct Workload Identity Federation, so any CI job that calls it uses the service-account form.
- 6.13 **[Claude → Thomas · Opus]** The privacy inventory `docs/privacy/data-inventory.md`: each SDK and table → data type, synced or not, linked to the user, purpose; draft App Privacy and Play Data safety answers (email, user ID, other user content, product interaction; no audio; no tracking) — *Done when:* Thomas has reviewed it.
- 6.14 **[Claude → Thomas · Sonnet]** Finish `infra/envs/prod`. Thomas runs `terraform -chdir=infra/envs/prod plan` in the admin user and pastes only the plan summary (the "Plan: N to add" line and the resource names) into the PR, since Claude can't read prod state. Prod costs (about $10/month) start at apply, so the apply waits for 8.9 — *Done when:* the plan is reviewed.
  - **Foot-gun:** a raw plan can contain sensitive values. Never paste it into a public repo.
- 6.15 **[Claude → Thomas · Sonnet, Opus review]** Runbooks: `docs/runbooks/api-rollback.md` (`gcloud run services update-traffic <service> --to-revisions=<previous revision>=100` sends all traffic back to the previous revision) and `db-restore.md` (PITR, point-in-time recovery: clone the instance at a chosen minute into a new instance, then repoint the service) — *Done when:* Claude has run both drills in dev. If dev is laptop-only, the drill uses a temporary dev instance, deleted afterwards.
- 6.16 **[Claude · Opus]** Phase review: `/code-review high` plus `/security-review` (auth, sync, deletion, IAM, the credential wall); fixes; the Status update — *Done when:* no high findings remain open.

**Exit criteria:** on the iPhone the dev build signs in, backs up, restores and deletes; CI deploys the API with backup and migration; the rollback and restore drills pass in dev; Claude's shell holds no owner credential; prod is written but not applied.

**Thomas checkpoint (≈2 h):** the device script: sign in with Apple, back up, restore onto a second device, delete a throwaway account.

### ➕ Phase 7 — Groups

**Status:** Not started · **Thomas time:** 8–14 h, about 2 h of it PR review

**Goal:** A leader creates a group, members join by code or QR, everyone learns the group's passages, and the group tree shows what the church knows together, without rankings. The app moves to SDK 58 before the beta.

**Prerequisites:** Phase 6 accounts.

- 7.1 **[Thomas + church]** **Gate: group privacy**, with the pastor and elders. Claude prepares a one-page memo — *Done when:* recorded.
  - Proposed default (R11's opt-in): counting toward the group's anonymous total is an explicit yes/no on the join screen, with neither preselected; showing a name is off by default. Should members be able to opt in to show their name and what they're learning?
  - Should the blossom threshold scale with group size? Is there a church-wide default rest day?
  - Who receives reports, and what response time do the community guidelines promise?
  - The domain for join links: a church-site subdomain if its web host can serve Apple's link file, or a cheap separate domain.
- 7.2 **[Claude · Opus]** Plan, using the two per-member columns in App Architecture §9: `count_in_total` (the join screen's explicit yes/no) and `show_name` (default false) — *Done when:* Thomas approves.
- 7.3 **[Claude · Sonnet, Opus review]** The groups API: `POST /v1/groups`, `POST /v1/groups/join` (6-character codes), owner/leader/member roles checked on the server, `POST /v1/groups/:id/passages` (title, references and headings only, never text), and a word filter on every user-authored field — *Done when:* integration tests prove a member can't do leader actions and no route accepts verse text.
- 7.4 **[Claude · Sonnet, Opus review]** Mastery sharing: the client sends its 31,086-bit rooted-verse bitset (`PUT /v1/mastery`) only while `count_in_total` is true for some group; `GET /v1/groups/:id/tree` returns per-chapter counts and birds, never a ranking, and per-person detail only where `show_name` is true — *Done when:* tests show a non-counting member's bits never reach the tree.
- 7.5 **[Claude · Sonnet]** The Groups tab and join links — *Done when:* a Maestro flow joins a group by code, and a link opens the app at the join screen.
  - It asks to sign in first (13+); create; join by typed code, or by scanning the leader's QR with the iPhone's own Camera app (the QR is a join link, so Seedling needs no camera permission); a share-sheet link; leader passages appear on members' shelves.
  - Join links, on the domain chosen at gate 7.1: host its `apple-app-site-association` and `assetlinks.json` files (small JSON files that tell iOS and Android a domain's links may open the app), add the Associated Domains entitlement, and publish a fallback web page for people without the app ("Get Seedling, then enter code ABC123"). Fall back to a custom scheme (`seedling://join/CODE`).
- 7.6 **[Claude · Sonnet]** The group tree in `packages/plant`: 10 genre limbs → 66 books (length by the square root of verse count) → 1,189 chapter twigs; leaf density; blossoms at the 7.1 threshold; birds; "Together we know 1,240 verses by heart"; a VoiceOver summary — *Done when:* determinism tests pass and the screenshots pass the checklist.
- 7.7 **[Claude → Thomas · Sonnet]** Report and block (Apple guideline 1.2): Report on group names and group passages, block, a leader removes a member. Each report writes a structured log entry, and a Cloud Logging log-based alert emails Thomas and the church contact (no third-party mail service). Claude drafts the community guidelines — *Done when:* a test report triggers the email, and Thomas and the church contact approve the guidelines.
- 7.8 **[Claude · Sonnet]** "Help someone set up", end to end: a leader takes a friend from install to joined in one sitting (text size, voice permission, first passage, QR) — *Done when:* the Maestro flow passes.
- 7.9 **[Thomas]** A test group on the iPhone (his own sign-in) and a simulator (test sign-in): create, join by QR, publish a passage, report it, block — *Done when:* the device script passes.
- 7.10 **[Claude → Thomas · Sonnet]** Upgrade to SDK 58 once it has been stable for 2–4 weeks (skip if 2.3 started on 58): `npx expo install expo@^58.0.0 --fix` moves every Expo-managed package to its SDK 58 pin (React Native 0.88, Skia 2.13.1, Reanimated 4.7.0, worklets 0.13.0); native tabs move to `expo-router/native-tabs`; jest-expo 58 with Jest 30. TypeScript stays ~6.0.3. SDK 58 makes the UIKit scene lifecycle (iOS's newer model for app windows) the default, which iOS 27 SDK builds need — *Done when:* all tests, Maestro flows and **[Thomas]**'s full device script pass.
  - It lands here, before any church signing or store upload, so a Phase 8a failure has one fewer possible cause.
- 7.11 **[Claude · Opus]** Phase review plus `/security-review` (authorization, user content); fixes; the Status update — *Done when:* no high findings remain open.

**Exit criteria:** groups work end to end on the dev backend; no route accepts or returns verse text or individual progress without consent; the app runs on SDK 58.

**Thomas checkpoint (≈1 h):** walk the pastor through the group tree on the iPhone.

### ➕ Phase 8a — iOS church beta

**Status:** Not started · **Thomas time:** 15–25 h, about 3 h of it PR review

**Goal:** Church members install the app through TestFlight, published by the church's Apple team, with every store requirement met. Android follows in 8b; one Android blocker never delays the iOS beta.

**Prerequisites:** Phases 6–7 (including 7.10); the church's Apple Organization team with Thomas as Admin (0.10); the church's giving URL.

- 8.1 **[Thomas]** **Gate: beta scope** — *Done when:* recorded.
  - Give in the beta, or wait for launch?
  - The tester list and size; whether any testers are in Texas (6.1).
  - One always-warm API instance (+≈$9.86/month), or accept 1–3 s cold starts at sign-in?
- 8.2 **[Claude · Opus]** Plan, with the release checklist, EAS profiles and tester onboarding — *Done when:* Thomas approves.
- 8.3 **[Thomas]** In the church team, as Admin: create the production bundle ID `org.<church>.seedling` with the Sign in with Apple and Declared Age Range capabilities, and its App Store Connect record (which reserves the name); create its Services ID and key and paste the key into `seedling-prod`'s Apple provider; set up the Google OAuth clients in `seedling-prod` and switch its OAuth consent screen from "Testing" to "In production" — *Done when:* the record exists in the church team.
  - **Foot-gun (the part people get wrong):** once any build is uploaded under a bundle ID, that ID can never be reused, and an app can't be transferred until a version has been released (R1). Never upload a production-ID build from Thomas's own team.
  - **Foot-gun:** while the consent screen says "Testing", only listed test users can sign in with Google.
- 8.4 **[Thomas + church]** Release credentials — *Done when:* `eas credentials` shows the church team's distribution certificate, provisioning profile and API key.
  - The Account Holder enables App Store Connect API access. Thomas (Admin) creates a team API key (App Manager role) and uploads it with `eas credentials`, so `eas submit` can upload without an interactive Apple login.
  - Thomas runs the first `eas build -p ios --profile beta` himself, so EAS can sign in to Apple and create the church's distribution certificate and provisioning profile. Claude can't do this interactive login.
- 8.5 **[Claude · Sonnet]** Release config in `app.config.ts` (Apple Developer Setup step 13) and a pre-submission check script — *Done when:* the script passes on a `beta` build.
  - `ios.config.usesNonExemptEncryption: false`; privacy manifests copied from each native dependency's `PrivacyInfo.xcprivacy` (Apple emails about missing reasons within minutes of an upload); the approved permission strings.
  - EAS profiles: `development` (dev bundle ID, Thomas's team), and `beta` and `production` (both the church's production bundle ID, on update channels `beta` and `production`). `APP_VARIANT` also switches the App Group and widget IDs, which derive from the bundle ID.
  - `runtimeVersion: { policy: 'fingerprint' }`, so an OTA update only reaches builds whose native code matches.
  - Per-profile values that aren't secret (Firebase config, API URL, Google client IDs) go in with `eas env:create`. `eas.yml` (the manual EAS workflow) uses an `EXPO_TOKEN` GitHub secret that **[Thomas]** adds.
  - The script checks Info.plist keys and manifest reasons in the build output.
- 8.6 **[Claude → Thomas · Opus]** The church-site pages as HTML (Google rejects PDFs): privacy policy (including that Firebase Auth and Cloud Run logs record IP addresses), terms and community guidelines, support with contact info, and an account-deletion page, all under the same legal entity name as the store listing, and linked from the app (5.11) — *Done when:* **[Thomas + church]** have published them and every link resolves.
- 8.7 **[Claude · Sonnet]** Give (if 8.1 said beta): one button in More → Give, About and the "Why is it free?" article, opening the church's page with `Linking.openURL` (Safari, not an in-app browser), with the approved wording and nothing unlocked — *Done when:* the church has approved the wording in writing (Thomas obtains it).
- 8.8 **[Thomas]** App Store Connect App Information from Claude's answer sheets (Apple Developer Setup step 12): US-only availability, DSA "not a trader", the age-rating questionnaire (honest for Scripture; expect 9+ or 13+), the App Privacy label from 6.13, privacy and support URLs, content rights; TestFlight's Beta App Description, feedback email and review contact — *Done when:* every section shows complete.
- 8.9 **[Thomas]** In the admin user, `terraform -chdir=infra/envs/prod apply` (prod costs begin, about $10/month), then approve the first prod deploy in GitHub — *Done when:* prod `/v1/health` answers.
- 8.10 **[Thomas]** Run the 6.15 restore drill once in prod, before any tester data exists — *Done when:* the clone answers a query and has been deleted.
- 8.11 **[Claude → Thomas · Sonnet]** Build and ship: Claude runs `eas build --profile beta --platform ios` (or `--local`); Thomas runs `eas submit`; TestFlight internal (Thomas), then an external group. The first external build goes through Beta App Review (Apple's light check before outside testers get a build); Claude drafts the review notes (works without an account; how to reach groups) — *Done when:* the external group is approved.
  - **Foot-gun:** don't use EAS ad hoc builds for the church; they're capped at 100 iPhones a year. TestFlight builds expire after 90 days.
- 8.12 **[Claude → Thomas · Sonnet, Opus review]** "Move my progress (file)" in More → Account, in every build: an export/import file (review events, enrollments, settings, plant seed, custom passages; pasted text only if the user chooses). Thomas uses it to move from the dev build to the beta build — *Done when:* Thomas's plant geometry hash and due counts match in both apps.
  - Account restore can't do this: the dev build signs in to `seedling-dev` and the beta to `seedling-prod`, and they are separate apps. Both can stay installed side by side. Testers changing phones without an account use the same file.
- 8.13 **[Claude → Thomas · Sonnet]** Tester onboarding and feedback — *Done when:* Thomas and one co-leader complete onboarding from the guide alone.
  - A one-page guide with the TestFlight public link as a QR code (no tester emails needed), and a setup-session plan built on "Help someone set up". In the session, turn on Automatic Updates in TestFlight.
  - The app shows its own plain banner, "A new version is ready. Open TestFlight to update.", from 2 weeks before its build expires (the build date is stamped in at build time). An expired build otherwise just says "expired".
  - More → "Send feedback": a mail draft to the church support address with the app version and device filled in. If no mail app can open it (`Linking.canOpenURL('mailto:')` is false), show the address with a Copy button. TestFlight's screenshot feedback also works.
  - An opt-in R&D export: review events with auto and final ratings, step kinds and timings; no text, and no trails unless chosen; plain consent wording.
- 8.14 **[Claude · Opus]** Phase review plus `/security-review` of the release config; fixes; the Status update — *Done when:* no high findings remain open.

**Exit criteria:** the external TestFlight group is approved and testers have installed; the church pages are published; the prod restore drill passed; Thomas's data has moved.

**Thomas checkpoint (≈2–3 h):** the first in-person setup session at church.

### ➕ Phase 8b — Android closed test

**Status:** Not started · **Thomas time:** 8–15 h, about 2 h of it PR review

**Goal:** Android testers install through Play closed testing from the church's Play account, with the same privacy gate as iOS. Decision 4 stands; this half of the beta just starts later.

**Prerequisites:** gate 8.15. Runs alongside Phase 9.

- 8.15 **[Thomas]** **Gate: start Android** — *Done when:* recorded.
  - 8a has run about 4 weeks without a data-loss bug, and an Android 13+ phone (ideally a Pixel) is in hand, borrowed or bought.
  - Android voice floor: on-device recognition on Android 13+ only, with typing below (Proposed), or sherpa-onnx early for the roughly 30% of Android phones on 12 or older?
- 8.16 **[Thomas]** Install Android Studio with an arm64-v8a Google Play emulator image — *Done when:* the emulator boots and Claude can run a Maestro flow on it.
- 8.17 **[Thomas + church]** The church signer creates the Organization Play Console account ($25 once; D-U-N-S, website and org phone; no prepaid cards; no refund if verification fails) and invites Thomas — *Done when:* Play internal testing is available.
  - Confirm on creation that the 12-testers-for-14-days rule doesn't apply to organizations (medium confidence).
- 8.18 **[Thomas]** Play forms: Data safety, the IARC rating questionnaire (the shared international age-rating system), target audience 13+, app access (test credentials), ads (none) and the deletion URL — *Done when:* every form shows complete.
- 8.19 **[Claude · Sonnet, Opus review]** The `android-ondevice` adapter in `apps/mobile/src/stt/` — *Done when:* unit tests mirror 3.5's refusal test, and the borrowed-phone script recognizes speech in airplane mode.
  - `probe()` requires API ≥ 33, on-device recognition available and the language model installed; otherwise it offers the model download or falls back to typing. `start()` refuses otherwise. No audio persistence. A Seedling rationale screen comes before the `RECORD_AUDIO` prompt.
  - **Foot-gun (the privacy gate):** Android recognizers can fall back to cloud recognition, and the emulator can't prove on-device behavior. Only the real-phone airplane-mode test does.
- 8.20 **[Claude → Thomas · Sonnet]** Android build and test — *Done when:* the closed test is live and **[Thomas]** has run the device script on the Android phone.
  - Config: `RECORD_AUDIO` only, unused permissions blocked, no `USE_EXACT_ALARM` (Play allows it only for alarm and calendar apps), target SDK 36.
  - An EAS Free build; every Maestro flow on the arm64 emulator; Firebase Test Lab Robo runs (Google's crawler taps through the app on hosted devices; free Spark plan: 10 virtual + 5 physical a day); Play internal, then a closed test through a Google Group. Android 13+ beeps on start and stop unless continuous mode is used.
  - Android offers Google sign-in only (Apple's 4.8 rule is iOS-only; Proposed). Someone who signed up with Apple can't sign in on Android until a web Apple flow exists (Later).
  - **[Thomas]** adds the Play App Signing SHA-1 (a fingerprint of the certificate Google re-signs the app with) to the Android Google OAuth client. **Foot-gun:** Play re-signs every app, so Google sign-in fails in Play builds until that SHA-1 is added; the upload key's SHA-1 isn't enough.
  - **[Thomas]** after the first build: download the upload keystore backup with `eas credentials` into a password manager. A lost upload key means a slow reset through Play support.
- 8.21 **[Claude · Opus]** Phase review plus `/security-review` of the Android privacy gate and release config; fixes; the Status update — *Done when:* no high findings remain open.

**Exit criteria:** the Android closed test is live; the Android privacy gate is reviewed and proven on a real phone.

**Thomas checkpoint (≈1 h):** the borrowed-phone script.

### ➕ Phase 9 — Beta iteration + launch prep

**Status:** Not started · **Thomas time:** 30–55 h, about 8 h of it PR review

**Goal:** Learn from real users for a fixed time box, fix what hurts, tune the engine on data instead of guesses, and build the public-launch features.

**Prerequisites:** Phase 8a testers active.

- 9.1 **[Claude → Thomas · Sonnet]** Weekly triage (about 30 minutes of Thomas's time): Thomas pastes or forwards feedback emails, TestFlight feedback, TestFlight crash reports and Play's Android vitals (Claude never signs in to store consoles); Claude returns a ranked list, and Thomas picks the week's issues — *Done when:* each beta week has a triage note in `docs/beta/`.
- 9.2 **[Claude · Sonnet]** The release cadence in `docs/runbooks/release.md` — *Done when:* merged and followed.
  - JS-only fixes ship as EAS Update OTAs (over-the-air updates) on the `beta` channel. **[Thomas]** publishes them (`eas update --channel beta`), or a workflow behind the `production` Environment does; Claude never does.
  - Native changes and every database migration ship as a new build, because a rollback would leave the schema ahead of the code.
  - Upload a new TestFlight build at least every 60 days, so the 90-day expiry never strands testers. EAS Free caps OTA updates at 1,000 monthly users.
- 9.3 **[Thomas]** Collect testers' opt-in exports every 2–4 weeks into a folder outside the repo — *Done when:* the first batch exists. The exports carry no text or names, so Claude can analyze them.
- 9.4 **[Claude · Sonnet]** Grading calibration: `scripts/calibrate_grading.py` compares `autoRating` with `finalRating` per input mode and step kind and proposes threshold changes, which ship as a new engine version with tests and an updated grade table (§4, 1.12) — *Done when:* the override rate per mode is reported and Thomas has approved or declined each change.
- 9.5 **[Claude · Sonnet]** FSRS parameters: `scripts/optimize_fsrs.py` runs py-fsrs's optimizer (`pip install "fsrs[optimizer]"`) on trial 2 and pooled beta logs and writes a parameters JSON. The app validates it with zod and uses it as the new default; per-user parameters via `/v1/me` come after a few hundred reviews — *Done when:* held-out log loss beats the FSRS-6 defaults, or the report says why not.
- 9.6 **[Claude · Opus]** The per-unit memory-state experiment (sequence v2 §9): Opus designs it; Sonnet builds a Python simulation comparing it with the ladder on trial 2 and beta logs. The metric: fewer reviews for the same check-up scores — *Done when:* the report is in `docs/rnd/`.
- 9.7 **[Thomas]** **Gate: R&D** — *Done when:* recorded.
  - Adopt the per-unit model (built behind the `Scheduler` interface in Phase 11), keep the ladder, or keep testing?
  - Should a section's recite step govern its verses' leaves once it exists, instead of the unit's Header→text?
- 9.8 **[Claude · Sonnet]** Ladder and plant tuning: the "Again on first sight" rate per step kind (a high rate means that step is too steep), plant stage thresholds, and the droop's tone from tester feedback — *Done when:* each change ships or is explicitly declined.
- 9.9 **[Claude · Sonnet]** Performance and battery: cold start, session frame rate, a 450-word recitation's battery use and heat, database growth after months of events, and low-end Android through Test Lab — *Done when:* the numbers are recorded and regressions are fixed.
- 9.10 **[Claude → Thomas + church · Opus drafts, Sonnet converts]** Launch content: the next shelf (Romans 8, Isaiah 52:13–53:12, Psalm 139, Isaiah 40–44, and Psalm 119 with its Aleph–Tav titles), the Psalms packs, and the Teachings of Jesus shelf with its "x of 1,955 verses" line — *Done when:* the same checks as 5.4 pass: lint, Thomas's review packets and the pastor's approval of interpretive headings.
- 9.11 **[Claude → Thomas + church · Opus]** The other six articles: Why the BSB?, Why open-source?, Why the Bible?, Why you?, Why this app? and Why a little each day? — *Done when:* Thomas and the pastor approve the voice and the theology.
- 9.12 **[Claude · Sonnet, Opus review]** Other translations and pasted text — *Done when:* KJV downloads, caches and studies offline; NC/ND translations aren't offered; a test proves no sync or export code path reads `pasted_text`.
  - Translations: chapter downloads from helloao into `texts.db` (a TS port of `src/chapter.py`'s flattening), limited to translations whose flags allow commercial use and derivatives, credited from the attribution table, behind the same consent rule as study helps (5.2).
  - Pasted text: a per-verse "my own text" field in the device-only `pasted_text` table, with no presets or imports, and edited text never labeled BSB or WEB. A build flag keeps it off until the legal review (10.5).
- 9.13 **[Claude → Thomas · Sonnet]** The home-screen widget, with expo-widgets ~57.0.24 (or the SDK 58 pin). After each session the app renders the plant offscreen (`makeImageSnapshot`) to a PNG in the App Group folder (storage shared by the app and its widget) and calls `updateSnapshot` with one line ("6 thirsty · about 4 min") — *Done when:* **[Thomas]** sees the widget update on the iPhone after a session.
  - **Foot-gun:** widget code can't use hooks, state, async calls or imports, so the app pushes everything. That Skia snapshots suit widgets is low confidence; the fallback is a text-only widget.
- 9.14 **[Claude · Sonnet]** Study-help pre-caching: once the user has consented, starting a passage downloads its chapters' notes and cross-references on Wi-Fi — *Done when:* a test passage's helps open in airplane mode.
- 9.15 **[Claude · Sonnet, Opus review]** The SpeechAnalyzer engine (3.13), if Phase 3 skipped it — *Done when:* it passes the Phase 3 device script.
- 9.16 **[Thomas]** **Gate: launch go/no-go** — *Done when:* recorded.
  - The beta has run at least 8 weeks (Proposed); no crash or data-loss bug for 3 weeks; the grade-override rate is stable; new testers finish onboarding without help.

**Exit criteria:** the 9.16 "go"; calibrated thresholds and default parameters shipped; the launch shelf and all articles approved; the public-launch features built.

**Thomas checkpoint (weekly, ≈30 min):** the triage pick.

### ➕ Phase 10 — Public launch

**Status:** Not started · **Thomas time:** 10–20 h, about 2 h of it PR review

**Goal:** Seedling is live on the US App Store (and Google Play, if 10.1 says so) under the church's name.

**Prerequisites:** the 9.16 "go".

- 10.1 **[Thomas]** **Gate: launch scope** — *Done when:* recorded.
  - Crash reporting. Proposed: none if TestFlight reports and Play vitals were enough to fix beta crashes. If one is added (Sentry, or Crashlytics, which needs native Firebase), it's declared as Diagnostics on both store forms and never starts for users known to be under 13.
  - Give at launch? Android at launch or later? Pasted text on (after 10.5)?
- 10.2 **[Claude · Opus]** The launch plan and checklist, including a re-check of rules that may have moved: state age-signal laws taking effect in 2027 (California AB 1043 on Jan 1, Utah on May 6, Louisiana on July 1; research: policy.md, medium confidence) and any posted iOS 27 SDK deadline — *Done when:* Thomas approves.
- 10.3 **[Claude → Thomas · Sonnet]** Store listings: name, a subtitle such as "Bible Memory", description, keywords, and screenshots captured on the simulator with test data at the required sizes. Avoid child-appealing imagery: it can trigger Google's Families review and make the app look child-directed under COPPA (the US children's online privacy law, covering under-13s) — *Done when:* Thomas approves.
- 10.4 **[Claude → Thomas · Sonnet]** Review notes and refreshed answer sheets: the app works without an account; a test account for groups; on-device speech; the Give framing; BSB in the public domain; US-only availability; the age rating, App Privacy label and Data safety form re-checked against the final build (and any crash SDK) — *Done when:* Thomas has entered them in both consoles.
- 10.5 **[Thomas + church]** Final legal review of the privacy policy, terms, the pasted-text feature, the credits page, the COPPA posture and the state age laws. An attorney is optional, but recommended before teen accounts exist in Texas — *Done when:* the church signs off in writing.
- 10.6 **[Claude · Sonnet, Opus review]** Age signals for everyone: integrate expo-age-range (Apple's Declared Age Range and Google's Play Age Signals) unconditionally. A US-wide launch has Texas users, so SB2420's duties apply (use store age signals, flag significant changes such as an age-rating change), and California AB 1043 starts Jan 1, 2027. A store signal of under 13 means local-only — *Done when:* device and emulator tests cover the adult, teen and declined responses.
- 10.7 **[Claude · Sonnet]** Launch build: turn pasted text on if 10.5 approved it; the `production` update channel; runbooks in `docs/runbooks/` for deletion requests, reports and releases. Past 1,000 monthly users, OTA updates need EAS Starter ($19/month) or go through the stores — *Done when:* a `production` build passes the pre-submission script and every device script.
- 10.8 **[Thomas]** Google Play production access: apply (running the 12-tester closed test first if it turned out to apply), read the pre-launch report, and rerun the Android phone script — *Done when:* production access is granted.
- 10.9 **[Thomas]** Submit for App Review with a phased release (Apple rolls the update out to automatic-update users over 7 days and lets you pause), and answer review messages (Claude drafts the replies) — *Done when:* approved and released.
- 10.10 **[Thomas + church]** Announce to the church, and cover support (reports, deletion requests, email) for the first two weeks — *Done when:* the announcement is out.
- 10.11 **[Claude · Opus]** Final review and the Status update — *Done when:* no high findings remain open.

**Exit criteria:** live in the US store(s); age signals handled; support, deletion and report handling run from the runbooks.

**Thomas checkpoint:** the launch itself.

### ➕ Phase 11 — Later

**Status:** Not started · **Thomas time:** per project

Candidates after launch. Each starts with an Opus plan and a Thomas gate, like any phase.

| Project | Start when | Notes | Owner |
|---|---|---|---|
| SpeechAnalyzer engine | If 3.13 and 9.15 both slipped | Swift local module, iOS 26+ | Claude · Sonnet, Opus review |
| Open-source STT (sherpa-onnx) | Android 12-and-older users want voice, or engines disagree too much | Streaming zipformer en-20M int8 (about 45 MB, downloaded on first use) with hotwords for names. A small custom Expo module over upstream sherpa-onnx, not react-native-sherpa-onnx (young, bundles LGPL FFmpeg). Keep Whisper and Moonshine out of grading: they can invent words during pauses | Claude |
| Per-unit memory model | Gate 9.7 says adopt | Behind the `Scheduler` interface; simulation and parity first | Claude · Opus design |
| Learn the outline only; list sections | Gate 5.2 deferred them | Phase 1 plus "Read it aloud" per section; `style: list` adds First letters steps and groups items in fives | Claude |
| Kids or family mode | The church asks for it | Parental consent, the amended COPPA rule (voiceprints count as personal information), counsel review | Thomas + church |
| Android widgets | After SDK 58 | expo-widgets for Android runs its own JS runtime | Claude |
| AI questions about a verse | Gate 5.2 said yes | A server endpoint (API keys can't live in the app), a hard budget cap, public-domain commentaries only (never Tyndale), pastor review of prompt and tone, a privacy-label change | Thomas gate; Claude builds |
| Licensed translations | The church wants ESV, NIV, NLT, NASB or CSB | The church applies (Crossway licenses only organizations). ESV's free terms cap local storage at 500 verses | Thomas + church |
| Web version | Gate 0.6 is reversed | expo-sqlite's web support is alpha; exclusive transactions are native-only | Claude · Opus memo |
| Localization | Demand outside English | UI strings, translations, STT locales (SpeechAnalyzer reserves only a few per app) | Claude |
| Half-verse parts | Poetry outlines need them | `12a`/`12b` boundaries at line breaks; mastery stays per verse | Claude |
| In-app Apple Pay giving | The church earns a Candid seal | Apple-approved nonprofits only; needs a payment provider | Thomas + church |
| Smaller items | When a need shows up | App Check and Crashlytics (need native Firebase modules), Siri shortcuts, Live Activities, Apple sign-in on Android, art packs (a new `renderVersion` with an opt-in "new look") | Claude |
