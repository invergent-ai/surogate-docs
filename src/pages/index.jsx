import React from 'react';
import Layout from '@theme/Layout';
import Link from '@docusaurus/Link';
import useDocusaurusContext from '@docusaurus/useDocusaurusContext';
import Figure from '@site/src/components/Figure';

export default function Home() {
  const {siteConfig} = useDocusaurusContext();
  return (
    <Layout
      title="Surogate Documentation"
      description="Two documentation tracks for Surogate Ops — Work mode for operators, Develop mode for builders."
    >
      <main style={{padding: '3rem 1.5rem', maxWidth: 960, margin: '0 auto'}}>
        <h1 style={{fontSize: '2.6rem', letterSpacing: '-0.03em', marginBottom: '0.5rem'}}>
          Surogate documentation
        </h1>
        <p style={{fontSize: '1.15rem', color: 'var(--ifm-color-emphasis-700)', marginTop: 0}}>
          Two documentation tracks — one for <strong>operators</strong> who run agents day-to-day,
          one for <strong>builders</strong> who design and train them. Pick the one that fits how
          you'll use the platform; toggle between them at any time using the pill in the navbar.
        </p>

        <div className="hero-cta-grid" style={modeGridStyle}>
          <Link className="hero-cta-card" style={modeCardStyle} to="/work">
            <h3 style={modeCardHeader}>Work mode</h3>
            <p style={modeCardBody}>
              You sign in, use existing agents, watch sessions, and improve from real traffic.
              Plain-language workflow guides, no code, no infrastructure.
            </p>
            <p style={modeCardLink}>Start at the workflow →</p>
          </Link>
          <Link className="hero-cta-card" style={modeCardStyle} to="/develop">
            <h3 style={modeCardHeader}>Develop mode</h3>
            <p style={modeCardBody}>
              You design agents, write skills, attach knowledge bases, train experts, run
              evaluations, ship to channels. Deep configuration, code snippets, runtime internals.
            </p>
            <p style={modeCardLink}>Start at the builder loop →</p>
          </Link>
        </div>

        <h2>What is Surogate?</h2>
        <p>
          Surogate is a hosted platform for building, deploying, and improving autonomous AI agents.
          You don't manage Kubernetes, model serving, policy enforcement, or the LLM loop yourself
          — the platform handles the runtime so you focus on what the agent does.
        </p>

        <p>The platform is built on three open-source components:</p>
        <ul>
          <li>
            <a href="https://github.com/invergent-ai/surogates"><b>surogates</b></a>{' '}
            — the agent runtime (harness, sessions, sandbox, governance, MCP integration)
          </li>
          <li>
            <a href="https://github.com/invergent-ai/surogate-ops"><b>surogate-ops</b></a>{' '}
            — the operator platform (the UI, billing, hub, training pipeline)
          </li>
          <li>
            <a href="https://github.com/invergent-ai/surogate-hub"><b>surogate-hub</b></a>{' '}
            — the lakeFS-backed artifact versioning store
          </li>
        </ul>

        <h2>Which mode is right for you?</h2>
        <table>
          <thead>
            <tr>
              <th>If you...</th>
              <th>Use</th>
            </tr>
          </thead>
          <tbody>
            <tr>
              <td>Chat with deployed agents, configure them in a UI, review sessions</td>
              <td><Link to="/work">Work mode</Link></td>
            </tr>
            <tr>
              <td>Manage skills, knowledge bases, channels, billing for your team</td>
              <td><Link to="/work">Work mode</Link></td>
            </tr>
            <tr>
              <td>Design new agents, write skills, configure tools / governance</td>
              <td><Link to="/develop">Develop mode</Link></td>
            </tr>
            <tr>
              <td>Train experts, run evaluations, integrate via the REST API</td>
              <td><Link to="/develop">Develop mode</Link></td>
            </tr>
            <tr>
              <td>Deploy on your own cluster, customize the runtime</td>
              <td><Link to="/develop">Develop mode</Link></td>
            </tr>
          </tbody>
        </table>

        <p style={{marginTop: '2.5rem', color: 'var(--ifm-color-emphasis-600)', fontSize: '0.9rem'}}>
          Looking for the training framework (<em>Surogate Trainer</em>)?{' '}
          <Link to="/old-docs">The legacy training documentation</Link> covers pretraining, SFT,
          GRPO, MoE, multi-GPU, and the C++/CUDA engine.
        </p>
      </main>
    </Layout>
  );
}

const modeGridStyle = {
  display: 'grid',
  gridTemplateColumns: '1fr 1fr',
  gap: '1.25rem',
  margin: '2rem 0',
};

const modeCardStyle = {
  display: 'block',
  padding: '1.5rem',
  borderRadius: '10px',
  border: '1px solid var(--ifm-color-emphasis-300)',
  background: 'var(--ifm-background-surface-color)',
  textDecoration: 'none',
  color: 'inherit',
  transition: 'transform 120ms ease-out, box-shadow 120ms ease-out',
};

const modeCardHeader = {
  margin: '0 0 0.5rem',
  color: 'var(--ifm-color-primary)',
  fontSize: '1.4rem',
};

const modeCardBody = {
  margin: 0,
  color: 'var(--ifm-color-emphasis-700)',
};

const modeCardLink = {
  margin: '0.75rem 0 0',
  fontWeight: 600,
  color: 'var(--ifm-color-primary)',
};
