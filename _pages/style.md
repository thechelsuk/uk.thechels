---
layout: pages
title: Style Guide
permalink: /style
seo: Style Guide
---


## Headings

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

Write paragraphs by simply typing text. Separate paragraphs with a blank line.

Example:

```markdown
This is the first paragraph.

This is the second paragraph.
```

This is the first paragraph.

This is the second paragraph.

## Emphasis

You can add emphasis by making text bold or italic.

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
[GitHub](https://github.com)
```

[GitHub](https://github.com)

## Images

Embed images using the following syntax:

```markdown
![Alt Text](Image URL)
```

Example:

```markdown
![GitHub Logo](/images/me72.png)
```

![GitHub Logo](/images/me72.png)

## Blockquotes

Create blockquotes using the `>` symbol.

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

Use triple backticks to create code blocks.

Example:

\`\`\`markdown
\`\`\`
This is a code block.
\`\`\`
\`\`\`

\`\`\`markdown
This is a code block.
\`\`\`

## Tables

Create tables using pipes `|` and hyphens `-`.

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

Create a horizontal rule using three or more hyphens, asterisks, or underscores.

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
[GitHub](https://github.com "GitHub Homepage")
```

[GitHub](https://github.com "GitHub Homepage")

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

You can create task lists using `- [ ]` for unchecked items and `- [x]` for checked items.

Example:

```markdown
- [ ] Task 1
- [x] Task 2
```

- [ ] Task 1
- [x] Task 2

### Definition Lists

You can create definition lists using terms and definitions.

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
> This is a blockquote with a custom class.
{: .custom-class}
```

> This is a blockquote with a custom class.
{: .custom-class}
