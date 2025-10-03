import React from 'react';
import { BrowserRouter as Router, Routes, Route, Navigate } from 'react-router-dom';
import styled from 'styled-components';

// Components
import Header from './components/Header';
import Footer from './components/Footer';
import Layout from './components/Layout';

// Pages
import About from './pages/About';
import Services from './pages/Services';
import Contact from './pages/Contact';

// Styled Components
const AppContainer = styled.div`
  min-height: 100vh;
  display: flex;
  flex-direction: column;
`;

// Component to redirect to HTML file
const HomeRedirect = () => {
  React.useEffect(() => {
    window.location.replace('/home-enhanced.html');
  }, []);
  return null;
};

function App() {
  return (
    <Router>
      <Routes>
        {/* Home route redirects to HTML file */}
        <Route path="/" element={<HomeRedirect />} />
        
        {/* Other routes with header, footer, and layout */}
        <Route path="/about" element={
          <AppContainer>
            <Header />
            <Layout>
              <About />
            </Layout>
            <Footer />
          </AppContainer>
        } />
        <Route path="/services" element={
          <AppContainer>
            <Header />
            <Layout>
              <Services />
            </Layout>
            <Footer />
          </AppContainer>
        } />
        <Route path="/contact" element={
          <AppContainer>
            <Header />
            <Layout>
              <Contact />
            </Layout>
            <Footer />
          </AppContainer>
        } />
      </Routes>
    </Router>
  );
}

export default App;
