import type { Metadata } from 'next';
import { transactions, formatINR } from '@/lib/mock-data';

export const metadata: Metadata = {
  title: 'Transactions',
  description: 'View your complete SBI account transaction history.',
};

export default function TransactionsPage() {
  return (
    <>
      <div className="page-header">
        <div>
          <h1 className="page-title">Transaction History</h1>
          <p className="page-subtitle">Account XXXX XXXX 4712 — Savings Account</p>
        </div>
        <button className="btn btn--outline" id="download-statement-btn">⬇ Download Statement</button>
      </div>

      <div className="txn-table-container">
        {/* Filter Bar */}
        <div className="txn-filter-bar">
          <input
            type="search"
            className="filter-input"
            placeholder="Search transactions…"
            id="txn-search-input"
            aria-label="Search transactions"
          />
          <select className="filter-select" id="txn-type-filter" aria-label="Filter by type">
            <option value="">All Types</option>
            <option value="credit">Credit</option>
            <option value="debit">Debit</option>
          </select>
          <select className="filter-select" id="txn-channel-filter" aria-label="Filter by channel">
            <option value="">All Channels</option>
            <option value="UPI">UPI</option>
            <option value="NEFT">NEFT</option>
            <option value="IMPS">IMPS</option>
            <option value="ATM">ATM</option>
            <option value="Online">Online</option>
          </select>
          <select className="filter-select" id="txn-date-filter" aria-label="Filter by period">
            <option value="30">Last 30 Days</option>
            <option value="90">Last 90 Days</option>
            <option value="180">Last 6 Months</option>
            <option value="365">Last 1 Year</option>
          </select>
        </div>

        {/* Summary Strip */}
        <div style={{
          display: 'flex', gap: 'var(--space-6)', padding: 'var(--space-3) var(--space-5)',
          background: 'var(--color-primary-pale)', borderBottom: '1px solid var(--color-border-light)',
          fontSize: 'var(--text-sm)',
        }}>
          <span>
            <strong style={{ color: 'var(--color-success)' }}>
              Total Credits: {formatINR(transactions.filter(t => t.type === 'credit').reduce((s, t) => s + t.amount, 0))}
            </strong>
          </span>
          <span>
            <strong style={{ color: 'var(--color-danger)' }}>
              Total Debits: {formatINR(transactions.filter(t => t.type === 'debit').reduce((s, t) => s + t.amount, 0))}
            </strong>
          </span>
          <span style={{ marginLeft: 'auto', color: 'var(--color-text-secondary)' }}>
            {transactions.length} transactions
          </span>
        </div>

        {/* Table */}
        <div style={{ overflowX: 'auto' }}>
          <table className="data-table" aria-label="Transaction history">
            <thead>
              <tr>
                <th>Date</th>
                <th>Description</th>
                <th>Category</th>
                <th>Channel</th>
                <th>Reference No.</th>
                <th style={{ textAlign: 'right' }}>Amount</th>
                <th style={{ textAlign: 'right' }}>Balance</th>
              </tr>
            </thead>
            <tbody>
              {transactions.map((txn) => (
                <tr key={txn.id}>
                  <td style={{ color: 'var(--color-text-secondary)', whiteSpace: 'nowrap' }}>{txn.date}</td>
                  <td style={{ maxWidth: 260 }}>
                    <div style={{
                      whiteSpace: 'nowrap', overflow: 'hidden', textOverflow: 'ellipsis',
                      maxWidth: 240, fontWeight: 500,
                    }}>
                      {txn.description}
                    </div>
                  </td>
                  <td>
                    <span className="badge badge--blue">{txn.category}</span>
                  </td>
                  <td style={{ color: 'var(--color-text-secondary)' }}>{txn.channel}</td>
                  <td>
                    <code style={{ fontSize: 'var(--text-xs)', color: 'var(--color-text-secondary)' }}>
                      {txn.reference}
                    </code>
                  </td>
                  <td style={{ textAlign: 'right' }}>
                    <span className={`txn-amount txn-amount--${txn.type}`}>
                      {txn.type === 'credit' ? '+' : '-'}{formatINR(txn.amount)}
                    </span>
                  </td>
                  <td style={{ textAlign: 'right', color: 'var(--color-text-secondary)' }}>
                    {formatINR(txn.balance)}
                  </td>
                </tr>
              ))}
            </tbody>
          </table>
        </div>

        {/* Pagination */}
        <div style={{
          display: 'flex', alignItems: 'center', justifyContent: 'space-between',
          padding: 'var(--space-4) var(--space-5)', borderTop: '1px solid var(--color-border-light)',
          fontSize: 'var(--text-sm)',
        }}>
          <span style={{ color: 'var(--color-text-secondary)' }}>
            Showing 1–{transactions.length} of {transactions.length} transactions
          </span>
          <div style={{ display: 'flex', gap: 'var(--space-2)' }}>
            <button className="btn btn--ghost" id="txn-prev-btn" aria-label="Previous page">← Prev</button>
            <button className="btn btn--primary" id="txn-next-btn" aria-label="Next page">Next →</button>
          </div>
        </div>
      </div>
    </>
  );
}
