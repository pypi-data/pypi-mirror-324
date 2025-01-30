import nltk
from nltk.corpus import words


# Check if the words corpus is available, and download it if missing
try:
    valid_words = set(words.words())  # Try to load words corpus
except LookupError:
    print("NLTK words corpus not found. Downloading now...")
    nltk.download('words')  # Download only if missing
    valid_words = set(words.words())  # Load again after downloading

# Add common abbreviations and domain-specific terms to the valid words set
custom_words = {
    "cust", "vend", "info", "dim", "trans", "tax", "docu",
    "prod", "dlv", "paym", "spec", "meta", "sales", "line",
    "delete", "price", "disc", "table", "term", "jour", "purch", 
    "packing", "calc", "eco", "res", "link", "parm", "invent",
    "slip", "markup"
}
valid_words.update(custom_words)

def dp_segment_with_longest_match(word):
    n = len(word)
    dp = [(None, 0)] * (n + 1)  # (segments, score)
    dp[0] = ([], 0)
    
    # Handle the case where the entire word is valid
    if word.lower() in valid_words:
        return [word.lower()]
    
    for i in range(1, n + 1):
        best_segments = None
        best_score = -1
        
        for j in range(i):
            word_segment = word[j:i].lower()
            
            # Skip single-letter segments unless they're at the start of a capitalized word
            if len(word_segment) == 1 and not (j == 0 and word[0].isupper()):
                continue
                
            # Check if this segment is a custom word or valid word
            is_custom = word_segment in custom_words
            is_valid = word_segment in valid_words or word_segment in {'a', 'i'}  # Allow 'a' and 'i' as valid segments
            
            if is_custom or is_valid:
                prev_segments, prev_score = dp[j]
                if prev_segments is not None:
                    # Score calculation: prioritize custom words and longer segments
                    # Significantly increase the penalty for short segments
                    length_score = len(word_segment) ** 2  # Square the length to favor longer segments
                    word_type_score = 3 if is_custom else (2 if len(word_segment) > 2 else 0.5)
                    total_score = prev_score + (length_score * word_type_score)
                    
                    # Additional penalty for creating too many segments
                    segment_count_penalty = len(prev_segments) * 0.1
                    total_score -= segment_count_penalty
                    
                    if total_score > best_score:
                        best_score = total_score
                        best_segments = prev_segments + [word_segment]
        
        dp[i] = (best_segments, best_score)
    
    result = dp[n][0]
    if result is None:
        # Fallback for unmatched segments
        return [word]
    return result

# Convert segmented words to PascalCase
def to_pascal_case(segmented_words):
    return ''.join(word.capitalize() for word in segmented_words)

