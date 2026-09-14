import os
import datetime
from beem import Steem
from beem.comment import Comment

# 1. Configuration variables
MY_ACCOUNT = "gikunju"  # Your Steem account name
TARGET_COMMUNITY = "hive-129948"  
CUSTOM_TAGS = ["general-writing", "art", "meme", "trc-20", "sunpump", "puss", "krsuccess"]

# The specific account receiving 100% of the rewards
REWARD_RECIPIENT = "bnwt"  

# 2. Extract configuration from GitHub Secrets
MY_PRIVATE_POSTING_KEY = os.getenv("STEEM_POSTING_KEY")
PROXY_URL = "https://steem-proxy.gikunju.workers.dev"  # Active worker endpoint

if not MY_PRIVATE_POSTING_KEY:
    print("Error: STEEM_POSTING_KEY secret is missing!")
    exit(1)

def get_ordinal_suffix(day):
    if 11 <= day <= 13:
        return "th"
    return {1: "st", 2: "nd", 3: "rd"}.get(day % 10, "th")

def generate_custom_date(dt_obj):
    """Generates date format: 23rd Tuesday March 2026"""
    day = dt_obj.day
    suffix = get_ordinal_suffix(day)
    weekday = dt_obj.strftime("%A")
    month = dt_obj.strftime("%B")
    year = dt_obj.strftime("%Y")
    return f"{day}{suffix} {weekday} {month} {year}"

# Build Date Formats (Synced to EAT Timezone)
now_eat = datetime.datetime.utcnow() + datetime.timedelta(hours=3) # UTC to EAT
formatted_date = generate_custom_date(now_eat)

# Content structure in Bangla
post_title = f"চাঁদের পথে Puss 🌙"
post_body = f"💌Puss কিনুন এবং HODL করুন!💌\n\nhttps://cdn.steemitimages.com/DQmYjwMKWAdVvPZU2kMrVRVkLxs81YZvP4mK8RzdNoGoA69/1000022553.jpg"

# Consistent permalink structure mapping
post_permlink = f"daily-blessing-{now_eat.strftime('%Y%m%d%H%M')}"

# Build the 100% beneficiary structure weight (10000 = 100%)
custom_beneficiaries = [
    {'account': REWARD_RECIPIENT, 'weight': 10000}
]

# 3. Connect and broadcast using standard Beem structures
try:
    print(f"Connecting to node via Cloudflare proxy: {PROXY_URL}")
    
    # Initialize the robust Steem client
    stm = Steem(
        node=[PROXY_URL],
        keys=[MY_PRIVATE_POSTING_KEY]
    )
    
    print(f"Broadcasting to community {TARGET_COMMUNITY} with 100% rewards to @{REWARD_RECIPIENT}...")
    
    # Post directly using the standard, tested blockchain structure wrapper
    stm.post(
        title=post_title,
        body=post_body,
        author=MY_ACCOUNT,
        permlink=post_permlink,
        tags=[TARGET_COMMUNITY] + CUSTOM_TAGS,
        parent_author="",
        parent_permlink=TARGET_COMMUNITY,
        beneficiaries=custom_beneficiaries
    )
    
    print("Post has been published.")

except Exception as e:
    print(f"CRITICAL ERROR: Broadcast routing failed: {e}")
    exit(1)
