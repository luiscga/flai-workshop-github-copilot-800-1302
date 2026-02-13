import React, { useState, useEffect } from 'react';

function Leaderboard() {
  const [leaderboard, setLeaderboard] = useState([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);

  useEffect(() => {
    const apiUrl = `https://${process.env.REACT_APP_CODESPACE_NAME}-8000.app.github.dev/api/leaderboard/`;
    console.log('Fetching leaderboard from:', apiUrl);
    
    fetch(apiUrl)
      .then(response => {
        console.log('Leaderboard response status:', response.status);
        if (!response.ok) {
          throw new Error(`HTTP error! status: ${response.status}`);
        }
        return response.json();
      })
      .then(data => {
        console.log('Leaderboard data received:', data);
        // Handle both paginated (.results) and plain array responses
        const leaderboardData = data.results || data;
        console.log('Processed leaderboard data:', leaderboardData);
        setLeaderboard(Array.isArray(leaderboardData) ? leaderboardData : []);
        setLoading(false);
      })
      .catch(error => {
        console.error('Error fetching leaderboard:', error);
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
          <h4>⚠️ Error Loading Leaderboard</h4>
          <p>{error}</p>
        </div>
      </div>
    );
  }

  return (
    <div className="container page-container">
      <div className="page-header">
        <h1>📊 Leaderboard</h1>
        <p className="text-muted">Top performers in the OctoFit challenge</p>
      </div>
      
      {leaderboard.length === 0 ? (
        <div className="empty-state">
          <p>No leaderboard data available.</p>
        </div>
      ) : (
        <div className="table-responsive">
          <table className="table table-hover">
            <thead>
              <tr>
                <th style={{width: '80px'}}>Rank</th>
                <th>User</th>
                <th>Team</th>
                <th>Total Points</th>
              </tr>
            </thead>
            <tbody>
              {leaderboard.map((entry, index) => (
                <tr key={entry.id || index}>
                  <td>
                    <span className={`rank-badge ${
                      index === 0 ? 'rank-1' :
                      index === 1 ? 'rank-2' :
                      index === 2 ? 'rank-3' :
                      'rank-other'
                    }`}>
                      {index === 0 ? '🥇' : index === 1 ? '🥈' : index === 2 ? '🥉' : index + 1}
                    </span>
                  </td>
                  <td>
                    <strong>{entry.user_name || entry.user}</strong>
                  </td>
                  <td>
                    {entry.team_name ? (
                      <span className="badge bg-primary">{entry.team_name}</span>
                    ) : (
                      <span className="text-muted">No Team</span>
                    )}
                  </td>
                  <td>
                    <span className="badge bg-success" style={{fontSize: '1rem'}}>
                      {entry.total_points || 0} pts
                    </span>
                  </td>
                </tr>
              ))}
            </tbody>
          </table>
        </div>
      )}
    </div>
  );
}

export default Leaderboard;
