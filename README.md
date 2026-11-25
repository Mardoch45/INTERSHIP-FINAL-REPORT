# PENETRATION TESTING REPORT

### Mediroza — Final Internship Project — Public Edition

**WEEK 4  |  CYBERSECURITY  |  NETWORKWALKS**

**Formatted report:** [PDF](docs/Public_Report_Mardochee_BONOU_B084.pdf) | [Editable DOCX](docs/Public_Report_Mardochee_BONOU_B084.docx)

**Evidence:** [Command reference](COMMANDS.md) | [Screenshot gallery](evidence/README.md)

| Field | Detail |
|---|---|
| Pentester | Mardochée BONOU |
| Program / Batch | B084 — Networkwalks |
| Documented assessment dates | 22–25 November 2026 |
| Milestones | M1: initial access; M2: PDF recovery; M3: data analysis; M4: reporting |
| Client / target | Demonstration hospital — mediroza.example |
| Phases covered | Reconnaissance, enumeration, impact validation, evidence analysis and reporting |
| Classification | Public — redacted evidence and synthetic demonstration data |
| GitHub profile | https://github.com/Mardoch45 |

# 1. Liability Disclaimer and Authorization

This assessment was conducted as a Networkwalks educational project whose brief states that written authorization was granted. Testing was limited to the authorized domain. Social engineering, denial of service and out-of-scope testing were excluded. The methods described here apply only to authorized environments.

This public edition includes explicitly redacted derivatives of the original VM screenshots. Patient records, employee and shareholder identities, individual salaries, document passwords and original verification hashes remain in the confidential deliverable. The .example domain and the repository SQL dataset are demonstration elements. Redacted screenshots document the original exercise; they are not evidence that commands were run against the example domain.

# 2. Introduction and Executive Summary

This report documents my final project during Week 4 of the Networkwalks Cybersecurity & Ethical Hacking internship. It extends reconnaissance into document recovery, examination of PDF protections and analysis of an exposed SQL backup.

The four milestones were to retrieve three patient reports, recover access to all three encrypted PDFs, identify exposed employee salaries and shareholder details, and produce a professional penetration testing report with evidence, risk analysis and remediation.

The trainee reports SQL injection as the initial access method and supplied input and report-page screenshots, but the complete HTTP request is not archived. Opening the three original PDFs and extracting the two SQL tables were independently verified locally. The proposed overall risk is High for confidentiality. Database modification and service interruption were not demonstrated.

| Milestone | Documented result | Evidence status |
| --- | --- | --- |
| M1 | Three patient reports retrieved | Reported by the trainee; supporting screenshots available |
| M2 | Three passwords recovered and documents opened | Verified against the original files |
| M3 | 30 employees and 10 shareholders extracted | Complete extraction and consistency checks |
| M4 | Report, command reference and evidence gallery | Prepared for review |

# 3. Scope and Methodology

Participant: Mardochée BONOU, Batch B084. The supplied project brief bears reference B083; the participant confirmed B084 as the correct personal batch. The brief allows five days, while the available evidence documents work from 22 to 25 November 2026.

The workflow included WHOIS, DNS resolution, web fingerprinting, path enumeration, portal examination, PDF retrieval, offline password testing, metadata examination and local SQL analysis. Technical assistance was used for data analysis and document preparation. Source observations are distinguished from interpretations and evidence limitations.

All records in the supplied staff and shareholders tables were analyzed. The network evidence was collected by the trainee and was not replayed when building this report. An open port, public address or identified technology is not by itself an exploitable vulnerability.

# 4. Tools Used

| Tool | Purpose |
| --- | --- |
| Kali Linux | Trainee VM environment |
| WHOIS, nslookup and DNSRecon | Domain and DNS reconnaissance |
| WhatWeb, Gobuster and Nmap | Web fingerprinting, path enumeration and service discovery |
| FTP client | Understanding service connectivity and rejected authentication |
| pdf2john and John the Ripper | Extracting verification data and offline password recovery |
| ExifTool and Poppler | Opening original PDFs, extracting text and inspecting metadata |
| curl | Preserving the backup response headers and file |
| Python and SQLite | Structured extraction, aggregation, joins and integrity checks |

# 5. Activities Performed and Results

## 5.1 Reconnaissance and Enumeration

```text
whois mediroza.example
nslookup mediroza.example
whatweb mediroza.example
dnsrecon -d mediroza.example
gobuster dir -u https://mediroza.example/ -w ./enumeration.txt
nmap -sV mediroza.example
```

These are command templates using a reserved example domain. The evidence gallery contains redacted original screenshots, with target names and addresses masked. The original results established the context; they were not treated as proof that every exposed service was vulnerable.

Anonymous FTP authentication was rejected. Reply 331 requested the next authentication step; reply 530 indicated rejection. No successful FTP login is claimed. DNS results and varying HTTP responses are contextual observations whose causes were not extrapolated.

## 5.2 M1 — Initial Access to Reports

The trainee confirms entering a SQL injection value in the patient portal Username field and obtaining the report links. An input screenshot and a subsequent report-page screenshot are available. The exact form route, complete request parameters and successful HTTP response are not archived.

```text
Confirmed Username input: admin' -- -
```

In a vulnerable query assembled by string concatenation, an apostrophe may terminate a string and a SQL comment may suppress a following condition. This explains the reported bypass mechanism; it is not recovered server source code. Administrative server control, database writes and operating-system compromise were not demonstrated.

## 5.3 M2 — PDF Password Recovery

The three documents use the PDF Standard security handler, revision 3, with RC4 and a 128-bit key. Passwords were recovered by wordlist testing, then each original was opened and its text extracted. This demonstrates predictable passwords, not direct key recovery independently of the password.

```text
pdf2john patient_report_1.pdf patient_report_2.pdf patient_report_3.pdf > pdfs_hash.hash
john --format=PDF --wordlist=WORDLIST.txt --pot=results.pot pdfs_hash.hash
john --show --format=PDF --pot=results.pot pdfs_hash.hash
```

Recovered values and verification hashes are withheld in this edition. The original command screenshot retains the three-result count while masking both password lists. Public command files explain the syntax; confidential inputs and wordlists are not bundled in the repository.

## 5.4 Metadata and the Backup Clue

```text
exiftool -password 'PDF_PASSWORD' patient_report_3.pdf
```

The useful metadata was encrypted with the PDF. Without a password, ExifTool reported a protected document. Opening the original revealed an operational comment pointing to a legacy backup directory. Re-exported copies retained the visible content but lost those metadata fields, so the original PDFs remained the evidence source.

## 5.5 M3 — SQL Retrieval and Data Analysis

```text
curl -q -sS -D backup_headers.txt -o backup.sql \
  'https://mediroza.example/legacy/backup.sql'

file backup.sql
head -n 20 backup.sql
```

The URL above is a redacted template, not the original target address. The trainee preserved an HTTP 200 response and a SQL verification copy matching the original download. The original request headers were not archived.

The backup contains staff and shareholders tables. CREATE TABLE defines columns; INSERT INTO specifies the value order. Only the two INSERT blocks were imported into local SQLite. MySQL SET, DROP and LOCK instructions were not executed, and no connection to the server database was required.

```text
SELECT full_name, job_title, department, monthly_salary_zar
FROM staff ORDER BY id;

SELECT shareholder_name, share_percent, shares_held, share_class
FROM shareholders ORDER BY id;
```

monthly_salary_zar means a monthly amount in South African rand. share_percent and shares_held mean the ownership percentage and number of shares. COUNT, SUM and JOIN support validation of row counts, totals and name matches.

| Audit result | Public presentation |
| --- | --- |
| 30 employees and 10 shareholders | Counts without individual identities |
| Salaries and ownership records | Real values retained in the confidential report |
| Consistency checks | Row counts, totals and name matches checked |
| Repository SQL dataset | 30 entirely fictional employees and 10 fictional shareholders |

A rejected directory listing does not establish that individual files are protected. Enumeration returned 403 for the legacy directory while the direct file request returned 200. The finding is web exposure of an internal backup; its contents demonstrate the impact.

## 5.6 Data Consistency and Limitations

The SQL header declares 27 August 2019, but three employment dates are later. This prevents assigning a reliable validity period to the salary amounts. HTTP Last-Modified dates the served file, not the salaries. The report describes the supplied records without claiming current salaries or the current hospital workforce.

# 6. Security Findings and Risk Analysis

| ID | Finding | Evidence / observation | Impact | Risk |
| --- | --- | --- | --- | --- |
| F-01 | Reported portal SQLi | Confirmed input and screenshots; raw request unavailable | Reported access to medical documents | High, provisional |
| F-02 | Predictable PDF passwords | Three originals opened after offline recovery | Disclosure of confidential reports | High |
| F-03 | Operational PDF metadata | Comment recovered from an original document | Discovery of a backup location | Low |
| F-04 | Exposed SQL backup | HTTP 200 and identical file; session-free request reported by trainee | Personal and financial data disclosure | High |

Ratings are qualitative and based on demonstrated confidentiality impact and documented access conditions. No CVSS score or additional privilege is invented. Lack of file access control is distinct from expected public headers, addresses or reachable ports.

## 6.1 Positive Controls and Cautious Interpretation

HTTPS redirection and rejection of anonymous FTP authentication were observed. They do not compensate for an exposed backup or predictable PDF passwords. A directory 403 response, missing DNSSEC answer or technology fingerprint is not automatically an exploitable vulnerability.

# 7. Recommendations

| Priority | Action | Retest criterion |
| --- | --- | --- |
| 1 | Remove backups from web-served directories and restrict storage access | The direct backup URL no longer returns SQL without authorization |
| 1 | Parameterize authentication queries and authorize each report download | The injection input is rejected and other accounts’ documents are inaccessible |
| 2 | Replace predictable document secrets with long, random, unique passwords | Recovered passwords no longer open reissued documents |
| 2 | Remove operational comments and internal paths from distributed metadata | New originals do not reveal the backup clue |
| 2 | Review access logs and search for other deployed backup copies | Exposure scope and similar files are documented |
| 3 | Validate backup provenance and data validity periods | Dates, versions and ownership are documented |

# 8. Conclusion and Personal Reflection

The exercise connects reconnaissance to impact analysis: recovered documents can reveal a metadata clue, and an accessible backup can disclose structured records without direct database access. M2 and M3 results were checked. A complete HTTP capture would strengthen the M1 evidence if one becomes available.

## 8.1 Skills Practiced

I worked on the distinction between reaching a service and successfully authenticating. An FTP 331 response does not establish that an account is valid or that a session is authenticated.

I developed my understanding of PDF password recovery: extracting verification data, selecting a wordlist and checking that the recovered password opens the original document are separate steps.

I learned to inspect original PDF metadata using the document password. A re-exported copy may preserve the visible report while losing operational comments that matter to the investigation.

I studied SQL backups by matching column names to row values, then using SELECT, COUNT, SUM and JOIN to produce readable tables and validate the results.

This project helped me distinguish reconnaissance observations from demonstrated vulnerabilities, retain supporting evidence and prepare a public portfolio version that protects confidential records.

The report follows the supplied sample: liability disclaimer, introduction, scope, tools, activities, risk analysis, recommendations, conclusion and evidence. The executive summary and full confidential data annexes also satisfy the Week 4 project brief.

# 9. Evidence Collected

The gallery pairs command syntax with screenshot evidence. Public images are edited derivatives of the original trainee screenshots, not reconstructed successful executions. Target addresses, recovered secrets and patient details are masked where applicable. Crops and redactions are documented in the evidence manifest.

## 9.1 WHOIS

![Domain registration reconnaissance — redacted original VM screenshot; see evidence manifest.](<evidence/screenshots/whois_redacted.png>)

Domain registration reconnaissance — redacted original VM screenshot; see evidence manifest.

## 9.2 WhatWeb

![Web fingerprinting and HTTP responses — redacted original VM screenshot; see evidence manifest.](<evidence/screenshots/whatweb_redacted.png>)

Web fingerprinting and HTTP responses — redacted original VM screenshot; see evidence manifest.

## 9.3 nslookup

![Domain resolution — redacted original VM screenshot; see evidence manifest.](<evidence/screenshots/nslookup_redacted.png>)

Domain resolution — redacted original VM screenshot; see evidence manifest.

## 9.4 DNSRecon

![DNS enumeration launch — redacted original VM screenshot; see evidence manifest.](<evidence/screenshots/dnsrecon_redacted.png>)

DNS enumeration launch — redacted original VM screenshot; see evidence manifest.

## 9.5 Gobuster

![Path enumeration and directory status codes — redacted original VM screenshot; see evidence manifest.](<evidence/screenshots/gobuster_redacted.png>)

Path enumeration and directory status codes — redacted original VM screenshot; see evidence manifest.

## 9.6 PDF Verification Data Extraction

![Actual pdf2john command — redacted original VM screenshot; see evidence manifest.](<evidence/screenshots/pdf_hash_extraction_redacted.png>)

Actual pdf2john command — redacted original VM screenshot; see evidence manifest.

## 9.7 PDF Password Recovery

![Actual John commands and three-result count — redacted original VM screenshot; see evidence manifest.](<evidence/screenshots/pdf_password_recovery_redacted.png>)

Actual John commands and three-result count — redacted original VM screenshot; see evidence manifest.

## 9.8 Portal Input

![Input capture; not proof of the successful HTTP response — redacted original VM screenshot; see evidence manifest.](<evidence/screenshots/portal_input_redacted.png>)

Input capture; not proof of the successful HTTP response — redacted original VM screenshot; see evidence manifest.

## 9.9 Report Download Page

![Three report download controls — redacted original VM screenshot; see evidence manifest.](<evidence/screenshots/reports_page_redacted.png>)

Three report download controls — redacted original VM screenshot; see evidence manifest.

## 9.10  Author and Project Information

| Field | Detail |
| --- | --- |
| Author | Mardochée BONOU |
| Program | Networkwalks Cybersecurity Internship — Week 4 — Batch B084 |
| GitHub profile | https://github.com/Mardoch45 |
| Project | Mediroza — evidence analysis and penetration testing report |
| Repository | https://github.com/Mardoch45/INTERSHIP-FINAL-REPORT |
