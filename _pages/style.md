---
layout: pages
title: Style Guide
permalink: /style
seo: Style Guide
---

This style guide acts as a visual guide to the mark-up styles used throughout the site and acts as a check that all likely mark-up is styled appropriately.

There is one additional style applied to the code blocks on this page for eligibility.


## Headings

The page or post title using`h1` headings.
Section uses `h2` and further sub-headings continue as needed, it's rare to go beyond `h4` if it feels like this is needed, rethink the content format.

Use the following markdown syntax to create headings:

```markdown
# Heading 1
## Heading 2
### Heading 3
#### Heading 4
##### Heading 5
###### Heading 6
```

Example:

# Heading 1
## Heading 2
### Heading 3
#### Heading 4
##### Heading 5
###### Heading 6

## Paragraphs

Paragraphs are simply typing text. Separate paragraphs with a blank line. This is a key tenant of markdown format, it allows the focus to be on content.

Example:

```markdown
This is the first paragraph.

This is the second paragraph.
```

This is the first paragraph.

This is the second paragraph.

## Emphasis

You can add emphasis by making text bold or italic. Use with caution and in limited fashion. Don't use `bold` for headings, it's not semantic.

- **Bold**: `**bold text**` or `__bold text__`
- *Italic*: `*italic text*` or `_italic text_`
- ***Bold and Italic***: `***bold and italic***` or `___bold and italic___`

Example:

```markdown
**This is bold text**

*This is italic text*

***This is bold and italic text***
```

**This is bold text**

*This is italic text*

***This is bold and italic text***

## Lists

### Unordered List

Use `-`, `*`, or `+` to create an unordered list.

Example:

```markdown
- Item 1
- Item 2
    - Subitem 1
    - Subitem 2
```

- Item 1
- Item 2
    - Subitem 1
    - Subitem 2

### Ordered List

Use numbers followed by a period to create an ordered list.

Example:

```markdown
1. First item
2. Second item
     1. Subitem 1
     2. Subitem 2
```

1. First item
2. Second item
     1. Subitem 1
     2. Subitem 2

## Links

Create links using the following syntax:

```markdown
[Link Text](URL)
```

Example:

```markdown
[TheChels](https://thechels.uk)
```

[TheChels](https://thechels.uk)

## Images

Embed images using the following syntax:

```markdown
![Alt Text](Image URL)
```

Example:

```markdown
![TheChels Logo](/images/me72.png)
```

![TheChels Logo](/images/me72.png)

## Blockquotes

Create blockquotes using the `>` symbol. For a large quote that has paragraphs of text use `>` with a blank link.

Example:

```markdown
> This is a blockquote.
```

> This is a blockquote.

## Code

### Inline Code

Use backticks to create inline code.

Example:

```markdown
Here is some `inline code`.
```

Here is some `inline code`.

### Code Blocks

Use triple backticks to create code blocks. and include the rendering/code e.g. `markdown`, `css`, or `html` to render code highlighting.

Example:

\`\`\`markdown

This is a code block.

using a multi-line approach.

\`\`\`


```markdown
This is a code block.
using a multi-line approach.
```


## Tables

Create tables using pipes `|` and hyphens `-`. Tables should be used for tabular content only and not for handling layouts or page structure. Don't have large tables as they are hard to read. If this is necessary then provide the file as a download e.g. excel or as a pdf

Example:

```markdown
| Header 1 | Header 2 |
|----------|----------|
| Row 1    | Data 1   |
| Row 2    | Data 2   |
```


| Header 1 | Header 2 |
|----------|----------|
| Row 1    | Data 1   |
| Row 2    | Data 2   |

## Horizontal Rule

Create a horizontal rule using three or more hyphens, asterisks, or underscores. This shouldn't be used in content, but it's included here for completeness

Example:

```markdown
---
```

---

## Additional Examples

### Links with Titles

You can add a title to a link that appears when you hover over it.

Example:

```markdown
[TheChels](https://thechels.uk "Homepage")
```

[TheChels](https://thechels.uk "Homepage")

### Nested Lists

You can create nested lists by indenting list items.

Example:

```markdown
1. First item
   - Subitem 1
   - Subitem 2
2. Second item
   * Subitem 1
   * Subitem 2
```

1. First item
   - Subitem 1
   - Subitem 2
2. Second item
   * Subitem 1
   * Subitem 2

### Task Lists

You can create task lists using `- [ ]` for unchecked items and `- [x]` for checked items, this might be used to convey progress of a list of work items but should be used sparingly.

Example:

```markdown
- [ ] Task 1
- [x] Task 2
```

- [ ] Task 1
- [x] Task 2

### Definition Lists

You can create definition lists using terms and definitions in markdown, but are unlikely to be used on this site.

Example:

```markdown
Term 1
: Definition 1

Term 2
: Definition 2
```

Term 1
: Definition 1

Term 2
: Definition 2

### Custom CSS Classes

You can add custom CSS classes to elements using the `{: .class}` syntax.

Example:

```markdown
> This is a blockquote with a custom class `secondary`.
{: .secondary}
```

> This is a blockquote with a custom class `secondary`.
{: .secondary}


## Fonts

You can apply custom fonts using the variables defined in the CSS.

## Fonts

You can apply custom fonts using the variables defined in the CSS.

Example:

```html
<ul>
    <li><span class="font-stack">This is the primary font.</span></li>
    <li><span class="font-mono">This is the mono font.</span></li>
</ul>
```

<ul>
    <li><span class="font-stack">This is the primary font.</span></li>
    <li><span class="font-mono">This is the mono font.</span></li>
</ul>

### Font Colors

You can apply custom font colors using the variables defined in the CSS. The `accent` color is used for borders or backgrounds and should be used for text for accessibility reasons as it's hard to read.

Example:

```html
<p>
    <span class="primary">This is primary text.</span><br>
    <span class="secondary">This is secondary text.</span><br>
    <span class="link">This is link text.</span><br>
    <span class="accent">This is the accent color.</span>
</p>
```

<p>
    <span class="primary">This is primary text.</span><br>
    <span class="secondary">This is secondary text.</span><br>
    <span class="link">This is link text.</span><br>
    <span class="accent">This is the accent color.</span>
</p>
