# Architecture Baseline

## Purpose

This repository is the central implementation and evidence base for Sizhu Atelier learning pages. It must support multiple topic clusters without splitting shared navigation, design tokens, analytics, SEO, accessibility, and review controls across separate repositories.

## Current decision

The baseline is framework-neutral and static-first. No framework, hosting provider, build tool, or content management system is assumed until repository and deployment discovery proves the required constraints.

## Logical layers

### `src/pages`
Owns canonical page routes and page composition.

### `src/components`
Owns shared header, footer, breadcrumbs, table of contents, related-content cards, source lists, disclaimers, diagrams, and CTA components.

### `src/content`
Owns reviewed copy, terminology, source ledgers, claim classification, and structured page data. Content must remain separable from presentation.

### `src/styles`
Owns design tokens, typography, layout primitives, component styles, responsive behavior, focus states, and reduced-motion behavior.

### `src/scripts`
Owns progressive enhancement, navigation behavior, optional accordions, and an analytics adapter. Core content must remain readable without JavaScript.

### `public/assets`
Owns optimized public images, icons, social images, and downloadable non-sensitive assets.

### `tests`
Owns structural, content-integrity, link, accessibility, metadata, and route validation.

## Canonical route model

Routes are declared in `src/routes.json`. The route manifest is the source for sitemap generation and duplicate-canonical checks until a build system replaces it.

## Content safety invariants

- No personal birth, chart, order, customer, payment, secret, or token data.
- No medical, diagnostic, treatment, or guaranteed-effect claims derived from traditional models.
- Hanzi, Pinyin, schools, correspondences, and historical claims require source and review status.
- Modern interpretations must be labeled and not presented as universally traditional.
- Product CTAs and educational claims remain distinguishable.

## Delivery invariants

- Jira key in branch and pull-request title.
- No direct feature development on `main`.
- Pull request required before integration.
- Published work requires route, canonical, metadata, accessibility, source, link, and analytics evidence.

## Open decisions

- Production repository and domain mapping.
- Hosting and nested-route behavior.
- Build tool or static-site generator.
- Analytics provider and event taxonomy.
- Content authoring format and editorial workflow.

These decisions must be evidenced before implementation-specific architecture is introduced.
