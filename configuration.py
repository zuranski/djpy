from supy.defaults import *
from supy import whereami

def mainTree():
	return ("djTree","tree")

def experiment():
	return "cms"

def cppFiles() :
    return [whereami()+"/../cpp/dict.cpp"]
