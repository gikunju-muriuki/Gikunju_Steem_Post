import os
from datetime import datetime, timezone
from beem import Steem
from beem.comment import Comment
from beem.discussions import Discussions_by_created

# 1. Configuration
MY_ACCOUNT = "blog.god"            # Your Steem account name
VOTE_WEIGHT = 3                 # Upvote weight (1 to 100)
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
    
    print("Fetching the latest posts globally from the blockchain history...")
    
    # Instantly query the latest 20 created posts on the network
    # We use a limit of 20 to ensure we find posts older than 5.3 minutes
    query = {"limit": 20, "tag": ""}
    discussions = Discussions_by_created(query, blockchain_instance=stm)
    
    upvote_done = False
    
    for post in discussions:
        author = post.get("author")
        permlink = post.get("permlink")
        identifier = f"@{author}/{permlink}"
        
        # Calculate the post age dynamically (using aware UTC datetimes)
        post_creation = post.get("created")
        if not post_creation:
            continue
            
        # Ensure post_creation is UTC aware
        if post_creation.tzinfo is None:
            post_creation = post_creation.replace(tzinfo=timezone.utc)
            
        now = datetime.now(timezone.utc)
        age_seconds = (now - post_creation).total_seconds()
        
        # 1. Check if the post meets your age condition (> 5.3 minutes)
        if age_seconds < AGE_THRESHOLD_SECONDS:
            print(f"Skipping {identifier}: Post is too new ({age_seconds / 60:.1f} mins old).")
            continue
            
        print(f"Target found! Post {identifier} is {age_seconds / 60:.1f} minutes old.")
        
        # 2. Safely pull active voters
        voters = []
        if hasattr(post, 'active_votes') and post.active_votes:
            voters = [v['voter'] for v in post.active_votes]
        
        if MY_ACCOUNT in voters:
            print(f"Skipping {identifier}: You have already upvoted this post.")
            continue
        
        # 3. Execute the upvote
        print(f"Upvoting {identifier} with {VOTE_WEIGHT}% power...")
        
        # Re-instantiate as a Comment object to ensure clean signing capabilities
        target_comment = Comment(identifier, blockchain_instance=stm)
        target_comment.upvote(weight=VOTE_WEIGHT, voter=MY_ACCOUNT)
        print("Upvote successfully broadcasted.")
        
        upvote_done = True
        break  # Exit the loop immediately after one successful upvote

    if not upvote_done:
        print("No matching posts older than 5.3 minutes were found in the recent history batch.")

except Exception as e:
    print(f"CRITICAL ERROR: {e}")
    exit(1)
