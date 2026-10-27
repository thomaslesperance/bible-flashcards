# Research: content

> Snapshot from 2026-10-14, written by Claude's research agents for the app spec (`../CLAUDE.md`). Each finding lists its sources and a confidence level. Recheck anything time-sensitive (versions, prices, store policies) before acting on it.

## Summary
The BSB is in the public domain. It was dedicated on 2023-04-30, and berean.bible says "Licensing is not required for any use." Attribution is appreciated but not required. The one request is that modified text not carry the Berean name. The Free Use Bible API is MIT-licensed, needs no key, publishes no rate limit, and explicitly allows storing and offline copies. The whole BSB is only 6.6 MB of chapter JSON, so v1 can bundle it rather than fetch it. One correction to the repo notes: in the local bible.eng.db, licenseNotice and licenseNotes are empty strings for all 51 translations. License data now lives only in the live API's structured `license` object (attribution, commercialUse, derivatives, copyleft, publicDomain). By those flags, 34 of the 51 English translations are public domain, 9 need attribution (7 of them share-alike), 1 needs attribution and allows no derivatives (GLW), and 7 are non-commercial or no-derivatives. BSB has no words-of-Jesus (red-letter) flags. The public-domain WEB (ENGWEBP) has them, and it marks 1,955 Gospel verses (42,608 BSB words, about 18 times the Sermon on the Mount). So "all teachings of Jesus" works as a shelf of smaller journeys, not one journey. Exact card counts come from running the repo's own sequence-v2 generator on scratch outlines. Ten Commandments: 81 cards / 7 days. Sermon on the Mount: 356 / 30. Farewell Discourse (John 13:31–17:26): 376 / 32. Songs of Ascents (Ps 120–134): 256 / 22. Luke 15: 94 / 8. Matthew 13: 168 / 14. Olivet Discourse (Matt 24–25): 276 / 23. All 150 Psalms is 2,461 verses, roughly 550 days. ESV, NIV, NLT, NASB and CSB all cap free use (about 500 verses; 1,000 for CSB) and would need a publisher license for in-app text. That license would have to be held by an organization (the church), not by Thomas. Letting users paste their own text is lower risk only if that text stays on the device: never synced, backed up to the server, or shared in groups.

## Findings
- **[high]** BSB is public domain as of 2023-04-30 and needs no license for any use, including apps. Attribution is appreciated but not required. Modified texts are asked not to use the Berean name.
  - berean.bible/terms.htm says Berean texts were 'officially dedicated to the public domain' on 2023-04-30 and links to a CC0 1.0 dedication (the CC0 link is medium confidence: the licensing page doesn't name CC0). It also says 'All uses are freely permitted.' berean.bible/licensing.htm says 'Licensing is not required for any use.' An optional form signs you up for updates. Implication: blanking words on cards is presentation, not a modified text. But if a user edits BSB wording in a custom journey, label it 'edited from BSB', not 'BSB'. MSB (Majority Standard Bible) has the same status.
  - sources: https://berean.bible/terms.htm, https://berean.bible/licensing.htm
- **[high]** The Free Use Bible API (bible.helloao.org) is MIT-licensed, needs no key or sign-up, and publishes no usage limit. Caching, storing and offline copies are explicitly allowed. AO Lab adds no restrictions of its own: each text keeps its own notice.
  - The docs comparison table says 'Yes. MIT licensed', 'No usage limits' and 'Nothing to sign up for'. A footnote allows copying content to your own hardware, servers or devices for offline use. 'Bundling' isn't named, but that footnote plus BSB's public-domain status covers bundling BSB. The Downloads page lists bible.db (11 GB), bible.eng.db (1.5 GB) and api.zip (1.5 GB), with no versioning or dates. (The local bible.eng.db is 2.6 GB on disk.)
  - sources: https://bible.helloao.org/docs/, https://bible.helloao.org/docs/guide/downloads.html
- **[high]** In the local data/bible.eng.db, licenseNotice and licenseNotes are empty strings for all 51 translations. This contradicts docs/method/bible-api-and-parser.md, which says to show `licenseNotice`. The live API instead has a structured `license` object per translation.
  - Query result: `SELECT count(*), sum(licenseNotice='') ... FROM Translation` returned 51 and 51. The live /api/available_translations.json gives each translation a nested `license` object {attribution, commercialUse, derivatives, copyleft, publicDomain} plus a top-level licenseUrl. Among the English entries only eng_net (NET Bible) has a licenseNotice. Side effect: src/deck/__main__.py credit_line() therefore prints only 'Scripture: Berean Standard Bible (BSB).' The app should keep its own attribution table, built from the live API's `license` flags plus a hand-written credit line per translation.
  - sources: data/bible.eng.db (Translation table), https://bible.helloao.org/api/available_translations.json
- **[medium]** The 51 English translations, grouped by the live API's license flags.
  - The flags were read through WebFetch summaries of the 1 MB JSON, so treat the table as medium confidence and re-check before shipping.

PUBLIC DOMAIN: attribution not required; commercial use and derivatives allowed (34):
- BSB, MSB, AAB, GHT
- WEB family: ENGWEBP, eng_web, eng_webc, eng_webpb, eng_webu, eng_weu, eng_wmb, eng_wmu
- KJV family: eng_kjv, eng_kja, eng_cpb
- eng_asv, eng_abt (ASV Byzantine), eng_bbe, eng_dby (Darby), eng_dra (Douay-Rheims), eng_gnv (Geneva 1599), eng_jps (JPS 1917), eng_lee (Leeser), eng_noy (Noyes), eng_rv5 (Revised Version), eng_tnt (Tyndale NT), eng_w88 (Wycliffe portions), eng_wbs (Webster), eng_ylt (Young's Literal)
- Septuagint/Targum: eng_boy, eng_bre, eng_lxu, eng_lxx, eng_oke

ATTRIBUTION + SHARE-ALIKE, commercial allowed (7): eng_lsv (LSV), eng_fbv (Free Bible Version), eng_t4t, eng_ulb, eng_pev, eng_our (OURB), eng_f35.

ATTRIBUTION only (2): eng_ojb, eng_tce.

ATTRIBUTION + NO DERIVATIVES (1): eng_glw.

NON-COMMERCIAL / NO DERIVATIVES (7): eng_net, eng_emtv, eng_aoi, eng_bar, eng_nna, eng_wyc2017, eng_wyc2018. Avoid these: a card that blanks words may count as a derivative, and donations muddy 'non-commercial'.

The WEB is public domain, but 'World English Bible' is an eBible.org trademark: don't call a modified text WEB.
  - sources: https://bible.helloao.org/api/available_translations.json, https://ebible.org/find/details.php?id=engwebp
- **[high]** BSB has no red-letter (wordsOfJesus) flags. 13 DB translations do, and the public-domain WEB (ENGWEBP) is the best source. Mapped onto BSB, Jesus' words in the Gospels cover 1,955 verses (1,776 at least half red) and 42,608 BSB words.
  - Chapters with flags, by translation:
- WEB family (ENGWEBP, eng_web/webc/webpb/webu/weu/wmb/wmu) and eng_tce: 103 each
- eng_kjv / eng_kja: 99
- eng_our: 166 (it also flags OT passages: Isaiah, Psalms, Pentateuch)
- eng_glw: 21 (John only)

ENGWEBP by book (verses with any red / at least half red / BSB words):
- MAT: 645 / 611 / 13,903
- MRK: 287 / 252 / 5,971
- LUK: 587 / 540 / 12,973
- JHN: 436 / 373 / 9,761
- ACT: 31 / 20 / 696
- REV: 69 / 67 / 1,879
- 1CO 2, 2CO 1, 1TI 1
- All books: 2,059 verses / 45,303 BSB words.

KJV gives nearly the same totals (Gospels: 1,936 verses, 42,103 BSB words). At about 3 cards per verse that is roughly 5,300–5,900 cards, or 15–16 months at 12 new cards a day, before removing synoptic duplicates (de-duplication is unverified). The longest red runs are the natural packages: Matt 24:4–51 (48 verses), Matt 5:3–48 (46), Matt 25 (46), Matt 10:5–42 (38), Matt 23:2–39 (38), Matt 6 (34), Mark 13:5–37 (33), Luke 6:20–49 (30), Luke 15:4–32 (29), John 5:19–47 (29), John 15 (27), John 17 (26).
  - sources: data/bible.eng.db (Chapter.json wordsOfJesus), scratchpad woj.py
- **[high]** BSB omits 19 verse numbers that WEB and KJV keep, so ref parsing and red-letter mapping must allow gaps.
  - The missing verses are Matt 17:21, 18:11, 23:14; Mark 7:16, 9:44, 9:46, 11:26, 15:28; Luke 17:36, 23:17; John 5:4; Acts 8:37, 15:34, 24:7, 28:29; Rom 14:24–26, 16:24. BSB totals 31,086 verses; ENGWEBP has 31,103. Seven red-letter WEB verses don't exist in BSB. The current generator's verses_of() raises ValueError when a range ends on a missing verse, e.g. a custom journey 'Matt 18:1–11'.
  - sources: data/bible.eng.db (ChapterVerse EXCEPT query)
- **[high]** Commentaries in the DB and live API: six are public domain (Public Domain Mark 1.0). Tyndale Open Study Notes (TOSN) are CC BY-SA 4.0. The cross-references are CC BY 4.0.
  - Public domain (live-API coverage):
- Adam Clarke (57 books)
- Jamieson-Fausset-Brown (66)
- John Gill (66)
- Keil-Delitzsch (39, OT only)
- Matthew Henry (65)
- John Calvin (48)

Tyndale Open Study Notes: CC BY-SA 4.0 (69 books, 1,243 chapters). Text size in the DB: Tyndale 4 MB, JFB 9 MB, Clarke 13 MB, Keil-Delitzsch 20 MB, Henry 29 MB, Gill 43 MB, Calvin 44 MB, so fetch on demand rather than bundle. Verse notes across the core passages (Matt 5–7, John 13–17, Exod 20, Ps 120–134): Gill 393, JFB 289, Tyndale 221, Clarke 157, Calvin 106, Henry 73 (Henry is written in long sections, not verse by verse).

OpenBible.info cross-references: CC BY 4.0, about 340,000 (344,799 rows; 40,762 have score ≥ 10).
  - sources: https://bible.helloao.org/api/available_commentaries.json, https://tyndaleopenresources.com/, https://www.openbible.info/labs/cross-references/, data/bible.eng.db (Commentary, Dataset, CommentaryChapterVerse)
- **[medium]** What CC BY-SA means for showing Tyndale notes in the app. Showing them unmodified with attribution is a 'collection', so the app itself doesn't have to be CC BY-SA. Editing, summarising or AI-rewriting the notes makes an adaptation, which must be released as CC BY-SA 4.0. DRM on the licensed files is not allowed.
  - The CC FAQ says a collection's license 'does not change the license applicable to the original material'. Share-alike applies only to adaptations with new creativity. Attribution means keeping the copyright notice, a license link, a license notice, a warranty disclaimer, a URI, and saying whether changes were made. The FAQ also says licensees 'may not place effective technological measures (including DRM) on the files'. Whether App Store app encryption counts as DRM on bundled CC BY-SA files is unresolved (low confidence). The safer pattern is to fetch Tyndale notes at runtime from the DRM-free API and cache them, rather than ship them inside the app binary. I couldn't find Tyndale's exact required credit wording; a secondary source dates the notes 2022.
  - sources: https://creativecommons.org/faq/, https://tyndaleopenresources.com/, https://freely-given.org/OBD/TOSN/details.htm
- **[high]** Tyndale Open Study Notes are keyed to NLT wording, not BSB.
  - In the DB, the Tyndale note on Matt 5:3 opens with the lemma (headword) 'poor and realize their need for him', which is NLT phrasing. Next to BSB text ('poor in spirit') this reads as a mismatch. Lead with JFB, Clarke or Henry, or show a note saying Tyndale notes quote the NLT.
  - sources: data/bible.eng.db (CommentaryChapterVerse tyndale MAT 5:3)
- **[high]** ESV API terms allow mobile apps without formal permission, within limits. The binding limit for a local-first app is that it may cache or store at most 500 verses or half a book, whichever is less.
  - Other limits:
- Up to 500 verses or half a book per query.
- No page may display more than 500 verses.
- 5,000 queries/day, 1,000/hour, 60/minute.
- Each quote must carry 'ESV', with the copyright notice and a link to esv.org.
- Free use is non-commercial only. A site counts as commercial if it is 'primarily designed' to get visitors to buy, donate, or accept ads.
- Crossway licenses 'organizations, not … individuals or solo developers'.

A user with several journeys would pass 500 stored verses, and only the church could apply for a formal license.
  - sources: https://api.esv.org/
- **[medium]** NIV, NLT, NASB and CSB permit small quotations without permission, but none of them covers an app that stores or shows the text. An in-app licensed translation needs a written license from the publisher.
  - - NIV (Biblica): up to 500 verses in any medium; not a complete book; under 25% of the work. Biblica's terms also ban commercial ads next to its text. The permissions page returned 403, so this comes from search snippets.
- NLT (Tyndale): 500 verses in print or eBook; under 25% of the work; no complete book. Apps aren't addressed; use the Permissions Questionnaire.
- NASB (Lockman): 500 verses; no complete book; at most 25% of the work. This comes from the printed copyright page via secondary sources; no official app policy found.
- CSB (Holman): 1,000 verses; at most 50% of the work; no complete book. Secondary source.
- API.Bible: free tier is non-commercial; 500 consecutive verses per request; 5,000 queries/day. Commercial use: email support@api.bible.
  - sources: https://www.biblica.com/permissions/, https://www.biblica.com/terms-of-use/, https://www.tyndale.com/permissions, https://guides.library.yale.edu/newtestament/nasb, https://support.sermonary.com/article/67-bible-translation-copyright-and-permission-notices, https://docs.api.bible/your-account/plans-pricing
- **[low]** Letting users paste their own copyrighted Bible text that stays on the device is fairly low risk, but only within strict limits. This is an honest risk summary, not legal advice.
  - Why the risk is lowish: the user makes a personal, non-commercial copy of a small portion for memorisation, and the app is a general tool like Anki or a notes app. The publisher's main exposure would be a claim against the developer for enabling infringement, which is weak when the app neither supplies nor hosts the text.

What raises the risk:
- Syncing or backing up pasted text to the server. You then host copies and need a DMCA agent ($6 per designation, valid 3 years) plus a takedown process.
- Sharing pasted text in groups or shared journeys. That is distribution.
- Named presets or one-tap import for 'NIV/ESV', or scraping. That conflicts with App Review 5.2.1 and 5.2.2 and with the source sites' terms.

Recommendation for v1: a per-verse 'my own text' field labelled personal-use, stored on the device only and excluded from server backup and sync. Shared journeys carry only the outline and references, never pasted text. Any text-bearing user content shared in groups falls under App Review 1.2 (filtering, reporting, blocking, published contact info).
  - sources: https://developer.apple.com/app-store/review/guidelines/, https://www.copyright.gov/dmca-directory/faq.html
- **[high]** BSB section headings exist for almost every proposed journey and can serve as the default outline, with three exceptions.
  - Headings available:
- Sermon on the Mount 5:3–7:27: 19 headings.
- John 13:31–17:26: 16 headings. BSB's own book outline (outlines.yml) also names 'The Farewell Discourse' 13:31–16:33, with 'Jesus’ Prayer' 17:1–26 as a sibling under 'The Last Supper' 13:1–17:26.
- Matt 24–25: 9. Matt 13: 10. Luke 15: 3. Romans 8: 5. Philippians: 15. James: 15.
- Each of Ps 120–134 has its own heading, plus a 'A song of ascents' subtitle.

The three exceptions:
- Ten Commandments: one heading (Exod 20:1); BSB puts the Deut heading at 5:5. Needs a hand outline.
- Single psalms: one heading each, and the stanza (paragraph) breaks are inconsistent. Ps 46's breaks fall at 10 and 11, not at the 'Selah' stanzas.
- Psalm 119: the 22 acrostic stanzas appear only as paragraph breaks, with no Aleph–Tav headings.

Quirk: Heb 11:30 has two consecutive heading blocks ('The Faith of Many' + '(Joshua–Malachi)'). A heading-to-outline builder must merge them. Also, data/outlines/outlines.yml covers only 6 books (Genesis, Isaiah, John, Acts, Romans, Revelation).
  - sources: data/bible.eng.db (Chapter.json headings), data/outlines/outlines.yml
- **[high]** Exact sizes from the repo's sequence-v2 generator (src.deck) at 12 new cards a day. 'Days' means days until every card has been introduced; reviews continue afterwards.
  - Each line: verses / BSB words / cards / days.
- Psalm 23, 2-stanza hand outline: 6 / 116 / 23 / 2
- Psalm 139, 4 stanzas: 24 / 387 / 60 / 5
- Ten Commandments, Exod 20:1–17, two-table hand outline: 17 / 320 / 81 / 7. Outline-heavy: 20 of the cards are Phase 1.
- Luke 15: 32 / 688 / 94 / 8
- Romans 8: 39 / 906 / 121 / 11
- Matt 13:1–52: 52 / 1,137 / 168 / 14
- Matt 24–25: 97 / 2,005 / 276 / 23
- Ps 120–134 as five triads: 101 / 1,577 / 256 / 22
- Sermon on the Mount 5:3–7:27, trial deck: 107 / 2,279 / 356 / 30
- John 14:1–17:26: 117 / 2,732 / 349 / 30
- John 13:31–17:26: 125 / 2,910 / 376 / 32
- Isaiah 40–44, trial 2: 141 / 3,713 / 436 / 37

Prose averages about 2.9–3.3 cards per verse. Psalms run lower (about 2.5) because their verses are short (13–16 words). The task's '111 verses' is Matt 5–7 in full (2,332 words). The tested deck covers 5:3–7:27, which is 107 verses.
  - sources: src/deck (run on scratch outlines in the session scratchpad), docs/method/sequence-v2.md
- **[medium]** Estimated sizes for journeys the generator can't build yet: multi-passage collections and very large sets.
  - Text-only generator runs on single psalms: Ps 1 = 11 cards, Ps 16 = 24, Ps 23 = 11, Ps 27 = 37, Ps 46 = 24, Ps 51 = 45, Ps 91 = 39, Ps 103 = 53, Ps 121 = 13, Ps 130 = 13, Ps 139 = 50, Ps 145 = 46, Ps 150 = 11. Collection estimates add about 3 outline cards per psalm.
- Psalms of Trust (1, 16, 23, 27, 46, 91, 121): 72 verses / 1,290 words, about 180 cards, about 15 days.
- Psalms of Praise (8, 19, 100, 103, 145, 150): 77 / 1,232, about 190 cards, about 16 days.
- Psalms of Repentance (32, 51, 130, 139): 62 / 1,033, about 150 cards, about 13 days.
- 'I am' sayings, core verses only (John 6:35; 8:12; 8:58; 10:9; 10:11; 11:25–26; 14:6; 15:5): 9 / 194, about 30 cards, about 3 days. With short context (6:35–40; 8:12; 8:56–58; 10:7–11; 11:25–26; 14:1–6; 15:1–5): 28 / 595, about 85 cards, about 8 days.
- Psalm 119: 176 / 2,292, about 500 cards, about 42 days.
- All 150 Psalms: 2,461 / 39,477, about 6,600 cards, about 550 days.
- Full parable set (Matt 13 + Luke 15 + 12 others): 270 / 5,808, about 850 cards, about 72 days.
  - sources: data/bible.eng.db, scratchpad refsets.py and per-psalm src.deck runs
- **[medium]** Where the passage boundaries are debated.
  - Farewell Discourse: Wikipedia gives John 14–17. It also notes that 13–17 can be read as one larger unit and that 13:31–38 leads into it. A common four-part split is 14, 15:1–17, 15:18–16:33, and 17. BSB's own outline uses 13:31–16:33 plus the prayer in ch. 17.

Ten Commandments: Exod 20:1–17 versus Deut 5:6–21. Deuteronomy says 'observe' the Sabbath where Exodus says 'remember', grounds it in the Exodus rather than in creation, and puts the coveting clauses in a different order. Numbering also differs by tradition. Jewish counting makes 20:2 the first saying. Catholic and Lutheran counting merges 3–6 and splits coveting into two. Reformed and Orthodox counting separates 'other gods' (v. 3) from 'images' (vv. 4–6). The Exodus text is shorter (320 vs 364 BSB words) and BSB gives it a heading.
  - sources: https://en.wikipedia.org/wiki/Farewell_Discourse, https://en.wikipedia.org/wiki/Ten_Commandments
- **[high]** The current deck generator handles only one book and one contiguous range. It crashes on a journey with a single leaf and no outline.
  - src/deck/tree.py load_tree() unpacks exactly one book, `(book_name, body), = spec.items()`, and requires each section's parts to cover its range exactly. So it can't take 'I am' sayings, psalm collections, or other cross-book journeys. Running it on a one-section psalm outline produced the cards, then raised `ValueError: max() iterable argument is empty` in report(): it computes `max(...)` over Phase 1 cards, and there are none. The app's port of the card ladder needs (a) a 'collection' root whose children are independent passages and (b) handling for journeys with no outline.
  - sources: src/deck/tree.py, src/deck/__main__.py
- **[high]** Bundling BSB on the device is cheap.
  - BSB Chapter.json totals 6.6 MB (all 1,189 chapters, with headings and poetry indents). Plain verse text is 3.6 MB, and footnotes add 9,835 rows / 0.48 MB. ENGWEBP is 5.8 MB, if a second translation or the red-letter flags are wanted. Commentaries total about 162 MB, so fetch and cache those per passage.
  - sources: data/bible.eng.db (size queries)

## recommendations
- Ship 10 starter journeys, ordered easy to hard (verses / cards / days at 12 new cards a day):
1. Psalm 23 'First Steps': 6 / 23 / 2
2. Ten Commandments, Exod 20:1–17: 17 / 81 / 7
3. Lost and Found, Luke 15: 32 / 94 / 8
4. 'I Am' sayings of John, core verses: 9 / ~30 / ~3
5. Psalms of Trust, Ps 1, 16, 23, 27, 46, 91, 121: 72 / ~180 / ~15
6. Parables of the Kingdom, Matt 13:1–52: 52 / 168 / 14
7. Songs of Ascents, Ps 120–134: 101 / 256 / 22
8. Olivet Discourse, Matt 24–25: 97 / 276 / 23
9. Sermon on the Mount, Matt 5:3–7:27: 107 / 356 / 30
10. Farewell Discourse, John 13:31–17:26: 125 / 376 / 32
Offer a 'next shelf' after these: Romans 8 (121 cards / 11 days), Isaiah 52:13–53:12, Psalm 139 (60 / 5), Isaiah 40–44 (436 / 37) and Psalm 119 (~500 / ~42).
- Split the Farewell Discourse into three sub-journeys a user can take on their own or in sequence: 13:31–14:31 (39 verses), 15:1–16:33 (60 verses), and 17:1–26 (the High Priestly Prayer: 26 verses, 626 words, ~80 cards, ~7 days). Use BSB's own book outline for the default headings.
- Ship 'All teachings of Jesus' as a shelf (a series of journeys), not one journey. It is ~42.6k words, about 15 months at 12 new cards a day. Suggested order: Sermon on the Mount → Lost and Found → Kingdom parables → Parables of grace (Luke 10:25–37, 18:9–14, Matt 18:21–35, 20:1–16: 82 verses, ~250 cards) → 'I am' sayings → Good Shepherd (John 10:1–18) / Bread of Life (John 6:22–58) → Olivet → Farewell. Show overall progress against the 1,955-verse red-letter total, with the flags taken from ENGWEBP and mapped to BSB refs.
- Ship the Psalms as about 10 themed packs plus the Songs of Ascents (as five triads), not as all 150 psalms (~550 days). Hand-author the stanza outline for each psalm, because BSB's paragraph breaks don't reliably match the stanzas. Psalm 119 needs the 22 Hebrew-letter titles (Aleph through Tav) written in.
- Ten Commandments: default to Exod 20:1–17 with a 'Love the LORD / Love your neighbor' two-table outline. Let the church pick the numbering tradition shown in the outline. Offer Deut 5:6–21 as a variant.
- Bundle the full BSB Chapter.json (6.6 MB) in the app. Add the ENGWEBP red-letter flags as a small table of verse refs, not the WEB text. Fetch commentaries per passage from the API and cache them.
- Build the app's attribution table from the live API's `license` object plus your own credit lines; the local DB's licenseNotice is empty. Show a BSB courtesy credit even though it isn't required. Show 'Tyndale Open Study Notes, CC BY-SA 4.0' with a license link and an 'unmodified, reformatted' note. Show 'Cross references: OpenBible.info, CC BY 4.0'.
- For 'quick links' commentary, lead with JFB or Clarke (public domain, verse-level, small). Mark Tyndale notes as quoting the NLT, and never AI-summarise them, since a summary would be an adaptation that must be released as CC BY-SA.
- Pasted user text: keep it per verse and on the device only. Exclude it from server backup, sync and group sharing; shared journeys carry only the outline and references. Don't offer named presets or imports for copyrighted translations.
- Extend the generator, or the app's port of it, to support multi-passage and cross-book 'collection' journeys, gaps where BSB omits a verse, and journeys with no outline. Fix the report() crash.

## gotchas
- Most likely mistake: trusting `licenseNotice` in the local bible.eng.db. It is empty for all 51 translations, and the repo notes wrongly say the app must show it. The live API is the only source of license flags.
- BSB lacks 19 verse numbers that WEB and KJV keep (e.g. Matt 17:21, 18:11, 23:14, Mark 9:44/46, John 5:4). Ref parsing for custom journeys, and the red-letter mapping, must allow gaps. The current generator raises ValueError when a range ends on one of them.
- Tyndale Open Study Notes headwords quote NLT phrasing, so they won't match BSB text on the card.
- CC BY-SA 4.0 forbids putting DRM on the licensed files. Whether the App Store's app encryption counts as DRM is unresolved. Fetching Tyndale notes at runtime from the DRM-free API avoids the question.
- ESV's 500-verse local-storage cap conflicts with a local-first app that holds several journeys. ESV licenses are issued only to organizations, and 'primarily designed' to get donations counts as commercial.
- 'World English Bible' is a trademark and 'Berean' is a requested name restriction. Don't call edited text WEB or BSB.
- BSB stanza breaks in the Psalms are inconsistent (Ps 46 breaks at verses 10 and 11), and Psalm 119 has no stanza headings. Heb 11:30 has two heading blocks back to back, which a headings-to-outline builder must merge.
- Short passages are outline-heavy: the Ten Commandments come to 4.8 cards per verse against about 3 for prose. One-verse units skip wave 2, and single-leaf journeys produce no Phase 1 cards and crash the current report().
- eng_our flags 'words of Jesus' in OT books (Psalms, Isaiah) as messianic readings. Use ENGWEBP or KJV as the red-letter source instead.
- Group-created custom journeys are user-generated content under App Store guideline 1.2: they need filtering, reporting, blocking and published contact info.

## human_actions
- Decide (with church leadership) which Ten Commandments numbering tradition and which Farewell Discourse boundary the default outlines use.
- Before public launch, have the church (or its counsel) review the 'paste your own text' feature and the attribution page. My analysis is not legal advice.
- If a licensed translation (ESV, NIV, NLT, NASB, CSB) is wanted later, the church as an organization must apply: ESV through Crossway's license form, NIV through Biblica, NLT through Tyndale's Permissions Questionnaire, NASB by writing to Lockman, CSB through Holman. Crossway won't license individuals.
- If the server ever stores user-pasted text or other user content, register a DMCA designated agent with the US Copyright Office ($6, renewed every 3 years) and publish a takedown contact.
- Optional: fill in the Berean licensing form (not required) to get BSB update notices.
- Review and approve the hand-authored outlines (Ten Commandments tables, psalm stanza titles, Psalm 119 Aleph–Tav, Ascents triads) before they ship as defaults.

## open_questions
- Should 'Teachings of Jesus' include red-letter text outside the Gospels (Acts 31 verses, Revelation 69, plus 1 Cor 11, 2 Cor 12, 1 Tim)? And should synoptic parallels be de-duplicated (that reduction hasn't been computed)?
- Should pasted user text be excluded from backup entirely in v1 (lost when switching phones), or end-to-end encrypted on the server? The second still means hosting a copy.
- Is the donation path enough to make the app 'commercial' under the ESV API terms and the CC NC licenses? It depends on how prominent the donation path is.
- Which commentaries should be surfaced by default: public-domain ones keyed to verses (JFB, Clarke) versus the modern but NLT-keyed Tyndale notes?
- Exact Tyndale credit wording and copyright year (2022 per a secondary source) weren't confirmed on an official Tyndale page.
- CC0 as the specific instrument behind BSB's public-domain status: the terms page links CC0 1.0, but the licensing page doesn't name it.
- NIV, NASB and CSB terms came from search snippets and secondary pages: Biblica returned 403, and no official Lockman or Holman app policy was found.
- Exact card counts for multi-passage journeys (psalm collections, 'I am' sayings) can't be computed until the generator supports collections; the current figures are estimates.