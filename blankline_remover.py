import os

def progress_bar(iteration, length=20):
    percent = iteration / 1385
    bar_length = int(length * percent)
    bar = '#' * bar_length + '-' * (length - bar_length)
    print(f'\r[{bar}] {iteration}/{1385}', end='', flush=True)

cosem_dir = os.path.join(os.getcwd(), 'CoSEM_v5')
#file_path = "CoSEM_v5/COSEM_v5_chunk_80.txt"

chunk_num = 1
while True:
    progress_bar(chunk_num)
    chunk_file = os.path.join(cosem_dir, 'COSEM_v5_chunk_' + str(chunk_num) + '.txt')
    if not os.path.exists(chunk_file):
        break # no more files
        
    with open(chunk_file, "r") as f:
        # Create a temporary file to store non-blank lines
        temp_file_path = chunk_file + ".temp"
        with open(temp_file_path, "w") as temp_f:
            for line in f:
                if line.strip():  # Only write non-blank lines
                    temp_f.write(line)

    # Replace the original file with the cleaned version
    os.replace(temp_file_path, chunk_file)
    chunk_num += 1