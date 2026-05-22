import React, {useEffect, useState} from 'react';
import {useLocation, useHistory} from '@docusaurus/router';
import clsx from 'clsx';
import styles from './styles.module.css';

/**
 * Pill-style Work / Develop toggle for the navbar. Mirrors the toggle in
 * ops.surogate.ai. Clicking switches to the equivalent page in the other
 * mode (mapped explicitly below); falls back to that mode's intro page
 * when no equivalent exists.
 *
 * Only renders when the user is inside a /work/* or /develop/* route.
 */
const EQUIVALENCE = {
  // Work → Develop
  '/work': '/develop',
  '/work/quickstart': '/develop/quickstart',
  '/work/workflow/run-agent': '/develop/loop/build',
  '/work/workflow/review-sessions': '/develop/loop/observe',
  '/work/workflow/improve-agent': '/develop/loop/train',
  '/work/library/skills': '/develop/features/skills-and-experts',
  '/work/library/knowledge-bases': '/develop/features/knowledge-bases',
  '/work/library/mcp-servers': '/develop/features/mcp-and-vault',
  '/work/channels/web': '/develop/features/agents',
  '/work/channels/slack': '/develop/features/agents',
  '/work/channels/telegram': '/develop/features/agents',
  '/work/channels/website-widget': '/develop/features/agents',
  '/work/channels/users': '/develop/features/agents',
  '/work/tools/goals': '/develop/loop/observe',
  '/work/tools/copilot': '/develop/tools/copilot',
  '/work/tools/inbox': '/develop/features/sessions',
  '/work/settings/profile': '/develop/settings/profile',
  '/work/settings/usage': '/develop/settings/usage',
  '/work/settings/billing': '/develop/settings/billing',
  '/work/use-cases': '/develop/use-cases',
  '/work/reference/glossary': '/develop/reference/glossary',
  '/work/reference/faq': '/develop',

  // Develop → Work
  '/develop': '/work',
  '/develop/quickstart': '/work/quickstart',
  '/develop/loop/overview': '/work/workflow/run-agent',
  '/develop/loop/build': '/work/workflow/run-agent',
  '/develop/loop/observe': '/work/workflow/review-sessions',
  '/develop/loop/train': '/work/workflow/improve-agent',
  '/develop/loop/redeploy': '/work/workflow/improve-agent',
  '/develop/features/agents': '/work/workflow/run-agent',
  '/develop/features/sessions': '/work/workflow/review-sessions',
  '/develop/features/compute': '/work',
  '/develop/features/models': '/work/library/skills',
  '/develop/features/skills-and-experts': '/work/library/skills',
  '/develop/features/knowledge-bases': '/work/library/knowledge-bases',
  '/develop/features/mcp-and-vault': '/work/library/mcp-servers',
  '/develop/features/hub': '/work/library/skills',
  '/develop/features/datasets': '/work/library/knowledge-bases',
  '/develop/features/training': '/work',
  '/develop/features/evaluations': '/work',
  '/develop/tools/dashboard': '/work',
  '/develop/tools/copilot': '/work/tools/copilot',
  '/develop/tools/templates': '/work/workflow/run-agent',
  '/develop/features/byo-llm': '/work/settings/billing',
  '/develop/use-cases': '/work/use-cases',
  '/develop/reference/runtime-architecture': '/work',
  '/develop/reference/tool-catalog': '/work/library/skills',
  '/develop/reference/event-types': '/work/workflow/review-sessions',
  '/develop/reference/glossary': '/work/reference/glossary',
};

const STORAGE_KEY = 'surogate-docs-mode';

function detectMode(pathname) {
  if (pathname.startsWith('/work')) return 'work';
  if (pathname.startsWith('/develop')) return 'develop';
  return null;
}

function targetFor(pathname, switchTo) {
  // 1) Explicit map
  const explicit = EQUIVALENCE[pathname.replace(/\/$/, '')];
  if (explicit) return explicit;

  // 2) Same-path swap
  const swapped =
    switchTo === 'work'
      ? pathname.replace(/^\/develop/, '/work')
      : pathname.replace(/^\/work/, '/develop');
  if (swapped !== pathname) return swapped;

  // 3) Fall back to mode intro
  return switchTo === 'work' ? '/work' : '/develop';
}

export default function ModeToggle() {
  const location = useLocation();
  const history = useHistory();
  const [mode, setMode] = useState('work');

  useEffect(() => {
    const detected = detectMode(location.pathname);
    if (detected) {
      setMode(detected);
      try {
        window.localStorage.setItem(STORAGE_KEY, detected);
      } catch {
        /* ignore localStorage errors */
      }
    }
  }, [location.pathname]);

  // Hide the toggle on routes that aren't part of either docs track
  // (e.g. legacy training-framework pages or the homepage).
  const inDocsTrack = detectMode(location.pathname) !== null;
  if (!inDocsTrack) return null;

  const click = (target) => {
    if (target === mode) return;
    history.push(targetFor(location.pathname, target));
  };

  return (
    <div className={styles.toggle} role="group" aria-label="Documentation mode">
      <button
        type="button"
        className={clsx(styles.option, mode === 'work' && styles.active)}
        onClick={() => click('work')}
        aria-pressed={mode === 'work'}
      >
        Work
      </button>
      <button
        type="button"
        className={clsx(styles.option, mode === 'develop' && styles.active)}
        onClick={() => click('develop')}
        aria-pressed={mode === 'develop'}
      >
        Develop
      </button>
    </div>
  );
}
