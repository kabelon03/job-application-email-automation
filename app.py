import streamlit as st
from database import create_database, add_application, get_applications_to_followup, mark_as_followed_up
from email_sender import send_followup_email
import sqlite3

# Initialize database
create_database()

st.title("📧 Job Application Email Automation")
st.markdown("Track your job applications and send automatic follow-up emails.")

# Sidebar settings
st.sidebar.header("⚙️ Settings")
sender_email = st.sidebar.text_input("Your Gmail Address")
sender_password = st.sidebar.text_input("Your App Password", type="password")

# Sidebar menu
menu = st.sidebar.selectbox("Menu", ["Add Application", "View Applications", "Run Follow-Up Checker"])

if menu == "Add Application":
    st.header("Add New Job Application")
    
    company_name = st.text_input("Company Name")
    contact_email = st.text_input("Contact Email")
    position = st.text_input("Position Applied For")
    
    if st.button("Add Application"):
        if company_name and contact_email and position:
            add_application(company_name, contact_email, position)
            st.success(f"Application for {position} at {company_name} added!")
        else:
            st.error("Please fill in all fields.")

elif menu == "View Applications":
    st.header("All Job Applications")
    
    conn = sqlite3.connect('job_applications.db')
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM applications')
    applications = cursor.fetchall()
    conn.close()
    
    if not applications:
        st.info("No applications yet. Add one from the menu!")
    else:
        for app in applications:
            st.write(f"**{app[3]}** at **{app[1]}**")
            st.write(f"Email: {app[2]} | Applied: {app[4]} | Status: {app[5]} | Followed Up: {'Yes' if app[6] else 'No'}")
            st.divider()

elif menu == "Run Follow-Up Checker":
    st.header("Follow-Up Checker")
    
    if st.button("Check & Send Follow-Ups"):
        if not sender_email or not sender_password:
            st.error("Please enter your Gmail and App Password in the Settings panel on the left.")
        else:
            applications = get_applications_to_followup()
            
            if not applications:
                st.info("No applications need a follow-up today.")
            else:
                for app in applications:
                    app_id, company_name, contact_email, position = app
                    success = send_followup_email(sender_email, contact_email, company_name, position)
                    if success:
                        mark_as_followed_up(app_id)
                        st.success(f"Follow-up sent to {company_name}!")
                    else:
                        st.error(f"Failed to send to {company_name}.")