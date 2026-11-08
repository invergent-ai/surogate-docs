// Which product and track a docs page belongs to, from its Starlight route id
// ('work', 'work/channels/slack', 'keel/builder/rules', '' for the home page).

export const PRODUCT_LABEL = { agents: 'Surogate Agents', keel: 'Surogate Keel', dms: 'Surogate DMS', portal: 'Surogate Portal' };
export const PRODUCT_HOME = { agents: '/work/', keel: '/keel/', dms: '/dms/', portal: '/portal/' };
export const TRACK_LABEL = { work: 'Work', develop: 'Develop', keel: 'Surogate Keel', dms: 'Surogate DMS', portal: 'Surogate Portal' };
export const TRACK_HOME = { work: '/work/', develop: '/develop/', keel: '/keel/', dms: '/dms/', portal: '/portal/' };

/** @returns {'work' | 'develop' | 'keel' | 'dms' | 'portal' | null} */
export function trackFor(id) {
  const first = id.split('/')[0];
  return first in TRACK_LABEL ? first : null;
}

/** @returns {'agents' | 'keel' | 'dms' | 'portal' | null} */
export function productFor(id) {
  const track = trackFor(id);
  if (track === null) return null;
  if (track === 'keel') return 'keel';
  if (track === 'dms') return 'dms';
  if (track === 'portal') return 'portal';
  return 'agents';
}
