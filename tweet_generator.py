#!/usr/bin/env python3
"""
Kitsune Kodo Tweet Generator
A simple CLI tool to generate commercial tweets using OpenAI API and post them to X (Twitter)

SUOMI TIIVISTYS:
- Skripti generoi mainostwiittejä (OpenAI GPT-4) ja voi postata ne X:ään (OAuth1).
- Käynnistys esimerkki: python tweet_generator.py --product kitsune_kodo --tone hype --length short --post
- Kysyy vahvistuksen ennen postausta, näyttää URL:n.
"""

import os
import sys
import argparse
from openai import OpenAI
from dotenv import load_dotenv
import tweepy

# Load environment variables
load_dotenv()

# Product information database
PRODUCTS = {
    'kitsune_kodo': {
        'name': 'Kitsune Kodo',
        'description': 'A unique NFT collection featuring fox spirit artwork with traditional Japanese aesthetics',
        'hashtags': ['#KitsuneKodo', '#NFT', '#CryptoArt', '#NFTCommunity', '#DigitalArt', '#Web3'],
        'url': 'https://opensea.io/collection/kitsune-kodo'
    },
    # Lisää uusia tuotteita tähän tarvittaessa
}

# Length presets (max characters)
LENGTH_PRESETS = {
    'short': 140,   # Lyhyt twiitti
    'medium': 220,  # Keskipitkä twiitti
    'long': 280     # Maksimi X-raja
}

def get_openai_client():
    """Inicialisoi OpenAI-clientti (vaatii OPENAI_API_KEY)."""
    api_key = os.getenv('OPENAI_API_KEY')
    if not api_key:
        print("❌ Error: OPENAI_API_KEY not found in environment variables.")
        print("Please create a .env file with your API key or set it as an environment variable.")
        sys.exit(1)
    return OpenAI(api_key=api_key)

def get_x_client():
    """Inicialisoi X (Twitter) OAuth1 -clientti (avain+salaisuus+tokenit)."""
    api_key = os.getenv('X_API_KEY')
    api_secret = os.getenv('X_API_SECRET')
    access_token = os.getenv('X_ACCESS_TOKEN')
    access_token_secret = os.getenv('X_ACCESS_TOKEN_SECRET')
    
    if not all([api_key, api_secret, access_token, access_token_secret]):
        print("❌ Error: X (Twitter) API credentials not found in environment variables.")
        print("Please add X API credentials to your .env file.")
        sys.exit(1)
    
    client = tweepy.Client(
        consumer_key=api_key,
        consumer_secret=api_secret,
        access_token=access_token,
        access_token_secret=access_token_secret
    )
    return client

def post_tweet_to_x(tweet_text):
    """Post a tweet to X (Twitter) using OAuth 1.0a."""
    try:
        client = get_x_client()
        response = client.create_tweet(text=tweet_text)
        tweet_id = response.data['id']
        
        # Get the authenticated user to construct the URL
        me = client.get_me()
        username = me.data.username
        tweet_url = f"https://x.com/{username}/status/{tweet_id}"
        
        return True, tweet_url
    except Exception as e:
        return False, str(e)

def generate_tweet(product, tone, length, variations=1, custom_message=None):
    """Generoi twiitti(t) annetulle tuotteelle, äänensävyllä ja pituudella."""
    
    client = get_openai_client()
    
    # Hae tuotetiedot (nimeä, kuvaus, hashtagit, URL)
    if product not in PRODUCTS:
        print(f"❌ Error: Unknown product '{product}'")
        print(f"Available products: {', '.join(PRODUCTS.keys())}")
        sys.exit(1)
    
    product_info = PRODUCTS[product]
    max_length = LENGTH_PRESETS.get(length, 280)
    
    # Rakenna system-prompt, johon lisätään sävy ja max-pituus
    system_message = f"""You are a professional social media manager creating engaging commercial tweets for X (Twitter).

Product: {product_info['name']}
Description: {product_info['description']}
Suggested hashtags: {', '.join(product_info['hashtags'])}
Product URL: {product_info['url']}

Create tweets that are:
- Attention-grabbing and optimized for engagement
- Maximum {max_length} characters
- Using a {tone} tone
- Include relevant emojis
- Include appropriate hashtags from the suggested list"""

    if custom_message:
        user_prompt = f"Create a commercial tweet with this message or angle: {custom_message}"
    else:
        user_prompt = f"Create a compelling commercial tweet promoting {product_info['name']}"
    
    try:
        if variations == 1:
            print(f"\n🦊 Generating tweet for {product_info['name']}...")
        else:
            print(f"\n🦊 Generating {variations} tweet variations for {product_info['name']}...")
        
        response = client.chat.completions.create(
            model="gpt-4",
            messages=[
                {"role": "system", "content": system_message},
                {"role": "user", "content": user_prompt if variations == 1 else f"{user_prompt}\n\nGenerate {variations} different variations. Number each tweet (1., 2., 3., etc.)"}
            ],
            temperature=0.85,
            max_tokens=500 if variations > 1 else 150
        )
        
        content = response.choices[0].message.content.strip()
        
        if variations == 1:
            return [content]
        else:
            # Pilko numeroitu lista vastauksesta variaatioiksi
            lines = content.split('\n')
            tweets = []
            current_tweet = ""
            
            for line in lines:
                line = line.strip()
                if line and line[0].isdigit() and ('. ' in line or ') ' in line):
                    if current_tweet:
                        tweets.append(current_tweet.strip())
                    current_tweet = line.split('. ', 1)[-1].split(') ', 1)[-1]
                elif current_tweet and line:
                    current_tweet += " " + line
            
            if current_tweet:
                tweets.append(current_tweet.strip())
            
            return [t for t in tweets if len(t) <= max_length][:variations]
    
    except Exception as e:
        print(f"❌ Error generating tweet: {e}")
        sys.exit(1)

def print_tweets(tweets, product, post=False):
    """Tulosta twiitit ja kysy tarvittaessa postausvahvistus."""
    product_info = PRODUCTS[product]
    
    print("\n" + "="*70)
    if len(tweets) == 1:
        print(f"✨ Generated Tweet for {product_info['name']}:")
    else:
        print(f"✨ Generated {len(tweets)} Tweet Variations for {product_info['name']}:")
    print("="*70)
    
    posted_tweets = []
    
    for idx, tweet in enumerate(tweets, 1):
        char_count = len(tweet)
        if len(tweets) > 1:
            print(f"\n[{idx}] {tweet}")
            print(f"    📊 {char_count}/280 characters")
        else:
            print(f"\n{tweet}\n")
            print(f"📊 Character count: {char_count}/280")
        
        # Postaa X:ään jos käyttäjä hyväksyy
        if post and len(tweets) == 1:
            print("\n" + "-"*70)
            response = input("📤 Post this tweet to X? (yes/no): ").strip().lower()
            if response in ['yes', 'y']:
                success, result = post_tweet_to_x(tweet)
                if success:
                    print(f"✅ Tweet posted successfully!")
                    print(f"🔗 URL: {result}")
                    posted_tweets.append(result)
                else:
                    print(f"❌ Failed to post tweet: {result}")
            print("-"*70)
        elif post and len(tweets) > 1:
            print(f"\n    Post this tweet? (yes/no): ", end="")
            response = input().strip().lower()
            if response in ['yes', 'y']:
                success, result = post_tweet_to_x(tweet)
                if success:
                    print(f"    ✅ Posted: {result}")
                    posted_tweets.append(result)
                else:
                    print(f"    ❌ Failed: {result}")
    
    print("="*70 + "\n")
    return posted_tweets

def main():
    """Main function with argparse."""
    
    parser = argparse.ArgumentParser(
        description='🦊 Kitsune Kodo Tweet Generator - Generate commercial tweets with OpenAI',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  %(prog)s --product kitsune_kodo --tone hype --length short
  %(prog)s --product kitsune_kodo --tone professional --length medium --variations 3
  %(prog)s --product kitsune_kodo --tone urgent --message "Limited edition drop tonight!"
  
Available products: kitsune_kodo
Available tones: professional, casual, hype, urgent, friendly, humorous, mysterious
Available lengths: short (140), medium (220), long (280)
        """
    )
    
    parser.add_argument(
        '--product',
        type=str,
        required=True,
        choices=list(PRODUCTS.keys()),
        help='Product to market (e.g., kitsune_kodo)'
    )
    
    parser.add_argument(
        '--tone',
        type=str,
        default='professional',
        choices=['professional', 'casual', 'hype', 'urgent', 'friendly', 'humorous', 'mysterious'],
        help='Tone of the tweet (default: professional)'
    )
    
    parser.add_argument(
        '--length',
        type=str,
        default='medium',
        choices=['short', 'medium', 'long'],
        help='Tweet length: short (140), medium (220), long (280) (default: medium)'
    )
    
    parser.add_argument(
        '--variations',
        type=int,
        default=1,
        metavar='N',
        help='Number of tweet variations to generate (default: 1)'
    )
    
    parser.add_argument(
        '--message',
        type=str,
        default=None,
        help='Custom message or angle for the tweet'
    )
    
    parser.add_argument(
        '--post',
        action='store_true',
        help='Post the generated tweet(s) to X (Twitter)'
    )
    
    args = parser.parse_args()
    
    # Generate tweets
    tweets = generate_tweet(
        product=args.product,
        tone=args.tone,
        length=args.length,
        variations=args.variations,
        custom_message=args.message
    )
    
    # Display results
    print_tweets(tweets, args.product, post=args.post)

if __name__ == "__main__":
    main()
