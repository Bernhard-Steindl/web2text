#!/bin/bash
# usage single file:
# ./to_utf8.sh MyFile.txt
# all files in folder:
# find /your/folder/here | xargs -n 1 ./to_utf8.sh
# https://stackoverflow.com/questions/11316986/how-to-convert-iso8859-15-to-utf8/44677555#44677555


TO="UTF-8"; FILE=$1
FROM=$(file -i $FILE | cut -d'=' -f2)
echo "file detected FROM=$FROM"
if [[ $FROM = "binary" ]]; then
 echo "Skipping binary $FILE..."
 exit 0
fi

iconv -f $FROM -t $TO -o $FILE.tmp $FILE; ERROR=$?
if [[ $ERROR -eq 0 ]]; then
  echo "Converting $FILE..."
  mv -f $FILE.tmp $FILE
  # use -i on linux for file:
  RESULT_TYPE=$(file -i $FILE | cut -d'=' -f2)
  echo "Resulting file is according to file cmd: $RESULT_TYPE"
else
  echo "Error on $FILE"
fi