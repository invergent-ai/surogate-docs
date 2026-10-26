// Marks a page's opening paragraph as the lead (class "lead") when it is the
// first block and short enough to read as one: at most 250 characters by default.
// Longer openings stay at body size rather than running to seven large lines.
import { toString } from 'hast-util-to-string';

export default function rehypeLead({ maxLength = 250 } = {}) {
  return (tree) => {
    const first = tree.children.find((node) => node.type === 'element');
    if (!first || first.tagName !== 'p') return;
    if (toString(first).trim().length > maxLength) return;
    const existing = first.properties.className ?? [];
    first.properties.className = [...existing, 'lead'];
  };
}
