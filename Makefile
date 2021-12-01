test1:
	python3 SkimPattern.py format1.lst

test2:
	python3 SkimPattern.py format2.lst

test3:
	python3 SkimPattern.py format3.lst

all:
	test1
	test2
	test3