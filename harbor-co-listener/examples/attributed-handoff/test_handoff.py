"""Offline browser replay with fictional contributors and generated audio."""
import json
import os
import unittest
from pathlib import Path

from playwright.sync_api import expect, sync_playwright


ROOT = Path(__file__).resolve().parent
NATIVE = ROOT.parents[1] / 'index.html'


def download(page, selector):
    with page.expect_download() as result:
        page.locator(selector).click()
    return json.loads(result.value.path().read_bytes())


def open_json(page, data):
    page.locator('#open').set_input_files({
        'name': 'synthetic.json', 'mimeType': 'application/json',
        'buffer': json.dumps(data, ensure_ascii=False).encode('utf-8'),
    })


def attach(page):
    page.locator('#clip').set_input_files(ROOT / 'example.wav')
    expect(page.locator('#listen-label')).to_be_visible()
    expect(page.locator('#listened')).not_to_be_checked()


def reply(page, alias, interpretation, self_report=False):
    page.locator('#who').fill(alias)
    page.locator('#words').fill(interpretation)
    if self_report:
        page.locator('#listened').check()
    page.locator('#append').click()
    expect(page.locator('#status')).to_contain_text('Reply appended')


class HandoffTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        pw = sync_playwright().start()
        cls.addClassCleanup(pw.stop)
        cls.browser = pw.chromium.launch(executable_path=os.environ.get('HARBOR_CHROMIUM'))
        cls.addClassCleanup(cls.browser.close)

    def fresh_view(self, path=ROOT / 'index.html'):
        ctx = self.browser.new_context(offline=True, viewport={'width': 390, 'height': 844})
        self.addCleanup(ctx.close)
        page = ctx.new_page()
        page.on('request', lambda req: self.remote.append(req.url) if req.url.startswith(('https:', 'http:')) else None)
        page.goto(path.as_uri())
        return page

    def setUp(self):
        self.remote = []

    def native_export(self):
        page = self.fresh_view(NATIVE)
        page.locator('#song').fill('Synthetic tones')
        page.locator('#heard').fill('One gap.')
        page.locator('#felt').fill('That pause felt like relief.')
        page.locator('#mark').click()
        page.locator('#noticed').fill('Earlier response with no author field.')
        page.locator('#respond').click()
        return download(page, '#export')

    def test_two_contexts_append_without_changing_source_or_inheriting_audio(self):
        original = self.native_export()
        first = self.fresh_view()
        open_json(first, original)
        expect(first.locator('#replies article')).to_have_count(0)
        expect(first.locator('#original .meta')).to_have_text([
            'Legacy record · identity, access and listening unknown'] * 2)

        attach(first)
        reply(first, 'Observer', 'A file was available to me.')
        self.assertEqual(download(first, '#save')['replies'][0]['listening'], 'UNKNOWN')
        attach(first)
        first.locator('#player').evaluate('p => { p.muted = true; return p.play() }')
        first.locator('#player').evaluate('p => p.pause()')
        expect(first.locator('#listened')).not_to_be_checked()
        reply(first, 'Playback check', 'Playback started in the synthetic test.')
        self.assertEqual(download(first, '#save')['replies'][1]['listening'], 'UNKNOWN')
        attach(first)
        reply(first, 'Rowan', 'I read the pause as hesitation.', self_report=True)
        packet = download(first, '#save')
        self.assertEqual(packet['session'], original)
        self.assertEqual([(r['access'], r['listening']) for r in packet['replies']], [
            ('DIRECT_AUDIO_AVAILABLE', 'UNKNOWN'), ('DIRECT_AUDIO_AVAILABLE', 'UNKNOWN'),
            ('DIRECT_AUDIO_AVAILABLE', 'SELF_REPORTED')])

        second = self.fresh_view()
        open_json(second, packet)
        expect(second.locator('#status')).to_contain_text('session JSON only')
        self.assertIsNone(second.locator('#player').get_attribute('src'))
        expect(second.locator('#listen-label')).to_be_hidden()
        words = '  I read relief in the listener’s words.\nI disagree with Rowan.  '
        reply(second, 'Jules', words)
        continued = download(second, '#save')
        self.assertEqual(continued['session'], original)
        self.assertEqual(continued['replies'][:-1], packet['replies'])
        self.assertEqual(continued['replies'][-1], {
            'momentIndex': 0, 'contributor': 'Jules', 'access': 'SESSION_JSON_ONLY',
            'listening': 'UNKNOWN', 'interpretation': words})
        self.assertEqual(download(second, '#source'), original)
        self.assertNotIn('example.wav', json.dumps(continued))
        self.assertEqual(self.remote, [])

    def test_exact_text_and_unattributed_legacy_entries_survive(self):
        source = self.native_export()
        words = ' \t“That pause felt like relief.”\r\n  Cafe\u0301 <quiet>  '
        source['moments'][0]['felt'] = words
        source['responses'][0]['timeSeconds'] = 1.2
        page = self.fresh_view()
        open_json(page, source)
        expect(page.locator('#status')).to_contain_text('Opened locally')
        self.assertEqual(page.locator('#original article').first.locator('p').last.text_content(), words)
        reply(page, 'Text reader', 'I can quote the original text.')
        packet = download(page, '#save')
        self.assertEqual(packet['session'], source)
        self.assertEqual(download(page, '#source'), source)
        self.assertEqual(len(packet['replies']), 1)

    def test_scripted_claims_marked_and_contradictory_records_rejected(self):
        page = self.fresh_view()
        original = download(page, '#save')
        self.assertTrue(all(r['scriptedExample'] for r in original['replies']))
        self.assertEqual(page.evaluate('document.documentElement.scrollWidth'), 390)
        for change in ({'listening': 'SELF_REPORTED'}, {'momentIndex': 5}, {'contributor': ''}):
            bad = json.loads(json.dumps(original))
            bad['replies'][-1].update(change)
            open_json(page, bad)
            expect(page.locator('#status')).to_contain_text('Could not open')
            self.assertEqual(download(page, '#save'), original)
        self.assertEqual(self.remote, [])

    def test_self_report_is_scoped_to_one_contributor_and_moment(self):
        page = self.fresh_view()
        source = download(page, '#source')
        source['moments'].append(dict(source['moments'][0], felt='A second moment.'))
        open_json(page, source)
        expect(page.locator('#status')).to_contain_text('Opened locally')
        attach(page)
        page.locator('#who').fill('Rowan')
        page.locator('#listened').check()
        page.locator('#target').select_option('1')
        expect(page.locator('#listened')).not_to_be_checked()
        page.locator('#listened').check()
        page.locator('#who').fill('Jules')
        expect(page.locator('#listened')).not_to_be_checked()
        # Replacing the clip cannot retroactively turn this view into a JSON-only view.
        page.locator('#clip').set_input_files({
            'name': 'unsupported.txt', 'mimeType': 'text/plain', 'buffer': b'synthetic'})
        expect(page.locator('#listen-label')).to_be_hidden()
        reply(page, 'Jules', 'A different reading of the second moment.')
        saved = download(page, '#save')['replies'][0]
        self.assertEqual((saved['contributor'], saved['momentIndex'], saved['listening'], saved['access']),
                         ('Jules', 1, 'UNKNOWN', 'DIRECT_AUDIO_AVAILABLE'))


if __name__ == '__main__':
    unittest.main()
