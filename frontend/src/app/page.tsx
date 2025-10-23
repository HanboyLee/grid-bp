"use client";

export default function HomePage() {
  return (
    <div className="space-y-6">
      <section className="bg-slate-900 rounded-xl shadow-lg p-6 border border-slate-800">
        <h2 className="text-2xl font-bold mb-4">Welcome</h2>
        <p className="text-slate-300 leading-relaxed">
          This is the Grid Trading Bot for the Backpack exchange. The application is currently
          in development. Features will be added incrementally according to the project
          documentation.
        </p>
      </section>

      <section className="grid grid-cols-1 md:grid-cols-3 gap-6">
        <div className="bg-slate-900 rounded-xl shadow-lg p-6 border border-slate-800">
          <h3 className="text-xl font-semibold mb-2">Strategy Status</h3>
          <p className="text-slate-400">Coming soon</p>
        </div>
        <div className="bg-slate-900 rounded-xl shadow-lg p-6 border border-slate-800">
          <h3 className="text-xl font-semibold mb-2">Current Price</h3>
          <p className="text-slate-400">Coming soon</p>
        </div>
        <div className="bg-slate-900 rounded-xl shadow-lg p-6 border border-slate-800">
          <h3 className="text-xl font-semibold mb-2">Total Capital</h3>
          <p className="text-slate-400">Coming soon</p>
        </div>
      </section>

      <section className="bg-slate-900 rounded-xl shadow-lg p-6 border border-slate-800">
        <h2 className="text-2xl font-bold mb-4">Quick Links</h2>
        <ul className="list-disc list-inside space-y-2 text-slate-300">
          <li>Configure trading parameters</li>
          <li>Monitor active orders</li>
          <li>View performance statistics</li>
          <li>Access full documentation</li>
        </ul>
      </section>
    </div>
  );
}
