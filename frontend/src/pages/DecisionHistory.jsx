import React, { useState, useEffect } from 'react';
import Navbar from '../components/Navbar';
import DecisionTable from '../components/DecisionTable';
import Loader from '../components/Loader';
import { decisionAPI, feedbackAPI } from '../services/api';

const DecisionHistory = () => {
  const [history, setHistory] = useState([]);
  const [loading, setLoading] = useState(true);

  const fetchHistory = async () => {
    try {
      const res = await decisionAPI.getHistory(50);
      setHistory(res.data);
    } catch (err) {
      console.error(err);
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => {
    fetchHistory();
  }, []);

  const handleFeedback = async (decisionId) => {
    const delay = prompt("Enter ACTUAL delay days experienced in transit (e.g., 2.5):", "2.0");
    if (delay === null) return;
    const extraCost = prompt("Enter ACTUAL extra cost incurred ($):", "150");
    const rating = prompt("Rate intervention outcome satisfaction (1 to 5):", "5");

    try {
      await feedbackAPI.submit(
        decisionId,
        Number(delay),
        Number(extraCost || 0),
        Number(rating || 5),
        "Recorded via Closed-Loop Decision Audit"
      );
      alert("Feedback logged into PostgreSQL closed-loop database! Automated model retraining queued.");
      fetchHistory();
    } catch (err) {
      alert("Feedback submission failed");
    }
  };

  if (loading) return <Loader text="Loading Audit Trail & Decision Log..." />;

  return (
    <div>
      <Navbar title="Decision History & PostgreSQL Write-Back Audit" />
      <div className="page-wrapper">
        <div className="glass-card">
          <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', marginBottom: '1.25rem' }}>
            <div>
              <h2 style={{ color: 'white', fontSize: '1.25rem' }}>Historical Prescriptive Actions Audit</h2>
              <p style={{ color: 'var(--text-muted)', fontSize: '0.85rem' }}>
                Immutable log of user approvals, overrides, and closed-loop outcome feedback.
              </p>
            </div>
          </div>

          <DecisionTable history={history} onFeedbackSubmit={handleFeedback} />
        </div>
      </div>
    </div>
  );
};

export default DecisionHistory;
