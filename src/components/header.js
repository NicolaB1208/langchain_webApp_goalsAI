import React, { useState, useEffect } from 'react';


const Header = () => {
  const [name, setName] = useState(null);

useEffect(() => {
  // Fetch the username from the Flask server
  fetch('/get-username')
    .then(response => {
      if(response.ok) {
        return response.json();
      }
      throw response;
    })
    .then(data => setName(data.name))
    .catch(error => console.error("Error fetching name:", error));
}, []); // The empty array ensures this effect runs only once on mount
  
  return (
    <div className="header">
      
      {name? (
        <>
          <span>You are logged in as {name}.</span>
          <span><a href="/logout" className="login-text">Log out</a></span>
        </>
      ) : (
        <>
          <span>
          <a href="/login" className="login-text">Log in</a>
          </span>
          <span>
            <button className="signup-button" onClick={() => window.location.href='/signup'}>Sign up</button>
          </span>
        </>
      )}
    </div>
  );
};

export default Header;
