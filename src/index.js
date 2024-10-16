import React, { useState, useEffect } from 'react';
import ReactDOM from 'react-dom';
import Chatbot from './components/chatbot';
import Footer from './components/footer';
import Header from './components/header';
import './style.css';

function App() {
  const [goals, setGoals] = useState([]);

  useEffect(() => {
    const fetchGoals = () => {
      console.log('Fetching goals...');
      fetch('/goals')
        .then(response => response.json())
        .then(data => {
          console.log('Goals fetched:', data);
          setGoals(data);
        })
        .catch(error => console.error('Error fetching goals:', error));
    };

    fetchGoals(); 
    const intervalId = setInterval(fetchGoals, 5000); // Fetch goals every 5 seconds;

    return () => clearInterval(intervalId); 
  }, []);

  console.log('App rendering, goals:', goals);

  return (
    <div className="main-container"> {/* New wrapper div */}
      <Header />
      <div className="container">
        <GoalsDisplay goals={goals} />
        <Chatbot />
      </div>
      <Footer />
    </div>
  );
}

function GoalsDisplay({ goals }) {
  if (goals.length === 0) {
    return <div className="no-goals-message"></div>;
  }

  return (
    <div className="goals-display">
      {goals.map((goal, index) => (
        <div key={index} className="goal">
          <h2>Goal: {goal.name}</h2>
          <p className="goal-description">{goal.description}</p>
          <h3>Verbs Actions:</h3>
          <p className="goal-description">{goal.action_verbs}</p>
          <h3>Measurability:</h3>
          <p className="goal-description">{goal.measurability}</p>
        </div>
      ))}
    </div>
  );
}

ReactDOM.render(
  <App />,
  document.getElementById('root')
);