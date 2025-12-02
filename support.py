import streamlit as st
from datetime import datetime
from db import init_collections

def handle_support_request():
    st.header("🆘 Create Support Ticket")
    
    with st.form("support_form"):
        name = st.text_input("Name")
        email = st.text_input("Email")
        issue = st.text_area("Describe your issue")
        priority = st.selectbox("Priority", ["normal", "high", "urgent"])
        
        submitted = st.form_submit_button("Submit Ticket")
        
        if submitted and name and email and issue:
            collections = init_collections()
            ticket = {
                "ticket_number": f"TKT-{int(datetime.now().timestamp())}",
                "customer_name": name,
                "customer_email": email,
                "issue": issue,
                "priority": priority,
                "status": "open",
                "created_at": datetime.now()
            }
            
            collections['support_tickets'].insert_one(ticket)
            st.success(f"✅ Ticket #{ticket['ticket_number']} created!")
            st.balloons()
            return f"Ticket created: {ticket['ticket_number']}"
    
    return "Fill out the form to create a ticket"
