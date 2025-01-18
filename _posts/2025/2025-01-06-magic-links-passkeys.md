---

layout: post
date: 2025-01-06
link: https://rmondello.com/2025/01/02/magic-links-and-passkeys/
title: Magic Links and Passkeys
cited: Ricky Mondello

---

A well-written post by [Ricky Mondello](https://www.linkedin.com/in/rmondello/) highlights their expertise in the password and authentication space.

The blog post on 404 media login flow is intriguing. As a strong advocate for password managers, I utilize Passkeys whenever available. However, I find it irritating and cringy that numerous essential services, such as a workplace pension provider, utilities, and other 'must-have, cannot be easily changed' services (e.g., Council Tax), still rely on SMS codes, lack autofill capabilities, or impose severely limited password lengths. For instance, Virgin Media's 20-character limit persists after at least 15 years.

Incidentally, Virgin Media's character limit strongly suggests that they do not hash and salt passwords, effectively storing them in plain text in a database. This practice is inherently insecure. Fortunately, I have finally ended my Virgin Media usage and adopted sensible practices such as avoiding duplicate passwords across all platforms.

My preferred authentication flow is autofilling a passkey, followed by autofilling the username and password for sites without passkey support. Applications like 1Password facilitate this process effortlessly. While magic links can be inconvenient, particularly due to the tendency to forget during the flow, as sites sometimes default to a password and it then involves a click and another autofill of an email address, and then one can encounter a slight delay and context switch while accessing email clients, which are often distracting due to unread emails.

On Apple devices, automatic prompts for code completion via SMS and email are provided, eliminating the need for magic links. This approach allows users to wait for the prompt and use it within the current app or website, minimizing distractions. Apple also offers the option to automatically delete access code emails, ensuring a seamless user experience. - I'd suggest the autofill code and the hash on magic links become one and we call them Magic Codes (keeping the simple and more user friendly 6 character string - think how GitHub show's just the first 6 characters on a commit visually)

> For the purpose of improving a passwordless authentication strategy using magic links, what's important to remember is that passkeys suffer from none of the security problems that passwords have, and that signing in with passkeys is super fast, keeps users in their context, and never requires switching over to another app.