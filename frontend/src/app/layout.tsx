import type { Metadata } from 'next';
import './globals.css';

export const metadata: Metadata = {
  title: 'ClarityOS',
  description: 'A psychometric career assessment platform.',
};

export default function RootLayout({
  children,
}: {
  children: React.ReactNode;
}) {
  return (
    <html lang="en">
      <body className="bg-[#FBF8F1] text-[#0a1118] antialiased min-h-screen">
        {children}
      </body>
    </html>
  );
}