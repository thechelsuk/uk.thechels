---

layout: post
syndicate: false
date: 2026-06-05 17:46
title: Cool down before you install as gems to be vetted
link: https://blog.rubygems.org/2026/06/03/cooldown-let-new-gems-be-vetted.html
cited: Ruby Gems
type: linked

---

Nice addition

> Most supply-chain attacks against RubyGems exploit a narrow window: an account is compromised, a malicious version ships, and any `bundle install` in the minutes that follow resolves straight to it. Bundler 4.0.13 introduces cooldown,  a time-based filter that refuses to resolve to a version until it has been public for at least _N_ days. Releases too new to have been scrutinized are passed over in favor of ones that have aged past the window.
> 
> The feature was designed in the open, drawing on how other ecosystems approach the same problem. It is opt-in, and complements rather than replaces existing defenses like mandatory 2FA and trusted publishing.