# Education and productivity apps for PrimitiveOS

Research and release record for 20 November 2026. The three delivery waves shipped together in Store under **Today › Study and work**. The original prioritization began with **Tasks**, **Reading Practice**, and **Cards Self-test**. [Live collection](https://primitiveos.github.io/kindle-primitive-catalog/v1/collections.json)

## Widely used reference apps

The figures below measure different things. Active users count engagement over a stated period, registered accounts and publisher reach are broader measures, and Google Play download bands are cumulative. The release priorities weigh that demand alongside touch effort, content preparation, offline use, and overlap with apps we already ship.

Apple's Vietnam free Education chart showed language-learning apps and several driving-theory practice apps near the top when checked. The US chart featured Duolingo, Classroom, and Quizlet. These are storefront snapshots. The recurring pattern useful for Kindle is a short lesson or set of questions that a learner can complete and revisit. [Vietnam Education chart](https://apps.apple.com/vn/iphone/charts/6017) · [US Education chart](https://apps.apple.com/us/iphone/charts/6017?chart=top-free)

| Reference app | Adoption signal | Workflow worth adapting |
|---|---|---|
| Duolingo | 153.1M monthly and 64.9M daily active users across its app and learning website in Q3 2026 | Teach a short concept, ask for a response, then let the learner revisit mistakes. [Duolingo Form 10-Q](https://investors.duolingo.com/static-files/f27581cd-cf47-4058-a316-2dcca04cfb00) · [Lesson workflow](https://blog.duolingo.com/duolingo-101-how-to-learn-a-language-on-duolingo/) |
| Khan Academy | 232M registered users and 100M learners who used it in school year 2025–26 | Organize worked examples and practice sets around individual skills. [Khan Academy reach](https://www.khanacademy.org/about) · [Course and unit mastery](https://support.khanacademy.org/hc/en-us/articles/115002552631-What-are-Course-and-Unit-Mastery) |
| Quizlet and AnkiDroid | Quizlet reports 60M learners on its About page, with no time period stated there. AnkiDroid shows 10M+ Android downloads. | Use one deck for both scheduled review and an optional self-test. [Quizlet About](https://quizlet.com/mission) · [Quizlet Learn](https://quizlet.com/features/learn) · [AnkiDroid listing](https://play.google.com/store/apps/details?id=com.ichi2.anki) · [Anki review](https://docs.ankiweb.net/manual/studying) |
| ReadTheory | Publisher reports 14M+ teachers and students. The reporting window is unspecified. | Follow a passage with questions and feedback that points the reader back to the text. [ReadTheory](https://readtheory.org/homepage/) |
| Photomath and Desmos | 100M+ and 10M+ Android downloads respectively | Use typed math with visible steps, and a separate equation-to-plot flow with a value table. [Photomath listing](https://play.google.com/store/apps/details?id=com.microblink.photomath) · [Desmos listing](https://play.google.com/store/apps/details?id=com.desmos.calculator) · [Desmos tools](https://help.desmos.com/hc/en-us/articles/4406040715149-Getting-Started-Desmos-Graphing-Calculator) |
| Merriam-Webster Dictionary | 50M+ Android downloads | Search an offline word list, open one readable definition, and save a word for later. [Dictionary listing](https://play.google.com/store/apps/details?id=com.merriamwebster) |
| Todoist and Microsoft To Do | Todoist reports 50M+ people and teams without a stated reporting period. Both apps show 10M+ Android downloads. | Capture a task quickly and give today's work a short list of its own. Microsoft has announced To Do app retirement for 30 June 2027, so the reference is its My Day workflow. [Todoist](https://www.todoist.com/) · [Todoist downloads](https://play.google.com/store/apps/details?id=com.todoist) · [Microsoft To Do downloads](https://play.google.com/store/apps/details?id=com.microsoft.todos) · [My Day](https://support.microsoft.com/en-us/todo/plan-and-connect-with-microsoft-to-do) · [Microsoft retirement notice](https://support.microsoft.com/en-us/planner/to-do-to-planner) |
| Google Keep | 1B+ Android downloads | Make a checklist quickly and check off items directly from the note. [Keep listing](https://play.google.com/store/apps/details?id=com.google.android.keep) · [Checklist controls](https://support.google.com/keep/answer/6395451?co=GENIE.Platform%3DAndroid) |
| Google Calendar | 10B+ Android downloads | Show upcoming commitments by date and offer manual file import. [Calendar listing](https://play.google.com/store/apps/details?id=com.google.android.calendar) · [File import](https://support.google.com/calendar/answer/37118) |
| Loop Habit Tracker and Focus To-Do | 5M+ and 10M+ Android downloads respectively | Log a habit in one tap and review progress by date. Group completed focus sessions by task or subject. [Loop listing](https://play.google.com/store/apps/details?id=org.isoron.uhabits) · [Focus To-Do listing](https://play.google.com/store/apps/details?id=com.superelement.pomodoro) |

A controlled study with prose passages found that recall tests improved later retention. That supports including short recall sessions alongside reading and review. The effectiveness of our specific exercises would need a separate evaluation. [Roediger and Karpicke, 2006](https://psychnet.wustl.edu/memory/wp-content/uploads/2018/04/Roediger-Karpicke-2006_PsychSci.pdf)

## New Kindle apps

| App | Screen and controls | First release |
|---|---|---|
| **Tasks** | Opens on **Today** with overdue and due rows, checkboxes, and one prominent **Add task** button. **Inbox**, **Upcoming**, and **Lists** are one tap away. The add sheet needs a title. **Date**, **List**, and **Repeat** are optional. Checking a row shows **Undo**. | Local tasks, date-only due dates, and named lists. Start with daily, weekdays, and weekly repeats. Completing an overdue repeating task advances it to the next scheduled date. Reminders and calendar sync can follow device validation. |
| **Reading Practice** | Opens to **Continue** and a paged list of passages by level. A passage uses a plain reading page and one **Questions** button. Each question has three large choices and a **Passage** button that preserves the current question. After a response, show a one-sentence explanation and **Next**. | Twelve original passages across two difficulty bands, each with three reviewed questions. Save reading position, answers, and misses for an optional retry. The pilot can use the same question screen for later topic packs. |
| **Math Practice** | Pick a skill, read one worked example, and tap **Start** for five problems. Show one problem, one answer field, a purpose-built number keypad, and **Hint** or **Check**. Feedback explains the step before **Next**. | Generated arithmetic, fractions, and percentages with checked answer keys. Accept equivalent answers where appropriate. Keep a local skill history and a short retry set. |
| **Language Practice** | Opens to the next short lesson. A card shows one phrase or dialogue line. The learner taps a choice, fills a blank, or builds a short sentence by tapping word tiles. **Review mistakes** opens a paged list by topic. | Ten original beginner English lessons for Vietnamese speakers. Exercises use text and word tiles. Physical Kindle verification of Vietnamese diacritics is pending. |
| **Dictionary** | Search opens the shared keyboard. Submitting a query shows a paged list of headwords. Tap one to open its definition and save it to favorites. Favorites can be opened without typing. | 24 original English starter definitions, accent-insensitive lookup, preview for UTF-8 TSV imports, and a two-column favorites export for Cards. |
| **Habits** | **Today** shows habits and their check-in controls. Tap a habit to view the last seven days and correct a missed or accidental entry. | Local daily and weekly targets, editable check-ins, and CSV export. |
| **Agenda** | Opens to appointments grouped by date. **Today** and **Next 7 days** show a chronological list. **Add event** collects title, date, and optional time on one sheet. Tap an event for details. | Local events and preview for one-off `.ics` imports with all-day, local, or UTC start times. Recurrence and calendar sync are possible later work. |

## Updates to existing apps

| App | Addition | Screen and controls |
|---|---|---|
| **Cards** | **Self-test** and a simple text import | Keep the existing due review, text-only Anki import, and TSV export. Add **Self-test** beside **Review** on a deck. Run up to ten cards with **Reveal**, **Recalled**, and **Missed**, then offer **Retry missed**. Self-test progress is separate from the review scheduler. Add a two-column TSV importer with a preview and duplicate check so study material can move between apps by file. |
| **Notes** | **Checklists** and a **Reading journal** template | Keep the same plain-text editor, search, pins, and files. A checklist can render Markdown-style checkboxes with explicit **Move up** and **Move down** actions. A journal template supplies fields for book, page, quote, and takeaway, and saves as ordinary text. Users can bring excerpts they exported themselves. |
| **Focus** | **Subject labels** and a **Study log** | Enter a label when useful, then start the existing timer. Add a **This week** page with minutes by subject and recent sessions. Keep the minute-based display and existing presets. Explore a Tasks handoff after both apps work independently. |
| **Calculator** | **Convert** first, then **Steps** and **Graph** | Keep arithmetic and history as the opening screen. **Convert** selects source and destination unit with a single number field. **Steps** can reveal one transformation at a time for a supported fraction or linear equation. **Graph** starts with lines and quadratics, using **Plot**, **Table**, and stepped zoom on a static monochrome canvas. |

Cards accepts a two-column TSV alongside the existing text-only Anki import. Browser saves HTML for offline reading, and KOReader handles e-books. Notes is a place for users' excerpts and takeaways, while Reading Practice supplies original questions and feedback. [Cards](https://github.com/PrimitiveOS/kindle-primitive-cards) · [Browser](https://github.com/PrimitiveOS/kindle-primitive-browser) · [KOReader](https://koreader.rocks/)

## Released apps

| App | Type | GitHub release |
|---|---|---|
| Tasks | New | [0.1.0](https://github.com/PrimitiveOS/kindle-primitive-tasks/releases/tag/v0.1.0) |
| Reading Practice | New | [0.1.0](https://github.com/PrimitiveOS/kindle-primitive-reading-practice/releases/tag/v0.1.0) |
| Math Practice | New | [0.1.0](https://github.com/PrimitiveOS/kindle-primitive-math-practice/releases/tag/v0.1.0) |
| Language Practice | New | [0.1.0](https://github.com/PrimitiveOS/kindle-primitive-language-practice/releases/tag/v0.1.0) |
| Dictionary | New | [0.1.1](https://github.com/PrimitiveOS/kindle-primitive-dictionary/releases/tag/v0.1.1) |
| Habits | New | [0.1.0](https://github.com/PrimitiveOS/kindle-primitive-habits/releases/tag/v0.1.0) |
| Agenda | New | [0.1.0](https://github.com/PrimitiveOS/kindle-primitive-agenda/releases/tag/v0.1.0) |
| Cards | Update | [0.1.1](https://github.com/PrimitiveOS/kindle-primitive-cards/releases/tag/v0.1.1) |
| Notes | Update | [0.1.1](https://github.com/PrimitiveOS/kindle-primitive-notes/releases/tag/v0.1.1) |
| Focus | Update | [0.1.1](https://github.com/PrimitiveOS/kindle-primitive-focus/releases/tag/v0.1.1) |
| Calculator | Update | [0.1.3](https://github.com/PrimitiveOS/kindle-primitive-calculator/releases/tag/v0.1.3) |

## Kindle interaction requirements

- **One main action per screen.** Provide **Continue**, **Review**, or **Add task** on the opening screen and keep a visible **Done** or **Back**. Aim to reach the first passage, practice question, or add sheet within two taps of opening the app.
- **Read like a page.** Use the shared portrait layout, large labelled buttons, and visible **Previous** and **Next** on long lists. The project's reference layout uses at least 100 px touch targets at 1264 × 1680. Scale them proportionally. Show correctness with text and symbols that work in both light and dark mode.
- **Refresh after an action.** Redraw the affected panel after a checkbox or answer, and redraw a full page on navigation. Keep the timer on its existing cadence. Open the shared keyboard only where text entry helps, and import longer lists or passages from a file. [Primitive UI](../.agents/skills/primitive-ui/SKILL.md) · [E-ink implementation notes](../.agents/skills/kindle-eink/SKILL.md)
- **Save on Kindle.** Keep the core workflows usable in airplane mode. Save completed actions and the current place in a session. Preview imports and report unsupported, malformed, oversized, or duplicate records before writing. Use the platform's storage lease so imports and saves cooperate with USB mode. Ship original or appropriately licensed starter content.
- **Reserve heavier features for a later decision.** Camera-based problem scanning, video courses, handwriting and dense editors, team workspaces, live classroom portals, and asleep-device reminders need separate usability or platform tests. Notes, Calendar-style lists, and question pages provide the corresponding everyday workflows in a small interface. [Notion's offline editing scope](https://www.notion.com/help/use-pages-offline) · [Classroom listing](https://play.google.com/store/apps/details?id=com.google.android.apps.classroom)

## Release verification

Desktop interaction and persistence checks passed. The ARMHF archives matched their public SHA-256, contained both licence files, and installed and removed successfully after a simulated catalog refresh. The seven new Store icons matched the package entries, and the live Store catalog matched the published listings, screenshots, and collection. [Local verification](local-verification.md) · [Catalog deployment](https://github.com/PrimitiveOS/kindle-primitive-catalog/actions/runs/44580696716)

Physical Oasis 3 checks for these versions remain open. The implementation plan tracks the app-specific checks and shared device gate. [Study and work milestones](implementation-plan.md#study-and-work-release)
