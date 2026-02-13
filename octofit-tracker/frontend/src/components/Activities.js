import React, { useState, useEffect } from 'react';

function Activities() {
  const [activities, setActivities] = useState([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);

  useEffect(() => {
    const apiUrl = `https://${process.env.REACT_APP_CODESPACE_NAME}-8000.app.github.dev/api/activities/`;
    console.log('Fetching activities from:', apiUrl);
    
    fetch(apiUrl)
      .then(response => {
        console.log('Activities response status:', response.status);
        if (!response.ok) {
          throw new Error(`HTTP error! status: ${response.status}`);
        }
        return response.json();
      })
      .then(data => {
        console.log('Activities data received:', data);
        // Handle both paginated (.results) and plain array responses
        const activitiesData = data.results || data;
        console.log('Processed activities data:', activitiesData);
        setActivities(Array.isArray(activitiesData) ? activitiesData : []);
        setLoading(false);
      })
      .catch(error => {
        console.error('Error fetching activities:', error);
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
          <h4>⚠️ Error Loading Activities</h4>
          <p>{error}</p>
        </div>
      </div>
    );
  }

  return (
    <div className="container page-container">
      <div className="page-header">
        <h1>🏃 Activities</h1>
        <p className="text-muted">Track all fitness activities and progress</p>
      </div>
      
      {activities.length === 0 ? (
        <div className="empty-state">
          <p>No activities found.</p>
        </div>
      ) : (
        <div className="table-responsive">
          <table className="table table-hover">
            <thead>
              <tr>
                <th>User</th>
                <th>Activity Type</th>
                <th>Duration (min)</th>
                <th>Calories Burned</th>
                <th>Date</th>
              </tr>
            </thead>
            <tbody>
              {activities.map(activity => (
                <tr key={activity.id}>
                  <td>
                    <strong>{activity.user_name || activity.user}</strong>
                  </td>
                  <td>
                    <span className={`badge ${
                      activity.activity_type === 'Running' ? 'bg-danger' :
                      activity.activity_type === 'Cycling' ? 'bg-info' :
                      activity.activity_type === 'Swimming' ? 'bg-primary' :
                      activity.activity_type === 'Weightlifting' ? 'bg-dark' :
                      activity.activity_type === 'Yoga' ? 'bg-success' :
                      'bg-secondary'
                    }`}>
                      {activity.activity_type}
                    </span>
                  </td>
                  <td>{activity.duration_minutes} min</td>
                  <td>
                    <strong>{activity.calories_burned}</strong> kcal
                  </td>
                  <td>{new Date(activity.date).toLocaleDateString()}</td>
                </tr>
              ))}
            </tbody>
          </table>
        </div>
      )}
    </div>
  );
}

export default Activities;
