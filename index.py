# coding: utf8
from docreader import DocumentStreamReader
from docreader import parse_command_line
from doc2words import extract_words
import struct

def make_dictionary_urlid():
    id_url = {}
    term_doc = {}
    reader = DocumentStreamReader(parse_command_line().files)
    i = 0
    for doc in reader:
        id_url[i] = doc.url
        for word in extract_words(doc.text):
            if not (word in term_doc):
                term_doc[word] = []
                term_doc[word].append(i)
            elif term_doc[word][len(term_doc[word])-1] != i:
                term_doc[word].append(i)
        i += 1
    return term_doc, id_url

def to_compression(dictionary):
    d_comp = {}
    for item in dictionary.items():
        d_comp[item[0]]  = []
        curid = 0
        for urlid in item[1]:
            comp_id = urlid - curid
            curid = urlid
            d_comp[item[0]].append(comp_id) 
    return d_comp

def uncompress(dictionary):
    d= {}
    for item in dictionary.items():
        d[item[0]]  = []
        curid = 0
        for urlid in item[1]:
            curid += urlid 
            d[item[0]].append(curid) 
    return d


def int_to_varbyte(integer, _bytearray):
    _integer = integer;
    store = []
    store.append(_integer % 128)
    _integer /= 128
    while _integer > 0:
        store.append(_integer % 128)
        _integer /= 128;

    for store_item in store[:0:-1]:
        _bytearray.append(store_item)

    _bytearray.append(store[0]+128)
    return _bytearray

def varbyte_to_int(_bytearray):
    # return value + size in byte in varbyte
    integers = []
    while(len(_bytearray) != 0):
        i = 0;
        if (_bytearray[0]) >= 128:
            integer = _bytearray[0] - 128
            _bytearray = _bytearray[1:];
            integers.append(integer)
            continue
        integer = _bytearray[0]
        i += 1
        while _bytearray[i] < 128:
            integer = integer * 128 +  _bytearray[i]
            i += 1
        integer = integer * 128 +  _bytearray[i] - 128
        _bytearray = _bytearray[i+1:]
        integers.append(integer)
    return integers

def to_varbyte_to_file(dictionary, filename):
    # return dict term_offset_size
    term_offset_size = {}
    offset = 0
    with open(filename, 'w') as file:
        for item in dictionary.items():
            term_inf = bytearray();
            #term_inf = int_to_varbyte(i, term_inf);
            for doc_id in item[1]:
                term_inf = int_to_varbyte(doc_id, term_inf)
            size = len(term_inf)
            term_offset_size[item[0]] = offset, size
            offset += size
            file.write(term_inf)
    return term_offset_size 


def store_dict( dictionary, file):
    with open(file, 'w') as f:
        for item in dictionary.items():
            f.write(item[0])
            for elem in item[1]:
                f.write(' ' + str(elem))
            f.write('\n')

def load_dict(file):
    d = {}
    with open(file, 'r') as f:
        for line in f:
            elems = line.split(' ')
            key = elems[0]
            elems = elems[1:]
            elems = map(lambda e: int(e,10), elems)
            d[key] = elems
    return d




def find_docid_by_term( terms ,term_offset_size, indexfile):
    term_docid = {}
    with open(indexfile, 'r') as f:
        a = bytearray(f.read())
    for term in terms:
        if (term_offset_size.get(term) != None):
            start = term_offset_size[term][0]
            end = term_offset_size[term][1] + start
            term_docid[term] = varbyte_to_int(a[start:end])
        else :
            term_docid[term] = []
    return term_docid
'''
def intersectCC( listdoccomp1, listdoccomp2):
    # compressed with compressed
    if (len(listdoccomp1) == 0 or len(listdoccomp2) == 0):
        return []
    listintersect = []
    idx1 = 0
    idx2 = 0
    value1 = 0
    value2 = 0
    ischange1 = True
    ischange2 = True
    while (idx1 != len(listdoccomp1) and idx2 != len(listdoccomp2)):
        if ischange1:
            value1 += listdoccomp1[idx1]
        if ischange2:
            value2 += listdoccomp2[idx2]
        if value1 == value2:
            listintersect.append(value1)
            idx1 += 1
            idx2 += 1
            ischange1 = True
            ischange2 = True
        elif value1 > value2:
            idx2 += 1
            ischange1 = False
            ischange2 = True
        else:
            idx1 += 1
            ischange1 = True
            ischange2 = False
    return listintersect

def intersectUC( listdoc1, listdoccomp2):
    # usual with compressed
    if (len(listdoc1) == 0 or len(listdoccomp2) == 0):
        return []
    listintersect = []
    idx1 = 0
    idx2 = 0
    value1 = 0
    value2 = 0
    ischange2 = True
    while (idx1 != len(listdoc1) and idx2 != len(listdoccomp2)):
        value1 = listdoc1[idx1]
        if ischange2:
            value2 += listdoccomp2[idx2]
        if value1 == value2:
            listintersect.append(value1)
            idx1 += 1
            idx2 += 1
            ischange2 = True
        elif value1 > value2:
            idx2 += 1
            ischange2 = True
        else:
            idx1 += 1
            ischange2 = False
    return listintersect
'''
def intersect( listdoc1, listdoc2):
    # usual with compressed
    if (len(listdoc1) == 0 or len(listdoc2) == 0):
        return []
    listintersect = []
    idx1 = 0
    idx2 = 0
    value1 = 0
    value2 = 0
    while (idx1 != len(listdoc1) and idx2 != len(listdoc2)):
        value1 = listdoc1[idx1]
        value2 = listdoc2[idx2]
        if value1 == value2:
            listintersect.append(value1)
            idx1 += 1
            idx2 += 1
        elif value1 > value2:
            idx2 += 1
        else:
            idx1 += 1
    return listintersect

def find_easy_request(request, fileindex, term_offset_size):
    terms = request.split('&')
    term_docid = find_docid_by_term(terms, term_offset_size, fileindex)
    term_docid = uncompress(term_docid)
    answer = []

    firsttime = True
    for item in term_docid.items():
        if not firsttime:
            answer = intersect(answer, item[1])
        else : 
            answer = item[1]
            firsttime = False

    return answer




'''
# TEST
d, urlid = make_dictionary_urlid()
i = 0
for item in d.items():
    print item[0], item[1], '\n'
    i += 1
    if i > 10:
        break
d = to_compression(d)
i = 0
for item in d.items():
    print item[0], item[1], '\n'
    i += 1
    if i > 10:
        break

d = uncompress(d)
i = 0
for item in d.items():
    print item[0], item[1], '\n'
    i += 1
    if i > 10:
        break

d = to_compression(d)


term_offset_size = to_varbyte_to_file(d, "Test")
#for item in d.items():
#    print item[0]
#for item in term_offset_size.items():
#    print item[0]
d = uncompress(d)
print d[u'системы']

answer = find_easy_request(u"системы & девятого", "Test", term_offset_size)
print len(d)
print answer
'''



if __name__ == '__main__':
    term_doc, id_url = make_dictionary_urlid()
    store_dict(term_doc, 'index')
    store_dict(id_url, 'Docid_url')
