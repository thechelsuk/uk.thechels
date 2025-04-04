---

layout: post
date: 2025-04-04
link: https://github.com/michaelkeeling/mob-programming-patterns
title: Mob Programming Patterns
cited: Michael Keeling

---

Mob programming is an approach to creating software in which the whole team works together on the same thing at the same time. At the heart of every effective mob there is a group of people working from a place of mutual respect to deliver the best software they can, as fast as they are able. Effective mob programming comes about from effective communication among teammates. Naturally, interaction styles will vary greatly from team to team and situation to situation. As such, there is no "one way to do mob programming." This is where a robust patterns catalog can help.

A pattern is a repeatable solution that emerges in response to a specific problem in a particular context. You might think of a patterns catalog as a collection of tools in a toolbox. While you might use your trusty hammer often, selecting the right tool for the job can not only make work easier, but the final result even better. They key lays in knowing when to use a particular pattern and how to use it.

Mob programming is still a relatively young method. We’re all learning how to practice mob programming better. While we’ve found it to be a very powerful method, it does take some practice to do well. The goal of this repository is to capture the patterns we’ve discovered so far in the hopes that other teams might find them useful as a jumping off point for getting started with mob programming.

## Mob Programming Patterns

| Pattern | Category | Gist |
| --- | --- | ---  |
| Facilitator | Mob role | Volunteer who helps the group stay focused and to help resolve differences of opinion. Typically the driver does not take this role. |
| Recorder | Mob role | Volunteers who capture notes such as context or design decisions on behalf of the mob.  |
| Researcher | Mob role | Volunteers who seek out information in real-time that is required for the mob to move forward. |
| Navigator | Mob role | Direct the driver in what to do. Members of the mob not currently driving are assumed to be a navigator. Navigators can contribute to the mob in many ways. |
| Driver | Mob role | The person currently at the keyboard, capturing the thoughts of the navigators as everyone works to solve a particular problem. |
| Devil’s Advocate | Mob role | A navigator who takes a contrarian position to help make the mob’s designs stronger. |
| Punch List | Collaboration | A task list used by the mob to track work items and select what to work on next. Punch lists can be text-based or graphical. |
| Splinter Group | Collaboration | One or more members of the mob who break away from the main group to complete a routine task. Splinter groups can also investigate alternatives for review by the whole mob. |
| Ridin’ Shotgun | Collaboration | A navigator who solely dictates the mob’s work to the exclusion of other navigators. |
| Mute your mic | Collaboration | A navigator chooses to temporarily remain silent as a navigator to give other navigators a chance to contribute. Used as a way to kick start a slow mob or prevent one person from dominating the mob. |
| Fight Club | Collaboration | A situation in which two or more participants fight over the direction of the mob with total disregard for the guiding principles of mutual respect and consideration. Extremely harmful to the mob, considered an anti-pattern. |
| Natural Swap | Collaboration | A new driver takes the keyboard without prompting by either a member of the mob or timer at a "natural" break in the work, such as after a test passes or a refactoring step is completed. |
| Forced Swap | Collaboration | A new driver takes the keyboard after being prompted by either a member of the mob or a timer. |
| Distracted non-Participant | Collaboration | Navigators who are present in the mob but otherwise do not participate, perhaps distracted by other work. |
| Thinking Out Loud | Driving | The driver articulates their current thinking as they are the prevailing expert in the room or see the path forward. |
| Tell me what to write | Driving | A prompt drivers will sometimes use to engage help from navigators, inviting someone from the mob to direct the driver. |
| Driving on Autopilot | Driving | A driver who proceeds without inputs from the rest of the mob. |
| Plowing Through | Driving | A driver who, with the support of the mob, works on the task at hand with the intent of completing it as quickly and painlessly as possible. Often combined with the thinking out loud pattern. |
