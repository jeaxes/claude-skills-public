# Liquid Glass — Native SwiftUI API ↔ Web Tokens

The native SwiftUI Liquid Glass API mapped to this repo's web/CSS tokens.
**Read this before treating any `materials.json` number as authoritative:**
Apple publishes **no** opacity, blur, frost, depth, corner-radius, or
container-spacing value for the Liquid Glass material. It is a
system-rendered, content-adaptive material. Every number in
`materials.json` is an **approximation for web rendering** — on Apple
platforms you use the API below, which exposes *style choices*, not
tunable blur/opacity knobs.

## References

- Apple — [Applying Liquid Glass to custom views](https://developer.apple.com/documentation/SwiftUI/Applying-Liquid-Glass-to-custom-views)
- Apple — [Adopting Liquid Glass](https://developer.apple.com/documentation/TechnologyOverviews/adopting-liquid-glass)
- WWDC25 Session 323 — [Build a SwiftUI app with the new design](https://developer.apple.com/videos/play/wwdc2025/323/)
- HIG — [Materials](https://developer.apple.com/design/human-interface-guidelines/materials)
- Repo tokens: [`packages/tokens/src/materials.json`](https://github.com/seunghan91/ios27-design-system/blob/main/packages/tokens/src/materials.json)
- Related: [glass-legibility.md](glass-legibility.md), [tokens.md](tokens.md)

## The `glassEffect` modifier

```swift
func glassEffect(
    _ glass: Glass = .regular,
    in shape: some Shape = DefaultGlassEffectShape()
) -> some View
```

- The first parameter is the **style** (`Glass`), defaulting to `.regular`.
- `in:` is a **clipping shape** — `Capsule`, `RoundedRectangle`,
  `ConcentricRectangle`, etc. It is **NOT** a container and **NOT** a
  `GlassEffectContainer`. (A common mistake is to pass a container here;
  the container is a separate wrapper view — see *Morphing* below.)

```swift
// Pill control (the DefaultGlassEffectShape analogue)
Button("Filter") { }
    .glassEffect(.regular, in: Capsule())

// Rounded card
content
    .glassEffect(.regular, in: RoundedRectangle(cornerRadius: 20))
```

## The three `Glass` styles

| Style | When to use | Web token analogue |
|---|---|---|
| `.regular` *(default)* | Functional / navigation chrome layer (toolbars, tab bars, floating controls). | `liquidGlass.regular.*` |
| `.clear` | More transparent; **only** over media-rich / colorful content where the foreground is high-contrast. | `liquidGlass.clear.*` |
| `.identity` | No glass — for conditionally disabling glass **without** a layout shift. | *(no numeric model; doc only)* |

`.regular` and `.clear` are both single adaptive materials — they
auto-adapt to light/dark appearance and to the content behind them.
`.identity` produces no effect and exists purely so you can toggle:

```swift
content
    .glassEffect(isEnabled ? .regular : .identity)
```

## Glass modifiers

```swift
extension Glass {
    func interactive(_ isEnabled: Bool = true) -> Glass
    func tint(_ color: Color?) -> Glass
}
```

- **`.interactive(_:)`** — makes the glass react to touch with
  system-driven animated motion (lensing / reactive highlight). The
  motion is provided and tuned by the system; **Apple publishes no
  scale, duration, or highlight numbers.**
- **`.tint(_:)`** — colors the glass. Maps to the repo's dark-mode tint
  token (`#ffffff` a:0.06) and, for web, to a low-alpha accent overlay.

```swift
Button("Send") { }
    .glassEffect(.regular.tint(.blue).interactive(), in: Capsule())
```

### Interactivity on the web (NOT Apple values)

There is no native blur/scale number to mirror. For web parity, reuse
the existing springs and add a **clearly non-Apple** approximation:

- press scale ≈ `0.96`
- a brief specular highlight on press

These are web-rendering conveniences only — they are *not* Apple-authored
and must not be treated as the native interactive response.

> Reconciles `glass-legibility.md` §9: the warning against 60fps
> property animation targets **custom** animation on glass, not the
> system-provided `.interactive()` response, which is cheap and
> system-tuned.

## Morphing — `GlassEffectContainer` & friends

`GlassEffectContainer` is a **separate wrapper view** (used like `HStack`
or `ZStack`) that groups nearby glass surfaces so they **merge into one
continuous piece and morph** as they move. It is not the `in:` argument.

```swift
func glassEffectID<ID: Hashable>(_ id: ID, in namespace: Namespace.ID) -> some View
func glassEffectUnion(id: ID?, namespace: Namespace.ID) -> some View
```

```swift
@Namespace private var glassNS

GlassEffectContainer(spacing: 24) {
    HStack {
        Image(systemName: "star")
            .glassEffect(.regular, in: Capsule())
            .glassEffectID("star", in: glassNS)
        Image(systemName: "heart")
            .glassEffect(.regular, in: Capsule())
            .glassEffectID("heart", in: glassNS)
    }
}
```

- **`glassEffectID(_:in:)`** — note the **capital `ID`**. Mirrors
  `matchedGeometryEffect`; drives matched-geometry-style morphing
  transitions between glass elements.
- **`glassEffectUnion(id:namespace:)`** — forces separated pieces to
  render as a single continuous glass shape.
- Merging is **qualitative** — Apple publishes no distance / overlap /
  spacing threshold. `spacing:` has no documented default value.

## Concentric corners

iOS 27 introduces shapes that derive their corner radius from the
container and the hardware's screen-corner curvature, so nested shapes
stay concentric:

- **`ConcentricRectangle`** — conforms to `Shape`; usable as the `in:`
  clipping shape.
- **`containerConcentric`** / **`containerShape`** — derive radius from
  the enclosing container.

```swift
content
    .glassEffect(.regular, in: ConcentricRectangle())
```

Rule of thumb: **inner radius = container radius − inset**, aligned to
the screen-corner curvature. There is no Apple-published fixed numeric
radius for glass; the `tokens.md` values (medium 20px, large 24px) are
**web/non-Apple fallbacks**. The pill (`9999px`) for capsule controls is
fine to keep as the `DefaultGlassEffectShape` analogue.

## Scroll edge effect

```swift
func scrollEdgeEffectStyle(_ style: ScrollEdgeEffectStyle?, for edge: Edge.Set) -> some View
```

- `ScrollEdgeEffectStyle.soft` — gentler / more elastic fade.
- `ScrollEdgeEffectStyle.hard` — firmer / snappier edge.
- `for:` selects the edge (top / bottom / leading / trailing).

```swift
ScrollView { /* … */ }
    .scrollEdgeEffectStyle(.soft, for: .top)
```

Apple publishes **no** numeric blur / opacity / physics values. The
repo's `scrollEdgeEffect.soft` / `.hard` numbers are web approximations,
and its `directions` array corresponds to the API's `for:` edge.

## Token → API mapping

`materials.json` numbers are **web approximations**; the API column is
the native equivalent (which has no tunable numbers).

| Web token (`materials.json`) | SwiftUI API call | Web/CSS approximation |
|---|---|---|
| `liquidGlass.regular.large` (frost 14) | `glassEffect(.regular, in: <Shape r:24>)` | `backdrop-filter: blur(14px)`; `border-radius: 24px` |
| `liquidGlass.regular.medium` (frost 12) | `glassEffect(.regular, in: <Shape r:20>)` | `backdrop-filter: blur(12px)`; `border-radius: 20px` |
| `liquidGlass.regular.small` (frost 7) | `glassEffect(.regular, in: Capsule())` | `backdrop-filter: blur(7px)`; `border-radius: 9999px` |
| `liquidGlass.clear.{light,dark}` (frost 5) | `glassEffect(.clear, in: <Shape>)` | `backdrop-filter: blur(5px)` over media, + scrim if needed |
| `liquidGlass.regular.*.dark.tint` (#ffffff a:0.06) | `.regular.tint(...)` | low-alpha accent overlay on the surface |
| *(no token — doc only)* | `.regular.interactive()` | press scale ≈ 0.96 + brief specular highlight *(non-Apple)* |
| *(no token — doc only)* | `glassEffect(isEnabled ? .regular : .identity)` | conditionally drop `backdrop-filter` without reflow |
| *(no token — doc only)* | `GlassEffectContainer` + `glassEffectID` / `glassEffectUnion` | qualitative merge; no CSS equivalent |
| `scrollEdgeEffect.soft` | `scrollEdgeEffectStyle(.soft, for: edge)` | gradient mask fade, blur ≈ 10px |
| `scrollEdgeEffect.hard` | `scrollEdgeEffectStyle(.hard, for: edge)` | firmer gradient mask, blur ≈ 60px |
| `backgroundMaterials.*` | UIKit `Material` stack (`.regular`, `.thin`, …) | classic blur materials — **not** Liquid Glass |

The `in:` shape's corner radius drives `border-radius`; `frostRadius`
maps to `backdrop-filter: blur(...)`; `tint` maps to a low-alpha accent
overlay.

## Placement (HIG)

Liquid Glass is a **distinct floating functional layer above content**:

- **Use for** navigation and controls — toolbars, tab bars, floating
  controls, sheet chrome, chips. Use sparingly.
- **Avoid** content backgrounds, large areas, and stacking glass on
  glass (see `glass-legibility.md` for the legibility consequences).
