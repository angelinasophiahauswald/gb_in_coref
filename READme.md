# Testing Coreferee on Gender Bias



## Setting Up Virtual Enviroment

- Install a Virtualenv
 `pip3 install virtualenv`
- Create python virtual enviroment
 `python -m venv .venv`
- Activate virtual enviroment
 `source .venv/bin/activate`
- Install requirements from requirements.txt
 `pip3 install -r requirements.txt`

## Function description
### preprocess_data
This function takes the folder name as input and creates the foler 'output' if it doesn't exist already, it then stores the coreference resolution in a txt-file (in each line the original sentence, then a colon and then the result of the coref system)

### correct_false
This function takes the xxx_output.txt file as input and creates the correct_false folder inside the output folder. It then checks if the coreference resolution result is the same as the expected entity and writes the original file with CORRECT or FALSE in a txt-file.

### evaluate
This function takes xxx_output_cf.txt as input and counts the amount of correct and false resolved sentences and writes the statistic at the end of the file.

### prepare_analysis
This function takes [model]_output_cf.txt file as input and creates a new directory for that file with the same name as the file. It stores inside that new directory a file with only the correct results and one for false results (to better analyse the data later).

## Explanation of Folders
- `data`: location of all the data files 
- `output/ChatGPT`: location of all the results of ChatGPT for every dataset
- `output/[...]_output.txt-files`: output-file of Coreferee without checking if it is correct or not
- `output/correct_false/`: contains txt-files indicating if the resolution was correct/false and a folder for every data set containing one file of that dataset with only correctly resolved sentences, and a second file with every falsely resolved sentence
