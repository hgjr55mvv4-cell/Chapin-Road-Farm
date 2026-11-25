# One listener moment, two readings

Open [the single-file demo](index.html) locally in a browser. The included [two-second sample](example.wav) has a 330 Hz tone, a pause at 1.2 seconds, and a 440 Hz tone. Both the scene and the collaborators are fictional.

The listener wrote **“That pause felt like relief.”** Rowan reads hesitation into the pause. Jules reads the listener’s words and disagrees. An older response also mentions the passage. Its timestamp gives no information about who wrote it or whether they listened. The two scripted replies are marked as examples in the downloaded data as well as on screen.

| Contributor | Material available for this reply | Listening evidence |
|---|---|---|
| Earlier v0.1 respondent | Unknown | Unknown |
| Rowan | Direct audio available | Explicit self-report in the fictional example |
| Jules | Session JSON only | Unknown |

## Try a handoff

1. Open the page and select **Save original session JSON**. Open that download in the demo to start from the legacy session alone. The earlier response stays unattributed.
2. Enter an alias, choose the listener moment, select the sample WAV, and add an interpretation. Selecting the file makes its audio available once the browser reads its metadata. Even pressing Play leaves listening unknown. The optional checkbox records only the named contributor’s self-report for that passage.
3. Select **Save handoff JSON**. Open another copy of the page offline and select the handoff file. The previous replies retain their evidence labels. The new contributor starts with JSON alone. Append a different reading and save again.

The packet contains the original v0.1 session object and a separate list of replies. Each reply names the contributor and points to a moment by its zero-based index in that enclosed source. The original-session download recovers the source field values, including whitespace and Unicode in listener text. JSON indentation or escaping can differ from the input file. Existing Listening Room readers can use the original-session download; the demo reads both file formats.

The evidence label describes access in the current reply view. A displayed alias is a declaration. The page cannot identify who was at the device, verify the selected audio matches the passage, or authenticate hearing. Audio bytes, local filenames and playback telemetry are excluded from handoff downloads. The packet format is experimental.

## Replay the browser test

From this directory, with Python Playwright and Chromium available, run:

```sh
python3 -m unittest -v test_handoff
```

Set `HARBOR_CHROMIUM` to the executable path to use a system Chromium. The test uses a native Listening Room export, the generated WAV, and isolated offline browser contexts. It checks exact source recovery, listening claims after selection and playback, disagreement linked to the same moment, malformed packet rejection, and separation of the next contributor’s evidence.
