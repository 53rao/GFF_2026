import type { Metadata } from 'next';
import Link from 'next/link';

export const metadata: Metadata = {
  title: 'Login',
  description: 'Sign in to your SBI Net Banking account securely.',
};

export default function UserLoginPage() {
  return (
    <div className="login-page" style={{ marginTop: 'calc(-1 * (var(--nav-height) + var(--space-8)))', minHeight: '100vh' }}>
      {/* Hero Panel */}
      <div className="login-page__hero">
        <div
          className="login-page__hero-circle"
          style={{ width: 320, height: 320, top: -80, left: -80 }}
        />
        <div
          className="login-page__hero-circle"
          style={{ width: 200, height: 200, bottom: 60, right: -60 }}
        />

        {/* SBI Logo */}
        <div style={{ marginBottom: 'var(--space-8)', position: 'relative', zIndex: 1 }}>
          <div style={{
            width: 80, height: 80, background: 'white', borderRadius: 16,
            display: 'flex', alignItems: 'center', justifyContent: 'center',
            margin: '0 auto var(--space-5)',
            boxShadow: '0 8px 32px hsl(210 72% 20% / 0.4)',
          }}>
            <span style={{ fontSize: 28, fontWeight: 800, color: 'hsl(210,72%,38%)', letterSpacing: '-1px' }}>SBI</span>
          </div>
          <p style={{ fontSize: 'var(--text-xs)', textTransform: 'uppercase', letterSpacing: '0.12em', color: 'hsl(210 60% 80%)', fontWeight: 600 }}>
            State Bank of India
          </p>
        </div>

        <h1 className="login-page__hero-title">Your Bank.<br />Anytime, Anywhere.</h1>
        <p className="login-page__hero-sub">
          Secure internet banking for over 500 million customers. Manage accounts, transfer funds, pay bills, and more — all from one place.
        </p>

        <div style={{ marginTop: 'var(--space-10)', display: 'flex', gap: 'var(--space-6)', position: 'relative', zIndex: 1 }}>
          {[
            { label: '500M+', desc: 'Customers' },
            { label: '22,000+', desc: 'Branches' },
            { label: '99.9%', desc: 'Uptime' },
          ].map(({ label, desc }) => (
            <div key={label} style={{ textAlign: 'center' }}>
              <div style={{ fontSize: 'var(--text-xl)', fontWeight: 700, color: 'white' }}>{label}</div>
              <div style={{ fontSize: 'var(--text-xs)', color: 'hsl(210 60% 78%)', marginTop: 2 }}>{desc}</div>
            </div>
          ))}
        </div>
      </div>

      {/* Form Pane */}
      <div className="login-page__form-pane">
        <form className="login-form" aria-label="SBI Net Banking Login">
          {/* Brand mark on form side */}
          <div className="login-form__logo">
            <div style={{
              width: 42, height: 42, background: 'var(--color-primary)', borderRadius: 10,
              display: 'flex', alignItems: 'center', justifyContent: 'center',
              flexShrink: 0,
            }}>
              <span style={{ fontWeight: 800, color: 'white', fontSize: 13, letterSpacing: '-0.5px' }}>SBI</span>
            </div>
            <div>
              <div style={{ fontSize: 'var(--text-sm)', fontWeight: 700, color: 'var(--color-text-primary)' }}>OnlineSBI</div>
              <div style={{ fontSize: 'var(--text-xs)', color: 'var(--color-text-secondary)' }}>Personal Banking</div>
            </div>
          </div>

          <h2 className="login-form__heading">Welcome back</h2>
          <p className="login-form__sub">Sign in to your account to continue.</p>

          <div className="form-group">
            <label className="form-label" htmlFor="username">Username / CIF Number</label>
            <input
              id="username"
              type="text"
              className="form-input"
              placeholder="Enter your username"
              autoComplete="username"
            />
          </div>

          <div className="form-group">
            <label className="form-label" htmlFor="password">Password</label>
            <input
              id="password"
              type="password"
              className="form-input"
              placeholder="Enter your password"
              autoComplete="current-password"
            />
          </div>

          <div style={{ display: 'flex', alignItems: 'center', justifyContent: 'space-between', marginBottom: 'var(--space-6)' }}>
            <label style={{ display: 'flex', alignItems: 'center', gap: 'var(--space-2)', fontSize: 'var(--text-sm)', color: 'var(--color-text-secondary)', cursor: 'pointer' }}>
              <input type="checkbox" id="remember-me" /> Remember me
            </label>
            <a href="#" style={{ fontSize: 'var(--text-sm)', color: 'var(--color-primary)', fontWeight: 500 }}>Forgot password?</a>
          </div>

          <Link href="/dashboard" className="btn btn--primary btn--full btn--lg" id="user-login-btn">
            Sign In Securely
          </Link>

          <div style={{ textAlign: 'center', marginTop: 'var(--space-6)', fontSize: 'var(--text-xs)', color: 'var(--color-text-tertiary)' }}>
            🔒 Protected by 256-bit SSL encryption
          </div>

          <hr style={{ margin: 'var(--space-6) 0', borderColor: 'var(--color-border-light)' }} />

          <div style={{ textAlign: 'center', fontSize: 'var(--text-sm)', color: 'var(--color-text-secondary)' }}>
            New to SBI?{' '}
            <a href="#" style={{ color: 'var(--color-primary)', fontWeight: 600 }}>Register Online</a>
          </div>

          <div style={{ textAlign: 'center', marginTop: 'var(--space-3)' }}>
            <Link href="/admin/login" style={{ fontSize: 'var(--text-xs)', color: 'var(--color-text-tertiary)' }}>
              Admin / Staff Portal →
            </Link>
          </div>
        </form>
      </div>
    </div>
  );
}
