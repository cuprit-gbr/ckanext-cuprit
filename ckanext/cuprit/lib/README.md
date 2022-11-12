# Updating Custom tags

The tags used with cKAN come from http://thesauri.dainst.org/


1. Use the script https://github.com/dainst/iqvoc_skosxl/blob/master/dai_scripts/complete_export.py
to export all thesauri data to thesauri.json.
1. run  `python3 thesauri2tags.py` to create a new pickle file
1. push the data to github
2. rebuild the cKAN container
