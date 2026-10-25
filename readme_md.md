# Legal Triage - Tenant Tool

An easy-to-use web tool that helps everyday tenants check rental agreements, protect their security deposits, and evaluate housing societies before moving in.

---

## 🎯 What Problem Did We Solve?

Renting a home in large cities comes with several hidden challenges:
1. **Risky Rental Contracts:** Most standard lease agreements contain one-sided, unfair clauses (like unlimited tenant liability or unfair termination rules) that ordinary tenants miss.
2. **Unfair Deposit Deductions:** When moving out, landlords often cut large amounts from the security deposit for routine painting or minor wear and tear, and going to court is too expensive.
3. **Lack of Building Insights:** Property listing websites show photos, but they do not provide reliable information regarding water supply, gate security, maintenance, or whether a society is friendly for bachelors.

---

## ✨ Key Features

* **Contract Scanner:** Upload a PDF, DOCX, or TXT lease agreement. The app runs 15 legal rules instantly to check for hidden risks, gives a 0–100 risk score, and generates fair replacement clauses along with a WhatsApp message draft.
* **Deposit Shield:** Calculates how much money a landlord can legally deduct based on a 24-month wear-and-tear rule and statutory interest, and prepares a formal legal demand notice.
* **Society Trust Index (DTI):** Rates residential societies out of 100 based on water, security, maintenance, and bachelor-friendliness scores, complete with a photo gallery.
* **Direct-Owner Marketplace:** Lets property owners list homes directly with zero brokerage fees, complete with verification checks and roommate matching tools.

---

## 🛠️ Technology Stack

* **Language:** Python 3.11
* **Interface:** Streamlit
* **Database:** SQLite 3 (stores user scans, listings, and reviews securely)
* **Libraries:** `pypdf`, `pdfplumber`, `python-docx`, `Pandas`, `Matplotlib`
* **Deployment:** Docker container support

---

## 📂 Project Structure

```text
.
├── app.py                 # Main application entry point and navigation setup
├── Dockerfile             # Container setup configuration
├── core/                  # Core logic and helper routines
│   ├── db.py              # Database setup and connection helpers
│   ├── extractor.py       # Document text extraction pipeline
│   ├── rulebook.py        # Legal rule check engine
│   ├── nav.py             # Page routing setup
│   └── premium_theme.py   # Interface styling code
├── views/                 # Application feature pages
│   ├── dashboard.py       # Overview dashboard page
│   ├── scan.py            # Contract scanning page
│   ├── tenant_workspace.py# Deposit recovery calculator and evidence vault
│   ├── society_reviews.py # Society trust rating page
│   ├── property_guide.py  # Direct owner property listings page
│   ├── roommates.py       # Roommate finder and covenant tool
│   └── about_pitch.py     # Business overview page
└── data/                  # Local folder for SQLite storage and uploaded files
```

---

## 🚀 Future Thoughts & Improvements

* **Multi-Language Support:** Expanding contract checks to support regional languages like Hindi, Gujarati, and Marathi.
* **Broader City Rules:** Extending legal rulebooks to cover more major cities and states across India.
* **Mobile App & Bot:** Building a lightweight mobile application or WhatsApp assistant for faster on-the-go checks.
* **Licensed Partner Integrations:** Collaborating with legal experts and digital escrow services to allow direct legal filings and secure deposit management.

---

## 💻 Getting Started

### 1. Clone the Repository
```bash
git clone https://github.com/username/legal-triage-tenant-tool.git
cd legal-triage-tenant-tool
```

### 2. Install Dependencies
```bash
pip install streamlit pypdf pdfplumber python-docx Pillow pandas matplotlib lxml
```

### 3. Run the Application
```bash
streamlit run app.py
```
Open your web browser and navigate to `http://localhost:8501`.

---

## 🐳 Running with Docker

```bash
# Build the image
docker build -t legal-triage-tool .

# Start the container
docker run -p 8501:8501 legal-triage-tool
```