from .document import Document
import re
from soynlp.normalizer import repeat_normalize
import logging

logger = logging.getLogger(__name__)

# https://github.com/YongWookHa/kor-text-preprocess/blob/master/src/clean.py
# https://github.com/monologg/KoELECTRA/blob/master/docs/preprocessing.md

class PreProcessing(Document):
    def __init__(self, args):
        Document.__init__(self, args)
        self.min_length = args.min_length
        self.is_news = args.news
        self.is_datetime = args.datetime
        self.sub1 = re.compile(r'[^ .,?!/@$%~％·∼()\x00-\x7F가-힣]+') # 한글/영어 및 띄어쓰기, 특수기호 일부를 제외한 모든 글자
        self.sub2 = re.compile(r'[\s]+')  # white space duplicate
        self.sub3 = re.compile(r' ?[\.]+')  # full stop duplicate
        self.sub4 = re.compile(r' ?[,]+ ?( ?,)+ ?')  # comma duplicate
        self.spe_char1 = re.compile(r'[·"]') # special characters replace with \s
        self.spe_char2 = re.compile(r' ?[<>\\*] ?') # special characters replace with ''

    def apply(self):
        self.lines = self.split_by_period()
        self.remove_en_sent()
        self.clean()
        self.lines = list(dict.fromkeys(self.lines))
        self.remove_parantheses()
        self.remove_list()
        self.remove_links()
        self.remove_unmatched_items()
        self.remove_repeat()
        if self.is_datetime: self.remove_datetime()
        if self.is_news: self.remove_news_brackets()
        self.lines = [l.strip('-').strip('=').strip('/').strip('*').strip() for l in self.lines if len(l) > self.min_length]
        self.write_lines()

    def clean(self):
        new_lines=[]
        for line in self.lines:
            cleaned = self.sub1.sub('', line.strip())
            cleaned = self.spe_char1.sub(' ',cleaned)
            cleaned = self.spe_char2.sub('',cleaned)
            cleaned = self.sub2.sub(' ', cleaned)
            cleaned = self.sub3.sub('.', cleaned)
            cleaned = self.sub4.sub(', ', cleaned)
            if len(cleaned) > self.min_length:
                new_lines.append(cleaned.strip())
        self.lines = self.split_by_punct(new_lines)

    def remove_en_sent(self):
        KOR = re.compile('[가-힣]')
        self.lines = [l for l in self.lines if KOR.search(l)]
    
    def remove_list(self):
        LIST = re.compile(r'.*[XVI|0-9][\.|\)]')
        self.lines = [l for l in self.lines if not LIST.match(l)]
    
    def remove_parantheses(self):
        PARANTHESES = re.compile(r"\([^()]*\)")
        self.lines = [PARANTHESES.sub('',l) for l in self.lines]    

    def remove_news_brackets(self):
        NEWS_BRACKETS = re.compile(r"(\[.+기자\])")
        # NEWS_EQUAL = re.compile(r".*(기자) ?= ?/")
        # NEWS_EQUAL2 = re.compile(r".*(AP|AFP|EPA|사진제공|News|뉴스|사진)=[^ ]+ ")
        self.lines = [NEWS_BRACKETS.sub('',l) for l in self.lines]  
        # self.lines = [NEWS_EQUAL.sub('',l) for l in self.lines]
        # self.lines = [NEWS_EQUAL2.sub('',l) for l in self.lines] 

    def remove_links(self):
        LINKS = re.compile(r"(www.|html|http|.com|.co|.kr|class|span|br|p/)")
        self.lines = [l for l in self.lines if not LINKS.search(l)] 
    
    def remove_unmatched_items(self):
        UNMATCHED_ITEMS = re.compile(r'[\[\]\(\)] ?')
        self.lines = [UNMATCHED_ITEMS.sub('',l) for l in self.lines]  
    
    def remove_repeat(self):
        self.lines = [repeat_normalize(l, num_repeats=2) for l in self.lines]

    def remove_datetime(self):
        DATETIME = re.compile(r'([0-9]{2,4}-[0-9]{2,4}-[0-9]{2} ?)(.*:[0-9]{2})?')
        self.lines = [DATETIME.sub('',l) for l in self.lines]  


if __name__ == "__main__":
    pass