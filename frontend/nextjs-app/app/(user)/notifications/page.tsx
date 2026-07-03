import type { Metadata } from 'next';
import { notifications } from '@/lib/mock-data';

export const metadata: Metadata = {
  title: 'Notifications',
  description: 'Your personalised banking engagement messages and alerts from SBI.',
};

const typeConfig: Record<string, { label: string; icon: string; badgeClass: string }> = {
  offer:    { label: 'Offer',    icon: '🎯', badgeClass: 'badge--blue'   },
  promo:    { label: 'Promo',    icon: '✨', badgeClass: 'badge--blue'   },
  alert:    { label: 'Alert',    icon: '🔔', badgeClass: 'badge--yellow' },
  reminder: { label: 'Reminder', icon: '📌', badgeClass: 'badge--gray'   },
};

const priorityConfig: Record<string, { label: string; badgeClass: string }> = {
  high:   { label: 'High Priority',   badgeClass: 'badge--red'    },
  medium: { label: 'Medium Priority', badgeClass: 'badge--yellow' },
  low:    { label: 'Low Priority',    badgeClass: 'badge--gray'   },
};

export default function NotificationsPage() {
  const unread = notifications.filter((n) => !n.read);
  const read   = notifications.filter((n) =>  n.read);

  return (
    <>
      <div className="page-header">
        <div>
          <h1 className="page-title">Notifications &amp; Alerts</h1>
          <p className="page-subtitle">
            Personalised messages from SBI · {unread.length} unread
          </p>
        </div>
        <button className="btn btn--ghost" id="mark-all-read-btn">Mark all as read</button>
      </div>

      {/* Tabs */}
      <div style={{ display: 'flex', gap: 'var(--space-2)', marginBottom: 'var(--space-6)' }}>
        {['All', 'Unread', 'Offers', 'Alerts'].map((tab, i) => (
          <button
            key={tab}
            id={`notif-tab-${tab.toLowerCase()}`}
            className={`btn ${i === 0 ? 'btn--primary' : 'btn--ghost'}`}
            style={{ fontSize: 'var(--text-sm)', padding: 'var(--space-2) var(--space-4)' }}
          >
            {tab}
          </button>
        ))}
      </div>

      {/* Unread Section */}
      {unread.length > 0 && (
        <section aria-label="Unread notifications">
          <h2 style={{
            fontSize: 'var(--text-xs)', fontWeight: 700, textTransform: 'uppercase',
            letterSpacing: '0.08em', color: 'var(--color-text-secondary)',
            marginBottom: 'var(--space-3)',
          }}>
            Unread — {unread.length}
          </h2>
          {unread.map((notif) => {
            const tc = typeConfig[notif.type] ?? typeConfig.alert;
            const pc = priorityConfig[notif.priority];
            return (
              <div key={notif.id} className="notif-card notif-card--unread">
                <div style={{ fontSize: 24, flexShrink: 0, marginTop: 2 }}>{tc.icon}</div>
                <div className="notif-card__content">
                  <div style={{ display: 'flex', alignItems: 'center', gap: 'var(--space-2)', marginBottom: 'var(--space-2)', flexWrap: 'wrap' }}>
                    <span className={`badge ${tc.badgeClass}`}>{tc.label}</span>
                    <span className={`badge ${pc.badgeClass}`}>{pc.label}</span>
                  </div>
                  <div className="notif-card__title">{notif.title}</div>
                  <div className="notif-card__body">{notif.body}</div>
                  <div style={{ display: 'flex', alignItems: 'center', justifyContent: 'space-between', marginTop: 'var(--space-3)' }}>
                    <span className="notif-card__time">{notif.timestamp}</span>
                    <div style={{ display: 'flex', gap: 'var(--space-2)' }}>
                      <button
                        className="btn btn--primary"
                        id={`notif-action-${notif.id}`}
                        style={{ fontSize: 'var(--text-xs)', padding: '4px 12px' }}
                      >
                        {notif.type === 'offer' || notif.type === 'promo' ? 'Know More' : 'View Details'}
                      </button>
                      <button
                        className="btn btn--ghost"
                        id={`notif-dismiss-${notif.id}`}
                        style={{ fontSize: 'var(--text-xs)', padding: '4px 10px' }}
                      >
                        Dismiss
                      </button>
                    </div>
                  </div>
                </div>
              </div>
            );
          })}
        </section>
      )}

      {/* Read Section */}
      {read.length > 0 && (
        <section aria-label="Read notifications" style={{ marginTop: 'var(--space-8)' }}>
          <h2 style={{
            fontSize: 'var(--text-xs)', fontWeight: 700, textTransform: 'uppercase',
            letterSpacing: '0.08em', color: 'var(--color-text-secondary)',
            marginBottom: 'var(--space-3)',
          }}>
            Earlier
          </h2>
          {read.map((notif) => {
            const tc = typeConfig[notif.type] ?? typeConfig.alert;
            return (
              <div key={notif.id} className="notif-card">
                <div style={{ fontSize: 20, flexShrink: 0, marginTop: 2, opacity: 0.5 }}>{tc.icon}</div>
                <div className="notif-card__content">
                  <div className="notif-card__title" style={{ color: 'var(--color-text-secondary)', fontWeight: 500 }}>
                    {notif.title}
                  </div>
                  <div className="notif-card__body">{notif.body}</div>
                  <div className="notif-card__time">{notif.timestamp}</div>
                </div>
              </div>
            );
          })}
        </section>
      )}
    </>
  );
}
