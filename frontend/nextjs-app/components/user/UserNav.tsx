'use client';

import Link from 'next/link';
import { usePathname } from 'next/navigation';
import { currentUser } from '@/lib/mock-data';

const navLinks = [
  { href: '/dashboard',     label: 'Dashboard'     },
  { href: '/transactions',  label: 'Transactions'  },
  { href: '/notifications', label: 'Notifications' },
  { href: '#',              label: 'Payments'      },
  { href: '#',              label: 'Investments'   },
  { href: '#',              label: 'Services'      },
];

export default function UserNav() {
  const pathname = usePathname();

  return (
    <nav className="user-nav" aria-label="SBI Net Banking main navigation">
      {/* Brand */}
      <Link href="/dashboard" className="user-nav__brand" id="nav-brand-link" aria-label="SBI Net Banking Home">
        <div className="user-nav__logo" aria-hidden="true">SBI</div>
        <div>
          <div className="user-nav__title">OnlineSBI</div>
          <div className="user-nav__subtitle">Personal Banking</div>
        </div>
      </Link>

      {/* Nav Links */}
      <ul className="user-nav__links" role="list">
        {navLinks.map(({ href, label }) => (
          <li key={label}>
            <Link
              href={href}
              id={`nav-link-${label.toLowerCase()}`}
              className={`user-nav__link ${pathname === href ? 'user-nav__link--active' : ''}`}
              aria-current={pathname === href ? 'page' : undefined}
            >
              {label}
            </Link>
          </li>
        ))}
      </ul>

      {/* User Actions */}
      <div className="user-nav__actions">
        <div className="user-nav__user-chip" aria-label={`Logged in as ${currentUser.name}`}>
          <div className="user-nav__avatar" aria-hidden="true">
            {currentUser.name.charAt(0)}
          </div>
          <span>{currentUser.name.split(' ')[0]}</span>
        </div>
        <Link href="/login" className="btn btn--ghost" id="nav-logout-btn"
          style={{ color: 'hsl(210 60% 85%)', fontSize: 'var(--text-sm)', padding: 'var(--space-2) var(--space-3)' }}>
          Logout
        </Link>
      </div>
    </nav>
  );
}
