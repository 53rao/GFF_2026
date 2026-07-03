import type { Metadata } from 'next';
import { agentStatuses } from '@/lib/mock-data';

export const metadata: Metadata = {
  title: 'Agent Pipeline',
  description: 'SBI Operations — Multi-agent pipeline status and performance monitoring.',
};

export default function AgentsPage() {
  const active  = agentStatuses.filter((a) => a.status === 'active');
  const idle    = agentStatuses.filter((a) => a.status === 'idle');
  const offline = agentStatuses.filter((a) => a.status === 'offline');

  return (
    <>
      <div className="admin-topbar">
        <div>
          <h1 className="admin-topbar__heading">Agent Pipeline</h1>
          <p className="admin-topbar__sub">
            {active.length} active · {idle.length} idle · {offline.length} offline
          </p>
        </div>
        <div style={{ display: 'flex', gap: 'var(--space-3)' }}>
          <button className="btn btn--ghost" id="agents-logs-btn" style={{ fontSize: 'var(--text-sm)' }}>View Logs</button>
          <button className="btn btn--primary" id="agents-deploy-btn" style={{ fontSize: 'var(--text-sm)' }}>Deploy Agent</button>
        </div>
      </div>

      {/* System Health Bar */}
      <div style={{
        background: 'var(--color-surface)', border: '1px solid var(--color-border-light)',
        borderRadius: 'var(--radius-card)', padding: 'var(--space-4) var(--space-6)',
        marginBottom: 'var(--space-5)', display: 'flex', alignItems: 'center', gap: 'var(--space-8)',
        boxShadow: 'var(--shadow-xs)',
      }}>
        <div style={{ display: 'flex', alignItems: 'center', gap: 'var(--space-2)' }}>
          <div style={{ width: 10, height: 10, borderRadius: '50%', background: 'var(--color-success)' }} />
          <span style={{ fontSize: 'var(--text-sm)', fontWeight: 700, color: 'var(--color-text-primary)' }}>
            System Healthy
          </span>
        </div>
        {[
          { label: 'Orchestrator Uptime', value: '99.97%' },
          { label: 'Avg Latency', value: '394ms' },
          { label: 'Messages/min', value: '142' },
          { label: 'Queue Depth', value: '7' },
          { label: 'Last Deploy', value: '2h ago' },
        ].map(({ label, value }) => (
          <div key={label}>
            <div style={{ fontSize: 'var(--text-xs)', color: 'var(--color-text-secondary)' }}>{label}</div>
            <div style={{ fontSize: 'var(--text-sm)', fontWeight: 700, color: 'var(--color-text-primary)' }}>{value}</div>
          </div>
        ))}
      </div>

      {/* Agent Cards */}
      <h2 style={{ fontSize: 'var(--text-sm)', fontWeight: 700, color: 'var(--color-text-secondary)', textTransform: 'uppercase', letterSpacing: '0.06em', marginBottom: 'var(--space-4)' }}>
        Agents — {agentStatuses.length} deployed
      </h2>

      <div className="agent-grid">
        {agentStatuses.map((agent) => (
          <div key={agent.id} className="agent-card">
            <div className="agent-card__header">
              <div>
                <div className="agent-card__name">{agent.name}</div>
                <div className="agent-card__type">{agent.type}</div>
              </div>
              <div style={{ display: 'flex', flexDirection: 'column', alignItems: 'flex-end', gap: 4 }}>
                <div className={`agent-status-dot agent-status-dot--${agent.status}`} />
                <span className={`badge ${agent.status === 'active' ? 'badge--green' : agent.status === 'idle' ? 'badge--yellow' : 'badge--gray'}`}>
                  {agent.status.charAt(0).toUpperCase() + agent.status.slice(1)}
                </span>
              </div>
            </div>

            <div className="agent-card__stats">
              <div>
                <div className="agent-card__stat-label">Active Cases</div>
                <div className="agent-card__stat-value">{agent.casesActive}</div>
              </div>
              <div>
                <div className="agent-card__stat-label">Resolved</div>
                <div className="agent-card__stat-value">{agent.casesResolved}</div>
              </div>
              <div>
                <div className="agent-card__stat-label">Success Rate</div>
                <div className="agent-card__stat-value" style={{ color: agent.successRate >= 95 ? 'var(--color-success)' : 'var(--color-warning)' }}>
                  {agent.successRate}%
                </div>
              </div>
              <div>
                <div className="agent-card__stat-label">Avg Response</div>
                <div className="agent-card__stat-value">{agent.avgResponseMs}ms</div>
              </div>
            </div>

            {/* Utilization */}
            <div style={{ marginBottom: 'var(--space-3)' }}>
              <div style={{ display: 'flex', justifyContent: 'space-between', marginBottom: 'var(--space-1)' }}>
                <span style={{ fontSize: 'var(--text-xs)', color: 'var(--color-text-secondary)' }}>Utilization</span>
                <span style={{ fontSize: 'var(--text-xs)', fontWeight: 700, color: 'var(--color-text-primary)' }}>{agent.utilization}%</span>
              </div>
              <div className="agent-card__progress">
                <div
                  className="agent-card__progress-fill"
                  style={{ width: `${agent.utilization}%` }}
                  role="progressbar"
                  aria-valuenow={agent.utilization}
                  aria-valuemin={0}
                  aria-valuemax={100}
                  aria-label={`${agent.name} utilization`}
                />
              </div>
            </div>

            <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center' }}>
              <span style={{ fontSize: 'var(--text-xs)', color: 'var(--color-text-tertiary)' }}>
                Last ping: {agent.lastPing}
              </span>
              <div style={{ display: 'flex', gap: 'var(--space-2)' }}>
                <button
                  className="btn btn--ghost"
                  id={`agent-logs-${agent.id}`}
                  style={{ fontSize: 'var(--text-xs)', padding: '3px 8px' }}
                >
                  Logs
                </button>
                <button
                  className="btn btn--outline"
                  id={`agent-detail-${agent.id}`}
                  style={{ fontSize: 'var(--text-xs)', padding: '3px 8px' }}
                >
                  Details
                </button>
              </div>
            </div>
          </div>
        ))}
      </div>

      {/* Pipeline Flow Diagram (static illustration) */}
      <div className="admin-table-container" style={{ padding: 'var(--space-5)' }}>
        <h3 style={{ fontSize: 'var(--text-sm)', fontWeight: 700, marginBottom: 'var(--space-4)', color: 'var(--color-text-primary)' }}>
          Agent Message Flow (Schematic)
        </h3>
        <div style={{
          display: 'flex', alignItems: 'center', gap: 'var(--space-3)',
          flexWrap: 'wrap', justifyContent: 'center', padding: 'var(--space-4)',
        }}>
          {[
            { name: 'Customer Event', color: 'var(--color-primary-pale)', textColor: 'var(--color-primary-dark)' },
            { name: '→', color: 'transparent', textColor: 'var(--color-text-tertiary)' },
            { name: 'Orchestrator', color: 'hsl(210 72% 38%)', textColor: 'white' },
            { name: '→', color: 'transparent', textColor: 'var(--color-text-tertiary)' },
            { name: 'Engagement\nAgent', color: 'var(--color-success-pale)', textColor: 'hsl(142 60% 28%)' },
            { name: '↕', color: 'transparent', textColor: 'var(--color-text-tertiary)' },
            { name: 'Compliance\nAgent', color: 'var(--color-warning-pale)', textColor: 'hsl(38 90% 30%)' },
            { name: '↕', color: 'transparent', textColor: 'var(--color-text-tertiary)' },
            { name: 'Fraud\nDetection', color: 'var(--color-danger-pale)', textColor: 'hsl(0 72% 38%)' },
          ].map(({ name, color, textColor }, i) => (
            <div key={i} style={{
              padding: name === '→' || name === '↕' ? '0 var(--space-1)' : 'var(--space-3) var(--space-4)',
              borderRadius: 'var(--radius-md)',
              background: color,
              color: textColor,
              fontSize: name === '→' || name === '↕' ? 'var(--text-xl)' : 'var(--text-xs)',
              fontWeight: name === '→' || name === '↕' ? 400 : 700,
              textAlign: 'center',
              whiteSpace: 'pre-line',
              boxShadow: name === '→' || name === '↕' ? 'none' : 'var(--shadow-xs)',
              minWidth: name === '→' || name === '↕' ? undefined : 90,
            }}>
              {name}
            </div>
          ))}
        </div>
      </div>
    </>
  );
}
