"""Synthetic demonstration for PAC-01-DEV-01.

Shows (1) a successful balanced comparison and (2) a deliberately
failed comparison construction. All data is fictional. Mock ranking
results below are NOT scientific evidence about music, preference, or
either condition -- they only exercise the harness machinery.

Run:  python3 demo.py
"""

from pac01_harness import (
    InsufficientBalance, ObservationState, Pilot, build_comparison,
    build_ranking, demo_catalog, mock_a1_ranking, mock_b_ranking,
)


def main():
    catalog = demo_catalog()
    print(f"Catalog: {len(catalog)} fictional recordings, "
          f"snapshot {catalog.snapshot_id}")
    a = mock_a1_ranking(catalog, ["synthetic folk"])
    b = mock_b_ranking(catalog, ["synthetic folk"])
    print(f"A1 top-8:         {list(a.ranked_ids)}")
    print(f"B-metadata top-8: {list(b.ranked_ids)}")

    comp = build_comparison(catalog, a, b, seed=11)
    print("\n--- Successful comparison ---")
    print(f"Queue (condition-labelled, researcher view): {list(comp.queue_ids)}")
    print(f"Shared (both conditions, stored once): {list(comp.shared_ids())}")
    print(f"A1-unique: {list(comp.unique_ids('A1'))}")
    print(f"B-unique:  {list(comp.unique_ids('B-metadata'))}")
    print(f"Listener view (no condition labels): {list(comp.listener_view())}")
    print(f"Dropped by artist cap: {list(comp.dropped_due_to_cap)}")
    print(f"Unbalanced remainder: {list(comp.unbalanced_remainder)}")

    pilot = Pilot(catalog)
    session = pilot.new_session("demo-session", comp)
    # Simulated reports: only heard songs get keep/pass labels.
    for rid in comp.unique_ids("A1"):
        session.record(rid, ObservationState.KEPT_AFTER_LISTENING,
                       heard_enough=True, replay_desire=True)
    for rid in comp.unique_ids("B-metadata"):
        session.record(rid, ObservationState.PASSED_AFTER_LISTENING,
                       heard_enough=True)
    for rid in comp.shared_ids()[:1]:
        session.record(rid, ObservationState.MAYBE)
    print("\nBinary summary (unique heard songs only; shared excluded):")
    for condition, values in session.binary_summary().items():
        print(f"  {condition}: {values}")
    print("Note: these counts describe mock rankings over fictional "
          "recordings. They prove the machinery runs, nothing more.")

    print("\n--- Deliberately failed comparison ---")
    try:
        build_comparison(
            catalog,
            build_ranking("A1", list(a.ranked_ids), catalog.snapshot_id,
                          "ctx", ["synthetic folk"], "v1", "demo"),
            build_ranking("B-metadata", list(a.ranked_ids),
                          catalog.snapshot_id, "ctx", ["synthetic folk"],
                          "v1", "demo"),
            seed=11)
    except InsufficientBalance as exc:
        print(f"INSUFFICIENT_BALANCE (expected): {exc}")

    pilot.delete_all()
    print("\nSessions after delete_all:", pilot.sessions)


if __name__ == "__main__":
    main()
