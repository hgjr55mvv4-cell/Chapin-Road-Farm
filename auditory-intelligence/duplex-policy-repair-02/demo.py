"""Deterministic toy scenarios illustrating repaired, unverified interaction policy."""
import json
from policy_repair import Input, Ledger


def speech(eid, t, text, thread='case', **more):
    values=dict(event_id=eid,revision=1,available_ms=t,kind='speech',thread_id=thread,
                text=text,observed_origin='task_user',source_confidence=.99,
                transcript_confidence=.99,authority='authorized',addressed_to='assistant',
                playback_match='nonmatch')
    values.update(more)
    return Input(**values)


def ui(eid, t, txid, expected):
    return Input(eid,1,t,'confirm',authority='authorized',transaction_id=txid,
                 ui_authorized=True,confirmed_value=expected)


def run():
    scenarios={
        'earlier_partial_then_complete':[speech('partial',100,'No, I...',thread='gate',transcript_confidence=.2),
                   speech('complete',300,'No, I meant the right gate',thread='gate')],
        'echo_false_task_user_playback_matched':[speech('echo',100,'No, I meant the right gate',
                        playback_match='match')],
        'confident_echo_bad_evidence':[speech('echo',100,'No, I meant the right gate',
                        playback_match='nonmatch')],
        'unknown_source_clear_text':[speech('unknown',100,'No, I meant the right gate',
                        observed_origin='unknown',source_confidence=.15)],
        'bad_confidence':[speech('nan',100,'No, I meant the right gate',
                        source_confidence=float('nan'))],
        'two_changes':[speech('gate',100,'No, I meant the right gate',thread='gate'),
                       speech('trays',300,'No, I meant 12 trays, not 20',thread='trays')],
    }
    output={}
    for name,events in scenarios.items():
        led=Ledger()
        for event in events:led.consume(event)
        if name=='unknown_source_clear_text':
            tx=led.event_txs['unknown']
            led.consume(ui('human_confirm',200,tx,('gate','right','')))
        elif name=='two_changes':
            led.consume(ui('human_gate_ok',400,led.event_txs['gate'],('gate','right','')))
            led.consume(ui('human_trays_ok',500,led.event_txs['trays'],('trays','12','not 20')))
        output[name]={
          'actions':[a.kind for a in led.actions],
          'pending_count':len(led.pending()),
          'logical_task_state':led.task_state,
          'physical_actions':0,
          'externally_supplied_mock_labels':True,
        }
    return {'version':'DUPLEX-POLICY-REPAIR-02','status':'EXPOSED_MOCK_ONLY',
            'no_audio_or_model_inference':True,'case_count':len(output),'cases':output}


if __name__=='__main__':
    print(json.dumps(run(),indent=2,allow_nan=False))
