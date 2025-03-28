---

layout: post
date: 2025-03-28
title: Missing Vowels

---

One from the archives, I used to run a twitter bot that would tweet a footballer's name with the vowels, spaces and hyphens removed and then tweet the answer a few minutes later.

The bit of python to do this  was

```python
stripped = str.maketrans(dict.fromkeys('aeiouAEIOU -'))
hidden_name = name.translate(stripped)
```

Here's also a handy method for making an anagram of a string

```python
 def get_anagram_of_string(name):
  letters = list(name)
   random.shuffle(letters)
   return ''.join(letters)
```