---

layout: post
date: 2025-01-26
link: https://www.stefanjudis.com/blog/load-the-default-os-font-with-css/
title: Load the default OS font with CSS
cited: Stefan Judis

---

Very cool indeed, I have given this site a little stylistic refresh over the last week or so.

- Reducing the used colour scheme to 5 major colours and one minor accent
- Updated the font family as per Stefan's post and removed a script call to Google

This should mean better performance, less maintenance and easier refreshes in the future utilising variables in my scss file.

> Cool! By using system-ui as default font, I could clean up a bit of CSS and go with this beauty.

>    ```css
>     body { font-family: system-ui, sans-serif; }
>    ```

> Nice and clean. This site will now render .SF NS on MacOS, and I don't have a Windows machine, but it seems to be Segoe UI Variable. But whatever is available on the OS does the trick for me.
