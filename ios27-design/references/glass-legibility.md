# Liquid Glass Legibility — Pitfalls & Rules

Liquid Glass is a *navigation layer* effect. Once you start layering it
on heroes, gradients, or photo backgrounds, contrast collapses quickly
and you ship buttons that no one can read. These are the recurring
anti-patterns from real shipped mistakes and the rules that prevent
them.

## TL;DR

| Surface | What to use | What not to use |
|---|---|---|
| Toolbar / Tab bar / Sheet grabber | `Material.regular` / `Material.thin` | Custom gradients |
| Chip on gradient hero | `rgba(white, 0.22)` + `border rgba(white, 0.35)` | `Material` (becomes muddy) |
| **Primary CTA on gradient** | Solid `#fff` fill, gradient text color | Glass fill (vanishes) |
| **Secondary CTA on gradient** | `rgba(black, 0.32)` + `border rgba(white, 0.55)` + text-shadow | Light glass (glass-on-glass) |
| Body text on gradient | White, `text-shadow 0 1px 3px rgba(0,0,0,.15)` | No shadow, opacity < 0.85 |
| Meta-card inside hero | Glass with hairline border, single layer | Nested glass |

## 1. Glass-on-glass is the #1 anti-pattern

If you put a translucent button on a gradient that already has glass
material applied, the button's blur layer composites against an
already-blurred backdrop — both lose definition and the result is a
flat fog. Apple's own guidance: **glass belongs to the navigation
chrome, not the content** ([WWDC25, Donny Wals notes]).

**Bad** (Swift):
```swift
ZStack {
    LinearGradient(...)               // gradient hero
    .ultraThinMaterial                // glass over gradient ← already a glass layer
    Button { } label: {
        Text("Create Bracket")
            .background(.ultraThinMaterial)   // ← second glass layer
    }
}
```

**Good**:
```swift
ZStack {
    LinearGradient(...)               // gradient hero (NO material)
    Button { } label: {
        Text("Create Bracket")
            .padding()
            .background(Color.black.opacity(0.32))     // solid-tinted, not glass
            .overlay(RoundedRectangle(cornerRadius: 14)
                .stroke(Color.white.opacity(0.55), lineWidth: 1.5))
    }
}
```

CSS equivalent:
```css
/* Bad: backdrop-filter on top of a backdrop-filter parent */
.cta { background: rgba(255,255,255,.22); backdrop-filter: blur(20px); }

/* Good: solid-tinted on gradient, strong border */
.cta-secondary {
  background: rgba(0,0,0,.32);
  border: 1.5px solid rgba(255,255,255,.55);
  color: #fff;
  text-shadow: 0 1px 2px rgba(0,0,0,.25);
}
```

## 2. White text on gradient needs a shadow

A gradient is bright in some places and dark in others — white text
will hit a light region and disappear. Always add a hairline shadow.

```swift
Text(title)
    .foregroundStyle(.white)
    .shadow(color: .black.opacity(0.12), radius: 3, y: 1)
```

```css
.hero-title { color: #fff; text-shadow: 0 1px 3px rgba(0,0,0,.15); }
```

Subtitles can be softer (`opacity: 0.9`) but never below `0.85` —
below that they're indistinguishable from disabled state.

## 3. CTA hierarchy on gradients: solid vs dark-glass

The primary CTA must be **solid white** (or solid accent) and the text
should take on the gradient's terminal color. This makes it the single
brightest object on screen.

The secondary CTA must be **dark-glass**, not light-glass. A light
button on a gradient hero looks "ghosted" — users can't tell whether
it's enabled or a placeholder.

```
┌─────────────────────────────────────┐
│  GRADIENT HERO                      │
│                                     │
│  ┌──────────────┐ ┌──────────────┐  │
│  │  Primary     │ │  Secondary   │  │
│  │  (solid #fff)│ │  (dark glass)│  │
│  │  text=tint   │ │  text=#fff   │  │
│  └──────────────┘ └──────────────┘  │
└─────────────────────────────────────┘
```

## 4. Meta cards inside heroes — single glass layer only

A "stats strip" (participants / count / D-day) is fine on a gradient
hero **if it's one glass layer with a hairline white border** —
two layers will mud out.

```swift
HStack { /* meta items */ }
    .padding()
    .background(
        RoundedRectangle(cornerRadius: 18, style: .continuous)
            .fill(Color.white.opacity(0.18))
            .overlay(RoundedRectangle(cornerRadius: 18, style: .continuous)
                .stroke(Color.white.opacity(0.3), lineWidth: 1))
            .background(.ultraThinMaterial, in: RoundedRectangle(cornerRadius: 18, style: .continuous))
    )
```

The `.ultraThinMaterial` is the *only* glass — the white fill on top
of it is a tint, not a second blur.

## 5. Status chip pill colors

| State | Fill | Border | Notes |
|---|---|---|---|
| Live / urgent | `red.opacity(0.35)` | `white.opacity(0.5)` | + pulsing dot |
| Neutral status | `white.opacity(0.22)` | `white.opacity(0.35)` | |
| Disabled / cancelled | `black.opacity(0.25)` | `white.opacity(0.2)` | text opacity 0.7 |

## 6. WCAG AA on gradients

Apple's HIG asks for **4.5:1** contrast on body text and **3:1** on
large text. Apple publishes **no numeric contrast threshold for the Liquid Glass material itself** — it is content-adaptive; measure the foreground against the gradient's lightest stop, and see [accessibility.md](accessibility.md) for the Reduce Transparency opaque fallback. Gradients vary by position — measure the lightest stop,
not the average. If a gradient's lightest stop is brighter than
`#bbb`, white text without shadow will fail AA there. Either:

- Darken the gradient's lightest stop, or
- Add a shadow (compensates ~1.5x perceived contrast), or
- Place text only in the darker half of the gradient.

## 7. Diagnostic checklist

Before shipping any glass surface, run these:

- [ ] Take a screenshot, blur it 20%. Are CTA buttons still
      distinguishable from the background?
- [ ] Increase Contrast (Settings → Accessibility → Display) — does
      every text+background pair gain a visible border / fill?
- [ ] Squint test: at 30% screen brightness in sunlight (simulate by
      lowering display to 25%), can the primary CTA be picked out in
      under 1 second?
- [ ] Dark mode parity: does the same surface in dark mode look
      *intentional*, or does the gradient invert into a muddy soup?
- [ ] No nested `Material` / `backdrop-filter` anywhere in the tree.
- [ ] Every white text node has a shadow OR is on a fill of
      `rgba(black, 0.32)+`.

## 8. SF Symbol on glass

When a button uses both an SF Symbol and text:

- Symbol weight: `.semibold` minimum, never `.regular`
- Symbol size matches text x-height, not cap-height — use
  `.font(.system(size: 13, weight: .semibold))` for a 14pt label
- Color: match text color exactly, never tint independently
  (independent tint reads as a status icon, not decoration)

## 9. Animation while glass is visible

Glass material itself has 7-14px backdrop-blur which is *expensive*
to recompute every frame. Avoid these on glass surfaces:

- 60fps property animations on `backgroundColor` / `opacity`
- Continuous scale/rotate gestures
- Particle effects behind the glass

Use Apple's springs (`snappy`, `gentle`) for one-shot transitions and
let the glass settle.

---

**Related**: [components.md](components.md) for component dimensions,
[tokens.md](tokens.md) for the color tokens this guide references, [accessibility.md](accessibility.md) for Reduce Transparency / Reduce Motion fallbacks, and [liquid-glass-api.md](liquid-glass-api.md) for the native SwiftUI API.
