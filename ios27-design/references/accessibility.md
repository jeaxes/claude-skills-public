# iOS 27 Accessibility — Unified Reference

The accessibility story for this design system is real but was scattered:
contrast/parity rules live in `CONTRIBUTING.md`, the glass legibility
checklist lives in [glass-legibility.md](glass-legibility.md), the touch
target lives in `spacing.json`, and Reduce Motion / Reduce Transparency /
VoiceOver guidance is spread across ~20+ component and section specs in
`packages/metadata/`. This file is the single place that ties each Apple
accessibility setting to its **token override**, its **CSS hook**, and its
**native (SwiftUI / UIKit) hook**.

Every numeric CSS value below is an **approximation for web rendering**.
Where Apple publishes no number (Liquid Glass legibility, Reduce
Transparency opacity, symbol-effect duration, Bold Text weight delta), this
file says so explicitly — never treat the web number as Apple-authoritative.

## References

- HIG — Accessibility: https://developer.apple.com/design/human-interface-guidelines/accessibility
- HIG — Typography (Dynamic Type): https://developer.apple.com/design/human-interface-guidelines/typography
- HIG — Color: https://developer.apple.com/design/human-interface-guidelines/color
- HIG — Motion: https://developer.apple.com/design/human-interface-guidelines/motion
- `UIAccessibility` flags: https://developer.apple.com/documentation/uikit/uiaccessibility
- SwiftUI Environment (accessibility): https://developer.apple.com/documentation/swiftui/environmentvalues
- WCAG 2.1 / 2.2 (W3C): https://www.w3.org/WAI/WCAG22/Understanding/
- Glass legibility & WCAG-on-gradient: [glass-legibility.md](glass-legibility.md) §6
- Color tokens (4 modes incl. IC): [tokens.md](tokens.md)
- Light/Dark Parity Contract: `CONTRIBUTING.md`

## Setting → hook map (TL;DR)

| Apple setting | UIKit flag | SwiftUI env | CSS hook | Token override |
|---|---|---|---|---|
| Dynamic Type (incl. AX1–AX5) | `preferredContentSizeCategory` | `dynamicTypeSize` | `rem` / `clamp()` on font-size | `typography.json` `dynamicType.ax1…ax5` |
| Increase Contrast | `isDarkerSystemColorsEnabled` | `colorSchemeContrast == .increased` | `@media (prefers-contrast: more)` | `colors.json` `icLight` / `icDark` |
| Reduce Transparency | `isReduceTransparencyEnabled` | `accessibilityReduceTransparency` | `@media (prefers-reduced-transparency: reduce)` | glass → opaque `--color-bg-secondary` |
| Reduce Motion | `isReduceMotionEnabled` | `accessibilityReduceMotion` | `@media (prefers-reduced-motion: reduce)` | `animations.json` `reduceMotion` |
| Differentiate Without Color | `shouldDifferentiateWithoutColor` | `accessibilityDifferentiateWithoutColor` | (none — always render glyph) | SF Symbol per state |
| Bold Text | `isBoldTextEnabled` | `legibilityWeight == .bold` | (none — read natively) | weight shift +1 step |
| On/Off Labels | (no public read API) | (no public read API) | (none — render glyphs) | `colors.json` `miscellaneous.toggle.axLabelOff` |

> Reality check on the CSS layer: a consumer using only `@tokens/css` today
> gets `prefers-color-scheme: dark` and nothing else. The token *data* for
> AX sizes, IC colors, and reduce-motion already exists — the media queries
> that wire them into CSS are listed below and still need shipping.

## 1. Dynamic Type (incl. AX1–AX5)

Never hardcode `px` on text. Scale with the type system so every style
grows with the user's chosen content-size category, all the way to **AX5**.
`typography.json` defines all 12 categories: the 7 standard
(`xSmall…xxxLarge`) plus the five accessibility sizes
(`ax1…ax5` = `accessibilityMedium / Large / ExtraLarge / ExtraExtraLarge /
ExtraExtraExtraLarge`). Body grows roughly `17pt (large) → 53pt (AX5)`.

**Caveat (provenance):** Apple publishes a per-style point table only at the
default *Large* setting. The AX1–AX5 per-style values in `typography.json`
are **UIFontMetrics-observed / community-derived, not Apple-published** —
see the `_dynamicTypeNote` key. The four title styles are encoded as holding
flat at their `xxxLarge` sizes (largeTitle 40 / title1 34 / title2 28 /
title3 26) across the AX range; this title-cap behavior was **not**
re-confirmed against the live Apple table. If exact title metrics matter,
verify empirically with `UIFont.preferredFont(forTextStyle:)` under each
`.accessibility*` trait.

**SwiftUI** — text styles scale automatically:

```swift
Text("Title").font(.headline)        // scales with Dynamic Type, incl. AX sizes

// Switch layout (not just size) at accessibility sizes:
@Environment(\.dynamicTypeSize) private var size
var body: some View {
    if size.isAccessibilitySize {
        VStack { icon; label }       // stack instead of side-by-side
    } else {
        HStack { icon; label }
    }
}
```

**CSS** — drive font-size from a scalable unit, never a fixed `px`:

```css
/* rem follows the user's root font-size; clamp() lets type grow toward AX5 */
.ios27-body { font-size: clamp(1.0625rem, 1rem + 0.5vw, 3.3125rem); }
/* 1.0625rem ≈ 17px (large default) … 3.3125rem ≈ 53px (≈ Body at AX5).
   The 53px ceiling is the web approximation of AX5 Body, not an Apple number. */
```

**Rules**
- At `isAccessibilityCategory` / `size.isAccessibilitySize`: switch HStack→VStack,
  hide non-essential glyphs, and **never truncate** body text.
- Test the whole UI at AX5 — it is the de-facto conformance bar.

## 2. Color contrast

Apple's HIG repeats the WCAG ratios: **4.5:1 for body text**, **3:1 for
large text and non-text UI** (icons, borders, focus rings). Apple states the
ratios but does **not** publish a numeric point-size threshold for "large
text" — only WCAG does: large text = **≥18pt regular / ≥14pt bold**
(≈24px / ≈18.66px CSS).

**Liquid Glass has no Apple-published contrast threshold.** Apple keeps glass
legibility qualitative: ensure a legible foreground over any material, avoid
busy content behind critical text, and **test under Increase Contrast +
Reduce Transparency**. The correct measurement posture is to measure the
foreground against the **opaque fallback** (see §4) and against the
gradient's **lightest stop** — full method (lightest-stop sampling,
shadow compensation, AA pass/fail on gradients) lives in
[glass-legibility.md](glass-legibility.md) §6. This file does not duplicate
it; cross-reference it.

## 3. Increase Contrast

`colors.json` ships an `icLight` / `icDark` variant for every accent, label,
fill, background, gray, and separator (the Light/Dark Parity Contract in
`CONTRIBUTING.md` mandates all four modes). When the OS *Increase Contrast*
setting is on, switch the palette to the `ic*` set.

**Native triggers**
- SwiftUI: `@Environment(\.colorSchemeContrast)` → `.increased`
- UIKit: `UIAccessibility.isDarkerSystemColorsEnabled` (and
  `traitCollection.accessibilityContrast == .high`)

**CSS trigger** — `@media (prefers-contrast: more)` (combine with the
dark block for the icDark set):

```css
@media (prefers-contrast: more) {
  :root {
    --color-label-secondary: rgba(60, 60, 67, 0.8);  /* icLight: #3c3c43 a:0.8 (vs default a:0.6) */
    --color-accent-blue:      #1e6ef4;                /* icLight accent */
    --color-bg-secondary:     #ebebef;                /* icLight background */
  }
}
@media (prefers-contrast: more) and (prefers-color-scheme: dark) {
  :root {
    --color-label-secondary: rgba(235, 235, 245, 0.7); /* icDark */
    --color-accent-blue:      #5cb8ff;
    --color-bg-secondary:     #242426;
  }
}
```

Vibrant accents (yellow `#ffcc00`, mint `#00c8b3`) fail body-text contrast on
white — do not use them for text on light backgrounds without meeting 4.5:1.

## 4. Reduce Transparency (CRITICAL for Liquid Glass)

When *Reduce Transparency* is on, the system makes its own materials opaque,
and **your custom glass must do the same**. Liquid Glass surfaces MUST fall
back to an **opaque fill**: drop `backdrop-filter` entirely and use
`--color-bg-secondary` (or the material's solid equivalent). Apple publishes
**no** numeric opacity for this — the fallback is simply *fully opaque*.

**Native triggers**
- SwiftUI: `@Environment(\.accessibilityReduceTransparency)`
- UIKit: `UIAccessibility.isReduceTransparencyEnabled`

**CSS** — the base hook every glass surface should consume:

```css
.ios27-liquid-glass {
  background: var(--glass-bg, rgba(255, 255, 255, 0.6));
  backdrop-filter: blur(var(--glass-blur, 12px));
}

@media (prefers-reduced-transparency: reduce) {
  :root {
    --glass-bg: var(--color-bg-secondary); /* #f2f2f7 light / #1c1c1e dark — opaque */
    --glass-blur: 0px;                      /* no blur: backdrop-filter becomes a no-op */
  }
  .ios27-liquid-glass { backdrop-filter: none; }
}
```

Once opaque, re-measure foreground contrast against the **solid** fill, not
the translucent one. (`materials.json` has no `reduceTransparency` block yet;
this opaque mapping is the spec it should encode.)

## 5. Reduce Motion

When *Reduce Motion* is on, avoid parallax, zoom/scale transitions, and
continuous animation; substitute a **cross-fade** (opacity only). Apple
mandates no duration; cross-dissolve is canonical. `animations.json` already
defines a `reduceMotion` block: `crossFadeDuration: 0.2`, `disable: [push,
pop, scale, "liquidGlass.tabIndicator morph", parallax]`, `keep: [opacity
fades]`.

**Native triggers**
- SwiftUI: `@Environment(\.accessibilityReduceMotion)`
- UIKit: `UIAccessibility.isReduceMotionEnabled`

**CSS**:

```css
@media (prefers-reduced-motion: reduce) {
  * {
    animation-duration: 0.2s !important;   /* crossFadeDuration */
    transition-property: opacity !important;
    transition-duration: 0.2s !important;
  }
  /* stop transform/scale motion only — KEEP the glass material intact.
     Removing backdrop-filter is Reduce Transparency's job, not Reduce Motion. */
  .ios27-liquid-glass,
  .ios27-tab-indicator,
  .ios27-sheet { transform: none !important; animation: none !important; }
}
```

Replace slide/scale/spring with a 0.2s `ease-out` opacity transition; keep
plain opacity fades.

## 6. Differentiate Without Color

Color alone must never carry meaning. Pair every color cue with a
**shape, glyph, or text label**. Status indicators carry an SF Symbol +
label, not just a hue. Suggested glyph-per-state map:

| State | SF Symbol | Color (also) |
|---|---|---|
| success | `checkmark.circle` | green |
| warning | `exclamationmark.triangle` | yellow/orange |
| error | `xmark.octagon` | red |
| live / active | `dot.radiowaves.up.forward` | red + pulsing dot |

Note: [glass-legibility.md](glass-legibility.md) §5 status chips currently
distinguish Live/Neutral/Disabled mainly by fill color — always render the
glyph so the state survives color-blind viewing.

**Native:** `@Environment(\.accessibilityDifferentiateWithoutColor)` /
`UIAccessibility.shouldDifferentiateWithoutColor`. **Web:** there is no media
query — render the glyph unconditionally (the safe color-blind default).

## 7. Bold Text

When the OS *Bold Text* setting is on, the system makes fonts heavier
UI-wide. System-font native apps inherit this automatically; web and
cross-platform consumers must opt in by shifting each style up roughly **one
weight step** (Regular→Medium, Semibold→Bold). Apple publishes no numeric
weight delta.

- SwiftUI: branch on `@Environment(\.legibilityWeight) == .bold`.
- UIKit: `UIAccessibility.isBoldTextEnabled`.
- Web: there is **no** media query for this. Read it natively (a Tauri /
  native shell can read the system setting and toggle a `.bold-text` class);
  otherwise provide a heavier base weight mode.

## 8. Minimum touch target

`spacing.json` `touchTarget.minimum = 44` with the **corrected** note. The
facts (these had been misstated before):

- **44×44pt is an Apple HIG figure**, not a WCAG AA requirement.
- **WCAG 2.1 SC 2.5.5 Target Size (Enhanced) = 44×44 CSS px → level AAA.**
- **WCAG 2.2 SC 2.5.8 Target Size (Minimum) = 24×24 CSS px → level AA.**
- WCAG units are CSS **px**; Apple's are **pt**.

So 44 satisfies Apple HIG and WCAG AAA; the WCAG **AA** floor is 24. Keep
every tappable control at ≥44pt regardless — the HIG figure is the stricter,
better target.

## 9. Focus indicators

Provide a **shared, contrast-verified focus ring** on *all* interactive
elements (not just buttons). Use `:focus-visible` with a **2px ring at ≥3:1**
against adjacent surfaces, in all four modes. Today only `button.md` ships a
ring (`outline: 2px solid #0088ff; outline-offset: 2px`) — promote it to a
shared token and add a "Focus state" row to every interactive spec (toggle,
segmented-control, text-field, tab-bar, stepper, page-control).

```css
:root {
  --focus-ring-color: #0088ff;  /* ⚠ #0088ff on white ≈ 3.0:1 — borderline at the 3:1 bar */
  --focus-ring-width: 2px;
  --focus-ring-offset: 2px;
}
@media (prefers-contrast: more) {
  :root { --focus-ring-color: #1e6ef4; }  /* IC accent for a safer margin */
}
.ios27-interactive:focus-visible {
  outline: var(--focus-ring-width) solid var(--focus-ring-color);
  outline-offset: var(--focus-ring-offset);
}
```

Re-verify the ring at ≥3:1 in light, dark, IC-light, and IC-dark — `#0088ff`
is on the edge on white (WCAG 1.4.11 non-text contrast; 2.4.7 / 2.4.13 focus
appearance). Native: Full Keyboard Access provides a system ring; custom
controls still need a clear indicator meeting 3:1.

## 10. VoiceOver & On/Off labels

**VoiceOver:** every control needs an accurate label, trait, and (where
useful) hint. Icon-only buttons MUST have a label. Decorative images are
hidden from the accessibility tree.

```swift
Button(action: share) { Image(systemName: "square.and.arrow.up") }
    .accessibilityLabel("Share")           // icon-only → needs a label

Image("hero-decoration").accessibilityHidden(true)  // decorative
```

```html
<button aria-label="Share"><svg aria-hidden="true">…</svg></button>
<img src="hero-decoration.png" alt="" aria-hidden="true">
```
(UIKit: set `isAccessibilityElement = false` on decorative views; SwiftUI:
`.accessibilityHidden(true)`.)

**On/Off labels for toggles:** the system *On/Off Labels* setting adds visible
state glyphs to switches so state is discernible without color — a **`|` (I)**
in the knob when **On**, an **`o` / hollow circle (O)** when **Off**. On iOS this
setting **is** publicly readable: `UIAccessibility.isOnOffSwitchLabelsEnabled`
(with `onOffSwitchLabelsDidChangeNotification`) — render the glyphs only when it
is enabled; rendering them unconditionally surfaces them to users who never
turned the setting on. The web platform has no equivalent media query, so gate
them behind your own app setting, or treat always-on as a deliberate
Differentiate-Without-Color choice (§6) only if that is an explicit product
decision. Use the `colors.json`
`miscellaneous.toggle.axLabelOff` token for the OFF glyph
(light `#b3b3b3` / dark `#a6a6a6` / icLight `#ffffff` / icDark `#ffffff`).

---

**Related:** [glass-legibility.md](glass-legibility.md) (§6 WCAG-on-gradient,
the opaque-fallback rationale), [tokens.md](tokens.md) (the four-mode color
tokens incl. IC), and `CONTRIBUTING.md` (the Light/Dark Parity Contract that
guarantees an `icLight`/`icDark` exists for every token).
