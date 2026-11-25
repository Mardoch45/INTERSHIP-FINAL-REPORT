from __future__ import annotations

import hashlib
import json
import re
import subprocess
import tempfile
import zipfile
from pathlib import Path
from xml.etree import ElementTree as ET


ROOT = Path(__file__).resolve().parents[1]
DOCS = ROOT / 'docs'
STEM = 'Mediroza_Penetration_Testing_Report_Professional'
NS = {'w': 'http://schemas.openxmlformats.org/wordprocessingml/2006/main'}


def normalize(text):
    text = text.replace('\u00ad', '').replace('\u00a0', ' ')
    text = re.sub(r'(?<=\w)-\s*\n\s*(?=\w)', '-', text)
    text = re.sub(r'\.{2,}', ' ', text)
    return re.sub(r'\s+', ' ', text).strip()


def digest(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def main():
    pdf = DOCS / (STEM + '.pdf')
    docx = DOCS / (STEM + '.docx')
    text = subprocess.check_output(['pdftotext', '-layout', str(pdf), '-'], text=True)
    pages = [page for page in text.split('\f') if page.strip()]
    pdf_text = normalize(text)
    raw_text = normalize(subprocess.check_output(['pdftotext', '-raw', str(pdf), '-'], text=True))
    checks = {}
    checks['page_count'] = len(pages)
    checks['no_blank_pages'] = all(len(page.strip()) > 500 for page in pages)
    checks['page_fields_correct'] = all(
        re.search(rf'PAGE\s+{index}\s*/\s*{len(pages)}\b', page)
        for index, page in enumerate(pages[1:], 2)
    )
    checks['no_replacement_characters'] = '\ufffd' not in text
    checks['no_accidental_patch_prefixes_in_commands'] = not re.search(r'^\s*\+\s+--?\w', text, re.M)
    with zipfile.ZipFile(docx) as archive:
        document = ET.fromstring(archive.read('word/document.xml'))
        bookmarks = {node.get('{'+NS['w']+'}name') for node in document.findall('.//w:bookmarkStart', NS)}
        links = [node.get('{'+NS['w']+'}anchor') for node in document.findall('.//w:hyperlink', NS)]
        checks['docx_internal_link_count'] = len(links)
        checks['docx_all_internal_links_resolve'] = all(link in bookmarks for link in links)
        fields = [node.text or '' for node in document.findall('.//w:instrText', NS)]
        fields += [node.get('{'+NS['w']+'}instr', '') for node in document.findall('.//w:fldSimple', NS)]
        checks['native_table_of_contents'] = any('TOC ' in field for field in fields)
        paragraphs = []
        for paragraph in document.findall('.//w:p', NS):
            tokens = []
            for node in paragraph.iter():
                if node.tag == '{'+NS['w']+'}t':
                    tokens.append(node.text or '')
                elif node.tag in ['{'+NS['w']+'}br', '{'+NS['w']+'}tab']:
                    tokens.append(' ')
            paragraphs.append(normalize(''.join(tokens)))
        checked = [paragraph for paragraph in paragraphs if len(paragraph) > 20 and '....' not in paragraph]
        mismatches = [paragraph for paragraph in checked if paragraph not in pdf_text and paragraph not in raw_text]
        checks['docx_pdf_paragraphs_compared'] = len(checked)
        checks['docx_pdf_text_matches'] = not mismatches
        image_hashes = {hashlib.sha256(archive.read(name)).hexdigest() for name in archive.namelist()
                        if name.startswith('word/media/')}
        manifest = json.loads((ROOT / 'evidence/manifest.json').read_text())
        checks['public_screenshots_unchanged'] = all(digest(ROOT / entry['file']) == entry['sha256']
                                                      for entry in manifest)
        checks['all_nine_original_public_derivatives_embedded'] = all(entry['sha256'] in image_hashes
                                                                     for entry in manifest)
        checks['embedded_image_count'] = len(image_hashes)
        profiles = {}
        for table in document.findall('.//w:tbl', NS):
            rows = [[normalize(' '.join(node.text or '' for node in cell.findall('.//w:t', NS)))
                     for cell in row.findall('w:tc', NS)] for row in table.findall('w:tr', NS)]
            if rows and rows[0] == ['Finding profile', 'Assessment detail']:
                profile = dict(rows[1:])
                profiles[profile['Finding ID']] = profile
        readme = (ROOT / 'README.md').read_text()
        summary_rows = re.findall(
            r'^\| (F-0[1-4]) \| ([^|]+) \| (High(?: \(provisional\))?|Low) \| '
            r'(Partially documented|Verified) \|$', readme, re.M)
        checks['four_uniform_finding_profiles'] = len(profiles) == 4
        checks['finding_severity_and_validation_match_readme'] = len(summary_rows) == 4 and all(
            profiles[identifier]['Severity'] == severity and profiles[identifier]['Validation Status'] == status
            for identifier, title, severity, status in summary_rows)
        checks['author_period_batch_match_readme'] = all(
            value in readme and value in pdf_text for value in ['Mardochée BONOU', '22–25 November 2026', 'B084'])
        tools = ['Kali Linux', 'WHOIS', 'nslookup', 'DNSRecon', 'WhatWeb', 'Gobuster', 'Nmap',
                 'FTP client', 'pdf2john', 'John the Ripper', 'ExifTool', 'Poppler', 'curl', 'Python', 'SQLite']
        checks['tools_match_readme'] = all(tool.lower() in readme.lower() and tool.lower() in pdf_text.lower()
                                          for tool in tools)
    with tempfile.TemporaryDirectory(prefix='mediroza-verify-') as temporary:
        bounds = Path(temporary) / 'bounds.html'
        subprocess.run(['pdftotext', '-bbox-layout', str(pdf), str(bounds)], check=True)
        ns = {'h': 'http://www.w3.org/1999/xhtml'}
        boxes = ET.parse(bounds).findall('.//h:word', ns)
        checks['text_within_page_bounds'] = all(
            45 <= float(word.get('xMin')) < float(word.get('xMax')) <= 550
            and 25 <= float(word.get('yMin')) < float(word.get('yMax')) <= 815
            for word in boxes
        )
        link_xml = subprocess.check_output(['pdftohtml', '-xml', '-hidden', '-i', '-stdout', str(pdf)], text=True)
        link_document = ET.fromstring(link_xml)
        pdf_links = link_document.findall('.//a')
        targets = [int(node.get('href').rsplit('#', 1)[1]) for node in pdf_links]
        checks['pdf_internal_link_count'] = len(targets)
        checks['pdf_all_links_target_existing_pages'] = all(1 <= target <= len(pages) for target in targets)
        toc_links = link_document.findall("./page[@number='2']//a")
        toc_entries = [node for node in toc_links if '...' in ''.join(node.itertext())]
        checks['toc_entry_count'] = len(toc_entries)
        checks['toc_printed_pages_match_link_targets'] = all(
            int(re.search(r'(\d+)\s*$', ''.join(node.itertext())).group(1)) ==
            int(node.get('href').rsplit('#', 1)[1]) for node in toc_entries
        )
        checks['toc_targets_match_section_titles'] = all(
            normalize(re.split(r'\.{2,}', ''.join(node.itertext()))[0]) in
            normalize(pages[int(node.get('href').rsplit('#', 1)[1]) - 1]) for node in toc_entries
        )
    checks['old_pdf_preserved_and_archive_identical'] = (
        digest(DOCS / 'Public_Report_Mardochee_BONOU_B084.pdf') ==
        digest(DOCS / 'archive/Public_Report_Mardochee_BONOU_B084_original.pdf')
    )
    checks['old_docx_preserved_and_archive_identical'] = (
        digest(DOCS / 'Public_Report_Mardochee_BONOU_B084.docx') ==
        digest(DOCS / 'archive/Public_Report_Mardochee_BONOU_B084_original.docx')
    )
    checks['readme_alignment'] = {
        'finding_ratings': {'F-01': 'High (provisional)', 'F-02': 'High', 'F-03': 'Low', 'F-04': 'High'},
        'overall_risk': 'HIGH', 'assessment_period': '22–25 November 2026',
        'author': 'Mardochée BONOU', 'batch': 'B084',
        'validation': {'F-01': 'Partially documented', 'F-02': 'Verified', 'F-03': 'Verified', 'F-04': 'Verified'},
    }
    checks['required_limits_present'] = all(value in pdf_text for value in [
        'Partially documented', 'High (provisional)', 'three original',
        '27 August 2019', 'three employment dates', 'No CVSS', 'No database modification',
        'complete originating request is not archived',
    ])
    checks['visual_review'] = {
        'status': 'Manual review of this edition is recorded in REPORT_REDESIGN_REVIEW.md; not an automated check',
        'checks': ['tables', 'image framing and legibility', 'isolated headings', 'blank pages',
                   'pagination', 'character rendering', 'confidentiality of public screenshots'],
    }
    failures = [name for name, value in checks.items() if value is False]
    if mismatches:
        print('DOCX/PDF paragraph mismatches:', json.dumps(mismatches, ensure_ascii=False))
    checks['passed'] = not failures
    checks['failures'] = failures
    checks['artifact_sha256'] = {path.name: digest(path) for path in [pdf, docx]}
    checks['readme_sha256'] = digest(ROOT / 'README.md')
    output = DOCS / 'professional_report_verification.json'
    output.write_text(json.dumps(checks, indent=2, ensure_ascii=False) + '\n')
    print(json.dumps(checks, indent=2, ensure_ascii=False))
    if failures:
        raise SystemExit(1)


if __name__ == '__main__':
    main()
