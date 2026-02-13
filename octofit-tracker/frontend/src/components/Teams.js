import React, { useState, useEffect } from 'react';

function Teams() {
  const [teams, setTeams] = useState([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);

  useEffect(() => {
    const apiUrl = `https://${process.env.REACT_APP_CODESPACE_NAME}-8000.app.github.dev/api/teams/`;
    console.log('Fetching teams from:', apiUrl);
    
    fetch(apiUrl)
      .then(response => {
        console.log('Teams response status:', response.status);
        if (!response.ok) {
          throw new Error(`HTTP error! status: ${response.status}`);
        }
        return response.json();
      })
      .then(data => {
        console.log('Teams data received:', data);
        // Handle both paginated (.results) and plain array responses
        const teamsData = data.results || data;
        console.log('Processed teams data:', teamsData);
        setTeams(Array.isArray(teamsData) ? teamsData : []);
        setLoading(false);
      })
      .catch(error => {
        console.error('Error fetching teams:', error);
        setError(error.message);
        setLoading(false);
      });
  }, []);

  if (loading) {
    return (
      <div className="container page-container">
        <div className="loading-spinner">
          <div className="spinner-border text-primary" role="status">
            <span className="visually-hidden">Loading...</span>
          </div>
        </div>
      </div>
    );
  }
  
  if (error) {
    return (
      <div className="container page-container">
        <div className="error-message">
          <h4>⚠️ Error Loading Teams</h4>
          <p>{error}</p>
        </div>
      </div>
    );
  }

  return (
    <div className="container page-container">
      <div className="page-header">
        <h1>🏆 Teams</h1>
        <p className="text-muted">Explore teams and join the competition</p>
      </div>
      
      {teams.length === 0 ? (
        <div className="empty-state">
          <p>No teams found.</p>
        </div>
      ) : (
        <div className="row">
          {teams.map(team => (
            <div key={team.id} className="col-md-4 mb-4">
              <div className="card">
                <div className="card-header">
                  <h5 className="mb-0">{team.name}</h5>
                </div>
                <div className="card-body">
                  <p className="card-text">{team.description || 'No description available'}</p>
                  <hr />
                  <div className="d-flex justify-content-between align-items-center flex-wrap">
                    <span className="badge bg-primary mb-2">
                      👥 {team.member_count || 0} {team.member_count === 1 ? 'Member' : 'Members'}
                    </span>
                    <small className="text-muted mb-2">
                      <strong>Created:</strong> {new Date(team.created_at).toLocaleDateString()}
                    </small>
                  </div>
                </div>
              </div>
            </div>
          ))}
        </div>
      )}
    </div>
  );
}

export default Teams;
