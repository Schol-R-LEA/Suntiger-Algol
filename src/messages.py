# part of the Suntiger Algol project
# initiated 2008:05:23, by Joseph Osako, Jr. <JoeJr@osakoweb.com>
# file last modified 2010:01:11

import sys

""" This module handles most user output, specifically error
messages and listing messages."""

################
## error messages
symtab = None
listing = None
out = None

def error_handlers(st, lst, dest):
	""" Sets up module-level global state and returns
	closure functions."""
	global symtab, listing, out
	symtab = st
	listing = lst
	out = dest

	def error(tok, message):
		""" output an error message and close compiler.
		
		This function is used for recovering from fatal errors.
		It does four things: it prints out the error message
		to both standard output and the listing file, writes
		a copy of the symbol table to the listing (for debugging),
		clears the object file, and closes listing and object files.
		"""
		global symtab, listing, out
		if tok is None or tok.type() == 0:
			msg = "ERROR: Unexpected End of File"
		else:
			msg = "ERROR line " + str(tok.line()) + ': ' + repr(tok) + message
		print(msg)
		listing.write('\n\n***' + msg + '***\n\n')
		listing.write(str(symtab)) # write the symtab to the listing file
		listing.close()
		out.truncate(0)		# destroy the output file
		out.close()
		sys.exit(1)

	def warning(tok, message):
		""" output a warning message.
		
		This is used for non-fatal errors. It prints the
		error message to standard out and returns to the compiler.
		"""
		print("\nwarning", repr(tok), message)
		
	# return the closures for error and warning
	return error, warning


################
## listing messages

from tokens import Token
step = ''
nl = False
		
def lister(listing):
	""" Binds the global listing file locally and return the listing function.
	"""
	def prefix(num):
		""" Utility function to generate the spacing for the line numbers.
		
		This returns a string of spaces, equal the number of digits
		in the highest expected line number (arbitrarily set at 9999)
		minus to the number of digits in the actual line number. This
		is used to keep the lines from drifting right as the line numbers
		increase.
		"""
		s = str(num)
		if (num < 1000):
			s = ' ' + s
		if (num < 100):
			s = ' ' + s
		if (num < 10):
			s = ' ' + s
		return s

	def print_listing(tok):
		""" Print a formatted listing of the current token.
		
		The main function of this is to print the current token to
		both standard output and the listing file. However, it also
		will indent the lines automagically based on the nesting; it
		keeps a running figure for the indentation, and sets it
		as the indicator tokens appear in the input stream. All
		tokens except literal strings are converted to upper case.
		"""
		global step, nl
		indents = [Token.BEGINTOK, Token.DOTOK, Token.THENTOK, Token.ELSETOK]
		dedents = [Token.ELSETOK, Token.ENDTOK, Token.ODTOK, Token.FITOK]
		
		if tok.type() in dedents:
			step = step[0:-3]
		if nl:
			line = prefix(tok.line())
			print('\n' + line + ':' + step, end=' ')
			listing.write('\n' + line + ': ' + step)
			nl = False
		lexeme = tok.value()
		if tok.type() != Token.STRINGLIT:
			lexeme = lexeme.upper()
		listing.write(lexeme + ' ')
		print(lexeme, end=' ')
		if tok.type() in indents:
			step = step + '   '
		if tok.type() == Token.SEMI or tok.type() in indents:
			nl = True

	print('   1:', end=' ')
	listing.write('   1: ')
	return print_listing
