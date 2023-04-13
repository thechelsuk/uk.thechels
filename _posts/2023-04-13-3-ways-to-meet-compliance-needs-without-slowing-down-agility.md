---

layout: post
date: 2023-04-13
link: https://github.blog/2023-02-24-3-ways-to-meet-compliance-needs-without-slowing-down-agility/
title: 3 ways to meet compliance needs without slowing down agility
cited: The GitHub Blog

---

> - You can [configure SAML single sign-on for your enterprise](https://docs.github.com/en/enterprise-cloud@latest/admin/identity-and-access-management/using-saml-for-enterprise-iam/configuring-saml-single-sign-on-for-your-enterprise). This is an additional check, allowing you to confirm the authenticity of your users against your own identity provider (while still using your own GitHub account).
> - You can then [synchronize team memberships](https://docs.github.com/en/enterprise-cloud@latest/organizations/organizing-members-into-teams/synchronizing-a-team-with-an-identity-provider-group) with groups in your identity provider. As a result, group membership changes in your identity provider update the team membership (and therefore associated access) in GitHub.
> - Alternatively, you could adopt GitHub [Enterprise Managed Users](https://docs.github.com/en/enterprise-cloud@latest/admin/identity-and-access-management/using-enterprise-managed-users-for-iam/about-enterprise-managed-users) (EMUs). This is a flavor of GitHub Enterprise where you can only log in with an account that is centrally managed through your identity provider. The user does not have to log in to GitHub with a personal account and use single sign on to access company resources. (For more information on this, check out [this blog post](https://github.blog/2022-12-20-emus-more-than-just-flightless-birds/) on exploring EMUs and the benefits they can bring.)