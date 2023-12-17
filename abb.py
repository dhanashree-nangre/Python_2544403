#import libraries
import pandas as pd
import warnings
import os

# To reset warnings to their default behavior (optional)
warnings.resetwarnings()

# Function to load letter values from a file
def load_letter_values():
    letter_values = {}
    with open("values.txt", "r") as values_file:
        for line in values_file:
            letter, value = line.strip().split()
            letter_values[letter] = int(value)
    return letter_values

# Function to calculate the weight of a character based on its position and rarity value from file
def weight_of_character(word, letter,letter_index):
    letter_values = load_letter_values()
    #For first character of word, return 0
    if letter_index==0:
        return 0
    #Condition to check last character and E
    elif letter == word[-1]:
        if letter != 'E':
            return 5
        else:
            return 20
    #Get score for middle chracter
    else:
        rarity_value = letter_values.get(letter, 0)
        return (letter_index + rarity_value)
    
# Function to get the word at a specific character index in a sentence        
def get_word_at_index(sentence, index):
    words = sentence.split()
    current_index = 0

    for word in words:
        word_length = len(word)
        if current_index + word_length > index:
            return word,current_index
        current_index += word_length + 1  # +1 for the space between words

    return None

# Function to calculate the score of an abbreviation
def calculate_score(name, abbreviation, position):
    score = 0
    second_letter_details = get_word_at_index(name,position[0])
    score += weight_of_character(second_letter_details[0],abbreviation[1],position[0]-second_letter_details[1])
    third_letter_details = get_word_at_index(name,position[1])
    score += weight_of_character(third_letter_details[0],abbreviation[2],position[1]-third_letter_details[1])
    return score

# Function to get possible combinations of abbreviations for a name
def get_possible_combinations_of_abbreviations(input_string):
    first_char = input_string[0]
    combinations_with_positions={}
    for i in range(1,len(input_string)-1):
        if input_string[i].isalpha():
            for j in range(i+1,len(input_string)):
                if input_string[j].isalpha():
                    #check if same abbreviation is there
                    if (first_char+input_string[i]+input_string[j]) in combinations_with_positions:
                        continue
                    else:
                        combinations_with_positions[(first_char+input_string[i]+input_string[j])]=[i,j]
    return combinations_with_positions

#main function
def main():
    input_filename = input("Enter the input file name (e.g., names.txt): ")
    surname = input("Enter your surname: ")
    output_filename = f"{surname}_{input_filename.replace('.txt', '')}_abbrevs.txt"  

    # Create a DataFrame to store scores
    scores=pd.DataFrame(columns=['name','abbreviation','score'])
    names = []

    # Read names from the input file
    with open(input_filename, "r") as input_file:
        names = [line.strip() for line in input_file]
    
    # Process each name and calculate scores
    for name in names:
        name_upper=name.upper()
        name_abbreviations = get_possible_combinations_of_abbreviations(name_upper)
        for key,value in name_abbreviations.items():
            score= calculate_score(name_upper,key,value)
            scores=scores.append({'name':name,'abbreviation':key,'score':score}, ignore_index=True)
    # Drop duplicate abbreviations and convert 'score' to numeric
    scores=scores[~scores['abbreviation'].duplicated(keep=False)]
    # Get rows with the minimum score for each name
    scores['score'] = pd.to_numeric(scores['score'], errors='coerce')
    result_df = scores.loc[scores.groupby(['name'])['score'].idxmin()]
    # Write the result DataFrame to a CSV file
    result_df.to_csv(f"{input_filename.replace('.txt', '')}_abbrevs.csv")
    # Merge rows based on name and write to a text file
    merged_df = result_df.groupby('name').apply(lambda group: ', '.join(group['abbreviation'])).reset_index(name='merged_abbreviations')
    merged_df.to_csv(output_filename, sep='\t', index=False)
    # Check if the file exists before deleting it
    if os.path.exists(output_filename):
        os.remove(output_filename)
        print(f"The file '{output_filename}' has been deleted.")
    with open(output_filename, 'a') as file:
        for name in names:
            row_with_name = merged_df.loc[merged_df['name'] == name]
            if not row_with_name.empty:
                file.writelines(row_with_name.to_string(index=False,header=False) + '\n')
            else:
                file.write(name+'\n')

            
    
if __name__ == "__main__":
    main()
