import os
import random
from datetime import datetime, timezone
from beem import Steem
from beem.account import Account
from beem.comment import Comment
from beem.discussions import Discussions_by_created

# =========================================================================
# 1. CONFIGURATION (TUNED FOR SMALL SP CURATION SNIPING)
# =========================================================================
MY_ACCOUNT = "blog.god"
VOTE_WEIGHT = 100.0               # Full 100% weight to clear dust thresholds (~10 votes/day)
MIN_VP_THRESHOLD = 80.0           # Keeps VP regenerating near peak efficiency
MIN_RC_THRESHOLD = 85.3

# Wider post age window (in minutes)
MIN_POST_AGE_MINS = 5.0
MAX_POST_AGE_MINS = 10.0

# Skip posts that ALREADY received a big whale vote (you want to be BEFORE them)
MAX_EXISTING_PAYOUT_SBD = 0.30

# Minimum word count floor
MIN_WORD_COUNT = 15

# How many recent posts to scan
FETCH_LIMIT = 400

BLACKLIST = {MY_ACCOUNT}

# Fast failover node list (skips slow NodeList network benchmark)
NODES = [
    "https://api.moecki.online",
    "https://api.campingclub.me",
    "https://api2.justyy.com",
    "https://api3.justyy.com",
    "https://steem-proxy.gikunju.workers.dev",
]

MY_PRIVATE_POSTING_KEY = os.getenv("STEEM_POSTING_KEY")
if not MY_PRIVATE_POSTING_KEY:
    print("Error: STEEM_POSTING_KEY secret is missing!")
    exit(1)

try:
    stm = Steem(node=NODES, keys=[MY_PRIVATE_POSTING_KEY])
    account_info = Account(MY_ACCOUNT, blockchain_instance=stm)

    # 2. Check Voting Power & Resource Credits
    current_vp = account_info.get_voting_power()
    rc_manabar = account_info.get_rc_manabar()
    current_rc = (rc_manabar["current_mana"] / rc_manabar["max_mana"]) * 100

    print(f"@{MY_ACCOUNT} | VP: {current_vp:.2f}% | RC: {current_rc:.2f}%")

    if current_vp < MIN_VP_THRESHOLD:
        print(f"Safety Halt: VP ({current_vp:.2f}%) below {MIN_VP_THRESHOLD}%. Letting VP recharge.")
        exit(0)

    if current_rc < MIN_RC_THRESHOLD:
        print(f"Safety Halt: RC ({current_rc:.2f}%) below {MIN_RC_THRESHOLD}%.")
        exit(0)

    # 3. Fetch Recent Posts (with fallback if a node caps query limit below 400)
    posts = []
    for limit_try in (FETCH_LIMIT, 200, 100):
        try:
            discussions = Discussions_by_created(
                {"limit": limit_try, "tag": ""}, blockchain_instance=stm
            )
            if discussions is not None:
                posts = list(discussions)
                if posts:
                    print(f"Fetched {len(posts)} posts (requested limit={limit_try}).")
                    break
        except Exception as fetch_err:
            print(f"Warning: Fetch with limit={limit_try} failed: {fetch_err}")

    if not posts:
        print("No posts returned from blockchain query.")
        exit(0)

    now = datetime.now(timezone.utc)
    candidates = []

    stats = {
        "fetched": len(posts),
        "in_age_window": 0,
        "skipped_blacklisted": 0,
        "skipped_age": 0,
        "skipped_payout": 0,
        "skipped_short": 0,
        "skipped_already_voted": 0,
    }

    for post in posts:
        if not post:
            continue

        author = post.get("author")
        permlink = post.get("permlink")
        if not author or not permlink:
            continue

        if author in BLACKLIST:
            stats["skipped_blacklisted"] += 1
            continue

        created = post.get("created")
        if not created:
            stats["skipped_age"] += 1
            continue
        if created.tzinfo is None:
            created = created.replace(tzinfo=timezone.utc)

        age_mins = (now - created).total_seconds() / 60.0
        if age_mins < MIN_POST_AGE_MINS or age_mins > MAX_POST_AGE_MINS:
            stats["skipped_age"] += 1
            continue

        stats["in_age_window"] += 1

        pending_payout = float(post.get("pending_payout_value", 0) or 0)
        if pending_payout > MAX_EXISTING_PAYOUT_SBD:
            stats["skipped_payout"] += 1
            continue

        body = post.get("body", "")
        word_count = len(body.split()) if body else 0
        if word_count < MIN_WORD_COUNT:
            stats["skipped_short"] += 1
            continue

        voters = [v["voter"] for v in post.get("active_votes", []) if "voter" in v]
        if MY_ACCOUNT in voters:
            stats["skipped_already_voted"] += 1
            continue

        candidates.append((age_mins, f"@{author}/{permlink}", word_count, pending_payout))

    print(
        f"[DIAGNOSTICS] Fetched: {stats['fetched']} | "
        f"In {MIN_POST_AGE_MINS}-{MAX_POST_AGE_MINS}m window: {stats['in_age_window']} | "
        f"Candidates: {len(candidates)} | "
        f"Skipped -> age: {stats['skipped_age']}, payout: {stats['skipped_payout']}, "
        f"short(<{MIN_WORD_COUNT}w): {stats['skipped_short']}, "
        f"already_voted: {stats['skipped_already_voted']}, "
        f"blacklisted: {stats['skipped_blacklisted']}"
    )

    if not candidates:
        print(
            f"No valid curation candidates found in the {MIN_POST_AGE_MINS}–{MAX_POST_AGE_MINS} min window."
        )
        exit(0)

    chosen_age, chosen_id, chosen_words, chosen_payout = random.choice(candidates)

    print(
        f"Voting on {chosen_id} | Pool size: {len(candidates)} | "
        f"Age: {chosen_age:.1f}m | Words: {chosen_words} | Payout: ${chosen_payout:.3f}"
    )
    target_comment = Comment(chosen_id, blockchain_instance=stm)
    target_comment.upvote(weight=VOTE_WEIGHT, voter=MY_ACCOUNT)
    print("Upvote successfully broadcasted at 100% weight.")

except Exception as e:
    print(f"CRITICAL ERROR: {e}")
    exit(1)
