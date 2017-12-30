# UdTree2Apertium
This utility will help you to convert UdTree files to Apertium format.

## How it is work
First you need to get a raw Apertium file.
Example for english:
```
cat en-ud-train.conllu | grep -e '^$' -e '^[0-9]' | cut -f2 | sed 's/$/¶/g' | apertium-destxt | lt-proc -w ~/source/apertium//languages/apertium-eng/eng.automorf.bin | apertium-retxt | sed 's/¶//g' > en-ud-train.apertium
```


Then you need to run this utility:
```
python converter.py tags/eng.csv en-ud-train.apertium en-ud-train.conllu eng.tagged
```

## Example
```bash
alxmamaev@alxmamaev-pc MINGW32 ~/Projects/UdTree2Apertium (master)
$ python converter.py tags/rus.csv ru-ud-train.apertium ru-ud-train.conllu rus.tagged
^Al/Al<np><ant><m><sg>$
^-/-<guio>$
^Zaman/Zaman<np><cog><sg>$
^:/:<sent>$
^American/American<adj>$
^forces/force<n><pl>$
```
