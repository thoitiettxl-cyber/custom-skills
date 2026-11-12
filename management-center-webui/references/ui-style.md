# UI/UX style guide — Management Center look, extracted from source

Source: `router-for-me/Cli-Proxy-API-Management-Center`, pinned commit
`64b4f5aed19b8f791eb21eb9e785ea379ea05b44` (2026-10-26), MIT, Copyright (c)
2026 Router-For.ME. All paths below are relative to that repo. This guide
re-expresses the style; short identifiers and values are quoted for
interoperability, per `references/PROVENANCE.md`. Functions, routes and
page behaviour belong to `SKILL.md` and `references/api-contract.md`, not here.

## How to read this guide

- Every value traces to a file:line at the pinned commit. A value with no
  source line is marked **NOT FOUND** or **[NEEDS-MEASUREMENT]** — do not
  treat it as source fact.
- "Light" is the `:root` block in `src/styles/themes.scss:6`. There is no
  `[data-theme='light']` block. "White" is `[data-theme='white']`
  (`themes.scss:96`), "Dark" is `[data-theme='dark']` (`themes.scss:166`).
  Auto is resolved in JS, never a CSS block (see §11).
- The source has two token systems that look alike but are separate:
  CSS custom properties (`--bg-primary`, …) in `themes.scss`, and SCSS
  compile-time variables (`$spacing-lg`, `$radius-md`, …) in
  `src/styles/variables.scss`. Do not assume they stay in sync; `--radius-md`
  and `$radius-md` happen to both be `8px`.
- Skeletons in this guide are framework-agnostic HTML + CSS. They use the
  source's global class names (`.btn`, `.card`, `.input`, … from
  `src/styles/components.scss`) where those exist. Classes from
  `*.module.scss` files are CSS-Modules in the source (hashed at build);
  skeletons for those components use plain class names with the same
  geometry and say so. A skeleton is a reproduction aid, not a claim that
  the source ships that exact markup.
- No browser run was made for this guide. Rendered sizes that JS measures
  at runtime, and any visual impression, are flagged, not asserted.

## 1. Design tokens — ready to copy

### 1.1 Theme blocks (copy verbatim)

Light = `:root`. White and dark redefine the same token set; values that
match light are repeated in the source blocks, not inherited, except for
the glass, motion and viz tokens in §1.2, which white and dark inherit
from `:root` — dark redefines only `--glass-border` and
`--viz-success`/`--viz-failure`, and white redefines no glass, motion or
viz token.

```css
:root {
  --bg-secondary: #faf9f5;
  --bg-primary: #f0eee8;
  --bg-tertiary: #e9e6df;
  --bg-hover: var(--bg-tertiary);
  --bg-quinary: #f6f4ee; /* defined in all 3 themes, never used in src/ — omit unless needed */
  --bg-error-light: rgba(198, 87, 70, 0.1);
  --floating-surface: #fffdf9;
  --floating-shadow: 0 12px 26px rgba(0, 0, 0, 0.14);
  --text-primary: #2d2a26;
  --text-secondary: #6d6760;
  --text-tertiary: #a29c95;
  --text-quaternary: #c0bab3;
  --text-muted: var(--text-tertiary); /* 1 use in src/ */
  --border-color: #e3e1db;
  --border-secondary: var(--border-color); /* 1 use in src/ */
  --border-primary: #d5d2cb;
  --border-hover: #cecac4;
  --primary-color: #8b8680;
  --primary-hover: #7f7a74;
  --primary-active: #726d67;
  --primary-contrast: #ffffff;
  --success-color: #10b981;
  --quota-medium-color: #e0aa14;
  --warning-color: #c65746;
  --error-color: #c65746;
  --danger-color: var(--error-color);
  --info-color: var(--primary-color);
  --warning-bg: rgba(198, 87, 70, 0.12);
  --warning-border: rgba(198, 87, 70, 0.35);
  --warning-text: var(--warning-color);
  --success-badge-bg: #d1fae5;
  --success-badge-text: #065f46;
  --success-badge-border: #6ee7b7;
  --failure-badge-bg: rgba(198, 87, 70, 0.14);
  --failure-badge-text: #8a3a30;
  --failure-badge-border: rgba(198, 87, 70, 0.35);
  --count-badge-bg: rgba(139, 134, 128, 0.18);
  --count-badge-text: var(--primary-active);
  --shadow: 0 1px 2px 0 rgb(0 0 0 / 0.08);
  --shadow-lg: 0 10px 18px -3px rgb(0 0 0 / 0.1);
  --radius-md: 8px;
  --primary-8: color-mix(in srgb, var(--primary-color) 8%, transparent);
  --primary-10: color-mix(in srgb, var(--primary-color) 10%, transparent);
  --primary-30: color-mix(in srgb, var(--primary-color) 30%, transparent);
  --amber-color: #d97706;
  --amber-text: #92400e;
  --amber-10: color-mix(in srgb, var(--amber-color) 10%, transparent);
  --amber-30: color-mix(in srgb, var(--amber-color) 30%, transparent);
  --destructive-color: var(--error-color);
  --destructive-10: color-mix(in srgb, var(--destructive-color) 10%, transparent);
  --destructive-30: color-mix(in srgb, var(--destructive-color) 30%, transparent);
  --muted-bg: var(--bg-tertiary);
  --muted-foreground: var(--text-secondary);
  --accent-bg: var(--bg-tertiary);
  --viz-success: #10b981;
  --viz-failure: #c65746;
  /* Glass + motion: defined once here, inherited by white/dark (§1.2). */
  --glass-blur: 12px;
  --glass-backdrop-filter: blur(var(--glass-blur));
  --glass-filter: blur(var(--glass-blur));
  --glass-bg: color-mix(in srgb, var(--bg-primary) 82%, transparent);
  --glass-bg-secondary: color-mix(in srgb, var(--bg-secondary) 82%, transparent); /* never used in src/ */
  --glass-border: color-mix(in srgb, var(--border-color) 60%, transparent);
  --ease-out-strong: cubic-bezier(0.23, 1, 0.32, 1);
  --dur-press: 160ms;
  --dur-hover: 200ms;
}

[data-theme='white'] {
  --bg-secondary: #ffffff;
  --bg-primary: #ffffff;
  --bg-tertiary: #f6f6f6;
  --bg-hover: var(--bg-tertiary);
  --bg-quinary: #ffffff;
  --bg-error-light: rgba(198, 87, 70, 0.08);
  --floating-surface: #ffffff;
  --floating-shadow: 0 12px 26px rgba(0, 0, 0, 0.12);
  --text-primary: #2d2a26;
  --text-secondary: #6d6760;
  --text-tertiary: #a29c95;
  --text-quaternary: #c0bab3;
  --text-muted: var(--text-tertiary);
  --border-color: #e5e5e5;
  --border-secondary: var(--border-color);
  --border-primary: #d9d9d9;
  --border-hover: #cccccc;
  --primary-color: #8b8680;
  --primary-hover: #7f7a74;
  --primary-active: #726d67;
  --primary-contrast: #ffffff;
  --success-color: #10b981;
  --quota-medium-color: #e0aa14;
  --warning-color: #c65746;
  --error-color: #c65746;
  --danger-color: var(--error-color);
  --info-color: var(--primary-color);
  --warning-bg: rgba(198, 87, 70, 0.12);
  --warning-border: rgba(198, 87, 70, 0.35);
  --warning-text: var(--warning-color);
  --success-badge-bg: #d1fae5;
  --success-badge-text: #065f46;
  --success-badge-border: #6ee7b7;
  --failure-badge-bg: rgba(198, 87, 70, 0.14);
  --failure-badge-text: #8a3a30;
  --failure-badge-border: rgba(198, 87, 70, 0.35);
  --count-badge-bg: rgba(139, 134, 128, 0.18);
  --count-badge-text: var(--primary-active);
  --shadow: 0 1px 2px 0 rgb(0 0 0 / 0.08);
  --shadow-lg: 0 10px 18px -3px rgb(0 0 0 / 0.1);
  --radius-md: 8px;
  --primary-8: color-mix(in srgb, var(--primary-color) 8%, transparent);
  --primary-10: color-mix(in srgb, var(--primary-color) 10%, transparent);
  --primary-30: color-mix(in srgb, var(--primary-color) 30%, transparent);
  --amber-color: #d97706;
  --amber-text: #92400e;
  --amber-10: color-mix(in srgb, var(--amber-color) 10%, transparent);
  --amber-30: color-mix(in srgb, var(--amber-color) 30%, transparent);
  --destructive-color: var(--error-color);
  --destructive-10: color-mix(in srgb, var(--destructive-color) 10%, transparent);
  --destructive-30: color-mix(in srgb, var(--destructive-color) 30%, transparent);
  --muted-bg: var(--bg-tertiary);
  --muted-foreground: var(--text-secondary);
  --accent-bg: var(--bg-tertiary);
  /* --viz-success / --viz-failure not redefined: inherit :root. */
}

[data-theme='dark'] {
  --bg-secondary: #151412;
  --bg-primary: #1d1b18;
  --bg-tertiary: #262320;
  --bg-hover: #2e2a26;
  --bg-quinary: #191714;
  --bg-error-light: rgba(198, 87, 70, 0.18);
  --floating-surface: #2a2723;
  --floating-shadow: 0 14px 30px rgba(0, 0, 0, 0.4);
  --text-primary: #f6f4f1;
  --text-secondary: #c9c3bb;
  --text-tertiary: #9c958d;
  --text-quaternary: #6f6962;
  --text-muted: var(--text-tertiary);
  --border-color: #3a3530;
  --border-secondary: var(--border-color);
  --border-primary: #4a453f;
  --border-hover: #5a544d;
  --primary-color: #8b8680;
  --primary-hover: #9a948e;
  --primary-active: #a6a099;
  --primary-contrast: #ffffff;
  --success-color: #10b981;
  --quota-medium-color: #ffd862;
  --warning-color: #c65746;
  --error-color: #c65746;
  --danger-color: var(--error-color);
  --info-color: var(--primary-color);
  --warning-bg: rgba(198, 87, 70, 0.22);
  --warning-border: rgba(198, 87, 70, 0.45);
  --warning-text: #f1b0a6;
  --success-badge-bg: rgba(6, 78, 59, 0.3);
  --success-badge-text: #6ee7b7;
  --success-badge-border: #059669;
  --failure-badge-bg: rgba(198, 87, 70, 0.24);
  --failure-badge-text: #f1b0a6;
  --failure-badge-border: rgba(198, 87, 70, 0.5);
  --count-badge-bg: rgba(139, 134, 128, 0.28);
  --count-badge-text: var(--primary-active);
  --shadow: 0 1px 3px 0 rgb(0 0 0 / 0.3);
  --shadow-lg: 0 10px 15px -3px rgb(0 0 0 / 0.3);
  --radius-md: 8px;
  --primary-8: color-mix(in srgb, var(--primary-color) 8%, transparent);
  --primary-10: color-mix(in srgb, var(--primary-color) 10%, transparent);
  --primary-30: color-mix(in srgb, var(--primary-color) 30%, transparent);
  --amber-color: #f59e0b;
  --amber-text: #fcd34d;
  --amber-10: color-mix(in srgb, var(--amber-color) 14%, transparent);
  --amber-30: color-mix(in srgb, var(--amber-color) 38%, transparent);
  --destructive-color: var(--error-color);
  --destructive-10: color-mix(in srgb, var(--destructive-color) 14%, transparent);
  --destructive-30: color-mix(in srgb, var(--destructive-color) 38%, transparent);
  --muted-bg: var(--bg-tertiary);
  --muted-foreground: var(--text-secondary);
  --accent-bg: var(--bg-tertiary);
  --viz-success: #0fae78;
  --viz-failure: #cf4b3a;
  --glass-border: color-mix(in srgb, var(--border-color) 55%, transparent);
}
```

Token lines: `src/styles/themes.scss:6-92` (`:root`), `:96-164` (white),
`:166-241` (dark). Light vs white differ **only** in backgrounds, borders,
`--bg-error-light` alpha (0.10 vs 0.08) and `--floating-shadow` alpha
(0.14 vs 0.12); text, primary and badge colours are identical.

### 1.2 Glass override — blur off on small screens and reduced motion

```css
@media (max-width: 768px), (prefers-reduced-motion: reduce), (prefers-reduced-transparency: reduce) {
  :root {
    --glass-backdrop-filter: none;
    --glass-filter: none;
    --glass-bg: var(--bg-primary);
    --glass-bg-secondary: var(--bg-secondary);
    --glass-border: var(--border-color);
  }
}
```

(`themes.scss:243-252`.) Glass surfaces fall back to solid theme
backgrounds; the floating header pills and the §6 gradient lose their blur.

### 1.3 Reading the palette

- Primary is a warm grey, `#8b8680`, in **all three themes**
  (`themes.scss:28,117,188`). It lightens on hover/active in dark only
  (`#9a948e` / `#a6a099`); in light/white it darkens (`#7f7a74` /
  `#726d67`). There is no saturated brand colour.
- `--warning-color` and `--error-color` are the **same red** `#c65746` in
  all themes. There is no yellow warning hue; the yellow family is amber
  (`--amber-color` `#d97706` light/white, `#f59e0b` dark). Do not invent
  a yellow warning state.
- `--info-color` is an alias of `--primary-color` in all themes. There is
  no separate blue info colour.
- Dark viz colours are stepped down (`--viz-success #0fae78`,
  `--viz-failure #cf4b3a`, `themes.scss:239-240`); a source comment cites
  an OKLCH brightness range and colour-blind separation. That is a comment
  claim, not a measurement made for this guide (§13.4).
- Defined but unused in `src/` (grep-proven: `$gray-400`/`$shadow-md` in
  `variables.scss`, `--bg-quinary`/`--glass-bg-secondary` in `themes.scss`). Omit them
  in a port unless a component actually needs them.

### 1.4 SCSS-only scale (compile-time — translate, do not copy as CSS vars)

`src/styles/variables.scss:6-44`. In plain-CSS skeletons below, these
appear as literal values.

| Scale | Values |
| --- | --- |
| Spacing | `4px, 8px, 16px, 24px, 32px, 48px` (`$spacing-xs/sm/md/lg/xl/2xl`, `:15-20`) |
| Radii | `4px, 8px, 12px, 9999px` (`$radius-sm/md/lg/full`, `:23-26`) |
| Shadows (SCSS) | `$shadow-sm: 0 1px 2px 0 rgb(0 0 0 / 0.05)`; `$shadow-md: 0 4px 6px -1px rgb(0 0 0 / 0.1)` (unused); `$shadow-lg: 0 10px 15px -3px rgb(0 0 0 / 0.1)` (`:29-31`). Prefer the `--shadow` / `--shadow-lg` CSS vars in §1.1, which are theme-aware — except modals, which use the fixed SCSS `$shadow-lg` (§7.6). |
| Transitions (SCSS) | `$transition-fast: 150ms ease`; `$transition-normal: 300ms ease` (`:34-35`). Prefer the motion tokens in §9 for interaction feedback. |
| Breakpoints | `$breakpoint-mobile: 768px`; `$breakpoint-tablet: 1024px` (`:38-39`) |
| Z-index scale | `$z-dropdown: 1000`; `$z-modal: 2000`; `$z-notification: 3000` (`:42-44`). Actual stacking values in §3.3. |
| Colours (SCSS mirrors) | `$primary-color #8b8680`, `$success-color #10b981`, `$warning-color #c65746`, `$error-color #c65746` (`:6-9`) |

## 2. Typography — there is no type scale

No font-size, font-weight, heading or letter-spacing scale exists in
`variables.scss`, `themes.scss`, `global.scss`, `mixins.scss` or
`reset.scss`. Sizes below are per-component declarations found in the
component and layout styles — a record of what is set, not a scale. Do
not extrapolate a scale from them, and do not claim a heading hierarchy
the source does not define.

### 2.1 Base

```css
body {
  font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', 'Roboto', 'Oxygen',
    'Ubuntu', 'Cantarell', 'Fira Sans', 'Droid Sans', 'Helvetica Neue', sans-serif;
  line-height: 1.5;
  -webkit-font-smoothing: antialiased;
  -moz-osx-font-smoothing: grayscale;
  background-color: var(--bg-secondary);
  color: var(--text-primary);
  transition: background-color 300ms ease, color 300ms ease; /* theme switch */
}
button, input, textarea, select { font: inherit; }
```

Stacks: `$font-family` (`variables.scss:47-49`), `$font-mono`
`ui-monospace, 'SF Mono', 'Cascadia Mono', 'JetBrains Mono', 'Fira Code',
Menlo, Consolas, 'Liberation Mono', monospace` (`variables.scss:51-53`).
Body defaults: `reset.scss:20-26,33-36`; body colours/transition:
`global.scss:13-19`. `$font-family` is used only by the body rule; all
other type inherits from it. No webfont is loaded; no `color-scheme`
property is set anywhere in `styles/` or `stores/`.

### 2.2 Sizes actually declared (per component, not a scale)

| Where | Size / weight |
| --- | --- |
| Card title, modal title | `18px / 700` (`components.scss:131,355`) |
| Sheet title | `18px / 600`; sheet eyebrow `11px / 500`, uppercase, `letter-spacing: 0.05em`; sheet description `13px`, `line-height: 1.5` (`Sheet.module.scss:95`) |
| Sidebar nav item | `13px / 600`; sub-item `12.5px / 600`, `min-height: 30px` (`layout.scss:573-588,705-712`) |
| Sidebar group label | `10px / 700`, `letter-spacing: 0.08em`, uppercase (`layout.scss:531-539`) |
| Brand title / subtitle | `15px / 800`; subtitle `10.5px / 500`, `line-height: 1.15` (`layout.scss:492-507`) |
| Nav badge | `10.5px / 700` expanded; `9px` rail (`layout.scss:657-669,438-448`) |
| Status badge / table body | `13px`; pill `12px`; table header `12px / 500` (`components.scss:152,190`; `Table.module.scss:15,23`) |
| Select trigger | `13px / 500`; small `12px`; placeholder `var(--text-tertiary)` (`Select.module.scss:13,52,65`) |
| Button small | `14px` (default `.btn` size is inherited, not declared) (`components.scss:65`) |
| Form label | `600`; hint `13px`, `var(--text-secondary)` (`components.scss:106`) |
| Checkbox label | `14px / 500`; toggle label `600` (`SelectionCheckbox.module.scss:83`; `ToggleSwitch.module.scss:65`) |
| Collapsible summary | `13px / 500`; hint `12px / 400` (`Collapsible.module.scss:11,46`) |
| Toast message | `0.875rem / 500`, `line-height: 1.5` (`NotificationContainer.module.scss:90`) |
| Tooltip (rail) | label `13px / 650`; meta `11.5px` at 60% opacity (`layout.scss:731-780`) |
| Empty-state title | `700` (size inherited); description `margin-top: 4px` (`components.scss:437`) |
| Log controls | `13px / 500` (`LogsPage.module.scss:117`) |

Truncation mixins (`mixins.scss:20-30`): `text-ellipsis` (single line) and
`text-ellipsis-multiline($lines: 2)` (line-clamp); 30 references in `src/`.

## 3. Spacing, radii, shadows, borders, z-index

### 3.1 Spacing

Use the §1.4 scale. The most-used steps by grep are `8px` and `16px`;
`24px` is the content gap (`.main-content gap: 24px`, `layout.scss:813`)
and the card padding. Content side padding is fluid, not a spacing step:
`clamp(20px, 3vw, 48px)` (§4).

### 3.2 Radii

`4px` (small), `8px` (default — controls, cards' inner elements, modal on
mobile), `12px` (cards, modals, sheets' dropdowns, toasts, empty states),
`9999px` (pills, badges, toggles, checkbox-adjacent circles). Exceptions
traced to source: nav item `9px`, sub-item `8px`, header pill `16px`
(desktop) / `14px` (mobile), floating buttons `11px`, sidebar logo `7px`,
checkbox box `7px`, toast close `8px`. Use the exception only in its own
component; do not generalise it.

### 3.3 Shadows and z-index

Shadows: use `--shadow` (cards, Select trigger) and `--shadow-lg`
(dropdowns, toasts) from §1.1. Modals are the exception: they use the
SCSS `$shadow-lg`, a fixed value, not the theme-aware CSS var (§7.6). Component-local shadows traced to
source: header pill `0 18px 44px rgb(0 0 0 / 0.17), inset 0 1px 0
rgb(255 255 255 / 0.04)`; popovers `0 20px 48px rgb(0 0 0 / 0.22)`; sheet
panel `-8px 0 32px rgba(0,0,0,0.16)` plus `var(--floating-shadow)`.

Z-index, lowest to highest (numbers as declared; relative order of
Select dropdown vs Sheet vs Modal was **not** verified beyond the numbers):

| Layer | z-index |
| --- | --- |
| `.top-gradient-blur` | `998` (`layout.scss:48`) |
| Sidebar / mobile backdrop | `999` (`layout.scss:397,925`); mobile fixed sidebar `1000` (`:933`) |
| `.main-header` | `1001` (`layout.scss:84`) |
| Rail tooltip, language/theme popovers | `1002` (`layout.scss:733,218`) |
| Log follow button | `2` (inside its own stacking context, `LogsPage.module.scss:338`) |
| Logs fullscreen card | `$z-modal - 1` = `1999` (`LogsPage.module.scss:571`) |
| Modal overlay / Sheet overlay | `2000` (`$z-modal`; `components.scss:225`, `Sheet.module.scss:4`) |
| Select / Autocomplete dropdown | `2010`, hard-coded in TS (`Select.tsx:37-40`, `AutocompleteInput.tsx:86-110`) |
| Notifications | `3000` (`$z-notification`; `NotificationContainer.module.scss:1`) |

### 3.4 Borders and reset

Default chrome: `1px solid var(--border-color)`. Sidebar header bottom
border, modal/sheet header/footer borders, table row borders and card
borders all use it. The shell uses translucent mixes of the border token
for the sidebar edge and header pill; skeletons below use the plain token
— the exact mix percentages in the shell are layout-chrome detail, not a
component rule.

Reset (`reset.scss:7-49`): `box-sizing: border-box`, zero margin/padding
on all elements; `html, body, #root` at `100%` height/width; links inherit
colour with no underline; lists unstyled. Scrollbar (`global.scss:30-44`):
`8px`, track `var(--bg-secondary)`, thumb `var(--border-color)` with
`9999px` radius, hover `var(--border-hover)`. Modal-open scroll lock:
`html.modal-open, body.modal-open { overflow: hidden }`
(`global.scss:20-27`).

## 4. Layout grid and breakpoints — flex shell, no grid, no max-width

### 4.1 Breakpoints

| Breakpoint | Rule |
| --- | --- |
| Mobile | `@media (max-width: 768px)` — `$breakpoint-mobile` (`variables.scss:38`, `mixins.scss:8-12`). The whole mobile block is `layout.scss:840-1018`. |
| Tablet | `@mixin tablet { @media (min-width: 769px) and (max-width: 1024px) }` (`mixins.scss:14-18`) — **defined but unused in `layout.scss`**; 769–1024px uses the desktop shell. Do not invent tablet-specific shell rules. |
| Desktop | No desktop mixin or breakpoint; above 1024px is the unlabelled default. |
| `100dvh` | `@supports (height: 100dvh)` — `.main-body`, `.sidebar`, `.content` use `100dvh` where supported, else `100vh` (`layout.scss:372-379,417-419,792-794`). |

### 4.2 Shell structure

No CSS grid is used for the shell; it is flexbox throughout. There is no
content `max-width`: content is fluid (`flex: 1`, `min-width: 0`) with
side padding `clamp(20px, 3vw, 48px)`.

DOM order (`MainLayout.tsx:973-985,1138-1151`):

```
div.app-shell[.sidebar-is-collapsed][.plugin-resource-shell]
  div.top-gradient-blur (aria-hidden)
  header.main-header
    button.sidebar-toggle-floating
    div.mobile-sidebar-actions > button.mobile-menu-btn
    div.header-actions.floating-actions (refresh, language, theme, logout)
  div.main-body
    button.sidebar-backdrop[.visible]
    aside.sidebar[.open][.collapsed]
      div.sidebar-header > div.sidebar-brand (logo + brand text)
      div.nav-section > div.nav-group* (label + items / drawers)
    div.nav-tooltip (only when a rail tooltip is shown)
    div.content[.content-logs][.content-plugin-resource] > main.main-content > PageTransition
```

Mechanics (`layout.scss:13-36,361-371,783-836`):

- `.app-shell`: column flex, `min-height: 100vh`, `height: 100vh`,
  `overflow: hidden`, `background: var(--bg-secondary)`. On mobile:
  `height: auto`, `overflow: visible`, page scrolls.
- `.main-body`: row flex, `flex: 1`, `min-height: 0`, `height: 100vh`,
  `overflow: hidden`. On mobile: `height: auto`, `min-height: 100vh`.
- `.content` is the desktop scroll container: `flex: 1`, column flex,
  `min-width: 0`, `height: 100vh`, `overflow-y: auto`,
  `scrollbar-gutter: stable`. Logs and plugin-resource variants override
  to `overflow: hidden`.
- `.main-content`: `flex: 1 0 auto`, `min-height: 100%`,
  `padding: 70px clamp(20px, 3vw, 48px) 40px`, column flex, `gap: 24px`,
  `overflow-x: hidden`. Logs variant: bottom padding `24px`,
  `overflow: hidden`. Plugin-resource variant: `padding: 0`, `gap: 0`.
- The desktop top padding is a fixed `70px`, **not** `var(--header-height)`
  (80px): the header is fixed and pointer-transparent except for its
  pills, so content starts 10px under the nominal header height and slides
  under the §6 gradient. Whether that overlap is intentional is
  [NEEDS-MEASUREMENT] — no comment in `layout.scss` states it for
  `.main-content`; the gradient exists to fade content under the header.
  On mobile the padding becomes header-height-relative:
  `calc(var(--header-height) + 16px) 16px 24px`.
- `--content-center-x`: JS writes the horizontal centre of `.content`
  (from `getBoundingClientRect`) to `documentElement` for bottom overlays
  (`MainLayout.tsx:418-447`). No consumer was found in the shell files
  read — do not invent one.
- `.plugin-resource-shell .top-gradient-blur { display: none }`
  (`layout.scss:39-43`).

### 4.3 Shell skeleton

```html
<div class="app-shell">
  <div class="top-gradient-blur" aria-hidden="true"></div>
  <header class="main-header">
    <button class="sidebar-toggle-floating" type="button" aria-label="Toggle sidebar">‹</button>
    <div class="mobile-sidebar-actions"><button class="mobile-menu-btn" type="button" aria-label="Open menu">☰</button></div>
    <div class="header-actions floating-actions">
      <button type="button" aria-label="Refresh">↻</button>
      <button type="button" aria-haspopup="menu" aria-expanded="false" aria-label="Language">A</button>
      <button type="button" aria-haspopup="menu" aria-expanded="false" aria-label="Theme">◐</button>
      <button type="button" aria-label="Log out">→</button>
    </div>
  </header>
  <div class="main-body">
    <button class="sidebar-backdrop" type="button" aria-label="Close sidebar"></button>
    <aside class="sidebar"><nav><!-- groups, §5 --></nav></aside>
    <div class="content"><main class="main-content"><!-- pages --></main></div>
  </div>
</div>
```

```css
.app-shell { display: flex; flex-direction: column; min-height: 100vh; height: 100vh; overflow: hidden; background: var(--bg-secondary); }
.main-body { display: flex; flex: 1; min-height: 0; height: 100vh; overflow: hidden; }
.content { flex: 1; display: flex; flex-direction: column; min-width: 0; height: 100vh; overflow-y: auto; scrollbar-gutter: stable; }
.main-content { flex: 1 0 auto; min-height: 100%; padding: 70px clamp(20px, 3vw, 48px) 40px; display: flex; flex-direction: column; gap: 24px; overflow-x: hidden; }
@media (max-width: 768px) {
  .app-shell { height: auto; overflow: visible; overflow-y: auto; }
  .main-body { height: auto; min-height: 100vh; overflow: visible; }
  .content { height: auto; overflow: visible; overflow-y: auto; }
  .main-content { padding: calc(var(--header-height, 74px) + 16px) 16px 24px; }
}
```

## 5. Sidebar drawer and floating top bar

### 5.1 Shell tokens (initial CSS values; JS overwrites `--header-height`)

```css
:root {
  --header-height: 80px;
  --shell-gutter: 24px;
  --sidebar-panel-width: 216px;
  --sidebar-collapsed-width: 60px;
  --sidebar-active-width: var(--sidebar-panel-width);
  --sidebar-gap: 0px;
  --floating-control-size: 38px;
}
@media (max-width: 768px) {
  :root {
    --header-height: 74px;
    --shell-gutter: 12px;
    --sidebar-panel-width: min(280px, calc(100vw - 24px));
    --floating-control-size: 36px;
  }
}
```

(`layout.scss:4-11,841-846`.) At runtime a `ResizeObserver` on the header
measures its real `offsetHeight` and writes `--header-height` to
`documentElement` (`MainLayout.tsx:358-384`); the CSS values are the
initial/fallback values. The exact rendered height is [NEEDS-MEASUREMENT].

### 5.2 Sidebar — desktop

`layout.scss:395-423`: `width: var(--sidebar-panel-width)`,
`height: 100vh`, `padding: 14px 10px`, column flex, `gap: 8px`,
`flex-shrink: 0`, `overflow-y: auto`, `background: var(--bg-primary)`,
right border, scrollbar hidden (`scrollbar-width: none`, webkit scrollbar
`display: none`); transitions on `width`/`transform`/`padding`, 300ms.

- Sidebar header: `min-height: 36px`, `padding: 2px 2px 10px`,
  `margin-bottom: 2px`, bottom border (`:461-468`).
- Brand logo `30px × 30px`, radius `7px`; brand title/subtitle per §2.2.
- Nav section: column flex, `gap: 10px`, `flex: 1`; groups `gap: 4px`;
  group labels per §2.2 (`:510-539`).
- Nav item: `padding: 6px 10px`, radius `9px`, `13px/600`, `gap: 10px`;
  icon box `18px × 18px`, inner icon `16px` (`layout.scss:619-642`). Hover shifts
  `translateX(1px)`; active uses a stronger background/border and the
  icon takes `var(--primary-active)` (`:677-703`).
- Sub-item: `min-height: 30px`, `padding: 5px 10px`, radius `8px`,
  `12.5px/600` (`:705-712`).
- Plugin drawers: column, `gap: 4px`; full-width toggle button; caret
  rotates 180° when open; sub-list `margin-left: 18px`, `padding-left: 10px`,
  1px left border (`:542-571`).

Collapsed rail (`layout.scss:424-458`): width `60px`, padding `14px 8px`,
centred brand/items, items `padding: 10px`; group labels hidden, replaced
by 24px divider lines (`height: 1px`, `width: 24px`, `margin: 4px auto`);
drawer carets hidden; sub-lists lose indent/border; badge becomes the
absolute 15px dot-badge (§7.4). Toggle: the floating pill (§5.4) and
keyboard shortcut `Ctrl+B` / `⌘B` (`sidebarShortcut.ts:1-21`; ignored
when focus is in an input, textarea or content-editable element).

State model (`MainLayout.tsx:328-329,356`): `sidebarOpen` (default
`false`, mobile drawer), `sidebarCollapsed` (default `false`, desktop
rail). Labels render when `!sidebarCollapsed || sidebarOpen`.

### 5.3 Sidebar — mobile drawer (≤768px)

`layout.scss:931-971`: fixed, `top: 0; bottom: 0; left: 0`, `z-index: 1000`,
`transform: translateX(calc(-100% - 24px))`; `.open` sets
`translateX(0)` (300ms transition). Even with `.collapsed`, the mobile
drawer uses full panel width and left-aligned items/badges — collapse is
a desktop-only visual state.

Backdrop (`layout.scss:382-394,923-930`): a `<button>`, `display: none`
on desktop; on mobile `position: fixed; inset: 0; z-index: 999`,
`background: rgb(8 8 8 / 0.46)` with `blur(4px)` from the base rule,
150ms opacity transition; `.visible` sets `opacity: 1` and
`pointer-events: auto`. When open it is focusable (`tabIndex: 0`) and
`aria-hidden` when closed (`MainLayout.tsx:1143-1148`). Close triggers
found: backdrop click, any nav-link click, hamburger toggle. **No
Escape-to-close handler and no focus trap / focus return for the drawer
were found** in `MainLayout.tsx` — do not claim them; adding them is new
work, not reproduction.

Hamburger: `.mobile-sidebar-actions` is `display: none` on desktop and
`inline-flex` at the left gutter on mobile; the floating toggle pill is
hidden on mobile (`layout.scss:857-878`).

### 5.4 Floating top bar

The header itself is **not a bar**: `.main-header` is `position: fixed`,
`top/right/left: 0`, `height: var(--header-height)`,
`pointer-events: none`, transparent, no border (`layout.scss:82-91`).
Everything visible floats as separate pills; `pointer-events: auto` is
restored on the pills and the toggle (`:144-163`).

Left pill — sidebar toggle (`layout.scss:93-141`): `24px` wide × `52px`
tall, radius `14px`, at `left: calc(var(--sidebar-active-width) - 12px)`,
vertically centred. Hover nudges `translateX(2px)`; `:focus-visible`
gets a 2px primary ring plus shadow. Hidden on mobile.

Right pill — header actions (`layout.scss:144-196`): `position: absolute`,
`top: var(--shell-gutter)`, `right: var(--shell-gutter)`, `inline-flex`,
`gap: 4px`, `padding: 6px`, radius `16px`, translucent `var(--bg-primary)`
with backdrop blur (`--glass-blur: 16px` locally), shadow
`0 18px 44px rgb(0 0 0 / 0.17), inset 0 1px 0 rgb(255 255 255 / 0.04)`.
Buttons inside: `--floating-control-size` square (38px / 36px mobile),
radius `11px`, `padding: 0`, transparent, `color: var(--text-secondary)`,
hover background 8% text-primary mix, colour → `var(--text-primary)`.
Order: refresh-all, language menu, theme menu, logout. On mobile the pill
shrinks (padding `5px`, gap `2px`, radius `14px`) and gets
`max-width: calc(100vw - 2*gutter - control-size - 14px)` so the two
pills cannot overlap (`:861-870`).

Popovers (`layout.scss:216-340`): `position: absolute`,
`top: calc(100% + 12px)`, `right: 0`, `z-index: 1002`, glass background
(88% bg-primary), shadow `0 20px 48px rgb(0 0 0 / 0.22)`. Language options
are full-width rows (`8px 10px`, `14px/500`; active = primary colour,
`600`, ✓ at 13px). Theme popover is a row of preview cards (preview
`72px × 52px`, label `11px`; active = 2px primary border). On mobile the
theme popover becomes a 2-column grid
`width: min(188px, calc(100vw - 16px))` and the language popover anchors
to the left edge. Popovers close on outside pointer-down or Escape
(`MainLayout.tsx:105-136`).

Collapsed-rail tooltip (`layout.scss:731-780`, `MainLayout.tsx:93-94,
331-335,770-810,388-413,1179-1192`): desktop only, hidden on mobile.
Dark hard-coded card (`#24211c` / `#f6f4f1`, **not** theme tokens),
`left: calc(var(--sidebar-active-width) + 20px)`,
`max-width: min(320px, calc(100vw - var(--sidebar-active-width) - 32px))`,
padding `9px 12px`, radius `10px`; label `13px/650` with ellipsis, meta
`11.5px` at 60% opacity; enter animation from `opacity: 0`,
`translateX(-4px)`, 150ms. Vertical position is the hovered/focused
element's centre, clamped with an `8px` viewport margin in JS. Triggered
on mouse-enter and on focus; a focused item suppresses other items'
hover tooltips. Wiring: `role="tooltip"`, `id="sidebar-nav-tooltip"`,
items get `aria-label` (label + badge) and `aria-describedby` only while
shown for that item; drawer toggles get `aria-expanded`.

### 5.5 Sidebar skeleton

```html
<aside class="sidebar">
  <div class="sidebar-header">
    <div class="sidebar-brand"><span class="brand-logo"></span>
      <span class="brand-text"><span class="brand-title">Product</span>
      <span class="brand-subtitle">Management Center</span></span>
    </div>
  </div>
  <nav class="nav-section">
    <div class="nav-group">
      <div class="nav-group-label">Operate</div>
      <a class="nav-item is-active" href="#"><span class="nav-icon">▦</span><span class="nav-label">Dashboard</span></a>
      <a class="nav-item" href="#"><span class="nav-icon">▦</span><span class="nav-label">Quick Start</span><span class="nav-badge" aria-hidden="true">3</span></a>
    </div>
  </nav>
</aside>
```

```css
.sidebar { width: var(--sidebar-panel-width, 216px); height: 100vh; padding: 14px 10px; display: flex; flex-direction: column; gap: 8px; flex-shrink: 0; overflow-y: auto; background: var(--bg-primary); border-right: 1px solid var(--border-color); scrollbar-width: none; }
.sidebar::-webkit-scrollbar { display: none; }
.sidebar-header { min-height: 36px; padding: 2px 2px 10px; margin-bottom: 2px; border-bottom: 1px solid var(--border-color); }
.brand-logo { width: 30px; height: 30px; border-radius: 7px; }
.brand-title { font-size: 15px; font-weight: 800; line-height: 1.15; }
.brand-subtitle { font-size: 10.5px; font-weight: 500; line-height: 1.15; color: var(--text-secondary); }
.nav-group-label { font-size: 10px; font-weight: 700; letter-spacing: 0.08em; text-transform: uppercase; padding: 0 10px 2px; color: var(--text-tertiary); }
.nav-item { display: flex; align-items: center; gap: 10px; padding: 6px 10px; border-radius: 9px; font-size: 13px; font-weight: 600; color: var(--text-primary); }
.nav-icon { width: 18px; height: 18px; display: inline-flex; align-items: center; justify-content: center; }
.nav-badge { min-width: 18px; height: 18px; margin-left: auto; padding: 0 5px; display: inline-flex; align-items: center; justify-content: center; border-radius: 9999px; font-size: 10.5px; font-weight: 700; line-height: 1; background: color-mix(in srgb, var(--text-primary) 9%, transparent); color: var(--text-primary); }
.sidebar.collapsed { width: 60px; padding: 14px 8px; }
@media (max-width: 768px) {
  .sidebar { position: fixed; top: 0; bottom: 0; left: 0; z-index: 1000; width: min(280px, calc(100vw - 24px)); transform: translateX(calc(-100% - 24px)); transition: transform 300ms ease; }
  .sidebar.open { transform: translateX(0); }
  .sidebar-backdrop { position: fixed; inset: 0; z-index: 999; background: rgb(8 8 8 / 0.46); backdrop-filter: blur(4px); opacity: 0; pointer-events: none; transition: opacity 150ms ease; }
  .sidebar-backdrop.visible { opacity: 1; pointer-events: auto; }
}
```

## 6. The header background — there is no pixel pattern

**No literal pixel pattern exists in the shell.** No
`repeating-linear-gradient`, dot/checker/noise `background-image`, tiled
`background-size`, image asset or `<canvas>` exists in `src/styles/*.scss`,
`src/components/layout/`, `src/App.tsx` or `index.html` at the pinned
commit (negative grep for `pixel|dither|repeating-|background-size|dot|
checker|noise|canvas`; the only hit is `.nav-sub-dot`, a 6px nav dot).
If a dithered texture appears in a screenshot, it does not come from the
shell files read — page-level radial gradients in dashboard/quota modules
were out of scope and were not examined as header candidates, and a newer
build than the pin may differ. Do not invent a pixel texture.

What the visual actually is: a fixed, pointer-transparent overlay,
`.top-gradient-blur`, an empty `<div aria-hidden="true">` as the first
child of `.app-shell`, that fades the page background downward and blurs
whatever scrolls underneath, with a mask fading the blur itself out.
Exact declarations (`layout.scss:45-80`):

```css
.top-gradient-blur {
  position: fixed;
  top: 0; right: 0; left: var(--sidebar-active-width);
  z-index: 998;
  height: 141px; /* 114px on mobile */
  pointer-events: none;
  background: linear-gradient(180deg,
    color-mix(in srgb, var(--bg-secondary) 88%, #0d0c0a) 0%,
    color-mix(in srgb, var(--bg-secondary) 54%, transparent) 36%,
    color-mix(in srgb, var(--bg-secondary) 22%, transparent) 66%,
    transparent 100%);
  --glass-blur: 22px; /* overrides the 12px theme default, locally */
  backdrop-filter: var(--glass-backdrop-filter);
  -webkit-backdrop-filter: var(--glass-backdrop-filter);
  mask-image: linear-gradient(to bottom, #000 0%, rgb(0 0 0 / 0.9) 24%,
    rgb(0 0 0 / 0.58) 48%, rgb(0 0 0 / 0.22) 72%, transparent 100%);
  -webkit-mask-image: linear-gradient(to bottom, #000 0%, rgb(0 0 0 / 0.9) 24%,
    rgb(0 0 0 / 0.58) 48%, rgb(0 0 0 / 0.22) 72%, transparent 100%);
  transition: left 300ms ease;
}
```

Notes: the gradient starts at the sidebar edge, so it tracks
collapse/expand with the 300ms `left` transition, and at 141px it is
taller than the 80px header, so the fade extends below the floating
pills. The top stop mixes in a hard-coded near-black `#0d0c0a` in both
themes — how that reads in light/white themes is [NEEDS-MEASUREMENT]
(no browser run). On mobile / reduced-motion / reduced-transparency the
backdrop filter becomes `none` (§1.2) and only the gradient remains.
The shell background itself is flat: `.app-shell` and `body` use
`var(--bg-secondary)` with no texture (`layout.scss:13-25`,
`global.scss:13`).

## 7. Components and states

### 7.1 Buttons

`.btn` (`components.scss:4-74`): `inline-flex`, centred, `gap: 8px`,
`border: 1px solid transparent`, radius `8px`, padding `10px 14px`,
`font-weight: 600`, `cursor: pointer`, `transition: all 150ms ease`,
default background `var(--bg-secondary)`, colour `var(--text-primary)`.
Font size, height/min-height, `:active` and `:focus`/`:focus-visible`
are **NOT STATED** for `.btn` — rendered height is padding + line-height
only. Do not convert the padding to a height claim.

| Variant | Background / border / colour | Hover |
| --- | --- | --- |
| `.btn-primary` (`:18`) | `var(--primary-color)`, text `var(--primary-contrast, #fff)` | → `var(--primary-hover)` |
| `.btn-secondary` (`:29`) | `var(--bg-tertiary)`, border `var(--border-color)` | bg → `var(--bg-hover, var(--bg-tertiary))`, border → `var(--border-hover)` |
| `.btn-ghost` (`:40`) | transparent, `var(--text-secondary)` | colour → `var(--text-primary)`, bg → `var(--bg-tertiary)` |
| `.btn-danger` (`:51`) | `$error-color`, `#fff` text | bg darkened 5% lightness |
| `.btn-full` (`:61`) | `width: 100%` | — |
| `.btn-sm` (`:65`) | `padding: 8px 10px`, `font-size: 14px` | — |
| `:disabled` (`:70`) | `opacity: 0.6`, `cursor: not-allowed` (all variants) | — |

`Button` component (`Button.tsx:3-32`): variants
`primary | secondary | ghost | danger` (default `primary`), sizes `md | sm`
(default `md`), `fullWidth`, `loading` (spinner before children, button
disabled while loading). No `plain`/`header`/`icon` variant exists; the
header look is the §5.4 layout override, not a variant. Dark override
(`components.scss:76-85`): `[data-theme='dark'] .btn`, `.btn-secondary`,
`.btn-ghost` → `color: #fff`; no dark override for primary/danger.

```html
<button class="btn btn-primary" type="button"><span>Save</span></button>
<button class="btn btn-secondary btn-sm" type="button"><span>Cancel</span></button>
<button class="btn btn-danger" type="button" disabled><span>Delete</span></button>
```

```css
.btn { display: inline-flex; align-items: center; justify-content: center; gap: 8px; border: 1px solid transparent; border-radius: 8px; padding: 10px 14px; font-weight: 600; cursor: pointer; transition: all 150ms ease; background-color: var(--bg-secondary); color: var(--text-primary); }
.btn-primary { background-color: var(--primary-color); border-color: var(--primary-color); color: var(--primary-contrast, #fff); }
.btn-primary:hover { background-color: var(--primary-hover); border-color: var(--primary-hover); }
.btn-secondary { background-color: var(--bg-tertiary); border-color: var(--border-color); color: var(--text-primary); }
.btn-secondary:hover { background-color: var(--bg-hover, var(--bg-tertiary)); border-color: var(--border-hover); }
.btn-ghost { background: transparent; border-color: transparent; color: var(--text-secondary); }
.btn-ghost:hover { color: var(--text-primary); background-color: var(--bg-tertiary); }
.btn-danger { background-color: #c65746; border-color: #c65746; color: #fff; }
.btn-sm { padding: 8px 10px; font-size: 14px; }
.btn-full { width: 100%; }
.btn:disabled { opacity: 0.6; cursor: not-allowed; }
```

### 7.2 Cards and lists

`.card` (`components.scss:123-151`): `background: var(--bg-primary)`,
`border: 1px solid var(--border-color)`, radius `12px`,
`box-shadow: var(--shadow)`, `padding: 24px`. `.card-header`: flex,
`space-between`, `gap: 8px`, wrap, `margin-bottom: 16px`; title
`18px/700`, `flex: 1 1 auto`, `min-width: 0`. **No card variants, hover
or selected state is stated.** `Card` (`Card.tsx:3-19`): `title?`,
`extra?`, `className?`, children; the header renders only if
`title || extra`; no collapsible, loading or footer slot.

`.item-list`: column flex, `gap: 8px`. `.item-row`
(`components.scss:503-538`): border, radius `8px`, padding `16px`,
`background: var(--bg-primary)`, flex `space-between`, `gap: 16px`, wrap;
`.item-meta` column, `gap: 6px`; `.item-title` `700`;
`.item-subtitle` `var(--text-secondary)`, monospace stack,
`word-break: break-all`; `.item-actions` flex, `gap: 8px`. **No hover,
selected or disabled state is stated** for `.item-row`. `.stack`:
column flex, `gap: 24px` (`:547`).

```html
<div class="card">
  <div class="card-header"><div class="title">Usage</div><span>extra</span></div>
  <p>Card body.</p>
</div>
<div class="item-list">
  <div class="item-row">
    <div class="item-meta"><span class="item-title">Key name</span><span class="item-subtitle">sk-…</span></div>
    <div class="item-actions"><button class="btn btn-ghost btn-sm" type="button"><span>Edit</span></button></div>
  </div>
</div>
```

```css
.card { background-color: var(--bg-primary); border: 1px solid var(--border-color); border-radius: 12px; box-shadow: var(--shadow); padding: 24px; }
.card-header { display: flex; align-items: center; justify-content: space-between; gap: 8px; flex-wrap: wrap; margin-bottom: 16px; }
.card-header .title { flex: 1 1 auto; min-width: 0; font-size: 18px; font-weight: 700; color: var(--text-primary); }
.item-list { display: flex; flex-direction: column; gap: 8px; }
.item-row { border: 1px solid var(--border-color); border-radius: 8px; padding: 16px; background: var(--bg-primary); display: flex; align-items: center; justify-content: space-between; gap: 16px; flex-wrap: wrap; }
.item-title { font-weight: 700; color: var(--text-primary); }
.item-subtitle { color: var(--text-secondary); font-family: ui-monospace, SFMono-Regular, Menlo, Monaco, Consolas, 'Liberation Mono', 'Courier New', monospace; word-break: break-all; }
```

### 7.3 Badges and pills

`.status-badge` (`components.scss:152-189`): `inline-flex`, `gap: 6px`,
`padding: 4px 10px`, radius `9999px`, `font-size: 13px`,
`border: 1px solid var(--border-color)`, `margin-bottom: 16px`; the
following sibling is forced to `display: block`. Variants use the SCSS
colour tokens at 0.35 border / 0.08 background alpha: `.success`
(`$success-color`), `.warning` / `.error` (both `$warning-color` /
`$error-color`, the same red), `.muted` (`var(--text-secondary)` only).
**No `.info` variant exists** for `.status-badge`. Note: the theme badge
tokens in §1.1 (`--success-badge-*`, `--failure-badge-*`) are a separate
set; the `.status-badge` variants use the SCSS colours, not those vars.

`.pill` (`components.scss:190`): `padding: 4px 10px`, radius `9999px`,
`background: var(--bg-secondary)`, `color: var(--text-secondary)`,
`border: 1px solid var(--border-color)`, `font-size: 12px`. No variants
or states stated.

Nav badge — see §5.5 skeleton (expanded `18px`, rail `15px` absolute,
mobile drawer back to expanded sizing; sr-only label via
`.nav-badge-sr-only`, 1×1px clipped, `layout.scss:675`).

```html
<span class="status-badge success">Healthy</span>
<span class="status-badge error">Failed</span>
<span class="pill">v8</span>
```

```css
.status-badge { display: inline-flex; align-items: center; gap: 6px; padding: 4px 10px; border-radius: 9999px; font-size: 13px; border: 1px solid var(--border-color); margin-bottom: 16px; }
.status-badge.success { color: #10b981; border-color: rgba(16, 185, 129, 0.35); background: rgba(16, 185, 129, 0.08); }
.status-badge.warning, .status-badge.error { color: #c65746; border-color: rgba(198, 87, 70, 0.35); background: rgba(198, 87, 70, 0.08); }
.status-badge.muted { color: var(--text-secondary); }
.pill { padding: 4px 10px; border-radius: 9999px; background: var(--bg-secondary); color: var(--text-secondary); border: 1px solid var(--border-color); font-size: 12px; }
```

### 7.4 Inputs, selects, autocomplete

`.input` / `textarea` (`components.scss:87-105`): `width: 100%`,
`border: 1px solid var(--border-color)`, radius `8px`,
`padding: 10px 12px`, `background: var(--bg-secondary)`,
`color: var(--text-primary)`, transition on `border-color` + `box-shadow`
(150ms). `:focus`: `outline: none`, border → `var(--primary-color)`,
`box-shadow: 0 0 0 3px rgba(139,134,128,0.18)` — note `:focus`, not
`:focus-visible`: the ring shows on mouse focus too. Height and font-size
are **NOT STATED**. Disabled and error-border styling are **NOT STATED**:
errors are a separate `.error-box` below the input, never a red border.

`.form-group` (`:106`): column flex, `gap: 4px`, `margin-bottom: 16px`;
`label { font-weight: 600; color: var(--text-primary) }`;
`.hint { color: var(--text-secondary); font-size: 13px }`. `Input`
(`Input.tsx:3-45`): `label?`, `hint?`, `error?`, `rightElement?` (absolute,
`right: 8px`, vertically centred); generated id, `aria-invalid` when
error, `aria-describedby` joining error + hint ids; error text in
`.error-box`, no `aria-errormessage`.

Select (CSS-Modules in source; skeleton uses plain classes):
trigger (`Select.module.scss:13-69`): `inline-flex`, `space-between`,
`gap: 8px`, `width: 100%`, `height: 40px`, `padding: 0 12px`,
`border: 1px solid var(--border-color)`, radius `8px`,
`background: var(--bg-primary)`, `box-shadow: var(--shadow)`,
`font-size: 13px`, `font-weight: 500`, `appearance: none`. Hover: border
→ `var(--border-hover)`. Focus/open: `outline: none`, shadow ring
`0 0 0 3px rgba(139,134,128,0.18)`; open also sets border →
`var(--primary-color)`. Small: `height: 28px`, `padding: 0 10px`,
`font-size: 12px`, no shadow. Placeholder: `var(--text-tertiary)`.
Chevron: 14px, `var(--text-secondary)`, rotates 180° when open. Disabled
visual styling is **NOT STATED** — `disabled` only disables the button
and suppresses opening. Dropdown (`Select.module.scss:80`,
`Select.tsx:37-40`): fixed, portalled, viewport-clamped (8px margin, 6px
offset), flips up/down, `max-height: 240px`, `z-index: 2010`,
`background: var(--bg-primary)`, border, radius `12px`, `padding: 6px`,
`box-shadow: var(--shadow-lg)`, column, `gap: 4px`, `overflow-y: auto`.
Option: `padding: 8px 12px`, radius `8px`, `13px/500`, hover →
`var(--bg-secondary)`; active (selected) option: border
`rgba(139,134,128,0.5)`, background 10% primary, `600`; highlighted
(keyboard/hover): background `var(--bg-secondary)`. Keyboard:
ArrowUp/Down, Home/End, Enter/Space commit, Escape closes + refocuses
trigger, Tab closes (`Select.tsx:190-260`, `aria-activedescendant`,
`role="listbox"/"option"`).

Autocomplete (`AutocompleteInput.tsx`): reuses `.input` / `.form-group` /
`.error-box`; 16px chevron at `opacity: 0.5`, `right: 8px`; dropdown
portalled, `z-index: 2010`, `max-height: min(200px, space)`, flips up;
option rows `padding: 8px 12px`, highlighted → `var(--bg-tertiary)`,
value `500`, label `0.85em` + `var(--text-secondary)`; substring match,
case-insensitive; no "no results" row is rendered (dropdown shows only
when open AND ≥1 filtered option). Keyboard: arrows move highlight
(clamped, no wrap), Enter selects, Escape/Tab closes.

```html
<div class="form-group">
  <label for="server-url">Server URL</label>
  <input class="input" id="server-url" type="text" placeholder="http://127.0.0.1:8317">
  <span class="hint">Detected from the page URL.</span>
</div>
<div class="form-group">
  <label for="level">Level</label>
  <button class="select-trigger" id="level" type="button" aria-haspopup="listbox" aria-expanded="false"><span>Info</span><span aria-hidden="true">⌄</span></button>
</div>
```

```css
.input { width: 100%; border: 1px solid var(--border-color); border-radius: 8px; padding: 10px 12px; background-color: var(--bg-secondary); color: var(--text-primary); transition: border-color 150ms ease, box-shadow 150ms ease; }
.input:focus { outline: none; border-color: var(--primary-color); box-shadow: 0 0 0 3px rgba(139, 134, 128, 0.18); }
.form-group { display: flex; flex-direction: column; gap: 4px; margin-bottom: 16px; }
.form-group label { font-weight: 600; color: var(--text-primary); }
.hint { color: var(--text-secondary); font-size: 13px; }
.select-trigger { display: inline-flex; align-items: center; justify-content: space-between; gap: 8px; width: 100%; height: 40px; padding: 0 12px; border: 1px solid var(--border-color); border-radius: 8px; background-color: var(--bg-primary); box-shadow: var(--shadow); font-size: 13px; font-weight: 500; text-align: left; appearance: none; cursor: pointer; color: var(--text-primary); }
.select-trigger:hover { border-color: var(--border-hover); }
.select-trigger:focus, .select-trigger[aria-expanded="true"] { outline: none; box-shadow: var(--shadow), 0 0 0 3px rgba(139, 134, 128, 0.18); }
.select-trigger[aria-expanded="true"] { border-color: var(--primary-color); }
.select-dropdown { position: fixed; z-index: 2010; max-height: 240px; overflow-y: auto; background: var(--bg-primary); border: 1px solid var(--border-color); border-radius: 12px; padding: 6px; box-shadow: var(--shadow-lg); display: flex; flex-direction: column; gap: 4px; }
.select-option { padding: 8px 12px; border-radius: 8px; border: 1px solid transparent; font-size: 13px; font-weight: 500; text-align: left; cursor: pointer; }
.select-option:hover { background: var(--bg-secondary); }
.select-option.is-active { border-color: rgba(139, 134, 128, 0.5); background: rgba(139, 134, 128, 0.1); font-weight: 600; }
```

### 7.5 Toggles and checkboxes

ToggleSwitch (CSS-Modules; skeleton plain classes):
`ToggleSwitch.module.scss:9-74`. `<label>` wrapping a visually hidden
native checkbox + track + thumb, optional label text left/right (default
right). Track: `44px × 24px`, `background: var(--border-color)`,
radius `9999px`. Thumb: `18px`, `top/left: 3px`, `#fff`, radius
`9999px`, `box-shadow: 0 1px 2px 0 rgb(0 0 0 / 0.05)`. Checked: track →
`var(--primary-color)`, thumb `translateX(20px)`. Focus-visible on the
hidden input draws on the track: `outline: 2px solid var(--text-primary)`,
offset `2px`. Disabled: `cursor: not-allowed`, track `opacity: 0.5`.
Label: `var(--text-primary)`, `600`. Reduced motion: track/thumb
`transition: none`. **The 44px figure is the track width, not a touch
target** — do not cite it as one (§10).

SelectionCheckbox (`SelectionCheckbox.module.scss:12-83`): box
`22px`, radius `7px`, `border: 1px solid var(--border-color)`,
background 92% bg-secondary mix, centred 12px check icon
(`stroke-width: 2.4`). Checked: border + background →
`var(--primary-color)`, icon `var(--primary-contrast, #fff)`. Hover:
border → primary + ring `0 0 0 3px` 16% primary. Active:
`scale(0.95)`. Focus-visible: primary border + 3px 16% ring + 1px 50%
ring. Disabled: root `cursor: not-allowed`, `opacity: 0.6`, hover/active
suppressed. Label: `14px/500`. Native input is 1×1px clipped absolute,
never `display: none`.

```html
<label class="toggle"><input type="checkbox"><span class="toggle-track"><span class="toggle-thumb"></span></span><span class="toggle-label">Enable</span></label>
<label class="checkbox"><input type="checkbox" checked><span class="checkbox-box" aria-hidden="true">✓</span><span class="checkbox-label">Select all</span></label>
```

```css
.toggle { display: inline-flex; align-items: center; gap: 8px; cursor: pointer; }
.toggle input { position: absolute; width: 1px; height: 1px; overflow: hidden; clip: rect(0 0 0 0); }
.toggle-track { position: relative; width: 44px; height: 24px; background: var(--border-color); border-radius: 9999px; flex-shrink: 0; transition: background-color 200ms cubic-bezier(0.23, 1, 0.32, 1); }
.toggle-thumb { position: absolute; top: 3px; left: 3px; width: 18px; height: 18px; background: #fff; border-radius: 9999px; box-shadow: 0 1px 2px 0 rgb(0 0 0 / 0.05); transition: transform 200ms cubic-bezier(0.23, 1, 0.32, 1); }
.toggle input:checked + .toggle-track { background: var(--primary-color); }
.toggle input:checked + .toggle-track .toggle-thumb { transform: translateX(20px); }
.toggle input:focus-visible + .toggle-track { outline: 2px solid var(--text-primary); outline-offset: 2px; }
.toggle-label { color: var(--text-primary); font-weight: 600; }
.checkbox-box { width: 22px; height: 22px; border-radius: 7px; border: 1px solid var(--border-color); display: inline-flex; align-items: center; justify-content: center; font-size: 12px; color: transparent; }
.checkbox input:checked + .checkbox-box { border-color: var(--primary-color); background: var(--primary-color); color: var(--primary-contrast, #fff); }
```

### 7.6 Modals and sheets

Modal (`components.scss:225-383`, `Modal.tsx`): overlay `position: fixed`,
`inset: 0`, `background: rgba(0, 0, 0, 0.35)`, flex centred,
`z-index: 2000`, `padding: 24px`. Panel: `background: var(--bg-primary)`,
radius `12px`, border, `box-shadow: $shadow-lg` (SCSS, fixed
`0 10px 15px -3px rgb(0 0 0 / 0.1)` — not the theme-aware `--shadow-lg`
CSS var),
`max-width: 100%`, `max-height: 90vh`, `overflow: hidden`, column flex,
`transform-origin: calc(100% - 28px) 28px`. Default width `520`
(inline, `max-width: 100%`, `Modal.tsx:32,186`). Enter: fade-in overlay
`0.25s ease-out`; panel scale-in `0.3s cubic-bezier(0.34, 1.56, 0.64, 1)`
from `scale(0.85) translateY(20px)`; exit: fade-out `0.35s ease-in`,
panel collapse `0.35s cubic-bezier(0.4, 0, 0.2, 1)` to `scale(0)`;
close is delayed 350ms for the exit animation. Header: `padding:
16px 24px`, bottom border; title `18px/700`. Body: `padding: 24px`,
`overflow: auto`, `max-height: 65vh`. Footer: `padding: 16px 24px`, top
border, flex end, `gap: 8px`. Close button (floating): absolute
`top/right: 12px`, `32×32px`, `background: var(--bg-secondary)`, border,
`color: var(--text-secondary)`, radius `9999px`; hover → text-primary /
bg-tertiary + `scale(1.1)`; active `scale(0.95)`; disabled `opacity: 0.6`.
**No `:focus-visible` rule is stated** for `.btn` or the modal close
button. On mobile (≤768px): overlay padding `16px`; modal
`max-height: calc(100vh - 32px)` (100dvh variant), radius `8px`; header
padding `16px` + `padding-right: 52px`; body `16px`, `max-height:
min(60vh, calc(100vh - 180px))`; footer column-reverse, stretch,
`.btn { width: 100% }`. Focus: trap with wrap, first-focusable on open,
return on close, Escape closes unless `closeDisabled`; `role="dialog"`,
`aria-modal="true"`, `aria-labelledby`, portal to `document.body`,
scroll locked. The header always renders, even untitled; the footer
renders only when provided. ConfirmationModal renders its buttons in an
inline flex row (`justify-content: flex-end`, `gap: 1rem`,
`margin-top: 2rem`), **not** `.modal-footer`, so the mobile full-width
button rule does not apply to it; its default confirm variant is
`primary`, not `danger`.

Sheet (`Sheet.module.scss`, `Sheet.tsx`): right-side drawer dialog, the
only sheet variant. Overlay: fixed, `inset: 0`,
`background: rgba(0, 0, 0, 0.45)`, `backdrop-filter: blur(2px)`,
`z-index: 2000`, flex end, starts `opacity: 0`. Panel: full height,
column flex, `background: var(--bg-primary)`, left border, shadow
`-8px 0 32px rgba(0,0,0,0.16)` + `var(--floating-shadow)`, starts
`translate3d(100%, 0, 0)`. Sizes: `md: min(640px, 100vw)`,
`lg: min(720px, 100vw)`, `xl: min(960px, 100vw)`; default `md`. Header:
`padding: 20px 56px 20px 24px`, bottom border, column, `gap: 4px`;
eyebrow `11px/500` uppercase `0.05em` `var(--muted-foreground)`; title
`18px/600`; description `13px`, `var(--muted-foreground)`,
`line-height: 1.5`. Body: `flex: 1`, `overflow-y: auto`, `padding: 24px`.
Footer: `padding: 16px 24px`, top border, flex end, `gap: 12px`, wrap.
Close: absolute `top/right: 14px`, `32×32px`, transparent, no border,
`color: var(--text-secondary)`, radius `8px`, 18px icon; hover →
bg-tertiary/text-primary; `:focus-visible` 2px primary ring, offset 2px.
Animation: overlay fade 280ms; panel slide-in 320ms
`cubic-bezier(0.16, 1, 0.3, 1)`, slide-out 280ms
`cubic-bezier(0.32, 0.67, 0)`; close delay 280ms. Same focus-trap /
restore / scroll-lock pattern as Modal. Mobile (≤640px): panel
`width: 100vw`, no left border; header `16px 52px 16px 16px`; body
`16px`; footer `12px 16px`. Reduced motion: all enter/exit animations
`none`; entering overlay `opacity: 1`, panel `transform: none`.

```html
<div class="modal-overlay">
  <div class="modal" role="dialog" aria-modal="true" aria-labelledby="modal-title" style="width:520px">
    <button class="modal-close-floating" type="button" aria-label="Close">✕</button>
    <div class="modal-header"><div class="modal-title" id="modal-title">Confirm</div></div>
    <div class="modal-body"><p>Body copy.</p></div>
    <div class="modal-footer"><button class="btn btn-ghost" type="button"><span>Cancel</span></button><button class="btn btn-primary" type="button"><span>Confirm</span></button></div>
  </div>
</div>
```

```css
.modal-overlay { position: fixed; inset: 0; background: rgba(0, 0, 0, 0.35); display: flex; align-items: center; justify-content: center; z-index: 2000; padding: 24px; }
.modal { position: relative; background: var(--bg-primary); border-radius: 12px; border: 1px solid var(--border-color); box-shadow: 0 10px 15px -3px rgb(0 0 0 / 0.1); /* $shadow-lg (SCSS) — fixed, not theme-aware */ max-width: 100%; max-height: 90vh; overflow: hidden; display: flex; flex-direction: column; }
.modal-close-floating { position: absolute; top: 12px; right: 12px; width: 32px; height: 32px; padding: 0; background: var(--bg-secondary); border: 1px solid var(--border-color); color: var(--text-secondary); border-radius: 9999px; display: flex; align-items: center; justify-content: center; cursor: pointer; }
.modal-close-floating:hover { color: var(--text-primary); background: var(--bg-tertiary); transform: scale(1.1); }
.modal-close-floating:active { transform: scale(0.95); }
.modal-close-floating:disabled { opacity: 0.6; }
.modal-header { display: flex; padding: 16px 24px; border-bottom: 1px solid var(--border-color); }
.modal-title { font-weight: 700; font-size: 18px; color: var(--text-primary); }
.modal-body { padding: 24px; overflow: auto; max-height: 65vh; }
.modal-footer { padding: 16px 24px; border-top: 1px solid var(--border-color); display: flex; justify-content: flex-end; gap: 8px; background: var(--bg-primary); }
```

### 7.7 Tables

`Table` (`Table.module.scss:4-70`, `Table.tsx:12-90`): wrap
`1px solid var(--border-color)`, radius `8px`, `overflow: hidden`,
`background: var(--bg-primary)`; inner scroll `overflow-x: auto`. Table:
`width: 100%`, `border-collapse: separate`, `border-spacing: 0`,
`font-size: 13px`, `color: var(--text-primary)`. Header: background
`var(--muted-bg)`; `th`: `color: var(--muted-foreground)`,
`font-weight: 500`, `font-size: 12px`, left-aligned,
`padding: 10px 14px`, bottom border, `vertical-align: middle`. Cells:
`padding: 12px 14px`, bottom border, `vertical-align: top`,
`line-height: 1.5`; last row has no bottom border. Row hover: `td`
background 50% `--accent-bg` mix. Selected row: `td` background
`var(--primary-8)`. Right alignment via `alignRight` prop. **No
pagination, sorting, density variants, sticky header or zebra rule is
stated.** Table empty state: NOT STATED.

```html
<div class="table-wrap"><div class="table-scroll"><table class="table">
  <thead><tr><th>Name</th><th>Value</th></tr></thead>
  <tbody><tr><td>Alpha</td><td>1</td></tr></tbody>
</table></div></div>
```

```css
.table-wrap { border: 1px solid var(--border-color); border-radius: 8px; overflow: hidden; background: var(--bg-primary); }
.table-scroll { overflow-x: auto; }
.table { width: 100%; border-collapse: separate; border-spacing: 0; font-size: 13px; color: var(--text-primary); }
.table thead { background: var(--muted-bg); }
.table th { color: var(--muted-foreground); font-weight: 500; font-size: 12px; text-align: left; padding: 10px 14px; border-bottom: 1px solid var(--border-color); vertical-align: middle; }
.table td { padding: 12px 14px; border-bottom: 1px solid var(--border-color); vertical-align: top; line-height: 1.5; }
.table tbody tr:last-child td { border-bottom: none; }
.table tbody tr:hover td { background: color-mix(in srgb, var(--accent-bg) 50%, transparent); }
.table tbody tr.selected td { background: var(--primary-8); }
```

### 7.8 Skeletons and collapsibles

Skeleton (`Skeleton.module.scss:4-30`, `Skeleton.tsx:5-16`): `<div
class="skeleton" aria-hidden="true">`; `width`/`height`/`rounded` are
inline-style props with **no defaults** — callers must supply dimensions
or the div collapses to block width with no height. Visual: gradient
`90deg, var(--bg-tertiary) 0%, var(--bg-hover) 50%, var(--bg-tertiary)
100%`, `background-size: 200% 100%`, `animation: shimmer 1.5s
ease-in-out infinite`, radius `8px`, `display: block`; shimmer sweeps
`background-position: 200% 0` → `-200% 0`. Reduced motion: animation
`none`, flat `var(--bg-tertiary)`.

Collapsible (`Collapsible.module.scss:4-95`, `Collapsible.tsx`): native
`<details>`/`<summary>`, not a JS accordion. Root: border, radius `8px`,
`background: var(--bg-primary)`, `overflow: hidden`. Summary:
`list-style: none`, native marker hidden, `cursor: pointer`,
`padding: 10px 14px`, `13px/500`, flex `space-between`, `gap: 12px`,
`user-select: none`; hover → 35% `--accent-bg` mix. `:focus-visible`:
`outline: 2px solid var(--primary-color)`, offset `-2px`. Hint: `12px`,
`var(--muted-foreground)`, `400`. Chevron: `16×16px`,
`var(--muted-foreground)`, rotates 180° when `details[open]`, transition
`var(--dur-hover, 200ms)` / `var(--ease-out-strong, ease-out)`. Content:
`padding: 14px`, top border; `flush` variant: `padding: 0`, border kept.
Open animation is opacity-only fade-in at `var(--dur-press, 160ms)` —
deliberately no height animation, so programmatic `details.open` jumps
do not fight it. Controlled (`open`) or uncontrolled (`defaultOpen`,
default `false`).

```html
<div class="skeleton" aria-hidden="true" style="width: 100%; height: 16px;"></div>
<details class="collapsible">
  <summary><span>Advanced settings</span><span aria-hidden="true">⌄</span></summary>
  <div class="collapsible-content"><p>Hidden content.</p></div>
</details>
```

```css
.skeleton { display: block; border-radius: 8px; background: linear-gradient(90deg, var(--bg-tertiary) 0%, var(--bg-hover) 50%, var(--bg-tertiary) 100%); background-size: 200% 100%; animation: shimmer 1.5s ease-in-out infinite; }
@keyframes shimmer { from { background-position: 200% 0; } to { background-position: -200% 0; } }
.collapsible { border: 1px solid var(--border-color); border-radius: 8px; background: var(--bg-primary); overflow: hidden; }
.collapsible summary { list-style: none; cursor: pointer; padding: 10px 14px; font-size: 13px; font-weight: 500; display: flex; justify-content: space-between; gap: 12px; user-select: none; }
.collapsible summary::-webkit-details-marker { display: none; }
.collapsible summary:focus-visible { outline: 2px solid var(--primary-color); outline-offset: -2px; }
.collapsible-content { padding: 14px; border-top: 1px solid var(--border-color); }
```

### 7.9 Toasts / notifications

`NotificationContainer` (`NotificationContainer.module.scss`,
`NotificationContainer.tsx`, `notificationTimer.ts`, `constants.ts:56`):
container `position: fixed`, `z-index: 3000`,
`top: max(1rem, env(safe-area-inset-top))`, `inset-inline: 0`, centred
column, `gap: 0.5rem`, safe-area padding, `pointer-events: none` (cards
re-enable it); empty container `display: none`. Card: `width: fit-content`,
`max-width: min(26rem, 100%)`, `padding: 0.625rem 0.625rem 0.625rem 0.875rem`,
border, radius `12px`, `background: var(--floating-surface)`,
`box-shadow: var(--shadow-lg), var(--shadow)`. Types `success`, `warning`,
`error`, `info` set only `--notification-accent` / `--notification-tint`;
icons (18px): success `IconCheckCircle2`, warning `IconAlertTriangle`,
info and error both `IconInfo`. Icon chip: `1.75rem` square, radius `50%`,
tint background, accent colour, `margin-top: 0.125rem`. Message:
`0.875rem/500`, `line-height: 1.5`, `overflow-wrap: anywhere`,
`white-space: pre-wrap`; an sr-only type prefix
(`notification.type_<type>:`) precedes the text; `role="alert"` for error,
`role="status"` otherwise. Duration: default `3000ms`, overridable per
notification; exit transition 160ms. The timer counts only "readable"
time: paused on hover (non-touch pointers only), on focus within the
card, and when the tab is hidden; pauses can overlap (a `Set` of
reasons). Dismiss: close button (16px icon); Escape dismisses
immediately; dismissing while focused moves focus to the next/previous
card button or the pre-container focus target. Close button: `2rem`
square — `44px` (`2.75rem`, with negative margins) under
`@media (pointer: coarse)` — radius `8px`, transparent,
`color: var(--text-secondary)`; hover (fine pointers only) →
bg-tertiary/text-primary; active `scale(0.96)`; `:focus-visible` 2px
`var(--text-secondary)` ring, offset 2px. Enter from `@starting-style`
(`opacity: 0`, `translateY(-8px) scale(0.98)`), 200ms; exit: `opacity: 0`,
`translateY(-6px) scale(0.98)`, 160ms, `pointer-events: none`, `inert`,
`aria-hidden`. Reduced motion: transform none, opacity-only 120ms.
`prefers-contrast: more`: border → `var(--text-primary)`. **No
maximum-visible / queue rule is stated** in the assigned files; the
notification store shape was out of scope.

### 7.10 Empty, loading and error states

Empty state (`.empty-state`, `components.scss:437-496`,
`EmptyState.tsx:4-19`): `border: 1px dashed var(--border-color)`,
radius `12px`, `padding: 24px`, `background: var(--bg-secondary)`, flex
`space-between`, `gap: 16px`, centred. Icon: `42×42px`, radius `9999px`,
`2px solid var(--border-color)`, centred; inner svg `20×20px`,
`var(--text-secondary)`. Title `700`; description
`var(--text-secondary)`, `margin-top: 4px`. Component: fixed `IconInbox`
(20px); props `title` (required), `description?`, `action?`. **No mobile
or variant rule is stated.**

Loading spinner (`.loading-spinner`, `components.scss:199-221`,
`LoadingSpinner.tsx:1-13`): CSS base `16px`, `border: 3px solid
rgba(255,255,255,0.2)`, top border `#fff`, `animation: spin 0.8s linear
infinite`; under `@supports (color: color-mix(...))` the border becomes
22% `currentColor` mix with top border `currentColor`, so the spinner
inherits surrounding text colour. Component: default `size = 20`,
inline size, `borderWidth: size / 7`, `role="status"`,
`aria-live="polite"`. In `Button`, it renders at 16px by CSS with no
explicit size prop.

Error box (`.error-box`, `components.scss:539`): `background:
rgba(198,87,70,0.1)`, `border: 1px solid rgba(198,87,70,0.4)`, radius
`8px`, `padding: 8px 16px`, `color: #c65746`. Used by `Input` /
`AutocompleteInput` for field errors. No icon, no title slot, no variant
stated. **There is no red-border input error state, no error variant for
Card/Table/Sheet, and no global page-loading or page-error component**
in the assigned files; feature pages render spinner / `.error-box` /
`EmptyState` inline.

```html
<div class="empty-state">
  <span class="empty-icon" aria-hidden="true">▤</span>
  <div><div class="empty-title">No auth files yet</div><div class="empty-desc">Upload one to get started.</div></div>
  <span class="empty-action"><button class="btn btn-primary btn-sm" type="button"><span>Upload</span></button></span>
</div>
<div class="error-box" role="alert">Server URL is required.</div>
```

```css
.empty-state { border: 1px dashed var(--border-color); border-radius: 12px; padding: 24px; background: var(--bg-secondary); display: flex; justify-content: space-between; gap: 16px; align-items: center; }
.empty-icon { width: 42px; height: 42px; border-radius: 9999px; border: 2px solid var(--border-color); display: inline-flex; align-items: center; justify-content: center; color: var(--text-secondary); flex-shrink: 0; }
.empty-title { font-weight: 700; color: var(--text-primary); }
.empty-desc { color: var(--text-secondary); margin-top: 4px; }
.error-box { background: rgba(198, 87, 70, 0.1); border: 1px solid rgba(198, 87, 70, 0.4); border-radius: 8px; padding: 8px 16px; color: #c65746; }
```

### 7.11 Log-viewer toolbar (feature-local chrome, stated values only)

`LogsPage.module.scss`: shared `--log-control-height: 40px` (36px in
the two responsive blocks) for search input, level select, filter toggle
and action buttons: `height` + `min-height`, radius `8px`,
`border: 1px solid var(--border-color)`, `background: var(--bg-primary)`,
`13px/500`, `line-height: 1`, no shadow. Search wrapper `flex: 1 1 180px`,
`min-width: 120px`; input `padding: 0 38px 0 12px`; clear button
`28×28px`; search icon `var(--text-tertiary)`. Level select
`min-width: 110px`. Toolbar: flex, centred, `gap: 8px`,
`margin-left: auto`, `padding-left: 4px`. Follow button: absolute,
`bottom: 48px`, `left: 50%`, `translateX(-50%)`, `z-index: 2`,
`box-shadow: 0 2px 12px var(--border-color)`. Fullscreen card: fixed,
`inset: 0`, `z-index: 1999`, `100% × 100dvh`, no border/radius,
safe-area padding; JS adds `logs-fullscreen-active` to `<body>`. Log-row
hover (fine pointers only): 5% primary mix. Log-row rendering, parsing
and filters are out of scope for this guide — do not extrapolate the log
viewer from this chrome alone.

## 8. Icons

### 8.1 Conventions

`src/components/ui/icons.tsx:1-19`: inline SVG icons, Lucide (ISC),
paths embedded "to keep the WebUI single-file/offline friendly"
(source cited as lucide-static). Every icon defaults to `size = 20`
(width = height = size, overridable per call site). Shared
`baseSvgProps`: `viewBox="0 0 24 24"`, `fill="none"`,
`stroke="currentColor"`, `strokeWidth={2}`, `strokeLinecap="round"`,
`strokeLinejoin="round"`. Every icon is `aria-hidden="true"` and
`focusable="false"` by default — decorative unless a call site overrides
the props. Sole fill exception: the centre dot of `IconFilterAll`
(`fill="currentColor" stroke="none"`, `:95`). No icon font, no external
icon files; provider icons are separate SVG assets under
`src/assets/icons/` (not inventoried here).

Skeleton for a new icon in the same convention:

```html
<svg width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true" focusable="false"><!-- paths --></svg>
```

Sizes at call sites (sampled): sidebar icons 18px at the call site
(`MainLayout.tsx:57-67`, `size={18}`) but the rendered glyph is
constrained to 16px by `.nav-icon svg` in `layout.scss` (§5.2) — draw
16px; modal close 20px (`Modal.tsx:202`); Sheet close 18px
(`Sheet.tsx:234`); notification icon 18px
(`NotificationContainer.tsx:98`); Select chevron 14px; checkbox
check 12px; collapsible chevron 16px; autocomplete chevron 16px. The
header 16px claim was taken from an earlier read of `MainLayout.tsx`
and was **not re-verified** in the icons scout — [NEEDS-MEASUREMENT]
before quoting a line number for it.

### 8.2 Complete inventory — all 52 exports in `icons.tsx`

48 `export function` + 4 `export const` aliases, verified by grep.
All default to size 20. Lines are the export lines at the pinned commit.

| Export | Line | Export | Line |
| --- | --- | --- | --- |
| `IconCopy` | :22 | `IconChevronUp` | :281 |
| `IconSlidersHorizontal` | :31 | `IconChevronDown` | :289 |
| `IconKey` | :47 | `IconChevronLeft` | :297 |
| `IconBot` | :57 | `IconSearch` | :305 |
| `IconModelCluster` (custom, 3-box cluster) | :70 | `IconX` | :314 |
| `IconFilterAll` | :84 | `IconCheck` | :323 |
| `IconFileText` | :100 | `IconEye` | :331 |
| `IconShield` | :112 | `IconEyeOff` | :340 |
| `IconSettings` | :120 | `IconInbox` | :351 |
| `IconPlug` | :129 | `IconSatellite` | :360 |
| `IconScrollText` | :140 | `IconTimer` | :372 |
| `IconInfo` | :151 | `IconDollarSign` | :382 |
| `IconRefreshCw` | :161 | `IconGithub` | :391 |
| `IconDownload` | :170 | `IconHeart` | :400 |
| `IconUpload` | :180 | `IconExternalLink` | :408 |
| `IconTrash2` | :190 | `IconBookOpen` | :418 |
| `IconMaximize2` | :202 | `IconCode` | :427 |
| `IconMinimize2` | :213 | `IconSidebarDashboard` | :436 |
| `IconPlus` | :224 | `IconSidebarQuickStart` | :447 |
| `IconPencil` | :233 | `IconSidebarConfig` (alias of `IconSlidersHorizontal`) | :455 |
| `IconAlertTriangle` | :242 | `IconSidebarPlugins` (alias of `IconPlug`) | :457 |
| `IconCheckCircle2` | :252 | `IconSidebarStore` | :459 |
| `IconNetwork` | :261 | `IconSidebarProviders` (alias of `IconNetwork`) | :471 |
| `IconLoader2` | :273 | `IconSidebarAuthFiles` | :473 |
| | | `IconSidebarOauth` | :482 |
| | | `IconSidebarQuota` | :492 |
| | | `IconSidebarLogs` (alias of `IconScrollText`) | :501 |
| | | `IconSidebarSystem` | :503 |

**Not in the set — do not claim them:** no `IconChevronRight`, `IconMenu`,
`IconSun`, `IconMoon`, `IconGlobe` or `IconLogout` as named exports.
Header/menu/theme/logout glyphs in the layout are inline SVGs at the
call site, not members of this set. A port must either add those glyphs
to the icon set explicitly or keep them inline, and say which.

## 9. Motion and transitions

### 9.1 Vocabulary

- Interaction feedback (CSS): press `160ms`, hover `200ms`, UI motion at
  most `300ms`, with the strong decelerating curve
  `cubic-bezier(0.23, 1, 0.32, 1)` — tokens `--dur-press`,
  `--dur-hover`, `--ease-out-strong` (`themes.scss:88-92`; source comment:
  built-in easings are "too weak"). Components reference them with
  fallbacks, e.g. `var(--dur-press, 160ms)`,
  `var(--ease-out-strong, ease-out)` (`Collapsible.module.scss:78`,
  `ToggleSwitch.module.scss:33`). SCSS transitions: `$transition-fast`
  `150ms ease`, `$transition-normal` `300ms ease` (`variables.scss:34-35`).
- Entrance (JS): reveal rises `24px` over `0.45s` with `easeOutQuart`
  (`1 - (1 - progress) ** 4`); count-up runs `900ms` with the same
  easing, `requestAnimationFrame`-driven, integer-rounded; group stagger
  `70ms` per item, whole-group budget capped at `360ms`
  (`min(0.07, 0.36 / (n - 1))`) (`motion.ts:8-15,126-127,171-193`).
- Page transitions: vertical enter `0.36s` / +28px / `easeOutQuart`,
  exit `0.22s` / 12px / `easeInQuad`, fading to 0; iOS variant `0.44s`
  `easeOutCubic`, entering layer from ±100% x, exiting layer to −22%
  (forward) or +100% (backward), background layer scaled `0.96` at
  opacity `0.5`, front layer shadow `-20px 0 36px rgba(0,0,0,0.20)`
  (`PageTransition.tsx:20-40,297-350,368-386`). Direction comes from
  route order; scroll offsets are remembered per location key and
  restored with `behavior: 'auto'` (no smooth scroll). The iOS variant
  is used only within Auth Files sub-pages; everything else is vertical.
- Library: `motion/mini` (`animate`) for reveal and page transitions
  (`motion.ts:2`, `PageTransition.tsx:3-5`).

### 9.2 Reveal helpers — rules for reuse

`useRevealOnScroll` / `useRevealGroup` (`motion.ts:21-153`):
IntersectionObserver, `rootMargin: '0px 0px -12% 0px'`,
`threshold: 0.05`, animate once (unobserve on intersect), opacity 0→1 +
`translate3d(0, 24px, 0)` → `translate3d(0, 0, 0)`; inline styles are
cleared after the animation. The initial hidden state is written by JS
in `useLayoutEffect` before paint, so content stays visible if the
script never runs — no CSS pre-class is required. Group children are
`[data-reveal]` descendants in DOM order; `data-reveal="scale"`
children additionally animate from `scale(0.97)`. `useCountUp` jumps
straight to the target when disabled, under reduced motion, or when
`from === target`.

### 9.3 Other keyframes (traced)

| Animation | Rule |
| --- | --- |
| Spinner | `spin 0.8s linear infinite`, 0→360° (`components.scss:206,216-221`); excluded-models spinner `900ms` (`ExcludedModelsPicker.module.scss:70`) |
| Modal overlay / panel | overlay fade-in `0.25s ease-out`, fade-out `0.35s ease-in`; panel scale-in `0.3s cubic-bezier(0.34, 1.56, 0.64, 1)` from `scale(0.85) translateY(20px)`, collapse `0.35s cubic-bezier(0.4, 0, 0.2, 1)` to `scale(0)`, origin at the close-button corner (`components.scss:236-296`) |
| Sheet overlay / panel | overlay fade 280ms; panel slide-in 320ms `cubic-bezier(0.16, 1, 0.3, 1)`, slide-out 280ms `cubic-bezier(0.32, 0.67, 0)`, from `translate3d(100%, 0, 0)` (`Sheet.module.scss:16-74`) |
| Skeleton shimmer | `shimmer 1.5s ease-in-out infinite` (§7.8) |
| Collapsible expand | opacity-only fade at `var(--dur-press, 160ms)` (§7.8) |
| Rail tooltip | `nav-tooltip-in`, 150ms (`layout.scss:750,771-774`) |
| OAuth header meta dot | `oauth-meta-breathe 1.6s ease-in-out infinite`, opacity dips to 0.3 at 50% (`OAuthHeader.module.scss:61-68`) |
| Toasts | enter 200ms, exit 160ms (§7.9) |

### 9.4 Reduced motion — what actually changes

Detection: `prefersReducedMotion()` =
`window.matchMedia('(prefers-reduced-motion: reduce)').matches`
(`motion.ts:17-20`); `PageTransition.tsx` defines its own local copy
with the same query (`:42-43`) — the duplication is a porting hazard;
share one helper in a port, do not reproduce the duplication silently.

- Reveal / group / count-up: skipped, content shown at its final state
  immediately (`motion.ts:41,113,178`).
- Page transition: spatial motion skipped; `0.15s` crossfade,
  `easeOutCubic`, both layers (`PageTransition.tsx:24,249,261-287`).
- Smooth scrolling in `ConfigTabs` and field-jump: `behavior: 'auto'`
  instead of `'smooth'` (`ConfigTabs.tsx:45`, `useFieldJump.ts:72`).
- Floating bars (BatchActionBar, FloatingSaveBar): slide-up entrance
  replaced by a `0.15s` linear opacity fade (`BatchActionBar.tsx:80-95`,
  `FloatingSaveBar.tsx:70-85`).
- CSS: 52 `@media (prefers-reduced-motion: reduce)` blocks across
  `src/**/*.scss`; the sampled pattern is `animation: none` /
  `transition: none` (skeleton → static background, toggle → no
  transitions, collapsible chevron/content → no animation, notification
  → 120ms opacity only, OAuth pulse stops). Glass blur is removed under
  reduced motion / reduced transparency / ≤768px (§1.2).
- **Not confirmed:** the global `spin` keyframe and modal CSS animations
  have no reduced-motion override in `components.scss` (no
  `prefers-reduced-motion` block was found there); Sheet's own block
  does disable its animations. Do not claim modal/spinner motion is
  reduced-motion-gated.

## 10. Mobile touch targets — no global rule exists

There is **no global 44px/48px touch-target rule** in the assigned
component or layout styles. The only 44px/48px figures found are not
touch targets: toggle-track width 44px (height 24px), log follow-button
offset `bottom: 48px`, and one `min-height: 44px` outside the component
set (`SecondaryScreenShell.module.scss:21`, not claimed as a rule).
The only coarse-pointer enlargement found is the toast close button
(§7.9). Stated heights to reuse verbatim:

| Control | Height |
| --- | --- |
| Select trigger | `40px` / small `28px` |
| Log controls | `40px` / responsive `36px` |
| Floating header buttons | `38px` desktop / `36px` mobile |
| Toast close | `32px` fine pointer / `44px` coarse pointer |
| Modal close / Sheet close | `32px` / `32px` |
| Checkbox box / toggle track | `22px` / `24px` high |
| `.btn` (md / sm), `.input` | **No height stated** — padding only; do not convert to a height |

If a port needs a touch-target minimum, that is new work: state it as a
port decision, not as a reproduction of the source.

## 11. Theme switching

Mechanism (`useThemeStore.ts`, `constants.ts:33`, `types/common.ts:5`):

1. Store: Zustand + `persist`, key `'cli-proxy-theme'`. State: `theme`
   (user choice, default `'auto'`) and `resolvedTheme`
   (`'light' | 'dark'`, default `'light'`).
2. Resolution: `getSystemTheme()` returns `'dark'` iff
   `matchMedia('(prefers-color-scheme: dark)')` matches, else `'light'`.
   `resolveAutoTheme()` maps dark → `'dark'`, light → **`'white'`** —
   auto on a light OS shows the **white** theme, never light. Explicit
   `'white'` stays `'white'`; explicit `'light'`/`'dark'` pass through.
   `resolvedTheme` normalises `'white'` to resolved light.
3. Application: `'dark'` → `documentElement.setAttribute('data-theme',
   'dark')`; `'white'` → `setAttribute('data-theme', 'white')`; anything
   else (i.e. `'light'`) → `removeAttribute('data-theme')`, falling back
   to the `:root` block.
4. Live changes: `initializeTheme()` applies the stored theme once, then
   subscribes to the `(prefers-color-scheme: dark)` media query; on
   change it re-resolves **only** while the stored theme is `'auto'`.
5. The body `background-color`/`color` transition (300ms, §2.1) is what
   animates a theme switch. No `color-scheme` CSS property is set in
   `styles/` or `stores/` — native form-control dark styling relies on
   the explicit tokens.

Theme preview cards (`THEME_CARDS`, `MainLayout.tsx:258-307`) are
**illustrations for the picker, not tokens**: four entries (`auto`,
`white`, `light`, `dark`) with label keys (`theme.auto`, `theme.white`,
`theme.light`, `theme.dark`) and preview colours that differ from the
tokens in places (e.g. auto `bg` is a split gradient
`linear-gradient(135deg, #ffffff 0 50%, #111111 50% 100%)`; auto `card`
uses `#1a1a1a` where the dark theme card is `#1d1b18`). **Do not copy
THEME_CARDS values as theme tokens.**

## 12. i18n and text handling

- Library: `i18next` + `react-i18next`, initialised once in
  `src/i18n/index.ts:15-32` with `useSuspense: false`.
- Six bundled JSON locales: `zh-CN`, `zh-TW`, `en`, `ru`, `vi`, `ko`
  (`i18n/index.ts:7-12,17-22`). Fallback: `fallbackLng: 'zh-CN'` —
  missing keys fall back to Simplified Chinese, **not** English.
- Interpolation: `escapeValue: false` (React already escapes).
  `{{count}}`, `{{name}}`, `{{message}}`, `{{type}}`, `{{total}}`,
  `{{provider}}` and others, always double-brace syntax in JSON values.
  Plurals: i18next `_one`/`_other` pairs (e.g. `cooldown_models_one` /
  `_other`, `en.json:239-243`); `_zero`/`_few`/`_many` use was not
  exhaustively audited.
- Language type: `'zh-CN' | 'zh-TW' | 'en' | 'ru' | 'vi' | 'ko'`
  (`types/common.ts:7`). Menu order:
  `['zh-CN', 'zh-TW', 'en', 'ru', 'vi', 'ko']` (`LANGUAGE_ORDER`,
  `constants.ts:39-46`); labels are i18n keys
  (`language.chinese`, `language.chinese_tw`, `language.english`,
  `language.russian`, `language.vietnamese`, `language.korean`) — the
  menu shows translated names, not hard-coded endonyms.
- Persistence: key `'cli-proxy-language'` (`constants.ts:34`). Initial
  language: stored value (if valid, accepting both a zustand-persist
  JSON envelope and a bare string) wins; otherwise browser language:
  `zh-TW`/`zh-HK`/`zh-MO`/`zh-Hant` → `zh-TW`, `zh*` → `zh-CN`,
  `ru*` → `ru`, `vi*` → `vi`, `ko*` → `ko`, anything else → `en`
  (`language.ts:12-60`). Switching rejects unsupported values silently,
  calls `i18n.changeLanguage`, persists with a merge guard
  (`useLanguageStore.ts:20-46`). `document.documentElement.lang` is set
  from the active language on every change (`App.tsx:51-54`).
- The shipped `index.html` starts as
  `<html lang="zh-CN" translate="no" class="notranslate">` with
  `<meta name="google" content="notranslate">` — machine translation is
  explicitly opted out (`index.html:2,5`).
- Copy is keyed, not hard-coded: `useTranslation()` / `t('…')` with
  dotted keys in 103 `.tsx` files; accessible labels are keyed too
  (e.g. modal close `aria-label={t('common.close')}`). Adding or
  changing a key means updating all six locales, including accessible
  labels. Locale parity is **imperfect**: leaf-key counts en 2038,
  ko 2038, ru 2034, vi 2044, zh-CN 2036, zh-TW 2064 (43 top-level
  groups, ru 42) — the zh-CN fallback, not parity, keeps the UI whole.
  Whether zero hard-coded user-facing strings exist was **not** proven
  by a sweep; do not claim it. Some `t()` calls pass `defaultValue` as
  a missing-key fallback, not a substitute for a locale entry.
- Number/date formatting (`utils/format.ts`): `formatCompactNumber`
  (1284 → `1.3K`, suffixes `['', 'K', 'M', 'B', 'T']`, ≤3 significant
  digits, re-tiers after rounding overflow, 999,999 → `1M`);
  `formatPercent(value, fractionDigits = 1)` (`toFixed`, trailing `.0`
  stripped, `—` for non-finite); `formatFileSize` (1024-based,
  2 decimals, B/KB/MB/GB); `maskApiKey` (keeps 2 chars at each end, 1 if
  shorter than 4, middle `*` to a total masked length of 10);
  `formatUnixTimestamp` accepts seconds/ms/µs/ns by magnitude and
  renders with `toLocaleString(locale?)`; date helpers use
  `toLocaleDateString`/`toLocaleString` with an optional locale;
  invalid values render as `''`. Call sites thread `i18n.language`
  into the helpers (sampled, not exhaustively audited).
- No `text-transform: uppercase` convention was audited; do not claim one.

## 13. Accessibility

### 13.1 Focus — per component, no global rule

There is **no global `:focus-visible` rule** in `src/styles/`. Focus
styling is per-component and inconsistent by design in this codebase;
reproduce each control's own rule rather than inventing one global ring.

| Control | Focus rule |
| --- | --- |
| `.input` / `textarea`, Select trigger | `:focus`: `outline: none` + primary border + `0 0 0 3px rgba(139,134,128,0.18)` ring (shows on mouse focus too) |
| Toggle track, collapsible summary, Sheet close | `:focus-visible`: 2px outline (toggle on the visible track via the hidden native input; collapsible offset `-2px`, others `2px`) |
| Checkbox box | `:focus-visible` on the hidden native input: **no outline** — border → `var(--primary-color)` plus two rings, `0 0 0 3px` 16% primary and `0 0 0 1px` 50% primary (`SelectionCheckbox.module.scss:66-70`) |
| Sidebar toggle, header buttons, language options, theme cards | `:focus-visible`: `outline: none` + `0 0 0 2px` primary mix ring — sidebar toggle 24% (`layout.scss:136`), header buttons 26% (`:198`), language options 22% (`:259`), theme cards 22% (`:302`) |
| Toast close | `:focus-visible`: 2px `var(--text-secondary)` ring, offset 2px |
| `button-reset` mixin | `:focus`: `outline: 2px solid $primary-color`, offset `2px` (small icon buttons; **not** applied to `.btn`) |
| `.btn`, modal close button, card, table | **NOT STATED** |
| Shared focusable selector | `a[href], button:not([disabled]), input:not([disabled]), select:not([disabled]), textarea:not([disabled]), [tabindex]:not([tabindex="-1"])` (`scrollLock.ts:88-95`) |

### 13.2 Keyboard: dialogs, menus, lists

- Modal / Sheet: focus moves to the first focusable element on open
  (fallback: close button, then the dialog itself); Tab/Shift+Tab wrap
  first↔last; with no focusable elements Tab is swallowed and the dialog
  is focused; focus returns to the pre-open element on close; Escape
  closes (unless `closeDisabled`), delayed by the close animation
  (350ms / 280ms); scroll locked; `role="dialog"`, `aria-modal="true"`,
  `aria-labelledby`, `tabIndex={-1}`, portal to `document.body`
  (`Modal.tsx:82-196`, `Sheet.tsx:132-231`).
- Select: ArrowDown/Up open then move highlight (wrapping), Home/End
  jump, Enter/Space open or commit, Escape closes and returns focus to
  the trigger, Tab closes; commit returns focus to the trigger. Full
  ARIA wiring (`aria-activedescendant` etc.) was only partially audited
  — keyboard behaviour and the option-id scheme are verified; role
  wiring is not fully claimed.
- Menus (language/theme): dismissed on outside pointer-down or Escape
  via a shared hook; buttons use `aria-haspopup="menu"`,
  `aria-expanded`; items use `role="menuitemradio"` + `aria-checked`.
- Sidebar toggle shortcut: `Ctrl+B` / `⌘B`, suppressed in inputs,
  textareas and content-editable elements (§5.2). No
  `aria-keyshortcuts` attribute was found — the shortcut is labelled in
  text/tooltips only.
- Notification dismiss: Escape on a focused card dismisses it; focus
  moves to the next/previous notification button, else to a saved
  return-focus target. Autocomplete / excluded-models picker Escape
  handling exists; exact behaviour was not fully audited in each case.
- No roving-tabindex grid/list pattern is claimed beyond Select.

### 13.3 ARIA, roles, live regions

Most-used attributes over `src/**/*.tsx` (grep counts): `aria-hidden`
126, `aria-label` 116, `aria-describedby` 26, `aria-pressed` 16,
`aria-invalid` 14, `aria-expanded` 11, `aria-labelledby` 10,
`aria-controls` 7, `aria-haspopup` 6, `aria-busy` 6, `aria-live` 5,
`aria-valuenow/min/max` 4 each, `aria-selected` 4,
`aria-activedescendant` 4, `aria-modal` 2, `aria-checked` 2. Roles:
`status` 17, `group` 14, `alert` 13, `img` 6, `option` 3, `listbox` 3,
`radiogroup` 2, `progressbar` 2, `menuitemradio` 2, `menu` 2,
`dialog` 2, plus single uses of `tooltip`, `toolbar`, `tabpanel`,
`tablist`, `tab`, `region`, `presentation`, `note`, `combobox`.

- Loading spinner: `role="status"` + `aria-live="polite"`, no text.
- Live regions are **polite only** (5 hits, all polite): spinner,
  batch-action count, floating save-bar status, OAuth flow status,
  SIWC bind status. No `aria-live="assertive"` was found; error/alert
  surfacing uses `role="alert"` (13 uses) instead.
- Screen-reader-only text: local `.srOnly` utilities (absolute, 1×1px,
  clipped) in NotificationContainer, CopyButton, QuotaCard, plus the
  global `.nav-badge-sr-only`. Notifications prefix an sr-only type
  label before the message text.
- Non-current page layers and exiting notifications: `aria-hidden` +
  `inert`. `inert` is used as a plain attribute; no polyfill or fallback
  was seen in the files read.
- **No skip link exists** — no skip-to-content pattern in `src/`. Do not
  claim one; adding one is new work.
- Colour-only meaning and contrast were **not audited** in this guide.
  The theme file carries a comment that the three themes passed
  contrast/colour-blindness/brightness checks (`themes.scss:236-241`);
  that is a comment claim, not a measurement. Toasts are the only
  forced-colours handling found: `prefers-contrast: more` → border
  `var(--text-primary)`.

### 13.4 Other global rules

Base font smoothing / line-height and `font: inherit` for form controls:
§2.1. Scrollbar: §3.4. Modal-open scroll lock: §3.4. The `prefers-contrast`
toast rule is in §7.9. Focus-visible behaviour on every custom control
(date pickers, CodeMirror editor, log viewer) was not audited — only the
shared controls in §13.1 were checked.

## 14. NOT FOUND — do not invent

1. No typography scale (font-size/weight/heading scale) in the style
   files read. Sizes in §2.2 are per-component declarations.
2. No global 44px/48px touch-target rule; no global `:focus-visible`
   rule; no skip link; no `aria-keyshortcuts`; no `color-scheme`.
3. No literal pixel/dither/dot/noise header texture in the shell (§6).
4. No standalone Routing page at the pinned commit (see `SKILL.md` §4.9).
5. No tablet-specific shell layout; the `tablet` mixin is unused in
   `layout.scss`. No content `max-width`. No grid in the shell.
6. No `.btn` font-size/height/`:active`/`:focus-visible`; no `.input`
   disabled or error-border styling; no Select disabled visual; no
   `.btn`/modal-close focus rule; no Card variants/hover; no Table
   empty/sort/pagination/sticky/zebra; no Skeleton defaults; no
   notification max-visible/queue rule or store shape; no
   confirmation-modal mobile full-width rule (it does not use
   `.modal-footer`).
7. No `.status-badge` `.info` variant; no `IconChevronRight`/`IconMenu`/
   `IconSun`/`IconMoon`/`IconGlobe`/`IconLogout` exports; no
   `IconChevronRight` in `icons.tsx` at all.
8. No consumer of `--content-center-x` found in the shell files read;
   no Escape/focus-trap for the mobile drawer; no verified stacking
   order of Select dropdown vs Sheet vs Modal beyond the raw numbers;
   no verified rendered `--header-height` (JS-measured) or visual effect
   of the hard-coded `#0d0c0a` gradient stop in light/white themes.
9. No reduced-motion override confirmed for the global `spin` keyframe
   or modal CSS animations; no full Select ARIA audit; no full
   touch-target audit; no contrast/colour-blindness measurement; no
   plural-category audit beyond `_one`/`_other`; no hard-coded-string
   sweep proving zero hard-coded copy; provider icon assets under
   `src/assets/icons/` not inventoried.
10. `THEME_CARDS` preview values are not tokens (§11). `$gray-400`,
    `$shadow-md`, `--bg-quinary`, `--glass-bg-secondary` are defined but
    unused in `src/` (§1.3).

## 15. Porting checklist

Copy as-is: the §1.1 token blocks and §1.2 glass override; the §2.1 base
rules; the §5 shell tokens and drawer/backdrop geometry; the §6
gradient overlay (with its `#0d0c0a` stop kept, and its light-theme
reading checked in a browser); the §7 component geometries; the §8 icon
convention and inventory; the §9 motion vocabulary and reduced-motion
collapses; the §11 theme-switching mechanism (including the
auto→white trap); the §12 i18n setup (six locales, zh-CN fallback,
keyed labels, locale-threaded formatting).

Adapt, stating the decision: SCSS `$` variables → CSS vars or literals
(§1.4); CSS-Modules class names → plain classes (skeletons show the
mapping); the `prefersReducedMotion` duplication → one shared helper
(§9.4); missing glyphs (right chevron, sun/moon, globe, logout) → add
to the icon set or keep inline (§8.2); a touch-target minimum, a skip
link, a global focus ring, or a typography scale, if wanted — all new
work, none in the source (§§10, 13, 14).

Leave behind: `THEME_CARDS` preview values as tokens; unused tokens
(§1.3); and the upstream hex palette as the new product's brand
identity — reuse the token *structure* from §1.1, and the values there
only where the goal is reproducing this look; a distinct product should
re-derive its own palette in that structure. Also leave behind the
sponsor/Quick Start special-casing and provider-specific lists (see
`SKILL.md` §9 and `PROVENANCE.md` REPO-ONLY); the v0 legacy probe; Chinese working comments as user copy; the `logo.jpg` asset and
exact theme palette as branding (the mechanism is ported, the brand is
not — per `PROVENANCE.md`).

Verify in a browser before shipping a port: rendered `--header-height`;
the `#0d0c0a` gradient stop in light/white themes; modal/spinner
behaviour under reduced motion; Select dropdown stacking against Sheet
and Modal; any component whose only evidence here is a call-site size
(header icons, §8.1). Static checks cannot verify browser interaction —
say so when a change needs a real browser check, as `SKILL.md` §8
requires.
