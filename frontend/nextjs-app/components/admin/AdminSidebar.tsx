'use client';

import Link from 'next/link';
import { usePathname } from 'next/navigation';

const navItems = [
  { href: '/admin/dashboard', label: 'Dashboard',       icon: '▦', badge: null },
  { href: '/admin/cases',     label: 'Case Queue',      icon: '⊞',  badge: '3'  },
  { href: '/admin/agents',    label: 'Agent Pipeline',  icon: '◈',  badge: null },
  { href: '/admin/handoffs',  label: 'Handoffs',        icon: '⇄',  badge: '2'  },
];

export default function AdminSidebar() {
  const pathname = usePathname();

  return (
    <aside className="admin-sidebar" aria-label="Admin navigation">
      {/* Brand */}
      <div className="admin-sidebar__brand">
        <div className="admin-sidebar__logo" aria-hidden="true">SBI</div>
        <div>
          <div className="admin-sidebar__title">Operations Hub</div>
          <div className="admin-sidebar__subtitle">Internal Portal</div>
        </div>
      </div>

      {/* Main Nav */}
      <nav className="admin-sidebar__section">
        <p className="admin-sidebar__section-label">Main Menu</p>
        <ul role="list">
          {navItems.map(({ href, label, icon, badge }) => (
            <li key={href}>
              <Link
                href={href}
                id={`admin-nav-${label.toLowerCase().replace(/\s+/g, '-')}`}
                className={`admin-nav__link ${pathname === href ? 'admin-nav__link--active' : ''}`}
                aria-current={pathname === href ? 'page' : undefined}
              >
                <span className="admin-nav__icon" aria-hidden="true">{icon}</span>
                {label}
                {badge && (
                  <span className="admin-nav__badge" aria-label={`${badge} items`}>{badge}</span>
                )}
              </Link>
            </li>
          ))}
        </ul>

        <div style={{ height: 1, background: 'hsl(210 72% 22%)', margin: 'var(--space-4) 0' }} />

        <p className="admin-sidebar__section-label">System</p>
        <ul role="list">
          {[
            { href: '#', label: 'Audit Logs',   icon: '≡' },
            { href: '#', label: 'Configuration', icon: '⚙' },
          ].map(({ href, label, icon }) => (
            <li key={label}>
              <Link href={href} className="admin-nav__link" id={`admin-nav-${label.toLowerCase().replace(/\s+/g, '-')}`}>
                <span className="admin-nav__icon" aria-hidden="true">{icon}</span>
                {label}
              </Link>
            </li>
          ))}
        </ul>
      </nav>

      {/* Footer: User chip */}
      <div className="admin-sidebar__footer">
        <div className="admin-user-chip">
          <div className="admin-user-chip__avatar" aria-hidden="true">RK</div>
          <div className="admin-user-chip__info">
            <div className="admin-user-chip__name">Rajan Krishnamurthy</div>
            <div className="admin-user-chip__role">Branch Operations Manager</div>
          </div>
        </div>
        <Link
          href="/admin/login"
          id="admin-logout-btn"
          style={{
            display: 'block', textAlign: 'center', marginTop: 'var(--space-3)',
            fontSize: 'var(--text-xs)', color: 'hsl(210 40% 60%)',
          }}
        >
          Sign out
        </Link>
      </div>
    </aside>
  );
}
