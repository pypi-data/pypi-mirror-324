import re
from pleenok.model.attack_tree import AttackTree, Node, Gate, GateType


def _capitalize(name: str) -> str:
	words = re.sub(r'[_-]', ' ', name).split()
	return ''.join(word.capitalize() for word in words)


def _generate_label(node: Node) -> str:
	if isinstance(node, Gate):
		if node.label is None:
			return "gate_" + node.get_id()
		else:
			return _capitalize(node.label)
	else:
		return _capitalize(node.label)


def generate_risqflan(at: AttackTree) -> str:
	attack_nodes = []
	attack_diagram = []
	attack_node_root = str(at)

	def traverse(at: Node):
		nonlocal attack_nodes, attack_diagram
		if isinstance(at, Gate):
			# attack nodes
			attack_nodes.append(_generate_label(at))
			for child in at.children:
				traverse(child)
			# attack diagram
			children = ", ".join(_generate_label(node) for node in at.children)
			root = _generate_label(at)
			if at.gate_type == GateType.AND:
				attack_diagram.append(f"{root} -AND-> {{{children}}}")
			elif at.gate_type == GateType.SEQUENCE_AND:
				attack_diagram.append(f"{root} -OAND-> [{children}]")
			elif at.gate_type == GateType.OR:
				attack_diagram.append(f"{root} -OR-> {{{children}}}")
			elif at.gate_type == GateType.XOR:
				attack_diagram.append(f"{root} -K1-> {{{children}}}")
		else:
			attack_nodes.append(_generate_label(at))

	traverse(at.root)
	template = """
begin model Empty
// This is an empty RisQFLan file
// Fill all the blocks to model your scenario name
//Here we specify variables and their initial values. This is convenient to express constraints and to ease the analysis
begin variables
end variables

// Here we specify all the things that can go wrong
// In particular successful actions of attacker

begin attack nodes
	{attack_nodes}
end attack nodes

// Reactive defensive actions
begin defense nodes
end defense nodes

// Permanent defensive actions
begin countermeasure nodes
end countermeasure nodes

// The diagram specifies how defensive actions and attacker actions relate to each other
begin attack diagram
	{attack_diagram}
end attack diagram

// Here we can specify classes of attackers with probabilistic behavior
begin attackers
	attacker1
end attackers

// The effectiveness of a defence depends on the class of attacker and the attack action
begin defense effectiveness
end defense effectiveness

// Attacks may not be detected
begin attack detection rates
end attack detection rates

// Attributes of attacks are specified here
begin attributes
end attributes

// One can here impose additional constraints on the attacker, e.g. based on his budget
begin quantitative constraints
end quantitative constraints

//Domain-specific actions executed by the attacker
begin actions
end actions

//Constraints on the execution of actions
begin action constraints

end action constraints
//The probabilistic behaviour of each attacker
begin attacker behaviour
	begin attack attacker = attacker1
		states = state1
		transitions = state1 - (succ({attack_node_root}),1.0) -> state1
	end attack
end attacker behaviour

// Here we specify the attacker we want to consider
begin init
	attacker1
end init

//Finally, you can specify 3 types of analysis
//analysis: statistical analysis of quantitative properties
//exportDTMC: export the state space of the model (if finite) in a discrete time Markov chain in the format supported by the model checkers PRISM and STORM
//simulate: perform a simulation to debug your model

// In this particular case we are just interested in the likelihood of success of each attack
begin analysis
	query = eval from 1 to 100 by 20 : {{ {attack_node_root} }}
	// Statistical confidence
	default delta = 0.1
	alpha = 0.1
	// Parallelism to be exploited in the machine
	parallelism = 1
end analysis

end model
"""
	return template.format(attack_nodes="\n\t".join(attack_nodes), attack_diagram="\n\t".join(attack_diagram),
						   attack_node_root=attack_node_root)
