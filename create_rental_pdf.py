from reportlab.lib import colors
from reportlab.lib.enums import TA_CENTER
from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import mm
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle, PageBreak

OUT = "/vercel/share/v0-project/mumbai-bachelor-rental-agreement-sample.pdf"
styles = getSampleStyleSheet()
styles.add(ParagraphStyle(name="TitleCenter", parent=styles["Title"], alignment=TA_CENTER, textColor=colors.HexColor("#243b63"), spaceAfter=10))
styles.add(ParagraphStyle(name="Subtitle", parent=styles["Normal"], alignment=TA_CENTER, textColor=colors.HexColor("#667085"), leading=16, spaceAfter=16))
styles.add(ParagraphStyle(name="Section", parent=styles["Heading2"], textColor=colors.HexColor("#243b63"), spaceBefore=12, spaceAfter=6))
styles.add(ParagraphStyle(name="Body", parent=styles["BodyText"], leading=15, spaceAfter=6))
styles.add(ParagraphStyle(name="Small", parent=styles["BodyText"], fontSize=8.5, leading=11, textColor=colors.HexColor("#667085")))

story = []
story += [Paragraph("LEAVE AND LICENSE AGREEMENT", styles["TitleCenter"]), Paragraph("Sample Mumbai residential agreement for a rented home occupied by working bachelors", styles["Subtitle"])]
notice = "<b>Sample for academic demonstration only.</b> Replace all bracketed fields, check the society rules, and have a Maharashtra property lawyer or registration professional review it before signing."
t = Table([[Paragraph(notice, styles["Body"])]], colWidths=[170*mm]); t.setStyle(TableStyle([("BACKGROUND", (0,0), (-1,-1), colors.HexColor("#eef4ff")), ("BOX", (0,0), (-1,-1), 0.7, colors.HexColor("#9bb6e3")), ("LEFTPADDING", (0,0), (-1,-1), 10), ("RIGHTPADDING", (0,0), (-1,-1), 10)])); story += [t, Spacer(1, 8)]

story += [Paragraph("1. Parties", styles["Section"]), Paragraph("This Agreement is made on <b>[DATE]</b> at Mumbai, Maharashtra, between <b>[LANDLORD FULL NAME]</b>, residing at <b>[LANDLORD ADDRESS]</b> (the “Licensor”), and the following licensees: <b>[BACHELOR 1 NAME]</b>, <b>[BACHELOR 2 NAME]</b>, and <b>[BACHELOR 3 NAME]</b>, collectively residing at the licensed premises (the “Licensees”). Each licensee is jointly responsible for the promises and payments in this Agreement.", styles["Body"])]

story += [Paragraph("2. Premises and permitted use", styles["Section"]), Paragraph("The Licensor permits the Licensees to occupy <b>[FULL FLAT ADDRESS, BUILDING, AREA, MUMBAI, PIN]</b>, including <b>[ROOMS / PARKING / FURNITURE]</b>. The premises may be used only as a private residence by the named Licensees. No paying guests, subletting, commercial activity, or additional occupants are allowed without the Licensor’s written consent.", styles["Body"])]

story += [Paragraph("3. Term and possession", styles["Section"]), Paragraph("The licence begins on <b>[START DATE]</b> and ends on <b>[END DATE]</b>. Possession will be handed over after payment of the deposit and first month’s licence fee. Renewal must be recorded in writing. On expiry or termination, the Licensees must vacate, return keys, and hand back the premises in reasonably clean condition, subject to normal wear and tear.", styles["Body"])]

story += [Paragraph("4. Fees and deposit", styles["Section"])]
data = [["Item", "Amount / timing"], ["Monthly licence fee", "INR [AMOUNT], payable by the [DAY] of each month"], ["Refundable security deposit", "INR [AMOUNT], subject to lawful deductions and settlement"], ["Utilities", "Electricity, gas, internet and water charges paid by [PARTY] as per actual bills"], ["Late payment", "INR [AMOUNT] or [PERCENT]% after [NUMBER] days, if agreed and lawful"]]
t = Table(data, colWidths=[55*mm, 115*mm]); t.setStyle(TableStyle([("BACKGROUND", (0,0), (-1,0), colors.HexColor("#243b63")), ("TEXTCOLOR", (0,0), (-1,0), colors.white), ("GRID", (0,0), (-1,-1), 0.4, colors.HexColor("#cbd5e1")), ("VALIGN", (0,0), (-1,-1), "TOP"), ("PADDING", (0,0), (-1,-1), 7)])); story += [t]

story += [Paragraph("5. Repairs, maintenance and condition", styles["Section"]), Paragraph("The Licensees must promptly report leaks, electrical faults, structural issues, or other damage. The Licensor is responsible for ordinary structural repairs unless damage was caused by the Licensees or their guests. The Licensees must not make alterations, drill into structural walls, change locks, or install appliances without written consent. An inventory and move-in condition record should be signed and attached.", styles["Body"])]

story += [Paragraph("6. House rules and society compliance", styles["Section"]), Paragraph("The Licensees must follow the housing society’s registered rules, visitor procedures, quiet hours, parking rules, waste rules, and safety requirements. The Licensees must not create nuisance, damage common areas, store hazardous items, or disturb neighbours. The Licensor should provide the applicable society rules before possession.", styles["Body"])]

story += [Paragraph("7. Police verification and identity documents", styles["Section"]), Paragraph("The parties will cooperate with Maharashtra police verification and society registration requirements, where applicable. The Licensees will provide accurate identity and employment/contact details. Personal documents should be shared only through a secure channel and retained only as required.", styles["Body"])]

story += [Paragraph("8. Visitors and additional occupants", styles["Section"]), Paragraph("Short-term visitors are permitted subject to society rules. No person may move in, pay rent, or receive exclusive use of a room without the Licensor’s written approval and any required update to the agreement or police/society records.", styles["Body"])]

story += [Paragraph("9. Termination", styles["Section"]), Paragraph("Either party may terminate this Agreement by giving <b>[30 / 60]</b> days’ written notice. Immediate termination may be sought for serious unlawful use, material non-payment after written demand, substantial property damage, or repeated nuisance, subject to applicable law and due process. The deposit must be accounted for after inspection and adjustment of undisputed dues.", styles["Body"])]

story += [Paragraph("10. Disputes and governing law", styles["Section"]), Paragraph("The parties will first try to resolve disputes in writing within 15 days. This Agreement is governed by the laws applicable in Maharashtra. Courts at Mumbai will have jurisdiction, subject to any mandatory legal forum or statutory process.", styles["Body"])]

story += [Paragraph("11. Signatures", styles["Section"])]
sig = [["Licensor", "Licensee 1", "Licensee 2", "Licensee 3"], ["\n\nSignature: __________", "\n\nSignature: __________", "\n\nSignature: __________", "\n\nSignature: __________"], ["Name: __________", "Name: __________", "Name: __________", "Name: __________"]]
t = Table(sig, colWidths=[42.5*mm]*4); t.setStyle(TableStyle([("BACKGROUND", (0,0), (-1,0), colors.HexColor("#eef4ff")), ("GRID", (0,0), (-1,-1), 0.4, colors.HexColor("#cbd5e1")), ("PADDING", (0,0), (-1,-1), 7), ("VALIGN", (0,0), (-1,-1), "TOP")])); story += [t, Spacer(1, 10), Paragraph("Witness 1: [NAME / SIGNATURE] &nbsp;&nbsp;&nbsp;&nbsp; Witness 2: [NAME / SIGNATURE]", styles["Body"])]

story += [PageBreak(), Paragraph("How The Dossier uses this sample", styles["Section"]), Paragraph("• The scanner checks whether important protections are present, missing, or one-sided.<br/>• It can flag payment terms, termination rights, deposit handling, liability, indemnity, governing law, renewal terms, and other playbook items.<br/>• The result shows the exact wording that triggered a finding, so a non-lawyer can discuss it with a mentor or lawyer.<br/>• This sample is intentionally educational and contains blanks rather than real personal information.", styles["Body"]), Paragraph("Important: A leave-and-license agreement is not a substitute for registration, stamp-duty guidance, society approval, police verification, or legal review. The correct process can depend on the facts and current Maharashtra requirements.", styles["Small"])]

doc = SimpleDocTemplate(OUT, pagesize=A4, rightMargin=20*mm, leftMargin=20*mm, topMargin=18*mm, bottomMargin=18*mm, title="Sample Mumbai Bachelor Rental Agreement")
doc.build(story)
print(OUT)
