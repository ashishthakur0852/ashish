import { BarChart, Bar, XAxis, YAxis, Tooltip, ResponsiveContainer, LineChart, Line } from 'recharts';

const kpis = [
  { label: 'Active Vessels', value: 54 },
  { label: 'Open Compliance Alerts', value: 117 },
  { label: 'Average Fuel / NM', value: '0.84' },
  { label: 'Voyages This Month', value: 488 }
];

const trendData = [
  { month: 'Jan', fuel: 21, fleet: 78 },
  { month: 'Feb', fuel: 20, fleet: 80 },
  { month: 'Mar', fuel: 22, fleet: 82 },
  { month: 'Apr', fuel: 19, fleet: 81 },
  { month: 'May', fuel: 18, fleet: 84 }
];

export function Dashboard() {
  return (
    <div className="dashboard">
      <div className="kpi-grid">
        {kpis.map((k) => <article key={k.label} className="kpi-card"><h4>{k.label}</h4><p>{k.value}</p></article>)}
      </div>
      <div className="chart-grid">
        <section className="panel">
          <h3>Fuel Efficiency Trend</h3>
          <ResponsiveContainer width="100%" height={260}>
            <LineChart data={trendData}><XAxis dataKey="month" /><YAxis /><Tooltip /><Line type="monotone" dataKey="fuel" stroke="#17a2b8" /></LineChart>
          </ResponsiveContainer>
        </section>
        <section className="panel">
          <h3>Fleet Performance Index</h3>
          <ResponsiveContainer width="100%" height={260}>
            <BarChart data={trendData}><XAxis dataKey="month" /><YAxis /><Tooltip /><Bar dataKey="fleet" fill="#0d6efd" /></BarChart>
          </ResponsiveContainer>
        </section>
      </div>
    </div>
  );
}
