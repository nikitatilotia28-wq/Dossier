# Dossier
A lightweight, explainable Python web application built with Streamlit and SQLite for automated rental agreement auditing, security deposit recovery calculations, and building trust scoring.

# Legal Triage/ Dossier - Tenant Tool

An easy-to-use web tool that helps everyday tenants check rental agreements, protect their security deposits, and evaluate housing societies before moving in.

---

## 📌 Problem Solved

Renting a home in large cities comes with several hidden challenges:
1. **Risky Rental Contracts:** Most standard lease agreements contain one-sided, unfair clauses (like unlimited tenant liability or unfair termination rules) that ordinary tenants miss.
2. **Unfair Deposit Deductions:** When moving out, landlords often cut large amounts from the security deposit for routine painting or minor wear and tear, and going to court is too expensive.
3. **Lack of Building Insights:** Property listing websites show photos, but they do not provide reliable information regarding water supply, gate security, maintenance, or whether a society is friendly for bachelors.

---

##  Key Features

* 📄 **Contract Scanner:** Upload a PDF, DOCX, or TXT lease agreement. The app runs 15 legal rules instantly to check for hidden risks, gives a 0–100 risk score, and generates fair replacement clauses along with a WhatsApp message draft.
* 🛡️ **Deposit Shield:** Calculates how much money a landlord can legally deduct based on a 24-month wear-and-tear rule and statutory interest, and prepares a formal legal demand notice.
* 🏢 **Society Trust Index (DTI):** Rates residential societies out of 100 based on water, security, maintenance, and bachelor-friendliness scores, complete with a photo gallery.
* 🏡 **Direct-Owner Marketplace:** Lets property owners list homes directly with zero brokerage fees, complete with verification checks and roommate matching tools.

---

## 🛠️ Technology Stack

* **Language:** Python 3.11
* **Interface:** Streamlit
* **Database:** SQLite 3 (stores user scans, listings, and reviews securely)
* **Libraries:** `pypdf`, `pdfplumber`, `python-docx`, `pandas`, `matplotlib`, `Pillow`
* **Deployment:** Docker container support

---

## 📂 Project Structure

text
├── app.py                 # Main entry point and page routing
├── Dockerfile             # Container setup
├── core/                  # Core logic and database tools
│   ├── db.py              # SQLite database functions
│   ├── extractor.py       # File reader for PDF, DOCX, and TXT
│   ├── rulebook.py        # 15 legal regex rules engine
│   ├── nav.py             # Page navigation setup
│   └── premium_theme.py   # UI styling and CSS
├── views/                 # Application pages
│   ├── dashboard.py       # Main metrics and dashboard
│   ├── scan.py            # Contract audit page
│   ├── tenant_workspace.py# Deposit recovery calculator
│   ├── society_reviews.py # Building ratings and reviews
│   ├── property_guide.py  # Direct owner property listings
│   ├── roommates.py       # Roommate finder and covenant
│   └── about_pitch.py     # Analytics and scenario simulator
└── data/                  # Local storage folder for database and files


Getting Started
1. Clone the Repository
Bash
git clone https://github.com/username/legal-triage-tenant-tool.git
cd legal-triage-tenant-tool
2. Install Dependencies
Bash
pip install streamlit pypdf pdfplumber python-docx Pillow pandas matplotlib lxml
3. Run the Application
Bash
streamlit run app.py
