# SF Symbols — iOS 27 Reference

SF Symbols 7 is the system iconography of iOS 27 (shipped at WWDC25):
**over 7,000 symbols**, integrated with the San Francisco font, scaling
with Dynamic Type. They have **4 rendering modes**, **9 weights**,
**3 scales**, Variable Color, and a documented animation set.

This file consolidates rendering modes / weights / scales / variable
color / animations and wires them to this repo's tokens. For symbols on
Liquid Glass, see [glass-legibility.md §8](glass-legibility.md) — that
guidance is **not** duplicated here.

## Packaging note

SF Symbols ships as a **separate Apple app + font** (SF Symbols 7), it is
**not** bundled in the Figma kit and there is no `icons` token namespace
in `packages/tokens`. On web, use an SF-Symbols-like icon set or inline
SVG and apply the rules below. Treat sizing/animation numbers marked
"web approximation" as rendering conventions, never as Apple-authoritative
values (Apple publishes no exact ratios or effect durations).

## Rendering Modes

Four modes (SwiftUI `symbolRenderingMode(...)`). When to use each, and how
each maps to this repo's accent + label-opacity tokens:

| Mode | Apple behavior | Use when | Token mapping |
|------|----------------|----------|---------------|
| Monochrome | Single tint fills the whole symbol | Default; toolbars, inline glyphs, anything where the icon is one solid color | `--color-label-primary`, or one `accents.*` |
| Hierarchical | One tint applied at different per-layer opacities for depth | A single-color icon that needs visual layering (e.g. filled badge) | One accent; derive depth from the label-opacity scale (see below) |
| Palette | Up to 3 explicit colors on distinct layers | Two-/three-tone icons where you control each layer | Up to 3 of `accents.*` + `labels`/`fills` |
| Multicolor | Apple's own intrinsic colors are preserved | Symbols with a canonical color identity (e.g. battery, weather) | Use the symbol's own colors — **never override** |

**Hierarchical depth is system-derived, not Apple-published.** Apple does
NOT publish exact secondary/tertiary opacity values. Approximate depth
from the existing label-opacity scale ([tokens.md](tokens.md) Labels):

| Layer | Opacity (Light) | Opacity (Dark) |
|-------|-----------------|----------------|
| primary | 1.0 | 1.0 |
| secondary | 0.6 | 0.7 |
| tertiary | 0.3 | 0.3 |

### Palette / Hierarchical token mapping

- Hierarchical / Monochrome tint → `accents.*.light` / `accents.*.dark`.
  Under **Increased Contrast**, swap to `accents.*.icLight` / `.icDark`.
- Palette → up to 3 colors from `accents.*` plus `labels` / `fills`.
- Always pair the `ic*` variant so the symbol keeps contrast parity in the
  Increased Contrast modes (same as the rest of the color system).
- These reuse existing tokens and add none.

## Weights

Nine weights, matching the San Francisco font ramp:
**ultralight, thin, light, regular, medium, semibold, bold, heavy, black.**

**Rule: a symbol's weight should MATCH the weight of the adjacent text.**
A Semibold Headline pairs a Semibold symbol; a Regular Body pairs a
Regular symbol. Aligning the two keeps optical weight consistent inline.

Mapping to this repo's typography ramp ([SKILL.md](../SKILL.md)
Typography → the `Weight` column):

| Text style | Text weight | Symbol weight |
|------------|-------------|---------------|
| Large Title / Title 1 / Title 2 | Regular or Bold | match (Regular ↔ Regular, Bold ↔ Bold) |
| Title 3 | Regular / Semibold | match |
| Headline | Semibold | Semibold |
| Body / Callout / Subheadline | Regular / Semibold | match |
| Footnote / Caption 2 | Regular / Semibold | match |
| Caption 1 | Regular / Medium | match |

**On Liquid Glass the floor is `.semibold`** (per
[glass-legibility.md §8](glass-legibility.md)) — even when the paired text
is lighter, never drop below Semibold on a glass control surface. That
rule overrides "match the text weight" for the glass case only.

## Scales

Three scales — **small / medium / large** — sized *relative to the
surrounding text/font* so a symbol stays visually balanced inline.

- SwiftUI: `imageScale(.small / .medium / .large)`
- UIKit: `UIImage.SymbolConfiguration.Scale`

Apple matches symbols to the font/text in general; it does **not** publish
a strict cap-height ratio per scale. (The repo's glass guide references
x-height — there is no authoritative single ratio.) Do not assert a
"relative to cap height" rule as an Apple spec.

**Web approximation** — render the symbol inline at `1em` so it
auto-scales with `font-size`. Offer the three scales as multipliers
(web convention, not Apple values):

| Scale | Web height (approximation) |
|-------|----------------------------|
| small | ≈ 0.9em |
| medium | ≈ 1.0em |
| large | ≈ 1.15em |

### Inline with text (web)

Inline symbols sit on the **text baseline** and inherit `font-size`.

- Set symbol height ≈ the label's `font-size`.
- Vertical-align to the baseline. A practical offset is
  `vertical-align: -0.125em` on a `1em` symbol — this px/em value is a
  **web convention, not an Apple number**.
- **Don't** float inline symbols off the baseline or pin them to a fixed
  px size that ignores the surrounding text.

## Variable Color

Variable Color fills a symbol's layers **progressively by a 0–100%
value**, and works across all rendering modes. It is value-driven, not a
fixed per-layer opacity.

- Use for: signal strength (wifi/cellular), volume/level, progress/loading.
- SwiftUI: `symbolEffect(.variableColor...)` with **iterative** vs
  **cumulative** options and an optional **reversing** flag.
  - *Iterative*: one layer lit at a time, advancing.
  - *Cumulative*: layers stay lit as the value climbs (signal bars).
- The "thresholds evenly spaced 0–100" detail is layer-count-dependent and
  tied to the value — not a fixed opacity Apple publishes.

**Web approximation** — drive per-layer SVG `opacity` (or `fill`) from a
single `--value` variable (0–1). Number of lit layers = `round(value ×
layerCount)`. This is a value-driven approximation, not an Apple ratio.

## Animations

SF Symbols effects, with the version each landed and the `symbolEffect(...)`
name. **New in SF Symbols 7 / iOS 27** (WWDC25 session 337): Draw On,
Draw Off, Variable Draw, Magic Replace enhancements, and optional gradient
rendering across all modes (Whole Symbol / By Layer / Individually).

Apple publishes **no exact durations** for these effects — the web column
maps each onto this repo's existing spring/duration tokens
([SKILL.md](../SKILL.md) Springs: `snappy` / `bouncy` / `gentle` / `stiff`),
which is an approximation, not an Apple value.

| Effect | Since | Intent | Web approximation |
|--------|-------|--------|-------------------|
| Draw On (Variable Draw) | 7 / iOS 27 | Stroke draws itself in | SVG `stroke-dashoffset` reveal, `gentle` timing |
| Draw Off | 7 / iOS 27 | Stroke retracts | reverse `stroke-dashoffset`, `gentle` |
| Magic Replace | 7 / iOS 27 | Smart swap between related symbols (shared enclosures, e.g. circle→filled checkmark) | crossfade + scale, `gentle` (or `stiff` for snap) |
| Replace | 5 / iOS 17 | Swap one symbol for another | crossfade, `stiff` |
| Appear | 5 / iOS 17 | Symbol fades/scales in | fade + scale 0.85→1, `snappy` |
| Disappear | 5 / iOS 17 | Symbol fades/scales out | reverse Appear, `snappy` |
| Bounce | 5 / iOS 17 | One-shot attention nudge | scale pop, `snappy` (overshoot) or `bouncy` for stronger pop |
| Pulse | 5 / iOS 17 | Opacity throb for ongoing state | opacity 1↔0.4 loop, ease-in-out |
| Variable Color | 5 / iOS 17 | Progressive 0–100% layer fill | per-layer opacity from `--value` (see above) |
| Wiggle | 6 / iOS 18 | Side-to-side shake for emphasis | small rotate/translate keyframes |
| Rotate | 6 / iOS 18 | Spins a rotatable layer | `transform: rotate` keyframes |
| Breathe | 6 / iOS 18 | Slow scale in/out for a calm "alive" state | scale 1↔1.06 loop, `gentle`, long duration |

Per [glass-legibility.md §9](glass-legibility.md): avoid continuous 60fps
symbol animations on glass surfaces (the backdrop-blur is expensive to
recompute every frame). Prefer one-shot effects (Bounce, Replace) and let
the glass settle.

## Symbols on Liquid Glass

Do not duplicate — see **[glass-legibility.md §8](glass-legibility.md)**.
The legibility-critical rules already live there: weight `.semibold`
minimum (never `.regular`), size matched to text x-height, and color must
match the text color exactly (no independent tint). On glass control
surfaces (tab bars, toolbars) prefer **Monochrome or Hierarchical**
symbols tinted from `--color-label-primary`; reserve **Multicolor** for
content, not chrome.

## CSS Usage

```css
/* Inline symbol that scales with the label and sits on the baseline */
.label .symbol {
  height: 1em;                  /* ≈ font-size (medium scale) */
  width: auto;
  vertical-align: -0.125em;     /* web baseline convention, not an Apple value */
  fill: var(--color-label-primary);   /* monochrome tint */
}

/* Variable Color: drive per-layer opacity from a 0–1 value */
.symbol [data-layer] { opacity: 0.2; }
.symbol[style*="--value"] [data-layer] { /* lit count = round(--value * layers) */ }
```

## JS Usage

```js
import { colors } from '@ios27_design_system/tokens';

// Monochrome / Hierarchical tint
const tint = colors.accents.blue.light;       // "#0088ff"
const tintIC = colors.accents.blue.icLight;   // Increased Contrast variant

// Palette (up to 3): pull distinct accents / labels
const palette = [colors.accents.blue.light, colors.accents.pink.light];
```

---

**Related**: [glass-legibility.md](glass-legibility.md) §8 (symbol on
glass) and §9 (animation on glass), [tokens.md](tokens.md) for accent /
label-opacity tokens, [../SKILL.md](../SKILL.md) for the typography weight
ramp and spring presets these rules map onto.
