import os
import shutil
from htmlnode import *
from textnode import *
from delimiter import *
from convert import *
def extract_title(markdown):
	lines = markdown.split("\n")
	for line in lines:
		if line.startswith("# "):
			return line[2:].strip()
		if line.startswith("#") and not line.startswith("##"):
			return line[1:].strip()
	raise Exception("No h1 header found in the markdown")

def generate_page(from_path, template_path, dest_path, basepath="/"):
	with open(from_path, 'r') as file:
		md = file.read()
	with open(template_path, 'r') as file:
		template = file.read()
	title = extract_title(md)
	print(f"generating {title} from {from_path} to {dest_path} using {template_path}")
	html_node = markdown_to_html_node(md)
	html = html_node.to_html()
	full_html = template.replace("{{ Title }}", title).replace("{{ Content }}", html).replace('href="/', f'href="{basepath}').replace('src="/',f'src="{basepath}')
	dest_dir = os.path.dirname(dest_path)
	if dest_dir:
		os.makedirs(dest_dir, exist_ok=True)
	with open(dest_path, 'w') as file:
		file.write(full_html)

def generate_pages_recursive(dir_path_content, template_path, dest_dir_path, basepath="/"):
	for item in os.listdir(dir_path_content):
		item_path = os.path.join(dir_path_content, item)
		if os.path.isfile(item_path) and item_path.endswith('.md'):
			basename = os.path.splitext(item)[0]
			dest_file_path = os.path.join(dest_dir_path, basename + '.html')
			generate_page(item_path, template_path, dest_file_path, basepath)
		else:
			new_dest_dir = os.path.join(dest_dir_path, item)
			os.makedirs(new_dest_dir, exist_ok=True)
			new_source_dir = item_path
			generate_pages_recursive(new_source_dir, template_path, new_dest_dir, basepath)
