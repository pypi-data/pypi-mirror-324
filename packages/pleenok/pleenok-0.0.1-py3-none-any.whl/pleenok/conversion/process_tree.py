from pm4py import ProcessTree
from pm4py.objects.process_tree.obj import Operator as PT_Operator
from pleenok.model.attack_tree import AttackTree, GateType, Gate, Node


def _process_tree_operators_to_attack_tree_operators(operator: str) -> str:
	if operator == PT_Operator.PARALLEL:
		return GateType.AND
	elif operator == PT_Operator.SEQUENCE:
		return GateType.SEQUENCE_AND
	elif operator == PT_Operator.XOR:
		return GateType.XOR
	elif operator == PT_Operator.OR:
		return GateType.OR
	else:
		raise Exception(f"Process Tree operator `{operator}' not supported")


def _attack_tree_operators_to_process_tree_operators(operator: str) -> str:
	if operator == GateType.AND:
		return PT_Operator.PARALLEL
	elif operator == GateType.SEQUENCE_AND:
		return PT_Operator.SEQUENCE
	elif operator == GateType.XOR:
		return PT_Operator.XOR
	elif operator == GateType.OR:
		return PT_Operator.OR
	else:
		raise Exception(f"Attack Tree operator `{operator}' not supported")


def process_tree_to_attack_tree(process_tree: ProcessTree) -> AttackTree:
	def traverse(pt: ProcessTree):
		if not pt.operator is None:  # the node is an operator
			gate = Gate(_process_tree_operators_to_attack_tree_operators(pt.operator))
			for child in pt.children:
				gate.add_child(traverse(child))
			return gate
		else:  # the node is an activity
			if pt.label is None:
				return Node(None)
			else:
				return Node(pt.label)
			
	return AttackTree(traverse(process_tree))


def attack_tree_to_process_tree_string(at: AttackTree) -> str:
	def traverse(at: Node):
		if isinstance(at, Gate):
			operator = _attack_tree_operators_to_process_tree_operators(at.gate_type)
			children = ",".join(traverse(node) for node in at.children)
			return f"{operator}({children})"
		else:
			if at.get_label() is None:
				return "tau"
			return "'" + at.get_label() + "'"

	return traverse(at.root)
