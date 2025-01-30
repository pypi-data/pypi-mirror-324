from graphviz import Source
from pleenok.model.attack_tree import AttackTree, Node, Gate, GateType, NodeType


def _border_for_node(node: Node) -> str:
	if node.node_type == NodeType.DEFENSE:
		return "#00AA00"
	else:
		return "#DD0000"

def generate_dot(at: AttackTree) -> str:
	gates_definitions = []
	basic_events_definitions = []
	relationships = []
	countermeasure_relations = []
	sequence_relationships = []
	subgraphs = []
	visited = set()

	def traverse(node: Node, parent_id: str = None):
		nonlocal gates_definitions, basic_events_definitions, relationships, sequence_relationships, subgraph
		node_id = node.get_id()
		if node_id in visited:
			return  # Skip already visited nodes
		visited.add(node_id)

		node_color = _border_for_node(node)
		if isinstance(node, Gate):
			if node.label is not None:
				gates_definitions.append(f"""
	n{node_id} [
		margin = 0,
		fillcolor = transparent,
		shape = plaintext,
		label = <
			<table border="0" cellpadding="8" cellspacing="0">
			  <tr>
				<td color="{node_color}" colspan="3" bgcolor="#F0F0F0" border="2"><font color="#000000" point-size="14" face="Calibri,Arial,sans-serif">{node.label}</font></td>
			  </tr>
			  <tr>
				<td></td>
				<td bgcolor="#666666" port="op" border="1" color="#000000" height="20"><font color="#FFFFFF" point-size="10" face="Consolas,monospace">{node.gate_type.value}</font></td>
				<td></td>
			  </tr>
			</table>> ];""")
			else:
				gates_definitions.append(f"\tn{node_id} [label=\"{node.gate_type.value}\"];")
			subgraph = []
			for child in node.children:
				child_id = child.get_id()
				source = f"n{child_id}"
				target = f"n{node_id}"
				if not isinstance(child, Gate):
					source += ":lbl:n"
				if node.label is not None:
					target += ":op"

				relationships.append(f"\t{source} -> {target};")
				traverse(child, node_id)

			if node.gate_type == GateType.SEQUENCE_AND:
				for i in range(len(node.children) - 1):
					c1 = node.children[i]
					c2 = node.children[i + 1]
					c1_id = "n" + c1.get_id()
					c2_id = "n" + c2.get_id()
					sequence_relationships.append(f"{c1_id} -> {c2_id}")
					subgraphs.append([f"{c1_id} {c2_id} "])
		else:
			if node.label is None:
				basic_events_definitions.append(f"\tn{node_id} [label=<<i>No action</i>>,shape=\"plain\",color=\"#ffffff\",fillcolor=\"#ffffff\"];")
			else:
				basic_events_definitions.append(f"\tn{node_id} [label=<<table border=\"0\" cellpadding=\"8\" cellspacing=\"0\"><tr><td port=\"lbl\" color=\"{node_color}\" bgcolor=\"#F0F0F0\" border=\"2\"><font color=\"#000000\" point-size=\"14\" face=\"Calibri,Arial,sans-serif\">{node.label}</font></td></tr><tr><td height=\"20\"><font point-size=\"10\"> </font></td></tr></table>>];")

		# adding node countermeasures
		for countermeasure in node.countermeasures:
			countermeasure_id = countermeasure.get_id()
			source = f"n{countermeasure_id}"
			target = f"n{node_id}"
			countermeasure_relations.append(f"\t{source} -> {target};")
			traverse(countermeasure, node_id)

	traverse(at.root)

	dot = """
digraph AttackTree {
	ranksep = 0.5
	outputorder = "edgesfirst"
	rankdir = "BT"
	ordering = in
	splines = polyline
	
	node [
		color = "#000000"
		fillcolor = "#666666"
		fontcolor ="#FFFFFF"
		shape = "box"
		style = "filled"
		fontname = "Consolas,monospace"
		fontsize = 10
		height = 0.4
	]
"""
	dot += "\n".join(gates_definitions) + "\n"
	dot += """
	node [
		color = "#DD0000"
		fillcolor = "transparent"
		fontcolor ="#000000"
		shape = "plaintext"
		style = "filled"
		fontname = "Calibri,Arial,sans-serif"
		fontsize = 14
		height = 0.5
		margin = 0
	]
"""
	dot += "\n".join(basic_events_definitions) + "\n"
	dot += """
	edge[
		dir = "none"
	]
"""
	dot += "\n".join(relationships) + "\n"
	dot += """
	edge[
		style = "dashed"
		color = "#AAAAAA"
		headclip = "false"
		tailclip = "false"
	]
	"""
	dot += "\n\t".join(sequence_relationships) + "\n"
	for subgraph in subgraphs:
		dot += f"\n	{{ rank=same; {' '.join(subgraph)} }}"
	dot += """
	edge[
		style = "dashed"
		color = "#666666"
	]
	"""
	dot += "\n\t".join(countermeasure_relations) + "\n"
	dot += "\n}"
	return Source(dot)
