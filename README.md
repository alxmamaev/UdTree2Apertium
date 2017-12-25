# UdTree2Apertium
Converter for tags from UD-tree bank to Apertium format.

## How it is work
To convertig tags you need create csv tags dict for your language (look to `tags/rus.csv`).
Then just run the program: <br>`python3 converter.py sict_file.csv aperium_parse_result.apertium input_ud_corpus.conllu output_apertium_file.appertium`

## Example
```bash
alxmamaev@alxmamaev-pc MINGW32 ~/Projects/UdTree2Apertium (master)
$ python converter.py tags/rus.csv test_apertium.tags test.conllu test.apertium
^Ровно/ровно<adv>$
^в/в<pr>$
^десять/десять<num><mfn><pl><acc>$
^часов/час<n><m><nn><pl><gen>$
^раздался/раздаваться$
^короткий/короткий<adj><sint><m><an><sg><nom>$
^звонок/звонок<n><m><nn><sg><nom>$
^./.<sent>$
```