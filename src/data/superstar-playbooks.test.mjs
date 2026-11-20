// The docs and Superstar's in-app Help show the same playbooks. A page that loses a step, a prompt or a fact
// from the catalogue fails here, and so does a playbook without a page.
import { test } from 'node:test';
import assert from 'node:assert/strict';
import { readFileSync } from 'node:fs';
import { PLAYBOOKS } from './superstar-playbooks.mjs';

const docs = new URL('../content/docs/superstar/', import.meta.url);
const read = (path) => readFileSync(new URL(path, docs), 'utf8');
const md = (html) => html.replace(/<b>(.*?)<\/b>/g, '**$1**');

test('every playbook has a page that carries its catalogue entry', () => {
  for (const p of PLAYBOOKS) {
    const page = read(`playbooks/${p.id}.mdx`);
    const missing = [p.lead, p.good, ...p.steps.flatMap(([t, h]) => [`**${t}**`, md(h)]), ...p.prompts, ...p.watch, ...p.measure]
      .filter((s) => !page.includes(s));
    assert.deepEqual(missing, [], p.id);
    assert.ok(page.includes(`<Tutorial id="${p.id}" />`), p.id);
  }
});

test('the prompt library has every prompt', () => {
  const page = read('prompts.mdx');
  assert.deepEqual(PLAYBOOKS.flatMap((p) => p.prompts).filter((s) => !page.includes(s)), []);
});

test('every next points at a playbook', () => {
  const ids = new Set(PLAYBOOKS.map((p) => p.id));
  assert.deepEqual(PLAYBOOKS.filter((p) => !ids.has(p.next)).map((p) => p.id), []);
});
