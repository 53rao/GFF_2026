'use client';

import { useState, useEffect } from 'react';
import Link from 'next/link';
import { fetchUserProfile, fetchUserTransactions, fetchUserEngagements } from '@/lib/api';
import { formatINR } from '@/lib/mock-data';

export default function DashboardPage() {
  const [profile, setProfile] = useState<any>(null);
  const [transactions, setTransactions] = useState<any[]>([]);
  const [engagements, setEngagements] = useState<any[]>([]);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    async function loadData() {
      try {
        const [profData, txData, engData] = await Promise.all([
          fetchUserProfile('CUST-1001'),
          fetchUserTransactions('CUST-1001', 10),
          fetchUserEngagements('CUST-1001')
        ]);
        setProfile(profData);
        setTransactions(txData);
        setEngagements(engData);
      } catch (err) {
        console.error('Failed to load live dashboard data:', err);
      } finally {
        setLoading(false);
      }
    }
    loadData();
  }, []);

  if (loading) {
    return (
      <div style={{ padding: 'var(--space-12)', textAlign: 'center', color: 'var(--color-text-secondary)' }}>
        Loading live data from FastAPI backend...
      </div>
    );
  }

  if (!profile) {
    return (
      <div style={{ padding: 'var(--space-12)', textAlign: 'center', color: 'var(--color-danger)' }}>
        Could not connect to FastAPI server at port 8000. Please ensure uvicorn is running.
      </div>
    );
  }

  const recentTxns = transactions.slice(0, 6);

  return (
    <>
      {/* Welcome Banner */}
      <div className="welcome-banner">
        <p className="welcome-banner__greeting">Good afternoon (Live Backend),</p>
        <h1 className="welcome-banner__name">{profile.full_name}</h1>
        <p className="welcome-banner__date">
          {new Date().toLocaleDateString('en-IN', { weekday: 'long', year: 'numeric', month: 'long', day: 'numeric' })}
          &nbsp;·&nbsp; CIF Number: {profile.cif_number}
          &nbsp;·&nbsp; <span style={{ color: 'hsl(142 60% 75%)' }}>● {profile.segment} Segment</span>
        </p>
      </div>

      {/* Account Cards */}
      <div style={{ marginBottom: 'var(--space-2)' }}>
        <div className="page-header" style={{ marginBottom: 'var(--space-4)' }}>
          <div>
            <h2 className="page-title" style={{ fontSize: 'var(--text-md)' }}>Your Live Holdings</h2>
          </div>
          <Link href="/transactions" className="btn btn--outline" id="view-all-accounts-btn">View All</Link>
        </div>
      </div>

      <div className="account-cards-grid" style={{ marginBottom: 'var(--space-8)' }}>
        {(profile.holdings || []).map((acc: any, idx: number) => (
          <div key={idx} className="account-card">
            <div className="account-card__type">{acc.product_name}</div>
            <div className="account-card__number">{acc.product_code}</div>
            <div className="account-card__balance-label">Available Balance</div>
            <div
              className="account-card__balance"
              style={{ color: 'var(--color-text-primary)' }}
            >
              {formatINR(acc.balance || 0)}
            </div>
            <span className="account-card__badge">
              <span style={{ width: 6, height: 6, borderRadius: '50%', background: 'var(--color-success)', display: 'inline-block' }} />
              Active
            </span>
          </div>
        ))}
      </div>

      {/* Main Grid */}
      <div className="dashboard-grid">
        {/* Left: Recent Transactions */}
        <div className="section-card">
          <div className="section-card__header">
            <span className="section-card__title">Recent Live Transactions</span>
            <Link href="/transactions" className="section-card__action" id="see-all-txns-link">See all</Link>
          </div>
          <div className="section-card__body">
            {recentTxns.map((txn) => {
              const isCredit = txn.type?.toUpperCase() === 'CREDIT';
              return (
                <div key={txn.id} className="txn-row">
                  <div className={`txn-icon txn-icon--${isCredit ? 'credit' : 'debit'}`}>
                    <span>{isCredit ? '↓' : '↑'}</span>
                  </div>
                  <div className="txn-info">
                    <div className="txn-info__desc" title={txn.description}>{txn.description}</div>
                    <div className="txn-info__meta">{txn.timestamp?.slice(0, 10)} · {txn.category}</div>
                  </div>
                  <div className={`txn-amount txn-amount--${isCredit ? 'credit' : 'debit'}`}>
                    {isCredit ? '+' : '-'}{formatINR(txn.amount)}
                  </div>
                </div>
              );
            })}
          </div>
        </div>

        {/* Right: Engagement Cases */}
        <div>
          <div style={{ display: 'flex', alignItems: 'center', justifyContent: 'space-between', marginBottom: 'var(--space-4)' }}>
            <h2 style={{ fontSize: 'var(--text-base)', fontWeight: 600, color: 'var(--color-text-primary)' }}>
              Proactive Cases
            </h2>
          </div>

          {engagements.length === 0 ? (
            <div className="notif-card" style={{ color: 'var(--color-text-secondary)' }}>
              No active engagement cases found.
            </div>
          ) : (
            engagements.slice(0, 4).map((caseItem: any) => (
              <div key={caseItem.id} className="notif-card notif-card--unread">
                <div className="notif-card__dot" />
                <div className="notif-card__content">
                  <div className="notif-card__title">Case {caseItem.id} ({caseItem.status})</div>
                  <div className="notif-card__body">Priority: {caseItem.priority}</div>
                </div>
              </div>
            ))
          )}
        </div>
      </div>
    </>
  );
}
