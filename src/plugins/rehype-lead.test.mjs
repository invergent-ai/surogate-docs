import assert from 'node:assert/strict';
import { test } from 'node:test';
import rehypeParse from 'rehype-parse';
import rehypeStringify from 'rehype-stringify';
import { unified } from 'unified';

import rehypeLead from './rehype-lead.mjs';

const run = async (html) =>
  String(await unified().use(rehypeParse, { fragment: true }).use(rehypeLead).use(rehypeStringify).process(html));

test('short first paragraph is the lead', async () => {
  assert.equal(await run('<p>Short opening.</p><p>Next.</p>'), '<p class="lead">Short opening.</p><p>Next.</p>');
});

test('250 characters is still a lead, 251 is not', async () => {
  assert.match(await run(`<p>${'a'.repeat(250)}</p>`), /class="lead"/);
  assert.doesNotMatch(await run(`<p>${'a'.repeat(251)}</p>`), /class="lead"/);
});

test('a heading first means no lead', async () => {
  assert.doesNotMatch(await run('<h2>Title</h2><p>Text.</p>'), /lead/);
});
