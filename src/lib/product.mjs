// Which product and track a docs page belongs to, from its Starlight route id
// ('work', 'work/channels/slack', 'keel/builder/rules', '' for the home page).

export const PRODUCT_LABEL = { agents: 'Surogate Agents', keel: 'Keel', dms: 'Surogate DMS' };
export const PRODUCT_HOME = { agents: '/work/', keel: '/keel/', dms: '/dms/' };
export const TRACK_LABEL = { work: 'Work', develop: 'Develop', keel: 'Keel', dms: 'Surogate DMS' };
export const TRACK_HOME = { work: '/work/', develop: '/develop/', keel: '/keel/', dms: '/dms/' };

/** @returns {'work' | 'develop' | 'keel' | 'dms' | null} */
export function trackFor(id) {
  const first = id.split('/')[0];
  return first in TRACK_LABEL ? first : null;
}

/** @returns {'agents' | 'keel' | 'dms' | null} */
export function productFor(id) {
  const track = trackFor(id);
  if (track === null) return null;
  if (track === 'keel') return 'keel';
  if (track === 'dms') return 'dms';
  return 'agents';
}
