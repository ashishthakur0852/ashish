import { Dashboard } from '../components/Dashboard';
import { ReportBuilder } from '../components/ReportBuilder';
import { useReportStore } from '../store/reportStore';

export function App() {
  const { darkMode, toggleDarkMode, role, setRole } = useReportStore();

  return (
    <div className={darkMode ? 'app dark' : 'app'}>
      <aside className="sidebar">
        <h2>MarineOps Insight</h2>
        <nav>
          <a>Dashboard</a>
          <a>Dynamic Reports</a>
          <a>Templates</a>
          <a>Automation</a>
        </nav>
      </aside>
      <main>
        <header className="topbar">
          <div>Fleet Operations / Dynamic Reporting</div>
          <div className="actions">
            <select value={role} onChange={(e) => setRole(e.target.value as any)}>
              <option value="operations">Operations Team</option>
              <option value="compliance">Compliance Officer</option>
              <option value="executive">Executive</option>
              <option value="ship_officer">Ship Officer</option>
            </select>
            <button onClick={toggleDarkMode}>Toggle Theme</button>
          </div>
        </header>
        <Dashboard />
        <ReportBuilder />
      </main>
    </div>
  );
}
