// The crew as the docs show it: the face each agent wears in Superstar (public/superstar/crew/<slug>.svg, taken from
// the app's own avatars) and its one-line job. `anchor` is its section on the crew page.
export const CREW = [
  ['Superstar', 'Answers anything you ask, does small jobs itself, hands bigger ones to the crew.', 'superstar'],
  ['Inbound qualifier', 'Researches each new lead, scores the fit, routes it and drafts the first reply.', 'inbound-qualifier'],
  ['Signal scout', 'Finds sourced reasons to write to an account now, and briefs you before a meeting.', 'signal-scout'],
  ['Relationships', 'Finds who can introduce you, and drafts the ask to that person.', 'relationships'],
  ['Follow-up keeper', "Turns call notes into the follow-up email and the deal's next step.", 'follow-up-keeper'],
  ['Strategist', "Reviews the pipeline and writes the week's plan.", 'strategist'],
  ['Content producer', 'Turns one source into posts, a newsletter section or an article.', 'content-producer'],
  ['Comment scout', 'Finds posts worth a real comment from you, and drafts it.', 'comment-scout'],
  ['Visual maker', 'Makes social cards, carousels and figures from real screenshots.', 'visual-maker-and-video-producer'],
  ['Video producer', 'Writes video briefs, scripts and cutdowns.', 'visual-maker-and-video-producer'],
  ['Publisher', 'Posts validated posts on your company profiles at their time. Nothing else.', 'publisher'],
].map(([name, job, anchor]) => ({ name, job, anchor, slug: name.toLowerCase().replace(/[^a-z]+/g, '-'), face: `/superstar/crew/${name.toLowerCase().replace(/[^a-z]+/g, '-')}.svg` }));

export const crewOf = (name) => CREW.find((c) => c.name === name);
