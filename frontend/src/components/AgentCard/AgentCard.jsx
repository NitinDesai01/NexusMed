import React from 'react';
import './AgentCard.css';

const AgentCard = ({ agent, onActivate }) => {
  const getStatusColor = (status) => {
    const colors = {
      active: 'green',
      inactive: 'gray',
      error: 'red',
      loading: 'yellow'
    };
    return colors[status] || 'gray';
  };

  const getStatusText = (status) => {
    const texts = {
      active: 'Active',
      inactive: 'Inactive',
      error: 'Error',
      loading: 'Loading...'
    };
    return texts[status] || status;
  };

  return (
    <div className={`agent-card status-${agent.status || 'inactive'}`}>
      <div className="agent-header">
        <div className="agent-icon">{agent.icon || '🤖'}</div>
        <div className="agent-info">
          <h3 className="agent-name">{agent.name}</h3>
          <p className="agent-description">{agent.description}</p>
        </div>
      </div>

      <div className="agent-status">
        <span className={`status-dot status-${agent.status || 'inactive'}`}></span>
        <span className="status-text">{getStatusText(agent.status)}</span>
      </div>

      {agent.metrics && (
        <div className="agent-metrics">
          {agent.metrics.map((metric, index) => (
            <div key={index} className="metric">
              <span className="metric-label">{metric.label}</span>
              <span className="metric-value">{metric.value}</span>
            </div>
          ))}
        </div>
      )}

      <div className="agent-actions">
        {onActivate && (
          <button
            onClick={() => onActivate(agent.id)}
            className="activate-btn"
            disabled={agent.status === 'active'}
          >
            {agent.status === 'active' ? 'Active' : 'Activate'}
          </button>
        )}
        <button className="details-btn">Details</button>
      </div>
    </div>
  );
};

export default AgentCard;