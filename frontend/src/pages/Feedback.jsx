import React, { useState, useEffect } from 'react';
import Navbar from '../components/Navbar';
import Loader from '../components/Loader';
import { decisionAPI, feedbackAPI } from '../services/api';
import { MessageSquare, Send, Award } from 'lucide-react';

const Feedback = () => {
  const [decisions, setDecisions] = useState([]);
  const [selectedDecision, setSelectedDecision] = useState('');
  const [actualDelay, setActualDelay] = useState(1.5);
  const [actualExtraCost, setActualExtraCost] = useState(250);
  const [outcomeRating, setOutcomeRating] = useState(5);
  const [notes, setNotes] = useState('');
  const [loading, setLoading] = useState(true);
  const [submitting, setSubmitting] = useState(false);

  useEffect(() => {
    decisionAPI.getHistory(30).then(res => setDecisions(res.data)).catch(console.error).finally(() => setLoading(false));
  }, []);

  const handleSubmit = async (e) => {
    e.preventDefault();
    if (!selectedDecision) return;
    setSubmitting(true);
    try {
      await feedbackAPI.submit(
        Number(selectedDecision),
        Number(actualDelay),
        Number(actualExtraCost),
        Number(outcomeRating),
        notes
      );
      alert("Closed-loop feedback recorded! Model retraining pipeline notified.");
      setNotes('');
    } catch (err) {
      alert("Failed to submit feedback");
    } finally {
      setSubmitting(false);
    }
  };

  if (loading) return <Loader text="Fetching Decision Logs..." />;

  return (
    <div>
      <Navbar title="Closed-Loop Feedback Collection System" />
      <div className="page-wrapper">
        <div style={{ maxWidth: '650px', margin: '0 auto' }} className="glass-card">
          <div style={{ display: 'flex', alignItems: 'center', gap: '0.75rem', marginBottom: '1.5rem' }}>
            <div style={{ padding: '0.5rem', background: 'rgba(99, 102, 241, 0.1)', borderRadius: '10px', color: 'var(--primary)' }}>
              <MessageSquare size={24} />
            </div>
            <div>
              <h2 style={{ color: 'white', fontSize: '1.25rem' }}>Submit Operational Outcome</h2>
              <p style={{ color: 'var(--text-muted)', fontSize: '0.85rem' }}>
                Feed actual arrival dates and intervention costs back to retrain XGBoost models automatically.
              </p>
            </div>
          </div>

          <form onSubmit={handleSubmit}>
            <div className="form-group">
              <label className="form-label">Select Associated Decision Record</label>
              <select className="form-input" value={selectedDecision} onChange={(e) => setSelectedDecision(e.target.value)} required>
                <option value="">-- Choose Decision --</option>
                {decisions.map(d => (
                  <option key={d.id} value={d.id}>
                    #DEC-{d.id} | Action: {d.action_taken} ({new Date(d.timestamp).toLocaleDateString()})
                  </option>
                ))}
              </select>
            </div>

            <div style={{ display: 'grid', gridTemplateColumns: '1fr 1fr', gap: '1rem' }}>
              <div className="form-group">
                <label className="form-label">Actual Delay Experienced (Days)</label>
                <input type="number" step="0.5" className="form-input" value={actualDelay} onChange={(e) => setActualDelay(e.target.value)} required />
              </div>

              <div className="form-group">
                <label className="form-label">Actual Extra Cost Incurred ($)</label>
                <input type="number" className="form-input" value={actualExtraCost} onChange={(e) => setActualExtraCost(e.target.value)} required />
              </div>
            </div>

            <div className="form-group">
              <label className="form-label">Intervention Outcome Rating (1 to 5 Stars)</label>
              <select className="form-input" value={outcomeRating} onChange={(e) => setOutcomeRating(e.target.value)}>
                <option value="5">⭐⭐⭐⭐⭐ 5 - Highly Effective Prescription</option>
                <option value="4">⭐⭐⭐⭐ 4 - Good Outcome</option>
                <option value="3">⭐⭐⭐ 3 - Neutral</option>
                <option value="2">⭐⭐ 2 - Suboptimal</option>
                <option value="1">⭐ 1 - Ineffective Intervention</option>
              </select>
            </div>

            <div className="form-group">
              <label className="form-label">Operational Notes / Root Cause Findings</label>
              <textarea
                className="form-input"
                rows="3"
                placeholder="e.g. Typhoon delayed Shanghai port exit by 1.5 extra days despite priority air re-route..."
                value={notes}
                onChange={(e) => setNotes(e.target.value)}
              />
            </div>

            <button type="submit" className="btn-primary" disabled={submitting || !selectedDecision} style={{ width: '100%', display: 'flex', alignItems: 'center', justifyContent: 'center', gap: '0.5rem', marginTop: '1rem' }}>
              <Send size={18} />
              {submitting ? "Writing to PostgreSQL..." : "Submit Outcome to Retraining Loop"}
            </button>
          </form>
        </div>
      </div>
    </div>
  );
};

export default Feedback;
