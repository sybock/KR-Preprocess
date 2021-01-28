
def extract_text(in_path,out_path,start_marker,end_marker):
    with open(in_path,'r') as r:
        is_text = False
        with open(out_path,'w') as o:
            for line in r:
                if line.strip() == start_marker: is_text = True; continue
                elif line.strip() == end_marker: is_text = False
                if is_text and line.strip() != '' and not line.startswith('<'):
                    o.write(line)

