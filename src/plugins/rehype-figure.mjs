// Turns a paragraph that holds only an image into a figure with a visible
// caption. The docs' alt texts are already full-sentence captions, so the
// sentence moves into <figcaption> and the alt is emptied, so screen readers
// don't read it twice. Images with no alt text are left alone.

const isBlank = (node) => node.type === 'text' && node.value.trim() === '';

function loneImage(node) {
  if (node.type !== 'element' || node.tagName !== 'p') return null;
  const content = node.children.filter((child) => !isBlank(child));
  if (content.length !== 1) return null;
  const [img] = content;
  if (img.type !== 'element' || img.tagName !== 'img') return null;
  return img.properties.alt ? img : null;
}

function walk(parent) {
  parent.children = parent.children.map((node) => {
    const img = loneImage(node);
    if (img) {
      const caption = String(img.properties.alt);
      img.properties.alt = '';
      return {
        type: 'element',
        tagName: 'figure',
        properties: {},
        children: [img, { type: 'element', tagName: 'figcaption', properties: {}, children: [{ type: 'text', value: caption }] }],
      };
    }
    if (node.children) walk(node);
    return node;
  });
}

export default function rehypeFigure() {
  return (tree) => walk(tree);
}
