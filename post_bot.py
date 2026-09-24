import os
import random
import time
from datetime import datetime, timezone
from beem import Steem
from beem.comment import Comment
from beem.discussions import Discussions_by_created

# =========================================================================
# INITIAL RAMP-UP VARIANCE DELAY (60 seconds to 15 minutes)
# =========================================================================
# 60 seconds = 1 minute | 900 seconds = 15 minutes
delay_seconds = random.randint(60, 900)
print(f"[DELAY LOGIC] Sleeping for {delay_seconds} seconds ({delay_seconds / 60:.1f} minutes) before starting script...")
time.sleep(delay_seconds)
print("[DELAY LOGIC] Delay cleared. Initializing Steem interaction.")

# 1. Configuration
MY_ACCOUNT = "blog.god"            # Your Steem account name
VOTE_WEIGHT = 1                   # Strategically hardcoded to 3% for high-volume growth
PROXY_URL = "https://steem-proxy.gikunju.workers.dev"
random_minutes = random.uniform(5.1, 25.0)
AGE_THRESHOLD_SECONDS = random_minutes * 60
print(f"Looking for posts older than {random_minutes:.1f} minutes but younger than 25.0 minutes.")

# TARGET_TAGS: The script will only look at posts containing any of these tags
TARGET_TAGS = ["xrp", "solana", "usdt", "blockchain", "trading", "steemitchallenge", "newcomers", "creativity", "steemexclusive", "art", "newcomer", "nigeria", "krsuccess", "creative", "trading", "bitcoin", "blog", "creative", "crypto", "steem", "photography", "game"]

# 2. Extract Key from GitHub Secrets
MY_PRIVATE_POSTING_KEY = os.getenv("STEEM_POSTING_KEY")

if not MY_PRIVATE_POSTING_KEY:
    print("Error: STEEM_POSTING_KEY secret is missing!")
    exit(1)

try:
    print(f"Connecting to node via proxy: {PROXY_URL}")
    stm = Steem(node=[PROXY_URL], keys=[MY_PRIVATE_POSTING_KEY])
    
    # =========================================================================
    # LIVE VOTING POWER & RESOURCE CREDIT SAFETY CHECKS
    # =========================================================================
    from beem.account import Account
    account_info = Account(MY_ACCOUNT, blockchain_instance=stm)
    
    # 1. Fetch Voting Power
    current_vp = account_info.get_voting_power()
    print(f"Account @{MY_ACCOUNT} live Voting Power: {current_vp:.2f}%")
    
    # 2. Fetch Resource Credits Percentage
    rc_manabar = account_info.get_rc_manabar()
    current_rc = (rc_manabar['current_mana'] / rc_manabar['max_mana']) * 100
    print(f"Account @{MY_ACCOUNT} live Resource Credits: {current_rc:.2f}%")
    
    # 3. Enforce Safeguards
    if current_vp < 80.0:
        print(f"⚠️ Safety Halt: Voting Power is too low ({current_vp:.2f}%). Skipping execution.")
        exit(0)
        
    if current_rc < 75.0:
        print(f"⚠️ Safety Halt: Resource Credits are too low ({current_rc:.2f}%). Skipping execution to avoid transaction failure.")
        exit(0)
    # =========================================================================

    print("Fetching the latest posts globally from the blockchain history...")

    query = {"limit": 70, "tag": ""}
    discussions = Discussions_by_created(query, blockchain_instance=stm)
    
    upvote_done = False
    
    for post in discussions:
        author = post.get("author")
        permlink = post.get("permlink")
        identifier = f"@{author}/{permlink}"
        
        # --- TAG FILTER LOGIC ---
        post_tags = post.get("tags", [])
        
        matching_tags = [t for t in post_tags if t.lower() in TARGET_TAGS]
        
        if not matching_tags:
            continue
            
        # Calculate the post age dynamically
        post_creation = post.get("created")
        if not post_creation:
            continue
            
        if post_creation.tzinfo is None:
            post_creation = post_creation.replace(tzinfo=timezone.utc)
            
        now = datetime.now(timezone.utc)
        age_seconds = (now - post_creation).total_seconds()
        
        if age_seconds < AGE_THRESHOLD_SECONDS:
            print(f"Skipping {identifier}: Matches tags {matching_tags} but is too new ({age_seconds / 60:.1f} mins old).")
            continue
            
        print(f"Target found! Post {identifier} matches tags {matching_tags} and is {age_seconds / 60:.1f} minutes old.")
        
        # 2. Safely pull active voters
        voters = []
        if hasattr(post, 'active_votes') and post.active_votes:
            voters = [v['voter'] for v in post.active_votes]
        
        if MY_ACCOUNT in voters:
            print(f"Skipping {identifier}: You have already upvoted this post.")
            continue
        
        # 3. Execute the upvote
        print(f"Upvoting {identifier} with {VOTE_WEIGHT}% power...")
        
        target_comment = Comment(identifier, blockchain_instance=stm)
        target_comment.upvote(weight=VOTE_WEIGHT, voter=MY_ACCOUNT)
        print("Upvote successfully broadcasted.")
        
        upvote_done = True
        break  

    if not upvote_done:
        print("No posts matching your target tags and age threshold were found in this history batch.")

except Exception as e:
    print(f"CRITICAL ERROR: {e}")
    exit(1)
