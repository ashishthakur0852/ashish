import { useState } from 'react';
import axios from 'axios';
import { useReportStore } from '../store/reportStore';

const DATASET_FIELDS: Record<string, string[]> = {
  fleet_performance: ['vessel_name', 'vessel_type', 'voyage_code', 'voyage_hours', 'cargo_tonnage'],
  fuel_efficiency: ['vessel_name', 'voyage_code', 'fuel_consumption_mt', 'avg_speed_knots', 'co2_emissions_mt'],
  maintenance_due: ['vessel_name', 'record_type', 'due_date', 'status', 'severity'],
  incident_safety: ['vessel_name', 'event_type', 'event_date', 'risk_level']
};

export function ReportBuilder() {
  const { selectedDataset, setDataset, selectedColumns, setColumns } = useReportStore();
  const [preview, setPreview] = useState<any[]>([]);

  const fields = DATASET_FIELDS[selectedDataset] || [];

  const runReport = async () => {
    const payload = { dataset: selectedDataset, columns: selectedColumns, page: 1, page_size: 25, filters: [], group_by: [], aggregations: [] };
    const { data } = await axios.post('http://localhost:8000/api/reports/run', payload);
    setPreview(data.rows);
  };

  return (
    <div className="builder-layout">
      <section className="panel">
        <h3>Report Builder</h3>
        <label>Dataset</label>
        <select value={selectedDataset} onChange={(e) => setDataset(e.target.value)}>
          {Object.keys(DATASET_FIELDS).map((ds) => <option key={ds} value={ds}>{ds}</option>)}
        </select>

        <label>Searchable Fields</label>
        <div className="field-list">
          {fields.map((f) => (
            <button key={f} onClick={() => setColumns(selectedColumns.includes(f) ? selectedColumns.filter((x) => x !== f) : [...selectedColumns, f])}>
              {selectedColumns.includes(f) ? '✓ ' : '+ '}{f}
            </button>
          ))}
        </div>
        <button className="primary" onClick={runReport}>Run Real-Time Preview</button>
      </section>

      <section className="panel preview">
        <h3>Live Preview</h3>
        <table>
          <thead>
            <tr>{selectedColumns.map((c) => <th key={c}>{c}</th>)}</tr>
          </thead>
          <tbody>
            {preview.map((row, idx) => (
              <tr key={idx}>{selectedColumns.map((c) => <td key={c}>{row[c]}</td>)}</tr>
            ))}
          </tbody>
        </table>
      </section>
    </div>
  );
}
