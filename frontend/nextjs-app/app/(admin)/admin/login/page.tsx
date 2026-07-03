import type { Metadata } from 'next';
import Link from 'next/link';

export const metadata: Metadata = {
  title: 'Admin Login',
  description: 'SBI Operations Hub — Staff login portal.',
};

export default function AdminLoginPage() {
  return (
    <div className="admin-login-page" style={{ marginLeft: 'calc(-1 * var(--sidebar-width))', width: '100vw' }}>
      <div className="admin-login-card">
        <div className="admin-login-card__badge">
          <span>🔐</span> Internal Staff Portal
        </div>

        <div style={{ display: 'flex', alignItems: 'center', gap: 'var(--space-3)', marginBottom: 'var(--space-8)' }}>
          <div style={{
            width: 44, height: 44, background: 'var(--color-primary-dark)', borderRadius: 10,
            display: 'flex', alignItems: 'center', justifyContent: 'center', flexShrink: 0,
          }}>
            <span style={{ fontWeight: 800, color: 'white', fontSize: 13, letterSpacing: '-0.5px' }}>SBI</span>
          </div>
          <div>
            <div style={{ fontWeight: 700, color: 'var(--color-text-primary)', fontSize: 'var(--text-base)' }}>Operations Hub</div>
            <div style={{ fontSize: 'var(--text-xs)', color: 'var(--color-text-secondary)' }}>Multi-Agent Banking System</div>
          </div>
        </div>

        <h1 style={{ fontSize: 'var(--text-xl)', fontWeight: 700, marginBottom: 'var(--space-2)' }}>Staff Sign In</h1>
        <p style={{ fontSize: 'var(--text-sm)', color: 'var(--color-text-secondary)', marginBottom: 'var(--space-8)' }}>
          Authorised personnel only. All access is logged and monitored.
        </p>

        <form aria-label="Admin login form">
          <div className="form-group">
            <label className="form-label" htmlFor="admin-emp-id">Employee ID</label>
            <input id="admin-emp-id" type="text" className="form-input" placeholder="e.g. EMP-2026-00142" autoComplete="username" />
          </div>
          <div className="form-group">
            <label className="form-label" htmlFor="admin-password">Password</label>
            <input id="admin-password" type="password" className="form-input" placeholder="Enter your password" autoComplete="current-password" />
          </div>
          <div className="form-group">
            <label className="form-label" htmlFor="admin-branch">Branch / Region</label>
            <select id="admin-branch" className="form-input" style={{ cursor: 'pointer' }}>
              <option value="">Select your branch…</option>
              <option>Head Office, Mumbai</option>
              <option>Delhi Circle</option>
              <option>Chennai Circle</option>
              <option>Kolkata Circle</option>
              <option>Bengaluru Circle</option>
            </select>
          </div>

          <Link href="/admin/dashboard" className="btn btn--primary btn--full btn--lg" id="admin-login-btn"
            style={{ marginTop: 'var(--space-2)' }}>
            Sign In
          </Link>
        </form>

        <div style={{
          marginTop: 'var(--space-6)', padding: 'var(--space-3) var(--space-4)',
          background: 'var(--color-warning-pale)', borderRadius: 'var(--radius-md)',
          fontSize: 'var(--text-xs)', color: 'hsl(38 90% 30%)', lineHeight: 'var(--leading-relaxed)',
        }}>
          ⚠️ This portal is restricted to authorised SBI employees. Unauthorised access attempts will be reported to IT Security.
        </div>

        <div style={{ textAlign: 'center', marginTop: 'var(--space-5)' }}>
          <Link href="/login" style={{ fontSize: 'var(--text-sm)', color: 'var(--color-primary)' }}>
            ← Customer Portal
          </Link>
        </div>
      </div>
    </div>
  );
}
