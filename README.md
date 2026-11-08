# Product Management Master Handbook

A visual, interactive Product Management study system organised around 12 Product Core modules. It is an independent educational resource — see the Disclaimer & trademarks page on the site.

## Open it
- **Live (public, anyone with the link):** https://pm-master-handbook-varun.netlify.app — Netlify project `pm-master-handbook-varun`. To publish changes: rebuild, then run `netlify deploy --prod --dir html/Interactive-PM-Handbook --site pm-master-handbook-varun --no-build`.
- **Interactive site:** `html/Interactive-PM-Handbook/index.html` — works offline straight from disk (no server, no API keys).
- **Entry point listing everything:** `index.html` in this folder.
- **All links in one file:** [`LINKS.md`](./LINKS.md): live pages and PDFs for every module, plus the resume and case-study portfolio.
- **PDFs:** `pdf/` — the complete handbook (444 pages, page-numbered contents, 527 bookmarks), 12 module PDFs, and separate PDFs for the Framework Library, Case Studies, Practical Projects and Interview Handbook.

## What's inside
| Part | Contents |
|---|---|
| 12 modules | Fundamentals · Strategy · Discovery · Prioritisation · UX · Communication · Analytics · Growth · Tech & System Design · LLMs/RAG · Vibe Coding · Agentic AI |
| Framework Library | 29 frameworks + a "which framework should I use?" selection guide |
| Case Study Library | 12 cases (food delivery, ride-hailing, e-commerce, streaming, music, messaging, collaboration, card onboarding, payments, learning, PLG, AI finance assistant) |
| Practical Projects | 5 end-to-end portfolio projects with datasets and model solutions |
| Interview Handbook | 106 questions in 13 categories, scorecard and practice worksheet |
| Templates | 10 reusable templates (PRD, one-pager, experiment plan/readout, launch checklist, stakeholder map/DACI, research kit, RICE/WSJF/roadmap, metrics/OKR/KPI tree, AI PRD/eval, decision log/retro) + the Module 11 starter app |
| Datasets | 11 synthetic CSVs (see `datasets/README.md`) |
| Glossary | 175 searchable terms |

## Honesty rules used throughout
- **"Key points"** boxes summarise the essentials of each topic in the handbook's own words.
- **"Hypothetical"** boxes and labels mark invented numbers. No real company results are claimed; company names are used only as widely known illustrations.
- Module titles follow a standard Product Management curriculum structure and may be refined.

## Rebuild after editing
Edit Markdown in `content/`, then from this folder:

```bash
python -I _build/build.py
```

```bash
python -I -X utf8 _build/pdf.py
```

```bash
python -I -X utf8 _build/validate.py
```

See `PROGRESS.md` for architecture, status and known gaps; `validation-reports/` for test results.

## Folder map
```
content/            Markdown sources (modules, frameworks, cases, projects, interview, pages, glossary)
html/Interactive-PM-Handbook/   generated website (self-contained, incl. pdf/ and downloads/)
pdf/                generated PDFs
templates/          reusable templates + vibe-coding-starter app
datasets/           synthetic CSV datasets
cases/ diagrams/ interview-preparation/ references/   pointers (content lives in content/ and the generated outputs)
validation-reports/ link, SQL, site, functional and PDF QA reports
_build/             build scripts, chart generator, CSS/JS
_source/, _private/  local-only working files (git-ignored, not published)
```
