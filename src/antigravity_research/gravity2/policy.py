"""Immutable GRAVITY2-00 policy and historical science-reference locks.

The 1.5429 J capacity is NOT powered-source energy. Historical numbers here
are protected comparison anchors, NOT results re-derived by this miner.
"""

PROGRAM = "GRAVITY2-R3B-ACTIONMINER"
SCHEMA = "gravity2.v1"

# Seconds, soft process-tree RSS MiB, persistent per-run MiB.
PRESETS = {
    "quick": (60, 384, 4),
    "short": (180, 640, 8),
    "focused": (300, 768, 12),
    "extended": (900, 1536, 30),
}

GLOBAL_MIB = 200
SCRATCH_MIB = 32
LOG_MAX_BYTES = 65536

# Mandatory source-code SHA locks, from the GRAVITY2 build plan.
# Missing or changed files are never silently accepted.
PARENTS = {
    "R3B_ORIGINAL": (
        "src/antigravity_research/agminer/"
        "hook17_fdual_f_global_mirror_prefight.py",
        "aa8f196fcae6a63405181ca62674e22ac67e5da88303759bdd99d25716fa2263",
    ),
    "R3B_LOADED": (
        "src/antigravity_research/agminer/"
        "hook17_f2_strong_payload_loading_rescue.py",
        "e1296794c25a4d0e4d5634c7e7d543a0b488b8d2a1963afcf7878bea1c1b99e7",
    ),
    "DELTA1_02": (
        "src/antigravity_research/delta1/"
        "delta1_02_r3b_portal_rank.py",
        "04d8d669adb1e4b067e75a285dd13f0fbaa6bbd879090b88e850a277baca9395",
    ),
}

# Later results are optional during installation.
# They are matched by exact SHA, not by newest filename.
OPTIONAL_RESULTS = {
    "F0C": (
        "delta1_f0c_*",
        "science.json",
        "3c671e54a44a23bd12d2fe2451aed6388bb3c4f6da37408d7abe54c808540f7f",
    ),
    "F0D": (
        "delta1_f0d_*",
        "science.json",
        "2db67eea46adf84327c14c0177c1863148893217a377ac67a1f3a39ec9cb6465",
    ),
    "F0E_R1": (
        "delta1_f0e_r1_*",
        "science.json",
        "bdc6d1b27befa108cc982d392e8bf265c17b96f814f54810d49b180d0dc834d4",
    ),
    "F0F": (
        "delta1_f0f_*",
        "science.json",
        "145f7db67b440cbd5e5f0c2023ccb1ac7ad9d2151b777f459e1c2fc3964c9e73",
    ),
    "F0G": (
        "delta1_f0g_*",
        "science.json",
        "c8e74278c73b4d74f43560f7dec275c8061ef3f83c33d52afe703a7360a91c1f",
    ),
}

ANCHORS = {
    "prescribed_mixed_field_capacity_j": 1.5429162116460216,
    "historical_preloaded_min_acceleration_m_s2": 9.80665,
    "historical_preloaded_energy_j_approx": 1.537764,
    "historical_loaded_min_acceleration_m_s2": -129.67185782242464,
    "historical_loaded_field_energy_j": 1.5211390382733165,
    "006D_coefficient": 23.591586299249,
}

GATES = [
    "G00_PARENT",
    "G01_ACTION",
    "G02_VARIATION",
    "G03_WARD",
    "G04_HEALTH",
    "G05_SOURCE",
    "G06_LOAD",
    "G07_METRIC",
    "G08_ENERGY",
    "G09_EXTERIOR",
    "G10_REACTION",
    "G11_REALISM",
]

HISTORICAL_FAILURES = [
    "R3X1 loaded -129.67185782242464 m/s2 at h=0.05 m",
    "R3A ordinary material suppression 1.84e15",
    "DELTA1-02 F_Y^2 rank independent fraction 0.159%-0.176%",
    "B6 corrected original boundary/source artifact",
    "B11-B13 source, interface and causal-response failures",
    "B14/B16 -410.388913 m/s2 inward hotspot NONCONVERGED",
    "B15 rotation-only rescue failed in tested scope",
    "B16 weak-loading rescue failed in tested scope",
    "F0D quadratic uniform mode unstable (scoped)",
    "F0F metric-independent theta F_X wedge F_Y: zero DIRECT Hilbert stress",
    "F0G isolated exterior dipole: inward at >=1m, NOT complete stress",
]
