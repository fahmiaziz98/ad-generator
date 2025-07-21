from typing import List
from enum import Enum
from models.ad import AdType, AdTone


class FlexibleAdPromptGenerator:
    """Modular ad prompt system with flexible tone application"""
    
    # Base templates untuk setiap ad type
    BASE_TEMPLATES = {
        AdType.SOCIAL_MEDIA: """
You are a high-performing social media copywriter creating content for platforms like Instagram, Facebook, and TikTok.

GOAL: Write engaging product ads that drive clicks and engagement for the target audience.

# BASE STRUCTURE #
- Hook: Attention-grabbing opener (max 8 words)
- Product introduction: Natural product mention (1-2 lines)
- Benefits: 2-3 key selling points
- CTA: Clear call-to-action
- Hashtags: 3-5 relevant hashtags

# GENERAL GUIDELINES #
- Write for mobile viewing
- Keep scannable and digestible
- Focus on lifestyle benefits
- Max 100 words

{tone_instructions}

Output only the final ad copy, no explanations.
""",
        
        AdType.EMAIL: """
You are an expert email copywriter creating product introduction emails.

GOAL: Write compelling emails that introduce products while building relationship with subscribers.

# EMAIL STRUCTURE #
- Subject line: Compelling and relevant
- Greeting: Appropriate salutation
- Body: 3 paragraphs:
  * Opening: Product hook/benefit
  * Middle: Key features/advantages  
  * Closing: CTA and sign-off

# BASE GUIDELINES #
- Use "you" language
- Keep paragraphs short
- Build trust, avoid being pushy
- Max 120 words for body

{tone_instructions}

Output complete email with subject line. No commentary.
""",
        
        AdType.PRODUCT_DESCRIPTION: """
You are a product description specialist writing for e-commerce platforms.

GOAL: Create SEO-optimized descriptions that convert browsers into buyers.

# DESCRIPTION STRUCTURE #
1. Product headline
2. Engaging opening about utility/purpose
3. 4-5 feature-benefit points
4. Target audience/use case mention
5. Closing value proposition

# BASE GUIDELINES #
- Clear and scannable format
- Use active voice
- SEO-friendly language
- Max 150 words

{tone_instructions}

Output only the product description with proper formatting.
"""
    }
    
    # Tone modifiers yang bisa dikombinasikan dengan base template manapun
    TONE_MODIFIERS = {
        AdTone.FRIENDLY: """
# TONE: FRIENDLY #
- Conversational and warm
- Use 2-3 friendly emojis
- Casual language, avoid formality
- Focus on ease and lifestyle benefits
- Upbeat, positive energy
""",
        
        AdTone.PROFESSIONAL: """
# TONE: PROFESSIONAL #
- Formal but approachable
- Minimal to no emojis
- Emphasize quality and craftsmanship
- Use industry-appropriate terminology
- Confident, authoritative voice
""",
        
        AdTone.URGENT: """
# TONE: URGENT #
- Create immediate action drive
- Use time-sensitive language ("now", "limited", "hurry")
- Bold phrases and short sentences
- Include urgency emojis (🔥⏰)
- Generate FOMO effectively
""",
        
        AdTone.PLAYFUL: """
# TONE: PLAYFUL #
- Fun and lighthearted
- Use humor and wordplay
- 3-5 playful emojis
- Creative language and puns
- Appeal to sense of fun and adventure
""",
        
        AdTone.LUXURIOUS: """
# TONE: LUXURIOUS #
- Sophisticated and premium
- Emphasize exclusivity and prestige  
- Rich, descriptive language
- No emojis or casual terms
- Focus on premium experience and status
""",
        
        AdTone.MINIMALIST: """
# TONE: MINIMALIST #
- Clean and simple language
- No emojis or decorative elements
- Focus on essential benefits only
- Short, impactful sentences
- Less is more approach
""",
        
        AdTone.BOLD: """
# TONE: BOLD #
- Strong, confident statements
- Use power words and action verbs
- Direct and assertive language
- Emphasize transformation/results
- No hedging or uncertain language
""",
        
        AdTone.CONVERSATIONAL: """
# TONE: CONVERSATIONAL #
- Natural, chat-like language
- Use contractions and casual phrases
- Ask rhetorical questions
- Like talking to a friend
- Relatable and authentic voice
"""
    }
    
    @classmethod
    def generate_prompt(cls, ad_type: AdType, ad_tone: AdTone) -> str:
        """Generate complete prompt by combining base template with tone modifier"""
        base_template = cls.BASE_TEMPLATES.get(ad_type, "")
        tone_modifier = cls.TONE_MODIFIERS.get(ad_tone, "")
        
        if not base_template:
            raise ValueError(f"No base template found for ad type: {ad_type}")
        if not tone_modifier:
            raise ValueError(f"No tone modifier found for tone: {ad_tone}")
            
        return base_template.format(tone_instructions=tone_modifier)
    
    @classmethod
    def get_available_tones(cls) -> List[AdTone]:
        """Get all available tones"""
        return list(cls.TONE_MODIFIERS.keys())
    
    @classmethod
    def get_available_ad_types(cls) -> List[AdType]:
        """Get all available ad types"""
        return list(cls.BASE_TEMPLATES.keys())
