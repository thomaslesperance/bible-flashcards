# Decisions

The durable record of Seedling's decisions: one dated entry per decision, newest gate answers at the bottom. The spec, [`.claude/app-requirements/CLAUDE.md`](../.claude/app-requirements/CLAUDE.md), explains the reasoning; each entry names the spec section to read.

- **Numbered decisions (1–13)** are Thomas's.
- **R-decisions (R1–R16)** are Claude's research resolutions. They stand unless Thomas overrides them.
- **Gate answers** are added below as Thomas settles each gate (Build Phases → Decision gates). Claude records them in a PR; Thomas approves it.

To change a decision, add a new entry that names the one it replaces and mark the old one **Replaced** or **Retired**. Don't delete entries.

## Thomas's decisions

### 1. How the spec is edited
- **Date:** 2026-10-14 · **Status:** Active
- Edit the spec in place, keep Thomas's text verbatim and mark Claude's additions. Long material goes in sibling files.
- **Spec:** the legend at the top of the spec.

### 2. Donations go to a church
- **Date:** 2026-10-14 · **Status:** Active
- Donations go to a church or an existing 501(c)(3).
- **Spec:** Features → Donation Path / PWYW.

### 3. Developer accounts
- **Date:** 2026-10-14 · **Status:** Replaced by 13 (2026-10-27)
- Was: Thomas's Individual accounts now, the church's Organization accounts later.
- **Spec:** Technical Specifications → Apple Developer Setup.

### 4. Release path
- **Date:** 2026-10-14 · **Status:** Active
- A personal dev build on Thomas's iPhone, then a church beta (TestFlight and Play closed testing), then public launch.
- **Spec:** Build Phases → Phase overview.

### 5. Speech-to-text
- **Date:** 2026-10-14 · **Status:** Active
- Native on-device recognizers first, behind a swappable interface; an open-source engine later.
- **Spec:** Features → Real-Time Recital Matching.

### 6. Monorepo
- **Date:** 2026-10-14 · **Status:** Active
- One monorepo in bible-flashcards. The Python generator is the reference implementation and the content pipeline.
- **Spec:** App Architecture → 2. Repo layout.

### 7. Scheduler
- **Date:** 2026-10-14 · **Status:** Active
- Port the sequence-v2 ladder (each card its own FSRS item) behind a pluggable scheduler. The per-unit memory model is later R&D (gate 9.7).
- **Spec:** Features → Robust Learning Algorithm.

### 8. Devices
- **Date:** 2026-10-14 · **Status:** Active
- iPhone only, plus Mac simulators.
- **Spec:** Technical Specifications → Stack.

### 9. Accounts and audio
- **Date:** 2026-10-14 · **Status:** Active
- Accounts are 13+ in v1. Raw audio never leaves the device. Kids mode comes later.
- **Spec:** App Architecture → 15. Privacy and security boundaries.

### 10. Backend
- **Date:** 2026-10-14 · **Status:** Active
- Cloud Run (TypeScript API), Cloud SQL Postgres and Firebase Auth, managed with Terraform.
- **Spec:** App Architecture → 9. Server and 13. Infrastructure.

### 11. Pace
- **Date:** 2026-10-14 · **Status:** Active
- Thomas works 5–10 hours a week.
- **Spec:** Build Phases → Phase overview.

### 12. Design
- **Date:** 2026-10-14 · **Status:** Active
- Claude designs in code (Expo and the simulator screenshot loop). Figma is optional.
- **Spec:** Features → Beautiful UI.

### 13. Thomas publishes on his own accounts
- **Date:** 2026-10-27 · **Status:** Active · **Replaces:** 3 · **Retires:** R1
- Thomas owns the production app on his Individual Apple account and a personal Google Play account. The Give button links to the church's giving page. There is no church paperwork.
- Bundle IDs: `com.<thomas>.seedling.dev` (development) and `com.<thomas>.seedling` (TestFlight and the stores), both in Thomas's team.
- **Spec:** Technical Specifications → Apple Developer Setup.

## Claude's research resolutions

### R1. The church owns the production app from the first TestFlight upload
- **Date:** 2026-10-14 · **Status:** Retired by 13 (2026-10-27)
- Was: the church's Apple Organization team owns the production app from the first TestFlight upload; Thomas's Individual account builds only a dev bundle ID; church paperwork starts in Phase 0.
- **Spec:** Technical Specifications → Apple Developer Setup.

### R2. Give opens the church's page
- **Date:** 2026-10-14 · **Status:** Active
- A "Give" button opens the church's giving page in Safari. It unlocks nothing and isn't pay-what-you-want. Stripe and the Chase account are dropped.
- **Spec:** Features → Donation Path / PWYW.

### R3. Local-first
- **Date:** 2026-10-14 · **Status:** Active
- The app works fully with no account and makes no network calls until the user opts in. Accounts (Sign in with Apple and Google) add backup, more devices and groups. Neutral age screen; in-app deletion.
- **Spec:** App Architecture → 10. Auth and accounts flow.

### R4. Client stack
- **Date:** 2026-10-14 · **Status:** Active
- Expo SDK 57, then 58 before the beta; Uniwind and HeroUI Native in place of Bootstrap; Skia for the plant; ts-fsrs.
- **Spec:** Technical Specifications → Stack.

### R5. Backend stack
- **Date:** 2026-10-14 · **Status:** Active
- Hono on Cloud Run, Postgres 18 on db-f1-micro, Identity Platform and an append-only sync log. About $10/month in prod, $0 in the personal phase.
- **Spec:** App Architecture → 9. Server.

### R6. Speech-to-text engines
- **Date:** 2026-10-14 · **Status:** Active
- expo-speech-recognition with a mandatory on-device check (voice turns off if it fails); SpeechAnalyzer in v1.5; sherpa-onnx later. Tested on the iPhone.
- **Spec:** Features → Real-Time Recital Matching → Engines by stage.

### R7. Grading
- **Date:** 2026-10-14 · **Status:** Active
- Every recall step is graded automatically from voice, typed first letters or a self-check. One tap confirms or overrides.
- **Spec:** Features → Robust Learning Algorithm.

### R8. Engine port
- **Date:** 2026-10-14 · **Status:** Active
- A TypeScript port of sequence v2 (compile, calendar release, FSRS, session, grade, mastery). Python emits golden JSON for parity tests.
- **Spec:** App Architecture → 4. Learning-engine pipeline.

### R9. Content
- **Date:** 2026-10-14 · **Status:** Active
- The full BSB is bundled; a 10-passage starter shelf; other translations and commentaries on demand; pasted text stays on the device.
- **Spec:** App Architecture → 7. Content format.

### R10. Names
- **Date:** 2026-10-14 · **Status:** Active (the app name is confirmed at gate 0.1)
- "Seedling". "Passages" and "Shelf" replace "journeys"; plain step names; never "card", "deck" or "FSRS" in the UI.
- **Spec:** Conceptual Requirements → App Name Ideas.

### R11. Progress plant
- **Date:** 2026-10-14 · **Status:** Active
- One personal plant. Passages are limbs shaped by their outlines; verses are leaves; "thirsty", never dead. A group tree with birds.
- **Spec:** Features → Progress Tracker.

### R12. Motivation
- **Date:** 2026-10-14 · **Status:** Active
- A weekly rhythm with rest days and repair; no leaderboards; capped catch-up; one opt-in reminder.
- **Spec:** Features → Robust Learning Algorithm → Weekly rhythm and reminders.

### R13. Accessibility
- **Date:** 2026-10-14 · **Status:** Active
- Dynamic Type 200%+, verse text ≥ 20 pt, 7:1 contrast, 56 pt buttons, colorblind-safe colors plus shapes, silence timeouts ≥ 6 s.
- **Spec:** Features → Beautiful UI → Accessibility defaults.

### R14. Launch compliance
- **Date:** 2026-10-14 · **Status:** Active (amended 2026-10-27 by 13: the pages moved from the church site to Seedling's own site)
- US-only; policy pages on Seedling's own site; an honest age rating; a privacy label with no audio.
- **Spec:** Technical Specifications → Apple Developer Setup.

### R15. User content in v1
- **Date:** 2026-10-14 · **Status:** Active
- Group names plus leader-authored passage titles and outline headings only; no chat; report and block.
- **Spec:** Features → User Groups and Shared Content.

### R16. Repo layout
- **Date:** 2026-10-14 · **Status:** Active
- `apps/mobile`, `apps/api`, `packages/{engine,recite,plant,shared}` and `infra/`. The existing Python stays where it is.
- **Spec:** App Architecture → 2. Repo layout.

## Gate answers

None recorded yet. Next up in Phase 0: 0.1 (name, domain, production bundle ID), 0.4 (iPhone model and iOS version) and 0.6 (repo and workflow).
