import smtplib
from email.message import EmailMessage
import ssl
import re

# Replace with your details
sender_email = "avivjoji@gmail.com"
receiver_email = "aj7305@srmist.edu.in"  # Chemist's email
app_password = "dcfoenealtutzilq"
subject = "Automated Prescription Analysis"

def preprocess_text(text):
    """
    Cleans and standardizes the prescription text.
    """
    text = text.lower()
    text = re.sub(r'[^a-zA-Z0-9\s]', '', text)  # Remove punctuation
    text = re.sub(r'\s+', ' ', text).strip()  # Remove extra spaces
    return text

def extract_medication_info(text):
    """
    Extracts medication names, dosages, and quantities using regular expressions.
    """
    medications = []
    # Regex to find medication names (improved to handle more cases)
    med_name_pattern = r'([a-zA-Z]+(?: [a-zA-Z]+)?)' # Captures multi-word names
    dosage_pattern = r'(\d+)(?:mg|ml|g)'  # Captures dosage
    quantity_pattern = r'(\d+) (?:tablet|capsule|pill|vial|dose|application|unit)s?' # Captures quantity

    # Find all medication names
    med_names = re.findall(med_name_pattern, text)
    dosages = re.findall(dosage_pattern, text)
    quantities = re.findall(quantity_pattern, text)

    # Combine extracted info (basic - could be improved with better logic)
    for i, med_name in enumerate(med_names):
        med_name = clean_medication_name(med_name) # Clean the name
        if med_name: # Only add if cleaned name is not empty
            medications.append({
                'name': med_name,
                'dosage': dosages[i] if i < len(dosages) else None,
                'quantity': quantities[i] if i < len(quantities) else None
            })
    return medications

def clean_medication_name(med_name):
    """
    Cleans and standardizes medication names.
    """
    med_name = med_name.strip()
    # Remove common words that are not part of the medication name
    stop_words = ["take", "use", "apply", "administer","orally","orally,", "injection"]
    words = med_name.split()
    cleaned_words = [word for word in words if word.lower() not in stop_words]
    return " ".join(cleaned_words)
def send_prescription_via_email_automated(prescription_text):
    """
    Analyzes the prescription and sends an email.
    """
    preprocessed_text = preprocess_text(prescription_text)
    medication_info = extract_medication_info(preprocessed_text)

    body = f"""
Hi Chemist,

The following medications were identified from the prescription:
{medication_info}

Please find the original prescription text below:
---
{prescription_text}
---

Kindly prepare the order and deliver to the user.

Name: [User's Name - Needs to be obtained]
Address: [User's Address - Needs to be obtained]
Phone: [User's Contact - Needs to be obtained]

Thank you!
"""

    msg = EmailMessage()
    msg.set_content(body)
    msg["From"] = sender_email
    msg["To"] = receiver_email
    msg["Subject"] = subject

    context = ssl.create_default_context()
    try:
        with smtplib.SMTP_SSL("smtp.gmail.com", 465, context=context) as server:
            server.login(sender_email, app_password)
            server.send_message(msg)
        print("📧 Automated prescription analysis and email sent! (No spaCy)")
    except Exception as e:
        print(f"Error sending email: {e}")

# Example usage:
prescription = "Take 2 Paracetamol 500mg tablets three times a day after meals.  Apply  Betamethasone cream."
send_prescription_via_email_automated(prescription)