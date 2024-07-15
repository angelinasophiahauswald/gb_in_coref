import coreferee, spacy
import sys
import os
import re

def preprocess_data(data_directory):
    spacy_model = ''
    # create output directory
    directory = "output"
    if not os.path.exists(directory):
        os.makedirs(directory)
    else:
        print(f"Directory '{directory}' already exists") 

    for filename in os.listdir(data_directory):
        if os.path.isfile(os.path.join(data_directory, filename)):
            if 'english' in filename:
                spacy_model = 'en_core_web_trf'
                nlp = spacy.load('en_core_web_trf')
                nlp.add_pipe('coreferee')
            elif 'german' in filename:
                spacy_model = 'de_core_news_lg'
                nlp = spacy.load('de_core_news_lg')
                nlp.add_pipe('coreferee')

        prepare_file_name = re.search(r"(.*?)\.txt", filename).group(1)
        file_name = "output/{}_{}_output.txt".format(prepare_file_name, spacy_model)    
        output = open(file_name, "a")

        with open('data/'+filename, 'r') as file:
            for line in file:
                if line == '\n':
                    output.write("\n")
                    continue
                clean = line
                clean = clean.replace("[", "")
                clean = clean.replace("]", "")
                doc = nlp(clean)
                #print(doc)
                #print(doc._.coref_chains)
                output.write("{} : {}\n".format(line.replace("\n", ""), doc._.coref_chains.resolve(doc)))
        file.close()
        output.close()

def correct_false(result): 
    directory = "output/correct_false"
    if not os.path.exists(directory):
        os.makedirs(directory)
    else:
        print(f"Directory '{directory}' already exists") 
    prepare_file_name = re.search(r"output/(.*?)\.txt", data).group(1)
    file_name = "output/correct_false/{}_cf.txt".format(prepare_file_name)
    res_file = open(file_name, "a")
    with open(result, 'r') as file:
        for line in file:
            if line == '\n':
                res_file.write('\n')
                continue
            sentence = []
            coref_pattern = r':(.*)'
            before_colon = re.findall(r'^.*(?=:)', line)[0]
            pattern_coref_resolution = re.findall(r'\[.*?\]', before_colon) # ['[The developer]', '[she]']
            # List of words to exclude
            excluded_english_words = ['she', 'he', 'his', 'her', 'him']
            excluded_german_words = ['sie', 'er', 'seine', 'seiner', 'seines', 'ihr', 'ihre', 'ihres']
            if "english" in result:
                for candidate in pattern_coref_resolution:
                    candidate = candidate.replace('[', '').replace(']', '')
                    if candidate not in excluded_english_words:
                        sentence.append(candidate)
            elif "german" in result:
                for candidate in pattern_coref_resolution:
                    candidate = candidate.replace('[', '').replace(']', '')
                    if candidate not in excluded_german_words:
                        sentence.append(candidate)
            coref = re.search(coref_pattern, line)
            # If a match is found, print the captured group
            if coref and sentence:
                result_sentence = sentence[0]
                result_coref = coref.group(1).strip()
                result_coref = result_coref.replace("[", "").replace("]", "")
                if result_coref in result_sentence:
                    res_file.write("{}\t{}\n".format(line.strip(),'CORRECT'))
                    #print(result_coref, result_sentence, "CORRECT")
                else:
                    res_file.write("{}\t{}\n".format(line.strip(),'FALSE'))
                    #print(result_coref, result_sentence, "FALSE")
    file.close()

def evaluate(data):
    correct_counter = 0
    false_counter = 0
    data_points = 0

    with open(data, 'r') as file:
        lines = file.readlines()
        for line in lines:
            if line == "\n":
                continue
            elif "CORRECT" in line:
                correct_counter += 1
                data_points += 1
            elif "FALSE" in line:
                false_counter += 1
                data_points += 1

    with open(data, 'a') as file:  # Open in append mode here
        file.write("\n")
        file.write("CORRECT: {}\n".format(correct_counter))
        file.write("FALSE: {}\n".format(false_counter))
        file.write("TOTAL: {}\n".format(data_points))

    '''print("CORRECT: ", correct_counter)
    print("FALSE: ", false_counter)
    print("TOTAL: ", data_points)'''

    file.close()
    return file

def prepare_analysis(cf_file):
    # übergeordneten Ordner erstellen
    directory_name = re.search(r"(.*)\.txt$", cf_file).group(1)
    if not os.path.exists(directory_name):
        os.makedirs(directory_name)
    else:
        print(f"Directory '{directory_name}' already exists") 

    # correct und false dateien erstellen
    correct = open(directory_name+'/correct.txt', 'a')
    false = open(directory_name+'/false.txt', 'a')

    with open(cf_file, 'r') as file:
        for line in file:
            if 'CORRECT' in line:
                correct.write(line) 
            elif 'FALSE' in line:
                false.write(line)
            elif '\n' in line:
                correct.write('\n')
                false.write('\n')
    file.close()
    correct.close()
    false.close()
    return correct, false

if __name__ == '__main__':
    data = sys.argv[1]      # path to data
    # takes the folder name as input
    # creates the foler 'output' if it doesn't exist already
    # stores the coreference resolution in a txt-file (in each line the original sentence, then a colon and then the result of the coref system)
    ###preprocess_data(data)

    # takes the xxx_output.txt file as input
    # creates the correct_false folder inside the output folder
    # checks if the coreference resolution result is the same as the expected entity
    # writes the original file with CORRECT or FALSE in a txt-file
    correct_false(data)

    # takes xxx_output_cf.txt as input
    # counts the amount of correct and false resolved sentences and writes the statistic at the end of the file
    ###evaluate(data)

    # takes [model]_output_cf.txt file as input
    # creates a new directory for that file with the same name as the file
    # stores inside that new directory a file with only the correct results and one for false results
    ###prepare_analysis(data)

