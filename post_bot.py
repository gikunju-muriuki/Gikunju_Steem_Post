import os
import time
from datetime import datetime
from beem import Steem
from beem.blockchain import Blockchain
from beem.comment import Comment

# 1. Configuration
MY_ACCOUNT = "gikunju"            # Your Steem account name
VOTE_WEIGHT = 100                 # Upvote weight (1 to 100)
PROXY_URL = "https://steem-proxy.gikunju.workers.dev"
AGE_THRESHOLD_SECONDS = 5.3 * 60  # 5.3 minutes = 318 seconds

# 2. Extract Key from GitHub Secrets
MY_PRIVATE_POSTING_KEY = os.getenv("STEEM_POSTING_KEY")

if not MY_PRIVATE_POSTING_KEY:
    print("Error: STEEM_POSTING_KEY secret is missing!")
    exit(1)

try:
    print(f"Connecting to node via proxy: {PROXY_URL}")
    stm = Steem(node=[PROXY_URL], keys=[MY_PRIVATE_POSTING_KEY])
    
    # Instantiate the global blockchain stream
    blockchain = Blockchain(blockchain_instance=stm)
    
    # FIX: Get the latest block number so we don't start from historical block #1
    current_block = blockchain.get_current_block_num()
    print(f"Monitoring Steem blockchain starting from live block #{current_block}...")
    
    # Stream live operations starting from the current head block
    for op in blockchain.stream(opNames=["comment"], start=current_block, threading=False):
        try:
            # Filter for root posts only (parent_author is empty for main posts)
            if op.get("parent_author") == "":
                author = op.get("author")
                permlink = op.get("permlink")
                identifier = f"@{author}/{permlink}"
                
                # Load the full post object to access metadata and votes
                post = Comment(identifier, blockchain_instance=stm)
                
                # Calculate the post age dynamically
                post_creation = post.get("created")
                if not post_creation:
                    continue
                    
                now = datetime.utcnow()
                age_seconds = (now - post_creation).total_seconds()
                
                # Check if the post meets your age condition (> 5.3 minutes)
                if age_seconds < AGE_THRESHOLD_SECONDS:
                    print(f"Skipping {identifier}: Post is too new ({age_seconds / 60:.1f} mins old).")
                    continue
                
                print(f"Target found! Post {identifier} is {age_seconds / 60:.1f} minutes old.")
                
                # Safely pull active voters
                voters = []
                if hasattr(post, 'active_votes') and post.active_votes:
                    voters = [v['voter'] for v in post.active_votes]
                
                if MY_ACCOUNT in voters:
                    print(f"Skipping. You have already upvoted this post.")
                    continue
                
                # Execute the upvote
                print(f"Upvoting {identifier} with {VOTE_WEIGHT}% power...")
                post.upvote(weight=VOTE_WEIGHT, voter=MY_ACCOUNT)
                print("Upvote successfully broadcasted. Exiting script.")
                
                # Break loop and exit after upvoting the latest valid post
                break
                
        except Exception as op_error:
            # Prevent a single bad block/operation from crashing the stream
            print(f"Error processing operation: {op_error}")
            continue

except Exception as e:
    print(f"CRITICAL ERROR: {e}")
    exit(1)
