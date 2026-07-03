import type { Metadata } from 'next';
import './globals.css';

export const metadata: Metadata = {
  title: {
    default: 'SBI Net Banking',
    template: '%s | SBI Net Banking',
  },
  description: 'State Bank of India — Secure, reliable internet banking for all your financial needs.',
  metadataBase: new URL('https://onlinesbi.sbi'),
};

export default function RootLayout({
  children,
}: {
  children: React.ReactNode;
}) {
  return (
    <html lang="en">
      <head>
        <link rel="preconnect" href="https://fonts.googleapis.com" />
        <link rel="preconnect" href="https://fonts.gstatic.com" crossOrigin="anonymous" />
      </head>
      <body>{children}</body>
    </html>
  );
}
