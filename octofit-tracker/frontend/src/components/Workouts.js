import React, { useState, useEffect } from 'react';

function Workouts() {
  const [workouts, setWorkouts] = useState([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);

  useEffect(() => {
    const apiUrl = `https://${process.env.REACT_APP_CODESPACE_NAME}-8000.app.github.dev/api/workouts/`;
    console.log('Fetching workouts from:', apiUrl);
    
    fetch(apiUrl)
      .then(response => {
        console.log('Workouts response status:', response.status);
        if (!response.ok) {
          throw new Error(`HTTP error! status: ${response.status}`);
        }
        return response.json();
      })
      .then(data => {
        console.log('Workouts data received:', data);
        // Handle both paginated (.results) and plain array responses
        const workoutsData = data.results || data;
        console.log('Processed workouts data:', workoutsData);
        setWorkouts(Array.isArray(workoutsData) ? workoutsData : []);
        setLoading(false);
      })
      .catch(error => {
        console.error('Error fetching workouts:', error);
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
          <h4>⚠️ Error Loading Workouts</h4>
          <p>{error}</p>
        </div>
      </div>
    );
  }

  return (
    <div className="container page-container">
      <div className="page-header">
        <h1>💪 Suggested Workouts</h1>
        <p className="text-muted">Personalized workout recommendations for your fitness journey</p>
      </div>
      
      {workouts.length === 0 ? (
        <div className="empty-state">
          <p>No workouts available.</p>
        </div>
      ) : (
        <div className="row">
          {workouts.map(workout => (
            <div key={workout.id} className="col-md-6 col-lg-4 mb-4">
              <div className="card">
                <div className="card-header">
                  <h5 className="mb-0">{workout.name}</h5>
                </div>
                <div className="card-body">
                  <h6 className="card-subtitle mb-3">
                    <span className={`badge ${
                      workout.workout_type === 'Cardio' ? 'bg-danger' :
                      workout.workout_type === 'Strength' ? 'bg-dark' :
                      workout.workout_type === 'Flexibility' ? 'bg-success' :
                      workout.workout_type === 'HIIT' ? 'bg-warning' :
                      'bg-info'
                    }`}>
                      {workout.workout_type}
                    </span>
                  </h6>
                  <p className="card-text">{workout.description || 'No description available'}</p>
                  <hr />
                  <div className="d-flex justify-content-between align-items-center">
                    <span className={`badge ${
                      workout.difficulty_level === 'Advanced' ? 'bg-danger' :
                      workout.difficulty_level === 'Intermediate' ? 'bg-warning' :
                      'bg-success'
                    }`}>
                      {workout.difficulty_level}
                    </span>
                    <small className="text-muted">
                      <strong>{workout.duration_minutes}</strong> min
                    </small>
                  </div>
                  <div className="mt-2">
                    <small className="text-muted">
                      🔥 <strong>{workout.calories_burned}</strong> calories
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

export default Workouts;
