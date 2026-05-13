import MDXComponents from "@theme-original/MDXComponents";
import Figure from "@site/src/components/Figure";

// Make <Figure> available in every .md / .mdx page without per-page imports.
export default {
  ...MDXComponents,
  Figure,
};
