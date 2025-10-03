# 📧 EmailJS Setup Guide for AirAware Contact Form

## 🚀 Quick Setup (5 minutes)

### Step 1: Create EmailJS Account
1. Go to [EmailJS.com](https://www.emailjs.com/)
2. Sign up for a free account
3. Verify your email address

### Step 2: Connect Your Email Service
1. In EmailJS dashboard, go to **"Email Services"**
2. Click **"Add New Service"**
3. Choose your email provider:
   - **Gmail** (recommended for testing)
   - **Outlook/Hotmail**
   - **Yahoo**
   - **Other SMTP**

4. Follow the setup instructions for your chosen service
5. **Note your SERVICE_ID** (e.g., `service_abc123`)

### Step 3: Create Email Template
1. Go to **"Email Templates"**
2. Click **"Create New Template"**
3. **Configure the template settings:**

**Template Settings:**
- **To Email:** `ankit200211222@gmail.com` (Your email where you want to receive messages)
- **From Name:** `{{from_name}}` (The sender's name from the form)
- **From Email:** `{{from_email}}` (The sender's email from the form)
- **Use Default Email Address:** ✅ Check this box
- **Reply To:** `{{from_email}}` (So you can reply directly to the sender)
- **Bcc:** Leave empty (unless you want copies sent elsewhere)
- **Cc:** Leave empty (unless you want copies sent elsewhere)

**Subject:**
```
🌍 New Contact from AirAware: {{subject}}
```

**Body:**
```html
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>New Contact from AirAware</title>
</head>
<body style="margin: 0; padding: 0; background: linear-gradient(135deg, #0f172a 0%, #1e293b 100%); font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, 'Helvetica Neue', Arial, sans-serif; min-height: 100vh;">
    
    <!-- Email Container -->
    <div style="max-width: 600px; margin: 20px auto; background: linear-gradient(135deg, #1e293b 0%, #0f172a 100%); border-radius: 20px; overflow: hidden; box-shadow: 0 25px 50px rgba(0,0,0,0.25); border: 1px solid rgba(148,163,184,0.1);">
        
        <!-- Header Section -->
        <div style="background: linear-gradient(135deg, #14b8a6 0%, #0d9488 100%); padding: 40px 30px; text-align: center; position: relative; overflow: hidden;">
            <!-- Background Pattern -->
            <div style="position: absolute; top: 0; left: 0; right: 0; bottom: 0; background: url('data:image/svg+xml;base64,PHN2ZyB3aWR0aD0iNDAiIGhlaWdodD0iNDAiIHZpZXdCb3g9IjAgMCA0MCA0MCIgZmlsbD0ibm9uZSIgeG1sbnM9Imh0dHA6Ly93d3cudzMub3JnLzIwMDAvc3ZnIj4KPGNpcmNsZSBjeD0iMjAiIGN5PSIyMCIgcj0iMSIgZmlsbD0icmdiYSgyNTUsMjU1LDI1NSwwLjEpIi8+Cjwvc3ZnPg==') repeat; opacity: 0.3;"></div>
            
            <div style="position: relative; z-index: 2;">
                <div style="display: inline-flex; align-items: center; gap: 12px; margin-bottom: 16px;">
                    <div style="width: 48px; height: 48px; background: rgba(255,255,255,0.15); border-radius: 16px; display: flex; align-items: center; justify-content: center; backdrop-filter: blur(10px); border: 1px solid rgba(255,255,255,0.2);">
                        <span style="font-size: 24px;">🌍</span>
                    </div>
                    <h1 style="color: white; margin: 0; font-size: 32px; font-weight: 700; text-shadow: 0 4px 8px rgba(0,0,0,0.3); font-family: 'Great Vibes', cursive;">AirAware</h1>
                </div>
                
                <div style="background: rgba(255,255,255,0.1); padding: 12px 24px; border-radius: 25px; display: inline-block; margin-bottom: 12px; backdrop-filter: blur(10px); border: 1px solid rgba(255,255,255,0.2);">
                    <span style="color: white; font-size: 14px; font-weight: 600; display: flex; align-items: center; gap: 8px;">
                        <span style="width: 8px; height: 8px; background: #f59e0b; border-radius: 50%; animation: pulse 2s infinite;"></span>
                        New Contact Inquiry
                    </span>
                </div>
                
                <p style="color: rgba(255,255,255,0.9); margin: 0; font-size: 16px; font-weight: 500;">Delhi-NCR Air Quality Management Platform</p>
            </div>
        </div>

        <!-- Main Content -->
        <div style="padding: 32px 28px; background: linear-gradient(135deg, #1e293b 0%, #0f172a 100%);">
            
            <!-- Contact Information Card -->
            <div style="background: rgba(30,41,59,0.4); border-radius: 16px; padding: 28px; margin-bottom: 24px; border: 1px solid rgba(148,163,184,0.1); backdrop-filter: blur(10px);">
                <h2 style="color: #f1f5f9; margin: 0 0 24px 0; font-size: 20px; font-weight: 700; display: flex; align-items: center; gap: 12px;">
                    <div style="width: 32px; height: 32px; background: linear-gradient(135deg, #14b8a6 0%, #0d9488 100%); border-radius: 10px; display: flex; align-items: center; justify-content: center;">
                        <span style="font-size: 16px;">👤</span>
                    </div>
                    Contact Details
                </h2>
                
                <div style="display: grid; gap: 20px;">
                    <!-- Email -->
                    <div style="background: rgba(20,184,166,0.05); border-radius: 12px; padding: 16px; border-left: 3px solid #14b8a6;">
                        <div style="color: #14b8a6; font-size: 12px; font-weight: 600; margin-bottom: 6px; text-transform: uppercase; letter-spacing: 0.5px;">📧 Email Address</div>
                        <a href="mailto:{{from_email}}" style="color: #e2e8f0; text-decoration: none; font-weight: 600; font-size: 16px; word-break: break-all; display: block;">{{from_email}}</a>
                    </div>
                    
                    <!-- Name -->
                    <div style="background: rgba(59,130,246,0.05); border-radius: 12px; padding: 16px; border-left: 3px solid #3b82f6;">
                        <div style="color: #60a5fa; font-size: 12px; font-weight: 600; margin-bottom: 6px; text-transform: uppercase; letter-spacing: 0.5px;">👨 Full Name</div>
                        <div style="color: #e2e8f0; font-weight: 600; font-size: 16px;">{{from_name}}</div>
                    </div>
                    
                    <!-- Organization -->
                    <div style="background: rgba(139,92,246,0.05); border-radius: 12px; padding: 16px; border-left: 3px solid #8b5cf6;">
                        <div style="color: #a78bfa; font-size: 12px; font-weight: 600; margin-bottom: 6px; text-transform: uppercase; letter-spacing: 0.5px;">🏢 Organization</div>
                        <div style="color: #e2e8f0; font-weight: 600; font-size: 16px;">{{organization}}</div>
                    </div>
                    
                    <!-- User Type -->
                    <div style="background: rgba(245,158,11,0.05); border-radius: 12px; padding: 16px; border-left: 3px solid #f59e0b;">
                        <div style="color: #fbbf24; font-size: 12px; font-weight: 600; margin-bottom: 8px; text-transform: uppercase; letter-spacing: 0.5px;">👥 User Type</div>
                        <span style="background: linear-gradient(135deg, #f59e0b 0%, #d97706 100%); color: white; padding: 8px 16px; border-radius: 20px; font-size: 13px; font-weight: 700; display: inline-block; text-transform: capitalize; box-shadow: 0 4px 12px rgba(245,158,11,0.3);">{{user_type}}</span>
                    </div>
                </div>
            </div>

            <!-- Subject Section -->
            <div style="background: rgba(59,130,246,0.1); border-radius: 16px; padding: 24px; margin-bottom: 24px; border: 1px solid rgba(59,130,246,0.2);">
                <h3 style="color: #60a5fa; margin: 0 0 16px 0; font-size: 18px; font-weight: 700; display: flex; align-items: center; gap: 12px;">
                    <div style="width: 28px; height: 28px; background: linear-gradient(135deg, #3b82f6 0%, #2563eb 100%); border-radius: 8px; display: flex; align-items: center; justify-content: center;">
                        <span style="font-size: 14px;">📋</span>
                    </div>
                    Subject
                </h3>
                <div style="background: rgba(30,41,59,0.6); border-radius: 12px; padding: 18px; border: 1px solid rgba(96,165,250,0.2);">
                    <p style="color: #e2e8f0; margin: 0; font-size: 16px; font-weight: 600; line-height: 1.6;">{{subject}}</p>
                </div>
            </div>

            <!-- Message Section -->
            <div style="background: rgba(16,185,129,0.1); border-radius: 16px; padding: 24px; margin-bottom: 28px; border: 1px solid rgba(16,185,129,0.2);">
                <h3 style="color: #34d399; margin: 0 0 16px 0; font-size: 18px; font-weight: 700; display: flex; align-items: center; gap: 12px;">
                    <div style="width: 28px; height: 28px; background: linear-gradient(135deg, #10b981 0%, #059669 100%); border-radius: 8px; display: flex; align-items: center; justify-content: center;">
                        <span style="font-size: 14px;">💬</span>
                    </div>
                    Message Details
                </h3>
                <div style="background: rgba(30,41,59,0.6); border-radius: 12px; padding: 20px; border: 1px solid rgba(52,211,153,0.2);">
                    <p style="color: #e2e8f0; margin: 0; font-size: 15px; line-height: 1.7; white-space: pre-wrap;">{{message}}</p>
                </div>
            </div>

            <!-- Reply Button -->
            <div style="text-align: center; margin-bottom: 8px;">
                <a href="mailto:{{from_email}}?subject=Re: {{subject}}" style="background: linear-gradient(135deg, #14b8a6 0%, #0d9488 100%); color: white; text-decoration: none; padding: 16px 32px; border-radius: 12px; font-weight: 700; font-size: 16px; display: inline-flex; align-items: center; gap: 10px; box-shadow: 0 8px 25px rgba(20,184,166,0.4); transition: all 0.3s ease; border: 1px solid rgba(255,255,255,0.1);">
                    <span>↩️</span>
                    Reply to {{from_name}}
                </a>
            </div>
        </div>

        <!-- Footer Section -->
        <div style="background: linear-gradient(135deg, #0f172a 0%, #1e293b 100%); padding: 32px 28px; text-align: center; border-top: 1px solid rgba(148,163,184,0.1);">
            <div style="margin-bottom: 24px;">
                <div style="display: inline-flex; align-items: center; gap: 10px; background: rgba(20,184,166,0.1); padding: 10px 20px; border-radius: 25px; margin-bottom: 16px; border: 1px solid rgba(20,184,166,0.2);">
                    <span style="width: 10px; height: 10px; background: #14b8a6; border-radius: 50%; animation: pulse 2s infinite;"></span>
                    <span style="color: #14b8a6; font-size: 13px; font-weight: 700; text-transform: uppercase; letter-spacing: 1px;">Live Monitoring</span>
                </div>
                <p style="color: #94a3b8; margin: 0; font-size: 14px; font-weight: 500;">Real-time insights • AI-powered predictions • Clean air solutions</p>
            </div>
            
            <!-- Links -->
            <div style="display: flex; justify-content: center; gap: 20px; margin-bottom: 24px; flex-wrap: wrap;">
                <a href="https://airaware.in" style="color: #64748b; text-decoration: none; font-size: 14px; font-weight: 600; display: flex; align-items: center; gap: 6px; padding: 6px 12px; border-radius: 8px; background: rgba(100,116,139,0.1); transition: all 0.3s;">🌐 Website</a>
                <a href="tel:+911123456789" style="color: #64748b; text-decoration: none; font-size: 14px; font-weight: 600; display: flex; align-items: center; gap: 6px; padding: 6px 12px; border-radius: 8px; background: rgba(100,116,139,0.1); transition: all 0.3s;">📞 Support</a>
                <a href="mailto:contact@airaware.in" style="color: #64748b; text-decoration: none; font-size: 14px; font-weight: 600; display: flex; align-items: center; gap: 6px; padding: 6px 12px; border-radius: 8px; background: rgba(100,116,139,0.1); transition: all 0.3s;">✉️ Contact</a>
            </div>
            
            <!-- Copyright -->
            <div style="border-top: 1px solid rgba(148,163,184,0.1); padding-top: 20px;">
                <p style="color: #64748b; margin: 0 0 8px 0; font-size: 13px; font-weight: 600;">© 2025 AirAware Delhi-NCR</p>
                <p style="color: #475569; margin: 0; font-size: 12px; display: flex; align-items: center; justify-content: center; gap: 6px;">
                    <span>Building cleaner cities through technology</span>
                    <span style="color: #14b8a6;">🌱</span>
                </p>
            </div>
        </div>
    </div>

    <style>
        @keyframes pulse {
            0%, 100% { opacity: 1; transform: scale(1); }
            50% { opacity: 0.7; transform: scale(1.05); }
        }
        
        @media only screen and (max-width: 640px) {
            .email-container {
                margin: 10px !important;
                border-radius: 16px !important;
            }
            .email-content {
                padding: 24px 20px !important;
            }
            .email-header {
                padding: 32px 20px !important;
            }
        }
    </style>

</body>
</html>
```

4. **Note your TEMPLATE_ID** (e.g., `template_xyz789`)

### Step 4: Get Your Public Key
1. Go to **"Account"** → **"General"**
2. Find your **Public Key** (e.g., `abcdefgh123456789`)

### Step 5: ✅ Configuration Complete!
Your website has been configured with your EmailJS credentials:

```javascript
// Your EmailJS Configuration (Already Set Up)
const EMAILJS_CONFIG = {
    PUBLIC_KEY: 'crHauJ88UDzOS4puy',
    SERVICE_ID: 'service_gmail_001', // Update if different
    TEMPLATE_ID: 'template_sxw9783'
};

// Initialization (Already Done)
emailjs.init(EMAILJS_CONFIG.PUBLIC_KEY);

// Email sending (Already Configured)
emailjs.send(
    EMAILJS_CONFIG.SERVICE_ID,
    EMAILJS_CONFIG.TEMPLATE_ID,
    templateParams
)
```

## 📁 Files Created:
- ✅ `.env` - Environment variables
- ✅ `src/config/emailConfig.js` - Configuration file  
- ✅ Updated `index.html` with your credentials

## ✅ Test Your Setup

1. Save your `index.html` file
2. Open your website
3. Fill out the contact form
4. Submit a test message
5. Check your email inbox

## 🎉 You're Done!

Your contact form will now send real emails to your inbox when users submit the form. You'll receive:

- ✅ **Professional formatted emails** with all form data
- 📧 **User's email** for easy replies
- 🏢 **Organization and user type** for better context
- 💬 **Full message** in a nice format

## 🔧 Troubleshooting

**Form not sending emails?**
- Check browser console for errors
- Verify your SERVICE_ID and TEMPLATE_ID are correct
- Make sure your PUBLIC_KEY is properly set
- Check EmailJS dashboard for delivery status

**Need help?**
- EmailJS Documentation: https://www.emailjs.com/docs/
- Free plan allows 200 emails/month
- Upgrade for more emails and features

---

**🌍 Happy air quality monitoring with AirAware!**