import type { Metadata } from 'next';
import { cases } from '@/lib/mock-data';

export const metadata: Metadata = {
  title: 'Case Queue',
  description: 'SBI Operations — Full case queue with priority, status, and SLA tracking.',
};

export default function CasesPage() {
  return (
    <>
      <div className="admin-topbar">
        <div>
          <h1 className="admin-topbar__heading">Case Queue</h1>
          <p className="admin-topbar__sub">{cases.length} total cases · {cases.filter(c => c.slaBreached).length} SLA breached</p>
        </div>
        <div style={{ display: 'flex', gap: 'var(--space-3)' }}>
          <button className="btn btn--ghost" id="cases-export-btn" style={{ fontSize: 'var(--text-sm)' }}>Export CSV</button>
          <button className="btn btn--primary" id="cases-new-btn" style={{ fontSize: 'var(--text-sm)' }}>+ New Case</button>
        </div>
      </div>

      {/* Quick Filters */}
      <div style={{ display: 'flex', gap: 'var(--space-2)', marginBottom: 'var(--space-5)', flexWrap: 'wrap' }}>
        {['All', 'Open', 'In Progress', 'Escalated', 'Resolved'].map((status, i) => (
          <button
            key={status}
            id={`case-filter-${status.toLowerCase().replace(/\s+/g, '-')}`}
            className={`btn ${i === 0 ? 'btn--primary' : 'btn--ghost'}`}
            style={{ fontSize: 'var(--text-xs)', padding: 'var(--space-1) var(--space-3)' }}
          >
            {status}
            {status === 'All' && <span style={{ marginLeft: 4, opacity: 0.7 }}>({cases.length})</span>}
          </button>
        ))}
      </div>

      <div className="admin-table-container">
        <div className="admin-table-header">
          <div>
            <div className="admin-table-header__title">All Cases</div>
            <div className="admin-table-header__count">Showing {cases.length} of {cases.length}</div>
          </div>
          <div className="admin-table-actions">
            <input
              type="search"
              className="admin-search"
              placeholder="Search by customer, case ID…"
              id="cases-search-input"
              aria-label="Search cases"
            />
            <select className="admin-search" id="cases-priority-filter" aria-label="Filter by priority"
              style={{ width: 'auto', cursor: 'pointer' }}>
              <option value="">All Priorities</option>
              <option>Critical</option>
              <option>High</option>
              <option>Medium</option>
              <option>Low</option>
            </select>
          </div>
        </div>

        <div style={{ overflowX: 'auto' }}>
          <table className="admin-table" aria-label="Case queue">
            <thead>
              <tr>
                <th className="sortable">Case ID ↕</th>
                <th>Customer</th>
                <th>Customer ID</th>
                <th className="sortable">Type</th>
                <th className="sortable">Priority ↕</th>
                <th className="sortable">Status ↕</th>
                <th>Assigned Agent</th>
                <th className="sortable">Created ↕</th>
                <th>Last Updated</th>
                <th>SLA</th>
                <th>Actions</th>
              </tr>
            </thead>
            <tbody>
              {cases.map((c) => (
                <tr key={c.id}>
                  <td>
                    <code style={{ fontSize: 'var(--text-xs)', color: 'var(--color-primary)', fontWeight: 600 }}>
                      {c.id}
                    </code>
                  </td>
                  <td style={{ fontWeight: 600 }}>{c.customerName}</td>
                  <td>
                    <code style={{ fontSize: 'var(--text-xs)', color: 'var(--color-text-secondary)' }}>
                      {c.customerId}
                    </code>
                  </td>
                  <td style={{ color: 'var(--color-text-secondary)' }}>{c.type}</td>
                  <td>
                    <span className={`badge ${
                      c.priority === 'Critical' ? 'badge--red' :
                      c.priority === 'High'     ? 'badge--yellow' :
                      c.priority === 'Medium'   ? 'badge--blue' : 'badge--gray'
                    }`}>
                      {c.priority === 'Critical' && '● '}{c.priority}
                    </span>
                  </td>
                  <td>
                    <span className={`badge ${
                      c.status === 'Escalated'      ? 'badge--red'    :
                      c.status === 'In Progress'    ? 'badge--blue'   :
                      c.status === 'Pending Review' ? 'badge--yellow' :
                      c.status === 'Resolved'       ? 'badge--green'  : 'badge--gray'
                    }`}>{c.status}</span>
                  </td>
                  <td style={{ color: 'var(--color-text-secondary)', fontSize: 'var(--text-xs)' }}>
                    {c.assignedAgent}
                  </td>
                  <td style={{ color: 'var(--color-text-secondary)', fontSize: 'var(--text-xs)' }}>{c.createdAt}</td>
                  <td style={{ color: 'var(--color-text-secondary)', fontSize: 'var(--text-xs)' }}>{c.updatedAt}</td>
                  <td>
                    <span style={{
                      fontSize: 'var(--text-xs)', fontWeight: 700,
                      color: c.slaBreached ? 'var(--color-danger)' : 'var(--color-success)',
                    }}>
                      {c.slaBreached ? `⚠ Breached` : `✓ ${c.sla}`}
                    </span>
                  </td>
                  <td>
                    <div style={{ display: 'flex', gap: 4 }}>
                      <button
                        className="btn btn--outline"
                        id={`case-view-${c.id}`}
                        style={{ fontSize: 'var(--text-xs)', padding: '2px 8px' }}
                      >
                        View
                      </button>
                      {c.status !== 'Resolved' && (
                        <button
                          className="btn btn--primary"
                          id={`case-assign-${c.id}`}
                          style={{ fontSize: 'var(--text-xs)', padding: '2px 8px' }}
                        >
                          Assign
                        </button>
                      )}
                    </div>
                  </td>
                </tr>
              ))}
            </tbody>
          </table>
        </div>

        {/* Footer */}
        <div style={{
          display: 'flex', alignItems: 'center', justifyContent: 'space-between',
          padding: 'var(--space-3) var(--space-5)', borderTop: '1px solid var(--color-border-light)',
          fontSize: 'var(--text-sm)',
        }}>
          <span style={{ color: 'var(--color-text-secondary)' }}>Showing 1–{cases.length} of {cases.length}</span>
          <div style={{ display: 'flex', gap: 'var(--space-2)' }}>
            <button className="btn btn--ghost" id="cases-prev-btn" style={{ fontSize: 'var(--text-sm)' }}>← Prev</button>
            <button className="btn btn--primary" id="cases-next-btn" style={{ fontSize: 'var(--text-sm)' }}>Next →</button>
          </div>
        </div>
      </div>
    </>
  );
}
