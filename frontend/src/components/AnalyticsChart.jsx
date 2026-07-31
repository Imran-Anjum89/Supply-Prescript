import React from 'react';
import { ResponsiveContainer, BarChart, Bar, XAxis, YAxis, Tooltip, PieChart, Pie, Cell } from 'recharts';

const COLORS = ['#10B981', '#F59E0B', '#EF4444', '#9333EA'];

export const RiskPieChart = ({ data }) => {
  const chartData = [
    { name: 'Low Risk', value: data?.LOW || 5 },
    { name: 'Medium Risk', value: data?.MEDIUM || 3 },
    { name: 'High Risk', value: data?.HIGH || 4 },
    { name: 'Critical Risk', value: data?.CRITICAL || 2 },
  ];

  return (
    <div style={{ height: 260, width: '100%' }}>
      <ResponsiveContainer>
        <PieChart>
          <Pie
            data={chartData}
            cx="50%"
            cy="50%"
            innerRadius={60}
            outerRadius={90}
            paddingAngle={5}
            dataKey="value"
          >
            {chartData.map((entry, index) => (
              <Cell key={`cell-${index}`} fill={COLORS[index % COLORS.length]} />
            ))}
          </Pie>
          <Tooltip
            contentStyle={{ background: '#121826', borderColor: 'rgba(255,255,255,0.1)', borderRadius: '8px', color: '#fff' }}
          />
        </PieChart>
      </ResponsiveContainer>
      <div style={{ display: 'flex', justifyContent: 'center', gap: '1rem', flexWrap: 'wrap', fontSize: '0.75rem' }}>
        {chartData.map((item, idx) => (
          <div key={item.name} style={{ display: 'flex', alignItems: 'center', gap: '0.3rem', color: 'var(--text-muted)' }}>
            <span style={{ width: 8, height: 8, borderRadius: '50%', background: COLORS[idx] }} />
            {item.name} ({item.value})
          </div>
        ))}
      </div>
    </div>
  );
};

export const DecisionBarChart = ({ data }) => {
  const chartData = [
    { name: 'Accepted', count: data?.accepted || 12, fill: '#10B981' },
    { name: 'Overridden', count: data?.overridden || 3, fill: '#F59E0B' },
    { name: 'Rejected', count: data?.rejected || 1, fill: '#EF4444' },
  ];

  return (
    <div style={{ height: 260, width: '100%' }}>
      <ResponsiveContainer>
        <BarChart data={chartData} margin={{ top: 20, right: 30, left: 0, bottom: 5 }}>
          <XAxis dataKey="name" stroke="#9CA3AF" fontSize={12} />
          <YAxis stroke="#9CA3AF" fontSize={12} />
          <Tooltip contentStyle={{ background: '#121826', borderColor: 'rgba(255,255,255,0.1)', borderRadius: '8px', color: '#fff' }} />
          <Bar dataKey="count" radius={[6, 6, 0, 0]}>
            {chartData.map((entry, index) => (
              <Cell key={`bar-${index}`} fill={entry.fill} />
            ))}
          </Bar>
        </BarChart>
      </ResponsiveContainer>
    </div>
  );
};
