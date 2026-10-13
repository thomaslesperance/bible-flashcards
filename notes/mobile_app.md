# Overview

Free Bible memory app attempting to help untalented, non-tech savvy people memorize large portions of the Bible, such as the Sermon on the Mount.

It combines a unique outline-based flashcard system developed by iteration with custom Anki flashcard decks with speech-to-text (STT) recitation feedback.

Other features of the app support this journey. I want to create an app I would want to use. And I want to least talented person in my church to be successful with it.

It uses open-source Bible text and study material.

## App Name Idea Elements

- Planted
- Grow
- Seed
- Seeded
- Seedling
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

- Sapling that grows shoots and leaves as user masters material

## Core Journies and Intro Material

- Sermon on the Mount
- Farewell Discourse
- All teachings of Jesus packaged somehow
- Ten commandments
- Book of Psalms<br><br>

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
Outline work, verse work, vocal recitation work.
Graduated difficulty system.
Genre-adaptive, but generally applied to any selection of material.

## Beautiful UI

Using AI's help with React Native and modern Bootstrap
Colorful and fun to look at
Cohesive aesthetic

## User Groups and Shared Content

- Group progress tracker that shows how much of the whole "tree" of the Bible the users collectively know by heart
- Groups can create custom Journies

## Access to free Bible APIs to enhance card content

- Quick links to public domain commentaries on text being learned to mitigate context switching and promote understanding

## Donation Path / PWYW

Option to give with promise to dedicate the money to the Great Commission.

# Tech Stack

- Cross-platform
- iOS SDKs for widgets and friction reduction
- React Native
- Bootstrap
- STT
- FSRS
- Local Sqlite
- Bible api
- GCP for users and groups?
- Stripe and Chase bank account

# Cost Projection

- ~$100 per year to host on Apple App Store
- api for backend
- database for users
- security/auth

# Payton Notes

~ $100 for apple developer license

Annoying part is the review and setup process for getting the app launched on App Store

- payments can go to your name because your EIN is just your ssn if you don't have one
- best to have a separate account for your actual revenue

- Screenshots, permissions, privacy policy, terms of service

- Expo and React Native
- Expo syncs up to Apple Build
- GCP equivalent of AWS Cognito once you get to user phase

- connectors, plugins
- project management
- github for PRs
- to whatever database you're using either local or cloud at that time
- Figma UI design
- expo -> review it's own work based on business specs for UI/UX
-   - can create a dev API backend on your laptop
-   - have expo put it to dev moded to the phone
-   - if it's too much local machine setup, just choose some difficult components to the actual cloud
- should be fine to give it access to GCP console, control it with policies
- let it get out of code and look at and view things with specific instructions
-   - view its own output
- set up a stripe account (simple audit)
-   - they have a sandbox you can test payments
-   -

- dev right in claude code
- determine infrastructure, architecture, scope
-   - no need to be limited anymore because of the capability of AI
-

### Optimize Claude cost

have opus plan the app and create a spec, pass it off to sonnet to build the pieces, then have opus review
ui specific task, opus 5.5 on high
