from pleenok.model.attack_tree import AttackTree, GateType, Node, Gate


def _attack_tree_operators_to_adtool(operator: str) -> str:
	if operator == GateType.AND:
		return "AND"
	elif operator == GateType.SEQUENCE_AND:
		return "SAND"
	elif operator == GateType.XOR:
		return "OR"
	elif operator == GateType.OR:
		return "OR"
	else:
		raise Exception(f"Attack Tree operator `{operator}' not supported")


def attack_tree_to_adtool_term(at: AttackTree) -> str:
	def traverse(at: Node):
		if isinstance(at, Gate):
			operator = _attack_tree_operators_to_adtool(at.gate_type)
			children = ",".join(traverse(node) for node in at.children)
			return f"{operator}({children})"
		else:
			return at.get_label()

	return traverse(at.root)
