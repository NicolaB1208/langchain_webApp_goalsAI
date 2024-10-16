import React from 'react';
import { FontAwesomeIcon } from '@fortawesome/react-fontawesome';
import { faLinkedin } from '@fortawesome/free-brands-svg-icons';
import { faEnvelope, faNewspaper } from '@fortawesome/free-solid-svg-icons';

const Footer = () => {
  return (
    <div className="footer">
      <span>Made by the Professional Beginner</span> {/* Use span instead of p */}
      <a href="https://www.linkedin.com/in/nicola-battoia/" target="_blank" rel="noopener noreferrer">
        <FontAwesomeIcon icon={ faLinkedin} size="sm" />
      </a>
      <a href="https://nicolabattoia.substack.com/" target="_blank" rel="noopener noreferrer">
        <FontAwesomeIcon icon={ faNewspaper } size="sm" />
      </a>
      <a href="mailto:nicola@fromzerotohere.it">
        <FontAwesomeIcon icon={ faEnvelope} size="sm" />
      </a>
    </div>
  );
};

export default Footer;