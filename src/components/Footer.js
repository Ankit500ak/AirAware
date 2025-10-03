import React from 'react';
import styled from 'styled-components';

const FooterContainer = styled.footer`
  background: #333;
  color: white;
  padding: 2rem 0;
  margin-top: auto;
`;

const FooterContent = styled.div`
  max-width: 1200px;
  margin: 0 auto;
  padding: 0 2rem;
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(250px, 1fr));
  gap: 2rem;
`;

const FooterSection = styled.div`
  h3 {
    margin-bottom: 1rem;
    color: #667eea;
  }
  
  p, ul {
    margin: 0;
    padding: 0;
    line-height: 1.6;
  }
  
  ul {
    list-style: none;
  }
  
  a {
    color: #ccc;
    text-decoration: none;
    
    &:hover {
      color: white;
    }
  }
`;

const FooterBottom = styled.div`
  border-top: 1px solid #555;
  margin-top: 2rem;
  padding-top: 1rem;
  text-align: center;
  color: #ccc;
`;

const Footer = () => {
  return (
    <FooterContainer>
      <FooterContent>
        <FooterSection>
          <h3>Air Aware</h3>
          <p>Making air quality monitoring accessible and actionable for everyone.</p>
        </FooterSection>
        <FooterSection>
          <h3>Quick Links</h3>
          <ul>
            <li><a href="/">Home</a></li>
            <li><a href="/about">About</a></li>
            <li><a href="/services">Services</a></li>
            <li><a href="/contact">Contact</a></li>
          </ul>
        </FooterSection>
        <FooterSection>
          <h3>Contact Info</h3>
          <p>Email: info@airaware.com</p>
          <p>Phone: (555) 123-4567</p>
        </FooterSection>
      </FooterContent>
      <FooterBottom>
        <p>&copy; 2025 Air Aware. All rights reserved.</p>
      </FooterBottom>
    </FooterContainer>
  );
};

export default Footer;