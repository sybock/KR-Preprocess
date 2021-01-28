# KR-Preprocess
Preprocessing tool for Korean NLP tasks

## Overview

**Functions**
1. Removes all characters except essential punctuation and Korean/English characters
2. Removes lines with only English
3. Removes lines that are a part of a list (Begin with numeral + .)
4. Cleans lines by removing parantheses and the content inside of parantheses
5. Removes lines with links/html content
6. Removes unmatched parantheses and brackets
7. Cleans repeated items (아하하하하하하 -> 아하하)

**Options**

Pass these optional functions as booleans to argsparse
1. `--news`: Cleans news items in Korean web crawl text
2. `--datetime`:  Cleans date-time text (ex. 2020-12-12 13:44)

## Requirements
Refer to requirements.txt
```
pip install -r 'requirements.txt'
```

## Usage

```
# Get help with options
python3 main.py -h

# Example usage
python3 main.py -i /data/dataset.txt -o /data_cleaned/dataset.txt -m 10 --news True -dt True
```

- You can add your custom regex functions to main.py to customize code for certain types of text data that require extra cleaning. 

Example (in main.py):
```python
    args = parser.parse_args()
    txt = PreProcessing(args)
    # Add extra cleaning step to cleain html text '\br' from all lines with one line
    txt.lines = [l.replace('/br','') for l in txt.lines]
    txt.apply()
```


## References

https://github.com/YongWookHa/kor-text-preprocess
https://monologg.kr/2020/05/02/koelectra-part1/#%EC%A0%84%EC%B2%98%EB%A6%AC-Preprocessing 