"""
Advanced Contract Generator - Legal-Heavy Templates
Generates realistic contracts with complex legal clauses, heavy penalties, and detailed terms.
"""

import random
import os
from datetime import datetime, timedelta

# Contract Templates
CONTRACT_TEMPLATES = {
    "master_service": {
        "name": "Master Service Agreement",
        "base_value": (50000, 500000),
        "penalties": (5000, 50000)
    },
    "nda": {
        "name": "Non-Disclosure Agreement",
        "base_value": (0, 25000),
        "penalties": (100000, 1000000)
    },
    "licensing": {
        "name": "Software Licensing and Distribution Agreement",
        "base_value": (100000, 2000000),
        "penalties": (25000, 250000)
    },
    "partnership": {
        "name": "Strategic Partnership Agreement",
        "base_value": (250000, 5000000),
        "penalties": (50000, 500000)
    },
    "employment": {
        "name": "Executive Employment Agreement",
        "base_value": (150000, 500000),
        "penalties": (25000, 100000)
    },
    "saas": {
        "name": "Software as a Service Agreement",
        "base_value": (50000, 500000),
        "penalties": (10000, 100000)
    },
    "data_processing": {
        "name": "Data Processing and Privacy Agreement",
        "base_value": (75000, 750000),
        "penalties": (100000, 5000000)
    },
    "acquisition": {
        "name": "Asset Purchase Agreement",
        "base_value": (1000000, 10000000),
        "penalties": (100000, 1000000)
    }
}

def generate_random_company():
    """Generate a random anonymous company name and address"""
    # Random company name patterns
    name_patterns = [
        f"Company {chr(random.randint(65, 90))}{chr(random.randint(65, 90))}{chr(random.randint(65, 90))}",  # Company ABC
        f"Entity {random.randint(100, 999)}",  # Entity 123
        f"Organization {chr(random.randint(65, 90))}{random.randint(10, 99)}",  # Organization A12
        f"Corporation {random.randint(1000, 9999)}",  # Corporation 1234
        f"Group {chr(random.randint(65, 90))}{chr(random.randint(65, 90))}{random.randint(1, 9)}",  # Group AB1
        f"Business {random.randint(10, 99)}{chr(random.randint(65, 90))}",  # Business 12A
        f"Enterprise {chr(random.randint(65, 90))}-{random.randint(100, 999)}",  # Enterprise X-123
        f"Firm {random.randint(500, 999)}",  # Firm 567
    ]
    
    # Random address patterns
    address_patterns = [
        f"Address {random.randint(100, 9999)}, Location {chr(random.randint(65, 90))}{chr(random.randint(65, 90))} {random.randint(10000, 99999)}",
        f"Building {chr(random.randint(65, 90))}{random.randint(1, 99)}, Suite {random.randint(100, 999)}",
        f"{random.randint(100, 9999)} Street {chr(random.randint(65, 90))}, City {random.randint(10, 99)}",
        f"Floor {random.randint(1, 50)}, Complex {chr(random.randint(65, 90))}{chr(random.randint(65, 90))}{chr(random.randint(65, 90))}",
        f"Unit {random.randint(1, 999)}, Zone {chr(random.randint(65, 90))}{random.randint(1, 9)}",
    ]
    
    return {
        "name": random.choice(name_patterns),
        "address": random.choice(address_patterns)
    }


def generate_master_service_agreement(contract_num: int, company1: dict, company2: dict, 
                                     start_date: datetime, end_date: datetime, value: int) -> str:
    """Generate a comprehensive Master Service Agreement with heavy legal terms"""
    
    penalty_breach = random.randint(10000, 50000)
    penalty_sla = random.randint(5000, 25000)
    penalty_termination = int(value * 0.25)  # 25% of contract value
    liability_cap = value * 12  # 12 months worth
    
    return f"""
MASTER SERVICE AGREEMENT

This Master Service Agreement ("Agreement") is entered into as of {start_date.strftime('%B %d, %Y')} 
("Effective Date"), by and between:

PARTY A: {company1['name']}
Address: {company1['address']}
("Company" or "Client")

AND

PARTY B: {company2['name']}
Address: {company2['address']}
("Vendor" or "Service Provider")

Collectively referred to as the "Parties" and individually as a "Party."

RECITALS

WHEREAS, the Company desires to engage the Vendor to provide comprehensive professional services;
WHEREAS, the Vendor represents that it has the expertise, resources, and capacity to perform such services;
WHEREAS, the Parties wish to establish the terms and conditions governing their business relationship;

NOW, THEREFORE, in consideration of the mutual covenants and agreements contained herein, and for other 
good and valuable consideration, the receipt and sufficiency of which are hereby acknowledged, the Parties 
agree as follows:

1. TERM AND TERMINATION

1.1 Initial Term: This Agreement shall commence on {start_date.strftime('%B %d, %Y')} and shall continue 
until {end_date.strftime('%B %d, %Y')} (the "Initial Term"), unless earlier terminated as provided herein.

1.2 Renewal: This Agreement shall automatically renew for successive one (1) year periods (each a "Renewal Term") 
unless either Party provides written notice of non-renewal at least ninety (90) days prior to the end of the 
then-current term.

1.3 Termination for Convenience: Either Party may terminate this Agreement for convenience upon sixty (60) 
days prior written notice to the other Party.

1.4 Termination for Cause: Either Party may terminate this Agreement immediately upon written notice if:
   (a) The other Party materially breaches any provision of this Agreement and fails to cure such breach 
       within thirty (30) days of receiving written notice;
   (b) The other Party becomes insolvent, files for bankruptcy, or makes an assignment for the benefit of creditors;
   (c) The other Party's professional license or accreditation is revoked or suspended.

1.5 Early Termination Penalty: In the event of termination by Company for convenience prior to the end of 
the Initial Term, Company shall pay Vendor an early termination fee equal to ${penalty_termination:,} USD 
(twenty-five percent of the remaining contract value) as liquidated damages, and not as a penalty.

2. SERVICES AND DELIVERABLES

2.1 Scope of Services: Vendor shall provide the following professional services as more particularly 
described in attached Statement of Work ("SOW"):
   (a) Strategic consulting and advisory services
   (b) Technical implementation and integration services
   (c) Ongoing support and maintenance
   (d) Training and knowledge transfer
   (e) Documentation and reporting

2.2 Service Levels: Vendor shall maintain service levels as specified in the Service Level Agreement 
("SLA") attached hereto as Exhibit A. Failure to meet SLAs shall result in service credits or penalties 
as specified in Section 7 herein.

2.3 Personnel: Vendor shall assign qualified personnel with appropriate expertise and experience. 
Vendor may not substitute key personnel without Company's prior written consent.

3. COMPENSATION AND PAYMENT TERMS

3.1 Fees: In consideration for the Services, Company shall pay Vendor ${value:,} USD per annum, 
payable in quarterly installments of ${value//4:,} USD.

3.2 Invoicing: Vendor shall submit invoices quarterly in advance. Each invoice shall itemize services 
rendered and any approved expenses.

3.3 Payment Terms: All invoices are due and payable net fifteen (15) days from the invoice date. 
Late payments shall accrue interest at the rate of 1.5% per month (18% per annum) or the maximum rate 
permitted by law, whichever is less.

3.4 Expenses: All expenses are included in the fees unless otherwise agreed in writing. Any expenses 
requiring pre-approval must be authorized by Company's designated representative.

3.5 Taxes: Fees are exclusive of all federal, state, local, and foreign taxes, duties, and similar 
assessments. Company shall be responsible for all such taxes except for taxes based on Vendor's income.

4. INTELLECTUAL PROPERTY RIGHTS

4.1 Work Product Ownership: All deliverables, work product, and materials created by Vendor in 
connection with this Agreement ("Work Product") shall be deemed "work made for hire" under U.S. 
copyright law and shall be the exclusive property of Company.

4.2 Assignment: To the extent any Work Product does not qualify as work made for hire, Vendor hereby 
irrevocably assigns to Company all right, title, and interest in and to such Work Product, including 
all intellectual property rights therein.

4.3 Pre-Existing Materials: Vendor retains ownership of any pre-existing materials, tools, or 
methodologies used in performing the Services. Vendor grants Company a perpetual, irrevocable, 
worldwide, royalty-free license to use such materials as incorporated into the Work Product.

5. CONFIDENTIALITY AND DATA PROTECTION

5.1 Confidential Information: Each Party acknowledges that it may receive confidential and proprietary 
information of the other Party ("Confidential Information"). Each Party agrees to:
   (a) Maintain the confidentiality of such information
   (b) Not disclose it to third parties without prior written consent
   (c) Use it only for purposes of performing this Agreement
   (d) Protect it with the same degree of care used to protect its own confidential information

5.2 Confidentiality Period: The obligations of confidentiality shall survive termination of this 
Agreement and continue indefinitely.

5.3 Data Protection Compliance: Vendor shall comply with all applicable data protection and privacy 
laws, including but not limited to GDPR, CCPA, and HIPAA (if applicable). Vendor shall implement 
appropriate technical and organizational measures to protect Personal Data.

5.4 Data Breach Notification: Vendor shall notify Company within twenty-four (24) hours of becoming 
aware of any unauthorized access, use, or disclosure of Company's Confidential Information or Personal Data.

5.5 Security Standards: Vendor shall maintain security certifications including SOC 2 Type II and 
ISO 27001 throughout the term of this Agreement.

6. REPRESENTATIONS AND WARRANTIES

6.1 Authority: Each Party represents and warrants that:
   (a) It has full power and authority to enter into this Agreement
   (b) This Agreement constitutes a legal, valid, and binding obligation
   (c) Execution of this Agreement does not violate any other agreement or obligation

6.2 Professional Standards: Vendor warrants that:
   (a) Services will be performed in a professional and workmanlike manner
   (b) Services will be performed by qualified personnel
   (c) Work Product will not infringe upon any third-party intellectual property rights
   (d) Vendor maintains all necessary licenses, permits, and insurance

6.3 Disclaimer: EXCEPT AS EXPRESSLY SET FORTH HEREIN, VENDOR MAKES NO WARRANTIES, EXPRESS OR IMPLIED, 
INCLUDING WARRANTIES OF MERCHANTABILITY OR FITNESS FOR A PARTICULAR PURPOSE.

7. SERVICE LEVEL PENALTIES AND LIQUIDATED DAMAGES

7.1 SLA Breach Penalty: In the event Vendor fails to meet the service levels specified in the SLA 
for any calendar month, Company shall be entitled to a service credit of ${penalty_sla:,} USD per 
incident, not to exceed ${penalty_sla * 5:,} USD per quarter.

7.2 Material Breach: In addition to any other remedies available at law or in equity, in the event 
of a material breach of this Agreement by Vendor, Company shall be entitled to liquidated damages 
of ${penalty_breach:,} USD per occurrence.

7.3 Data Breach Penalties: In the event of a data breach caused by Vendor's negligence or failure 
to comply with security requirements:
   (a) Initial penalty: ${penalty_breach * 2:,} USD
   (b) Daily penalty: ${penalty_breach // 10:,} USD per day until breach is remediated
   (c) Vendor shall bear all costs of breach notification, credit monitoring, and remediation

7.4 Limitation: The Parties agree that the liquidated damages specified herein represent a reasonable 
estimate of actual damages and are not intended as a penalty.

8. INDEMNIFICATION

8.1 Vendor's Indemnification: Vendor shall defend, indemnify, and hold harmless Company, its officers, 
directors, employees, and agents from and against any and all claims, damages, losses, liabilities, 
costs, and expenses (including reasonable attorneys' fees) arising out of or resulting from:
   (a) Vendor's breach of this Agreement
   (b) Vendor's negligence or willful misconduct
   (c) Infringement of third-party intellectual property rights by the Work Product
   (d) Violation of applicable laws or regulations by Vendor
   (e) Any data breach or security incident caused by Vendor

8.2 Company's Indemnification: Company shall defend, indemnify, and hold harmless Vendor from and 
against any claims arising out of:
   (a) Company's breach of this Agreement
   (b) Company's misuse of the Work Product
   (c) Claims that Company's materials infringe third-party rights

8.3 Indemnification Process: The indemnified Party shall:
   (a) Promptly notify the indemnifying Party of any claim
   (b) Cooperate in the defense of such claim
   (c) Allow the indemnifying Party to control the defense and settlement

9. LIMITATION OF LIABILITY

9.1 Cap on Liability: Except as provided in Section 9.2, each Party's total cumulative liability 
under this Agreement shall not exceed ${liability_cap:,} USD (twelve months of fees paid).

9.2 Exceptions: The limitation of liability shall not apply to:
   (a) Breaches of confidentiality obligations
   (b) Intellectual property infringement claims
   (c) Gross negligence or willful misconduct
   (d) Indemnification obligations
   (e) Fraud or criminal acts

9.3 Consequential Damages: NEITHER PARTY SHALL BE LIABLE FOR ANY INDIRECT, INCIDENTAL, SPECIAL, 
CONSEQUENTIAL, OR PUNITIVE DAMAGES, INCLUDING LOST PROFITS, EVEN IF ADVISED OF THE POSSIBILITY THEREOF.

10. INSURANCE

10.1 Required Coverage: Vendor shall maintain the following insurance coverage throughout the term:
   (a) Commercial General Liability: ${penalty_breach * 20:,} USD per occurrence
   (b) Professional Liability (E&O): ${penalty_breach * 20:,} USD per claim
   (c) Cyber Liability Insurance: ${penalty_breach * 10:,} USD per incident
   (d) Workers' Compensation: As required by applicable law

10.2 Proof of Insurance: Vendor shall provide certificates of insurance to Company upon request 
and shall name Company as an additional insured on all applicable policies.

11. COMPLIANCE AND AUDIT RIGHTS

11.1 Legal Compliance: Each Party shall comply with all applicable federal, state, local, and 
foreign laws, regulations, and industry standards, including but not limited to:
   (a) Anti-bribery and anti-corruption laws (FCPA, UK Bribery Act)
   (b) Export control regulations (ITAR, EAR)
   (c) Labor and employment laws
   (d) Environmental regulations
   (e) Data protection and privacy laws

11.2 Audit Rights: Company shall have the right, upon reasonable notice and during regular business 
hours, to audit Vendor's compliance with this Agreement, including inspection of records, facilities, 
and security controls.

11.3 Non-Compliance Penalties: Failure to comply with applicable laws or permit audit as required 
shall constitute a material breach and may result in immediate termination and penalties of up to 
${penalty_breach * 5:,} USD.

12. FORCE MAJEURE

12.1 Excused Performance: Neither Party shall be liable for any failure or delay in performance due 
to causes beyond its reasonable control, including acts of God, war, terrorism, strikes, government 
orders, epidemics, or natural disasters ("Force Majeure Event").

12.2 Notice and Mitigation: The affected Party shall:
   (a) Promptly notify the other Party of the Force Majeure Event
   (b) Use commercially reasonable efforts to mitigate the effects
   (c) Resume performance as soon as reasonably practicable

12.3 Right to Terminate: If a Force Majeure Event continues for more than sixty (60) days, either 
Party may terminate this Agreement upon written notice without penalty.

13. DISPUTE RESOLUTION

13.1 Negotiation: In the event of any dispute arising under this Agreement, the Parties shall first 
attempt to resolve the matter through good faith negotiations between senior executives.

13.2 Mediation: If negotiations fail to resolve the dispute within thirty (30) days, the Parties 
agree to submit the matter to non-binding mediation before a mutually agreed mediator.

13.3 Arbitration: Any dispute not resolved through mediation shall be resolved through binding 
arbitration administered by the American Arbitration Association in accordance with its Commercial 
Arbitration Rules.

13.4 Arbitration Location: Arbitration shall be conducted in Jurisdiction A.

13.5 Costs: Each Party shall bear its own costs of arbitration, with the arbitrator's fees split equally.

13.6 Injunctive Relief: Nothing herein shall prevent either Party from seeking injunctive relief in 
a court of competent jurisdiction for breaches of confidentiality or intellectual property rights.

14. GENERAL PROVISIONS

14.1 Entire Agreement: This Agreement, including all exhibits and attachments, constitutes the entire 
agreement between the Parties and supersedes all prior negotiations, understandings, and agreements.

14.2 Amendments: This Agreement may be amended only by a written instrument signed by both Parties.

14.3 Assignment: Neither Party may assign this Agreement without the prior written consent of the 
other Party, except that either Party may assign to a successor in connection with a merger, acquisition, 
or sale of substantially all assets.

14.4 Severability: If any provision of this Agreement is held to be invalid or unenforceable, the 
remaining provisions shall continue in full force and effect.

14.5 Waiver: No waiver of any provision shall be deemed a waiver of any other provision or of the 
same provision on another occasion.

14.6 Governing Law: This Agreement shall be governed by and construed in accordance with the laws 
of Jurisdiction A, without regard to its conflict of law principles.

14.7 Notices: All notices under this Agreement shall be in writing and delivered by certified mail, 
overnight courier, or email with confirmation of receipt to the addresses set forth above.

14.8 Survival: Provisions relating to confidentiality, intellectual property, indemnification, 
limitation of liability, and dispute resolution shall survive termination of this Agreement.

14.9 Counterparts: This Agreement may be executed in counterparts, each of which shall be deemed 
an original and all of which together shall constitute one instrument.

IN WITNESS WHEREOF, the Parties have executed this Agreement as of the date first written above.

{company1['name']}                    {company2['name']}

By: _____________________             By: _____________________
Name: [Authorized Signatory]          Name: [Authorized Signatory]
Title: Chief Executive Officer        Title: Chief Executive Officer
Date: {start_date.strftime('%B %d, %Y')}                    Date: {start_date.strftime('%B %d, %Y')}


EXHIBITS:

Exhibit A: Service Level Agreement
Exhibit B: Statement of Work
Exhibit C: Security Requirements and Standards
Exhibit D: Data Processing Addendum
Exhibit E: Approved Expense Categories

[END OF AGREEMENT]

Contract Number: CNT-2024-{str(contract_num).zfill(3)}
Total Contract Value: ${value:,} USD
Annual Payment: ${value:,} USD (quarterly payments of ${value//4:,} USD)
Term: {start_date.strftime('%B %d, %Y')} to {end_date.strftime('%B %d, %Y')}
"""


def generate_nda_agreement(contract_num: int, company1: dict, company2: dict, 
                          start_date: datetime, end_date: datetime) -> str:
    """Generate a strict Non-Disclosure Agreement with heavy penalties"""
    
    penalty_breach = random.randint(500000, 2000000)
    penalty_per_day = random.randint(10000, 50000)
    
    return f"""
MUTUAL NON-DISCLOSURE AGREEMENT

This Mutual Non-Disclosure Agreement ("Agreement") is entered into as of {start_date.strftime('%B %d, %Y')} 
("Effective Date"), by and between:

PARTY A: {company1['name']}
Address: {company1['address']}
("Disclosing Party A")

AND

PARTY B: {company2['name']}
Address: {company2['address']}
("Disclosing Party B")

Each party may be referred to individually as a "Party" or collectively as the "Parties."

RECITALS

WHEREAS, the Parties wish to explore a potential business relationship concerning [Strategic Partnership/
Merger & Acquisition/Technology Licensing/Joint Venture] ("Purpose");

WHEREAS, in connection with such discussions, each Party may disclose to the other certain confidential 
and proprietary information;

WHEREAS, the Parties desire to protect the confidentiality of such information;

NOW, THEREFORE, in consideration of the mutual covenants and agreements contained herein, the Parties 
agree as follows:

1. DEFINITION OF CONFIDENTIAL INFORMATION

1.1 Scope: "Confidential Information" means any and all technical, business, financial, customer, or 
other information disclosed by one Party (the "Disclosing Party") to the other Party (the "Receiving Party"), 
whether disclosed orally, in writing, electronically, or by inspection of tangible objects, including but 
not limited to:

   (a) Trade secrets, inventions, ideas, processes, formulas, source code, algorithms, and know-how
   (b) Financial information, including revenues, costs, profits, sales figures, and pricing strategies
   (c) Business plans, marketing plans, and strategic initiatives
   (d) Customer lists, supplier lists, and vendor information
   (e) Product specifications, designs, drawings, and prototypes
   (f) Research and development activities and results
   (g) Personnel information, including compensation and organizational structure
   (h) Information regarding mergers, acquisitions, divestitures, or other transactions
   (i) Any other information marked "Confidential," "Proprietary," or with a similar designation
   (j) Information that a reasonable person would understand to be confidential given its nature and 
       the circumstances of disclosure

1.2 Exclusions: Confidential Information shall not include information that:
   (a) Was known to the Receiving Party prior to disclosure, as evidenced by written records
   (b) Is or becomes publicly available through no breach of this Agreement
   (c) Is rightfully received by the Receiving Party from a third party without breach of any obligation
   (d) Is independently developed by the Receiving Party without use of the Confidential Information
   (e) Is required to be disclosed by law, regulation, or court order (subject to Section 3.4)

2. OBLIGATIONS OF RECEIVING PARTY

2.1 Non-Disclosure: The Receiving Party shall:
   (a) Hold all Confidential Information in strict confidence
   (b) Not disclose Confidential Information to any third party without prior written consent
   (c) Not use Confidential Information for any purpose other than the Purpose
   (d) Protect Confidential Information with the same degree of care used to protect its own confidential 
       information, but in no event less than reasonable care

2.2 Limited Disclosure: The Receiving Party may disclose Confidential Information only to its employees, 
officers, directors, consultants, and advisors (collectively, "Representatives") who:
   (a) Have a legitimate need to know for the Purpose
   (b) Have been informed of the confidential nature of the information
   (c) Are bound by confidentiality obligations no less restrictive than those contained herein

2.3 Responsibility for Representatives: The Receiving Party shall be fully responsible and liable for 
any breach of this Agreement by its Representatives.

2.4 Security Measures: The Receiving Party shall implement and maintain appropriate technical, 
organizational, and physical safeguards to protect Confidential Information, including:
   (a) Access controls and authentication mechanisms
   (b) Encryption of data at rest and in transit
   (c) Secure storage facilities and locked cabinets
   (d) Regular security audits and penetration testing
   (e) Employee training on data protection and confidentiality

3. ADDITIONAL OBLIGATIONS

3.1 No Reverse Engineering: The Receiving Party shall not reverse engineer, disassemble, or decompile 
any prototypes, software, or technical information disclosed by the Disclosing Party.

3.2 No Copying: The Receiving Party shall not copy, reproduce, or create derivative works based on 
Confidential Information without the Disclosing Party's prior written consent.

3.3 Return of Materials: Upon request or termination of this Agreement, the Receiving Party shall:
   (a) Promptly return or destroy all Confidential Information and copies thereof
   (b) Certify in writing that all such materials have been returned or destroyed
   (c) Permanently delete all electronic copies of Confidential Information

3.4 Compelled Disclosure: If the Receiving Party is required by law, regulation, or court order to 
disclose Confidential Information, it shall:
   (a) Promptly notify the Disclosing Party (unless prohibited by law)
   (b) Cooperate with the Disclosing Party's efforts to obtain protective orders
   (c) Disclose only the minimum information required
   (d) Request confidential treatment of the disclosed information

4. NO LICENSE OR OWNERSHIP RIGHTS

4.1 Ownership: All Confidential Information remains the exclusive property of the Disclosing Party. 
No license or other rights in the Confidential Information are granted or implied by this Agreement.

4.2 No Obligation to Proceed: Nothing in this Agreement obligates either Party to proceed with any 
transaction, enter into any business relationship, or continue discussions.

4.3 No Warranty: All Confidential Information is provided "AS IS" without any warranty of accuracy, 
completeness, or fitness for any purpose.

5. TERM AND TERMINATION

5.1 Term: This Agreement shall commence on the Effective Date and continue until {end_date.strftime('%B %d, %Y')}.

5.2 Survival: The obligations of confidentiality hereunder shall survive termination of this Agreement 
and continue for a period of ten (10) years from the date of disclosure, or indefinitely for information 
constituting trade secrets under applicable law.

5.3 Return of Materials: Within ten (10) business days of termination, each Party shall comply with 
the obligations set forth in Section 3.3.

6. REMEDIES AND ENFORCEMENT

6.1 Irreparable Harm: The Receiving Party acknowledges that any breach of this Agreement may cause 
irreparable harm to the Disclosing Party for which monetary damages would be an inadequate remedy.

6.2 Injunctive Relief: Accordingly, in addition to all other remedies available at law or in equity, 
the Disclosing Party shall be entitled to seek injunctive relief, specific performance, and other 
equitable remedies to prevent or restrain any breach or threatened breach of this Agreement.

6.3 Liquidated Damages: In the event of any unauthorized disclosure or use of Confidential Information, 
the Receiving Party shall pay to the Disclosing Party liquidated damages in the amount of:
   (a) ${penalty_breach:,} USD per breach incident
   (b) ${penalty_per_day:,} USD per day for each day the breach continues unremediated
   (c) All costs and expenses incurred by the Disclosing Party in responding to the breach, including:
       - Forensic investigation costs
       - Customer notification expenses
       - Credit monitoring services
       - Public relations and crisis management
       - Legal fees and court costs

6.4 Actual Damages: The liquidated damages specified above are in addition to, and not in lieu of, 
any actual damages suffered by the Disclosing Party as a result of the breach.

6.5 Data Breach Obligations: In the event of any data breach, unauthorized access, or security incident 
involving Confidential Information, the Receiving Party shall:
   (a) Immediately notify the Disclosing Party (within 24 hours of discovery)
   (b) Conduct a thorough investigation and provide a detailed incident report
   (c) Take immediate steps to contain and remediate the breach
   (d) Cooperate fully with any investigation by the Disclosing Party or regulatory authorities
   (e) Bear all costs associated with breach notification, remediation, and damages

7. REGULATORY COMPLIANCE

7.1 Applicable Laws: Each Party shall comply with all applicable laws and regulations regarding the 
protection of confidential information, including but not limited to:
   (a) Trade secret laws (Defend Trade Secrets Act, state trade secret acts)
   (b) Data protection laws (GDPR, CCPA, HIPAA if applicable)
   (c) Export control regulations (ITAR, EAR)
   (d) Securities laws and regulations regarding material non-public information

7.2 GDPR Compliance: If Confidential Information includes Personal Data subject to GDPR, the Receiving 
Party shall:
   (a) Process such data only as necessary for the Purpose
   (b) Implement appropriate technical and organizational measures
   (c) Maintain records of processing activities
   (d) Comply with data subject rights requests
   (e) Report any personal data breaches within 72 hours

7.3 Reporting Obligations: The Parties acknowledge that certain disclosures may trigger reporting 
obligations under securities laws or other regulations. Each Party agrees to consult with legal counsel 
before making any such disclosures.

8. NON-SOLICITATION AND NON-COMPETE

8.1 Non-Solicitation of Employees: During the term of this Agreement and for twenty-four (24) months 
thereafter, neither Party shall, without the prior written consent of the other Party:
   (a) Solicit, recruit, or hire any employee of the other Party who had access to Confidential Information
   (b) Encourage any such employee to leave their employment
   (c) Assist any third party in soliciting or hiring such employees

8.2 Non-Solicitation Penalty: Any breach of the non-solicitation provision shall result in a penalty 
of ${penalty_breach // 2:,} USD per employee solicited or hired, plus reimbursement of all recruitment 
and training costs.

8.3 Limited Non-Compete: If the Parties do not proceed with the contemplated transaction, each Party 
agrees not to use the Confidential Information of the other Party to develop competing products or 
services for a period of twelve (12) months.

9. AUDIT AND MONITORING RIGHTS

9.1 Audit Rights: Upon reasonable notice, the Disclosing Party shall have the right to audit the 
Receiving Party's compliance with this Agreement, including:
   (a) Inspection of security measures and controls
   (b) Review of access logs and monitoring records
   (c) Verification of destruction or return of materials

9.2 Monitoring: The Receiving Party consents to the Disclosing Party's use of technological measures 
to monitor access to and use of Confidential Information, including watermarking, tracking codes, and 
digital rights management.

10. INDEMNIFICATION

10.1 Indemnity: The Receiving Party shall indemnify, defend, and hold harmless the Disclosing Party 
and its officers, directors, employees, and agents from and against any and all claims, damages, losses, 
liabilities, costs, and expenses (including reasonable attorneys' fees) arising out of or resulting from:
   (a) Any breach of this Agreement by the Receiving Party
   (b) Any unauthorized use or disclosure of Confidential Information
   (c) Any negligence or willful misconduct of the Receiving Party
   (d) Any violation of applicable laws by the Receiving Party

11. GENERAL PROVISIONS

11.1 Governing Law: This Agreement shall be governed by and construed in accordance with the laws of 
Jurisdiction A, without regard to its conflicts of law principles.

11.2 Jurisdiction and Venue: The Parties consent to the exclusive jurisdiction and venue of the courts 
located in Jurisdiction A for any disputes arising under this Agreement.

11.3 Entire Agreement: This Agreement constitutes the entire agreement between the Parties regarding 
the subject matter hereof and supersedes all prior agreements and understandings.

11.4 Amendments: This Agreement may be amended only by a written instrument signed by both Parties.

11.5 Severability: If any provision of this Agreement is held to be invalid or unenforceable, the 
remaining provisions shall remain in full force and effect.

11.6 Waiver: No waiver of any provision shall be deemed a waiver of any other provision or of the same 
provision on another occasion.

11.7 Assignment: Neither Party may assign its rights or obligations under this Agreement without the 
prior written consent of the other Party.

11.8 Notices: All notices shall be in writing and delivered by certified mail, overnight courier, or 
email with confirmation of receipt to the addresses set forth above.

11.9 Counterparts: This Agreement may be executed in counterparts, each of which shall be deemed an 
original.

11.10 Survival: All provisions of this Agreement that by their nature should survive termination shall 
survive, including but not limited to Sections 2, 3, 6, 7, 8, and 10.

IN WITNESS WHEREOF, the Parties have executed this Agreement as of the date first written above.

{company1['name']}                    {company2['name']}

By: _____________________             By: _____________________
Name: [Authorized Signatory]          Name: [Authorized Signatory]
Title: Chief Executive Officer        Title: Chief Executive Officer
Date: {start_date.strftime('%B %d, %Y')}                    Date: {start_date.strftime('%B %d, %Y')}

[END OF AGREEMENT]

Contract Number: CNT-2024-{str(contract_num).zfill(3)}
Agreement Type: Mutual Non-Disclosure Agreement
Term: {start_date.strftime('%B %d, %Y')} to {end_date.strftime('%B %d, %Y')}
Confidentiality Period: 10 years from disclosure (indefinite for trade secrets)
Breach Penalty: ${penalty_breach:,} USD per incident + ${penalty_per_day:,} USD per day
"""


def main():
    """Generate advanced legal contracts"""
    
    print("\n" + "="*70)
    print("ADVANCED CONTRACT GENERATOR - LEGAL-HEAVY TEMPLATES")
    print("="*70 + "\n")
    
    # Create contracts directory
    os.makedirs("data/contracts_advanced", exist_ok=True)
    
    # Generate 30 contracts with varied types
    contract_types = ['master_service', 'nda']  # We have generators for these two
    generated_count = 0
    start_num = 101  # Start from CNT-2024-101
    
    for i in range(30):
        contract_num = start_num + i
        contract_type = random.choice(contract_types)
        
        # Generate random anonymous companies
        company1 = generate_random_company()
        company2 = generate_random_company()
        
        # Generate random dates
        # Some contracts in the past, some active, some future
        days_offset = random.randint(-365, 180)  # Can start up to 1 year ago or 6 months in future
        start_date = datetime.now() + timedelta(days=days_offset)
        
        # Contract duration varies
        duration_days = random.randint(365, 1825)  # 1 to 5 years
        end_date = start_date + timedelta(days=duration_days)
        
        try:
            if contract_type == 'master_service':
                # Varied contract values
                template = CONTRACT_TEMPLATES['master_service']
                value = random.randint(template['base_value'][0], template['base_value'][1])
                contract = generate_master_service_agreement(contract_num, company1, company2, start_date, end_date, value)
                type_name = "Master Service Agreement"
                
            elif contract_type == 'nda':
                contract = generate_nda_agreement(contract_num, company1, company2, start_date, end_date)
                type_name = "Non-Disclosure Agreement"
            
            # Save contract
            filename = f"data/contracts_advanced/CNT-2024-{str(contract_num).zfill(3)}.txt"
            with open(filename, 'w', encoding='utf-8') as f:
                f.write(contract)
            
            generated_count += 1
            print(f"[OK] Generated: CNT-2024-{str(contract_num).zfill(3)} ({type_name})")
            print(f"     Parties: {company1['name'][:30]}... & {company2['name'][:30]}...")
            print(f"     Term: {start_date.strftime('%Y-%m-%d')} to {end_date.strftime('%Y-%m-%d')}")
            
        except Exception as e:
            print(f"[ERROR] Failed to generate CNT-2024-{str(contract_num).zfill(3)}: {e}")
    
    print("\n" + "="*70)
    print(f"[OK] Successfully generated {generated_count} advanced legal contracts")
    print(f"[OK] Location: data/contracts_advanced/")
    print(f"[OK] Contract Numbers: CNT-2024-{str(start_num).zfill(3)} to CNT-2024-{str(start_num + 29).zfill(3)}")
    print("="*70 + "\n")
    
    print("Contract Features:")
    print("[+] Heavy legal language and terminology")
    print("[+] Substantial penalty clauses ($10K - $2M)")
    print("[+] Detailed indemnification provisions")
    print("[+] Comprehensive compliance requirements")
    print("[+] Data breach and security obligations")
    print("[+] Liquidated damages provisions")
    print("[+] Arbitration and dispute resolution")
    print("[+] Insurance requirements")
    print("[+] Force majeure clauses")
    print("[+] Survival and severability provisions")
    print("\nContract Types Distribution:")
    print(f"  - Master Service Agreements: ~{int(generated_count * 0.5)}")
    print(f"  - Non-Disclosure Agreements: ~{int(generated_count * 0.5)}")
    print(f"\nTotal Files: {generated_count}\n")


if __name__ == "__main__":
    main()