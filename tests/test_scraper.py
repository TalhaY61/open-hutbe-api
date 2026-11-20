import unittest
from datetime import date

from scripts.scraper import BASE_SITE, extract_pdf_candidates


class ScraperCompatibilityTests(unittest.TestCase):
    def test_table_keeps_pdf_word_and_date_together(self):
        html = '''<table><tr><td>20.11.2026</td><td>
            <a href="/Documents/hutbe.pdf">Cuma Hutbesi</a>
            <a href="/Documents/hutbe.docx">Word</a>
            </td></tr></table>'''
        candidates = extract_pdf_candidates(html, BASE_SITE)
        self.assertEqual(len(candidates), 1)
        candidate = candidates[0]
        self.assertEqual(candidate['source_pdf_url'], BASE_SITE + '/Documents/hutbe.pdf')
        self.assertEqual(candidate['source_doc_url'], BASE_SITE + '/Documents/hutbe.docx')
        self.assertEqual(candidate['title'], 'Cuma Hutbesi')
        self.assertEqual(candidate['date'], date(2026, 11, 20))

    def test_sharepoint_list_keeps_pdf_word_and_date_together(self):
        html = '''<script>var WPQ2ListData = {"Row": [{
            "PDF": "/Documents/hutbe.pdf", "Word": "/Documents/hutbe.doc",
            "Title": "Cuma Hutbesi", "Tarih": "20.11.2026"
            }]};</script>'''
        candidates = extract_pdf_candidates(html, BASE_SITE)
        self.assertEqual(len(candidates), 1)
        candidate = candidates[0]
        self.assertEqual(candidate['source_pdf_url'], BASE_SITE + '/Documents/hutbe.pdf')
        self.assertEqual(candidate['source_doc_url'], BASE_SITE + '/Documents/hutbe.doc')
        self.assertEqual(candidate['title'], 'Cuma Hutbesi')
        self.assertEqual(candidate['date'], date(2026, 11, 20))


if __name__ == '__main__':
    unittest.main()
