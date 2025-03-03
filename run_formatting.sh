# runs all formatting scripts in the correct order

# Usage: newline_remover.sh

# iterates through all files in the CoSEM_v5 directory, 
# and removes all empty lines, except the one at the very end
python3 blankline_remover.py

# iterates through all files in the CoSEM_v5 directory,
# removes the final empty row
for filename in CoSEM_v5/*.txt; do
    truncate -s-1 $filename
done

# iterates through all files in the CoSEM_v5 directory,
# and generate the .tsv file containing all lines' metadata
python3 setup.py

# all done!
echo "Formatting done."