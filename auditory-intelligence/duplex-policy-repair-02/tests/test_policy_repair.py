import math
import sys
import unittest
from pathlib import Path
sys.path.insert(0,str(Path(__file__).resolve().parents[1]))
from policy_repair import Input,Ledger,replay,parse_correction


def speech(id, t, text='No, I meant the right gate', **kw):
    d={'event_id':id,'revision':1,'available_ms':t,'text':text,'thread_id':id,
       'observed_origin':'task_user','source_confidence':.99,
       'transcript_confidence':.99,'authority':'authorized',
       'addressed_to':'assistant','playback_match':'nonmatch'}
    d.update(kw)
    return Input(**d)


def ui(id,t,tx,kind='confirm',confirmed_value=('gate','right',''),**kw):
    return Input(event_id=id,revision=1,available_ms=t,kind=kind,
                 authority='authorized',ui_authorized=True,transaction_id=tx,
                 confirmed_value=confirmed_value,**kw)


class RepairTests(unittest.TestCase):
    def test_01_anchored_negation_and_quantity(self):
        self.assertEqual(parse_correction('No, I meant 12 trays, not 20'),('trays','12','not 20'))
        self.assertEqual(parse_correction("No, don't turn left; turn right"),('direction','right','not left'))
        self.assertIsNone(parse_correction('Don\'t change the twenty'))
        self.assertIsNone(parse_correction('Not twelve—twenty'))

    def test_02_proposal_cannot_commit_without_ui(self):
        s=Ledger();r=s.consume(speech('a',100))
        self.assertEqual(r[0].kind,'PROPOSE_CHANGE')
        self.assertFalse(s.task_state)
        self.assertEqual(s.pending()[0]['status'],'AWAIT_CONFIRM')

    def test_03_explicit_commit_stays_logical_only(self):
        s=Ledger();tx=s.consume(speech('a',100))[0].transaction_id
        self.assertEqual(s.consume(ui('click',130,tx))[0].kind,'COMMIT_UI_CONFIRMED')
        self.assertEqual(s.task_state['gate'],'right')
        self.assertFalse(s.pending())

    def test_04_unauthorized_control_cannot_commit(self):
        s=Ledger();tx=s.consume(speech('a',100))[0].transaction_id
        c=Input('button',1,120,'confirm',authority='unauthorized',ui_authorized=True,transaction_id=tx)
        self.assertEqual(s.consume(c)[0].kind,'REJECT_UNAUTHORIZED_CONTROL')
        self.assertEqual(s.task_state,{})

    def test_05_incomplete_then_complete_same_thread_resolves(self):
        s=Ledger();s.consume(speech('first',100,'No, I...',thread_id='gate_session',transcript_confidence=.6))
        actions=s.consume(speech('second',230,'No, I meant the right gate',thread_id='gate_session'))
        self.assertEqual([x.kind for x in actions],['RETRACT_PENDING','PROPOSE_CHANGE'])
        self.assertEqual(len(s.pending()),1)
        self.assertEqual(s.pending()[0]['event_id'],'second')

    def test_06_earlier_uncertain_source_does_not_block_later(self):
        s=Ledger();a=s.consume(speech('first',100,thread_id='north',observed_origin='unknown',source_confidence=.2))
        self.assertEqual(a[0].kind,'ASK_SOURCE_CONFIRMATION')
        b=s.consume(speech('later',200,thread_id='east'))
        self.assertEqual(b[0].kind,'PROPOSE_CHANGE')
        self.assertEqual(len(s.pending()),2)

    def test_07_old_proposal_same_thread_requires_supersession(self):
        s=Ledger();s.consume(speech('one',100,thread_id='shared'))
        x=s.consume(speech('two',200,'No, I meant the left gate',thread_id='shared'))
        self.assertEqual(x[0].kind,'ASK_SUPERSESSION')
        self.assertEqual(s.txs['one@1'].status,'AWAIT_CONFIRM')
        self.assertEqual(s.txs['two@1'].status,'ASK_SUPERSESSION')

    def test_08_explicit_resolution_can_replace_uncommitted(self):
        s=Ledger();s.consume(speech('one',100,thread_id='shared'))
        acts=s.consume(speech('two',200,'No, I meant the left gate',thread_id='shared',resolves_event_id='one'))
        self.assertEqual([x.kind for x in acts],['RETRACT_PENDING','PROPOSE_CHANGE'])
        self.assertEqual(s.txs['one@1'].status,'VOID')

    def test_09_unrelated_speech_does_not_consume_pending(self):
        s=Ledger();s.consume(speech('one',100,'No, I...',transcript_confidence=.4))
        self.assertEqual(s.consume(speech('chatter',150,'The weather changed',thread_id='weather')),[])
        self.assertEqual(s.txs['one@1'].status,'ASK_TEXT')
        self.assertEqual(s.consume(speech('second',200))[0].kind,'PROPOSE_CHANGE')

    def test_10_duplicate_delivery_idempotent(self):
        s=Ledger();e=speech('one',100)
        s.consume(e);self.assertEqual(s.consume(e),[])
        self.assertEqual(len(s.actions),1)

    def test_11_collision_same_version_rejected(self):
        s=Ledger();s.consume(speech('one',100))
        r=s.consume(speech('one',150,'No, I meant the left gate'))
        self.assertEqual(r[0].kind,'REJECT_REVISION_COLLISION')

    def test_12_revision_retracts_pending_no_rewrite(self):
        s=Ledger();s.consume(speech('one',100))
        old=speech('one',300,'No, I meant the left gate',revision=2)
        r=s.consume(old)
        self.assertEqual([x.kind for x in r],['RETRACT_PENDING','PROPOSE_CHANGE'])
        self.assertEqual(s.actions[0].value,('gate','right',''))
        self.assertEqual(s.txs['one@1'].status,'VOID')

    def test_13_revision_cannot_rewrite_committed(self):
        s=Ledger();tx=s.consume(speech('one',100))[0].transaction_id
        s.consume(ui('ok',200,tx))
        r=s.consume(speech('one',300,'No, I meant the left gate',revision=2))
        self.assertEqual(r[0].kind,'REJECT_COMMITTED_REVISION')
        self.assertEqual(s.task_state['gate'],'right')

    def test_14_cancel_pending(self):
        s=Ledger();tx=s.consume(speech('one',100))[0].transaction_id
        self.assertEqual(s.consume(ui('cancel',220,tx,kind='cancel'))[0].kind,'RETRACT_PENDING')
        self.assertEqual(s.consume(ui('too_late',240,tx))[0].kind,'REJECT_STALE_CONTROL')

    def test_15_two_successive_changes_distinct_threads(self):
        s=Ledger();a=s.consume(speech('g1',100,thread_id='g'))[0].transaction_id
        s.consume(ui('ok1',150,a))
        b=s.consume(speech('g2',230,'No, I meant 12 trays, not 20',thread_id='trays'))[0].transaction_id
        s.consume(ui('ok2',290,b,confirmed_value=('trays','12','not 20')))
        self.assertEqual(s.task_state,{'gate':'right','trays':'12'})
        self.assertEqual([a.kind for a in s.actions].count('COMMIT_UI_CONFIRMED'),2)

    def test_16_nan_and_infinity_rejected(self):
        for value in (float('nan'),float('inf'),-float('inf'),-0.1,1.01):
            for key in ('source_confidence','transcript_confidence'):
                with self.subTest(value=value,key=key):
                    s=Ledger();r=s.consume(speech('bad',100,**{key:value}))
                    self.assertEqual(r[0].kind,'ABSTAIN_INVALID_INPUT')
                    self.assertFalse(s.pending())

    def test_17_verified_playback_match_suppresses_wrong_source(self):
        s=Ledger();r=s.consume(speech('echo',100,observed_origin='task_user',source_confidence=.99,playback_match='match'))
        self.assertEqual(r[0].kind,'IGNORE_NON_TASK_SOUND')
        self.assertEqual(s.task_state,{})

    def test_18_unknown_playback_blocks_false_authority(self):
        s=Ledger();r=s.consume(speech('echo',100,observed_origin='task_user',source_confidence=.99,playback_match='unknown'))
        self.assertEqual(r[0].kind,'ASK_SOURCE_CONFIRMATION')

    def test_19_source_role_addressee_are_distinct(self):
        for kw in ({'authority':'unknown'}, {'authority':'unauthorized'},{'addressed_to':'other'},
                   {'addressed_to':'unknown'},{'observed_origin':'unknown'}, {'source_confidence':.6}):
            s=Ledger();r=s.consume(speech('u',100,**kw))
            self.assertEqual(r[0].kind,'ASK_SOURCE_CONFIRMATION')
            self.assertEqual(s.task_state,{})

    def test_20_quotes_are_not_actions_given_explicit_quote_flag(self):
        s=Ledger();r=s.consume(speech('q',100,'No, I meant the right gate',quoted=True))
        self.assertEqual(r[0].kind,'IGNORE_QUOTATION')
        self.assertEqual(s.task_state,{})

    def test_21_identical_prefixes_equal_even_if_future_differs(self):
        common=speech('shared',100,'No, I...',transcript_confidence=.4,thread_id='g')
        right=speech('late',600,'No, I meant the right gate',thread_id='g')
        left=speech('late',600,'No, I meant the left gate',thread_id='g')
        for t in (0,100,200,599):
            self.assertEqual(replay([common,right],t),replay([common,left],t))
        self.assertNotEqual(replay([common,right],600),replay([common,left],600))

    def test_22_restart_from_prefix_identical(self):
        events=[speech('first',100,'No, I...',transcript_confidence=.2,thread_id='g'),
                speech('second',220,'No, I meant the right gate',thread_id='g')]
        for t in (0,100,219,220):
            x=replay(events,t)
            self.assertEqual(x,replay(events[:1 if t<220 else 2],t))

    def test_23_revision_arrives_later_no_early_revision_effect(self):
        first=speech('one',100)
        new=speech('one',500,'No, I meant the left gate',revision=2)
        self.assertEqual(replay([first,new],300),replay([first],300))
        self.assertNotEqual(replay([first,new],500),replay([first],500))

    def test_24_pending_duration_measured_as_pending_not_safe(self):
        s=Ledger();s.consume(speech('one',100,'No, I...',transcript_confidence=.3))
        s.consume(speech('unrelated',1_000_000,'All done'))
        self.assertEqual(s.pending()[0]['age_ms'],999900)
        self.assertEqual(s.txs['one@1'].status,'ASK_TEXT')


    def test_25_unknown_source_explicit_ui_confirm_exact_content(self):
        s=Ledger()
        r=s.consume(speech('uncertain',100,observed_origin='unknown',source_confidence=.22))
        self.assertEqual(r[0].kind,'ASK_SOURCE_CONFIRMATION')
        tx=r[0].transaction_id
        self.assertEqual(s.consume(ui('ack',140,tx,confirmed_value=('gate','right','')))[0].kind,
                         'COMMIT_UI_CONFIRMED')
        self.assertEqual(s.task_state,{'gate':'right'})

    def test_26_ui_mismatched_value_does_not_commit(self):
        s=Ledger();tx=s.consume(speech('p',100))[0].transaction_id
        r=s.consume(ui('wrong',200,tx,confirmed_value=('gate','left','')))
        self.assertEqual(r[0].kind,'REJECT_CONFIRM_VALUE_MISMATCH')
        self.assertEqual(s.task_state,{})
        self.assertEqual(s.txs[tx].status,'AWAIT_CONFIRM')

    def test_27_low_confidence_text_cannot_be_ui_auto_confirmed(self):
        s=Ledger();tx=s.consume(speech('p',100,transcript_confidence=.2))[0].transaction_id
        self.assertEqual(s.consume(ui('click',200,tx))[0].kind,'REJECT_UNRESOLVED_CONFIRMATION')

    def test_28_no_real_world_actuator_command(self):
        s=Ledger();tx=s.consume(speech('one',100))[0].transaction_id
        s.consume(ui('confirmation',130,tx))
        self.assertEqual(s.task_state,{'gate':'right'})
        allowed={'PROPOSE_CHANGE','COMMIT_UI_CONFIRMED','RETRACT_PENDING','ASK_SOURCE_CONFIRMATION',
                 'ASK_TEXT_CLARIFICATION','ASK_SUPERSESSION','IGNORE_NON_TASK_SOUND',
                 'IGNORE_QUOTATION','ABSTAIN_INVALID_INPUT','REJECT_UNAUTHORIZED_CONTROL',
                 'REJECT_STALE_CONTROL','REJECT_UNRESOLVED_CONFIRMATION',
                 'REJECT_REVISION_COLLISION','REJECT_COMMITTED_REVISION','REJECT_CONFIRM_VALUE_MISMATCH'}
        self.assertTrue(set(a.kind for a in s.actions).issubset(allowed))

if __name__ == '__main__':unittest.main()
