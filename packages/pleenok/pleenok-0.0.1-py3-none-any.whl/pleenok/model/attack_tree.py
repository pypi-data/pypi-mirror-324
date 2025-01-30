from typing import List, Union
from enum import Enum
import uuid


class GateType(Enum):
	AND = "AND"
	SEQUENCE_AND = "S-AND"
	OR = "OR"
	XOR = "XOR"


class NodeType(Enum):
	ATTACK = "ATTACK"
	DEFENSE = "DEFENSE"


class Node:
	def __init__(self, label: str, node_type: NodeType = NodeType.ATTACK):
		self._id = uuid.uuid4()
		self.node_type = node_type
		self.label = label
		self.countermeasures = []

	def get_label(self) -> str:
		return self.label

	def get_id(self):
		return self._id.hex

	def add_countermeasure(self, countermeasure: Union['Node', 'Gate']):
		if self.node_type == countermeasure.node_type:
			raise Exception("Cannot add countermeasure of same type")
		self.countermeasures.append(countermeasure)
		return countermeasure

	def __str__(self) -> str:
		if self.label is None:
			return "node_" + self.get_id()
		else:
			return "[" + self.node_type.name + "]" + self.label


class Gate(Node):
	def __init__(self, gate_type: GateType, label: str = None, node_type: NodeType = NodeType.ATTACK):
		super().__init__(label, node_type)
		self.gate_type = gate_type
		self.children = []

	def add_child(self, child: Union['Gate', 'Node']):
		if self.node_type != child.node_type:
			raise Exception("Cannot add child of different type, use add_countermeasure instead")
		self.children.append(child)
		return self

	def add_gate(self, gate_type: GateType, label: str = None):
		g = Gate(gate_type, label, self.node_type)
		self.add_child(g)
		return g

	def add_attack(self, attack: str):
		be = Node(attack, NodeType.ATTACK)
		self.add_child(be)
		return be

	def add_defense(self, defense: str):
		be = Node(defense, NodeType.DEFENSE)
		self.add_child(be)
		return be

	def add_and_gate(self, label: str = None):
		return self.add_gate(GateType.AND, label)

	def add_sequence_and_gate(self, label: str = None):
		return self.add_gate(GateType.SEQUENCE_AND, label)

	def add_or_gate(self, label: str = None):
		return self.add_gate(GateType.OR, label)

	def __str__(self) -> str:
		return "gate_" + self.get_id()


class AttackTree:
	def __init__(self, root: Node):
		self.root = root
