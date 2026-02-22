---

layout: post
date: 2026-02-22
link: https://www.malwarebytes.com/blog/news/2026/02/age-verification-vendor-persona-left-frontend-exposed
title: Age verification vendor Persona left frontend exposed
cited: Malwarebytes

---

Oops

> Researchers investigating Discord's age-verification checks [say they discovered](https://www.therage.co/persona-age-verification/) an exposed frontend belonging to Persona, the identity-verification vendor used by Discord. It revealed a far more expansive surveillance and financial intelligence stack than a simple "teen safety" tool. 
> 
> A short while ago we reported that [Discord will limit profiles to teen-appropriate mode until you verify your age](https://www.malwarebytes.com/blog/news/2026/02/discord-will-limit-profiles-to-teen-appropriate-mode-until-you-verify-your-age). That means anyone would wants to continue using Discord as before would have to let it scan their face--and the internet was far from happy.
> 
> To analyze these scans, Discord uses biometric identity verification start-up Persona Identities, Inc. a venture that offers Know Your Customer (KYC) and Anti-Money Laundering (AML) solutions that rely on biometric identity checks to estimate a user's age.
> 
> To demonstrate the privacy implications, researchers [took a closer look](https://cybernews.com/privacy/persona-leak-exposes-global-surveillance-capabilities/) and found a publicly exposed Persona frontend on a US government--authorized server, with 2,456 accessible files.
> You read that right. According to researcher "Celeste" the exposed code, which has now been removed, sat at a US government-authorized endpoint that appears to have been isolated from its regular work environment.
> 
> In those files, the researchers found details about the extensive surveillance Persona software performs on its users. Beyond checking their age, the software performs 269 distinct verification checks, runs facial recognition against watchlists and politically exposed persons, screens "adverse media" across 14 categories (including terrorism and espionage), and assigns risk and similarity scores.