# coding: utf8
import index
import pickle as pkl

if __name__ == "__main__":
	with open('index', 'r') as f:
	    term_doc = pkl.load(f)
	term_doc = index.to_compression(term_doc)
	term_offset_size = index.to_varbyte_to_file(term_doc, 'index')
	#print term_offset_size
	with open('control', 'w') as f:
	    pkl.dump(term_offset_size, f)
	#print term_doc[u'системы']

