## Overview

A comprehensive tidy-up of `style.scss`, `style_print.scss`, and the `_layouts` / `_includes` templates. Items are grouped by priority and type.

---

## 🔴 High Priority

### 1. Fix `.sr-only` — Accessibility Bug
`display: none` hides content from **everyone**, including screen readers. This defeats the purpose of the class entirely.

**File:** `style.scss` line 600

**Current:**
```scss
.sr-only {
    display: none;
}
```

**Fix:**
```scss
.sr-only {
    clip-path: inset(50%);
    height: 1px;
    overflow: hidden;
    position: absolute;
    white-space: nowrap;
    width: 1px;
}
```

---

### 2. Fix Unclosed `<p>` tag in `films.html`
An opening `<p>` is used where a closing `</p>` should be, resulting in invalid HTML.

**File:** `_layouts/films.html`

```html
<p>
  <small>... RSS Feed</a> |
  </small>

<p>   <!-- ← should be </p> -->
```

---

### 3. Fix Mismatched `</b>` tags in `directory.html`
Every `<li>` in this file has a closing `</b>` with no matching opening `<b>`.

**File:** `_layouts/directory.html`

```html
<li>{{ site.posts | size }}</b> posts written.</li>
<!--                    ↑ stray closing tag, no opening <b> -->
```

This affects every list item in both the Content Summary and Site Data Summary sections.

---

### 4. Merge Duplicate `img` Rule
`img` is defined twice in `style.scss` with no reason for separation.

**Files:** `style.scss` lines 354 and 454

**Fix:** Merge into one:
```scss
img {
    display: block;
    max-width: 100%;
    height: auto;
    border: 1px solid $primary;
}
```

---

## 🟡 Medium Priority — CSS Modernisation

### 5. Add `.flow` and `.stack` Utility Classes
Replace scattered, inconsistent vertical margins with the lobotomised owl pattern. This reduces CSS and makes spacing more predictable.

**Add to `style.scss`:**
```scss
.flow > * + * {
    margin-block-start: var(--flow-space, 1em);
}

.stack > * + * {
    margin-block-start: 1.5rem;
}
```

**Then remove or reduce these rules** (once `.flow` is applied to parent containers in the HTML):
- `article { margin: 3em 0; }` — replace with `--flow-space: 3em` override
- `h1-h6 { margin-top: 0.75em; }` — replace with `--flow-space: 0.75em` override
- `ol li, ul li { margin-bottom: 7px; }` — use `.stack` on list elements
- `ul ul, ol ol... { margin-top/bottom }` — covered by `.flow`

**HTML changes needed** — add `class="flow"` to:
- `<div id="blog-archives">` in `_layouts/index.html`
- `<article>` in `_layouts/post.html`
- Parent containers in `blogroll.html`, `teams.html`, `directory.html`

---

### 6. Remove Outdated Vendor Prefixes
These prefixes haven't been needed since ~2015.

**File:** `style.scss` lines 142–144

```scss
-webkit-box-sizing: content-box;  // remove
-moz-box-sizing: content-box;     // remove
box-sizing: content-box;          // keep
```

Same applies in `style_print.scss`.

---

### 7. Simplify Heading Link Selectors with `:is()`
Already using `:is()` elsewhere (line 482) — apply it here too.

**File:** `style.scss` lines 294–309

**Current:**
```scss
h1 a, h2 a, h3 a, h4 a, h5 a, h6 a { ... }
```

**Fix:**
```scss
:is(h1, h2, h3, h4, h5, h6) a {
    text-decoration: none;
    color: $primary;

    &:hover, &:focus {
        text-decoration: none;
    }
}
```

---

### 8. Standardise Units — Replace `px` with `rem`
Mixed `px` and `rem`/`em` units reduce accessibility (user font scaling is ignored).

**Files:** `style.scss`

| Current | Suggested |
|---|---|
| `.meta { font-size: 12px; }` | `font-size: 0.75rem;` |
| `ol li { margin-bottom: 7px; }` | `margin-bottom: 0.4375rem;` |
| `table th, td { padding: 8px; }` | `padding: 0.5rem;` |
| `.post > h2 { margin-top: 60px; }` | `margin-top: 3.75rem;` (or review if needed at all) |

---

### 9. Remove Redundant `font-family` in `pre > code`
`font-family` is already inherited from the `pre, code` rule above.

**File:** `style.scss` lines 374–377

```scss
pre > code {
    font-family: $font-mono; // remove — already inherited
    font-size: 0.9em;        // keep
}
```

---

### 10. Move Inline Styles to CSS Classes

**`_includes/footer.html`** — avatar image has inline styles:
```html
style="display:inline;vertical-align:text-bottom;position:relative;top:-1px;"
```
Move to a `.footer-avatar` class in `style.scss`.

**`_layouts/post.html`** — hidden microformat links use inline `style="display:none":
```html
<a class="u-url" href="..." style="display:none"></a>
```
Move to a `.u-url` or `.visually-hidden-link` class.

---

## 🟢 Low Priority — Housekeeping

### 11. `.post-title` Class Has No CSS Rule
Used on `<h1>` in every single layout, but never defined in `style.scss`. Either add an intentional rule or remove the class from the HTML templates.

**Used in:** `default.html`, `index.html`, `post.html`, `books.html`, `blogroll.html`, `films.html`, `teams.html`, `slashes.html`, `directory.html`

---

### 12. `.table-striped` Has No CSS Rule
Used in `films.html` but never defined in `style.scss` — the class currently does nothing.

**File:** `_layouts/films.html`

**Fix:** Either add a rule or remove the class:
```scss
.table-striped tr:nth-child(even) {
    background-color: $alt-tab;
}
```
(Note: the generic `table` rule already handles this — so `.table-striped` may just be removable.)

---

### 13. `.blog-menu ul` Has No List Reset
`.blog-menu` is used on `<nav>` elements containing `<ul>` lists, but there is no style reset for the list itself — bullets and default padding will show.

**File:** `style.scss`

**Fix:**
```scss
.blog-menu ul {
    list-style: none;
    padding: 0;
    margin: 0;
}
```

---

### 14. Consolidate Media Queries
Three breakpoints exist but the smallest has a redundant `min-width: 320px` constraint.

**File:** `style.scss` lines 527, 569, 584

```scss
@media only screen and (min-width: 320px) and (max-width: 480px) { ... }
// simplify to:
@media screen and (max-width: 480px) { ... }
```

Consider consolidating all three breakpoints into a single organised section at the bottom of the file.

---

### 15. Remove Duplicate `mobile-web-app-capable` Meta Tag
Appears twice in `_includes/header.html`.

```html
<meta name="mobile-web-app-capable" content="yes">  <!-- appears twice -->
```

Remove one.

---

### 16. Remove Commented-Out Star Icon in `post_icon.html`
Appears to be a v1 leftover.

**File:** `_includes/post_icon.html`

```html
<!-- &#9733; -->
```

---

### 17. Check `.radius` Class Usage
`style.scss` line 223 defines `.radius { border-radius: 1em; }` — verify this is actually used in any HTML/markdown. If not, remove it.

---

### 18. Review `.post > h2` Override
```scss
.post > h2 {
    margin-top: 60px;
    margin-right: 130px;
}
```
This uses `px` units and looks like it may be a v1 layout hack. Review whether it's still needed or whether it can be replaced with a more intentional approach once `.flow` is adopted.