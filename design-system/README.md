# Openly Useful Design System

Version **1.0.0** — the public, implementation-ready expression of Openly Useful.

## Brand idea

**Useful things, openly made.** Openly Useful is a comfortable sharing ecosystem for practical public tools. It should feel like entering a well-kept community computer lab: capable equipment, familiar rituals, patient maintainers, and room at the terminal for one more person.

The core metaphor is the **Open Shell**. Its rounded opening bracket is simultaneously:

- a Unix shell, where useful work begins;
- an open doorway, inviting participation;
- a protective boundary, made safe without being closed;
- a half-built frame, acknowledging that public work can always improve.

## Principles

1. **Open, not exposed.** Show how things work while giving people clear boundaries and safe defaults.
2. **Familiar, not frozen.** Borrow the emotional memory of shared terminals, READMEs, computer clubs, and early web communities—not their usability limitations.
3. **Useful before impressive.** Prefer direct language, obvious controls, and durable patterns.
4. **Warm through evidence.** Trust comes from visible status, documentation, and honest constraints, supported by humane materials and tone.
5. **One more chair.** Every surface should suggest that participation is expected and welcomed.

## Identity architecture

| Element | Role | Rule |
|---|---|---|
| Open Shell mark | Primary symbol | Use the supplied SVG; do not redraw, rotate, close, outline twice, or place inside a circle. |
| Wordmark | Primary name | Set “Openly Useful” in the primary sans at 650–720 weight with tight optical tracking. |
| Lockup | Mark + wordmark | Keep one mark-width of clear space on all sides. Mark height equals cap-height plus 20%. |
| Shellfolk | Character language | Rounded modular helpers derived from the bracket. Show cooperation and useful work, never heroic posing. |
| Bracket trail | Supporting pattern | Repeat the mark at low contrast in one direction. Never make a decorative confetti field. |

Minimum mark size is 20 CSS pixels or 6 mm. Use the green mark on Shell surfaces and the reverse mark on Ink or Terminal surfaces. The mark is not an alphabetic “C”; always preserve the squared open-side terminals.

## Color

| Token | Hex | Purpose |
|---|---:|---|
| Shell 50 | `#F7F3E9` | Primary canvas; comfortable paper warmth |
| Shell 0 | `#FFFDF8` | Raised surface |
| Unix Ink | `#171A18` | Primary text and dark field |
| Terminal 600 | `#247A4B` | Brand mark, primary action, positive status |
| Terminal 100 | `#DCE7DB` | Selection, quiet success, supportive background |
| Process 600 | `#3568A8` | Focus, links, active/in-progress state |
| Warning 600 | `#9A5B15` | Caution only |
| Danger 600 | `#A33B35` | Destructive/error only |

Do not rely on color alone for status. Terminal green is not decoration; reserve it for identity, progress, and participation. Process blue is a utility color, not a competing brand color.

## Typography

- **Primary:** Atkinson Hyperlegible Next, with the documented system sans fallback. Its open forms support the brand’s legibility and safety promise.
- **Technical:** IBM Plex Mono, with the documented system monospace fallback. Use for labels, commands, version strings, and status—not body paragraphs.
- Display text uses sentence case, tight tracking, and direct language.
- Body measure: 45–72 characters. Minimum body size: 16 px. Labels: 12 px minimum when essential.
- Never simulate nostalgia with pixel fonts, all-caps paragraphs, CRT distortion, or low-contrast green-on-black body text.

The website does not call third-party font services; a consuming project may self-host the OFL-licensed typefaces or use the fallbacks.

## Layout, shape, and material

- Base grid: 4 px. Standard component rhythm: 8 px. Section rhythm: 64–128 px.
- Layout grid: 12 columns desktop, 6 tablet, 4 mobile.
- Default content width: 1,240 px. Text width: 720 px maximum.
- Square corners communicate infrastructure; rounded corners communicate welcome. Most interactive surfaces use 8–14 px radii.
- Shadows are quiet and material. Avoid glassmorphism, glowing gradients, or floating-card excess.
- Texture may suggest recycled paper, matte plastic, cork, wood, or faint CRT phosphor. Texture must never reduce legibility.

## Components

### Button

| Variant | Use | Default | Hover/active | Disabled/loading |
|---|---|---|---|---|
| Primary | One main action per region | Ink field, Shell text | Terminal field / 1 px press | 45% opacity / retain label width |
| Secondary | Supporting action | Transparent, Ink border | Shell surface | 45% opacity |
| Quiet | Inline utility | No field | Terminal-100 field | 45% opacity |
| Danger | Confirm destructive work | Danger text/border | Danger field, Shell text | 45% opacity |

All button targets are at least 44×44 px, expose a visible label, use native button/link semantics, and show the two-color focus ring.

### Link

Body links are underlined by default. Navigation links may omit the underline only when position and hover/focus treatment make their affordance clear. External links use `↗` as a visual supplement, never as the accessible name.

### Status chip

Statuses use a dot, word, and semantic color: `Open`, `In progress`, `Merged`, `Needs help`, `Archived`. Chips are informational by default; use a button only when they change a filter.

### Project card

Project cards include status, category, title, one-sentence purpose, and one clear destination. The entire card may not be a link when it contains secondary actions. A visible focus-within treatment is required.

### Input

Labels are persistent above inputs. Helper and error text occupy a stable region. Errors include text and an icon or prefix; never color alone. Use `aria-describedby` and `aria-invalid` where appropriate.

### Notice

Use `info`, `success`, `warning`, and `danger` variants. Each has a plain-language heading, optional next action, semantic icon, and live-region behavior only when dynamically inserted.

### Terminal panel

Terminal styling is for real commands, examples, and status—not atmosphere-only fake code. Provide a copy action, visible focus, wrap long lines, and retain semantic text contrast.

## Patterns

### Project index

Lead with filterable status and purpose, not logos. Preserve a stable URL for filtered views. Empty states should explain what exists and how to contribute.

### Contribution invitation

Use this order: context → concrete ways to help → skill/time expectation → code of conduct → destination. “Good first issue” must point to maintained work, not a dead-end label.

### Public status

Every active project displays current state, maintainer, last meaningful update, known constraints, and next useful action. Unknown is a valid documented state.

### Destructive confirmation

Name the object, state the consequence, provide a non-destructive exit, and require deliberate confirmation. Never use nostalgia or playful character art inside destructive flows.

## Shellfolk art direction

Shellfolk are modular maintainers, not mascots pasted onto products. Their square heads, softened joints, and bracket-shaped visors derive directly from the mark. Depict two or more whenever possible: pairing, reviewing, carrying, repairing, or sharing one workstation. Their world uses beige computing hardware, community noticeboards, plants, mugs, paper manuals, and modern accessibility equipment.

Avoid penguins, horns, wings, capes, weapons, exaggerated gamer poses, collectible-toy gloss, branded game proportions, or faces that imply gender/race through stereotypes. Nostalgia should come from shared rituals and materials, not copied characters.

## Voice

| We sound | Not like |
|---|---|
| Direct and neighborly | Corporate or overfamiliar |
| Honest about status | Breathless or absolute |
| Technically capable | Gatekeeping or jargon-first |
| Inviting action | Vague inspiration |

Prefer: “Here’s what works.” “This part is still rough.” “Pick it up here.” “There’s room to help.”

Avoid: “Revolutionary.” “Effortless.” “For everyone” without evidence. “Democratize.” “Join the movement” as a substitute for a concrete action.

## Accessibility baseline

- Target WCAG 2.2 AA; treat visible focus and 44 px targets as defaults.
- Text contrast: 4.5:1 minimum; large text: 3:1; meaningful UI boundaries: 3:1.
- Support 200% text zoom, reflow at 320 CSS px, forced colors, reduced motion, and keyboard-only use.
- Animation must clarify state, remain under 400 ms, never flash, and stop under `prefers-reduced-motion`.
- Character and texture imagery is decorative unless it carries unique information; decorative instances use empty alt text.

## Governance

- System version follows semantic versioning. Tokens and components carry the same release number.
- Patch: correction without visual/API change. Minor: additive token/component. Major: rename, removal, or meaning change.
- Deprecations remain available for one minor release and include a migration note.
- A system change requires: problem statement, before/after, token impact, accessibility review, responsive evidence, and maintainer approval.
- Source of truth: this directory. `tokens.css` is canonical; generated platform formats must not be hand-edited.

## Sources and standards

- [WCAG 2.2](https://www.w3.org/TR/WCAG22/) for contrast, reflow, target, motion, and input guidance.
- [WAI’s current WCAG 2.2 understanding material](https://www.w3.org/WAI/WCAG22/understanding/) for focus and implementation interpretation.
- [Linux kernel coding style](https://www.kernel.org/doc/html/latest/process/coding-style.html) for the cultural preference toward simplicity, readability, maintainability, and commonly available tools—not literal visual imitation.
