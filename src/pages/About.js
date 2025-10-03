import React from 'react';
import styled from 'styled-components';

const AboutContainer = styled.div`
  max-width: 800px;
  margin: 0 auto;
  padding: 2rem 0;
`;

const Title = styled.h1`
  color: #333;
  text-align: center;
  margin-bottom: 2rem;
`;

const Section = styled.section`
  margin-bottom: 3rem;
`;

const SectionTitle = styled.h2`
  color: #667eea;
  border-bottom: 2px solid #667eea;
  padding-bottom: 0.5rem;
  margin-bottom: 1rem;
`;

const Paragraph = styled.p`
  line-height: 1.8;
  color: #666;
  margin-bottom: 1rem;
`;

const TeamGrid = styled.div`
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(250px, 1fr));
  gap: 2rem;
  margin-top: 2rem;
`;

const TeamMember = styled.div`
  background: white;
  padding: 2rem;
  border-radius: 10px;
  box-shadow: 0 5px 15px rgba(0,0,0,0.1);
  text-align: center;
`;

const About = () => {
  return (
    <AboutContainer>
      <Title>About Air Aware</Title>
      
      <Section>
        <SectionTitle>Our Mission</SectionTitle>
        <Paragraph>
          Air Aware is dedicated to making air quality information accessible, understandable, 
          and actionable for communities worldwide. We believe that everyone deserves to breathe 
          clean air and have the tools to monitor and improve their environment.
        </Paragraph>
      </Section>

      <Section>
        <SectionTitle>What We Do</SectionTitle>
        <Paragraph>
          We provide real-time air quality monitoring through advanced sensor networks, 
          comprehensive data analytics, and user-friendly interfaces. Our platform helps 
          individuals, businesses, and communities make informed decisions about air quality.
        </Paragraph>
        <Paragraph>
          Our services include air quality monitoring, pollution source identification, 
          health impact assessments, and personalized recommendations for improving 
          indoor and outdoor air quality.
        </Paragraph>
      </Section>

      <Section>
        <SectionTitle>Our Team</SectionTitle>
        <TeamGrid>
          <TeamMember>
            <h3>Sarah Johnson</h3>
            <p>CEO & Founder</p>
            <p>Environmental Engineer with 10+ years experience in air quality research.</p>
          </TeamMember>
          <TeamMember>
            <h3>Mike Chen</h3>
            <p>CTO</p>
            <p>Software architect specializing in IoT and environmental monitoring systems.</p>
          </TeamMember>
          <TeamMember>
            <h3>Dr. Emily Rodriguez</h3>
            <p>Chief Scientist</p>
            <p>Atmospheric scientist with expertise in air pollution and climate change.</p>
          </TeamMember>
        </TeamGrid>
      </Section>
    </AboutContainer>
  );
};

export default About;