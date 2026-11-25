from __future__ import annotations

import argparse
import hashlib
import json
import zipfile
from pathlib import Path
from xml.etree import ElementTree as ET

from PIL import Image


ROOT = Path(__file__).resolve().parents[1]
OUTPUT = ROOT / 'docs'
STEM = 'Mediroza_Penetration_Testing_Report_Professional'
NAVY = '182D3D'
TEAL = '087F86'
INK = '293C48'
MUTED = '526874'
LIGHT = 'EFF4F5'
AMBER = '96501E'
NS = {
    'w': 'http://schemas.openxmlformats.org/wordprocessingml/2006/main',
    'r': 'http://schemas.openxmlformats.org/officeDocument/2006/relationships',
    'wp': 'http://schemas.openxmlformats.org/drawingml/2006/wordprocessingDrawing',
    'a': 'http://schemas.openxmlformats.org/drawingml/2006/main',
    'pic': 'http://schemas.openxmlformats.org/drawingml/2006/picture',
}
for prefix, uri in NS.items():
    ET.register_namespace(prefix, uri)


def element(parent, tag, attrs=None, text=None):
    result = ET.SubElement(parent, qualified(tag))
    for name, value in (attrs or {}).items():
        result.set(qualified(name) if ':' in name else name, str(value))
    if text is not None:
        result.text = text
    return result


def qualified(name):
    if ':' not in name:
        return name
    prefix, local = name.split(':', 1)
    return '{' + NS[prefix] + '}' + local


def xml_bytes(node):
    return ET.tostring(node, encoding='utf-8', xml_declaration=True)


class Report:
    def __init__(self):
        self.document = ET.Element(qualified('w:document'))
        self.body = element(self.document, 'w:body')
        self.images = []
        self.bookmark_id = 0
        self.evidence = []

    def run(self, paragraph, text, bold=False, color=None, size=None, font=None):
        run = element(paragraph, 'w:r')
        props = element(run, 'w:rPr')
        if bold:
            element(props, 'w:b')
        if color:
            element(props, 'w:color', {'w:val': color})
        if size:
            element(props, 'w:sz', {'w:val': round(size * 2)})
        if font:
            element(props, 'w:rFonts', {'w:ascii': font, 'w:hAnsi': font})
        for index, line in enumerate(text.split('\n')):
            if index:
                element(run, 'w:br')
            node = element(run, 'w:t', text=line)
            node.set('{http://www.w3.org/XML/1998/namespace}space', 'preserve')
        return run

    def bookmark(self, paragraph, name):
        self.bookmark_id += 1
        element(paragraph, 'w:bookmarkStart', {'w:id': self.bookmark_id, 'w:name': name})
        element(paragraph, 'w:bookmarkEnd', {'w:id': self.bookmark_id})

    def paragraph(self, text='', style='Normal', parent=None, bookmark=None, **kwargs):
        paragraph = element(parent if parent is not None else self.body, 'w:p')
        props = element(paragraph, 'w:pPr')
        element(props, 'w:pStyle', {'w:val': style})
        if bookmark:
            self.bookmark(paragraph, bookmark)
        if text:
            self.run(paragraph, text, **kwargs)
        return paragraph

    def heading(self, text, level=1, bookmark=None):
        return self.paragraph(text, f'Heading{level}', bookmark=bookmark)

    def page(self, title, bookmark, continuation=False):
        paragraph = self.heading(title, 2 if continuation else 1, bookmark)
        element(paragraph.find(qualified('w:pPr')), 'w:pageBreakBefore')

    def link(self, paragraph, text, anchor):
        link = element(paragraph, 'w:hyperlink', {'w:anchor': anchor, 'w:history': '1'})
        self.run(link, text, color=TEAL)

    def reference(self, label, links):
        paragraph = self.paragraph(style='Caption')
        self.run(paragraph, label + ' ')
        for index, (text, anchor) in enumerate(links):
            if index:
                self.run(paragraph, '  ·  ')
            self.link(paragraph, text, anchor)

    def label(self, label, text):
        self.paragraph(label, 'Label')
        self.paragraph(text)

    def callout(self, title, text):
        paragraph = self.paragraph(style='Callout')
        self.run(paragraph, title + '  ', bold=True, color=NAVY)
        self.run(paragraph, text)

    def code(self, text):
        lines = text.splitlines()
        for index, line in enumerate(lines):
            paragraph = self.paragraph(line, 'Code')
            if index < len(lines) - 1:
                element(paragraph.find(qualified('w:pPr')), 'w:keepNext')

    def table(self, heads, rows, widths, small=False):
        table = element(self.body, 'w:tbl')
        props = element(table, 'w:tblPr')
        element(props, 'w:tblW', {'w:w': sum(widths), 'w:type': 'dxa'})
        element(props, 'w:tblLayout', {'w:type': 'fixed'})
        margins = element(props, 'w:tblCellMar')
        for side in ['top', 'left', 'bottom', 'right']:
            element(margins, f'w:{side}', {'w:w': '90', 'w:type': 'dxa'})
        borders = element(props, 'w:tblBorders')
        for side in ['top', 'left', 'bottom', 'right', 'insideH', 'insideV']:
            element(borders, f'w:{side}', {'w:val': 'nil'})
        grid = element(table, 'w:tblGrid')
        for width in widths:
            element(grid, 'w:gridCol', {'w:w': width})
        for row_index, values in enumerate([heads] + rows):
            row = element(table, 'w:tr')
            row_props = element(row, 'w:trPr')
            element(row_props, 'w:cantSplit')
            if row_index == 0:
                element(row_props, 'w:tblHeader')
            for column, value in enumerate(values):
                cell = element(row, 'w:tc')
                cell_props = element(cell, 'w:tcPr')
                element(cell_props, 'w:tcW', {'w:w': widths[column], 'w:type': 'dxa'})
                element(cell_props, 'w:vAlign', {'w:val': 'center'})
                fill = NAVY if row_index == 0 else LIGHT if row_index % 2 else 'FFFFFF'
                element(cell_props, 'w:shd', {'w:fill': fill, 'w:val': 'clear'})
                self.paragraph(str(value), 'TableText', parent=cell,
                               bold=row_index == 0, color='FFFFFF' if row_index == 0 else INK,
                               size=9 if small else 9.5)
        self.paragraph('', 'AfterTable')
        return table

    def figure(self, identifier, key, title, caption, related, width=6.5, max_height=3.8,
               crop_right_pixels=0):
        source = ROOT / 'evidence' / 'screenshots' / f'{key}_redacted.png'
        image = Image.open(source)
        visible_width = image.width - crop_right_pixels
        height = width * image.height / visible_width
        if height > max_height:
            width *= max_height / height
            height = max_height
        self.paragraph(f'{identifier}  |  {title}', 'EvidenceTitle', bookmark=identifier.replace('-', ''))
        paragraph = self.paragraph(style='Image')
        drawing = element(element(paragraph, 'w:r'), 'w:drawing')
        inline = element(drawing, 'wp:inline', {'distT': 0, 'distB': 0, 'distL': 0, 'distR': 0})
        extent = {'cx': round(width * 914400), 'cy': round(height * 914400)}
        element(inline, 'wp:extent', extent)
        image_index = len(self.images) + 1
        element(inline, 'wp:docPr', {'id': image_index, 'name': identifier + ' ' + title,
                                   'descr': caption + ' Existing redacted derivative; source pixels unchanged.'})
        graphic = element(inline, 'a:graphic')
        data = element(graphic, 'a:graphicData', {'uri': NS['pic']})
        picture = element(data, 'pic:pic')
        nonvisual = element(picture, 'pic:nvPicPr')
        element(nonvisual, 'pic:cNvPr', {'id': image_index, 'name': source.name})
        element(nonvisual, 'pic:cNvPicPr')
        fill = element(picture, 'pic:blipFill')
        element(fill, 'a:blip', {'r:embed': f'rIdImage{image_index}'})
        if crop_right_pixels:
            element(fill, 'a:srcRect', {'r': round(100000 * crop_right_pixels / image.width)})
        element(element(fill, 'a:stretch'), 'a:fillRect')
        shape = element(picture, 'pic:spPr')
        transform = element(shape, 'a:xfrm')
        element(transform, 'a:off', {'x': 0, 'y': 0})
        element(transform, 'a:ext', extent)
        element(element(shape, 'a:prstGeom', {'prst': 'rect'}), 'a:avLst')
        self.images.append(source)
        self.paragraph(caption + ' Public redacted screenshot.', 'Caption')
        anchor = 'Recon' if related == 'Reconnaissance' else related.replace('-', '')
        self.reference('Related:', [(related, anchor)])
        self.evidence.append({'id': identifier, 'title': title, 'file': str(source.relative_to(ROOT)),
                              'related': related, 'kind': 'Existing redacted screenshot',
                              'display_crop_right_pixels': crop_right_pixels})

    def record(self, identifier, title, description, related):
        self.paragraph(f'{identifier}  |  {title}', 'EvidenceTitle', bookmark=identifier.replace('-', ''))
        self.paragraph(description)
        self.reference('Related:', [(related, related.replace('-', ''))])
        self.evidence.append({'id': identifier, 'title': title, 'related': related,
                              'kind': 'Restricted original artifact; public narrative summary only'})

    def finding(self, identifier, title, severity, component, validation, description,
                evidence, impact, recommendation, retest, refs):
        if identifier == 'F-01':
            self.page('04  Security Findings', 'Findings')
            self.paragraph(f'{identifier} — {title}', 'FindingTitle', bookmark=identifier.replace('-', ''))
        else:
            paragraph = self.paragraph(f'{identifier} — {title}', 'FindingTitle', bookmark=identifier.replace('-', ''))
            element(paragraph.find(qualified('w:pPr')), 'w:pageBreakBefore')
        self.paragraph('SECURITY FINDING', 'Kicker')
        profile = self.table(['Finding profile', 'Assessment detail'], [
            ['Finding ID', identifier],
            ['Severity', severity],
            ['Affected Component', component],
            ['Validation Status', validation],
        ], [2750, 6810])
        severity_cell = profile.findall(qualified('w:tr'))[2].findall(qualified('w:tc'))[1]
        for properties in severity_cell.iter(qualified('w:rPr')):
            properties.find(qualified('w:color')).set(qualified('w:val'), TEAL if severity == 'Low' else AMBER)
            element(properties, 'w:b')
        self.label('Description', description)
        self.label('Technical Evidence', evidence)
        self.reference('Evidence:', [(item, item.replace('-', '')) for item in refs])
        self.label('Impact', impact)
        self.label('Recommendation', recommendation)
        self.label('Retest Criteria', retest)
        self.label('Validation Status', validation + '. No remediation retest is documented in the supplied evidence.')

    def build(self):
        self.paragraph('NETWORKWALKS  /  CYBERSECURITY & ETHICAL HACKING', 'Kicker')
        self.paragraph('PUBLIC EDITION   •   25 NOVEMBER 2026   •   VERSION 2.0', 'CoverMeta')
        self.paragraph('MEDIROZA', 'CoverTitle')
        self.paragraph('Penetration\nTesting Report', 'CoverSubtitle')
        self.paragraph('Application access. Document security. Backup exposure.', 'CoverDeck')
        self.callout('OVERALL RISK: HIGH', 'Four findings · three verified · one partially documented')
        self.table(['ENGAGEMENT', 'REPORT DETAILS'], [
            ['Assessor', 'Mardochée BONOU'],
            ['Organization / Program', 'Networkwalks — Cybersecurity & Ethical Hacking'],
            ['Project / Batch', 'Final Internship Project — Week 4 / B084'],
            ['Assessment period', '22–25 November 2026'],
            ['Target', 'Demonstration hospital — target details redacted'],
            ['Classification', 'Public — redacted technical report'],
        ], [2850, 6710])
        self.paragraph('Authorized educational assessment', 'CoverNote')
        self.paragraph('Prepared for technical review. Patient data, recovered passwords, original verification '
                       'hashes and internal operational details are withheld.', 'CoverSmall')

        self.page('Contents', 'Contents')
        self.body[-1].find(qualified('w:pPr')).find(qualified('w:pStyle')).set(qualified('w:val'), 'ContentsTitle')
        self.paragraph('Document navigation', 'Kicker')
        paragraph = self.paragraph()
        field = element(paragraph, 'w:fldSimple', {'w:instr': ' TOC \\o "1-1" \\h \\z '})
        self.run(field, 'Contents will be updated during export.')
        self.heading('Reading this edition', 3)
        self.paragraph('The assessment results explain the sequence of observations. The finding sheets describe '
                       'the security implications and acceptance criteria. Evidence is placed beside the relevant '
                       'technical result; Appendix A provides a linked register rather than duplicate images.')
        self.paragraph('“Verified” refers to the supplied artifacts and documented local checks. '
                       'It does not mean the target was tested again while preparing this edition. '
                       'The placeholder mediroza.example is illustrative and is not the assessed host.')
        self.heading('Finding navigation', 3)
        for identifier, title in [('F-01', 'SQL Injection in Patient Portal'),
                                  ('F-02', 'Weak PDF Password Protection'),
                                  ('F-03', 'Information Disclosure Through PDF Metadata'),
                                  ('F-04', 'Exposed SQL Database Backup')]:
            self.reference('', [(identifier + ' — ' + title, identifier.replace('-', ''))])

        self.page('01  Executive Summary', 'Summary')
        self.paragraph('Confidentiality exposure across application, document and backup controls', 'Deck')
        self.paragraph('The Mediroza assessment examined a demonstration hospital environment during '
                       '22–25 November 2026 under the Networkwalks internship program. Work covered '
                       'reconnaissance, the patient portal, protected PDF reports and an exposed SQL backup.')
        self.paragraph('The strongest verified results concern offline access to three original PDF reports '
                       'after password recovery, an operational clue in original PDF metadata, and local '
                       'analysis of a retrieved backup containing two tables. The reported SQL injection '
                       'is supported by screenshots but lacks a complete archived HTTP transaction.')
        self.table(['ID', 'Security Finding', 'Severity', 'Validation'], [
            ['F-01', 'SQL Injection — Patient Portal', 'High\n(provisional)', 'Partially documented'],
            ['F-02', 'Weak PDF Password Protection', 'High', 'Verified'],
            ['F-03', 'Information Disclosure Through PDF Metadata', 'Low', 'Verified'],
            ['F-04', 'Exposed SQL Database Backup', 'High', 'Verified'],
        ], [700, 4310, 1650, 2900])
        self.heading('Business impact', 2)
        self.paragraph('Patient documentation and employee / shareholder information were exposed to '
                       'confidentiality risks. The backup analysis identified 30 employee records and '
                       '10 shareholder records. Those counts describe the supplied file, not a verified '
                       'current workforce or ownership register.')
        self.heading('Decisions and immediate priorities', 2)
        self.paragraph('Remove web-accessible backup copies first. Address unsafe query construction '
                       'and enforce authorization on every document request, while obtaining the missing '
                       'F-01 transaction evidence during an authorized retest. Reissue documents with '
                       'strong, unique secrets and sanitize metadata during generation.')
        self.callout('Assessment boundary', 'Overall risk is qualitative and rated HIGH. No database '
                     'modification, administrative server control or service disruption was demonstrated. '
                     'No CVSS scores are assigned.')

        self.page('02  Engagement Overview', 'Engagement')
        self.heading('2.1  Authorization and Disclaimer', 2)
        self.paragraph('This was an authorized educational exercise under the Networkwalks internship '
                       'program. Authorization is described in the supplied project brief; testing was '
                       'limited to the environment covered by that authorization. Social engineering, '
                       'denial of service, out-of-scope testing and unauthorized production-data '
                       'modification were excluded.')
        self.paragraph('This public edition withholds patient records, employee identities, individual '
                       'salaries, shareholder details, recovered passwords, original verification hashes '
                       'and internal operational information. Existing public screenshot redactions are '
                       'retained. The repository’s demonstration dataset is not evidence of target findings.')
        self.heading('2.2  Scope', 2)
        self.table(['Component', 'Assessment objective'], [
            ['Web application / patient portal', 'Examine authentication and access to patient reports.'],
            ['Three original patient PDFs', 'Assess offline password resistance and original metadata.'],
            ['Web-accessible storage', 'Distinguish directory restrictions from direct-file access.'],
            ['Retrieved SQL backup', 'Examine the two relevant tables and confidentiality impact locally.'],
        ], [3200, 6360])
        self.heading('2.3  Methodology and evidence boundaries', 2)
        self.paragraph('Reconnaissance and enumeration informed the portal examination. Retrieved PDFs '
                       'were examined through offline password recovery and metadata review. The backup '
                       'was then examined through response artifacts, file comparison and local SQL '
                       'analysis. Reporting separates direct artifact verification, trainee-reported '
                       'network observations and inference.')
        self.paragraph('The sequence is not evidence of a reproducible end-to-end compromise. In '
                       'particular, the F-01 request / response and backend query were not archived. '
                       'No additional live target requests were made to prepare this report.')
        self.heading('2.4  Tools and Technologies', 2)
        self.table(['Purpose', 'Tools'], [
            ['Environment / reconnaissance', 'Kali Linux; WHOIS; nslookup; DNSRecon; WhatWeb'],
            ['Enumeration / services', 'Gobuster; Nmap; FTP client'],
            ['Document examination', 'pdf2john; John the Ripper; ExifTool; Poppler'],
            ['Retrieval / local analysis', 'curl; Python; SQLite'],
        ], [3200, 6360], small=True)

        self.page('03  Assessment Results', 'Results')
        self.heading('3.1  Reconnaissance and Enumeration', 2, 'Recon')
        self.paragraph('Domain registration, DNS resolution and web fingerprinting established context '
                       'for the application examination. These observations support scoping; they are '
                       'not separate vulnerabilities. The following derivatives preserve their existing redactions.')
        self.figure('E-01', 'whois', 'Domain registration reconnaissance',
                    'WHOIS command and initial registration output. Target name and registry identifier are masked.',
                    'Reconnaissance', max_height=1.8)
        self.figure('E-02', 'whatweb', 'Web technology identification',
                    'Visible HTTP 301 and 403 observations and web fingerprint output. This is not an access-control test.',
                    'Reconnaissance', max_height=1.3)
        self.figure('E-03', 'nslookup', 'DNS resolution',
                    'Domain-resolution output with the assessed name and returned address masked.',
                    'Reconnaissance', width=4.6, max_height=1.55)
        self.figure('E-04', 'dnsrecon', 'DNS enumeration launch',
                    'Launch and initial status only; no full DNS inventory. Empty right-hand background '
                    'is cropped for display; source bytes are unchanged.',
                    'Reconnaissance', max_height=0.9, crop_right_pixels=419)

        self.page('3.1  Enumeration — interpreting access controls', 'Enumeration', continuation=True)
        self.paragraph('Gobuster returned HTTP 403 for a legacy directory. That result demonstrates '
                       'restricted directory access, not protection of every file beneath that path. '
                       'The supplied backup response later records HTTP 200 for a direct-file request (F-04).')
        self.figure('E-05', 'gobuster', 'Web path enumeration',
                    'Enumeration output includes directory-level 403 responses. It does not show the later backup download.',
                    'F-04', width=4.0, max_height=5.6)
        self.heading('Service observations', 3)
        self.paragraph('The documented FTP interaction returned 331 to request the next authentication '
                       'step and 530 to reject authentication. No successful FTP login was obtained. '
                       'Nmap and FTP form part of the documented toolset, but no additional public '
                       'screenshot for these steps is supplied. No FTP finding is asserted.')
        self.callout('Interpretation', 'HTTPS redirection, directory restrictions and rejected anonymous '
                     'FTP authentication are positive observations. They do not compensate for direct '
                     'backup-file exposure or weak document protection.')

        self.page('3.2  Initial Access — Patient Portal', 'Portal', continuation=True)
        self.paragraph('The trainee reports that the Username input admin\' -- - led to a report-download '
                       'page. E-06 records the input; E-07 records a page with three download controls. '
                       'These are separate screenshots and do not preserve the intervening HTTP exchange.')
        self.figure('E-06', 'portal_input', 'Patient portal input',
                    'The input field is visible alongside “Username not found”. This frame alone shows '
                    'neither a successful login nor a successful injection.',
                    'F-01', width=3.4, max_height=4.3)
        self.figure('E-07', 'reports_page', 'Patient report download controls',
                    'Three download controls are visible. Patient identifiers, report references and '
                    'dates remain masked. The image does not establish how the page was reached.',
                    'F-01', width=6.5, max_height=2.46)
        self.callout('Validation limit', 'No complete HTTP request, server response or backend SQL '
                     'query is archived. F-01 remains partially documented and High (provisional).')

        self.page('3.3  PDF Password Recovery', 'PDFRecovery', continuation=True)
        self.paragraph('Verification data was extracted from the three encrypted patient reports and '
                       'tested offline using John the Ripper and a wordlist. The documents use PDF '
                       'Standard Security Handler revision 3, RC4 and a 128-bit key. The successful '
                       'method was password guessing; no independent cryptographic key recovery is claimed.')
        self.figure('E-08', 'pdf_hash_extraction', 'PDF verification-data extraction',
                    'The pdf2john command includes all three original report filenames. No verification '
                    'hash is printed in this derivative.', 'F-02', max_height=0.9)
        self.figure('E-09', 'pdf_password_recovery', 'Offline password recovery results',
                    'The retained John output reports three recovered hashes and zero remaining. '
                    'Recovered password values remain redacted.', 'F-02', max_height=2.85)
        self.record('E-10', 'Original-document opening checks',
                    'The retained local validation record documents successful opening of each of '
                    'the three original PDFs. Extracted text was checked; original-file integrity was '
                    'preserved. The record, passwords and report content are restricted and are not '
                    'embedded in this edition.', 'F-02')
        self.callout('Result', 'All three originals were opened after password recovery. Re-exported '
                     'reading copies do not replace the originals for metadata examination.')

        self.page('3.4  PDF Metadata Examination', 'Metadata', continuation=True)
        self.paragraph('Metadata examination of an original protected PDF recovered an operational '
                       'comment identifying a legacy backup location. A re-exported copy did not retain '
                       'that metadata in the same form. The original remains the evidence source; '
                       'the internal comment and author information are withheld.')
        self.record('E-11', 'Operational metadata in an original PDF',
                    'The original third PDF and its retained metadata extraction support the existence '
                    'of the operational backup-location clue. No public screenshot of that examination '
                    'is available. This entry is a narrative evidence reference, not a reconstructed capture.', 'F-03')
        self.heading('3.5  SQL Backup Retrieval and Analysis', 2, 'Backup')
        self.paragraph('The trainee supplied a direct-download response and a second SQL verification '
                       'copy. The retained headers record HTTP 200. The two supplied files match '
                       'byte for byte. A session-free retrieval is reported by the trainee; the '
                       'complete originating request is not archived, so the headers alone cannot '
                       'establish the absence of cookies or other authentication.')
        self.record('E-12', 'Backup response and matching SQL copies',
                    'The retained response headers show HTTP 200 and an SQL content type. The supplied '
                    'download and verification file are identical. Original target details, internal '
                    'paths and file verification hashes are withheld.', 'F-04')
        self.record('E-13', 'Local extraction and consistency checks',
                    'The two relevant tables were analyzed locally using SQLite: staff (30 records) '
                    'and shareholders (10 records). Only relevant INSERT data was imported; original '
                    'MySQL administrative instructions were not executed. Detailed records remain restricted.', 'F-04')
        self.table(['Dataset', 'Records', 'Information categories'], [
            ['staff', '30', 'Employee identity, role, department and monthly salary'],
            ['shareholders', '10', 'Identity, ownership percentage, share count and class'],
        ], [1900, 1000, 6660])
        self.callout('Data currency limit', 'The SQL header states 27 August 2019, yet three employment '
                     'dates are later. Neither that header nor HTTP Last-Modified establishes the '
                     'currency of salaries or organizational records.')

        self.finding('F-01', 'SQL Injection in Patient Portal', 'High (provisional)',
                     'Patient portal authentication interface', 'Partially documented',
                     'A SQL injection input in the Username field was reported to allow access to '
                     'patient-report links. Unsafe string concatenation could allow supplied input '
                     'to alter SQL interpretation, but the application query itself was not captured.',
                     'The documented input is admin\' -- -. E-06 displays that value together with '
                     '“Username not found”; E-07 separately shows three report download controls. '
                     'The trainee reports a successful transition between the two states. The '
                     'screenshots do not independently establish that causal sequence.',
                     'If confirmed, authentication bypass could expose patient documents to an '
                     'unauthorized person. No database write access, data modification or server '
                     'control was demonstrated.',
                     'Use parameterized queries throughout authentication and data access. Apply '
                     'server-side validation as an additional control. Enforce document-level '
                     'authorization on every download; access to one account must not expose '
                     'another patient’s reports.',
                     'During an authorized retest, archive a sanitized request / response pair '
                     'for the original input and appropriate negative controls. Confirm the input '
                     'does not bypass authentication. Test permitted and cross-account document '
                     'requests to confirm server-side authorization. Capture outcomes without '
                     'including patient data or session secrets in the public report.',
                     ['E-06', 'E-07'])

        self.finding('F-02', 'Weak PDF Password Protection', 'High',
                     'Three original patient PDF reports', 'Verified',
                     'All three document passwords were recovered through offline wordlist testing, '
                     'and the original encrypted PDFs were opened using the recovered values. '
                     'This demonstrates weak password selection in the assessed documents, '
                     'rather than an independent break of the encryption key.',
                     'E-08 records extraction for the three PDFs. E-09 shows three recovered '
                     'results and zero remaining. E-10 records successful opening of all three '
                     'originals and text checks. The original protection is revision 3, RC4, '
                     '128-bit. Passwords and verification hashes are withheld.',
                     'A person who obtains encrypted document copies can test guesses offline '
                     'without relying on portal rate limits. Successful recovery exposes the '
                     'medical content. Portal authorization and document password strength '
                     'therefore address different parts of the confidentiality risk.',
                     'Use long, randomly generated, unique document passwords where password '
                     'protection is required. Deliver secrets through an appropriate separate '
                     'channel. Place documents behind authenticated and authorized storage. '
                     'Review distribution practices and migrate to modern, compatible encryption '
                     'rather than retaining legacy RC4 protection.',
                     'Reissue the assessed documents and confirm that previous passwords no '
                     'longer open them. Under an agreed offline test budget, repeat the previously '
                     'successful approach and record the outcome. Verify the selected protection '
                     'settings and authorized access to storage. A failed bounded wordlist test '
                     'alone does not prove passwords cannot be recovered.',
                     ['E-08', 'E-09', 'E-10'])

        self.finding('F-03', 'Information Disclosure Through PDF Metadata', 'Low',
                     'Metadata of an original patient PDF', 'Verified',
                     'An operational comment in an original protected PDF disclosed information '
                     'about a legacy backup location. Such generation-time metadata was unnecessary '
                     'for the report recipient and provided an infrastructure clue.',
                     'E-11 refers to the original third PDF and its retained metadata extraction. '
                     'The comment was not retained in the same form in the re-exported reading '
                     'copy. No public screenshot is available; the internal comment and metadata '
                     'author value are withheld rather than recreated.',
                     'The disclosed information could guide further investigation of internal '
                     'storage. The metadata clue did not itself grant database access. The '
                     'separate backup exposure is assessed in F-04, so its full confidentiality '
                     'impact is not attributed twice.',
                     'Remove operational comments, internal paths and unnecessary author details '
                     'from the document-generation workflow. Apply an explicit metadata allowlist '
                     'before distribution. Keep infrastructure notes in access-controlled '
                     'operational records rather than patient-facing files.',
                     'Generate new documents through the normal production workflow. Examine '
                     'metadata on the actual files distributed to recipients and verify that '
                     'operational comments and internal locations are absent. Check that the '
                     'sanitization step preserves intended clinical content and access controls. '
                     'Do not substitute a later re-export for the delivered file.',
                     ['E-11'])

        self.finding('F-04', 'Exposed SQL Database Backup', 'High',
                     'Legacy web-accessible backup storage', 'Verified',
                     'A legacy SQL backup was retrieved by direct HTTP request and supplied for '
                     'offline analysis. Directory-level HTTP 403 responses did not prevent a '
                     'direct-file response containing the backup. The retrieved data concerns '
                     'employee and shareholder information.',
                     'E-12 contains the retained HTTP 200 response and matching download / '
                     'verification copies. E-13 supports local analysis of staff (30 records) '
                     'and shareholders (10 records). Session-free retrieval is trainee-reported; '
                     'a complete originating request is not retained. Local extraction was '
                     'verified; no live database connection is claimed.',
                     'Backup disclosure exposes personal, employment, compensation and ownership '
                     'information outside its intended access boundary. Record counts describe '
                     'the supplied backup. Its 27 August 2019 header conflicts with three later '
                     'employment dates, preventing claims about current salaries or workforce.',
                     'Remove backups from the web document root and deny public access at the '
                     'storage and infrastructure layers. Require authentication and authorization '
                     'for legitimate retrieval. Identify other deployed copies, review access '
                     'logs for downloads and establish controlled backup retention and distribution.',
                     'Preserve a sanitized unauthenticated request / response showing that the '
                     'former direct-file location no longer returns SQL contents. Check alternate '
                     'copies and storage locations. Confirm that legitimate backup workflows still '
                     'operate through authorized channels. Verify response content as well as '
                     'status; disabling directory listing alone is insufficient.',
                     ['E-05', 'E-12', 'E-13'])

        self.page('05  Risk Assessment', 'Risk')
        self.paragraph('Qualitative severity, with evidence confidence shown separately', 'Deck')
        self.paragraph('Ratings follow the README and reflect confidentiality impact and documented '
                       'access conditions. There are three High findings, including one provisional '
                       'rating, and one Low finding. No Critical finding or numeric CVSS score is assigned.')
        self.table(['Finding', 'Severity', 'Risk rationale / evidence boundary'], [
            ['F-01', 'High\n(provisional)', 'Potential patient-document access through reported SQL injection. '
             'Screenshots support the report, but a complete HTTP transaction is missing.'],
            ['F-02', 'High', 'All three original PDFs opened after offline password recovery. '
             'Encrypted copies did not provide effective confidentiality against the successful guesses.'],
            ['F-03', 'Low', 'Verified operational metadata clue. Aids discovery; does not itself '
             'grant backup access.'],
            ['F-04', 'High', 'Retrieved backup and verified local extraction expose two internal '
             'datasets. Session-free request conditions remain trainee-reported.'],
        ], [1000, 1750, 6810])
        self.heading('Evidence confidence and overall risk', 2)
        self.paragraph('Severity and validation status answer different questions. F-01 remains '
                       'provisional because its exploitation path cannot be independently reproduced '
                       'from the archived material. F-02, F-03 and F-04 have verified artifact results. '
                       'The overall rating remains HIGH because verified document and backup exposure '
                       'already demonstrate material confidentiality weaknesses.')
        self.heading('Positive observations', 2)
        self.paragraph('HTTPS redirection was observed; anonymous FTP authentication was rejected; '
                       'the legacy directory restricted access. These controls are useful but do not '
                       'resolve the specific findings. Public DNS records, fingerprints and reachable '
                       'ports are not counted as vulnerabilities without evidence of a weakness.')
        self.heading('Limits of impact', 2)
        self.paragraph('No database modification, administrative server control or service interruption '
                       'was demonstrated. The assessment does not establish the current validity of '
                       'the backup records, access by third parties or compromise beyond the supplied evidence.')

        self.page('06  Remediation Plan', 'Remediation')
        self.paragraph('Recommended sequencing — implementation and retesting remain pending', 'Deck')
        self.paragraph('The priority labels below match the README. “Critical remediation priority” '
                       'describes urgency; it does not change a finding’s High severity to Critical. '
                       'Owner roles are proposed for coordination and are not confirmed assignments.')
        self.table(['Priority / Finding', 'Recommended action', 'Suggested owner / closure evidence'], [
            ['Critical priority\nF-04', 'Remove public backup copies; move retained backups outside '
             'web-served storage and restrict access.', 'Operations / infrastructure\nSanitized direct-file '
             'request no longer returns SQL.'],
            ['Critical priority\nF-01', 'Correct query construction and enforce authorization on '
             'each document request; capture the missing validation evidence.', 'Application team\n'
             'Authentication and cross-account authorization retest.'],
            ['High priority\nF-02', 'Reissue PDFs with strong unique secrets; review document '
             'storage and delivery.', 'Application / document owner\nOld secrets rejected; bounded '
             'offline test and access checks recorded.'],
            ['High priority\nF-03', 'Sanitize operational metadata in the actual generation workflow.',
             'Document owner\nDelivered originals contain no internal operational clues.'],
            ['High priority\nF-04', 'Review access logs and search for other exposed backups.',
             'Operations / security\nExposure review and duplicate-file inventory documented.'],
            ['Medium priority\nF-02 / F-03 / F-04', 'Formalize secure document generation, storage '
             'and backup retention.', 'Service owners\nControls documented and verified on new outputs.'],
        ], [1900, 4210, 3450], small=True)
        self.heading('07  Conclusion', 1, 'Conclusion')
        self.paragraph('The assessment identifies confidentiality weaknesses across document protection '
                       'and backup management, together with a partially documented patient-portal '
                       'SQL injection report. Remediation should first remove direct backup exposure '
                       'and strengthen application access controls, then improve document generation '
                       'and protection. Closure requires evidence-based retesting; the supplied '
                       'material does not document completed remediation.')

        self.page('Appendix A — Evidence Gallery and Register', 'EvidenceRegister')
        self.paragraph('Images are embedded with their technical results in Section 03. This register '
                       'provides navigation, finding associations and provenance without repeating '
                       'the screenshots. E-10–E-13 identify restricted source artifacts summarized '
                       'in the public text; they are not screenshots.')
        self.table(['Evidence', 'Title / source type', 'Association'], [
            [entry['id'], entry['title'] + '\n' + ('Redacted screenshot' if entry.get('file') else
             'Restricted artifact — narrative reference'),
             'Reconnaissance context' if entry['related'] == 'Reconnaissance' else entry['related']]
            for entry in self.evidence
        ], [1050, 6360, 2150], small=True)
        paragraph = self.paragraph(style='Caption')
        self.run(paragraph, 'Jump to evidence: ')
        for index, entry in enumerate(self.evidence):
            if index:
                self.run(paragraph, '  ·  ')
            self.link(paragraph, entry['id'], entry['id'].replace('-', ''))
        self.heading('Evidence handling', 2)
        self.paragraph('E-01–E-09 use the existing public derivatives listed in evidence/manifest.json. '
                       'Their image bytes are embedded unchanged. All original captures and existing '
                       'reports are preserved. Redacted content is neither reconstructed nor inferred. '
                       'Reconnaissance evidence is deliberately not assigned a fabricated vulnerability.')
        self.paragraph('The full F-01 HTTP transaction, a public metadata screenshot and a public '
                       'backup-download screenshot are absent. The report uses clear narrative '
                       'references to retained artifacts where images are unavailable. Original '
                       'patient reports, SQL records and credentials are excluded from the deliverables.')

        self.page('Appendix B — Technical Command Reference', 'Commands')
        self.callout('Reference only', 'These commands document the assessment workflow using '
                     'mediroza.example and generic paths. They are illustrative syntax, not evidence '
                     'of execution against that placeholder. Use only within an authorized scope.')
        self.heading('B.1  Reconnaissance and service identification', 2)
        self.code('whois mediroza.example\nnslookup mediroza.example\nwhatweb mediroza.example\n'
                  'dnsrecon -d mediroza.example\nnmap -sV mediroza.example')
        self.heading('B.2  Web path enumeration', 2)
        self.code('gobuster dir -u https://mediroza.example/ ' + '\\\n' + '  -w enumeration.txt')
        self.paragraph('E-01–E-05 support the retained reconnaissance and enumeration observations. '
                       'The command list does not establish vulnerabilities in every discovered service.')
        self.heading('B.3  PDF verification-data extraction and recovery', 2)
        self.code('pdf2john patient_report_1.pdf patient_report_2.pdf ' + '\\\n' +
                  '  patient_report_3.pdf > pdfs_hash.hash\n\n'
                  'john --format=PDF --wordlist=WORDLIST.txt ' + '\\\n' +
                  '  --pot=results.pot pdfs_hash.hash\n\n'
                  'john --show --format=PDF --pot=results.pot pdfs_hash.hash')
        self.paragraph('Verification data and pot files contain sensitive material and must remain '
                       'restricted. The public report retains only the redacted result (E-09) '
                       'and the original-opening validation summary (E-10).')
        self.heading('B.4  Original PDF metadata examination', 2)
        self.code("exiftool -password 'PDF_PASSWORD' patient_report_3.pdf")
        self.paragraph('PDF_PASSWORD is a placeholder. The documented examination used the '
                       'original PDF. Preserve its metadata and integrity; a re-exported reading '
                       'copy is not an equivalent evidence source (E-11).')

        self.page('Appendix B — Backup and Local SQL Analysis', 'SQLCommands', continuation=True)
        self.heading('B.5  Backup response and local file examination', 2)
        self.code('curl -q -sS --max-time 30 -D backup_headers.txt ' + '\\\n' +
                  "  -o backup.sql -w 'HTTP status: %{http_code}\\n' " + '\\\n' +
                  "  'https://mediroza.example/legacy/backup.sql'\n\n"
                  'file backup.sql\nhead -n 20 backup.sql\nsha256sum backup.sql verification_copy.sql')
        self.paragraph('The URL and filenames are examples, not the original target location. '
                       'A retained response is evidence of the response itself; proof of a '
                       'session-free request additionally requires the originating request. '
                       'Hash comparison establishes file identity, not who could retrieve it (E-12).')
        self.heading('B.6  Local data analysis', 2)
        self.code('SELECT COUNT(*) AS employee_count FROM staff;\n'
                  'SELECT COUNT(*) AS shareholder_count FROM shareholders;\n\n'
                  'SELECT full_name, job_title, department, monthly_salary_zar\n'
                  'FROM staff ORDER BY id;\n\n'
                  'SELECT shareholder_name, share_percent, shares_held, share_class\n'
                  'FROM shareholders ORDER BY id;')
        self.paragraph('These queries describe analysis against a local SQLite database populated '
                       'from the relevant INSERT statements. They do not imply a connection to '
                       'the hospital database. Do not execute the original MySQL administrative '
                       'instructions merely to inspect the data. Identifiable query output '
                       'must remain outside the public report (E-13).')
        self.heading('Author and document control', 2)
        self.table(['Field', 'Information'], [
            ['Author / Organization', 'Mardochée BONOU / Networkwalks'],
            ['Program / Batch', 'Cybersecurity & Ethical Hacking / B084'],
            ['Project / Assessment period', 'Mediroza — Final Internship Project / 22–25 November 2026'],
            ['Edition / Issue date', 'Public · Version 2.0 / 25 November 2026'],
            ['Editorial reference', 'Current repository README.md; four findings and unchanged risk levels'],
            ['Profile / Repository', 'github.com/Mardoch45 / Mardoch45/INTERSHIP-FINAL-REPORT'],
        ], [3000, 6560], small=True)

    def save(self):
        section = element(self.body, 'w:sectPr')
        element(section, 'w:headerReference', {'w:type': 'default', 'r:id': 'rIdHeader'})
        element(section, 'w:footerReference', {'w:type': 'default', 'r:id': 'rIdFooter'})
        element(section, 'w:pgSz', {'w:w': '11906', 'w:h': '16838'})
        element(section, 'w:pgMar', {'w:top': '1100', 'w:bottom': '1040', 'w:left': '1173',
                                   'w:right': '1173', 'w:header': '530', 'w:footer': '530'})
        element(section, 'w:titlePg')
        relationships_ns = 'http://schemas.openxmlformats.org/package/2006/relationships'
        relationships = ET.Element('Relationships', xmlns=relationships_ns)
        relationship_type = NS['r'] + '/'
        for identifier, kind, target in [('rIdStyles', 'styles', 'styles.xml'),
                                         ('rIdSettings', 'settings', 'settings.xml'),
                                         ('rIdHeader', 'header', 'header1.xml'),
                                         ('rIdFooter', 'footer', 'footer1.xml')]:
            ET.SubElement(relationships, 'Relationship', Id=identifier,
                          Type=relationship_type + kind, Target=target)
        for index, source in enumerate(self.images, 1):
            ET.SubElement(relationships, 'Relationship', Id=f'rIdImage{index}',
                          Type=relationship_type + 'image', Target=f'media/{source.name}')
        package_relationships = ET.Element('Relationships', xmlns=relationships_ns)
        ET.SubElement(package_relationships, 'Relationship', Id='rId1', Type=relationship_type + 'officeDocument',
                      Target='word/document.xml')
        ET.SubElement(package_relationships, 'Relationship', Id='rId2',
                      Type='http://schemas.openxmlformats.org/package/2006/relationships/metadata/core-properties',
                      Target='docProps/core.xml')
        types = ET.Element('Types', xmlns='http://schemas.openxmlformats.org/package/2006/content-types')
        for ext, mime in [('rels', 'application/vnd.openxmlformats-package.relationships+xml'),
                          ('xml', 'application/xml'), ('png', 'image/png')]:
            ET.SubElement(types, 'Default', Extension=ext, ContentType=mime)
        for name, kind in [('document', 'document.main'), ('styles', 'styles'), ('settings', 'settings'),
                           ('header1', 'header'), ('footer1', 'footer')]:
            ET.SubElement(types, 'Override', PartName=f'/word/{name}.xml',
                          ContentType=f'application/vnd.openxmlformats-officedocument.wordprocessingml.{kind}+xml')
        ET.SubElement(types, 'Override', PartName='/docProps/core.xml',
                      ContentType='application/vnd.openxmlformats-package.core-properties+xml')
        core = ('<?xml version="1.0" encoding="UTF-8"?>'
                '<cp:coreProperties xmlns:cp="http://schemas.openxmlformats.org/package/2006/metadata/core-properties" '
                'xmlns:dc="http://purl.org/dc/elements/1.1/">'
                '<dc:title>Mediroza — Penetration Testing Report — Public Edition</dc:title>'
                '<dc:creator>Mardochée BONOU</dc:creator>'
                '<dc:subject>Networkwalks — Cybersecurity &amp; Ethical Hacking — B084</dc:subject>'
                '<cp:keywords>Public; redacted; technical assessment; version 2.0</cp:keywords>'
                '</cp:coreProperties>')
        settings = ET.Element(qualified('w:settings'))
        element(settings, 'w:updateFields', {'w:val': 'true'})
        element(settings, 'w:defaultTabStop', {'w:val': '720'})
        header = ET.Element(qualified('w:hdr'))
        self.paragraph('MEDIROZA  /  PENETRATION TESTING REPORT', 'Header', parent=header)
        footer = ET.Element(qualified('w:ftr'))
        paragraph = self.paragraph('PUBLIC EDITION   ·   M. BONOU   ·   B084', 'Footer', parent=footer)
        self.run(paragraph, '\t')
        self.run(paragraph, 'PAGE ')
        field = element(paragraph, 'w:fldSimple', {'w:instr': ' PAGE '})
        self.run(field, '1')
        self.run(paragraph, ' / ')
        field = element(paragraph, 'w:fldSimple', {'w:instr': ' NUMPAGES '})
        self.run(field, '18')
        with zipfile.ZipFile(OUTPUT / (STEM + '.docx'), 'w', zipfile.ZIP_DEFLATED) as archive:
            for name, content in {
                '[Content_Types].xml': xml_bytes(types), '_rels/.rels': xml_bytes(package_relationships),
                'word/document.xml': xml_bytes(self.document), 'word/styles.xml': styles(),
                'word/settings.xml': xml_bytes(settings), 'word/header1.xml': xml_bytes(header),
                'word/footer1.xml': xml_bytes(footer), 'word/_rels/document.xml.rels': xml_bytes(relationships),
                'docProps/core.xml': core.encode(),
            }.items():
                archive.writestr(name, content)
            for source in self.images:
                archive.write(source, f'word/media/{source.name}')
        (OUTPUT / 'professional_report_evidence.json').write_text(
            json.dumps(self.evidence, indent=2, ensure_ascii=False) + '\n')


def styles():
    root = ET.Element(qualified('w:styles'))
    defaults = element(root, 'w:docDefaults')
    run_props = element(element(defaults, 'w:rPrDefault'), 'w:rPr')
    element(run_props, 'w:rFonts', {'w:ascii': 'Lato', 'w:hAnsi': 'Lato'})
    element(run_props, 'w:sz', {'w:val': '21'})
    element(run_props, 'w:color', {'w:val': INK})
    element(run_props, 'w:lang', {'w:val': 'en-GB'})
    formats = {
        'Normal': (10.5, INK, False, 0, 115, False),
        'Heading1': (21, NAVY, True, 0, 215, True),
        'ContentsTitle': (21, NAVY, True, 0, 215, True),
        'FindingTitle': (18, NAVY, True, 0, 160, True),
        'Heading2': (13, TEAL, True, 155, 90, True),
        'Heading3': (11, NAVY, True, 145, 65, True),
        'Kicker': (9, TEAL, True, 0, 100, True),
        'Deck': (13, MUTED, False, 0, 220, True),
        'Label': (10.5, TEAL, True, 155, 65, True),
        'TableText': (9.5, INK, False, 0, 25, False),
        'AfterTable': (2, INK, False, 0, 45, False),
        'Caption': (8.5, MUTED, False, 45, 60, False),
        'EvidenceTitle': (10, TEAL, True, 125, 55, True),
        'Image': (2, INK, False, 0, 0, True),
        'Callout': (10.5, INK, False, 125, 145, False),
        'Code': (9, INK, False, 0, 15, False),
        'Header': (8, MUTED, True, 0, 0, False),
        'Footer': (8, MUTED, False, 0, 0, False),
        'CoverMeta': (9, MUTED, False, 120, 650, False),
        'CoverTitle': (46, NAVY, True, 0, 150, True),
        'CoverSubtitle': (30, NAVY, False, 0, 200, True),
        'CoverDeck': (12, TEAL, False, 0, 400, True),
        'CoverNote': (13, TEAL, True, 400, 120, True),
        'CoverSmall': (10, MUTED, False, 0, 0, False),
        'TOC1': (10, INK, False, 60, 35, False),
        'TOC2': (9.5, MUTED, False, 0, 30, False),
    }
    for identifier, (size, color, bold, before, after, keep) in formats.items():
        style = element(root, 'w:style', {'w:type': 'paragraph', 'w:styleId': identifier})
        element(style, 'w:name', {'w:val': identifier if not identifier.startswith('Heading') else
                                'heading ' + identifier[-1]})
        if identifier != 'Normal':
            element(style, 'w:basedOn', {'w:val': 'Normal'})
        element(style, 'w:next', {'w:val': 'Normal'})
        props = element(style, 'w:pPr')
        element(props, 'w:spacing', {'w:before': before, 'w:after': after, 'w:line': 267, 'w:lineRule': 'auto'})
        element(props, 'w:widowControl')
        if keep:
            element(props, 'w:keepNext')
        element(props, 'w:keepLines')
        if identifier.startswith('Heading'):
            element(props, 'w:outlineLvl', {'w:val': int(identifier[-1]) - 1})
        if identifier == 'Image':
            element(props, 'w:jc', {'w:val': 'center'})
        if identifier in ['Code', 'Callout']:
            element(props, 'w:shd', {'w:fill': LIGHT, 'w:val': 'clear'})
            element(props, 'w:ind', {'w:left': '130', 'w:right': '130'})
        if identifier in ['Header', 'Footer']:
            border = element(props, 'w:pBdr')
            element(border, 'w:bottom' if identifier == 'Header' else 'w:top',
                    {'w:val': 'single', 'w:sz': '4', 'w:space': '7', 'w:color': 'CBD7DB'})
        if identifier == 'Footer':
            element(element(props, 'w:tabs'), 'w:tab', {'w:val': 'right', 'w:pos': '9560'})
        if identifier.startswith('TOC'):
            element(element(props, 'w:tabs'), 'w:tab', {'w:val': 'right', 'w:pos': '9560', 'w:leader': 'dot'})
            if identifier == 'TOC2':
                element(props, 'w:ind', {'w:left': '200'})
        run = element(style, 'w:rPr')
        element(run, 'w:sz', {'w:val': round(size * 2)})
        element(run, 'w:color', {'w:val': color})
        if bold:
            element(run, 'w:b')
        if identifier == 'Code':
            element(run, 'w:rFonts', {'w:ascii': 'DejaVu Sans Mono', 'w:hAnsi': 'DejaVu Sans Mono'})
    return xml_bytes(root)


def export():
    import ctypes
    import os
    import uno
    from com.sun.star.beans import PropertyValue

    os.environ['URE_BOOTSTRAP'] = 'vnd.sun.star.pathname:/usr/lib/libreoffice/program/fundamentalrc'
    library = ctypes.CDLL('/usr/lib/libreoffice/program/libmergedlo.so', mode=ctypes.RTLD_GLOBAL)
    initialize = library.libreofficekit_hook_2
    initialize.argtypes = [ctypes.c_char_p, ctypes.c_char_p]
    initialize.restype = ctypes.c_void_p
    engine = initialize(b'/usr/lib/libreoffice/program', b'file:///tmp/mediroza-professional-embedded')
    if not engine:
        raise RuntimeError('Embedded LibreOffice initialization failed')
    context = uno.getComponentContext()

    def prop(name, value):
        result = PropertyValue()
        result.Name = name
        result.Value = value
        return result

    desktop = context.ServiceManager.createInstanceWithContext('com.sun.star.frame.Desktop', context)
    document = None
    try:
        document = desktop.loadComponentFromURL((OUTPUT / (STEM + '.docx')).as_uri(), '_blank', 0,
                                                 (prop('Hidden', True), prop('UpdateDocMode', 3)))
        if document is None:
            raise RuntimeError('Could not load generated DOCX')
        document.refresh()
        indexes = document.getDocumentIndexes()
        for index in range(indexes.getCount()):
            indexes.getByIndex(index).update()
        fields = document.getTextFields()
        fields.refresh()
        document.refresh()
        for index in range(indexes.getCount()):
            indexes.getByIndex(index).update()
        document.storeAsURL((OUTPUT / (STEM + '.docx')).as_uri(),
                            (prop('FilterName', 'Office Open XML Text'), prop('Overwrite', True)))
        document.storeToURL((OUTPUT / (STEM + '.pdf')).as_uri(),
                            (prop('FilterName', 'writer_pdf_Export'), prop('Overwrite', True),
                             prop('FilterData', (prop('ExportBookmarks', True), prop('UseTaggedPDF', True)))))
        print(json.dumps({'docx': STEM + '.docx', 'pdf': STEM + '.pdf',
                          'pages': document.CurrentController.PageCount, 'contents_indexes': indexes.getCount()}))
    finally:
        if document is not None:
            document.close(True)


def main():
    parser = argparse.ArgumentParser(description='Build the public professional Mediroza report.')
    parser.add_argument('--export', action='store_true', help='Update the native contents and export PDF using LibreOffice / UNO.')
    args = parser.parse_args()
    manifest = json.loads((ROOT / 'evidence' / 'manifest.json').read_text())
    for entry in manifest:
        path = ROOT / entry['file']
        if hashlib.sha256(path.read_bytes()).hexdigest() != entry['sha256']:
            raise RuntimeError('Screenshot differs from evidence manifest: ' + entry['id'])
    report = Report()
    report.build()
    report.save()
    if args.export:
        export()
    else:
        print(OUTPUT / (STEM + '.docx'))


if __name__ == '__main__':
    main()
