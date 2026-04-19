import sqlite3
from datetime import datetime, timedelta

def create_database():
    conn = sqlite3.connect('job_applications.db')
    cursor = conn.cursor()
    
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS applications (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            company_name TEXT NOT NULL,
            contact_email TEXT NOT NULL,
            position TEXT NOT NULL,
            date_applied TEXT NOT NULL,
            status TEXT DEFAULT 'pending',
            followed_up INTEGER DEFAULT 0
        )
    ''')
    
    conn.commit()
    conn.close()
    print("Database created successfully!")

def add_application(company_name, contact_email, position):
    conn = sqlite3.connect('job_applications.db')
    cursor = conn.cursor()
    
    cursor.execute('''
        INSERT INTO applications (company_name, contact_email, position, date_applied)
        VALUES (?, ?, ?, ?)
    ''', (company_name, contact_email, position, datetime.now().strftime('%Y-%m-%d')))
    
    conn.commit()
    conn.close()
    print(f"Application for {position} at {company_name} added!")

def get_applications_to_followup():
    conn = sqlite3.connect('job_applications.db')
    cursor = conn.cursor()
    
    seven_days_ago = (datetime.now() - timedelta(days=7)).strftime('%Y-%m-%d')
    
    cursor.execute('''
        SELECT id, company_name, contact_email, position
        FROM applications
        WHERE date_applied <= ?
        AND followed_up = 0
        AND status = 'pending'
    ''', (seven_days_ago,))
    
    applications = cursor.fetchall()
    conn.close()
    return applications

def mark_as_followed_up(application_id):
    conn = sqlite3.connect('job_applications.db')
    cursor = conn.cursor()
    
    cursor.execute('''
        UPDATE applications
        SET followed_up = 1
        WHERE id = ?
    ''', (application_id,))
    
    conn.commit()
    conn.close()

def add_test_application():
    conn = sqlite3.connect('job_applications.db')
    cursor = conn.cursor()
    
    cursor.execute('''
        INSERT INTO applications (company_name, contact_email, position, date_applied)
        VALUES (?, ?, ?, ?)
    ''', ("Test Company", "kabelon03@gmail.com", "Software Engineer", "2026-04-01"))
    
    conn.commit()
    conn.close()
    print("Test application added!")

if __name__ == '__main__':
    create_database()
    add_application("Google", "recruiter@google.com", "Software Engineer")
    add_test_application()