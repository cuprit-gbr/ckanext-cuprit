# Updateing Custom tags

The tags used with cKAN come from http://thesauri.dainst.org/
Use the script https://github.com/dainst/iqvoc_skosxl/blob/master/dai_scripts/complete_export.py
to export thesauri data to thesauri.json.

Then:

1. use thesauri2tags.py to create a new pickle file
2. push the data to github
3. rebuild the ckan container
