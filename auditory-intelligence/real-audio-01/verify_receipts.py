"""Check that permanent case CSV matches freshly executed real-audio case JSON.

Results JSON is produced ONLY after ten actual WAV clips were downloaded and validated.
No test-fixture or mocked-results fallback is permitted.
"""
import csv,hashlib,json
from pathlib import Path

ORIGINAL_JSON_SHA="4ccc41912a9a0ba05790828a989b3efffe8874e873124b479fbc0e5da5c35d0c"
ORIGINAL_CSV_SHA="c5f14b064d8f2d05ea71520c182cdf0fe8e14b4f1d836ec20b0de6b4345b27ad"

def main():
    jf=Path("results.json");cf=Path("receipts/real_case_decisions.csv")
    assert hashlib.sha256(jf.read_bytes()).hexdigest()==ORIGINAL_JSON_SHA,"Original result changed; make new versioned receipt instead of overwriting"
    assert hashlib.sha256(cf.read_bytes()).hexdigest()==ORIGINAL_CSV_SHA,"Case-ledger bytes do not match published source"
    data=json.loads(jf.read_text());rows=list(csv.DictReader(cf.open()))
    assert len(rows)==len(data["rows"])==48
    for i,(saved,new) in enumerate(zip(rows,data["rows"])):
        assert int(saved["source_group"])==new["source_group"],i
        assert saved["slots"]==">".join(new["slot_sources"]),i
        assert float(saved["gain"])==new["gain"],i
        assert int(saved["truth"])==int(new["planted_dog_then_chainsaw"]),i
        for method,prefix in [("energy","energy"),("zcr","zcr"),("multiband","multiband")]:
            assert int(saved[prefix+"_alert"])==int(new["predictions"][method]["matched"]), (i,method)
            if method!="energy":
                assert saved[prefix+"_labels"]==">".join(new["predictions"][method]["labels"]),(i,method)
    for method in ("energy","zcr","multiband"):
        cc=data["methods"][method]
        assert cc["true_A_then_B"]+cc["miss_A_then_B"]==6
        assert cc["false_A_then_B"]+cc["true_no_match"]==42
    print("VERIFIED_FULL_SOURCE_RESULT_HASH_AND_ALL_48_CASE_ROWS")

if __name__=="__main__":main()
