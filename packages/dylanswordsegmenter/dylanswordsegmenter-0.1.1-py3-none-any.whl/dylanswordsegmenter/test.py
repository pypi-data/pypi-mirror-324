from dylanswordsegmenter import dp_segment_with_longest_match, to_pascal_case


words_list = [
    "commissioncalc",
    "commissionsalesgroup",
    "salesline",
    "saleslinedelete",
    "custtable",
    "salesrep"
]

for word in words_list:
    segmented = dp_segment_with_longest_match(word)
    pascal_case = to_pascal_case(segmented)
    print(f"Original: {word} -> Segmented: {segmented} -> PascalCase: {pascal_case}")

