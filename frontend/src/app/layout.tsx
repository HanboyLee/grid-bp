import "../styles/globals.css";
import type { ReactNode } from "react";

export const metadata = {
  title: "Backpack Grid Trading Bot",
  description: "Grid trading bot dashboard for Backpack exchange",
};

export default function RootLayout({ children }: { children: ReactNode }) {
  return (
    <html lang="en">
      <body className="bg-slate-950 text-slate-100 min-h-screen">
        <div className="mx-auto max-w-6xl px-6 py-8 space-y-8">
          <header className="flex flex-col gap-2">
            <h1 className="text-3xl font-bold">Backpack Grid Trading Bot</h1>
            <p className="text-slate-400">
              Monitor your automated perpetual futures grid strategy in real time.
            </p>
          </header>
          <main>{children}</main>
        </div>
      </body>
    </html>
  );
}
