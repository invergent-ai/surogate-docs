// The theme switch: flip between light and dark and remember the choice under
// Starlight's own key, so its ThemeProvider applies it on the next page. With
// nothing stored, Starlight follows the operating system.

export const STORAGE_KEY = 'starlight-theme';

/** @param {'light' | 'dark'} current */
export function nextTheme(current) {
  return current === 'dark' ? 'light' : 'dark';
}

/** @param {'light' | 'dark'} theme */
export function applyTheme(theme, doc = document, storage = localStorage) {
  doc.documentElement.dataset.theme = theme;
  try {
    storage.setItem(STORAGE_KEY, theme);
  } catch {
    // Storage can be blocked; the theme still applies to this page.
  }
}
