import type { Metadata } from "next";
import { Inter } from "next/font/google";
import "./globals.css";

const inter = Inter({ subsets: ["latin"] });

export const metadata: Metadata = {
  title: "Multi-Agent Financial Research Analyst",
  description: "Enterprise-grade AI research analyst automating financial earnings memo generation.",
};

export default function RootLayout({
  children,
}: {
  children: React.ReactNode;
}) {
  return (
    <html lang="en" className="dark">
      <body className={`${inter.className} bg-[#090d16] text-slate-100 min-h-screen`}>
        {children}
      </body>
    </html>
  );
}
