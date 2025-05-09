from enum import Enum

class BlockType(Enum):
	PARAGRAPH = "paragraph"
	HEADING = "heading"
	CODE = "code"
	QUOTE = "quote"
	UNORDERED = "unordered_list"
	ORDERED = "ordered_list"

class TextType(Enum):
	TEXT = "text"
	BOLD = "bold"
	ITALIC = "italic"
	CODE = "code"
	LINK = "link"
	IMAGE = "image"

class TextNode():
	def __init__(self, text, text_type, url=None, alttext=None):
		self.text = text
		self.text_type = text_type
		self.url = url
		self.alt = alttext

	def __eq__(self, target):
		return self.text == target.text and self.text_type == target.text_type and self.url == target.url


	def __repr__(self):
		return f"TextNode({self.text}, {self.text_type}, {self.url})"
