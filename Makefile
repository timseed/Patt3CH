test1:
	python3 SkimPattern.py format1.lst

test2:
	python3 SkimPattern.py format2.lst

test3:
	python3 SkimPattern.py format3.lst

test1p:
	python3 SkimPattern.py format1.lst MASTERPLUS.SCP

test2p:
	python3 SkimPattern.py format2.lst MASTERPLUS.SCP

test3p:
	python3 SkimPattern.py format3.lst MASTERPLUS.SCP

buildmaster:
	python3 PatternBuilder.py MASTER.SCP

buildmasterplus:
	#cat MASTER.SCP calls.txt |sort | uniq > MASTERPLUS.SCP
	python3 PatternBuilder.py MASTERPLUS.SCP


all:
	test1
	test2
	test3