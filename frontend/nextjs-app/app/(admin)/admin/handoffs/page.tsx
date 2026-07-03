import type { Metadata } from 'next';
import { handoffs } from '@/lib/mock-data';

export const metadata: Metadata = {
  title: 'Handoff Management',
  description: 'SBI Operations — Track and manage inter-agent handoff requests.',
};

export default function HandoffsPage() {
  const pending   = handoffs.filter((h) => h.status === 'Pending');
  const accepted  = handoffs.filter((h) => h.status === 'Accepted');
  const completed = handoffs.filter((h) => h.status === 'Completed');

  return (
    <>
      <div className="admin-topbar">
        <div>
          <h1 className="admin-topbar__heading">Handoff Management</h1>
          <p className="admin-topbar__sub">
            {pending.length} pending · {accepted.length} accepted · {completed.length} completed
          </p>
        </div>
        <button className="btn btn--outline" id="handoffs-export-btn" style={{ fontSize: 'var(--text-sm)' }}>
          Export
        </button>
      </div>

      {/* Summary Cards */}
      <div className="kpi-grid" style={{ gridTemplateColumns: 'repeat(4, 1fr)', marginBottom: 'var(--space-5)' }}>
        {[
          { label: 'Total Handoffs',  value: handoffs.length,    color: 'var(--color-primary)'       },
          { label: 'Pending',         value: pending.length,     color: 'var(--color-warning)'        },
          { label: 'Accepted',        value: accepted.length,    color: 'var(--color-success)'        },
          { label: 'Completed',       value: completed.length,   color: 'var(--color-text-secondary)' },
        ].map(({ label, value, color }) => (
          <div key={label} className="kpi-card">
            <div className="kpi-card__label">{label}</div>
            <div className="kpi-card__value" style={{ color }}>{value}</div>
          </div>
        ))}
      </div>

      {/* Filter Tabs */}
      <div style={{ display: 'flex', gap: 'var(--space-2)', marginBottom: 'var(--space-4)' }}>
        {['All', 'Pending', 'Accepted', 'Completed', 'Rejected'].map((status, i) => (
          <button
            key={status}
            id={`handoffs-filter-${status.toLowerCase()}`}
            className={`btn ${i === 0 ? 'btn--primary' : 'btn--ghost'}`}
            style={{ fontSize: 'var(--text-xs)', padding: 'var(--space-1) var(--space-3)' }}
          >
            {status}
          </button>
        ))}
      </div>

      <div className="admin-table-container">
        <div className="admin-table-header">
          <div className="admin-table-header__title">All Handoffs</div>
          <div className="admin-table-actions">
            <input
              type="search"
              className="admin-search"
              placeholder="Search handoffs…"
              id="handoffs-search-input"
              aria-label="Search handoffs"
            />
          </div>
        </div>

        <div style={{ overflowX: 'auto' }}>
          <table className="admin-table" aria-label="Handoff management table">
            <thead>
              <tr>
                <th>Handoff ID</th>
                <th>Customer</th>
                <th>From Agent</th>
                <th>To Agent</th>
                <th>Reason</th>
                <th>Status</th>
                <th>Created</th>
                <th>Resolved</th>
                <th>Notes</th>
                <th>Actions</th>
              </tr>
            </thead>
            <tbody>
              {handoffs.map((h) => (
                <tr key={h.id}>
                  <td>
                    <code style={{ fontSize: 'var(--text-xs)', color: 'var(--color-primary)', fontWeight: 600 }}>
                      {h.id}
                    </code>
                  </td>
                  <td>
                    <div style={{ fontWeight: 600, fontSize: 'var(--text-sm)' }}>{h.customerName}</div>
                    <div style={{ fontSize: 'var(--text-xs)', color: 'var(--color-text-tertiary)' }}>{h.customerId}</div>
                  </td>
                  <td style={{ fontSize: 'var(--text-xs)', color: 'var(--color-text-secondary)' }}>{h.fromAgent}</td>
                  <td style={{ fontSize: 'var(--text-xs)', color: 'var(--color-primary)', fontWeight: 600 }}>{h.toAgent}</td>
                  <td style={{ maxWidth: 200 }}>
                    <div style={{ fontSize: 'var(--text-xs)', color: 'var(--color-text-secondary)', whiteSpace: 'nowrap', overflow: 'hidden', textOverflow: 'ellipsis', maxWidth: 180 }}>
                      {h.reason}
                    </div>
                  </td>
                  <td>
                    <span className={`badge ${
                      h.status === 'Pending'   ? 'badge--yellow' :
                      h.status === 'Accepted'  ? 'badge--blue'   :
                      h.status === 'Completed' ? 'badge--green'  : 'badge--red'
                    }`}>{h.status}</span>
                  </td>
                  <td style={{ fontSize: 'var(--text-xs)', color: 'var(--color-text-secondary)', whiteSpace: 'nowrap' }}>
                    {h.createdAt}
                  </td>
                  <td style={{ fontSize: 'var(--text-xs)', color: 'var(--color-text-secondary)', whiteSpace: 'nowrap' }}>
                    {h.resolvedAt ?? '—'}
                  </td>
                  <td style={{ maxWidth: 200 }}>
                    <div style={{ fontSize: 'var(--text-xs)', color: 'var(--color-text-secondary)', whiteSpace: 'nowrap', overflow: 'hidden', textOverflow: 'ellipsis', maxWidth: 180 }}
                      title={h.notes}>
                      {h.notes}
                    </div>
                  </td>
                  <td>
                    {h.status === 'Pending' && (
                      <div style={{ display: 'flex', gap: 4 }}>
                        <button
                          className="btn btn--primary"
                          id={`handoff-accept-${h.id}`}
                          style={{ fontSize: 'var(--text-xs)', padding: '2px 8px' }}
                        >
                          Accept
                        </button>
                        <button
                          className="btn btn--ghost"
                          id={`handoff-reject-${h.id}`}
                          style={{ fontSize: 'var(--text-xs)', padding: '2px 8px', color: 'var(--color-danger)' }}
                        >
                          Reject
                        </button>
                      </div>
                    )}
                    {h.status !== 'Pending' && (
                      <button
                        className="btn btn--ghost"
                        id={`handoff-view-${h.id}`}
                        style={{ fontSize: 'var(--text-xs)', padding: '2px 8px' }}
                      >
                        View
                      </button>
                    )}
                  </td>
                </tr>
              ))}
            </tbody>
          </table>
        </div>
      </div>
    </>
  );
}
