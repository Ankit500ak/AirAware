import React from 'react';
import styled from 'styled-components';

const ServicesContainer = styled.div`
  padding: 2rem 0;
`;

const Title = styled.h1`
  color: #333;
  text-align: center;
  margin-bottom: 3rem;
`;

const ServicesGrid = styled.div`
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(350px, 1fr));
  gap: 2rem;
  margin-bottom: 3rem;
`;

const ServiceCard = styled.div`
  background: white;
  padding: 2rem;
  border-radius: 10px;
  box-shadow: 0 5px 15px rgba(0,0,0,0.1);
  transition: transform 0.3s;
  
  &:hover {
    transform: translateY(-5px);
  }
`;

const ServiceIcon = styled.div`
  font-size: 3rem;
  margin-bottom: 1rem;
  text-align: center;
`;

const ServiceTitle = styled.h3`
  color: #667eea;
  margin-bottom: 1rem;
  text-align: center;
`;

const ServiceDescription = styled.p`
  color: #666;
  line-height: 1.6;
  margin-bottom: 1rem;
`;

const ServiceFeatures = styled.ul`
  color: #666;
  line-height: 1.6;
  
  li {
    margin-bottom: 0.5rem;
  }
`;

const CTASection = styled.section`
  background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
  color: white;
  padding: 3rem 2rem;
  border-radius: 10px;
  text-align: center;
  margin-top: 3rem;
`;

const CTATitle = styled.h2`
  margin-bottom: 1rem;
`;

const CTAButton = styled.button`
  background: white;
  color: #667eea;
  border: none;
  padding: 1rem 2rem;
  font-size: 1.1rem;
  border-radius: 5px;
  cursor: pointer;
  font-weight: bold;
  transition: transform 0.3s;
  
  &:hover {
    transform: translateY(-2px);
  }
`;

const Services = () => {
  return (
    <ServicesContainer>
      <Title>Our Services</Title>
      
      <ServicesGrid>
        <ServiceCard>
          <ServiceIcon>🌍</ServiceIcon>
          <ServiceTitle>Environmental Monitoring</ServiceTitle>
          <ServiceDescription>
            Comprehensive air quality monitoring for outdoor environments using 
            state-of-the-art sensor networks.
          </ServiceDescription>
          <ServiceFeatures>
            <li>Real-time PM2.5, PM10, and ozone monitoring</li>
            <li>Weather correlation analysis</li>
            <li>Pollution source identification</li>
            <li>Historical data and trends</li>
          </ServiceFeatures>
        </ServiceCard>

        <ServiceCard>
          <ServiceIcon>🏢</ServiceIcon>
          <ServiceTitle>Indoor Air Quality</ServiceTitle>
          <ServiceDescription>
            Monitor and improve indoor air quality in homes, offices, and commercial spaces.
          </ServiceDescription>
          <ServiceFeatures>
            <li>VOC and CO2 level monitoring</li>
            <li>Humidity and temperature tracking</li>
            <li>Air purifier recommendations</li>
            <li>Ventilation optimization</li>
          </ServiceFeatures>
        </ServiceCard>

        <ServiceCard>
          <ServiceIcon>📱</ServiceIcon>
          <ServiceTitle>Mobile Monitoring</ServiceTitle>
          <ServiceDescription>
            Portable air quality monitoring solutions for personal and professional use.
          </ServiceDescription>
          <ServiceFeatures>
            <li>Personal exposure tracking</li>
            <li>Mobile app integration</li>
            <li>GPS-enabled data logging</li>
            <li>Health impact assessments</li>
          </ServiceFeatures>
        </ServiceCard>

        <ServiceCard>
          <ServiceIcon>🏭</ServiceIcon>
          <ServiceTitle>Industrial Solutions</ServiceTitle>
          <ServiceDescription>
            Specialized monitoring and compliance solutions for industrial facilities.
          </ServiceDescription>
          <ServiceFeatures>
            <li>Emissions monitoring</li>
            <li>Regulatory compliance reporting</li>
            <li>Process optimization</li>
            <li>Environmental impact assessment</li>
          </ServiceFeatures>
        </ServiceCard>

        <ServiceCard>
          <ServiceIcon>🎓</ServiceIcon>
          <ServiceTitle>Research & Consulting</ServiceTitle>
          <ServiceDescription>
            Expert consultation and research services for environmental projects.
          </ServiceDescription>
          <ServiceFeatures>
            <li>Air quality studies</li>
            <li>Policy development support</li>
            <li>Custom research projects</li>
            <li>Data analysis and reporting</li>
          </ServiceFeatures>
        </ServiceCard>

        <ServiceCard>
          <ServiceIcon>🔔</ServiceIcon>
          <ServiceTitle>Alert Systems</ServiceTitle>
          <ServiceDescription>
            Smart notification systems to keep you informed about air quality changes.
          </ServiceDescription>
          <ServiceFeatures>
            <li>Real-time alerts</li>
            <li>Customizable thresholds</li>
            <li>Multi-channel notifications</li>
            <li>Health recommendations</li>
          </ServiceFeatures>
        </ServiceCard>
      </ServicesGrid>

      <CTASection>
        <CTATitle>Ready to Get Started?</CTATitle>
        <p>Contact us today to learn more about how our services can help you monitor and improve air quality.</p>
        <CTAButton>Contact Us</CTAButton>
      </CTASection>
    </ServicesContainer>
  );
};

export default Services;