import type { Metadata } from 'next';
import UserNav from '@/components/user/UserNav';

export const metadata: Metadata = {
  title: {
    default: 'SBI Net Banking — Personal',
    template: '%s | SBI Net Banking',
  },
  description: 'Manage your SBI accounts, view transactions, and receive personalised banking offers.',
};

export default function UserLayout({ children }: { children: React.ReactNode }) {
  return (
    <div className="user-shell">
      <UserNav />
      <main className="user-main">{children}</main>
    </div>
  );
}
