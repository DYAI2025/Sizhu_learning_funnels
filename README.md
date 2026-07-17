# Sizhu Atelier Learning Funnels

Central codebase for the English Sizhu Atelier learning and discovery experience.

## Product boundary

This repository owns the learning pages that connect trustworthy educational content with Sizhu Atelier products, Etsy, and selected Bazodiac experiences.

## Planned canonical routes

- `/learn/`
- `/learn/wu-xing/`
- `/learn/wu-xing/feng-shui/`
- `/learn/wu-xing/tcm-organs/`
- `/learn/wu-xing/food-scents-colors/`
- `/learn/bazi/`
- `/learn/bazi/four-pillars-day-master/`
- `/learn/bazi/da-yun/`
- `/learn/bazi/hehun/`
- `/learn/zi-wei-dou-shu/`
- `/learn/bazodiac-fusion/`

## Architecture principles

- Static-first and progressively enhanced.
- One shared design system and navigation.
- Content, presentation, analytics, and source evidence remain separated.
- Chinese terminology and cultural claims require review before publication.
- Traditional models are not presented as medical or scientific proof.
- No personal birth, chart, customer, or payment data belongs in this repository.

## Repository layout

- `docs/` — architecture, decisions, plans, and governance
- `public/` — public static assets
- `src/components/` — shared page fragments and UI components
- `src/content/` — reviewed structured content by topic
- `src/pages/` — canonical page routes
- `src/styles/` — shared and page-level styling
- `src/scripts/` — progressive enhancement and analytics adapters
- `tests/` — structural, content, accessibility, and link checks

## Delivery workflow

1. Jira defines the outcome and acceptance criteria.
2. Each story uses a dedicated branch containing its Jira key.
3. Pull requests provide review and verification evidence.
4. Publishing requires content, terminology, accessibility, SEO, and link validation.

Current implementation story: `BZG-32` — Wu Xing and Feng Shui.