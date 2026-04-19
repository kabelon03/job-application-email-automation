# Job Application Email Automation

A Python automation tool that tracks job applications and automatically sends follow-up emails after 7 days.

## Features
- Track job applications in a local database
- Automatically send personalized follow-up emails after 7 days
- Simple CLI menu to manage applications
- Daily scheduler that runs automatically at 9am

## Project Structure
email_automation/
    database.py       # Database setup and queries
    email_sender.py   # Email sending logic
    main.py           # CLI menu and scheduler
    README.md         # Project documentation

## Setup
1. Clone the repository
2. Install dependencies: pip install schedule
3. Set up Gmail App Password and add it as an environment variable:
   - Variable name: EMAIL_PASSWORD
   - Variable value: your 16 character app password
4. Update SENDER_EMAIL in main.py with your Gmail address
5. Run: python main.py

## Usage
- Option 1: Add a new job application
- Option 2: Run follow-up checker manually
- Option 3: Start automatic daily scheduler
- Option 4: Exit