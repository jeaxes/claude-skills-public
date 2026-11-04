---
name: ios27-design
description: |
  iOS 27 / iPadOS 27 Liquid Glass design system for web and app development.
  Exact design tokens, component specs, layout patterns, and animation parameters
  from Apple's official Figma Community Kit.

  Use when:
  - Building UI with iOS 27, iPadOS 27, or Liquid Glass design language
  - User mentions "iOS 27", "Liquid Glass", "iPadOS 27", "Apple design"
  - Code imports @ios27_design_system/* packages
  - Creating tab bars, toolbars, sheets, alerts, buttons in Apple style
  - Needing Apple color values, typography scales, spacing, or spring animations
  - Implementing light and dark mode
  - Questions about Liquid Glass blur, refraction, depth parameters

  Do NOT use for: SwiftUI/UIKit native dev (use Apple docs), general CSS unrelated to iOS 27.
---

# iOS 27 Design System

Build iOS 27 Liquid Glass interfaces on web and cross-platform.
Values inherited from the [iOS & iPadOS 26 Figma Community Kit](https://www.figma.com/community/file/1527721578857867021);
iOS 27 deltas from WWDC 2026 (2026-06-08).

**Measured against Apple's official iOS 27 kit** — [Figma file 1651309003795292092](https://www.figma.com/community/file/1651309003795292092/ios-and-ipados-27),
kit 27.0.2, on 2026-07-29. Materials, spacing, component metrics, typography, and
the app icon model come from the kit. Colors measured identical to iOS 26.
Backdrop-blur radii remain approximations — Figma's `GLASS` effect does not expose
its blur through the REST API.

## What iOS 27 changed (read this first)

Liquid Glass was retuned, not replaced.

| Change | Use |
|---|---|
| **Transparency slider** — system-wide, ultra clear ↔ fully tinted, replaces the binary Reduce Transparency toggle | `--ios27-glass-transparency`, `--ios27-glass-opacity-scale`, `--ios27-glass-blur-scale`; presets `.ios27-glass-ultra-clear` / `-clear` / `-default` / `-tinted` / `-fully-tinted` |
| **Stronger diffusion** | Backdrop blur large 18 / medium 15 / small 9 (approximate) |
| **Rim ring** — measured as a LIGHT grey ring, not a dark border | `--ios27-glass-rim` (`#dbdbdb` light, `#a6a6a6` dark), spread 0.5 |
| **Inner shadows** — what reads as the lit rim is two DARK inner shadows | `--ios27-glass-inner`, ±40 Y offset, −40 spread |
| **Uniform toolbar** once content scrolls under the top bar | `.ios27-toolbar-uniform` |
| **Sidebar** edge to edge, colored icons return | `.ios27-sidebar` |
| **Prominent Tab** — search stays a separate capsule; the slot is generalized so any tab can take it. Kit property: `Type: Default / Search Role / Prominent Tab` | Tab Bar spec |
| **App icons** rebuilt as multiple glass layers baked into artwork; gyroscopic shimmer removed | `.ios27-app-icon`, `.ios27-app-icon__layer--{background,middle,foreground}` |

**Rules that follow from this**

- Never hard-code glass opacity or blur. Multiply the scale variables so surfaces
  follow the user's slider.
- `prefers-reduced-transparency: reduce` still overrides the slider. Accessibility
  sits above personalization.
- Verify contrast at **both** ends of the range — passing at the default says
  nothing about ultra clear.
- Do not design an icon whose character depends on motion; the shimmer is gone.
- Refract the layers under the glass, never the top mark — that is what made
  iOS 26 icons read as blurry.

**Token naming**: canonical prefix is `--ios27-*`. iOS 26 names (`--color-*`,
`--font-*`, `--space-*`) resolve through `tokens/css/legacy`.

## Packages

```bash
npm install @ios27_design_system/tokens          # CSS/JS/Dart tokens
npm install @ios27_design_system/svelte           # Svelte 5
npm install @ios27_design_system/rails            # Rails 8 + Hotwire
npm install @ios27_design_system/svelte-inertia   # Svelte 5 + Inertia.js
npm install @ios27_design_system/metadata         # 36 specs + 48 pages
```

## Typography (SF Pro)

| Style | Size | Line Height | Weight | Spacing |
|-------|------|-------------|--------|---------|
| Large Title | 34 | 41 | Regular/Bold | 0.4 |
| Title 1 | 28 | 34 | Regular/Bold | 0.38 |
| Title 2 | 22 | 28 | Regular/Bold | -0.26 |
| Title 3 | 20 | 25 | Regular/Semibold | -0.45 |
| Headline | 17 | 22 | Semibold | -0.43 |
| Body | 17 | 22 | Regular/Semibold | -0.43 |
| Callout | 16 | 21 | Regular/Semibold | -0.31 |
| Subheadline | 15 | 20 | Regular/Semibold | -0.23 |
| Footnote | 13 | 18 | Regular/Semibold | -0.08 |
| Caption 1 | 12 | 16 | Regular/**Semibold** | 0 |
| Caption 2 | 11 | 13 | Regular/Semibold | 0.06 |

Font stack: `"SF Pro", -apple-system, system-ui, sans-serif`
**Dynamic Type**: 7 standard sizes (xSmall–xxxLarge) + **5 accessibility sizes (AX1–AX5)** per style — never hardcode px. **Weights**: 9-step SF ramp (ultraLight 100 → black 900). SF Pro Text < 20pt, Display ≥ 20pt (auto).

## Spacing (8pt grid)

```
Scale:  0=0, 1=4, 2=8, 3=12, 4=16, 5=20, 6=24, 8=32, 10=40
Inset:  xs=8, sm=12, md=16, lg=20, xl=24, xxl=32
Margin: iPhone=16px, iPad=20px
Radius: none=0, xs=4, sm=8, md=10, lg=12, xl=16, xxl=20, xxxl=26, glass=34, full=9999
```

iOS 27 glass chrome converges on **34** (alert, menu, context menu, Liquid Glass
regular, floating sheet top) with **38** for larger surfaces (popover,
edge-to-edge sheet, iPad sheet). The iOS 26 14pt dialog radius is gone.

## Liquid Glass

Measured from kit 27.0.2. Regular large and medium are identical.

```
Regular (large = medium)      radius 34
  Light  fill #ffffff/0.70 + #bfbfbf/0.10 overlay
         shadow 0 8 48 rgba(0,0,0,0.25)
         rim    #dbdbdb spread 0.5
  Dark   fill #1a1a1a/0.70
         shadow 0 8 48 rgba(0,0,0,0.45)
         rim    #a6a6a6 spread 0.5
  Both   inner shadow ±40 Y, blur 10, spread −40

Regular small (48pt)          radius 100 idle / 1000 active
  Light  #747480/0.08     Dark  #767680/0.12
  Active + Prominent: white backing 94% + #0088ff tint, LINEAR_BURN

Clear                         radius 23
  base #101010, overlay #ffffff/0.04

Scroll edge   soft: container blur 10 + masked layer blur 100 @ 0.9
              hard: blur 6, #ffffff/0.85 light, #000000/0.55 dark

Backdrop blur (approximate)   large 18, medium 15, small 9, clear 7
```

## Animations

```
Springs (response / damping → CSS):
  snappy:  0.3 / 0.8  → cubic-bezier(0.34, 1.56, 0.64, 1.0)   [buttons, tabs]
  bouncy:  0.5 / 0.65 → cubic-bezier(0.68, -0.55, 0.265, 1.55) [launch, notification]
  gentle:  0.55 / 0.825 → cubic-bezier(0.25, 0.46, 0.45, 0.94) [sheets, pages]
  stiff:   0.25 / 1.0 → no bounce                                [alerts, menus]

Durations: tab=0.3s, sheet-present=0.5s, sheet-dismiss=0.3s,
  alert=0.2s, context-menu=0.25s, tab-indicator=0.45s
```

## Component Dimensions

| Component | Height | Key Specs |
|-----------|--------|-----------|
| Status Bar | 62pt iPhone / 24pt iPad | kit band; UIKit still reports a 59pt inset |
| Nav Bar | **54pt** / 125pt large title | was 44 / 96 in iOS 26 |
| Tab Bar | **54pt** control, 62pt glass platter, 95pt total | minimized 40 / 48 / 88 |
| Toolbar | **top 54pt, bottom 84pt** | no longer one height |
| List Row | **52pt** / 68pt tall | 16pt separator inset |
| Alert | **300pt** wide, radius **34** | buttons 48pt pill, 14pt padding, 8pt gaps |
| Sheet | Medium / Large / Large (Stacked) | grabber **58×4pt** @ top 5, radius 38 |
| Button | 28 / 34 / 50pt | pill |
| Progress | determinate track **4pt** (was 6) | spinners 14 / 20 / 35 |
| Touch Target | 44×44pt minimum | WCAG AA |
| Safe Area | top=59pt, bottom=34pt | iPhone 16 — see Status Bar note |

## Rules

**DO**: Use semantic tokens (`--color-label-primary`), 8pt grid, min 44pt touch, spring animations, Light+Dark support.

**DON'T**: Hardcode hex colors, skip the glass shadow stack, use linear easing, skip Reduce Transparency / Reduce Motion fallbacks (see [accessibility.md](references/accessibility.md)).

⚠️ Apple **removed the increased-contrast appearance mode** from the iOS 27 kit's
Colors page (change log 27.0.0). Increased Contrast is still an accessibility
setting to honor at runtime; it is no longer a separate authoring mode.

**Glass legibility** (recurring shipping mistake — see [glass-legibility.md](references/glass-legibility.md)):
- Glass belongs to the **navigation layer**. Toolbars, tab bars, sheet grabbers — yes. Heroes, content cards, photo overlays — no.
- **Never nest glass.** `Material` on top of `Material` (or `backdrop-filter` on top of `backdrop-filter`) compounds blur and turns to fog. One layer at most.
- **Primary CTA on a gradient = solid `#fff` fill**, secondary CTA = `rgba(black, 0.32)` + 1.5px white border. Light glass on gradient looks ghosted.
- **White text on gradient needs `text-shadow 0 1px 3px rgba(0,0,0,.15)`.** Subtitles ≥ 0.85 opacity.
- Measure WCAG AA against the gradient's **lightest stop**, not its average.

## Detailed References

- **Full color tokens** (79 vars × 4 modes): [references/tokens.md](references/tokens.md)
- **36 component specs**: [references/components.md](references/components.md)
- **Layout patterns + 48 pages**: [references/layouts.md](references/layouts.md)
- **Framework code examples**: [references/frameworks.md](references/frameworks.md)
- **Glass legibility pitfalls** (CTAs, text on gradients, nesting rules): [references/glass-legibility.md](references/glass-legibility.md)
- **Liquid Glass native API** (SwiftUI glassEffect/.regular/.clear/.identity, GlassEffectContainer, token→API map): [references/liquid-glass-api.md](references/liquid-glass-api.md)
- **SF Symbols** (rendering modes, weights, scales, Variable Color, SF Symbols 7 animations): [references/sf-symbols.md](references/sf-symbols.md)
- **Accessibility** (Dynamic Type AX1–AX5, Reduce Transparency / Reduce Motion fallbacks, contrast, focus): [references/accessibility.md](references/accessibility.md)
