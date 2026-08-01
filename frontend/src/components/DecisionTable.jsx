import React from 'react';
import '../styles/table.css';

const DecisionTable = ({ history, onFeedbackSubmit }) => {
  return (
    <div className="custom-table-container">
      <table className="custom-table">
        <thead>
          <tr>
            <th>Decision ID</th>
            <th>Recommendation ID</th>
            <th>Action Taken</th>
            <th>Override Reason</th>
            <th>Timestamp</th>
            <th>Closed Loop Feedback</th>
          </tr>
        </thead>
        <tbody>
          {history && history.length > 0 ? (
            history.map((row) => (
              <tr key={row.id}>
                <td>#DEC-{row.id}</td>
                <td>#REC-{row.recommendation_id}</td>
                <td>
                  <span className={`badge ${row.action_taken === 'ACCEPTED' ? 'badge-low' : 'badge-high'}`}>
                    {row.action_taken}
                  </span>
                </td>
                <td>{row.override_reason || '-'}</td>
                <td style={{ color: 'var(--text-dim)', fontSize: '0.8rem' }}>
                  {new Date(row.timestamp).toLocaleString()}
                </td>
                <td>
                  {onFeedbackSubmit && (
                    <button
                      onClick={() => onFeedbackSubmit(row.id)}
                      style={{
                        padding: '0.35rem 0.75rem',
                        fontSize: '0.75rem',
                        background: 'rgba(99, 102, 241, 0.15)',
                        border: '1px solid rgba(99, 102, 241, 0.3)',
                        color: 'var(--primary)',
                        borderRadius: '6px',
                        fontWeight: 600
                      }}
                    >
                      Log Outcome Feedback
                    </button>
                  )}
                </td>
              </tr>
            ))
          ) : (
            <tr>
              <td colSpan="6" style={{ textAlign: 'center', color: 'var(--text-dim)', padding: '2rem' }}>
                No decision history recorded yet.
              </td>
            </tr>
          )}
        </tbody>
      </table>
    </div>
  );
};

export default DecisionTable;
