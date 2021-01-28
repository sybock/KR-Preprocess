import os
import re 
import gzip
import logging

logger = logging.getLogger(__name__)

class Document():
    def __init__(self, args):
        '''
        in_path: path of input file
        out_path: path of output file. set as '/' if you want to overwrite input file
        '''
        self.in_path = args.input
        self.out_path = args.output
        self.lines = self._read_lines()
        logger.info(f'Total lines in file before cleaning: {len(self.lines):,}')

    def _read_lines(self):
        logger.info(f'Reading file {self.in_path}')
        if self.in_path.endswith('.gz'):
            with gzip.open(self.in_path,'rt') as f:
                lines = f.readlines()
        else:
            with open(self.in_path, 'r') as f:
                lines = f.readlines()
        return [l.strip() for l in lines if l != '\n' and l.strip() != '']        
    
    def split_by_period(self):
        doc = ' '.join(self.lines)
        doc = doc.replace('. ', '.\n')
        doc = doc.replace('? ', '?\n')
        doc = doc.replace('! ', '!\n')
        return doc.splitlines(True)

    def split_by_punct(self, lines_list):
        doc = ' '.join(lines_list)
        PERIOD = re.compile(r'(?<!([A-Z]))\. +')
        doc = PERIOD.sub('.\n', doc)
        doc = doc.replace('? ', '?\n')
        doc = doc.replace('! ', '!\n')
        return doc.splitlines(True)

    def write_lines(self):
        if not os.path.exists(os.path.split(self.out_path)[0]):
            os.makedirs(os.path.split(self.out_path)[0])
        logger.info(f'Total lines in file after cleaning: {len(self.lines):,}')
        logger.info(f'Writing cleaned file to {self.out_path}')
        doc = ''.join(self.split_by_punct(self.lines))
        if self.out_path.endswith('.gz'):
            with open(self.out_path,'wt') as o:
                o.write(doc)
        else:
            with open(self.out_path, "w") as o:
                o.write(doc)

if __name__ == "__main__":
    pass