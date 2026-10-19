# Conceptual Requirements

Free Bible memory app attempting to help untalented, non-tech savvy people memorize large portions of the Bible, such as the Sermon on the Mount.

It combines a speech-to-text (STT) recitation feedback concept with a unique outline-based flashcard system developed by iteration with custom Anki flashcard decks.

Other features of the app defined below support and motivate this journey. In short, I want to create an app I would want to use. And I want the least talented person in my church to be successful with it.

It uses open-source Bible text and study material at this time with limited support for other Bible translations as defined below.

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

# Features

## Progress Tracker

- Sapling growing out of the soil that gradually grows shoots and leaves as user masters material
- Governed by some algorithm in the background that dictates the pseudo-random character of the plant and how it develops given a magnitutde of content the user has mastered

## Core Journies and Intro Material

### Core Journies

Pre-defined sections of material the user can choose to begin learning right away. Not too jazzed about the term "journies" though.

- Sermon on the Mount
- Farewell Discourse
- All teachings of Jesus packaged somehow
- Ten commandments
- Book of Psalms

### Into Material

Simple, potent, and quickly digestible articles to orient and introduce the user to the circumstance.

- Why the BSB?
- Why open-source?
- Why memorize?
- Why the Bible?
- Why you?
- Why this app?

## Custom Journies, Outlines, and Verse Text

- User can build their own custom journey:
- Collection of disparate verses, portions of books, collections of books, etc.
- Input their own outline to use instead of the default
- Depending on legality, user can paste in their own Bible text by verse

## Real-Time Recital Matching

Similar to a karaoke machine, user begins reciting Bible text and open-source STT models parse their input.
Their input forms a moving trail behind a middle marker with the answer text appearing behind the marker.
The level of match between input and answer text is indicated by color coding.
These trails are stored and can be compared later on to show progress as trails are spotty and then turn to green.

## Robust Learning Algorithm

Using open-source FSRS at the core of the material review loop.
Outline-based approach rather than reference-verse approach to enhance recall through greater understanding of text shape and logic.
Well-designed sequence of learning phases for tackling large portions of text.
Outline work, text work, vocal recitation work.
Graduated difficulty system.
Genre-adaptive, but generally applied to any selection of material.
\*Requires more R&D and is the core of the product.

## Beautiful UI

Using AI's help with React Native and modern Bootstrap
Colorful and fun to look at
Cohesive aesthetic

## User Groups and Shared Content

- Group progress tracker that shows how much of the whole "tree" of the Bible the users collectively know by heart
- Groups can create custom Journies

## Access to free Bible APIs to enhance card content

- Quick links to public domain commentaries on text being learned to mitigate context switching and promote understanding
- Quickly check to see if an answer is available to a hang up in understanding so that learning can resume

## Donation Path / PWYW

Option to give with some kind of promise to dedicate the money to the Great Commission.

# Technical Specifications and Requirements

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

## Cost Generators

- Apple Developer license for host on Apple App Store with (~$100 per year)
- Google Play Store developer license?
- GCP:
- api for backend
- database for users
- security/auth

## Apple Developer Setup

- tedious
- payments can go to your name because your EIN is just your SSN if you don't have an EIN
- best to have a separate account for your actual revenue
- Screenshots, permissions, privacy policy, terms of service

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

### Optimize Claude cost

Example optimizations:

- have opus plan the app and create a spec, pass it off to sonnet to build the pieces, then have opus 5.5 on high review
  ui specific task
- explicity define a reinforcement learning loop for agent to produce work and check its own output, such as designing a ui, then viewing the ui, then adjusting, etc.:
- e.g., expo -> review it's own work based on business specs for UI/UX:
- can create a dev API backend on your laptop
- have expo put it to dev mode on your phone
- might be too much local machine setup to mock auth for dev, so likely just use GCP prod auth

## App Architecture

## Build Phases with Instructions
