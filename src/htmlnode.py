class HTMLNode():
	def __init__(self, tag=None, value=None, children=None, props=None):
		self.tag = tag
		self.value = value
		self.children = children
		self.props = props

	def to_html(self):
		raise NotImplementedError

	def props_to_html(self):
		html_props = ""
		for key in self.props:
			html_props = html_props + f' {key}="{self.props[key]}"'
		return html_props

	def __repr__(self):
		return f"HTMLNode({self.tag},{self.value},{self.children},{self.props})"

class LeafNode(HTMLNode):
	def __init__(self, tag, value, props=None):
		super().__init__(tag, value, None, props)

	def to_html(self):
		if self.value == None:
			raise ValueError("no value")
		if self.tag == None:
			return self.value
		if self.props != None:
			return f"<{self.tag}{HTMLNode.props_to_html(self)}>{self.value}</{self.tag}>"
		else:
			return f"<{self.tag}>{self.value}</{self.tag}>"

class ParentNode(HTMLNode):
	def __init__(self, tag, children, props=None):
		super().__init__(tag, None, children, props)

	def to_html(self):
		if self.tag is None:
			raise ValueError("missing tag")
		if self.children is None:
			raise ValueError("where my kids!?!?")
		if self.props is not None:
			html = f"<{self.tag}{HTMLNode.props_to_html(self)}>"
		else:
			html = f"<{self.tag}>"

		for child in self.children:
			html = html + child.to_html()
		html = html + f"</{self.tag}>"
		return html
