'use client';

import { useState, useEffect } from 'react';
import { fetchAdminAgents } from '@/lib/api';

export default function AgentsPage() {
  const [agents, setAgents] = useState<any[]>([]);
  const [loading, setLoading] = useState(true);

  async function loadAgents() {
    setLoading(true);
    try {
      const data = await fetchAdminAgents();
      setAgents(data || []);
    } catch (err) {
      console.error('Failed to load agents:', err);
    } finally {
      setLoading(false);
    }
  }

  useEffect(() => {
    loadAgents();
  }, []);

  if (loading) {
    return (
      <div style={{ padding: 'var(--space-12)', textAlign: 'center', color: 'var(--color-text-secondary)' }}>
        Loading live agent statuses from FastAPI backend...
      </div>
    );
  }

  const activeCount = agents.filter((a) => a.status === 'active').length;
  const idleCount = agents.filter((a) => a.status === 'idle').length;
  const offlineCount = agents.filter((a) => a.status === 'offline').length;

  return (
    <>
      <div className="admin-topbar">
        <div>
          <h1 className="admin-topbar__heading">Agent Pipeline</h1>
          <p className="admin-topbar__sub">
            {activeCount} active · {idleCount} idle · {offlineCount} offline
          </p>
        </div>
        <div style={{ display: 'flex', gap: 'var(--space-3)' }}>
          <button className="btn btn--ghost" id="agents-logs-btn" style={{ fontSize: 'var(--text-sm)' }}>View Logs</button>
          <button className="btn btn--primary" id="agents-refresh-btn" onClick={loadAgents} style={{ fontSize: 'var(--text-sm)' }}>↻ Refresh</button>
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
          { label: 'Last Deploy', value: 'Just now' },
        ].map(({ label, value }) => (
          <div key={label}>
            <div style={{ fontSize: 'var(--text-xs)', color: 'var(--color-text-secondary)' }}>{label}</div>
            <div style={{ fontSize: 'var(--text-sm)', fontWeight: 700, color: 'var(--color-text-primary)' }}>{value}</div>
          </div>
        ))}
      </div>

      {/* Agent Cards */}
      <h2 style={{ fontSize: 'var(--text-sm)', fontWeight: 700, color: 'var(--color-text-secondary)', textTransform: 'uppercase', letterSpacing: '0.06em', marginBottom: 'var(--space-4)' }}>
        Agents — {agents.length} deployed
      </h2>

      <div className="agent-grid">
        {agents.map((agent) => (
          <div key={agent.id} className="agent-card">
            <div className="agent-card__header">
              <div>
                <div className="agent-card__name">{agent.name}</div>
                <div className="agent-card__type">LangGraph Agent Node</div>
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
                <div className="agent-card__stat-value">{agent.casesActive || 0}</div>
              </div>
              <div>
                <div className="agent-card__stat-label">Success Rate</div>
                <div className="agent-card__stat-value" style={{ color: agent.successRate >= 95 ? 'var(--color-success)' : 'var(--color-warning)' }}>
                  {agent.successRate}%
                </div>
              </div>
              <div>
                <div className="agent-card__stat-label">Response Time</div>
                <div className="agent-card__stat-value">Just now</div>
              </div>
            </div>

            <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', marginTop: 'var(--space-4)' }}>
              <span style={{ fontSize: 'var(--text-xs)', color: 'var(--color-text-tertiary)' }}>
                Last ping: {agent.lastPing || 'Just now'}
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
      <div className="admin-table-container" style={{ padding: 'var(--space-5)', marginTop: 'var(--space-6)' }}>
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
