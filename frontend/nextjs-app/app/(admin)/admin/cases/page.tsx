'use client';

import { useState, useEffect } from 'react';
import { fetchAdminCases } from '@/lib/api';
import { formatINR } from '@/lib/mock-data';

export default function CasesPage() {
  const [cases, setCases] = useState<any[]>([]);
  const [filteredCases, setFilteredCases] = useState<any[]>([]);
  const [loading, setLoading] = useState(true);
  const [statusFilter, setStatusFilter] = useState('All');
  const [priorityFilter, setPriorityFilter] = useState('');
  const [searchQuery, setSearchQuery] = useState('');

  async function loadCases() {
    setLoading(true);
    try {
      const data = await fetchAdminCases();
      setCases(data || []);
    } catch (err) {
      console.error('Failed to load cases:', err);
    } finally {
      setLoading(false);
    }
  }

  useEffect(() => {
    loadCases();
  }, []);

  useEffect(() => {
    let result = [...cases];

    if (statusFilter !== 'All') {
      result = result.filter(
        (c) => c.status?.toLowerCase() === statusFilter.toLowerCase()
      );
    }

    if (priorityFilter) {
      result = result.filter(
        (c) => c.priority?.toLowerCase() === priorityFilter.toLowerCase()
      );
    }

    if (searchQuery.trim()) {
      const query = searchQuery.toLowerCase();
      result = result.filter(
        (c) =>
          c.id?.toLowerCase().includes(query) ||
          c.customer_id?.toLowerCase().includes(query) ||
          c.customerName?.toLowerCase().includes(query) ||
          c.type?.toLowerCase().includes(query)
      );
    }

    setFilteredCases(result);
  }, [cases, statusFilter, priorityFilter, searchQuery]);

  if (loading) {
    return (
      <div style={{ padding: 'var(--space-12)', textAlign: 'center', color: 'var(--color-text-secondary)' }}>
        Loading live case queue from FastAPI backend...
      </div>
    );
  }

  const breachedCount = filteredCases.filter((c) => c.slaBreached).length;

  return (
    <>
      <div className="admin-topbar">
        <div>
          <h1 className="admin-topbar__heading">Case Queue</h1>
          <p className="admin-topbar__sub">
            {filteredCases.length} total cases · {breachedCount} SLA breached
          </p>
        </div>
        <div style={{ display: 'flex', gap: 'var(--space-3)' }}>
          <button className="btn btn--ghost" id="cases-export-btn" style={{ fontSize: 'var(--text-sm)' }}>Export CSV</button>
          <button className="btn btn--primary" id="cases-refresh-btn" onClick={loadCases} style={{ fontSize: 'var(--text-sm)' }}>↻ Refresh</button>
        </div>
      </div>

      {/* Quick Filters */}
      <div style={{ display: 'flex', gap: 'var(--space-2)', marginBottom: 'var(--space-5)', flexWrap: 'wrap' }}>
        {['All', 'Open', 'In Progress', 'Escalated', 'Resolved'].map((status) => (
          <button
            key={status}
            id={`case-filter-${status.toLowerCase().replace(/\s+/g, '-')}`}
            className={`btn ${statusFilter === status ? 'btn--primary' : 'btn--ghost'}`}
            onClick={() => setStatusFilter(status)}
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
            <div className="admin-table-header__count">Showing {filteredCases.length} of {cases.length}</div>
          </div>
          <div className="admin-table-actions">
            <input
              type="search"
              className="admin-search"
              placeholder="Search by customer, case ID…"
              id="cases-search-input"
              value={searchQuery}
              onChange={(e) => setSearchQuery(e.target.value)}
              aria-label="Search cases"
            />
            <select
              className="admin-search"
              id="cases-priority-filter"
              aria-label="Filter by priority"
              value={priorityFilter}
              onChange={(e) => setPriorityFilter(e.target.value)}
              style={{ width: 'auto', cursor: 'pointer' }}
            >
              <option value="">All Priorities</option>
              <option value="critical">Critical</option>
              <option value="high">High</option>
              <option value="medium">Medium</option>
              <option value="low">Low</option>
            </select>
          </div>
        </div>

        <div style={{ overflowX: 'auto' }}>
          <table className="admin-table" aria-label="Case queue">
            <thead>
              <tr>
                <th>Case ID</th>
                <th>Customer</th>
                <th>Customer ID</th>
                <th>Type</th>
                <th>Priority</th>
                <th>Status</th>
                <th>Queue / Route</th>
                <th>Created At</th>
                <th>SLA</th>
              </tr>
            </thead>
            <tbody>
              {filteredCases.length === 0 ? (
                <tr>
                  <td colSpan={9} style={{ textAlign: 'center', padding: 'var(--space-6)' }}>
                    No cases match the selected filters.
                  </td>
                </tr>
              ) : (
                filteredCases.map((c) => (
                  <tr key={c.id}>
                    <td>
                      <code style={{ fontSize: 'var(--text-xs)', color: 'var(--color-primary)', fontWeight: 600 }}>
                        {c.id}
                      </code>
                    </td>
                    <td style={{ fontWeight: 600 }}>{c.customerName || 'Standard Client'}</td>
                    <td>
                      <code style={{ fontSize: 'var(--text-xs)', color: 'var(--color-text-secondary)' }}>
                        {c.customer_id || c.customerId}
                      </code>
                    </td>
                    <td style={{ color: 'var(--color-text-secondary)' }}>{c.type}</td>
                    <td>
                      <span className={`badge ${
                        c.priority?.toLowerCase() === 'critical' ? 'badge--red' :
                        c.priority?.toLowerCase() === 'high'     ? 'badge--yellow' :
                        c.priority?.toLowerCase() === 'medium'   ? 'badge--blue' : 'badge--gray'
                      }`}>
                        {c.priority}
                      </span>
                    </td>
                    <td>
                      <span className={`badge ${
                        c.status?.toLowerCase() === 'escalated'      ? 'badge--red'    :
                        c.status?.toLowerCase() === 'in progress'    ? 'badge--blue'   :
                        c.status?.toLowerCase() === 'assigned'       ? 'badge--blue'   :
                        c.status?.toLowerCase() === 'resolved'       ? 'badge--green'  : 'badge--gray'
                      }`}>{c.status}</span>
                    </td>
                    <td style={{ color: 'var(--color-text-secondary)', fontSize: 'var(--text-xs)' }}>
                      {c.assigned_queue || c.assignedQueue || c.assignedAgent}
                    </td>
                    <td style={{ color: 'var(--color-text-secondary)', fontSize: 'var(--text-xs)' }}>
                      {c.created_at?.slice(0, 19).replace('T', ' ') || c.createdAt}
                    </td>
                    <td>
                      <span style={{
                        fontSize: 'var(--text-xs)', fontWeight: 700,
                        color: c.slaBreached ? 'var(--color-danger)' : 'var(--color-success)',
                      }}>
                        {c.slaBreached ? `⚠ Breached` : `✓ ${c.sla}`}
                      </span>
                    </td>
                  </tr>
                ))
              )}
            </tbody>
          </table>
        </div>
      </div>
    </>
  );
}
