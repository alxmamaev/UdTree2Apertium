# UdTree2Apertium
Converter for tags from UD-tree bank to Apertium format.

## How it is work
To convertig tags you need create csv tags dict for your language (look to `tags/rus.csv`).
Then just run the program: <br>`python3 converter.py sict_file.csv input_ud_corpus.conllu output_apertium_file.apertium`

## Example
```bash
alxmamaev@alxmamaev-pc MINGW32 ~/Projects/UdTree2Apertium (master)
$ python converter.py tags/rus.csv test.conllu test.apertium
^Ровно/ровно<adv><pst>$
^в/в<pr>$
^десять/десять<num><acc>$
^часов/час<n><nn><gen><m><pl>$
^раздался/раздаваться<vblex><m><sg><past><midv>$
^короткий/короткий<adj><nom><pst><m><sg>$
^звонок/звонок<n><nn><nom><m><sg>$
^./.<sent>$
```
