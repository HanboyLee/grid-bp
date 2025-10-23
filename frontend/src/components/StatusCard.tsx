"use client";

import type { ReactNode } from "react";

interface StatusCardProps {
  title: string;
  value: ReactNode;
  description?: string;
}

export function StatusCard({ title, value, description }: StatusCardProps) {
  return (
    <div className="bg-slate-900 rounded-xl shadow-lg p-6 border border-slate-800">
      <h3 className="text-xl font-semibold mb-2">{title}</h3>
      <div className="text-3xl font-bold mb-1">{value}</div>
      {description ? <p className="text-slate-400 text-sm">{description}</p> : null}
    </div>
  );
}
