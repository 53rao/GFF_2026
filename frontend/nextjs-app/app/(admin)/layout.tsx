import type { Metadata } from 'next';
import AdminSidebar from '@/components/admin/AdminSidebar';

export const metadata: Metadata = {
  title: {
    default: 'SBI Operations Hub',
    template: '%s | SBI Operations Hub',
  },
  description: 'SBI internal operations dashboard — case management, agent pipeline, and handoff tracking.',
};

export default function AdminLayout({ children }: { children: React.ReactNode }) {
  return (
    <div className="admin-shell">
      <AdminSidebar />
      <main className="admin-main">{children}</main>
    </div>
  );
}
