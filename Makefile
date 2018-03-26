all:
	./index.sh varbyte dataset/lenta.ru_159b9f4b-972b-48b1-8ec3-44fbd6be33c4_01.gz 
	./make_dict.sh
	./search.sh < test.txt

tar:
	tar -cvzf index.tar.gz index.sh index.py make_dict.sh make_dict.py search.sh search.py doc2words.py docreader.py document_pb2.py document.proto