// EmailJS Configuration
// Note: In a frontend app, these values will be visible to users
// For production, consider using environment-specific builds

const EMAIL_CONFIG = {
    // EmailJS Credentials
    PUBLIC_KEY: 'crHauJ88UDzOS4puy',
    SERVICE_ID: 'service_gmail_001', // Replace with your actual service ID
    TEMPLATE_ID: 'template_sxw9783',
    
    // Contact Information
    CONTACT_EMAIL: 'ankit200211222@gmail.com',
    WEBSITE_URL: 'https://airaware.in',
    SUPPORT_PHONE: '+911123456789',
    
    // Form Configuration
    SUCCESS_MESSAGE: {
        title: '✨ Message Sent Successfully!',
        description: 'Thank you for reaching out! We\'ll respond within 24 hours.'
    },
    ERROR_MESSAGE: {
        title: '❌ Message Failed to Send',
        description: 'Please try again or email us directly at ankit200211222@gmail.com'
    }
};

// Export for use in other files (if using modules)
if (typeof module !== 'undefined' && module.exports) {
    module.exports = EMAIL_CONFIG;
}

// Make available globally for direct HTML usage
window.EMAIL_CONFIG = EMAIL_CONFIG;