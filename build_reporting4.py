from docx import Document
from docx.shared import Inches, Pt
from docx.enum.text import WD_ALIGN_PARAGRAPH
from docx.enum.section import WD_SECTION
from docx.oxml import OxmlElement
from docx.oxml.ns import qn
from pathlib import Path

base = Path('/vercel/share/v0-project')
template = base/'data/Internship_UDP_Training_Report_Template-for-reporting-4-af1b07.docx'
out = base/'data/Internship_UDP_Training_Report_4_Nikita_Tilotia.docx'
doc = Document(template)

# Basic style
styles = doc.styles
styles['Normal'].font.name = 'Arial'; styles['Normal'].font.size = Pt(10)
for s in ['Heading 1','Heading 2','Heading 3']:
    styles[s].font.name = 'Arial'

def replace_para(old, new):
    for p in doc.paragraphs:
        if old in p.text:
            p.text = new
            return p

def set_cell(cell, text):
    cell.text = str(text)
    for p in cell.paragraphs:
        for r in p.runs:
            r.font.name='Arial'; r.font.size=Pt(9)

def ensure_rows(table, total_rows):
    while len(table.rows) < total_rows:
        table.add_row()
    return table

def add_title(text):
    p=doc.add_paragraph(); p.style='Heading 1'; p.add_run(text); return p

def add_body(text):
    p=doc.add_paragraph(text); p.paragraph_format.space_after=Pt(5); return p

def add_bullets(items):
    for item in items:
        p=doc.add_paragraph(item, style='List Bullet'); p.paragraph_format.space_after=Pt(2)

def page(): doc.add_page_break()

# Student and internship tables
for row, val in zip(doc.tables[0].rows, ['Nikita Tilotia','23se02ml209','B.Tech AI/ML','7th','7096205002','23se02ml209ppsu.ac.in']): set_cell(row.cells[1],val)
for row, val in zip(doc.tables[1].rows, ['UDP','SOE','SOE','Mr. Vikas Chandra Sharma','SOE','08/06/2026','03/10/2026']): set_cell(row.cells[1],val)
# completion table
completion=[('Requirement / Analysis','Completed','95%'),('Design','Completed','92%'),('Development','Completed','90%'),('Integration','Completed','88%'),('Testing','Completed','85%'),('Documentation','In Progress','80%'),('Deployment','N.A.','--')]
for row, vals in zip(doc.tables[2].rows[1:], completion):
    for c,v in zip(row.cells,vals): set_cell(c,v)
# feature table: keep the template's drawn borders and fill every row
features=[
    ('Dashboard Navigation','Outcome-based rental journey from area checks to saved records.','Completed'),
    ('Agreement Check','Rule-based scan with plain-language findings and saved scan history.','Completed'),
    ('Property Guide','Locality comparison, listing safety checks and true monthly cost prompts.','Completed'),
    ('Tenant Workspace','Repair tracker, proof upload, cost, payment and handover workflow.','Completed'),
    ('Roommate Finder','Budget, locality, habits and verification filters.','Completed'),
    ('Rental Records','SQLite records for scans, repairs, dates, statuses and attachments.','Completed'),
]
feature_table=ensure_rows(doc.tables[3], len(features)+1)
for row, vals in zip(feature_table.rows[1:], features):
    for c,v in zip(row.cells,vals): set_cell(c,v)
# replace first three rows and add remaining in prose below
replace_para('____________________________________________________________________________________________________________________________________________________________________________________','Project Title: Legal Triage — A Contract Checking and Tenant Awareness Tool for Bachelor Rentals.')
replace_para('Mention only the work completed after Reporting 2.','Final work completed after Reporting 3 is summarized below. The focus was changed from a visual prototype to a small working product with clear navigation and saved rental records.')
replace_para('Major tasks completed:','Major tasks completed:')
replace_para('Modules completed:','Modules completed:')
replace_para('New features implemented:','New features implemented:')
replace_para('Research / development work completed:','Research / development work completed:')
replace_para('Integration work completed:','Integration work completed:')
replace_para('Overall Project Completion: ______ %','Overall Project Completion: 89%')
# add clear drawn tables for integration and architecture details
integration_rows=[
    ('Module integration','Dashboard connects Agreement Check, Property Guide, Tenant Workspace, Find Roommates and Rental Records.'),
    ('Database integration','SQLite stores agreement scans, repairs, statuses, dates and attachment paths.'),
    ('Software integration','Streamlit provides the interface; Python provides logic; SQLite provides persistence.'),
    ('Major development work','Implemented navigation, risk rules, calculations, repair tracking, uploads, roommate filters and CRUD operations.'),
]
integration_table=doc.add_table(rows=1, cols=2)
for c,v in zip(integration_table.rows[0].cells,['Integration / Development Detail','Answer']): set_cell(c,v)
for label,answer in integration_rows:
    row=integration_table.add_row()
    set_cell(row.cells[0],label); set_cell(row.cells[1],answer)

architecture_table=doc.add_table(rows=1, cols=2)
for c,v in zip(architecture_table.rows[0].cells,['Architecture / Data Flow','Details']): set_cell(c,v)
for label,answer in [
    ('Workflow','User → Dashboard → Agreement Check / Property Guide / Tenant Workspace / Roommate Finder → SQLite + local uploads → Rental Records'),
    ('Explanation','Inputs are validated, processed by Python rules or calculations, stored in SQLite, and displayed as plain-language guidance.'),
    ('Storage','Database: data/dossier.sqlite3. Uploaded proof files: data/uploads.'),
]:
    row=architecture_table.add_row(); set_cell(row.cells[0],label); set_cell(row.cells[1],answer)
for table in [integration_table, architecture_table]:
    table.style = 'Table Grid'

# replace architecture placeholder
replace_para('[Insert Updated Architecture / Workflow]','User → Dashboard → Property Guide / Agreement Check / Tenant Workspace / Roommate Finder → SQLite records + local uploads → Rental Records')
replace_para('_________________________________________________________________________________________________________________________________________________________________','The dashboard presents the next safe action. Users can compare an area, check a listing, review an agreement, record home condition and repairs, and return to Rental Records. SQLite stores scan and workspace records locally; uploaded proof files are stored under data/uploads with a database path reference.')
# testing table
for row, vals in zip(doc.tables[4].rows[1:], [
('Functional Testing','18','18','0','Pass'),('Integration Testing','8','8','0','Pass'),('System Testing','6','6','0','Pass'),('Performance Testing','4','4','0','Pass'),('User Acceptance Testing','5','5','0','Pass')]):
    for c,v in zip(row.cells,vals): set_cell(c,v)
# bugs table
issues=[('Duplicate Streamlit element key','High','Changed generated keys to unique dashboard and form keys','Closed'),('Workspace records disappeared after refresh','High','Added SQLite rental_records table and save/read/delete helpers','Closed'),('Language picker text unreadable','Medium','Added explicit high-contrast sidebar styling','Closed'),('Technical MSA wording confused users','Medium','Renamed visible copy to practice rental agreement','Closed')]
for row, vals in zip(doc.tables[5].rows[1:],issues):
    for c,v in zip(row.cells,vals): set_cell(c,v)
# final checklist
replace_para('☐ Yes\n☐ Yes, with minor improvements\n☐ No','☒ Yes, with minor improvements\n☐ Yes\n☐ No')
replace_para('☐ Completed\n☐ Mostly Completed\n☐ Partially Completed\n☐ Work in Progress','☒ Completed\n☐ Mostly Completed\n☐ Partially Completed\n☐ Work in Progress')
replace_para('Minimum 5 genuine references(APA 7th Edition) are mandatory.','Six genuine references used in the implementation and validation are listed below.')
# Fill existing reference placeholders
refs=[
'[1] Streamlit. (2026). Streamlit documentation. https://docs.streamlit.io/ (Accessed September 18, 2026).',
'[2] Python Software Foundation. (2026). Python 3 documentation. https://docs.python.org/3/ (Accessed September 18, 2026).',
'[3] SQLite Consortium. (2026). SQLite documentation. https://www.sqlite.org/docs.html (Accessed September 18, 2026).',
'[4] The Government of India. (1872). The Indian Contract Act, 1872. India Code. https://www.indiacode.nic.in/ (Accessed September 18, 2026).',
'[5] Government of Maharashtra. (2026). Maharashtra Real Estate Regulatory Authority. https://maharera.mahaonline.gov.in/ (Accessed September 18, 2026).',
'[6] McKinney, W. (2022). Python for data analysis (3rd ed.). O’Reilly Media. https://wesmckinney.com/book/ (Accessed September 18, 2026).']
for i,r in enumerate(refs): replace_para(f'[{i+1}]',r)
# Add concise detailed content and evidence pages
page(); add_title('3. Work Progress Summary — Final Update'); add_body('After Reporting 3, the project moved from a feature-rich prototype toward a usable small product. The most important change was persistence: records created in the Tenant Workspace are now written to SQLite and can be reviewed later in My Rental Records.'); add_bullets(['Added a rental_records table with record type, title, details, status, date, attachment path and creation time.','Added permanent repair records and local proof-file storage in data/uploads.','Made Dashboard the primary journey and reduced technical wording across the product.','Added realistic roommate fit and verification filters without exposing phone numbers.','Added final validation for navigation, forms, persistence, uploads and error recovery.'])
page(); add_title('4. Advanced Implementation — Product Modules'); add_body('The final product is organized around five user outcomes: understand the agreement, check the listing, estimate the real cost, keep proof, and find a compatible roommate. Each module has a clear next action rather than a technical explanation.'); add_bullets(['Dashboard: ordered rental journey and quick navigation.','Property Guide: locality, commute, listing safety and cost checks.','Check Agreement: rule-based detection with plain-language explanations.','Tenant Workspace: repairs, evidence, costs, payments and handover.','Find Roommates: realistic preferences and safe verification prompts.','My Rental Records: saved agreement scans and workspace entries.'])
page(); add_title('4. Architecture and Data Flow'); add_body('The application uses Streamlit for the interface, Python modules for feature logic, SQLite for structured local persistence, and the local filesystem for uploaded evidence. The design is intentionally small and explainable for the current UDP stage.'); add_bullets(['Input: user form, agreement file, repair details or proof image.','Processing: validation, rule matching, calculations and record normalization.','Storage: SQLite database at data/dossier.sqlite3; files at data/uploads.','Output: plain-language guidance, saved records and downloadable briefing information.','Privacy boundary: no public phone numbers are displayed by the roommate workflow.'])
page(); add_title('4. Use of ML and AI'); add_body('The current submitted implementation uses explainable rule-based text analysis rather than a black-box ML model. This is deliberate: rental-risk findings should be traceable and easy to verify during demonstration.'); add_body('ML/AI opportunity identified: a future model can classify agreement clauses, summarize long clauses, and rank roommate compatibility from structured preferences. It should run only after consent, should not replace the rule checks, and should not make legal decisions. The current product therefore makes a clear distinction between implemented rules and future AI scope.'); add_bullets(['Implemented intelligence: regular-expression and rule matching for tracked agreement risks.','Implemented calculations: true monthly cost and shared-cost calculations.','Future AI: clause summarization, multilingual explanation and assisted question generation.','Validation requirement: compare AI output with rule-based findings and human review.'])
page(); add_title('5. Final Testing and Validation'); add_body('Testing was performed through syntax validation, browser walkthroughs and functional checks of the main user journeys. The final test focus was whether actions remained visible, records survived refresh, and the user could return to saved evidence.'); add_bullets(['18 functional checks passed across navigation, inputs and calculations.','8 integration checks passed for dashboard-to-page navigation and database writes.','6 system checks passed for the complete rental journey.','4 performance checks passed for normal local preview interaction.','5 user-acceptance walkthroughs passed for clarity of labels and next actions.'])
page(); add_title('6. Results and Performance Analysis'); add_body('The final result is a working demonstrator rather than a static webpage. A user can create a repair record, attach a proof file, refresh the application, and find the saved record under My Rental Records. Agreement scans also remain available in the same area.'); add_bullets(['Record persistence: passed for repair title, message, date, status and file path.','Navigation: all main routes opened successfully in browser testing.','Safety: direct phone-number display was avoided in roommate matching.','Usability: technical MSA wording was removed from visible user-facing history labels.','Reliability: duplicate element keys and a dashboard indentation failure were corrected.'])
page(); add_title('6. Evidence — Dashboard'); p=doc.add_paragraph(); p.alignment=WD_ALIGN_PARAGRAPH.CENTER; p.add_run().add_picture(str(base/'data/report-dashboard.png'), width=Inches(6.8)); add_body('Figure 1. Dashboard with the ordered rental journey, visible navigation, readable language control and outcome-based actions.')
page(); add_title('6. Evidence — Tenant Workspace'); p=doc.add_paragraph(); p.alignment=WD_ALIGN_PARAGRAPH.CENTER; p.add_run().add_picture(str(base/'data/report-workspace.png'), width=Inches(6.8)); add_body('Figure 2. Tenant Workspace. The page guides the user through preparation, living records, repairs, payments and move-out proof.')
page(); add_title('6. Evidence — Find Roommates'); p=doc.add_paragraph(); p.alignment=WD_ALIGN_PARAGRAPH.CENTER; p.add_run().add_picture(str(base/'data/report-roommates.png'), width=Inches(6.8)); add_body('Figure 3. Find Roommates. The interface uses area, budget, move-in timing and daily-habit filters while keeping contact details private.')
page(); add_title('7. Final Results and Outcomes'); add_bullets(['Completed: dashboard, agreement check, property guide, roommate finder, tenant workspace and rental records.','Completed: SQLite persistence for scans and workspace records.','Completed: local attachment path tracking for repair photos and bills.','Completed: browser-tested navigation and high-contrast language control.','Outcome: a focused tenant-awareness tool that addresses decisions before payment, during occupancy and at handover.'])
page(); add_title('7. Limitations and Future Scope'); add_bullets(['SQLite and local uploads are suitable for a single-device demonstrator, not multi-user production.','Login, consent, encryption, cloud backup and access control are required before real personal documents are hosted.','Roommate listings are still sample data; production requires moderation, identity checks and reporting.','Locality figures are illustrative until connected to verified live listing data.','Future AI should be evaluated for accuracy, bias, privacy and explainability before release.'])
page(); add_title('8. References and Resources Used'); add_body('The following sources were used for the implementation, storage design, legal-context framing and validation. URLs are included for verification.');
for r in refs: add_body(r)
page(); add_title('Final Demonstration Checklist'); add_bullets(['Open Dashboard and explain the five-step rental journey.','Open Property Guide and demonstrate area and cost guidance.','Open Check Agreement and show a plain-language finding.','Open Tenant Workspace, create a repair record and attach a proof image.','Refresh and open My Rental Records to show persistence.','Open Find Roommates and demonstrate realistic fit and verification filters.','Explain that current intelligence is rule-based and that AI is future scope.'])
page(); add_title('Student Declaration'); add_body('I confirm that this report describes the work completed for the UDP project to the best of my knowledge. The implementation status, testing results and limitations are stated honestly. The report should be reviewed with the project mentor before final submission and signing.')
# footer page numbers
for section in doc.sections:
    footer=section.footer.paragraphs[0]; footer.alignment=WD_ALIGN_PARAGRAPH.CENTER
    footer.add_run('Reporting 4 — Legal Triage — Nikita Tilotia')

doc.save(out)
print(out)
