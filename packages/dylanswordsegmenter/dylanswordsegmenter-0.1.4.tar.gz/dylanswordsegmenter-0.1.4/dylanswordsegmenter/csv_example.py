import csv
from dylanswordsegmenter import dp_segment_with_longest_match, to_pascal_case

# Input and output CSV file paths
INPUT_CSV = "input_words.csv"  # Replace with your actual input file
OUTPUT_CSV = "output_words.csv"

# Read words from CSV file
def read_words_from_csv(input_csv):
    words = []
    with open(input_csv, mode="r", encoding="utf-8") as file:
        reader = csv.reader(file)
        for row in reader:
            if row:  # Skip empty rows
                words.append(row[0].strip())  # Assuming words are in the first column
    return words

# Write results to CSV file
def write_results_to_csv(output_csv, results):
    with open(output_csv, mode="w", encoding="utf-8", newline="") as file:
        writer = csv.writer(file)
        writer.writerow(["Original Word", "PascalCase"])  # Headers
        writer.writerows(results)

# Process words and generate output
def process_words(input_csv, output_csv):
    words_list = read_words_from_csv(input_csv)
    results = []

    for word in words_list:
        pascal_case = to_pascal_case(dp_segment_with_longest_match(word))
        results.append([word, pascal_case])

    write_results_to_csv(output_csv, results)
    print(f"✅ Processed {len(results)} words. Output saved to {output_csv}")

# Run the script
if __name__ == "__main__":
    process_words(INPUT_CSV, OUTPUT_CSV)

