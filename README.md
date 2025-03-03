# CoSEM to AntConc Metadata Mapper

[The Corpus of Singapore English Messages (CoSEM)](https://github.com/wdwgonzales/CoSEM) contains nearly 900,000 lines of text messaging, along with metadata tags containing demographic information about the sender. This project is intended to be used in order to automate the reformatting I required to correctly load the corpus into [AntConc](https://www.laurenceanthony.net/software/antconc/) for analysis. 

The following sections include the software needed to make this project work, the steps required to successfully load CoSEM into AntConc, an explanation for how to use the metadata in searches, and may be updated to include a simple command-line python script to ease the generation of the SQL queries needed.

## Dependencies
This project requires:
- the download and unzipping of the corpus chunks found in [The Corpus of Singapore English Messages (CoSEM)](https://github.com/wdwgonzales/CoSEM),
- [AntConc](https://www.laurenceanthony.net/software/antconc/) to load and make use of the corpus,
- [Python3](https://www.python.org/) to run the formatting scripts,
- and access to a Unix shell to run a shell script.

The basic usage of these are explained below.

## Usage
### 1. Download the CoSEM
Download corpus_COESEM_v5.zip from the [CoSEM repository](https://github.com/wdwgonzales/CoSEM?tab=readme-ov-file). Unzip it, and place the CoSEM_v5 folder inside this project. **Note:** these steps will make slight changes to the files, so you can make a copy of the files, should you need them.

The file structure should look like this:

    CoSEM Mapper/
      ├─ blankline_remover.py
      ├─ CoSEM_v5/
      ├─ README.md
      ├─ run_formatting.sh
      └─ setup.py 
        
### 2. Run Formatting
All formatting can be run using the `run_formatting.sh` shell script. Simply enter `sh run_formatting.sh` your Unix shell, while in the project directory.

Once the full script has run, the file system should look like this (new files marked with an asterisk (*)):

    CoSEM Mapper/
      ├─ blankline_remover.py
      ├─ CoSEM_v5/
      ├─ demographic_metadata.tsv*
      ├─ README.md
      ├─ run_formatting.sh
      └─ setup.py 

### 3. Create Corpus
Launch [AntConc](https://www.laurenceanthony.net/software/antconc/) and open the Corpus Manager: File>Open Corpus Manager or `Ctrl+O`. 

Under Corpus Source, select Raw File(s). Under Raw Files Corpus Builder, you can optionally enter a new corpus name, before clicking Add File(s) and selecting all of the files inside the `CoSEM_v5` folder, or Add Directory and selecting the folder itself. Alternatively you can drag and drop the files into the window below the buttons.

Under Basic Settings you want to change Row Processor to `One text per row`. Under Advnced Options>Metatable Tables(s), either click Add File(s) and add the `demographic_metadata.tsv` file, or drag and drop it into the window below the buttons.

At the bottom of the Corpus Manager window, there is a Create button, which will start processing the input files and create the corpus. Once it is done, you can also save the corpus as a `.db` file, which can be useful if you want to open the corpus again later. Simply click the Save (to file) button on the right.

Once done you can select Corpus Database under Corpus Source, and you will be able to see your new corpus under User (List). You may need to double click it in order to open the corpus. Once done, you can click the Return to Main Window button.

### 4. Using the Corpus
I have no idea what one does with a corpus, but now you can do it *with metadata!*

You can use the metadata extracted from the messages using the Adv Search checkbox next to the search box. Enter a word, and check the box. A new window will open.

At the bottom, check the SQL Search box, and here you will be able to add conditions based on the metadata. The basic formula is `["demographic_metadata", "<condition>", "doc_id"]`. Once you've entered it into the textbox, click Add, or press `Enter`, to add it to the list. All items in the list will be used to filter the search. You can right click an item in order to remove it from the list.

Once you've added the formula(s), click Apply to save the changes and close the window. Pressing Start in the main window will start the search. To disable the advanced search, simply uncheck the Adv Search checkbox.

You are able to filter using the following metadata:
- `age`
- `nationality`
- `race`
- `gender`
- `year`

`age` and `year` can be entered simply as integers. `nationality` and `race` is entered using a (seemingly quite) standardized two character country code in a string format (like this `'<code>'`), e.g. `'SG'` for Singaporean, `'IN'` for Indian, and so on, as described by Gonzales et al. on page 6 (376) in the [CoSEM Overview Paper](https://github.com/wdwgonzales/CoSEM/blob/main/Overview%20paper/Gonzales%20et%20al.%20-%202023%20-%20The%20Corpus%20of%20Singapore%20English%20Messages%20(CoSEM).pdf). `gender` is similarly entered using a one character code in a string format, e.g. `'F'` for female, `'M'` for male. Unknown values seem to be entered as `'XX'` or `'X'`, respectively.

#### Example conditions:
1. In order to filter for messages sent by 21-year-olds, you would enter `["demographic_metadata", "age = 21", "doc_id"]`.
2. In order to filter for messages sent by Singaporean nationals, you would enter `["demographic_metadata", "nationality = 'SG'", "doc_id"]`.
3. In order to filter for messages sent by Indians you would enter `["demographic_metadata", "race = 'IN'", "doc_id"]`.
4. In order to filter for messages sent by men, you would enter `["demographic_metadata", "gender = 'M'", "doc_id"]`.
5. In order to filter for messages sent by 25-year-old Singaporean nationals from China, you would enter both `["demographic_metadata", "age = 25", "doc_id"]`, `["demographic_metadata", "nationality = 'SG'", "doc_id"]` and `["demographic_metadata", "race = 'CH'", "doc_id"]`.

SQL allows for comparisons that aren't just equality. You can also use `<>` to check for inequality (e.g. if age *is not* 21) `<`, and `<=`, `>`, and `>=` to compare for age and year (e.g. age is *greater than* 21). It may not be super useful for this particular dataset, but SQL also allows searches for *similar* strings using wildcards - `%` for *any number* of symbols, and `_` for *one* symbol - e.g. `race LIKE 'C%'` will include Chinese `CH`, Chinese-Indian `CI`, and Chinese-Malay `CM` in the search results.

For more information on the specifics of the SQL queries, see [this discussion on the AntConc Google Group](https://groups.google.com/g/AntConc/c/Si5EdVrIddE), specifically the replies from Laurence Anthony.

