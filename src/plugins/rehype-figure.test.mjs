import assert from 'node:assert/strict';
import { test } from 'node:test';
import rehypeParse from 'rehype-parse';
import rehypeStringify from 'rehype-stringify';
import { unified } from 'unified';

import rehypeFigure from './rehype-figure.mjs';

const run = async (html) =>
  String(await unified().use(rehypeParse, { fragment: true }).use(rehypeFigure).use(rehypeStringify).process(html));

test('a lone image becomes a captioned figure', async () => {
  assert.equal(
    await run('<p><img src="a.png" alt="The Channels tab"></p>'),
    '<figure><img src="a.png" alt=""><figcaption>The Channels tab</figcaption></figure>',
  );
});

test('an image inside text is left alone', async () => {
  assert.equal(await run('<p>See <img src="a.png" alt="x"> here.</p>'), '<p>See <img src="a.png" alt="x"> here.</p>');
});
