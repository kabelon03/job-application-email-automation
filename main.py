import schedule
import time
import sys
from database import get_applications_to_followup, mark_as_followed_up, add_application, create_database
from email_sender import send_followup_email

SENDER_EMAIL = 'kabelon03@gmail.com'

def run_followup_checker():
    print("Checking for applications to follow up on...")
    
    applications = get_applications_to_followup()
    
    if not applications:
        print("No applications need a follow-up today.")
        return
    
    print(f"Found {len(applications)} application(s) to follow up on.")
    
    for app in applications:
        app_id, company_name, contact_email, position = app
        
        print(f"Sending follow-up to {company_name}...")
        
        success = send_followup_email(
            sender_email=SENDER_EMAIL,
            recipient_email=contact_email,
            company_name=company_name,
            position=position
        )
        
        if success:
            mark_as_followed_up(app_id)
            print(f"Marked {company_name} as followed up.")

def add_new_application():
    print("\n--- Add New Job Application ---")
    company_name = input("Company name: ")
    contact_email = input("Contact email: ")
    position = input("Position applied for: ")
    add_application(company_name, contact_email, position)

def show_menu():
    print("\n--- Job Application Email Automation ---")
    print("1. Add new job application")
    print("2. Run follow-up checker now")
    print("3. Start automatic scheduler")
    print("4. Exit")
    return input("Choose an option: ")

def start_scheduler():
    print("Scheduler started - running every day at 9am. Press Ctrl+C to stop.")
    run_followup_checker()
    schedule.every().day.at("09:00").do(run_followup_checker)
    while True:
        schedule.run_pending()
        time.sleep(60)

if __name__ == '__main__':
    create_database()
    while True:
        choice = show_menu()
        if choice == '1':
            add_new_application()
        elif choice == '2':
            run_followup_checker()
        elif choice == '3':
            start_scheduler()
        elif choice == '4':
            print("Goodbye!")
            sys.exit()
        else:
            print("Invalid option, try again.")