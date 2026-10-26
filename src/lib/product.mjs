// Which product and track a docs page belongs to, from its Starlight route id
// ('work', 'work/channels/slack', 'keel/builder/rules', '' for the home page).

export const PRODUCT_LABEL = { agents: 'Surogate Agents', keel: 'Keel' };
export const PRODUCT_HOME = { agents: '/work/', keel: '/keel/' };
export const TRACK_LABEL = { work: 'Work', develop: 'Develop', keel: 'Keel' };
export const TRACK_HOME = { work: '/work/', develop: '/develop/', keel: '/keel/' };

/** @returns {'work' | 'develop' | 'keel' | null} */
export function trackFor(id) {
  const first = id.split('/')[0];
  return first in TRACK_LABEL ? first : null;
}

/** @returns {'agents' | 'keel' | null} */
export function productFor(id) {
  const track = trackFor(id);
  if (track === null) return null;
  return track === 'keel' ? 'keel' : 'agents';
}
