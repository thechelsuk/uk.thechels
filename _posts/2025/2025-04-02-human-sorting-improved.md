---

layout: post
date: 2025-04-02
link: https://nedbatchelder.com/blog/202503/human_sorting_improved.html
title: Human sorting improved
cited: Ned Batchelder

---

> I wrote about this long ago ([Human sorting](https://nedbatchelder.com/blog/200712/human_sorting.html)), but have continued to tweak the code and needed to [add it to a project](https://github.com/nedbat/watchgha/commit/cfcd48ac3f24f5b76aa02caa695af13e37f38bcf) recently. Here's the latest:
>
>
>     import re
>
>     def human_key(s: str) -> tuple[list[str | int], str]:
>         """Turn a string into a sortable value that works how humans expect.
>
>         "z23A" -> (["z", 23, "a"], "z23A")
>
>         The original string is appended as a last value to ensure the
>         key is unique enough so that "x1y" and "x001y" can be distinguished.
>
>         """
>         def try_int(s: str) -> str | int:
>             """If `s` is a number, return an int, else `s` unchanged."""
>             try:
>                 return int(s)
>             except ValueError:
>                 return s
>
>         return ([try_int(c) for c in re.split(r"(\d+)", s.casefold())], s)
>
>     def human_sort(strings: list[str]) -> None:
>         """Sort a list of strings how humans expect."""
>         strings.sort(key=human_key)
>
>
> The central idea here is to turn a string like `"Python 3.9"` into the key `["Python ", 3, ".", 9]` so that numeric components will be sorted by their numeric value. The re.split() function gives us interleaved words and numbers, and try_int() turns the numbers into actual numbers, giving us sortable key lists.
>