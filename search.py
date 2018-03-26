#coding:utf8
import index
import sys
import pickle as pkl

def print_answer(request, answer, id_url):
    print request
    print len(answer)
    for docid in answer:
        print id_url[str(docid)]



if __name__ == "__main__":
    with open('index', 'r') as f:
        ids = bytearray(f.read())
    with open('control', 'r') as f:
        term_offset_size = pkl.load(f)
    with open('docid_url', 'r') as f:
        id_url = pkl.load(f)
    
    requests = sys.stdin.read().strip().split('\n')
    for request in requests:
        answer = index.find_easy_request(request, ids, term_offset_size)
        print_answer(request, answer, id_url)



