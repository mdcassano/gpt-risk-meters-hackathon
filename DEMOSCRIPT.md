Hello, this is the demo submission for team "Where we are going, we need AI".

The team consists of Michael Cassano, Ahbishek Ahbishek, Jason Garber and Vladimir Maslo.

We integrated GPT-4 into Cisco Vulnerability Management to simplify how users create and explain asset searches.  This leads to a better user experience and transforms sales demos into an impressive displays of innovation.

Let me show you how it works.

This is the Explore screen of our product, customers use it to construct and save groups of assets called asset searches.  For new users, creating an asset search is problematic due to the difficult syntax.  Our improvement solves this.

- Show the plain english to syntax

In addition to making it easier to create asset searches.  We have leveraged our prompting to offer plain english explanations of existing asset searches.  Users can now revisit existing syntax and have it explained to them in plain english instead of having to comb through the technicalities.

- Paste in a difficult syntax

We created this capability by explaining our product in a robust prompt for use in GPT-4.  We then built a microservice that makes synchronous calls to Azure's OpenAI API.  We then wired the new microservice into the user interface of our existing web system.  We built a testing harness to ensure that tweaks make to the AI prompts did not result in breaking changes in the AI responses.

With GPT-4 we were able to rapidly prototype our ideas and spend the majority of our time engineering the user experience and expanding the prompt for our use case.

- Show the Github link and the base prompt

We can provide access to the Github repository where all the technical details can be found.

Thank you for watching our demo submission.
