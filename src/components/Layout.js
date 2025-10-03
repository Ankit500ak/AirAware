import React from 'react';
import { useLocation } from 'react-router-dom';
import styled from 'styled-components';

const LayoutContainer = styled.div`
  min-height: 100vh;
  display: flex;
  flex-direction: column;
`;

const MainContent = styled.main`
  flex: 1;
  padding: ${props => props.isHomePage ? '0' : '2rem'};
  max-width: ${props => props.isHomePage ? 'none' : '1200px'};
  margin: 0 auto;
  width: 100%;
`;

const Layout = ({ children }) => {
  const location = useLocation();
  const isHomePage = location.pathname === '/';

  return (
    <LayoutContainer>
      <MainContent isHomePage={isHomePage}>
        {children}
      </MainContent>
    </LayoutContainer>
  );
};

export default Layout;