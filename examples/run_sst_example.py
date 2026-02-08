"""
Example: Running the SST Protocol on a sample claim.

This script demonstrates how to use the Socratic Stress Test
to classify a claim through the full 7-step methodology.
"""

from sst.core.protocol import SSTProtocol


def main():
    # --- Example 1: Claim with sources (should classify as FACT or HYP) ---
    print("=" * 60)
    print("EXAMPLE 1: Claim with sources")
    print("=" * 60)

    protocol = SSTProtocol(mode="basic")

    statement = "Water boils at 100 degrees Celsius at sea level."
    sources = [
        "CRC Handbook of Chemistry and Physics, 97th Edition",
        "NIST Standard Reference Database",
    ]

    report = protocol.run_full_protocol(statement, sources, coherence_score=90.0)

    print(f"Claim   : {report['claim']}")
    print(f"Label   : {report['full_analysis']['step5']['label']}")
    print(f"Confidence: {report['full_analysis']['step6']['confidence']}")
    print(f"Steps   : {len(report['steps_completed'])}")
    print()

    # --- Example 2: Claim without sources (should downgrade) ---
    print("=" * 60)
    print("EXAMPLE 2: Claim without sources")
    print("=" * 60)

    protocol2 = SSTProtocol(mode="deep-auto")

    statement2 = "Dark matter constitutes 27% of the universe."
    sources2 = []

    report2 = protocol2.run_full_protocol(statement2, sources2, coherence_score=60.0)

    print(f"Claim   : {report2['claim']}")
    print(f"Label   : {report2['full_analysis']['step5']['label']}")
    print(f"Confidence: {report2['full_analysis']['step6']['confidence']}")
    print(f"Steps   : {len(report2['steps_completed'])}")
    print()

    # --- Example 3: Vague claim (should classify as UNK) ---
    print("=" * 60)
    print("EXAMPLE 3: Vague claim")
    print("=" * 60)

    protocol3 = SSTProtocol(mode="deep-ask")

    statement3 = "Some people say that coffee is bad for you."
    sources3 = []

    report3 = protocol3.run_full_protocol(statement3, sources3, coherence_score=30.0)

    print(f"Claim   : {report3['claim']}")
    print(f"Label   : {report3['full_analysis']['step5']['label']}")
    print(f"Confidence: {report3['full_analysis']['step6']['confidence']}")
    print(f"Steps   : {len(report3['steps_completed'])}")


if __name__ == "__main__":
    main()