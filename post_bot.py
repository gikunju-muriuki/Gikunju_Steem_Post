import os
import datetime
from beem import Steem
from beem.comment import Comment

# ==========================================
# 1. CONFIGURATION VARIABLES
# ==========================================
MY_ACCOUNT = "gikunju"  
TARGET_COMMUNITY = "hive-129948"  
CUSTOM_TAGS = ["blog", "article", "writing", "krsuccess"]
REWARD_RECIPIENT = "bnwt"
custom_beneficiaries = [
    {'account': REWARD_RECIPIENT,
     'weight': 10000
    }
]

# ========================================================
# 2. The specific account receiving 100% of the rewards
# ========================================================
MY_PRIVATE_POSTING_KEY = os.getenv("STEEM_POSTING_KEY")
PROXY_URL = "https://steem-proxy.gikunju.workers.dev"  # Your worker endpoint

if not MY_PRIVATE_POSTING_KEY:
    print("Error: STEEM_POSTING_KEY secret is missing!")
    exit(1)
    
# ===============================================# 
# 3. 32-Day Rotated Content Library (English) - Cycle 1 (1 to 16)
# ===============================================
ARTICLES_POOL = {
    1: {
        "title": "How Embracing Constraints Fuels Real Innovation",
        "image": "https://cdn.steemitimages.com/DQmf1CNJXC5n5K3BgnajpKjQz52uUHwRxSY5PCWXRDeVfcz/1000022723.jpg",
        "body": "We frequently complain about boundaries like tight budgets, restricted schedules, or minimal materials when tackling a project. However, complete freedom can lead to creative paralysis, whereas clear limitations demand that we think resourcefully.\n\nInstead of viewing your current limitations as an obstacle today, treat them as a creative playground. Let your lack of resources inspire you to find a completely unique, highly inventive path forward."
    },
    2: {
        "title": "Finding Deep Creative Inspiration in Quiet Spaces",
        "image": "https://cdn.steemitimages.com/DQmPsxUrdtCke3wV59GfQVaZD1V3FbVjVE4zoGG6UEygE8y/1000022724.jpg",
        "body": "Fresh ideas rarely surface when our minds are constantly flooded with notifications, errands, and continuous digital noise. True breakthroughs generally happen during the quiet, unstructured moments of our day when our thoughts are free to wander.\n\nStep away from your workstation today and go for a short walk without headphones or your phone. Allow your environment to fill your senses naturally, and you may be surprised by the fresh perspectives that suddenly emerge."
    },
    3: {
        "title": "The Strategic Value of Conducting Regular Self-Reviews",
        "image": "https://cdn.steemitimages.com/DQmcGEd82avNGh8tryVmhUQQUPKU1bM8ZdHyBknhmkMb4TL/1000022725.jpg",
        "body": "It is incredibly easy to stay endlessly active while inadvertently moving in completely the wrong direction. Without routine periods of reflection, we tend to repeat ineffective behaviors and lose sight of our core targets.\n\nDedicate a brief window at the end of this week to evaluate what went well and what felt draining. Use these lessons to fine-tune your schedule, ensuring your daily efforts remain aligned with your core values."
    },
    4: {
        "title": "Embracing Fresh Beginnings and New Opportunities",
        "image": "https://cdn.steemitimages.com/DQmVg4cztzWumSPABhoqCiDrJ6HsAKNa3BUdx4KpWoMiSni/1000022726.jpg",
        "body": "Every new sunrise serves as a quiet invitation to recalibrate our targets and leave yesterday's disappointments behind. It is easy to get trapped dwelling on past missteps, but authentic progress happens only when we focus our attention on the present.\n\nTake a few moments today to write down three small objectives you want to hit. By breaking your larger goals down into immediate, actionable steps, you generate a healthy momentum that naturally carries you forward."
    },
    5: {
        "title": "Developing Ultimate Trust in Your Unique Lifepath",
        "image": "https://cdn.steemitimages.com/DQmcpRSLh9RVa5vnjcPdFLc5PWfytxudeXXkXECW9hzfiEU/1000022727.jpg",
        "body": "Constantly measuring your personal milestones against other people's curated social feeds is a direct path to dissatisfaction. Everyone moves on an entirely distinct timeline, shaped by completely different life dynamics and purposes.\n\nFocus your competitive drive solely on outperforming the person you were yesterday. Trusting your individual journey keeps you grounded, inspired, and fully dedicated to unlocking your own ultimate potential."
    },
    6: {
        "title": "Unlocking Potential Through Genuine Self-Compassion",
        "image": "https://cdn.steemitimages.com/DQmQsLd16YSmYvWHW8Dae8R4qRyrrTbxKB9SrSSrPY5rN4S/1000022728.jpg",
        "body": "We are frequently our own harshest critics, judging ourselves in a manner we would never use with a close friend. While harsh self-criticism feels like motivation, it actually creates stress and stalls long-term personal development.\n\nIf you make a mistake today, consciously swap out harsh self-blame for understanding and objective analysis. Realize that errors are merely valuable data points on the path toward mastering any new skill or routine."
    },
    7: {
        "title": "The Overlooked Value of Practicing Active Listening",
        "image": "https://cdn.steemitimages.com/DQmQGDp82f2ztJdeQBab5DGQjC3h2f45g1eTLsxefkaHfMZ/1000022729.jpg",
        "body": "Most people do not listen to understand what is being said; they listen primarily to formulate their next response. Meaningful connection and deep collaboration occur when we silence our internal monologues and focus entirely on the speaker.\n\nIn your conversations today, challenge yourself to let others finish their thoughts completely before you speak. Ask meaningful follow-up questions instead of instantly steering the topic back to your own stories."
    },
    8: {
        "title": "Learning to Say No with Ultimate Confidence and Grace",
        "image": "https://cdn.steemitimages.com/DQmXa5dCN3KQkd6LB1QoMEEz6FD7W1ZAZ8eLLcDb17HJuAG/1000022730.jpg",
        "body": "Every time you agree to a non-essential commitment, you are automatically declining your own top priorities. People-pleasing might seem helpful in the moment, but it ultimately creates resentment and severe personal burnout.\n\nWhen someone requests your time today, check your true bandwidth before offering an answer. It is completely acceptable to give a polite, honest refusal to protect your focus for your primary obligations."
    },
    9: {
        "title": "Overcoming Procrastination by Simplifying the First Step",
        "image": "https://cdn.steemitimages.com/DQmeLSRCMrf12Yf4GDvfmFCcQBoYMwpbH9AHuiE594GQEn4/1000022735.jpg",
        "body": "Delaying tasks is rarely caused by laziness; it is usually an emotional management tool for a project that feels intimidating. When a responsibility seems too large, our minds naturally search for quick distractions to bypass the discomfort.\n\nTo beat the overwhelm, divide your toughest task today into a step so ridiculously small that it takes almost zero willpower. Commit to working on just that single micro-step for five minutes, and watch the initial friction fade away."
    },
    10: {
        "title": "The Crucial Balance Between Hard Work and Rest",
        "image": "https://cdn.steemitimages.com/DQmZkjJBm7UzYMXUHNapZfAKgBUUNjafUdk5USpC4pKu4et/1000022736.jpg",
        "body": "Our culture heavily praises the non-stop grind, but constant exhaustion is never a reliable formula for true success. Rest is not a reward you must earn only after burning out; it is a structural requirement for sustained high performance.\n\nTreat your recovery time with the exact same priority you give to your most critical business meetings. Block out an hour this evening strictly for unwinding, allowing your mind and body to genuinely restore."
    },
    11: {
        "title": "Cultivating Mindful Awareness in a Busy World",
        "image": "https://cdn.steemitimages.com/DQmeYsVqFPBwsvfueqrCitdEUaD8puAXEQtr9g67B82Waf7/1000022737.jpg",
        "body": "Modern life constantly splits our attention in a thousand directions, leaving us feeling fragmented and depleted. Cultivating awareness doesn't require sitting in isolation for hours; it simply means being completely anchored where you are right now.\n\nTry eating your next meal or enjoying your beverage without checking a digital screen. Pay attention to the textures, temperatures, and flavors, offering your nervous system a critical moment to relax and reset."
    },
    12: {
        "title": "The Power of Defining Clear Financial Goals",
        "image": "https://steemitimages.com",
        "body": "Vague intentions like 'wanting to save more' rarely transform into permanent habit shifts. True financial independence starts when you map out explicit, measurable goals—such as establishing a specific emergency fund or creating a definitive debt payoff timeline.\n\nTake fifteen minutes today to document one concrete financial milestone for the coming year. Breaking this target down into steady monthly actions changes an intimidating challenge into a highly manageable path."
    },
    13: {
        "title": "The Power of Intentional Daily Micro-Habits",
        "image": "https://steemitimages.com",
        "body": "We frequently underestimate the massive compounding effect that tiny, everyday routines have on our long-term results. Reading just five pages or stretching for ten minutes might feel minor today, but consistency multiplies these efforts over time.\n\nReview your current morning flow and pinpoint where you can introduce one healthy micro-habit. Commit to completing it without exception today, and watch how it subtly upgrades your daily energy and concentration."
    },
    14: {
        "title": "The Ripple Effect of Small Acts of Kindness",
        "image": "https://steemitimages.com",
        "body": "We often assume we need to execute grand, costly gestures to make a difference in the lives of those around us. In reality, a genuine compliment, holding a door, or sending an encouraging note can completely pivot someone's afternoon.\n\nMake it a point to offer one unexpected token of kindness or validation to someone today. These small gestures build a wonderful ripple effect, boosting both the recipient's mood and your own internal happiness."
    },
    15: {
        "title": "Building Resilience Against Life's Unexpected Hurdles",
        "image": "https://steemitimages.com",
        "body": "Disruptions and sudden changes are entirely inevitable, but our psychological reaction to them remains completely within our hands. Building true resilience isn't about ignoring difficulties; it is about mastering the art of adapting and bouncing back quickly.\n\nWhen a small annoyance happens today, step back and ask yourself if this issue will matter in a month. Shifting your timeline perspective instantly drops stress levels and helps you solve problems with a collected, rational mind."
    },
    16: {
        "title": "The Direct Connection Between Sleep and Daily Success",
        "image": "https://steemitimages.com",
        "body": "Sacrificing sleep to squeeze out more working hours is a common trap that quickly derails your mental processing speed. Ongoing sleep deprivation damages your mood, dampens creative thinking, and triggers costly errors in decision-making.\n\nCommit to a calming evening wind-down routine tonight by stowing away electronic devices thirty minutes before turning off the lights. Prioritizing deep rest ensures you meet tomorrow with full focus and physical vitality."
    },
    17: {
        "title": "The Life-Changing Magic of Keeping a Workspace Clean",
        "image": "https://steemitimages.com",
        "body": "A physical environment crowded with stray notes, dirty mugs, and scattered items creates a continuous, underlying cognitive strain. It forces your brain to waste energy filtering out visual noise, which actively reduces your memory capacity.\n\nBefore launching into your core projects today, clear everything off your desk except the absolute necessities. You will instantly feel a lighter mental load and find it much easier to lock into deep focus blocks."
    },
    18: {
        "title": "Decluttering Your Digital Environment for Mental Clarity",
        "image": "https://steemitimages.com",
        "body": "A chaotic digital setup can trigger just as much background anxiety and split-second distraction as a messy physical desk. Overloaded inboxes, unorganized desktop folders, and constant pings fragment your cognitive attention.\n\nTake ten minutes today to unsubscribe from lists you no longer read and archive old files. A streamlined digital ecosystem brings immediate mental clarity and allows your daily tasks to flow much more seamlessly."
    },
    19: {
        "title": "The Subtle Art of Protecting Your Personal Energy",
        "image": "https://steemitimages.com",
        "body": "Your time and emotional capacity are strictly limited resources that must be managed with absolute intent every day. Defaulting to a 'yes' for every request or taking on other people's complaints leaves you empty-handed for your own life.\n\nPractice establishing polite but firm boundaries today regarding your schedule and mental availability. Guarding your internal peace ensures you can bring your highest, most authentic effort to the things that truly matter."
    },
    20: {
        "title": "Embracing the Uncomfortable Journey of Personal Growth",
        "image": "https://steemitimages.com",
        "body": "Genuine personal development never takes place within the safe, predictable borders of our comfort zones. Real improvement demands that we step out into the awkward, uncertain territory where failure and education live side by side.\n\nIdentify one task or hard talk you have been avoiding because it feels intimidating or uncomfortable. Face it head-on today, recognizing that moving through brief discomfort is exactly how you stretch your capabilities."
    },
    21: {
        "title": "Celebrating Your Incremental Progress Over Time",
        "image": "https://steemitimages.com",
        "body": "We are often so intensely focused on the distant mountain peak that we neglect to look back and see how much ground we have already covered. Ignoring your milestones turns the self-improvement journey into an endless, exhausting chore.\n\nTake a brief pause today to acknowledge a skill or routine you handle with ease now that used to trip you up last year. Validating your own evolution builds the deep internal confidence required to take on your next major challenge."
    },
    22: {
        "title": "How Physical Movement Boosts Daily Brain Power",
        "image": "https://steemitimages.com",
        "body": "Our bodies and minds operate as a deeply tied, single system that constantly drives overall performance. Sitting entirely still at a desk for hours cuts down on blood circulation to the brain, inducing foggy thinking and midday fatigue.\n\nBreak up your stationary blocks today by standing to stretch or pacing around the room every single hour. Even a quick two minutes of movement re-oxygenates your body, instantly sharpening your focus, mood, and output."
    },
    23: {
        "title": "Developing a Grounded Perspective on Perfectionism",
        "image": "https://steemitimages.com",
        "body": "Perfectionism is usually just a beautiful mask for deep-seated fear—fear of being judged, failing, or falling short. Demanding perfection freezes projects indefinitely, locking you away from helpful real-world testing and growth.\n\nSet your sights on excellent execution rather than flawless perfection in your tasks today. Keep in mind that a completed piece of work out in the world is infinitely more useful than a flawless project hidden away in a draft folder."
    },
    24: {
        "title": "Curating Your Mind's Daily Information Diet",
        "image": "https://steemitimages.com",
        "body": "Just like the nutrition we choose determines our physical health, the media we absorb defines our psychological balance. Regularly taking in over-dramatized news and hostile social timelines triggers a stressed, uneasy outlook on life.\n\nTake a realistic look at the accounts and platforms you open most often during the week. Swap out at least one unhelpful source for educational channels, constructive essays, or supportive communities."
    },
    25: {
        "title": "Nurturing Professional Growth Through Active Learning",
        "image": "https://steemitimages.com",
        "body": "The landscapes of industry and technology shift so quickly that static skillsets rapidly become outdated. Staying dedicated to consistent learning is the absolute best safety policy for your career future and individual growth.\n\nFind a short educational post, podcast episode, or tutorial walkthrough tied to your industry today. Invest just fifteen minutes into absorbing that information and think about how to apply it directly to your current tasks."
    },
    26: {
        "title": "Finding Deep Fulfillment in Simple Daily Pleasures",
        "image": "https://steemitimages.com",
        "body": "It is remarkably easy to pass through life waiting for massive milestones to finally permit ourselves to feel happy. However, authentic lifestyle satisfaction is actually constructed by capturing and enjoying small, everyday moments of peace.\n\nWhether it is the touch of morning sun, a great blend of coffee, or an easy laugh with a teammate, step into it. Pause for ten seconds to truly value these basic pleasures as they arrive during your afternoon."
    },
    27: {
        "title": "Unlocking Creative Solutions Through Critical Thinking",
        "image": "https://steemitimages.com",
        "body": "When hit by an unexpected problem, our automatic reflex is often to worry or fall back on old, tired routines. Critical thinking means pulling back, identifying hidden assumptions, and evaluating the core problem from fresh perspectives.\n\nIf you encounter a roadblock today, do not just attempt to smash through it using the exact same methods. Ask yourself how an outsider would navigate this issue, and look for a more efficient, creative shortcut."
    },
    28: {
        "title": "The Loneliness Epidemic and the Need for Connection",
        "image": "https://steemitimages.com",
        "body": "Despite being more digitally linked than any prior generation, an incredible number of people report feeling profoundly isolated. Social network comments function as a superficial substitute for raw, authentic human bonds.\n\nReach out to an old teammate or a family member today with a direct phone call or a thoughtful text. Spending a few minutes tending to your personal support circle pays massive dividends for your mental health."
    },
    29: {
        "title": "Cultivating Patience in an Era of Instant Gratification",
        "image": "https://steemitimages.com",
        "body": "We exist in an on-demand ecosystem where rapid delivery, live streams, and instant notifications have skewed our expectations. Because trivial things show up instantly, we incorrectly assume major personal updates should materialize overnight too.\n\nRemind yourself today that life-changing achievements like career expertise, deep relationships, and wellness take time. Welcome the slow, steady progress and practice patience when rewards require time to grow."
    },
    30: {
        "title": "The Invaluable Strength of True Emotional Maturity",
        "image": "https://steemitimages.com",
        "body": "Emotional maturity shows up in the critical space between feeling an intense response and picking your actual behavior. Snapping out of immediate anger or irritation almost always makes an already tense situation far worse.\n\nWhen someone tests your limits today, take a full, deliberate breath before saying a word. Mastering your initial reflex empowers you to handle the problem logically and defuse friction without drama."
    },
    31: {
        "title": "Cultivating Genuine Gratitude During Difficult Times",
        "image": "https://steemitimages.com",
        "body": "Building a practice of gratitude is not about forcing positive thinking or overlooking the heavy trials in your life. It is simply about deliberately training your mind to appreciate the good things that exist right alongside the struggles.\n\nBefore turning in tonight, write down three specific moments that brought a smile to your face today. Shifting your focus to what is going right actively lowers stress markers and directly upgrades your sleep quality."
    },
    32: {
        "title": "Shifting Focus From Final Outcomes to Daily Systems",
        "image": "steemitimages.com",
        "body": "Obsessing completely over a distant destination can leave you feeling frustrated by how much further you still have to travel. Top performers and those who miss the mark often share identical goals; it is the daily operational system that sets them apart.\n\nForget about the ultimate finish line for a second and focus fully on handling your routine excellently today. Trust that if your daily systems are robust, the milestones will naturally take care of themselves."
    }
    }


# ==========================================
# 4. Dynamic Selection
# ==========================================
# Determine rotation index based on Day of the Year 
# (This ensures a clean 1-32 loop that auto-wraps at the end of cycles)
now_eat = datetime.datetime.utcnow() + datetime.timedelta(hours=3) # UTC to EAT
day_of_year = now_eat.timetuple().tm_yday
selected_index = ((day_of_year - 1) % 32) + 1  

# Human-readable date function
def get_ordinal_suffix(day):
    if 11 <= day <= 13:
        return "th"
    return {1: "st", 2: "nd", 3: "rd"}.get(day % 10, "th")

day = now_eat.day
suffix = get_ordinal_suffix(day)
formatted_date = f"{day}{suffix} {now_eat.strftime('%A %B %Y')}"

# Fetch today's unique article elements
article = ARTICLES_POOL[selected_index]

post_title = f"{article['title']} — {formatted_date}"
post_body = f"{article['body']}\n\n{article['image']}"

post_permlink = f"daily-insight-day-{selected_index}-{now_eat.strftime('%Y%m%d')}"
  

# ==========================================
# 5. Connect and broadcast to blockchain
# ==========================================

try:
    print(f"Connecting to node via Cloudflare proxy: {PROXY_URL}")
    
    # Initialize the robust Steem client
    stm = Steem(
        node=[PROXY_URL],
        keys=[MY_PRIVATE_POSTING_KEY]
    )
    
    print(f"Broadcasting Day {selected_index} to community {TARGET_COMMUNITY}.")
    
    # Post directly using the standard blockchain wrapper
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
    
    print(f"Post #{selected_index} has been published to {TARGET_COMMUNITY}.")

except Exception as e:
    print(f"CRITICAL ERROR: Broadcast routing failed: {e}")
    exit(1)
