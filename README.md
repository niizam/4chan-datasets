# 4chan-datasets
Example of how to use:
1. Clone the [HF repo](https://huggingface.co/datasets/niizam/4chan-datasets)
2. Use `merge.py` to merge text files, for example:
```
python merge.py -d repo/pol -o pol-merged.txt
````
3. Then turn `pol-merged.txt` into json/csv format
```
python tokenizer.py pol-merged.txt pol-dataset.json
or
python tokenizer.py pol-merged.txt pol-dataset.csv
```
