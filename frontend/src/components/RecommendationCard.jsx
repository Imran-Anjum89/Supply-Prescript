import React, { useState } from 'react';
import { CheckCircle2, AlertCircle, XCircle, Sliders, DollarSign, Clock, Zap } from 'lucide-react';

const RecommendationCard = ({ recommendation, onDecision }) => {
  const [overrideReason, setOverrideReason] = useState('');
  const [showOverride, setShowOverride] = useState(false);

  if (!recommendation) return null;

  return (
    <div className="glass-card" style={{ borderLeft: '4px solid var(--primary)' }}>
      <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'flex-start', marginBottom: '1rem' }}>
        <div>
          <div style={{ display: 'flex', alignItems: 'center', gap: '0.5rem' }}>
            <Sliders size={20} color="var(--accent-cyan)" />
            <h3 style={{ color: 'white', fontSize: '1.1rem' }}>PuLP Prescriptive Recommendation</h3>
          </div>
          <p style={{ fontSize: '0.8rem', color: 'var(--text-muted)', marginTop: '0.2rem' }}>
            Optimal Mixed-Integer Solution
          </p>
        </div>

        <span className="badge badge-low" style={{ background: 'rgba(34, 211, 238, 0.15)', color: '#22D3EE', border: '1px solid rgba(34, 211, 238, 0.3)' }}>
          ROI {recommendation.roi_score}x
        </span>
      </div>

      <div style={{ background: 'rgba(99, 102, 241, 0.08)', padding: '1.25rem', borderRadius: '12px', border: '1px solid rgba(99, 102, 241, 0.2)', marginBottom: '1.25rem' }}>
        <div style={{ fontSize: '0.75rem', fontWeight: 600, color: 'var(--primary)', textTransform: 'uppercase', letterSpacing: '0.05em' }}>
          Optimal Prescribed Strategy
        </div>
        <div style={{ fontSize: '1.2rem', fontWeight: 700, color: 'white', marginTop: '0.25rem' }}>
          {recommendation.suggested_action}
        </div>
        {recommendation.expedited_carrier && (
          <div style={{ fontSize: '0.85rem', color: 'var(--text-muted)', marginTop: '0.2rem' }}>
            Partner: <span style={{ color: 'white', fontWeight: 500 }}>{recommendation.expedited_carrier}</span>
          </div>
        )}
      </div>

      <div style={{ display: 'grid', gridTemplateColumns: '1fr 1fr', gap: '1rem', marginBottom: '1.25rem' }}>
        <div style={{ background: 'rgba(0,0,0,0.2)', padding: '0.85rem 1rem', borderRadius: '10px' }}>
          <div style={{ display: 'flex', alignItems: 'center', gap: '0.4rem', fontSize: '0.8rem', color: 'var(--text-dim)' }}>
            <DollarSign size={14} color="#F59E0B" />
            Extra Intervention Cost
          </div>
          <div style={{ fontSize: '1.25rem', fontWeight: 700, color: 'white', marginTop: '0.2rem' }}>
            ${recommendation.estimated_extra_cost}
          </div>
        </div>

        <div style={{ background: 'rgba(0,0,0,0.2)', padding: '0.85rem 1rem', borderRadius: '10px' }}>
          <div style={{ display: 'flex', alignItems: 'center', gap: '0.4rem', fontSize: '0.8rem', color: 'var(--text-dim)' }}>
            <Clock size={14} color="#34D399" />
            Transit Days Saved
          </div>
          <div style={{ fontSize: '1.25rem', fontWeight: 700, color: '#34D399', marginTop: '0.2rem' }}>
            {recommendation.time_saved_days} Days
          </div>
        </div>
      </div>

      {recommendation.status === 'PENDING' ? (
        <div>
          {!showOverride ? (
            <div style={{ display: 'flex', gap: '0.75rem' }}>
              <button
                onClick={() => onDecision(recommendation.id, 'ACCEPTED')}
                className="btn-primary"
                style={{ flex: 1, display: 'flex', alignItems: 'center', justifyContent: 'center', gap: '0.4rem', background: 'linear-gradient(135deg, #10B981 0%, #059669 100%)' }}
              >
                <CheckCircle2 size={18} />
                Accept Strategy
              </button>
              <button
                onClick={() => setShowOverride(true)}
                style={{ flex: 1, padding: '0.75rem', background: 'rgba(255,255,255,0.05)', border: '1px solid var(--border-color)', borderRadius: 'var(--radius-sm)', color: 'white', fontWeight: 600 }}
              >
                Override Strategy
              </button>
            </div>
          ) : (
            <div style={{ background: 'rgba(0,0,0,0.3)', padding: '1rem', borderRadius: '10px', border: '1px solid var(--border-color)' }}>
              <label style={{ fontSize: '0.8rem', color: 'var(--text-muted)', display: 'block', marginBottom: '0.4rem' }}>
                Reason for Overriding Prescribed Action:
              </label>
              <input
                type="text"
                className="form-input"
                placeholder="e.g. Budget constraint approved by CFO"
                value={overrideReason}
                onChange={(e) => setOverrideReason(e.target.value)}
                style={{ marginBottom: '0.75rem' }}
              />
              <div style={{ display: 'flex', gap: '0.5rem' }}>
                <button
                  onClick={() => onDecision(recommendation.id, 'OVERRIDDEN', overrideReason)}
                  className="btn-primary"
                  style={{ flex: 1, fontSize: '0.85rem', padding: '0.5rem' }}
                >
                  Submit Override
                </button>
                <button
                  onClick={() => setShowOverride(false)}
                  style={{ padding: '0.5rem 1rem', background: 'transparent', color: 'var(--text-muted)', fontSize: '0.85rem' }}
                >
                  Cancel
                </button>
              </div>
            </div>
          )}
        </div>
      ) : (
        <div style={{ fontSize: '0.85rem', color: 'var(--text-dim)', textAlign: 'center', fontStyle: 'italic', paddingTop: '0.5rem', borderTop: '1px solid var(--border-color)' }}>
          Decision Recorded: <strong style={{ color: 'white' }}>{recommendation.status}</strong>
        </div>
      )}
    </div>
  );
};

export default RecommendationCard;
