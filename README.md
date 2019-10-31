# zg-uni-file-renamer
Convert names of files from Zawgyi to Unicode in a given directory
Similar to file content converter from Zawgyi to Unicode (see https://github.com/lenaye/zawgyi-unicode-file-converter), this script will rename all files written in Zawgyi to Unicode (without affecting the actual contents of the files).

As before, the zg2uni Python function code snippet used in the script comes courtesy of Rabbbit Conveter: https://github.com/Rabbit-Converter/Rabbit

<b>Usage:</b><p>
<p>
><i>python zg-uni-file-renamer.py -s {source directory}</i>
<p>
This will scan the entire source directory and rename each file (regardless of the extension) to Unicode in the same directory.
