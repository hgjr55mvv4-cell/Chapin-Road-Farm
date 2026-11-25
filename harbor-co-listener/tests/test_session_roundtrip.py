"""Offline browser tests. Run with python3 -m unittest discover -s tests in this component.

Requires Python Playwright and its Chromium browser, or HARBOR_CHROMIUM pointing
to an installed Chromium binary. HARBOR_EXPORT_PAGE can point to an older
index.html to produce the input using the actual historical exporter.
"""
import io
import json
import os
import unittest
import wave
from pathlib import Path

from playwright.sync_api import expect, sync_playwright


PAGE = Path(__file__).resolve().parents[1] / 'index.html'


def local_audio(page):
    audio = io.BytesIO()
    with wave.open(audio, 'wb') as wav:
        wav.setnchannels(1)
        wav.setsampwidth(1)
        wav.setframerate(8000)
        wav.writeframes(bytes([128]) * 24000)
    page.locator('#file').set_input_files({
        'name': 'synthetic.wav', 'mimeType': 'audio/wav', 'buffer': audio.getvalue(),
    })
    page.wait_for_function("document.getElementById('audio').readyState >= 1")


def export(page):
    with page.expect_download() as download:
        page.locator('#export').click()
    return json.loads(download.value.path().read_bytes())


def open_file(page, data, name='session.json'):
    payload = data if isinstance(data, bytes) else json.dumps(data).encode()
    page.locator('#session-file').set_input_files({
        'name': name, 'mimeType': 'application/json', 'buffer': payload,
    })


def session_data(exported):
    return {key: value for key, value in exported.items() if key != 'exportedAt'}


class SessionRoundtripTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        playwright = sync_playwright().start()
        cls.addClassCleanup(playwright.stop)
        cls.browser = playwright.chromium.launch(executable_path=os.environ.get('HARBOR_CHROMIUM'))
        cls.addClassCleanup(cls.browser.close)

    def setUp(self):
        self.context = self.browser.new_context(offline=True)
        self.addCleanup(self.context.close)
        self.remote_requests = []
        def record_request(request):
            if request.url.startswith(('http://', 'https://')):
                self.remote_requests.append(request.url)
        self.context.on('request', record_request)
        self.page = self.context.new_page()
        self.page.goto(PAGE.as_uri())

    def test_export_reopen_append_and_export_offline(self):
        source = self.context.new_page()
        source.goto(Path(os.environ.get('HARBOR_EXPORT_PAGE', PAGE)).resolve().as_uri())
        source.locator('#heard').fill('First, a pause.')
        source.locator('#mark').click()
        local_audio(source)
        source.locator('#song').fill('Synthetic piece')
        source.locator('#artist').fill('Test ensemble')
        source.locator('#audio').evaluate('audio => { audio.currentTime = 1.25 }')
        source.wait_for_function("!document.getElementById('audio').seeking")
        source.locator('#noticed').fill('A second perspective.')
        source.locator('#uncertain').fill('Unsure about the timing.')
        source.locator('#respond').click()
        source.locator('#heard').fill('An entry after the response.')
        source.locator('#felt').fill('Quiet <then> loud.')
        source.locator('#mark').click()
        original = export(source)
        source.close()
        self.assertIsNone(original['moments'][0]['timeSeconds'])
        self.assertEqual(original['responses'][0]['timeSeconds'], 1.25)

        page = self.page
        open_file(page, original)
        expect(page.locator('#status')).to_contain_text('Session opened')
        expect(page.locator('#timeline article strong')).to_have_text([
            'Your moment · untimed', 'Listener response · 0:01', 'Your moment · 0:01',
        ])
        self.assertEqual(session_data(export(page)), session_data(original))
        page.locator('#heard').fill('Added after reopening.')
        page.locator('#mark').click()
        appended = export(page)
        new_note = appended['moments'].pop()
        self.assertEqual(new_note['heard'], 'Added after reopening.')
        self.assertIsNone(new_note['timeSeconds'])
        self.assertEqual(session_data(appended), session_data(original))
        local_audio(page)
        page.locator('#audio').evaluate('audio => { audio.currentTime = 2.5 }')
        page.wait_for_function("!document.getElementById('audio').seeking")
        page.locator('#noticed').fill('Timed after reselecting the audio.')
        page.locator('#respond').click()
        continued = export(page)
        self.assertEqual(continued['responses'][-1]['timeSeconds'], 2.5)
        self.assertEqual(continued['song'], original['song'])
        self.assertEqual(self.remote_requests, [])

    def test_invalid_files_and_cancel_preserve_active_work(self):
        page = self.page
        replacement = export(page)
        local_audio(page)
        page.locator('#heard').fill('Existing note')
        page.locator('#mark').click()
        page.locator('#felt').fill('Unsubmitted draft')
        original = session_data(export(page))
        audio_url = page.locator('#audio').get_attribute('src')
        for invalid in (b'{', dict(replacement, schema='future-version'),
                        dict(replacement, responses=[{'timeSeconds': -1}])):
            open_file(page, invalid)
            expect(page.locator('#status')).to_contain_text('current session is intact')
            self.assertEqual(session_data(export(page)), original)
            expect(page.locator('#felt')).to_have_value('Unsubmitted draft')
            self.assertEqual(page.locator('#audio').get_attribute('src'), audio_url)

        page.once('dialog', lambda dialog: dialog.dismiss())
        open_file(page, replacement)
        expect(page.locator('#status')).to_have_text('Kept your current session.')
        self.assertEqual(session_data(export(page)), original)
        expect(page.locator('#felt')).to_have_value('Unsubmitted draft')
        self.assertEqual(page.locator('#audio').get_attribute('src'), audio_url)

        page.once('dialog', lambda dialog: dialog.accept())
        open_file(page, replacement)
        expect(page.locator('#status')).to_contain_text('Session opened')
        expect(page.locator('#felt')).to_have_value('')
        self.assertIsNone(page.locator('#audio').get_attribute('src'))
        self.assertEqual(session_data(export(page)), session_data(replacement))

    def test_preserve_listener_text_and_song_spacing(self):
        page = self.page
        words = ' \t“relief” — Cafe\u0301\n  second line  '
        page.locator('#heard').fill('  \n ')
        page.locator('#mark').click()
        self.assertEqual(export(page)['moments'], [])
        page.locator('#heard').fill(words)
        page.locator('#mark').click()
        page.locator('#noticed').fill(words)
        page.locator('#respond').click()
        page.locator('#song').fill('  Synthetic title  ')
        page.locator('#artist').fill('  Test ensemble  ')
        saved = export(page)
        self.assertEqual(saved['moments'][0]['heard'], words)
        self.assertEqual(saved['responses'][0]['noticed'], words)
        self.assertEqual(saved['song'], {'title': '  Synthetic title  ', 'artist': '  Test ensemble  '})
        saved['moments'][0]['felt'] = '  original\r\nspacing  '
        page.reload()
        open_file(page, saved)
        expect(page.locator('#status')).to_contain_text('Session opened')
        local_audio(page)
        self.assertEqual(session_data(export(page)), session_data(saved))

    def test_reselecting_audio_preserves_an_empty_archived_title(self):
        page = self.page
        saved = export(page)
        open_file(page, saved)
        expect(page.locator('#status')).to_contain_text('Session opened')
        local_audio(page)
        self.assertEqual(session_data(export(page)), session_data(saved))

    def test_latest_file_selection_wins(self):
        page = self.page
        empty = export(page)
        page.evaluate("""() => {
          const original = File.prototype.text;
          File.prototype.text = async function () {
            const contents = await original.call(this);
            if (this.name === 'slow.json') {
              await new Promise(resolve => { window.release = resolve });
              window.slowReadCompleted = true;
            }
            return contents;
          };
        }""")
        open_file(page, dict(empty, song={'title': 'Old selection', 'artist': ''}), 'slow.json')
        page.wait_for_function("typeof window.release === 'function'")
        open_file(page, dict(empty, song={'title': 'Latest selection', 'artist': ''}))
        expect(page.locator('#song')).to_have_value('Latest selection')
        dialogs = []
        def acknowledge(dialog):
            dialogs.append(dialog.message)
            dialog.accept()
        page.on('dialog', acknowledge)
        page.evaluate('() => window.release()')
        page.wait_for_function("window.slowReadCompleted === true")
        self.assertEqual(export(page)['song']['title'], 'Latest selection')
        self.assertEqual(dialogs, [])
