#!/usr/bin/env python3
"""
Kitsune Art Generator
Generoi AI-pohjaisia Kitsune-taideteoksia käyttäen DALL-E:ä.
Tallentaa PNG:t kitsune_art/ -kansioon.

SUOMI TIIVISTYS:
- Luo uniikkeja Kitsune-kuvia DALL-E:llä (OpenAI).
- Tyyppi: fire, dark, ice, demon, spirit, sacred.
- Spec-parametrit: kupin featuret (fusjoinit, värit, tehosteita).
- PNG-nimet: L33t-tyyli Kitsune-nimitykset.
- Tallennus: kitsune_art/ -kansio.

Esimerkki: python kitsune_art_generator.py --type fire --specs "9-tailed fox with crimson fur and golden eyes"
"""

import os
import sys
import argparse
import requests
from openai import OpenAI
from dotenv import load_dotenv
import random
from datetime import datetime

# Load environment variables
load_dotenv()

# Kitsune-tyypeista vastaavat luonnit (prompt-base)
KITSUNE_TYPES = {
    'fire': {
        'name': 'Fire Kitsune',
        'description': 'Tulinen kitsune, punaisin ja kultaisin väreillä, liekkejä värisemässä.',
        'style': 'crimson and gold, blazing energy, mystical flames'
    },
    'dark': {
        'name': 'Dark Kitsune',
        'description': 'Pimeä ja mystinen kitsune, musta ja violetti väritys, mustat aaveet.',
        'style': 'shadow-infused, dark purples and blacks, sinister mystique'
    },
    'ice': {
        'name': 'Ice Kitsune',
        'description': 'Jäätävä kitsune, sinisen ja valkoisen väritys, jääkiteet ja lumikiteet.',
        'style': 'crystalline blue and white, frosty aura, glacial elegance'
    },
    'demon': {
        'name': 'Demon Kitsune',
        'description': 'Paholainen kitsune, harmaa ja punainen väritys, piikkilineet ja sarvet.',
        'style': 'demonic red and gray, horns and claws, malevolent presence'
    },
    'spirit': {
        'name': 'Spirit Kitsune',
        'description': 'Hengen kitsune, valkoinen ja hopean väritys, hehkuvat aaveet.',
        'style': 'ethereal white and silver, glowing wisps, divine presence'
    },
    'sacred': {
        'name': 'Sacred Kitsune',
        'description': 'Pyhä kitsune, kultainen ja vaalea väritys, pyhä valo.',
        'style': 'golden and radiant, holy light, celestial majesty'
    }
}

# L33t-tyyli Kitsune-nimitykset
KITSUNE_NAMES = [
    'K1tsun3_',
    'X4l_Kud@',
    'F0x_Sp1r1t',
    'My5t1c_T@1l',
    'D3m0n_F0x',
    'K1tsun3_L0rd',
    'T41l_0f_F1r3',
    'Sh@d0w_F0x',
    'G0ld3n_F1r3',
    'N1ght_T@1l',
    'C3l35t1@l_K1tsu',
    'M00n_F0x',
    'V01d_Kud@',
    'R4z0r_T@1l',
    'Sp1r1t_0f_0ld'
]

def get_openai_client():
    """Hae OpenAI-client (vaatii OPENAI_API_KEY)."""
    api_key = os.getenv('OPENAI_API_KEY')
    if not api_key:
        print("❌ Error: OPENAI_API_KEY not found in environment variables.")
        sys.exit(1)
    return OpenAI(api_key=api_key)

def generate_kitsune_art(kitsune_type, custom_specs=None):
    """Generoi Kitsune-kuva DALL-E:llä annetulle tyypille ja spec:eille."""
    
    if kitsune_type not in KITSUNE_TYPES:
        print(f"❌ Error: Unknown kitsune type '{kitsune_type}'")
        print(f"Available types: {', '.join(KITSUNE_TYPES.keys())}")
        sys.exit(1)
    
    type_info = KITSUNE_TYPES[kitsune_type]
    
    # Rakenna prompt
    prompt = f"""Create a beautiful and mystical Kitsune (Japanese fox spirit) art piece.
    
Type: {type_info['name']}
Style: {type_info['style']}
Description: {type_info['description']}"""
    
    if custom_specs:
        prompt += f"\nSpecial Features: {custom_specs}"
    
    prompt += "\n\nArtistic style: Traditional Japanese art meets modern digital art, magical aura, high quality, detailed, fantastical."
    
    print(f"\n🦊 Generoi Kitsune-taidetta ({type_info['name']})...")
    print(f"   Prompt: {prompt[:100]}...")
    
    try:
        client = get_openai_client()
        
        response = client.images.generate(
            model="dall-e-3",
            prompt=prompt,
            n=1,
            size="1024x1024",
            quality="standard"
        )
        
        image_url = response.data[0].url
        return image_url
    
    except Exception as e:
        print(f"❌ Error generating art: {e}")
        sys.exit(1)

def download_and_save_image(image_url, kitsune_type):
    """Lataa kuvan ja tallenna se kitsune_art/ -kansioon."""
    
    try:
        # Generoi uniikki nimi
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        name_prefix = random.choice(KITSUNE_NAMES)
        filename = f"{name_prefix}_{kitsune_type}_{timestamp}.png"
        
        filepath = os.path.join('kitsune_art', filename)
        
        # Lataa kuva
        print(f"\n📥 Lataa kuva ({image_url[:50]}...)...")
        response = requests.get(image_url)
        response.raise_for_status()
        
        # Tallenna PNG:ksi
        with open(filepath, 'wb') as f:
            f.write(response.content)
        
        print(f"✅ Kuva tallennettu: {filepath}")
        return filepath
    
    except Exception as e:
        print(f"❌ Error downloading/saving image: {e}")
        sys.exit(1)

def print_kitsune_info(kitsune_type):
    """Tulosta Kitsune-tyypin tiedot."""
    if kitsune_type in KITSUNE_TYPES:
        info = KITSUNE_TYPES[kitsune_type]
        print(f"\n🦊 {info['name']}")
        print(f"   Tyyli: {info['style']}")

def main():
    """Pää-funktio argparse:lla."""
    
    parser = argparse.ArgumentParser(
        description='🦊 Kitsune Art Generator - Generoi AI-pohjaisia Kitsune-taideteoksia',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Esimerkkejä:
  %(prog)s --type fire
  %(prog)s --type dark --specs "9-tailed fox with crimson fur"
  %(prog)s --type ice --specs "ice shards surrounding the kitsune"

Saatavilla olevat tyypit: fire, dark, ice, demon, spirit, sacred
        """
    )
    
    parser.add_argument(
        '--type',
        type=str,
        required=True,
        choices=list(KITSUNE_TYPES.keys()),
        help='Kitsune-tyyppi (fire, dark, ice, demon, spirit, sacred)'
    )
    
    parser.add_argument(
        '--specs',
        type=str,
        default=None,
        help='Lisää ominaisuudet (esim. "9-tailed fox with golden eyes")'
    )
    
    args = parser.parse_args()
    
    # Generoi taide
    image_url = generate_kitsune_art(args.type, args.specs)
    
    # Lataa ja tallenna
    filepath = download_and_save_image(image_url, args.type)
    
    # Tulosta tiedot
    print_kitsune_info(args.type)
    
    print(f"\n" + "="*70)
    print(f"✨ Kitsune-taide luotu onnistuneesti!")
    print(f"📁 Tallennus: {filepath}")
    print(f"="*70 + "\n")

if __name__ == "__main__":
    main()
