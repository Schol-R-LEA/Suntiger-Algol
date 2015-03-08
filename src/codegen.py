
# part of the Suntiger Algol project
# initiated 2008:05:23, by Joseph Osako, Jr. <josephosako@gmail.com>
# file last modified 2015:03:08

import os, sys
from io import TextIOWrapper
from Symbol import *
from labels import lits
from tokens import Token
from SymbolTable import SymbolTable
from typecheck import typecheck

symtab = None
out = None

@typecheck
def codegen(st, dest: TextIOWrapper):
	global symtab, out, lits
	symtab = st
	out = dest

	def emit(output):
		""" Output a line of generated assembly code.
		"""
		out.write('\t' + output + '\n')
	
	def emit_prolog():
		""" Generate the start of the output file."""
		out.write('# Baby Algol output file ' + out.name + '\n\n')
		out.write('.text\n')
		out.write('.globl main\n')
		out.write('main:\n')
		emit('la $a0, ps')
		emit('li $v0, 4')
		emit('syscall')
		out.write('# Program Start\n\n')
	
	def emit_epilog():
		""" Generate the end of the output file."""
		global lits
		out.write("\n# Program End\n")
		emit('la $a0, pe')
		emit('li $v0, 4')
		emit('syscall')
		emit('li $v0, 10\n\tsyscall')
		out.write('.data\n')
		emit('ps:\t.asciiz "RUNNING PROGRAM\\n"')
		emit('pe:\t.asciiz "\\nPROGRAM ENDED\\n"')
		emit('nl:\t.asciiz "\\n"')
		emit('sFalse:\t.asciiz\t"FALSE"')
		emit('sTrue:\t.asciiz\t"TRUE"')
		emit('boolLookup:\t.word\tsFalse, sTrue\n')
		emit('charSwap:\t.space 1')
		emit('\t.byte 0')
		out.write('.align 4\n\n')

		# insert the labels and data for the literals
		for label in lits:
			lit = lits.get(label)
			out.write('\t' + label + ':')
			if lit.type() == Token.STRINGLIT:
				out.write('\t.asciiz\t' + lit.value() + '\n' \
				+ '.align 4\n')
			elif lit.type() == Token.CHARLIT:
				out.write('\t.asciiz\t\"' + (lit.value())[1] + '\"\n' \
				+ '.align 4\n')
			elif lit.type() == Token.BOOLLIT:
				if lit.value().upper() == 'TRUE':
					out.write('\t.byte\t1\n')
				else:
					out.write('\t.byte\t0\n')
				out.write('.align 4\n')
			else:
				out.write('\t.word\t' + lit.value() + '\n')



	def load(reg, location, ltype):
		"""Insert a load instruction based on reg name and a location
		
		This function is used for one of the most common operations
		in the MIPS set, namely, loading to a register. It is common
		enough and appears in enough places to justify a special function.
		Also, because of how constants are handled, it has to deal with
		both offsets and labels.
	"""
		emit("move " + reg + ", $zero")
		if isinstance(location, str):           # label or reg
			if location[0] == '$':          # register
				emit('move ' + reg + ', ' + location)
			else:
				emit("la $t0, " + location)
				if ltype in ["CHAR", "BOOLEAN"]:
					emit("lb " + reg + ", 0($t0)")
				else:
					emit("lw " + reg + ", 0($t0)")
		else:
			# offset
			if ltype in ["CHAR", "BOOLEAN"]:
				emit("lb " + reg + ", " + str(location) + "($sp)")
			else:
				emit("lw " + reg + ", " + str(location) + "($sp)")
			
	def store(reg, location, ltype):
		"""Insert a store instruction based on a reg name and a location
		
		This is the counterpart to load(), and is a separate function for
		the same reasons. However, it is somewhat simpler, as it does not
		have to handle the case of a constant label (for tolerably
		obvious reasons).
		"""
		if isinstance(location, str) and location[0] == '$':
			emit('move ' + location + ', ' + reg)
		else:
			out.write('\ts')
			if ltype in ["CHAR", "BOOLEAN"]:
				out.write('b')
			else:
				out.write('w')
			out.write(' ' + reg + ", " + str(location) + "($sp)\n")
			
	emit_prolog()
	return emit, emit_epilog, load, store

