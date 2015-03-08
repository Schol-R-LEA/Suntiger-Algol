
# part of the Suntiger Algol project
# initiated 2008:05:23, by Joseph Osako, Jr. <josephosako@gmail.com>
# file last modified 2015:03:08


from typecheck import typecheck
from tokens import Token


lits = dict()
curr_reg = 3
label_count = 0


def addlit(tok):
	global lits
	# first, see if it is already in list, and if so, reuse the label
	for test in lits:
		if lits[test].value() == tok.value():
			return test
	# not already there, create a new one
	label = "lit" + str(len(lits))
	lits[label] = tok
	return label


@typecheck
def get_label(brtype: str) -> str:
	global label_count
	label = brtype + '.' + str(label_count)
	label_count += 1
	return label


def get_temp():
	global curr_reg, label_count
	if curr_reg <= 8:
		temp = '$t' + str(curr_reg)
		curr_reg += 1
	else:
		tempOffset -= 4
		temp = tempoffset + currOffset
	return temp


def free_temps():
	global curr_reg, label_count
	curr_reg = 3
	tempoffset = 0
