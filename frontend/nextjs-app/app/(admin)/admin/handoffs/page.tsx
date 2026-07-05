'use client';

import { useState, useEffect } from 'react';
import { fetchAdminCases } from '@/lib/api';

export default function HandoffsPage() {
  const [cases, setCases] = useState<any[]>([]);
  const [handoffs, setHandoffs] = useState<any[]>([]);
  const [filteredHandoffs, setFilteredHandoffs] = useState<any[]>([]);
  const [loading, setLoading] = useState(true);
  const [statusFilter, setStatusFilter] = useState('All');
  const [searchQuery, setSearchQuery] = useState('');

  async function loadHandoffs() {
    setLoading(true);
    try {
      const data = await fetchAdminCases();
      setCases(data || []);
    } catch (err) {
      console.error('Failed to load cases for handoffs:', err);
    } finally {
      setLoading(false);
    }
  }

  useEffect(() => {
    loadHandoffs();
  }, []);

  useEffect(() => {
    // Derive handoff items from cases that are routed to human queues
    // (any case that has an assigned_queue which is not "Automated Nurture Loop")
    const derived = cases
      .filter((c) => c.assigned_queue && c.assigned_queue !== 'Automated Nurture Loop')
      .map((c) => {
        let handoffStatus: 'Pending' | 'Accepted' | 'Completed' | 'Rejected' = 'Pending';
        if (c.status?.toLowerCase() === 'resolved') {
          handoffStatus = 'Completed';
        } else if (c.status?.toLowerCase() === 'assigned' || c.status?.toLowerCase() === 'in progress') {
          handoffStatus = 'Accepted';
        }

        return {
          id: c.id?.replace('CASE-', 'HO-') || 'HO-UNKNOWN',
          caseId: c.id,
          customerName: c.customerName || 'Standard Client',
          customerId: c.customer_id,
          fromAgent: 'Router Agent',
          toAgent: c.assigned_queue,
          reason: c.type || 'Handoff to Queue',
          status: handoffStatus,
          createdAt: c.created_at?.slice(0, 19).replace('T', ' ') || '',
          resolvedAt: c.status?.toLowerCase() === 'resolved' ? c.created_at?.slice(0, 19).replace('T', ' ') : null,
          notes: `Escalated with priority ${c.priority} and SLA ${c.sla}.`,
        };
      });

    setHandoffs(derived);
  }, [cases]);

  useEffect(() => {
    let result = [...handoffs];

    if (statusFilter !== 'All') {
      result = result.filter(
        (h) => h.status?.toLowerCase() === statusFilter.toLowerCase()
      );
    }

    if (searchQuery.trim()) {
      const query = searchQuery.toLowerCase();
      result = result.filter(
        (h) =>
          h.id?.toLowerCase().includes(query) ||
          h.customerId?.toLowerCase().includes(query) ||
          h.customerName?.toLowerCase().includes(query) ||
          h.toAgent?.toLowerCase().includes(query) ||
          h.reason?.toLowerCase().includes(query)
      );
    }

    setFilteredHandoffs(result);
  }, [handoffs, statusFilter, searchQuery]);

  if (loading) {
    return (
      <div style={{ padding: 'var(--space-12)', textAlign: 'center', color: 'var(--color-text-secondary)' }}>
        Loading live handoff queues from FastAPI backend...
      </div>
    );
  }

  const pendingCount = handoffs.filter((h) => h.status === 'Pending').length;
  const acceptedCount = handoffs.filter((h) => h.status === 'Accepted').length;
  const completedCount = handoffs.filter((h) => h.status === 'Completed').length;

  return (
    <>
      <div className="admin-topbar">
        <div>
          <h1 className="admin-topbar__heading">Handoff Management</h1>
          <p className="admin-topbar__sub">
            {pendingCount} pending · {acceptedCount} accepted · {completedCount} completed
          </p>
        </div>
        <button className="btn btn--primary" id="handoffs-refresh-btn" onClick={loadHandoffs} style={{ fontSize: 'var(--text-sm)' }}>
          ↻ Refresh
        </button>
      </div>

      {/* Summary Cards */}
      <div className="kpi-grid" style={{ gridTemplateColumns: 'repeat(4, 1fr)', marginBottom: 'var(--space-5)' }}>
        {[
          { label: 'Total Handoffs',  value: handoffs.length,    color: 'var(--color-primary)'       },
          { label: 'Pending Review',  value: pendingCount,     color: 'var(--color-warning)'        },
          { label: 'Accepted / Active', value: acceptedCount,    color: 'var(--color-success)'        },
          { label: 'Completed',       value: completedCount,   color: 'var(--color-text-secondary)' },
        ].map(({ label, value, color }) => (
          <div key={label} className="kpi-card">
            <div className="kpi-card__label">{label}</div>
            <div className="kpi-card__value" style={{ color }}>{value}</div>
          </div>
        ))}
      </div>

      {/* Filter Tabs */}
      <div style={{ display: 'flex', gap: 'var(--space-2)', marginBottom: 'var(--space-4)' }}>
        {['All', 'Pending', 'Accepted', 'Completed', 'Rejected'].map((status) => (
          <button
            key={status}
            id={`handoffs-filter-${status.toLowerCase()}`}
            className={`btn ${statusFilter === status ? 'btn--primary' : 'btn--ghost'}`}
            onClick={() => setStatusFilter(status)}
            style={{ fontSize: 'var(--text-xs)', padding: 'var(--space-1) var(--space-3)' }}
          >
            {status}
          </button>
        ))}
      </div>

      <div className="admin-table-container">
        <div className="admin-table-header">
          <div className="admin-table-header__title">All Agent Handoffs</div>
          <div className="admin-table-actions">
            <input
              type="search"
              className="admin-search"
              placeholder="Search handoffs…"
              id="handoffs-search-input"
              value={searchQuery}
              onChange={(e) => setSearchQuery(e.target.value)}
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
                <th>To Agent / Queue</th>
                <th>Escalation Reason</th>
                <th>Status</th>
                <th>Created At</th>
                <th>Resolved At</th>
                <th>Notes</th>
              </tr>
            </thead>
            <tbody>
              {filteredHandoffs.length === 0 ? (
                <tr>
                  <td colSpan={9} style={{ textAlign: 'center', padding: 'var(--space-6)' }}>
                    No handoffs found.
                  </td>
                </tr>
              ) : (
                filteredHandoffs.map((h) => (
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
                      <div style={{ fontSize: 'var(--text-xs)', color: 'var(--color-text-secondary)', whiteSpace: 'nowrap', overflow: 'hidden', textOverflow: 'ellipsis', maxWidth: 180 }}
                        title={h.reason}>
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
