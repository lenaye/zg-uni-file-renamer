# -*- coding: utf-8 -*-
# Leonard Aye --- 2019
# zg2uni-file-renamer.py
# This script renames files created in ZG and renames them with unicode.
# The file content and file type remains untouched.

# This script uses Rabbit-Python function module from
# https://github.com/Rabbit-Converter/Rabbit
# Credit to Rabbit Converter team  for the zg2uni mapping rules source code

import os
import re
import argparse
import datetime

#Credit to Rabbit Converter team for this function
def zg2uni(text):
    rules = [
        { "from": u"(\u103d|\u1087)", "to": u"\u103e" }, { "from": u"\u103c", "to": u"\u103d" },
        { "from": u"(\u103b|\u107e|\u107f|\u1080|\u1081|\u1082|\u1083|\u1084)", "to": u"\u103c" },
        { "from": u"(\u103a|\u107d)", "to": u"\u103b" }, { "from": u"\u1039", "to": u"\u103a" },
        { "from": u"\u106a", "to": u"\u1009" }, { "from": u"\u106b", "to": u"\u100a" },
        { "from": u"\u106c", "to": u"\u1039\u100b" }, { "from": u"\u106d", "to": u"\u1039\u100c" },
        { "from": u"\u106e", "to": u"\u100d\u1039\u100d" }, { "from": u"\u106f", "to": u"\u100d\u1039\u100e" },
        { "from": u"\u1070", "to": u"\u1039\u100f" }, { "from": u"(\u1071|\u1072)", "to": u"\u1039\u1010" },
        { "from": u"\u1060", "to": u"\u1039\u1000" }, { "from": u"\u1061", "to": u"\u1039\u1001" },
        { "from": u"\u1062", "to": u"\u1039\u1002" }, { "from": u"\u1063", "to": u"\u1039\u1003" },
        { "from": u"\u1065", "to": u"\u1039\u1005" }, { "from": u"\u1068", "to": u"\u1039\u1007" },
        { "from": u"\u1069", "to": u"\u1039\u1008" }, { "from": u"/(\u1073|\u1074)/g", "to": u"\u1039\u1011" },
        { "from": u"\u1075", "to": u"\u1039\u1012" }, { "from": u"\u1076", "to": u"\u1039\u1013" },
        { "from": u"\u1077", "to": u"\u1039\u1014" }, { "from": u"\u1078", "to": u"\u1039\u1015" },
        { "from": u"\u1079", "to": u"\u1039\u1016" }, { "from": u"\u107a", "to": u"\u1039\u1017" },
        { "from": u"\u107c", "to": u"\u1039\u1019" }, { "from": u"\u1085", "to": u"\u1039\u101c" },
        { "from": u"\u1033", "to": u"\u102f" }, { "from": u"\u1034", "to": u"\u1030" },
        { "from": u"\u103f", "to": u"\u1030" }, { "from": u"\u1086", "to": u"\u103f" },
        { "from": u"\u1036\u1088", "to": u"\u1088\u1036" }, { "from": u"\u1088", "to": u"\u103e\u102f" },
        { "from": u"\u1089", "to": u"\u103e\u1030" }, { "from": u"\u108a", "to": u"\u103d\u103e" },
        { "from": u"([\u1000-\u1021])\u1064", "to": u"\u1004\u103a\u1039\\1" },
        { "from": u"([\u1000-\u1021])\u108b", "to": u"\u1004\u103a\u1039\\1\u102d" },
        { "from": u"([\u1000-\u1021])\u108c", "to": u"\u1004\u103a\u1039\\1\u102e" },
        { "from": u"([\u1000-\u1021])\u108d", "to": u"\u1004\u103a\u1039\\1\u1036" },
        { "from": u"\u108e", "to": u"\u102d\u1036" }, { "from": u"\u108f", "to": u"\u1014" },
        { "from": u"\u1090", "to": u"\u101b" }, { "from": u"\u1091", "to": u"\u100f\u1039\u1091" },
        { "from": u"\u1019\u102c(\u107b|\u1093)", "to": u"\u1019\u1039\u1018\u102c" },
        { "from": u"(\u107b|\u1093)", "to": u"\u103a\u1018" }, { "from": u"(\u1094|\u1095)", "to": u"\u1037" },
        { "from": u"\u1096", "to": u"\u1039\u1010\u103d" }, { "from": u"\u1097", "to": u"\u100b\u1039\u100b" },
        { "from": u"\u103c([\u1000-\u1021])([\u1000-\u1021])?", "to": u"\\1\u103c\\2" },
        { "from": u"([\u1000-\u1021])\u103c\u103a", "to": u"\u103c\\1\u103a" },
        { "from": u"\u1031([\u1000-\u1021])(\u103e)?(\u103b)?", "to": u"\\1\\2\\3\u1031" },
        { "from": u"([\u1000-\u1021])\u1031([\u103b\u103c\u103d\u103e]+)", "to": u"\\1\\2\u1031" },
        { "from": u"\u1032\u103d", "to": u"\u103d\u1032" }, { "from": u"\u103d\u103b", "to": u"\u103b\u103d" },
        { "from": u"\u103a\u1037", "to": u"\u1037\u103a" },
        { "from": u"\u102f(\u102d|\u102e|\u1036|\u1037)\u102f", "to": u"\u102f\\1" },
        { "from": u"\u102f\u102f", "to": u"\u102f" }, { "from": u"(\u102f|\u1030)(\u102d|\u102e)", "to": u"\\2\\1" },
        { "from": u"(\u103e)(\u103b|\u1037)", "to": u"\\2\\1" },
        { "from": u"\u1025(\u103a|\u102c)", "to": u"\u1009\\1" },
        { "from": u"\u1025\u102e", "to": u"\u1026" }, { "from": u"\u1005\u103b", "to": u"\u1008" },
        { "from": u"\u1036(\u102f|\u1030)", "to": u"\\1\u1036" },
        { "from": u"\u1031\u1037\u103e", "to": u"\u103e\u1031\u1037" },
        { "from": u"\u1031\u103e\u102c", "to": u"\u103e\u1031\u102c" },
        { "from": u"\u105a", "to": u"\u102b\u103a" },
        { "from": u"\u1031\u103b\u103e", "to": u"\u103b\u103e\u1031" },
        { "from": u"(\u102d|\u102e)(\u103d|\u103e)", "to": u"\\2\\1" },
        { "from": u"\u102c\u1039([\u1000-\u1021])", "to": u"\u1039\\1\u102c" },
        { "from": u"\u103c\u1004\u103a\u1039([\u1000-\u1021])", "to": u"\u1004\u103a\u1039\\1\u103c" },
        { "from": u"\u1039\u103c\u103a\u1039([\u1000-\u1021])", "to": u"\u103a\u1039\\1\u103c" },
        { "from": u"\u103c\u1039([\u1000-\u1021])", "to": u"\u1039\\1\u103c" },
        { "from": u"\u1036\u1039([\u1000-\u1021])", "to": u"\u1039\\1\u1036" },
        { "from": u"\u1092", "to": u"\u100b\u1039\u100c" }, { "from": u"\u104e", "to": u"\u104e\u1004\u103a\u1038" },
        { "from": u"\u1040(\u102b|\u102c|\u1036)", "to": u"\u101d\\1" },
        { "from": u"\u1025\u1039", "to": u"\u1009\u1039" },
        { "from": u"([\u1000-\u1021])\u103c\u1031\u103d", "to": u"\\1\u103c\u103d\u1031" },
        { "from": u"([\u1000-\u1021])\u103d\u1031\u103b", "to": u"\\1\u103b\u103d\u1031" }
    ]

    for rule in rules:
        text = re.sub(rule["from"], rule["to"], text)
    return text
#End of Rabbit Converter rule source code


def zg2unifilerename(directory):
    print(datetime.datetime.now())
    print('\nRenaming: ', end='')
    try:
        #For each file in a given directory convert each file to Unicode
        for zgfilename in os.listdir(directory):
            zgpath = directory +'\\'+zgfilename
            unifilename = zg2uni(zgfilename)
            unipath = directory+'\\'+unifilename
            os.rename(zgpath,unipath)
            print('.', end='')
    except FileNotFoundError as Error:
        print ('\n\nFile or Directory not found: ', Error)
    print('\n')

    print(datetime.datetime.now())


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Converts file names in Zawgyi to Unicode.')
    parser.add_argument("-s", "--source", required=True, help='Source directory')
    args = parser.parse_args()
    zg2unifilerename(args.source)
