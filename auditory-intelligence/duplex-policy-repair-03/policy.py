"""DUPLEX-POLICY-REPAIR-03: safe mock ledger with separated ingress/control APIs.

Mock labels do NOT establish acoustic origin, addressee, identity or authorization.
HostPort is a TRUST BOUNDARY INTEGRATION CONTRACT, not authentication itself.
All state updates are LOGICAL. No physical actions, audio or model inference.
"""
from __future__ import annotations
from dataclasses import dataclass, field, asdict
from typing import Callable
import math
import re

ORIGINS={'task_user','bystander','assistant_self','echo','unknown'}
ROLES={'authorized','unauthorized','unknown'}
ADDRESSEES={'assistant','other','unknown'}
ECHO={'match','nonmatch','unknown'}
TERMINAL={'COMMITTED','VOID'}
FIELDS={
    'gate':{'left','right'},'valve':{'left','right'},
    'path':{'left','right'},'direction':{'left','right'},
}

@dataclass(frozen=True)
class Speech:
    event_id:str
    revision:int
    observed_ms:int
    available_ms:int
    text:str
    thread_id:str=''
    referent_id:str=''
    observed_origin:str='unknown'
    source_confidence:float=0.
    transcript_confidence:float=0.
    authority:str='unknown'
    addressed_to:str='unknown'
    playback_match:str='unknown'
    quoted:bool=False
    supersedes_txid:str=''

@dataclass
class Transaction:
    id:str
    source_event_id:str
    thread_id:str
    referent_id:str
    field:str
    status:str
    observed_ms:int
    available_ms:int
    updated_ms:int
    proposal:tuple[str,str,str]|None=None
    state_version:int=0
    original_value:str|None=None
    reason:str=''
    supersedes_txid:str=''

@dataclass(frozen=True)
class Action:
    at_ms:int
    kind:str
    id:str
    txid:str=''
    proposal:tuple[str,str,str]|None=None
    reason:str=''


def parse(text:str)->tuple[str,str,str]|None:
    # Deliberately anchored toy grammar: NOT a reliable ASR semantic parser.
    if type(text) is not str or len(text)>256:return None
    t=text.strip().lower().replace('’',"'")
    m=re.fullmatch(r'no,? i meant the (left|right) (gate|valve|path)[.!]?',t)
    if m:return (m.group(2),m.group(1),'')
    m=re.fullmatch(r'no,? i meant (\d{1,4}) trays,? not (\d{1,4})[.!]?',t)
    if m and m.group(1)!=m.group(2) and 1<=int(m.group(1))<=9999 and 1<=int(m.group(2))<=9999:
        return ('trays',str(int(m.group(1))),'not '+str(int(m.group(2))))
    m=re.fullmatch(r"no,? don't turn (left|right);? turn (left|right)[.!]?",t)
    if m and m.group(1)!=m.group(2):return ('direction',m.group(2),'not '+m.group(1))
    return None


def validate_proposal(p):
    if type(p) is not tuple or len(p)!=3 or any(type(x) is not str for x in p):return False
    field,value,rejected=p
    if len(field)>32 or len(value)>64 or len(rejected)>64:return False
    if field=='trays':
        return bool(re.fullmatch(r'[1-9][0-9]{0,3}',value) and re.fullmatch(r'not [1-9][0-9]{0,3}',rejected)) and value!=rejected[4:]
    return field in FIELDS and value in FIELDS[field] and (not rejected or
        (rejected.startswith('not ') and rejected[4:] in FIELDS[field] and rejected[4:]!=value))


def validate_speech(e):
    if type(e) is not Speech:return 'not Speech input'
    if any(type(x) is not str or len(x)>80 for x in (e.event_id,e.thread_id,e.referent_id,e.supersedes_txid)) or not e.event_id:
        return 'invalid identifiers'
    if type(e.text) is not str or len(e.text)>256:return 'text too long/invalid'
    if any(type(x) is not int or x<0 for x in (e.observed_ms,e.available_ms)) or e.available_ms<e.observed_ms:
        return 'invalid observation/delivery clocks'
    if type(e.revision) is not int or not 1<=e.revision<=1000:return 'invalid revision'
    if (any(type(x) is not str for x in (e.observed_origin,e.authority,e.addressed_to,e.playback_match)) or
        e.observed_origin not in ORIGINS or e.authority not in ROLES or
        e.addressed_to not in ADDRESSEES or e.playback_match not in ECHO):
        return 'invalid category'
    if type(e.quoted) is not bool:return 'quoted flag must be boolean'
    for val in (e.source_confidence,e.transcript_confidence):
        if type(val) not in (int,float) or not math.isfinite(val) or not 0<=val<=1:return 'confidence outside finite range'
    return None

class Ledger:
    def __init__(self,initial_state:dict[tuple[str,str],str]|None=None):
        self.latest:dict[str,Speech]={}
        self.transactions:dict[str,Transaction]={}
        self.event_txids:dict[str,str]={}
        self.values:dict[tuple[str,str],str]=dict(initial_state or {})
        self.versions:dict[tuple[str,str],int]={k:0 for k in self.values}
        self.actions:list[Action]=[]
        # Host events are deduplicated across multiple authorized adapters.
        self.clock=-1
        self.host_action_ids:set[str]=set()
        # This object must only be provided to a real host UI boundary, never the microphone/transcript ingress.
        self.__host_secret=object()

    def _emit(self,at,kind,id,txid='',proposal=None,reason=''):
        a=Action(at,kind,id,txid,proposal,reason)
        self.actions.append(a)
        return a

    def _void(self,tx,eid,t,reason):
        if tx.status not in TERMINAL:
            tx.status='VOID';tx.updated_ms=t
            self._emit(t,'RETRACT_PENDING',eid,tx.id,reason=reason)

    def ingest(self,e:Speech)->list[Action]:
        """UNTRUSTED observed speech input. Cannot commit a task-state change."""
        start=len(self.actions)
        reason=validate_speech(e)
        if reason:
            self._emit(getattr(e,'available_ms',0),'ABSTAIN_INVALID_INPUT',getattr(e,'event_id','?'),reason=reason)
            return self.actions[start:]
        if e.available_ms<self.clock:
            self._emit(e.available_ms,'REJECT_TIME_TRAVEL',e.event_id)
            return self.actions[start:]
        self.clock=e.available_ms
        old=self.latest.get(e.event_id)
        if old:
            if e.revision<=old.revision:
                if e.revision==old.revision and e!=old:self._emit(e.available_ms,'REJECT_REVISION_COLLISION',e.event_id)
                return self.actions[start:]
            if (old.observed_ms!=e.observed_ms or old.thread_id!=e.thread_id or
                old.referent_id!=e.referent_id):
                self._emit(e.available_ms,'REJECT_REVISION_IDENTITY_CHANGE',e.event_id)
                return self.actions[start:]
            oldid=self.event_txids.get(e.event_id)
            if oldid:
                tx=self.transactions[oldid]
                if tx.status=='COMMITTED':
                    self._emit(e.available_ms,'REJECT_COMMITTED_REVISION',e.event_id,oldid)
                    return self.actions[start:]
                self._void(tx,e.event_id,e.available_ms,'New transcript revision')
        self.latest[e.event_id]=e
        if e.playback_match=='match' or e.observed_origin in ('echo','assistant_self','bystander'):
            self._emit(e.available_ms,'IGNORE_NON_TASK_SOUND',e.event_id)
            return self.actions[start:]
        if e.quoted:
            self._emit(e.available_ms,'IGNORE_QUOTATION',e.event_id)
            return self.actions[start:]
        value=parse(e.text)
        maybe=bool(re.match(r'^\s*(no\b|not\s)',e.text.lower()))
        if value is None and not maybe:return self.actions[start:]
        field=value[0] if value else ''
        # A referent must be supplied by separate task context; thread ID is NOT a referent.
        if not e.referent_id:
            self._emit(e.available_ms,'ASK_REFERENT',e.event_id,reason='No task referent confirmed')
            return self.actions[start:]
        key=(e.referent_id,field)
        target=None
        if e.supersedes_txid:
            target=self.transactions.get(e.supersedes_txid)
            if (not target or target.status in TERMINAL or target.thread_id!=e.thread_id or
                target.referent_id!=e.referent_id or target.observed_ms>=e.observed_ms):
                self._emit(e.available_ms,'REJECT_INVALID_SUPERSESSION',e.event_id,reason='Explicit link, same referent/thread, increasing observed time required')
                return self.actions[start:]
            # Reject linked supersession with conflicting known field.
            if value and target.field and target.field!=field:
                self._emit(e.available_ms,'REJECT_DIFFERENT_FIELD_SUPERSESSION',e.event_id)
                return self.actions[start:]
            # Link only: do NOT retract the prior transaction on untrusted speech.
            # Retraction is deferred until a separate trusted host confirms this change.
        # No automatic same-thread supersession. Multiple proposals for same (field, referent) may not both proceed.
        if value:
            contenders=[t for t in self.transactions.values() if t.status not in TERMINAL and
                       t.referent_id==e.referent_id and t.field==field and t.source_event_id!=e.event_id]
            if contenders and not e.supersedes_txid:
                self._emit(e.available_ms,'ASK_EXPLICIT_SUPERSESSION',e.event_id,
                           reason='Pending change for same exact referent and field')
                return self.actions[start:]
        status='ASK_TEXT' if value is None or e.transcript_confidence<.8 else 'ASK_SOURCE'
        if value and e.transcript_confidence>=.8 and e.observed_origin=='task_user' and e.source_confidence>=.8 and e.authority=='authorized' and e.addressed_to=='assistant' and e.playback_match=='nonmatch':
            status='AWAIT_CONFIRM'
        txid=f'{e.event_id}@{e.revision}'
        tx=Transaction(txid,e.event_id,e.thread_id,e.referent_id,field,status,e.observed_ms,e.available_ms,e.available_ms,
                       value,self.versions.get(key,0),self.values.get(key),
                       reason='Mock transcript, not trusted evidence',supersedes_txid=e.supersedes_txid)
        self.transactions[txid]=tx;self.event_txids[e.event_id]=txid
        action={'ASK_TEXT':'ASK_TEXT_CLARIFICATION','ASK_SOURCE':'ASK_SOURCE_CONFIRMATION','AWAIT_CONFIRM':'PROPOSE_CHANGE'}[status]
        self._emit(e.available_ms,action,e.event_id,txid,value)
        return self.actions[start:]

    def trusted_host_port(self,authorizer:Callable[[str,str],bool]):
        """Only the trusted host integrator may retain this adapter/authorizer.

        The ledger cannot prove the host is truly authenticated or the UI was actually displayed.
        """
        if not callable(authorizer):raise TypeError('Host authorizer callback required')
        return HostPort(self,self.__host_secret,authorizer)

    def _host_apply(self,secret,op,event_id,at_ms,txid,shown_value,referent_id,expected_current,expected_version,actor):
        if secret is not self.__host_secret:raise PermissionError('Not a host port')
        if type(at_ms) is not int or at_ms<self.clock or type(event_id) is not str or not event_id or len(event_id)>80:
            raise ValueError('Invalid host event ordering')
        if event_id in self.host_action_ids:
            return self._emit(at_ms,'REJECT_DUPLICATE_HOST_ACTION',event_id,txid)
        self.host_action_ids.add(event_id)
        self.clock=at_ms
        if op == 'manual_change':
            # Speech/ASR must never be a prerequisite for a trusted UI edit.
            # Host authentication & display are external, mocked in this DEV.
            if (type(referent_id) is not str or not 1 <= len(referent_id) <= 80
                    or not validate_proposal(shown_value)):
                return self._emit(at_ms,'REJECT_CONTROL_MISMATCH',event_id)
            field,new,rejected=shown_value
            key=(referent_id,field)
            current=self.values.get(key)
            version=self.versions.get(key,0)
            if version!=expected_version or current!=expected_current:
                return self._emit(at_ms,'REJECT_STALE_TASK_STATE',event_id)
            if rejected.startswith('not ') and current!=rejected[4:]:
                return self._emit(at_ms,'REJECT_REJECTED_VALUE_NOT_CURRENT',event_id)
            self.values[key]=new
            self.versions[key]=version+1
            return self._emit(at_ms,'COMMIT_MANUAL_UI_CHANGE',event_id,proposal=shown_value,
                              reason='Host-authored manual change, no acoustic or physical actuation')
        tx=self.transactions.get(txid)
        if tx is None or tx.status in TERMINAL:
            return self._emit(at_ms,'REJECT_STALE_CONTROL',event_id,txid)
        if op=='cancel':
            self._void(tx,event_id,at_ms,'Host-approved cancellation')
            return self.actions[-1]
        if op!='confirm' or tx.proposal is None or tx.status not in ('AWAIT_CONFIRM','ASK_SOURCE'):
            return self._emit(at_ms,'REJECT_UNRESOLVED_CONFIRMATION',event_id,txid)
        if not validate_proposal(shown_value) or shown_value!=tx.proposal or type(referent_id) is not str or referent_id!=tx.referent_id:
            return self._emit(at_ms,'REJECT_CONTROL_MISMATCH',event_id,txid)
        key=(tx.referent_id,tx.field)
        current=self.values.get(key)
        version=self.versions.get(key,0)
        if version!=expected_version or expected_version!=tx.state_version or current!=expected_current or current!=tx.original_value:
            return self._emit(at_ms,'REJECT_STALE_TASK_STATE',event_id,txid)
        field,new,rejected=tx.proposal
        if rejected.startswith('not ') and current!=rejected[4:]:
            return self._emit(at_ms,'REJECT_REJECTED_VALUE_NOT_CURRENT',event_id,txid)
        # A separate trusted host confirmation now authorizes supersession.
        # Check pending target still refers to the same field/referent and predates us.
        target=None
        if tx.supersedes_txid:
            target=self.transactions.get(tx.supersedes_txid)
            if (target is None or target.status in TERMINAL or target.id==tx.id or
                target.field not in ('',tx.field) or target.referent_id!=tx.referent_id or
                target.thread_id!=tx.thread_id or target.observed_ms>=tx.observed_ms):
                return self._emit(at_ms,'REJECT_STALE_SUPERSESSION',event_id,txid)
        self.values[key]=new;self.versions[key]=version+1
        if target is not None:
            self._void(target,event_id,at_ms,'Superseded by separately host-confirmed change')
        tx.status='COMMITTED';tx.updated_ms=at_ms
        return self._emit(at_ms,'COMMIT_LOGICAL_CHANGE',event_id,txid,tx.proposal,
                          'Trusted host asserted reviewed change; no physical action')

    def snapshot(self):
        return {'clock_ms':self.clock,'values':{f'{k[0]}/{k[1]}':v for k,v in sorted(self.values.items())},
                'versions':{f'{k[0]}/{k[1]}':v for k,v in sorted(self.versions.items())},
                'transactions':{k:asdict(v) for k,v in sorted(self.transactions.items())},
                'actions':[asdict(a) for a in self.actions]}

class HostPort:
    """Out-of-band mock integration boundary. Not a credential/security product."""
    def __init__(self,ledger,secret,authorizer):
        self.__ledger=ledger;self.__secret=secret;self.__auth=authorizer

    def _perform(self,op,actor,event_id,at_ms,txid,shown_value,referent_id,expected_current,expected_version):
        if not self.__auth(actor,op):
            return Action(at_ms,'REJECT_UNAUTHORIZED_HOST',event_id,txid)
        result=self.__ledger._host_apply(self.__secret,op,event_id,at_ms,txid,shown_value,referent_id,expected_current,expected_version,actor)
        return result

    def confirm(self,*,actor,event_id,at_ms,txid,shown_value,referent_id,expected_current,expected_version):
        return self._perform('confirm',actor,event_id,at_ms,txid,shown_value,referent_id,expected_current,expected_version)

    def cancel(self,*,actor,event_id,at_ms,txid):
        return self._perform('cancel',actor,event_id,at_ms,txid,None,'',None,0)

    def manual_change(self,*,actor,event_id,at_ms,referent_id,shown_value,expected_current,expected_version):
        """Explicit accessible UI value entry, even if the microphone never hears it."""
        return self._perform('manual_change',actor,event_id,at_ms,'',shown_value,
                             referent_id,expected_current,expected_version)


def replay_speech_only(events:list[Speech],cutoff_ms:int,initial_state=None):
    """Reproduce available mock speech prefix, excluding unpersisted host controls.

    Do NOT use this as crash-recovery logic for approved transactions.
    """
    state=Ledger(initial_state)
    for _,e in sorted(enumerate(events),key=lambda x:(x[1].available_ms,x[0])):
        if e.available_ms>cutoff_ms:break
        state.ingest(e)
    return state.snapshot()
