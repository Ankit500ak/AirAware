import React, { useEffect } from 'react';

const Home = () => {
  useEffect(() => {
    // Redirect to the HTML file directly
    window.location.href = '/home-enhanced.html';
  }, []);

  return null;
};

export default Home;
