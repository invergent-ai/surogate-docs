import assert from 'node:assert/strict';
import { test } from 'node:test';

import { productFor, trackFor } from './product.mjs';

test('tracks', () => {
  assert.equal(trackFor('work'), 'work');
  assert.equal(trackFor('work/channels/slack'), 'work');
  assert.equal(trackFor('develop/features/training'), 'develop');
  assert.equal(trackFor('keel/builder/rules'), 'keel');
  assert.equal(trackFor(''), null);
  assert.equal(trackFor('workshop'), null);
});

test('products', () => {
  assert.equal(productFor('develop'), 'agents');
  assert.equal(productFor('keel'), 'keel');
  assert.equal(productFor(''), null);
});

test('dms', () => {
  assert.equal(trackFor('dms'), 'dms');
  assert.equal(trackFor('dms/admin/people'), 'dms');
  assert.equal(trackFor('dmsx'), null);
  assert.equal(productFor('dms'), 'dms');
  assert.equal(productFor('dms/work/search'), 'dms');
});
