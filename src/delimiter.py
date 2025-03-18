from textnode import *
def split_nodes_delimiter(old_nodes, delimiter, text_type):
	new_nodes = []

	for old_node in old_nodes:
        # If node isn't TEXT type, just add it as-is
		if old_node.text_type != TextType.TEXT:
			new_nodes.append(old_node)
			continue

        # Handle text nodes by searching for delimiter pairs
		text = old_node.text
        # ... (search for delimiter pairs logic)
		start_index = text.find(delimiter)
		if start_index == -1: # No delimiter found
			new_nodes.append(old_node)
			continue

		end_index = text.find(delimiter, start_index + len(delimiter))
		if end_index == -1:
			raise Exception(f"No closing delimiter found for {delimiter}")

		before_text = text[:start_index]
		delimited_text = text[start_index+len(delimiter):end_index]
		after_text = text[end_index + len(delimiter):]

		if before_text:
			new_nodes.append(TextNode(before_text, TextType.TEXT))
		if delimited_text:
			new_nodes.append(TextNode(delimited_text, text_type))
		if after_text:
			temp_node = TextNode(after_text, TextType.TEXT)
			result_nodes = split_nodes_delimiter([temp_node], delimiter, text_type)
			new_nodes.extend(result_nodes)

	return new_nodes

