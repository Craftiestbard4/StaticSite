import sys
from textnode import *
import os
import shutil
from htmlnode import *
from textnode import *
from delimiter import *
from convert import *
from markdown_parser import *
basepath = "/"
if len(sys.argv)>1:
	basepath = sys.argv[1]
def copy_static():
	if os.path.exists("docs"):
		shutil.rmtree("docs")
	os.mkdir("docs")
	copy_directory("static", "docs")

def copy_directory(source, destination):
	for item in os.listdir(source):
		source_path = os.path.join(source, item)
		dest_path = os.path.join(destination, item)
		if os.path.isfile(source_path):
			print(f"copying file: {source_path} to {dest_path}")
			shutil.copy(source_path, dest_path)
		else:
			print(f"Creating directory: {dest_path}")
			os.makedirs(dest_path, exist_ok=True)
			copy_directory(source_path, dest_path)

def main():
	copy_static()
	generate_pages_recursive("content", "template.html", "docs", basepath)
	print(basepath)
main()
