#!/usr/bin/python

# part of the Suntiger Algol project
# initiated 2008:05:23, by Alice Osako <alicetrillianosako@gmail.com>
# file last modified 2022:02:11

class DuplicateSymbolException (Exception):
	"""Exception indicating a duplicate SymbolTable entry"""
	def __init__(self, key, context):
		self.__key = key
		self.__context = context
		
	def getKey(self):
		"""Accessor for the key of the duplicate entry"""
		return self.__key

	def getContext(self):
		"""Accessor for the context in which the compiler
		tried to add a duplicate entry"""
		return self.__context

	def __repr__(self):
		"""Create string representation of the DuplicateSymbolException
		
		Returns the default error message.
		"""
		return "Duplicate declaration of identifier " + self.__key + \
		" in block " + self.__context


class NestingException (Exception):
	def __init__(self, entry, exit):
		self.__entry = entry
		self.__exit = exit
	
	def getEntry(self):
		return self.__entry

	def getExit(self):
		return self.__exit

	def __repr__(self):
		"""Create string representation of the NestingException
		
		Returns the default error message.
		"""
		return "Mismatched block nesting between " \
		+ self.__entry + " and " + self.__exit


class BottomOfTableStackException (Exception):
	def __init__(self, table):
		self.__table = table
	
	def __repr__(self):
		"""Create string representation of the NonSymbolEntryException
		
		Returns the default error message.
		"""
		return self.__table + " is the root of the symbol table."


class NonSymbolEntryException (Exception):
	def __init__(self, entry):
		self._entry = entry
	
	def __repr__(self):
		"""Create string representation of the NonSymbolEntryException
		
		Returns the default error message.
		"""
		return str(type(entry)) + " is not a valid symbol type."

class KeywordException (Exception):
	def __init__(self):
		pass

	def __repr__(self):
		"""Create string representation of the KeywordException
	
		Returns the default error message.
		"""
		return "Could not create new keyword list."
