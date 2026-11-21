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
MIN_VP_THRESHOLD = 65.0           # Keeps VP regenerating near peak efficiency
MIN_RC_THRESHOLD = 83.0

# Optimal post age window (in minutes):
# Clears the 5-minute reverse-auction penalty while beating late whale votes
MIN_POST_AGE_MINS = 5.3
MAX_POST_AGE_MINS = 6.3

# Skip posts that ALREADY received a big whale vote (you want to be BEFORE them)
MAX_EXISTING_PAYOUT_SBD = 0.30

# High-value communities & tags actively curated by @booming / @steemcurator accounts
TARGET_TAGS = {
    "steemexclusive", "thediarygame", "bangla", "burnsteem25",
    "club5050", "club75", "club100", "newcomers", "kr", "crypto", "krsuccess", "nigeria"
}

BLACKLIST = {MY_ACCOUNT}

# Fast failover node list (skips slow NodeList network benchmark)
NODES = [
    "https://api.moecki.online",
    "https://api.campingclub.me",
    "https://api2.justyy.com",
    "https://api3.justyy.com",
    "https://steem-proxy.gikunju.workers.dev"
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

    # 3. Fetch Recent Posts
    discussions = Discussions_by_created({"limit": 100, "tag": ""}, blockchain_instance=stm)
    now = datetime.now(timezone.utc)
    candidates = []

    for post in discussions:
        author = post.get("author")
        permlink = post.get("permlink")
        if not author or not permlink or author in BLACKLIST:
            continue

        # Check age window strictly (both min AND max age)
        created = post.get("created")
        if not created:
            continue
        if created.tzinfo is None:
            created = created.replace(tzinfo=timezone.utc)

        age_mins = (now - created).total_seconds() / 60.0
        if age_mins < MIN_POST_AGE_MINS or age_mins > MAX_POST_AGE_MINS:
            continue

        # Skip if a whale has already voted on it
        pending_payout = float(post.get("pending_payout_value", 0))
        if pending_payout > MAX_EXISTING_PAYOUT_SBD:
            continue

        # Check spam / quality length (at least 120 words for curated posts)
        body = post.get("body", "")
        word_count = len(body.split()) if body else 0
        if word_count < 120:
            continue

        # Check if already voted
        voters = [v["voter"] for v in post.get("active_votes", []) if "voter" in v]
        if MY_ACCOUNT in voters:
            continue

        # Match against target tags (any non-blacklisted author)
        post_tags = {t.lower() for t in post.get("tags", [])}
        matching_tags = post_tags.intersection(TARGET_TAGS)

        if not matching_tags:
            continue

        candidates.append((age_mins, f"@{author}/{permlink}", list(matching_tags)))

    if not candidates:
        print(
            f"No valid curation candidates found in the {MIN_POST_AGE_MINS}–{MAX_POST_AGE_MINS} min window."
        )
        exit(0)

    # Pick a random post among all valid matching candidates
    chosen_age, chosen_id, chosen_tags = random.choice(candidates)

    print(
        f"Voting on {chosen_id} | Pool size: {len(candidates)} | Age: {chosen_age:.1f}m | Tags: {chosen_tags}"
    )
    target_comment = Comment(chosen_id, blockchain_instance=stm)
    target_comment.upvote(weight=VOTE_WEIGHT, voter=MY_ACCOUNT)
    print("Upvote successfully broadcasted at 100% weight.")

except Exception as e:
    print(f"CRITICAL ERROR: {e}")
    exit(1)
