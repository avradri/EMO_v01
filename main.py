"""
EMO v0.1 main script.

This script:
- Loads data from the `data/` folder.
- Computes:
    - Organismality Index (OI)
    - Synergy / O-information-like indicator
    - Global Workspace Ignition (GWI)
    - Self-Model Fidelity (SMF)
    - Information-time (τ_I)
- Prints summary results to the console.

You can later extend it to produce plots, figures, or write to files.
"""

import textwrap

import matplotlib.pyplot as plt

from emo import data_sources, organismality, synergy, gwi, smf, info_time


def print_header(title: str) -> None:
    print("\n" + "=" * 80)
    print(title)
    print("=" * 80)


def run_organismality() -> None:
    print_header("Organismality Index (OI)")

    treaties_df = data_sources.load_treaties()
    conflict_df = data_sources.load_conflict()

    if treaties_df is None or conflict_df is None:
        print("[WARN] Missing treaties or conflict CSVs. Skipping OI.")
        return

    result = organismality.compute_organismality(treaties_df, conflict_df)

    if result.latest_value is None:
        print("[WARN] Could not compute OI (no overlapping years).")
        return

    print(f"Latest OI (World): {result.latest_value:.3f}")
    if result.trend_20y_slope is not None:
        print(f"20-year trend (slope per year): {result.trend_20y_slope:.4f}")
    else:
        print("20-year trend: not enough data.")

    # Simple OI plot
    df = result.series
    if not df.empty:
        plt.figure()
        plt.plot(df["year"], df["oi"], marker="o")
        plt.title("Organismality Index (OI) over time")
        plt.xlabel("Year")
        plt.ylabel("OI")
        plt.grid(True)
        plt.tight_layout()
        plt.show()


def run_synergy() -> None:
    print_header("Synergy / O-information-like indicator")

    news_df, pubs_df, conflict_df = data_sources.load_synergy_streams()

    if news_df is None or pubs_df is None:
        print("[WARN] Missing news or publications CSVs. Skipping synergy.")
        return

    result = synergy.compute_synergy_gaussian(news_df, pubs_df, conflict_df)

    if result.synergy_index is None:
        print("[WARN] Could not compute synergy index (insufficient or degenerate data).")
        return

    print(f"Gaussian synergy-like index: {result.synergy_index:.4f}")
    print(f"Streams used: {', '.join(result.used_columns)}")


def run_gwi() -> None:
    print_header("Global Workspace Ignition (GWI)")

    news_df, wiki_df = data_sources.load_gwi_streams()

    if news_df is None or wiki_df is None:
        print("[WARN] Missing GWI streams (news or Wikipedia). Skipping GWI.")
        return

    result = gwi.compute_gwi(news_df, wiki_df)

    if result is None:
        print("[WARN] Could not compute GWI (no overlap or empty data).")
        return

    print(f"Ignition percentile threshold: {result.threshold:.4f}")
    print(f"Number of ignition events: {len(result.ignition_events)}")

    if not result.ignition_events.empty:
        print("Sample ignition events (first 5):")
        print(result.ignition_events.head()[["date", "ignition"]])


def run_smf() -> None:
    print_header("Self-Model Fidelity (SMF)")

    target_df = data_sources.load_co2_target()
    actual_df = data_sources.load_co2_actual()

    if target_df is None or actual_df is None:
        print("[WARN] Missing CO₂ target or actual CSVs. Skipping SMF.")
        return

    result = smf.compute_smf(target_df, actual_df)

    if result.global_smf is None:
        print("[WARN] Could not compute SMF (no overlap).")
        return

    print(f"Global SMF score: {result.global_smf:.3f}")
    if result.correlation is not None:
        print(f"Correlation between target and actual: {result.correlation:.3f}")
    else:
        print("Correlation: not enough data.")


def run_info_time() -> None:
    print_header("Information-time (τ_I)")

    skill_df = data_sources.load_ecmwf_skill()
    if skill_df is None:
        print("[WARN] Missing ECMWF skill CSV. Skipping τ_I.")
        return

    result = info_time.compute_info_time(skill_df)

    if result.tau_span is None or result.calendar_span is None:
        print("[WARN] Could not compute τ_I (insufficient data).")
        return

    print(f"Calendar span: {result.calendar_span:.1f} years")
    print(f"Information-time span: {result.tau_span:.4f}")
    if result.accel_ratio is not None:
        print(f"Acceleration factor (τ_I / calendar): {result.accel_ratio:.4f}")
    else:
        print("Acceleration factor: undefined (calendar span <= 0).")


def main() -> None:
    print(
        textwrap.dedent(
            """
            EMO v0.1 – Emergent Mind Observatory prototype

            This script computes five basic vital signs for humanity as an emergent mind,
            using simple metrics and CSV-based data sources. For a first run, you can
            start with small, hand-crafted datasets in the `data/` folder, then
            progressively replace them with real OWID, GDELT, OpenAlex, Wikipedia, and
            ECMWF data.
            """
        )
    )

    run_organismality()
    run_synergy()
    run_gwi()
    run_smf()
    run_info_time()


if __name__ == "__main__":
    main()
