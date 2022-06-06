---

layout: post
date: 2022-06-06
link: https://paperless.blog/start-test-names-with-should
title: Start test names with should
cited: paperless

---

I like this, I'd name my tests `function_` first to identify and sort when executing - this view really helps me view test cases and look for gaps.

E.g.,  `add_should_return_sum_of_values`


> A trick I learned from Dave Hounslow, a former colleague, is to start test names with “should”¹. This has a few advantages over test [function name]:
> It removes redundancy, because the function name should already be in the call stack.
> It is falsifiable, that is, a person reviewing the test can decide to which degree the name agrees with the actual test. For example, they could point out that should replace children when updating instance verifies that new children are added, but not that old children are removed.
> It encourages testing one property of the function per test, like should apply discount when total cost exceeds 100 dollars, should create record for valid input, and should return error code 1 for unknown error. test [function name] encourages testing everything the function does (branches, side effects, error conditions, etc.) in one test. 
> It invites the developer to write something human readable. I usually find “test …” names to be clunky to read. This may just be bias after years of using this technique. 
> It is better than a comment explaining what the test does, because the comment will not be shown when the test fails.