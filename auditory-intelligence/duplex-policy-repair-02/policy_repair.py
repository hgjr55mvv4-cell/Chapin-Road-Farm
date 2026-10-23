"""DUPLEX-POLICY-REPAIR-02: deterministic event-only correction transactions.

NO AUDIO; source, role, address and echo signals are EXTERNALLY PROVIDED MOCKS.
All tasks require separate explicit user control before commit. No physical action.
"""
from __future__ import annotations
from dataclasses import dataclass, field, asdict
import json
import math
import re

ORIGINS = {'task_user', 'bystander', 'assistant_self', 'echo', 'unknown'}
ROLES = {'authorized', 'unauthorized', 'unknown'}
ADDRESSEES = {'assistant', 'other', 'unknown'}
ECHO = {'match', 'nonmatch', 'unknown'}
KINDS = {'speech', 'confirm', 'cancel'}

@dataclass(frozen=True)
class Input:
    event_id: str
    revision: int
    available_ms: int
    kind: str = 'speech'
    thread_id: str = ''
    text: str = ''
    observed_origin: str = 'unknown'
    source_confidence: float = 0.0
    transcript_confidence: float = 0.0
    authority: str = 'unknown'  # provided by external session ownership, NOT voice
    addressed_to: str = 'unknown'  # source of address evidence separately logged
    playback_match: str = 'unknown'  # externally supplied echo estimate; NOT measured
    quoted: bool = False  # external quote annotation; not reliably supplied by ASR
    resolves_event_id: str = ''
    transaction_id: str = ''
    ui_authorized: bool = False  # explicit out-of-band confirmation/cancel
    confirmed_value: tuple[str, str, str] | None = None  # exact UI-displayed triple

@dataclass
class Tx:
    transaction_id: str
    event_id: str
    thread_id: str
    status: str
    created_ms: int
    updated_ms: int
    proposed: tuple[str, str, str] | None = None
    unresolved_reason: str = ''

@dataclass(frozen=True)
class Action:
    at_ms: int
    kind: str
    event_id: str
    transaction_id: str = ''
    value: tuple[str, str, str] | None = None
    reason: str = ''


def parse_correction(text: str) -> tuple[str, str, str] | None:
    """Small anchored toy grammar; NEVER claim general speech understanding."""
    t = text.strip().lower().replace('’', "'")
    m = re.fullmatch(r'no,? i meant the (left|right) (gate|valve|path)[.!]?', t)
    if m:
        return m.group(2), m.group(1), ''
    m = re.fullmatch(r'no,? i meant (\d+) trays,? not (\d+)[.!]?', t)
    if m and m.group(1) != m.group(2):
        return 'trays', m.group(1), 'not ' + m.group(2)
    m = re.fullmatch(r"no,? don't turn (left|right);? turn (left|right)[.!]?", t)
    if m and m.group(1) != m.group(2):
        return 'direction', m.group(2), 'not ' + m.group(1)
    return None


def likely_correction(text: str) -> bool:
    return bool(re.match(r'^(?:no,? i\b|not\s+(?:twelve|twenty|\d))', text.strip().lower()))


def invalid_input(e: Input) -> str | None:
    if not isinstance(e.event_id, str) or not e.event_id:
        return 'bad event identifier'
    if type(e.available_ms) is not int or e.available_ms < 0 or type(e.revision) is not int or e.revision < 1:
        return 'invalid timestamp or revision'
    if e.kind not in KINDS or e.observed_origin not in ORIGINS or e.authority not in ROLES or e.addressed_to not in ADDRESSEES or e.playback_match not in ECHO:
        return 'invalid categorical field'
    for label, val in [('source_confidence', e.source_confidence), ('transcript_confidence', e.transcript_confidence)]:
        if type(val) not in (int, float) or not math.isfinite(val) or not 0 <= val <= 1:
            return label + ' outside finite [0,1]'
    return None


class Ledger:
    """Append-only observed actions; later transcript revisions cannot rewrite history."""
    def __init__(self):
        self.latest: dict[str, Input] = {}
        self.txs: dict[str, Tx] = {}
        self.event_txs: dict[str, str] = {}
        self.task_state: dict[str, str] = {}
        self.actions: list[Action] = []
        self.clock_ms: int = -1

    def _emit(self, e: Input, kind: str, txid='', value=None, reason=''):
        action = Action(e.available_ms, kind, e.event_id, txid, value, reason)
        self.actions.append(action)
        return action

    def _new_tx(self, e: Input, status: str, reason: str, proposed=None):
        txid = f'{e.event_id}@{e.revision}'
        tx = Tx(txid, e.event_id, e.thread_id, status, e.available_ms, e.available_ms, proposed, reason)
        self.txs[txid] = tx
        self.event_txs[e.event_id] = txid
        return tx

    def _void(self, txid: str, e: Input, reason: str):
        tx = self.txs.get(txid)
        if tx and tx.status not in ('COMMITTED', 'VOID'):
            tx.status = 'VOID'
            tx.updated_ms = e.available_ms
            self._emit(e, 'RETRACT_PENDING', txid, reason=reason)

    def consume(self, e: Input) -> list[Action]:
        start = len(self.actions)
        if e.available_ms < self.clock_ms:
            raise ValueError('Time-travel input; replay the ordered event log')
        self.clock_ms = e.available_ms
        failure = invalid_input(e)
        if failure:
            self._emit(e, 'ABSTAIN_INVALID_INPUT', reason=failure)
            return self.actions[start:]
        old = self.latest.get(e.event_id)
        if old and e.revision == old.revision:
            if e != old:
                self._emit(e, 'REJECT_REVISION_COLLISION', reason='Same version, conflicting payload')
            # Identical deliveries are fully idempotent.
            return self.actions[start:]
        if old and e.revision < old.revision:
            return self.actions[start:]
        if old:
            old_tx = self.event_txs.get(e.event_id)
            if old_tx:
                self._void(old_tx, e, 'Transcript revised; prior proposal not confirmed')
            # Revisions to already confirmed changes cannot retroactively edit them.
            if old_tx and self.txs[old_tx].status == 'COMMITTED':
                self._emit(e, 'REJECT_COMMITTED_REVISION', old_tx)
                return self.actions[start:]
        self.latest[e.event_id] = e

        if e.kind in ('confirm', 'cancel'):
            tx = self.txs.get(e.transaction_id)
            if not e.ui_authorized or e.authority != 'authorized':
                self._emit(e, 'REJECT_UNAUTHORIZED_CONTROL', e.transaction_id)
            elif not tx or tx.status not in ('AWAIT_CONFIRM', 'ASK_SOURCE', 'ASK_TEXT', 'ASK_SUPERSESSION'):
                self._emit(e, 'REJECT_STALE_CONTROL', e.transaction_id)
            elif e.kind == 'cancel':
                self._void(tx.transaction_id, e, 'Explicitly cancelled by authorized UI control')
            elif tx.status not in ('AWAIT_CONFIRM', 'ASK_SOURCE') or tx.proposed is None:
                self._emit(e, 'REJECT_UNRESOLVED_CONFIRMATION', tx.transaction_id)
            elif e.confirmed_value != tx.proposed:
                self._emit(e, 'REJECT_CONFIRM_VALUE_MISMATCH', tx.transaction_id,
                           reason='UI must affirm exact field, new value, and rejected value')
            else:
                field, new_value, _ = tx.proposed
                self.task_state[field] = new_value
                tx.status = 'COMMITTED'
                tx.updated_ms = e.available_ms
                self._emit(e, 'COMMIT_UI_CONFIRMED', tx.transaction_id, tx.proposed,
                           'No physical action; task ledger value only')
            return self.actions[start:]

        # A verified playback echo beats even a high-confidence wrong speaker tag.
        if e.playback_match == 'match' or e.observed_origin in ('bystander','assistant_self','echo'):
            self._emit(e, 'IGNORE_NON_TASK_SOUND', reason='Known irrelevant source or matched playback')
            return self.actions[start:]
        if e.quoted:
            self._emit(e, 'IGNORE_QUOTATION', reason='Quote flag supplied by scenario, not inferred from ASR')
            return self.actions[start:]

        parsed = parse_correction(e.text)
        if parsed is None and not likely_correction(e.text):
            return self.actions[start:]

        # Newer complete correction supersedes an earlier unresolved correction
        # only with *explicit* transaction link or the same externally assigned thread.
        if e.resolves_event_id:
            previous = self.event_txs.get(e.resolves_event_id)
            if previous:
                self._void(previous, e, 'Explicit resolution/supersession reference')
            else:
                self._emit(e, 'ASK_SUPERSESSION', reason='Resolution target was not found')
                return self.actions[start:]
        elif e.thread_id:
            # A complete correction can resolve ASK_TEXT/ASK_SOURCE within same thread,
            # but must not silently override an unconfirmed complete proposal.
            for old_tx in list(self.txs.values()):
                if old_tx.thread_id == e.thread_id and old_tx.status not in ('COMMITTED', 'VOID'):
                    if parsed and old_tx.status in ('ASK_SOURCE', 'ASK_TEXT'):
                        self._void(old_tx.transaction_id, e, 'Later complete correction in same thread')
                    elif old_tx.event_id != e.event_id:
                        tx = self._new_tx(e, 'ASK_SUPERSESSION', 'Older pending complete change requires explicit resolution')
                        self._emit(e, 'ASK_SUPERSESSION', tx.transaction_id)
                        return self.actions[start:]
        if parsed is None or e.transcript_confidence < .8:
            tx = self._new_tx(e, 'ASK_TEXT', 'Incomplete or low-confidence text')
            self._emit(e, 'ASK_TEXT_CLARIFICATION', tx.transaction_id)
        elif (e.observed_origin != 'task_user' or e.source_confidence < .8
              or e.authority != 'authorized' or e.addressed_to != 'assistant'
              or e.playback_match != 'nonmatch'):
            tx = self._new_tx(e, 'ASK_SOURCE', 'Source, role, address, or playback still uncertain', parsed)
            self._emit(e, 'ASK_SOURCE_CONFIRMATION', tx.transaction_id)
        else:
            tx = self._new_tx(e, 'AWAIT_CONFIRM', 'Structured proposal; human UI confirmation required', parsed)
            self._emit(e, 'PROPOSE_CHANGE', tx.transaction_id, parsed)
        return self.actions[start:]

    def pending(self):
        return [asdict(tx) | {'age_ms':self.clock_ms-tx.created_ms}
                for tx in self.txs.values() if tx.status not in ('COMMITTED','VOID')]

    def snapshot(self):
        return {'clock_ms':self.clock_ms,'task_state':dict(self.task_state),
                'transactions':{k:asdict(v) for k,v in sorted(self.txs.items())},
                'pending':self.pending(),
                'actions':[asdict(a) for a in self.actions]}


def replay(inputs: list[Input] | tuple[Input,...], cutoff_ms: int) -> dict:
    """Causally replay an event log: no future event or revision may enter state."""
    state=Ledger()
    for _,e in sorted(enumerate(inputs),key=lambda p:(p[1].available_ms,p[0])):
        if e.available_ms > cutoff_ms:break
        state.consume(e)
    return state.snapshot()


def from_json_lines(path: str):
    with open(path, encoding='utf-8') as handle:
        return [Input(**json.loads(x)) for x in handle if x.strip()]
