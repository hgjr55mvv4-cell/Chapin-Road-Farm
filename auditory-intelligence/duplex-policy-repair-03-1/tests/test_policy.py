import copy, math, pathlib, sys, unittest
sys.path.insert(0,str(pathlib.Path(__file__).resolve().parents[1]))
from policy import Speech,Ledger,HostPort,parse,validate_proposal,replay_speech_only

def speech(id='e1', t=200, text='No, I meant the right gate', **kw):
    d=dict(event_id=id,revision=1,observed_ms=t-100,available_ms=t,text=text,thread_id='session1',
           referent_id='north_gate',observed_origin='task_user',source_confidence=.99,
           transcript_confidence=.99,authority='authorized',addressed_to='assistant',playback_match='nonmatch',quoted=False)
    d.update(kw)
    return Speech(**d)
def host(ledger):return ledger.trusted_host_port(lambda actor,op:actor=='verified_user' and op in ('confirm','cancel','manual_change'))
def confirm(port,tx,event_id='click',at_ms=500,proposed=('gate','right',''),expected_current='left',expected_version=0):
    return port.confirm(actor='verified_user',event_id=event_id,at_ms=at_ms,txid=tx,
                        shown_value=proposed,referent_id='north_gate',expected_current=expected_current,expected_version=expected_version)
class Tests(unittest.TestCase):
    def test01_parse_anchored(self):
        self.assertEqual(parse('No, I meant the right gate'),('gate','right',''))
        self.assertIsNone(parse('He said "No, I meant the right gate"'))
        self.assertIsNone(parse('No, I meant the right gate and then drive away'))
    def test02_quantity_bounded(self):
        self.assertEqual(parse('No I meant 12 trays, not 20'),('trays','12','not 20'))
        self.assertIsNone(parse('No I meant 10000 trays, not 20'))
    def test03_negation(self):
        self.assertEqual(parse("No, don't turn left; turn right"),('direction','right','not left'))
    def test04_no_ingress_commit_api(self):
        l=Ledger({('north_gate','gate'):'left'});r=l.ingest(speech())
        self.assertEqual(r[0].kind,'PROPOSE_CHANGE');self.assertEqual(l.values[('north_gate','gate')],'left')
        with self.assertRaises(TypeError):speech(kind='confirm')
    def test05_untrusted_boolean_cannot_inject(self):
        with self.assertRaises(TypeError):speech(ui_authorized=True)
    def test06_real_mock_host_confirmation(self):
        l=Ledger({('north_gate','gate'):'left'});t=l.ingest(speech())[0].txid
        self.assertEqual(confirm(host(l),t).kind,'COMMIT_LOGICAL_CHANGE')
        self.assertEqual(l.values[('north_gate','gate')],'right')
    def test07_untrusted_host_denied(self):
        l=Ledger({('north_gate','gate'):'left'});t=l.ingest(speech())[0].txid
        p=l.trusted_host_port(lambda actor,op:False)
        r=p.confirm(actor='forged',event_id='click',at_ms=500,txid=t,
                    shown_value=('gate','right',''),referent_id='north_gate',expected_current='left',expected_version=0)
        self.assertEqual(r.kind,'REJECT_UNAUTHORIZED_HOST');self.assertEqual(l.values[('north_gate','gate')],'left')
    def test08_confident_mislabeled_echo_proposal_still_possible(self):
        l=Ledger({('north_gate','gate'):'left'})
        r=l.ingest(speech(observed_origin='task_user',playback_match='nonmatch'))
        self.assertEqual(r[0].kind,'PROPOSE_CHANGE')
        self.assertEqual(l.values[('north_gate','gate')],'left')
    def test09_quote_flag_blocks(self):
        l=Ledger();self.assertEqual(l.ingest(speech(quoted=True))[0].kind,'IGNORE_QUOTATION')
    def test10_malformed_quote_flag_rejected(self):
        l=Ledger();self.assertEqual(l.ingest(speech(quoted='false'))[0].kind,'ABSTAIN_INVALID_INPUT')
    def test11_nonfinite_confidence(self):
        for v in (float('nan'),float('inf'),-float('inf'),-0.1,1.1):
            for field in ('source_confidence','transcript_confidence'):
                with self.subTest(v=v,field=field):
                    self.assertEqual(Ledger().ingest(speech(**{field:v}))[0].kind,'ABSTAIN_INVALID_INPUT')
    def test12_delivery_before_observed(self):
        self.assertEqual(Ledger().ingest(speech(observed_ms=400))[0].kind,'ABSTAIN_INVALID_INPUT')
    def test13_missing_referent_refuses_proposal(self):
        self.assertEqual(Ledger().ingest(speech(referent_id=''))[0].kind,'ASK_REFERENT')
    def test14_same_thread_distinct_referents_separate(self):
        l=Ledger();l.ingest(speech('a',200,referent_id='north_gate'))
        r=l.ingest(speech('b',300,referent_id='south_gate'))
        self.assertEqual(r[0].kind,'PROPOSE_CHANGE');self.assertEqual(len(l.transactions),2)
    def test15_conflict_same_referent_field_blocks(self):
        l=Ledger();l.ingest(speech('a',200))
        self.assertEqual(l.ingest(speech('b',300))[0].kind,'ASK_EXPLICIT_SUPERSESSION')
    def test16_explicit_supersession_requires_newer_observation(self):
        l=Ledger();l.ingest(speech('a',300))
        r=l.ingest(speech('b',350,supersedes_txid='a@1',observed_ms=150))
        self.assertEqual(r[0].kind,'REJECT_INVALID_SUPERSESSION')
        self.assertEqual(l.transactions['a@1'].status,'AWAIT_CONFIRM')
    def test17_explicit_supersession_newer_observation_works(self):
        l=Ledger();l.ingest(speech('a',200))
        r=l.ingest(speech('b',300,text='No, I meant the left gate',supersedes_txid='a@1'))
        self.assertEqual([x.kind for x in r],['PROPOSE_CHANGE'])
        self.assertEqual(l.transactions['a@1'].status,'AWAIT_CONFIRM')
    def test18_wrong_referent_supersession_rejected(self):
        l=Ledger();l.ingest(speech('a',200))
        r=l.ingest(speech('b',300,referent_id='south_gate',supersedes_txid='a@1'))
        self.assertEqual(r[0].kind,'REJECT_INVALID_SUPERSESSION')
    def test19_field_swap_supersession_rejected(self):
        l=Ledger();l.ingest(speech('a',200))
        r=l.ingest(speech('b',300,text='No, I meant the right path',supersedes_txid='a@1'))
        self.assertEqual(r[0].kind,'REJECT_DIFFERENT_FIELD_SUPERSESSION')
    def test20_incomplete_then_explicit_completion(self):
        l=Ledger();l.ingest(speech('a',200,text='No, I...'))
        r=l.ingest(speech('b',300,supersedes_txid='a@1'))
        self.assertEqual([x.kind for x in r],['PROPOSE_CHANGE'])
        self.assertEqual(l.transactions['a@1'].status,'ASK_TEXT')
    def test21_unrelated_event_leaves_pending(self):
        l=Ledger();l.ingest(speech('a',200,text='No, I...'))
        self.assertEqual(l.ingest(speech('b',300,text='nice weather')),[])
        self.assertEqual(l.transactions['a@1'].status,'ASK_TEXT')
    def test22_source_uncertainty_can_be_manually_corrected(self):
        l=Ledger({('north_gate','gate'):'left'});r=l.ingest(speech(source_confidence=.2,observed_origin='unknown'))
        self.assertEqual(r[0].kind,'ASK_SOURCE_CONFIRMATION')
        self.assertEqual(confirm(host(l),r[0].txid).kind,'COMMIT_LOGICAL_CHANGE')
        # Deliberately permits an independently reviewed manual correction even if speech source unknown.
    def test23_stale_task_version_rejected(self):
        l=Ledger({('north_gate','gate'):'left'});tx=l.ingest(speech())[0].txid
        l.values[('north_gate','gate')]='right';l.versions[('north_gate','gate')]=1
        self.assertEqual(confirm(host(l),tx).kind,'REJECT_STALE_TASK_STATE')
    def test24_rejected_value_requires_current_state(self):
        l=Ledger({('north_gate','trays'):'30'})
        tx=l.ingest(speech(text='No, I meant 12 trays, not 20'))[0].txid
        p=l.trusted_host_port(lambda actor,op:True)
        out=p.confirm(actor='verified_user',event_id='confirm',at_ms=500,txid=tx,referent_id='north_gate',
                      shown_value=('trays','12','not 20'),expected_current='30',expected_version=0)
        self.assertEqual(out.kind,'REJECT_REJECTED_VALUE_NOT_CURRENT')
    def test25_duplicate_speech_idempotent(self):
        l=Ledger();e=speech();l.ingest(e)
        self.assertEqual(l.ingest(e),[])
    def test26_collision_different_payload(self):
        l=Ledger();l.ingest(speech())
        self.assertEqual(l.ingest(speech(text='No, I meant the left gate'))[0].kind,'REJECT_REVISION_COLLISION')
    def test27_revision_not_retroactive_and_voids(self):
        l=Ledger();l.ingest(speech());r=l.ingest(speech(revision=2,available_ms=500))
        self.assertEqual([a.kind for a in r],['RETRACT_PENDING','PROPOSE_CHANGE'])
        self.assertEqual(l.transactions['e1@1'].status,'VOID')
    def test28_revision_cannot_mutate_observation_identity(self):
        l=Ledger();l.ingest(speech());r=l.ingest(speech(revision=2,available_ms=500,referent_id='south_gate'))
        self.assertEqual(r[0].kind,'REJECT_REVISION_IDENTITY_CHANGE')
    def test29_revision_cannot_rewrite_committed(self):
        l=Ledger({('north_gate','gate'):'left'});tx=l.ingest(speech())[0].txid
        confirm(host(l),tx)
        self.assertEqual(l.ingest(speech(revision=2,available_ms=600))[0].kind,'REJECT_COMMITTED_REVISION')
    def test30_prefix_replay_deterministic(self):
        inputs=[speech('first',200,text='No, I...'),speech('second',500,supersedes_txid='first@1')]
        def replay(prefix):
            l=Ledger();[l.ingest(x) for x in prefix];return l.snapshot()
        self.assertEqual(replay(inputs[:1]),replay([inputs[0]]))
        self.assertNotEqual(replay(inputs),replay(inputs[:1]))
    def test31_cancel_only_via_host(self):
        l=Ledger();tx=l.ingest(speech())[0].txid
        out=host(l).cancel(actor='verified_user',event_id='cancel',at_ms=500,txid=tx)
        self.assertEqual(out.kind,'RETRACT_PENDING');self.assertEqual(l.transactions[tx].status,'VOID')
    def test32_old_commit_not_in_future(self):
        l=Ledger({('north_gate','gate'):'left'})
        l.ingest(speech());pre=copy.deepcopy(l.snapshot())
        tx='e1@1';confirm(host(l),tx)
        self.assertEqual(pre['values']['north_gate/gate'],'left')
    def test33_competing_revisions_are_deterministic(self):
        l=Ledger();l.ingest(speech())
        self.assertEqual(l.ingest(speech(revision=2,available_ms=100))[0].kind,'REJECT_TIME_TRAVEL')
    def test34_validation_no_unbounded_text(self):
        self.assertEqual(Ledger().ingest(speech(text='No '+('x'*500)))[0].kind,'ABSTAIN_INVALID_INPUT')
    def test35_validation_proposal_whitelist(self):
        self.assertFalse(validate_proposal(('gate','<script>','')))
        self.assertFalse(validate_proposal(('trays','-2','not 20')))
        self.assertTrue(validate_proposal(('trays','12','not 20')))
    def test36_false_negative_echo_tag_not_committed(self):
        l=Ledger({('north_gate','gate'):'left'});l.ingest(speech(observed_origin='task_user',playback_match='nonmatch'))
        self.assertEqual(l.values[('north_gate','gate')],'left')
    def test37_wrong_referral_ignored(self):
        l=Ledger();self.assertEqual(l.ingest(speech(observed_origin='bystander'))[0].kind,'IGNORE_NON_TASK_SOUND')
    def test38_untrusted_helper_input_type_rejected(self):
        l=Ledger();self.assertEqual(l.ingest({'event_id':'e1','ui_authorized':True})[0].kind,'ABSTAIN_INVALID_INPUT')
    def test39_unknown_playback_asks(self):
        self.assertEqual(Ledger().ingest(speech(playback_match='unknown'))[0].kind,'ASK_SOURCE_CONFIRMATION')
    def test41_cross_host_ports_one_click_is_idempotent(self):
        l=Ledger({('north_gate','gate'):'left'});tx=l.ingest(speech())[0].txid
        a=confirm(host(l),tx,event_id='ui-1')
        b=confirm(host(l),tx,event_id='ui-1',at_ms=600)
        self.assertEqual(a.kind,'COMMIT_LOGICAL_CHANGE')
        self.assertEqual(b.kind,'REJECT_DUPLICATE_HOST_ACTION')
    def test42_unhashable_category_rejected_not_crash(self):
        l=Ledger();self.assertEqual(l.ingest(speech(authority=[]))[0].kind,'ABSTAIN_INVALID_INPUT')
    def test43_identical_prefix_and_replay(self):
        shared=speech('first',200,text='No, I...')
        a=speech('later',500,supersedes_txid='first@1')
        b=speech('later',500,text='No, I meant the left gate',supersedes_txid='first@1')
        for cutoff in (0,199,200,499):
            self.assertEqual(replay_speech_only([shared,a],cutoff),replay_speech_only([shared,b],cutoff))
        self.assertNotEqual(replay_speech_only([shared,a],500),replay_speech_only([shared,b],500))
    def test44_two_successive_values_same_referent_have_versions(self):
        l=Ledger({('north_gate','gate'):'left'});p=host(l)
        first=l.ingest(speech('first',200))[0].txid
        r=p.confirm(actor='verified_user',event_id='ui1',at_ms=500,txid=first,shown_value=('gate','right',''),
                    referent_id='north_gate',expected_current='left',expected_version=0)
        self.assertEqual(r.kind,'COMMIT_LOGICAL_CHANGE')
        second=l.ingest(speech('second',600,text='No, I meant the left gate'))[0].txid
        r=p.confirm(actor='verified_user',event_id='ui2',at_ms=700,txid=second,shown_value=('gate','left',''),
                    referent_id='north_gate',expected_current='right',expected_version=1)
        self.assertEqual(r.kind,'COMMIT_LOGICAL_CHANGE')
        self.assertEqual(l.values[('north_gate','gate')],'left')
        self.assertEqual(l.versions[('north_gate','gate')],2)
    def test40_natural_quotation_ambiguity_remains(self):
        l=Ledger();r=l.ingest(speech())
        self.assertEqual(r[0].kind,'PROPOSE_CHANGE')  # Unflagged literal quote can look identical.
        self.assertEqual(l.values,{})

    def test45_two_host_ports_share_dedupe_across_adapters(self):
        l=Ledger({('north_gate','gate'):'left'});tx=l.ingest(speech())[0].txid
        self.assertEqual(confirm(host(l),tx).kind,'COMMIT_LOGICAL_CHANGE')
        self.assertEqual(confirm(host(l),tx).kind,'REJECT_DUPLICATE_HOST_ACTION')
        self.assertEqual(l.values[('north_gate','gate')],'right')

    def test46_manual_ui_without_sound_is_accessible(self):
        l=Ledger({('north_gate','gate'):'left'});p=host(l)
        r=p.manual_change(actor='verified_user',event_id='manual1',at_ms=200,
            referent_id='north_gate',shown_value=('gate','right',''),expected_current='left',expected_version=0)
        self.assertEqual(r.kind,'COMMIT_MANUAL_UI_CHANGE')
        self.assertEqual(l.values[('north_gate','gate')],'right')

    def test47_manual_not_authorized_rejected(self):
        l=Ledger({('north_gate','gate'):'left'});p=host(l)
        r=p.manual_change(actor='untrusted_audio',event_id='manual1',at_ms=200,
            referent_id='north_gate',shown_value=('gate','right',''),expected_current='left',expected_version=0)
        self.assertEqual(r.kind,'REJECT_UNAUTHORIZED_HOST')
        self.assertEqual(l.values[('north_gate','gate')],'left')

    def test48_manual_stale_task_version_rejected(self):
        l=Ledger({('north_gate','gate'):'left'});p=host(l)
        r=p.manual_change(actor='verified_user',event_id='manual1',at_ms=200,
            referent_id='north_gate',shown_value=('gate','right',''),expected_current='left',expected_version=1)
        self.assertEqual(r.kind,'REJECT_STALE_TASK_STATE')
        self.assertEqual(l.values[('north_gate','gate')],'left')

    def test49_manual_quantity_rejected_current_mismatch(self):
        l=Ledger({('bedA','trays'):'30'});p=host(l)
        r=p.manual_change(actor='verified_user',event_id='manual1',at_ms=200,
            referent_id='bedA',shown_value=('trays','12','not 20'),expected_current='30',expected_version=0)
        self.assertEqual(r.kind,'REJECT_REJECTED_VALUE_NOT_CURRENT')

    def test50_manual_illegal_value_and_referent_rejected(self):
        for ref,value in [('north_gate',('gate','<script>','')),('',('gate','right',''))]:
            l=Ledger();p=host(l)
            r=p.manual_change(actor='verified_user',event_id='manual',at_ms=200,
                referent_id=ref,shown_value=value,expected_current=None,expected_version=0)
            self.assertEqual(r.kind,'REJECT_CONTROL_MISMATCH')
            self.assertEqual(l.values,{})

    def test51_no_confirm_via_untrusted_speech_event(self):
        l=Ledger({('north_gate','gate'):'left'});tx=l.ingest(speech())[0].txid
        o=l.ingest({'kind':'confirm','event_id':'click','txid':tx,'ui_authorized':True})
        self.assertEqual(o[0].kind,'ABSTAIN_INVALID_INPUT')
        self.assertEqual(l.values[('north_gate','gate')],'left')

    def test52_rejected_host_control_id_cannot_be_reused(self):
        l=Ledger({('north_gate','gate'):'left'});tx=l.ingest(speech())[0].txid
        p=host(l)
        r=p.confirm(actor='verified_user',event_id='same',at_ms=500,txid=tx,
          shown_value=('gate','wrong',''),referent_id='north_gate',expected_current='left',expected_version=0)
        self.assertEqual(r.kind,'REJECT_CONTROL_MISMATCH')
        self.assertEqual(confirm(p,tx,event_id='same',at_ms=600).kind,'REJECT_DUPLICATE_HOST_ACTION')
        self.assertEqual(l.values[('north_gate','gate')],'left')

    def test53_two_pending_tasks_different_referents_host_updates_separately(self):
        l=Ledger({('north_gate','gate'):'left',('south_gate','gate'):'left'})
        tx1=l.ingest(speech('a',200,referent_id='north_gate'))[0].txid
        tx2=l.ingest(speech('b',300,referent_id='south_gate'))[0].txid
        p=host(l)
        self.assertEqual(confirm(p,tx1,event_id='c1',at_ms=400).kind,'COMMIT_LOGICAL_CHANGE')
        r=p.confirm(actor='verified_user',event_id='c2',at_ms=500,txid=tx2,
            shown_value=('gate','right',''),referent_id='south_gate',expected_current='left',expected_version=0)
        self.assertEqual(r.kind,'COMMIT_LOGICAL_CHANGE')
        self.assertEqual(l.values[('south_gate','gate')],'right')

    def test55_unknown_source_link_cannot_retract_existing_proposal(self):
        l=Ledger({('north_gate','gate'):'left'});l.ingest(speech('good',200))
        x=l.ingest(speech('bad',300,observed_origin='unknown',authority='unauthorized',
                          source_confidence=.1,supersedes_txid='good@1'))
        self.assertEqual([r.kind for r in x],['ASK_SOURCE_CONFIRMATION'])
        self.assertEqual(l.transactions['good@1'].status,'AWAIT_CONFIRM')
        self.assertEqual(l.values[('north_gate','gate')],'left')
    def test56_linked_change_voids_original_only_after_host_confirm(self):
        l=Ledger({('north_gate','gate'):'left'});l.ingest(speech('good',200))
        proposal=l.ingest(speech('later',300,text='No, I meant the left gate',supersedes_txid='good@1'))
        self.assertEqual(proposal[0].kind,'PROPOSE_CHANGE')
        self.assertEqual(l.transactions['good@1'].status,'AWAIT_CONFIRM')
        port=host(l)
        result=port.confirm(actor='verified_user',event_id='approve',at_ms=350,txid='later@1',
                            shown_value=('gate','left',''),referent_id='north_gate',
                            expected_current='left',expected_version=0)
        self.assertEqual(result.kind,'COMMIT_LOGICAL_CHANGE')
        self.assertEqual(l.transactions['good@1'].status,'VOID')
    def test57_reject_linked_commit_after_target_committed(self):
        l=Ledger({('north_gate','gate'):'left'});l.ingest(speech('good',200))
        l.ingest(speech('later',300,text='No, I meant the left gate',supersedes_txid='good@1'))
        p=host(l)
        p.confirm(actor='verified_user',event_id='approve_old',at_ms=400,txid='good@1',
                  shown_value=('gate','right',''),referent_id='north_gate',
                  expected_current='left',expected_version=0)
        result=p.confirm(actor='verified_user',event_id='approve_new',at_ms=500,txid='later@1',
                         shown_value=('gate','left',''),referent_id='north_gate',
                         expected_current='right',expected_version=1)
        self.assertIn(result.kind,('REJECT_STALE_TASK_STATE','REJECT_STALE_SUPERSESSION'))
    def test54_one_false_proposal_cannot_mutate_task_without_host_port(self):
        l=Ledger({('north_gate','gate'):'left'})
        r=l.ingest(speech(observed_origin='task_user',playback_match='nonmatch'))
        self.assertEqual(r[0].kind,'PROPOSE_CHANGE')
        self.assertEqual(l.values[('north_gate','gate')],'left')
        self.assertEqual(l.host_action_ids,set())

if __name__=='__main__':unittest.main()
