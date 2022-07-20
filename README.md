# Exif_Tool-1.0

This project was created in python3.9.

Functionality: What this program does currently is take a JPEG and outputs all of the JPEG's EXIF tag information but only on IFD0 (Still a WIP). It gives out the tags name and the tags description. The way i made this program is by reading in the image but in bytes and then from the i used the TIFF specification to extract the tag information. Setting up the tag information was a little tricky, since there are a lot of exif tags and I needed to find a way to implement them i decided the best way was to set up a script that scraped the data off a table from https://exiftool.org/TagNames/EXIF.html. Using this I fed all that information into a text document and used that text document to help aid my program.

Overall this was a really cool project and there are still things i want to finish with this program. I want it to eventually go through all IFDs and i also want to create a decent looking GUI that will show the picture on the side. The main thing i want to add is Values but there is a lot to do if i want to add values. Currently the program can actually pull values but it was too complicated and time consuming to add them in the right format so I left it for another day. Overall creating this taught me how to extract data from websites, gave me a deeper understanding of EXIF and also the TIFF specification.
