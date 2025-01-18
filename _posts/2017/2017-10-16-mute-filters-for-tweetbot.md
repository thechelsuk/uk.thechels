---
layout: post
title : Mute filters for Tweetbot
tags:
  - other
---

A bunch of regexes for muting on TweetBot, the popular iOS/Mac twitter app.
It is recommended you test regexes with some tweet text (TweetBot lets you copy a tweet’s text) so paste it on regexr.com The TweetBot app also shows you how many tweets are returned from your timeline for said regex, check these!

##### Check-ins, social sites user requests etc

+ `(?i)checked.*in` - I checked in at...
+ `LinkedIn` - Linked In
+ `(?i)please.*(\bwatch\b|\bfollow\b)|(\bwatch\b|\bfollow\b).*(me|please|back)` - Follow me, watch me, follow back, watch me please, follow me please etc
+  `( RT -|LIKE -)` - people stil use these instead of proper polls.
+  `I.liked.a.@YouTube.video` - youtube etc

##### Irritants 

+ `#(([D|d]arts\w*)|([A|a]shes\w*))|([B|b]oxing\w*))` — Sports I don’t care for
+ `go again` - Gerrard said this once, now everyone does. irritating as f*ck
+ `(#NW)|(#Now[W|w]atching)|(#NP)|(#Now[P|p]laying)` - now playing/watching

##### Celebs 

+ `([B|b]ieber)|([B|b]ieb)` — Filter all references to the word Bieber
+ `\b([B|b]eckham)\b` — Filter all references to the word Beckham
+ `([K|k]atie [H|h]opkins)` - Filter all reference to the rent a troll.
+ `([D|d]onald [T|t]rump)|[T|t]rump` - Donald Trump’s a c***


##### Media
+ `[D|d]aily [M|m|F|f]ail?|Mail Online|dailym.ai|dailymail.co.uk|[M|m]ail[S|s]port` - Daily Mail/Fail
+ `#[A|a]sk\w*` - Any Ask [celeb] 
+ `([X|x] [F|f]actor|[X|x][F|f]actor|#x[F|f]actor)` - x factor
+ `#[E|e]urovision\w*` - Eurovision
+ `#FIFA\w*` - Fifa (including the game)
+ `#GBBO\w*` - Great British Bake Off
+ `#BakeOff\w*` - Great British Bake Off
+ `#BAFTA\w*` - Bafta
+ `#BGT\w*` - Britains Got Talent
+ `#BBC\w*` - BBC hashtag
+ `#ImACeleb` - z list shithousery
+ `#[H|h]omeland` - TV show i don’t watch
+  `(#[T|t]he[A|a]pprentice)|(#[A|a]pprentice)` - Apprentice obvs.
+ `#[B|b]allon\w*` - Ballon d’or
+ `#(Glasto|GLASTO|glasto)\w*` - Glastonbury
+ `#ssnhq\w*` - Sky Sports News Hashtags
+ `#[V|v]ote\w*` - Vote hashtags

##### Format

+ `^[A-Z\s\p{P}]*$` - tweets in all caps
+ `\n{6,}` — Posts with 6+ new lines.
+ `(#.*?){6,}` — Posts with 6+ hastags.
+ `#\w{24,}` — Posts that contain long hashtags.
+ `(@.*){5}` - mute all tweets containing more than 5 @ mentions.
+ `^((#|@)\S+\s*)+$` - Tweets consisting solely of @usernames and #hashtags, separated by whitespace

##### Accounts

+ `[P|p]redict[T|t]he[S|s]ix` - some people i follow promote these, but i don’t really care
+ `[C|c]helsea[F|f]ansYT` - some people i follow promote these, but i don’t really care
+ `[B|b]reath[S|s]port` - some people i follow write for these but i don’t really care.
+ `[B|b]reathe[S|s]port` - some people i follow write for these but i don’t really care.
+ `[G|g]et[W|w]est[C|c]helsea` - some people i follow write for these but i don’t really care.
+ `uMAXitFootball` - some people i follow write for these but i don’t really care.

##### Apps (mute clients)

+ SumAll
+ SumAll Authentication
+ Twitter Ads
+ Unfollowers
+ Unfollowers.me
+ Untappd
+ LinkedIn
+ JustUnfollow
+ Foursquare
+ fllwrs
+ Deezer
+ BreatheSport
+ Bloglovin
+ Twibbon
+ Kicca (Syndicate)
+ SnappyTV.com
+ SoundCloud
+ Facebook
+ Crowdfire App
