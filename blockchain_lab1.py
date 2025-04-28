import streamlit as st
import time
import json
import hashlib

# Event ticket sales ledger
event_ticket_sales_ledger = []

# Function to calculate hash
def calculate_hash(block):
    # Convert the dictionary to a JSON string before encoding
    encoded_block = json.dumps(block, sort_keys=True).encode()
    return hashlib.sha256(encoded_block).hexdigest()

# Function to add a ticket sale to the blockchain
def add_ticket_sale(event_name, ticket_id, buyer_id, seller_id, price):
    if not event_ticket_sales_ledger:
        previous_hash = "0"  # Genesis block
    else:
        previous_hash = calculate_hash(event_ticket_sales_ledger[-1])

    block = {
        'previous_hash': previous_hash,
        'timestamp': time.time(),
        'data': {
            'event_name': event_name,
            'ticket_id': ticket_id,
            'buyer_id': buyer_id,
            'seller_id': seller_id,
            'price': price
        }
    }
    block['hash'] = calculate_hash(block)
    event_ticket_sales_ledger.append(block)

# Streamlit UI
st.title("Event Ticket Sales Blockchain")
st.write("This is a simple implementation of a blockchain for event ticket sales.")

# Display the ledger
st.subheader("Event Ticket Sales Ledger")
if event_ticket_sales_ledger:
    for idx, block in enumerate(event_ticket_sales_ledger):
        st.write(f"**Block {idx + 1}:**")
        st.write(f"- **Event Name:** {block['data']['event_name']}")
        st.write(f"- **Ticket ID:** {block['data']['ticket_id']}")
        st.write(f"- **Buyer ID:** {block['data']['buyer_id']}")
        st.write(f"- **Seller ID:** {block['data']['seller_id']}")
        st.write(f"- **Price:** ${block['data']['price']}")
        st.write(f"- **Timestamp:** {time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(block['timestamp']))}")
        st.write(f"- **Previous Hash:** {block['previous_hash']}")
        st.write(f"- **Hash:** {block['hash']}")
        st.write("---")
else:
    st.write("No ticket sales yet.")

# Input fields for adding new ticket sale
st.subheader("Add a New Ticket Sale")
event_name = st.text_input("Event Name")
ticket_id = st.text_input("Ticket ID")
buyer_id = st.text_input("Buyer ID")
seller_id = st.text_input("Seller ID")
price = st.number_input("Price ($)", min_value=0)

# Add ticket sale when button is clicked
if st.button("Add Ticket Sale"):
    if event_name and ticket_id and buyer_id and seller_id and price > 0:
        add_ticket_sale(event_name, ticket_id, buyer_id, seller_id, price)
        st.success("Ticket sale added successfully!")
    else:
        st.error("Please fill all fields correctly.")

# Add some default ticket sales for testing
if st.button("Add Default Ticket Sales"):
    add_ticket_sale("Concert A", "T123", "Buyer1", "Seller1", 50)
    add_ticket_sale("Concert B", "T456", "Buyer2", "Seller2", 75)
    add_ticket_sale("Concert A", "T789", "Buyer3", "Seller1", 60)
    st.success("Default ticket sales added!")

