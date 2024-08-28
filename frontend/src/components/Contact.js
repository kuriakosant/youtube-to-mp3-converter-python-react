import React from 'react';
import { FaEnvelope, FaGithub } from 'react-icons/fa';
import 'styles/Contact.css';  // Corrected import

function Contact() {
  return (
    <div className="contact-container">
      <h1>Contact Me</h1>
      <div className="contact-item">
        <FaEnvelope className="contact-icon" />
        <a href="mailto:kuriakosant2003@gmail.com" className="contact-link">kuriakosant2003@gmail.com</a>
      </div>
      <div className="contact-item">
        <FaGithub className="contact-icon" />
        <a href="https://github.com/kuriakosant" className="contact-link" target="_blank" rel="noopener noreferrer">
          github.com/kuriakosant
        </a>
      </div>
    </div>
  );
}

export default Contact;
