from docx import Document
from docx.shared import Inches, Pt, RGBColor
from docx.enum.text import WD_ALIGN_PARAGRAPH
from docx.enum.table import WD_TABLE_ALIGNMENT
from docx.oxml import OxmlElement
from docx.oxml.ns import qn
from pathlib import Path

out='data/The_Dossier_Reporting_3.docx'
d=Document()
sec=d.sections[0]; sec.top_margin=Inches(.65); sec.bottom_margin=Inches(.65); sec.left_margin=Inches(.7); sec.right_margin=Inches(.7)
for s in d.styles:
    if s.name=='Normal': s.font.name='Arial'; s.font.size=Pt(9)
for name,size in [('Title',20),('Heading 1',14),('Heading 2',11)]:
    s=d.styles[name]; s.font.name='Arial'; s.font.size=Pt(size); s.font.bold=True; s.font.color.rgb=RGBColor(31,55,91)
def p(text='',bold=False):
    x=d.add_paragraph(); r=x.add_run(text); r.bold=bold; return x
def h(text,l=1): d.add_heading(text,l)
def bullets(items):
    for x in items: d.add_paragraph(x,style='List Bullet')
def shade(cell,fill='1F375B'):
    shd=OxmlElement('w:shd'); shd.set(qn('w:fill'),fill); cell._tc.get_or_add_tcPr().append(shd)
def table(headers,rows):
    t=d.add_table(rows=1,cols=len(headers)); t.style='Table Grid'; t.alignment=WD_TABLE_ALIGNMENT.CENTER
    for c,v in zip(t.rows[0].cells,headers): c.text=v; shade(c); c.paragraphs[0].runs[0].font.color.rgb=RGBColor(255,255,255); c.paragraphs[0].runs[0].bold=True
    for row in rows:
        for c,v in zip(t.add_row().cells,row): c.text=str(v)
    return t

x=d.add_paragraph(); x.alignment=WD_ALIGN_PARAGRAPH.CENTER; r=x.add_run('INTERNSHIP / UDP / TRAINING REPORT – REPORTING 3'); r.bold=True; r.font.size=Pt(18); r.font.color.rgb=RGBColor(31,55,91)
x=d.add_paragraph(); x.alignment=WD_ALIGN_PARAGRAPH.CENTER; x.add_run('Advanced Implementation, Testing & Validation Progress Report').bold=True
p('Project: The Dossier – A Contract Checking and Tenant Awareness Tool for Mumbai Bachelor Rentals')
p('Student Name: Nikita Tilotia\nEnrollment Number: 23SE02ML209\nProgram/Branch: BTECH AI/ML\nSemester: 7\nContact Number: 7096205002\nEmail ID: 23se02ml209@ppsu.ac.in')
p('Type: UDP\nCompany/Organization: SOE\nDepartment/Domain: SOE\nMentor (Company): Mr. Vikas Chandra Sharma\nMentor (Institute): SOE\nStart Date: 08/06/2026\nEnd Date: 03/10/2026')

h('3. Work Progress Summary')
h('a) Project Title',2); p('The Dossier – A Contract Checking and Tenant Awareness Tool for Mumbai Bachelor Rentals')
h('b) Brief Overview of Work Completed After Reporting 2',2)
p('After Reporting 2, the project was expanded from a contract review tool into a practical rental-safety workspace. The existing agreement scanner was retained. New work focused on helping a Mumbai tenant choose an area, find a suitable roommate, prepare before signing, keep evidence during the tenancy, and record move-out actions.')
p('The map was redesigned as a locality decision tool rather than a decorative map. It now presents commute, estimated rent share, transport, monsoon, building and bachelor-society signals. These values are clearly labelled as demonstration estimates and are not presented as verified live market data. A roommate finder was added with locality, budget, move-in period and preference filters. A Tenant Workspace was added for before-signing checks, landlord questions, move-in records, move-out handover, shared-cost calculation, repair notes and payment evidence.')
h('Major tasks completed',2); bullets(['Created a locality discovery map for selected Mumbai areas.','Added filters and a locality decision snapshot.','Connected selected locality to the roommate finder.','Added roommate profiles, compatibility information and request-to-connect actions.','Added shared rent, maintenance and utility cost calculation.','Added repair, payment and receipt recording controls.','Simplified navigation and renamed History as My Rental Records.','Improved primary button contrast and tested the updated pages in a browser.'])
h('Modules completed',2); table(['Module','Work completed','Status'],[['Locality Decision Map','Area signals, commute view, rent share, transport, monsoon and building checks.','Completed'],['Roommate Finder','Search by area, budget and move-in period; request to connect.','Completed'],['Tenant Workspace','Before-signing, landlord questions, move-in, move-out and shared costs.','Completed'],['Contract Scanner','Existing clause review and plain-language findings retained.','Completed'],['My Rental Records','Existing scan history retained under a clearer name.','Completed'],['Property Buying Guidance','Plain-language buying checks and MahaRERA reminder retained.','In progress']])
h('Research / development work completed',2); p('The feature direction was reviewed around real rental problems faced by Mumbai bachelors: unclear society rules, roommate compatibility, total monthly cost, weak proof of payments, repair disputes and deposit recovery. The project was kept rule-based and explainable. Unverified locality figures were marked as demo estimates to avoid presenting sample data as official market information.')
h('Integration work completed',2); p('The new pages were integrated into the existing Streamlit multi-page application. Local navigation now connects the map, roommate finder, contract scanner and tenant workspace. No external API was added in this reporting period.')

h('c) Overall Project Completion Status',2)
table(['Component','Status','Completion (%)'],[['Requirement / Analysis','Completed','90'],['Design','Completed','90'],['Development','Completed','85'],['Integration','Completed','80'],['Testing','In Progress','70'],['Documentation','In Progress','70'],['Deployment','N.A.','0']])
p('Overall Project Completion: 82%')

h('4. Advanced Implementation')
h('a) Module / Feature Implementation',2)
table(['Module / Feature','Work Completed','Status'],[['Locality decision map','Added area selection, budget and commute filters, decision snapshot, area signals and source/demo labels.','Completed'],['Roommate finder','Added matching filters, rent share, move-in period, preference summary and safe request-to-connect action.','Completed'],['Tenant Workspace','Added checklists, landlord questions, WhatsApp-ready message, shared-cost calculator, repair/payment records and move-out actions.','Completed'],['Navigation and presentation','Removed generic Learn and Rulebook from main navigation, renamed History, improved button contrast and kept only useful rental flows.','Completed']])
h('b) Integration / Development Details',2)
p('Module integration: Property Guide stores the selected locality in Streamlit session state and passes it to the Roommate Finder. The agreement scanner remains the document-based review module, while the Tenant Workspace provides actions before and after the scan.')
p('API integration: No external API was used in this period. The map is a transparent prototype using local demonstration data. It must be connected to verified sources before public deployment.')
p('Database integration: Existing SQLite storage continues to store agreement reviews and their findings. The new workspace records are currently interactive prototype records and need permanent database tables in the next phase.')
p('Software integration: Python, Streamlit, SQLite, pypdf, python-docx and ReportLab continue to work together. Browser testing was used to verify routes and visible controls.')
p('Major coding work: Added views/roommates.py and views/property_guide.py, extended views/tenant_workspace.py, updated app.py navigation, and improved the Streamlit theme for readable action buttons.')
h('c) Final / Updated Architecture',2)
p('User selects Mumbai locality → reviews area decision snapshot → filters roommate matches → sends a safe connection request → uploads rental agreement → receives clause findings → asks landlord questions → records move-in condition, payments and repairs → completes move-out handover and deposit follow-up.')
p('The architecture keeps the original contract scanner and adds practical actions around it. The result is one connected rental journey rather than separate reading pages.')

h('5. Testing and Validation')
h('Testing Performed',2); table(['Test No.','Test / Function','Expected Result','Actual Result','Status'],[['1','Open Property Guide','Map and locality signals appear.','Property Guide opened and showed locality decision content.','Pass'],['2','Select locality and find roommates','Roommate page opens with selected area.','Selected area was carried into Roommate Finder.','Pass'],['3','Filter roommate listings','Only matching profiles appear.','Area and budget filters worked on demo profiles.','Pass'],['4','Open Tenant Workspace','All practical tabs and controls appear.','Before-signing, landlord questions, move-in, move-out and shared-cost tabs appeared.','Pass'],['5','Run Python validation','Updated files compile without syntax errors.','app.py and updated view/theme files passed py_compile.','Pass'],['6','Use map data responsibly','Demo values are not presented as official data.','Labels and source/estimate notes were shown.','Pass']])
p('Testing methods used: Functional Testing, Unit-level syntax validation, Integration Testing, System Testing and User-flow validation in a browser. Performance testing and formal user testing were not performed in this period.')

h('6. Results and Performance Analysis')
h('a) Final / Updated Results',2); bullets(['The application now supports a connected rental journey instead of only a scan result.','The map helps a user compare locality factors before contacting a roommate.','The roommate finder connects locality, budget and move-in timing.','The Tenant Workspace turns findings into questions, records and follow-up actions.','The navigation now gives each main page a clear purpose.'])
h('b) Performance Results',2); table(['Parameter / Metric','Result Obtained','Expected / Target','Status'],[['Updated files syntax check','Passed','No syntax errors','Met'],['Main new pages','Property Guide, Roommate Finder and Tenant Workspace loaded','All new pages load','Met'],['Locality handoff','Selected locality passed to roommate search','No repeated manual entry','Met'],['Data transparency','Demo labels shown for sample locality figures','No misleading market claim','Met'],['Automated live market accuracy','Not measured','Use verified live sources before deployment','Pending']])
h('c) Output / Result Screenshots',2)
p('Screenshot 1: Property Guide – locality decision map showing area signals and practical renting/buying checks.\nScreenshot 2: Roommate Finder – locality, budget and move-in filters with request-to-connect actions.\nScreenshot 3: Tenant Workspace – before-signing checklist, landlord questions, move-in record and shared-cost calculator.')
p('Evidence note: Actual browser screenshots should be inserted from the project preview before final submission. The testing record above reflects the browser validation performed during implementation.')

h('7. Challenges, Solutions and Improvements')
table(['Challenge / Problem','Solution Implemented','Final Outcome'],[['Sample rent and map figures could be mistaken for verified data.','Added demo-estimate and source/date wording and avoided claims of live accuracy.','More transparent prototype.'],['Roommate matching needed to be useful without unsafe public contact sharing.','Used preference filters and a request-to-connect action instead of displaying personal contact details.','Safer first-contact flow.'],['The project had useful features but navigation felt like separate pages.','Connected Property Guide, Roommate Finder, Scanner and Workspace into one rental journey.','Clearer product purpose.'],['Shared rent, repair and deposit problems happen outside the agreement.','Added cost calculator, evidence fields, repair status and move-out actions.','Broader practical value.']])
h('Improvements made after Reporting 2',2); bullets(['Replaced generic navigation with outcome-based pages.','Added map-driven locality selection.','Added roommate discovery and locality handoff.','Added practical rental records and shared-cost tools.','Improved accessibility of primary buttons through stronger text contrast.','Kept the app’s legal-adjacent limits clear: it is a first-check tool, not legal advice.'])

h('8. Current Project Status'); p('☒ Mostly Completed   ☐ Completed   ☐ Partially Completed   ☐ Work in Progress')
h('Completed Components',2); bullets(['Mumbai rental agreement scanner','Rule-based risk findings','Locality decision map prototype','Roommate Finder prototype','Tenant Workspace','Shared-cost calculator','Repair and payment record controls','Browser validation of main flows'])
h('Pending Components',2); bullets(['Verified live locality and rent data','Permanent database tables for roommate and evidence records','Authentication and privacy controls','Real user testing with Mumbai tenants','Formal legal review and deployment security checks'])
h('Work Planned Before Reporting 4',2); bullets(['Connect only verified or user-submitted locality data with source and date.','Add database persistence for roommate listings and tenant records.','Add profile safety, report and block controls.','Run a small usability test with real tenants or students after consent.','Insert genuine screenshots and attach test evidence.','Complete deployment and privacy documentation.'])

h('9. Learning and Skills Acquired')
h('Technical Skills',2); bullets(['Multi-page Streamlit integration and session-state navigation.','Building filter-based user flows.','Designing transparent rule-based outputs.','Handling document review alongside workflow records.','Browser-based functional validation.','Using SQLite-backed history and planning future persistence.'])
h('Tools / Technologies Learned',2); p('Python, Streamlit, SQLite, pypdf, python-docx, ReportLab, regular expressions, HTML/CSS styling, session state and browser testing.')
h('Professional Skills',2); bullets(['Converting user feedback into product changes.','Separating demo data from verified information.','Designing for non-technical users.','Thinking about privacy, safety and responsible claims.','Connecting multiple features around one real-world user journey.'])
h('Major Learning',2); p('A useful civic-tech product must not only explain a problem. It should help the user take the next safe action, keep proof, and understand the limits of the system. This reporting period helped move The Dossier in that direction.')

h('10. References and Resources Used')
refs=['Government of India. (n.d.). India Code: The Indian Contract Act, 1872. https://www.indiacode.nic.in','Government of India. (n.d.). India Code: The Registration Act, 1908. https://www.indiacode.nic.in','Maharashtra Department of Registration and Stamps. (n.d.). Official portal. https://igrmaharashtra.gov.in','MahaRERA. (n.d.). Maharashtra Real Estate Regulatory Authority. https://maharera.mahaonline.gov.in','Streamlit. (n.d.). Streamlit documentation. https://docs.streamlit.io','Python Software Foundation. (n.d.). Python documentation. https://docs.python.org','pypdf developers. (n.d.). pypdf documentation. https://pypdf.readthedocs.io','Python-docx developers. (n.d.). python-docx documentation. https://python-docx.readthedocs.io']
for r in refs: p(r)
p('Reference note: These resources were used for the application’s document processing, web framework, database workflow and legal-adjacent background. Locality and rent figures in the prototype are demonstration data and are not cited as official market statistics.')

h('Evaluation (To be filled by Mentor)'); table(['Criteria','Bloom’s Level','Marks Obtained (Out of 20)'],[['Work Completion','L3 – Apply',''],['Methodology Implementation','L3 – Apply / L4 – Analyze',''],['Tools & Technologies','L3 – Apply',''],['Documentation','L2 – Understand / L3 – Apply',''],['Understanding of Work','L2 – Understand / L4 – Analyze',''],['Total Marks','','']])
p('Student Signature: ____________________    Mentor (Company): ____________________    Mentor (Institute): ____________________')
p('Mentor Remarks: ____________________________________________________________________________________')
d.save(out); print(out)
