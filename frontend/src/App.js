import React from 'react';
import { BrowserRouter as Router, Route, Routes } from 'react-router-dom';
import Home from 'components/Home';
import About from 'components/About';
import Contact from 'components/Contact';
import Header from 'components/Header';
import Footer from 'components/Footer';
import './App.css';

function App() {
  return (
    <Router>
      <div className="App">
        {/* Header */}
        <Header />
        
        {/* Page Routes */}
        <Routes>
          <Route path="/" element={<Home />} />
          <Route path="/about" element={<About />} />
          <Route path="/contact" element={<Contact />} />
        </Routes>

        {/* Footer */}
        <Footer />
      </div>
    </Router>
  );
}

export default App;
