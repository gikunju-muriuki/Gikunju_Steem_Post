import os
import random
import time
from datetime import datetime, timezone
from beem import Steem
from beem.comment import Comment
from beem.discussions import Discussions_by_created
from beem.nodelist import NodeList

# =========================================================================
# INITIAL RAMP-UP VARIANCE DELAY (60 seconds to 15 minutes)
# =========================================================================
delay_seconds = random.randint(60, 900)
print(f"[DELAY LOGIC] Sleeping for {delay_seconds} seconds ({delay_seconds / 60:.1f} minutes) before starting script...")
time.sleep(delay_seconds)
print("[DELAY LOGIC] Delay cleared. Initializing Steem interaction.")

# 1. Configuration & Blacklist
MY_ACCOUNT = "blog.god"            # Your Steem account name
VOTE_WEIGHT = 33.3                   # VP recharge mode
PROXY_URL = "https://steem-proxy.gikunju.workers.dev"

# BLACKLIST: Excludes your own account and any undesirable authors/spammers
BLACKLIST = {MY_ACCOUNT, "spamaccount1", "knownabuser2"}

# Precision Curation Timing: Optimized for Steem's peak reward window (5 to 15 minutes)
random_minutes = random.uniform(5.0, 15.0)
AGE_THRESHOLD_SECONDS = random_minutes * 60
print(f"Looking for posts older than {random_minutes:.1f} minutes but younger than 15.0 minutes for optimal curation rewards.")

# TARGET_TAGS: Converted to a Python set for O(1) lightning-fast lookups
TARGET_TAGS = {
    "xrp", "solana", "usdt", "blockchain", "trading", "steemitchallenge", 
    "newcomers", "creativity", "steemexclusive", "art", "newcomer", 
    "nigeria", "krsuccess", "creative", "bitcoin", "blog", "crypto", 
    "steem", "photography", "game"
}

# 2. Extract Key from GitHub Secrets
MY_PRIVATE_POSTING_KEY = os.getenv("STEEM_POSTING_KEY")

if not MY_PRIVATE_POSTING_KEY:
    print("Error: STEEM_POSTING_KEY secret is missing!")
    exit(1)

try:
    print("Fetching active Steem nodes and configuring failover...")
    nodelist = NodeList()
    nodelist.update_nodes()
    # Combine your custom proxy URL with the global healthy node list
    available_nodes = [PROXY_URL] + nodelist.get_steem_nodes()

    print(f"Connecting to Steem blockchain with failover support...")
    stm = Steem(node=available_nodes, keys=[MY_PRIVATE_POSTING_KEY])
    
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
        
        # --- BLACKLIST FILTER LOGIC ---
        if author in BLACKLIST:
            print(f"Skipping {identifier}: Author @{author} is blacklisted.")
            continue
        
        # --- TAG FILTER LOGIC (O(1) Set Intersection) ---
        post_tags = post.get("tags", [])
        matching_tags = [t for t in post_tags if t.lower() in TARGET_TAGS]
        
        if not matching_tags:
            continue
            
        # --- CONTENT LENGTH FILTER LOGIC (Spam Protection) ---
        post_body = post.get("body", "")
        word_count = len(post_body.split()) if post_body else 0
        if word_count > 0 and word_count < 40:
            print(f"Skipping {identifier}: Content too short ({word_count} words - potential spam).")
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
        
        # Safely pull active voters
        voters = []
        if hasattr(post, 'active_votes') and post.active_votes:
            voters = [v['voter'] for v in post.active_votes]
        
        if MY_ACCOUNT in voters:
            print(f"Skipping {identifier}: You have already upvoted this post.")
            continue
        
        # Execute the upvote
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
