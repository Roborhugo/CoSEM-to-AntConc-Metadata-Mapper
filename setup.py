import os
import re
import csv
import argparse
import time

# ----------------- Argument Parsing -----------------

# include an optional argument flag to specify if we want to make
# copies of the files without the tags
parser = argparse.ArgumentParser(description="A script to extract tags from CoSEM files.")
parser.add_argument("--clean_copies", "-c", action="store_true", help="Create clean copies of the files without tags.")

args = parser.parse_args()

if args.clean_copies:
    print("Extracting metadata from CoSEM tags and creating copies exluding tags.")
else:
    print("Extracting metadata from CoSEM tags.")
    print("Use the -c flag to create clean copies of the files without tags.")


def progress_bar(iteration, length=20):
    percent = iteration / 1385
    bar_length = int(length * percent)
    bar = '#' * bar_length + '-' * (length - bar_length)
    print(f'\r[{bar}] {iteration}/{1385}', end='', flush=True)

# ----------------- File Paths and Files -----------------

# define the path to the current directory
current_dir = os.getcwd()
if(args.clean_copies):
    # define the path to the directory where we will store the clean copies
    clean_copies_dir = os.path.join(current_dir, 'clean_copies')
    # create the clean_copies directory if it does not exist
    if not os.path.exists(clean_copies_dir):
        os.makedirs(clean_copies_dir)

# define the path to the AntConc directory
cosem_dir = os.path.join(os.getcwd(), 'CoSEM_v5')

# define the path to the output TSV file
output_file_path = os.path.join(current_dir, 'demographic_metadata.tsv')
# create the output file
output_file = open(output_file_path, 'w', newline='')
# create a csv writer object
writer = csv.writer(output_file, delimiter='\t')
# write the header row
writer.writerow(['doc_id', 'age', 'nationality', 'race', 'gender', 'year'])


# ----------------- Extracting Metadata -----------------

# iterate through all .txt files in the AntConc directory, in order
# "COSEM_v5_chunk_#.txt", where # is the chunk number
chunk_num = 1
doc_id = 0
start = time.time()
while True:
    progress_bar(chunk_num)
    chunk_file = os.path.join(cosem_dir, 'COSEM_v5_chunk_' + str(chunk_num) + '.txt')
    if not os.path.exists(chunk_file):
        break # no more files

    # open the chunk file
    f = open(chunk_file, 'r')
    
    # read the file line by line
    for line in f:    
        tag = re.search(r'<<COSEM:.*>>', line)

        # if tag is not None, extract the metadata
        # if tag is none, this line belongs to the same message
        # and so it has the same metadata
        if tag is not None:
            tag = tag.group(0)
            tag = tag.replace('\u202C', "") # occassionally the tag has a weird character
            tag = tag.split('-')

            age = tag[2][0:2]
            nationality = tag[2][2:4]
            race = tag[2][4:6]
            gender = tag[2][6]
            year = tag[3][0:4]

        if (nationality[0] == '\u202C'):
            print(chunk_num)
            quit()
        # add to tsv file
        writer.writerow([doc_id, age, nationality, race, gender, year])

        # if we want to create clean copies of the files without tags
        # Do as follows: Create a new file named
        # "COSEM_v5_chunk_#_<doc_id>.txt" and write the line in it
        if args.clean_copies:
            # create file if it does not exist
            clean_copy_file = os.path.join(clean_copies_dir, 'COSEM_v5_chunk_' + str(chunk_num) + '_' + str(doc_id) + '.txt')
            clean_copy = open(clean_copy_file, 'w')
            clean_copy.write(line)
            clean_copy.close()

        doc_id += 1





    chunk_num += 1

print("\nFinished extracting metadata.")

end = time.time()

print('Time taken:', end - start)
print("Number of documents:", doc_id)