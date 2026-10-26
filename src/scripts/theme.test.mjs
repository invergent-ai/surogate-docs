import assert from 'node:assert/strict';
import { test } from 'node:test';

import { applyTheme, nextTheme } from './theme.mjs';

test('nextTheme flips', () => {
  assert.equal(nextTheme('light'), 'dark');
  assert.equal(nextTheme('dark'), 'light');
});

test('applyTheme sets the attribute and remembers the choice', () => {
  const doc = { documentElement: { dataset: {} } };
  const store = new Map();
  applyTheme('dark', doc, { setItem: (k, v) => store.set(k, v) });
  assert.equal(doc.documentElement.dataset.theme, 'dark');
  assert.equal(store.get('starlight-theme'), 'dark');
});
