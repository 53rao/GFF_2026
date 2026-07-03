'use client';

import { useState, useEffect } from 'react';
import Link from 'next/link';
import { fetchAdminCustomers, fetchAdminSignals, fetchAdminCases, triggerSentinelRun } from '@/lib/api';
import { agentStatuses, handoffs } from '@/lib/mock-data';

export default function AdminDashboardPage() {
  const [customers, setCustomers] = useState<any[]>([]);
  const [signals, setSignals] = useState<any[]>([]);
  const [cases, setCases] = useState<any[]>([]);
  const [loading, setLoading] = useState(true);
  const [runningSentinel, setRunningSentinel] = useState(false);

  async function loadData() {
    setLoading(true);
    try {
      const [custData, sigData, caseData] = await Promise.all([
        fetchAdminCustomers(1, 30),
        fetchAdminSignals(),
        fetchAdminCases()
      ]);
      setCustomers(custData.items || []);
      setSignals(sigData || []);
      setCases(caseData || []);
    } catch (err) {
      console.error('Failed to load admin dashboard data:', err);
    } finally {
      setLoading(false);
    }
  }

  useEffect(() => {
    loadData();
  }, []);

  async function handleRunSentinel() {
    setRunningSentinel(true);
    try {
      await triggerSentinelRun('CUST-1001');
      await triggerSentinelRun('CUST-1002');
      await triggerSentinelRun('CUST-1003');
      await triggerSentinelRun('CUST-1004');
      await loadData();
    } catch (err) {
      console.error('Error running sentinel:', err);
    } finally {
      setRunningSentinel(false);
    }
  }

  if (loading) {
    return (
      <div style={{ padding: 'var(--space-12)', textAlign: 'center', color: 'var(--color-text-secondary)' }}>
        Loading Operations Hub from FastAPI backend...
      </div>
    );
  }

  const kpis = [
    { label: 'Total Customers',     value: customers.length.toString(), delta: 'Live JSON Store', dir: 'flat' },
    { label: 'Detected Signals',    value: signals.length.toString(),   delta: 'Sentinel Active',  dir: 'up'   },
    { label: 'Active Pipeline Cases', value: cases.length.toString(),     delta: 'Auto-orchestrated',dir: 'up'   },
    { label: 'Agents Deployed',     value: '9',                         delta: 'LangGraph Nodes',  dir: 'flat' },
  ];

  return (
    <>
      <div className="admin-topbar">
        <div>
          <h1 className="admin-topbar__heading">Operations Dashboard (Live Backend)</h1>
          <p className="admin-topbar__sub">
            {new Date().toLocaleDateString('en-IN', { weekday: 'long', year: 'numeric', month: 'long', day: 'numeric' })}
            &nbsp;·&nbsp; Connected to FastAPI Port 8000
          </p>
        </div>
        <div style={{ display: 'flex', gap: 'var(--space-3)' }}>
          <button 
            className="btn btn--outline" 
            id="run-sentinel-btn" 
            onClick={handleRunSentinel}
            disabled={runningSentinel}
            style={{ fontSize: 'var(--text-sm)', borderColor: 'var(--color-primary)', color: 'var(--color-primary)' }}
          >
            {runningSentinel ? 'Running Sentinel...' : '⚡ Run Sentinel Detection'}
          </button>
          <button className="btn btn--primary" id="admin-refresh-btn" onClick={loadData} style={{ fontSize: 'var(--text-sm)' }}>
            ↻ Refresh
          </button>
        </div>
      </div>

      {/* KPI Grid */}
      <div className="kpi-grid">
        {kpis.map(({ label, value, delta, dir }) => (
          <div key={label} className="kpi-card">
            <div className="kpi-card__label">{label}</div>
            <div className="kpi-card__value">{value}</div>
            <div className={`kpi-card__delta kpi-card__delta--${dir === 'up' ? 'up' : 'flat'}`}>
              <span>{dir === 'up' ? '↑' : '→'}</span>
              {delta}
            </div>
          </div>
        ))}
      </div>

      <div className="admin-dashboard-grid">
        {/* Left: Detected Signals / Cases */}
        <div>
          <div className="admin-table-container">
            <div className="admin-table-header">
              <div>
                <div className="admin-table-header__title">Live Detected Signals (Sentinel Output)</div>
                <div className="admin-table-header__count">{signals.length} anomalies detected across customer store</div>
              </div>
              <Link href="/admin/cases" className="btn btn--outline" id="admin-view-all-cases-btn"
                style={{ fontSize: 'var(--text-sm)', padding: 'var(--space-2) var(--space-4)' }}>
                View All
              </Link>
            </div>
            <div style={{ overflowX: 'auto' }}>
              <table className="admin-table" aria-label="Detected signals summary">
                <thead>
                  <tr>
                    <th>Signal ID</th>
                    <th>Customer ID</th>
                    <th>Type</th>
                    <th>Confidence</th>
                    <th>Urgency</th>
                    <th>Detected At</th>
                  </tr>
                </thead>
                <tbody>
                  {signals.length === 0 ? (
                    <tr>
                      <td colSpan={6} style={{ textAlign: 'center', padding: 'var(--space-6)' }}>
                        No signals detected yet. Click "⚡ Run Sentinel Detection" above!
                      </td>
                    </tr>
                  ) : (
                    signals.map((s: any) => (
                      <tr key={s.signal_id}>
                        <td><code style={{ fontSize: 'var(--text-xs)' }}>{s.signal_id}</code></td>
                        <td style={{ fontWeight: 600 }}>{s.customer_id}</td>
                        <td>
                          <span className={`badge ${
                            s.signal_type === 'LARGE_INFLOW' ? 'badge--green' :
                            s.signal_type === 'SPENDING_SPIKE' ? 'badge--red' : 'badge--yellow'
                          }`}>{s.signal_type}</span>
                        </td>
                        <td>{(s.confidence * 100).toFixed(0)}%</td>
                        <td>
                          <span className="badge badge--blue">Level {s.urgency}</span>
                        </td>
                        <td style={{ fontSize: 'var(--text-xs)', color: 'var(--color-text-secondary)' }}>
                          {s.detected_at?.slice(0, 19).replace('T', ' ')}
                        </td>
                      </tr>
                    ))
                  )}
                </tbody>
              </table>
            </div>
          </div>
        </div>

        {/* Right: Customer Directory Preview */}
        <div style={{ display: 'flex', flexDirection: 'column', gap: 'var(--space-4)' }}>
          <div className="admin-panel">
            <div className="admin-panel__header">
              <span className="admin-panel__title">Live Customers ({customers.length})</span>
            </div>
            <div className="admin-panel__body" style={{ padding: 0, maxHeight: 400, overflowY: 'auto' }}>
              {customers.slice(0, 6).map((c: any) => (
                <div key={c.id} style={{
                  display: 'flex', alignItems: 'center', gap: 'var(--space-3)',
                  padding: 'var(--space-3) var(--space-5)',
                  borderBottom: '1px solid var(--color-border-light)',
                }}>
                  <div className="agent-status-dot agent-status-dot--active" />
                  <div style={{ flex: 1, minWidth: 0 }}>
                    <div style={{ fontSize: 'var(--text-sm)', fontWeight: 600, whiteSpace: 'nowrap', overflow: 'hidden', textOverflow: 'ellipsis' }}>
                      {c.full_name} ({c.id})
                    </div>
                    <div style={{ fontSize: 'var(--text-xs)', color: 'var(--color-text-secondary)' }}>
                      {c.segment} · Balance: ₹{(c.account_balance || 0).toLocaleString('en-IN')}
                    </div>
                  </div>
                </div>
              ))}
            </div>
          </div>
        </div>
      </div>
    </>
  );
}
