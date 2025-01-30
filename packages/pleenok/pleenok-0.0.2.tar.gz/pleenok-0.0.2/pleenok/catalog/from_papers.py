from pleenok.model.attack_tree import AttackTree, Gate, GateType, NodeType, Node


def falco21_fig4() -> AttackTree:
	# From https://doi.org/10.1109/SMC-IT51442.2021.00016
	at = Gate(GateType.SEQUENCE_AND, "Tamper data received from CubeSAT")
	at1 = at.add_and_gate("Admin access to database server")
	at1.add_attack("Login to server via SSH")
	at11 = at1.add_or_gate("Steal credentials to database")
	at11.add_attack("Search for misconfiguration")
	at11.add_attack("Get priviledged access to server")
	at1.add_attack("Login to phpMyAdmin interface")
	at.add_attack("Change data logged in flight database")
	return AttackTree(at)


def kordy12_fig1() -> AttackTree:
	# From https://satoss.uni.lu/members/barbara/papers/ADT12.pdf
	d1 = Gate(GateType.AND, "Data confidentiality", NodeType.DEFENSE)
	d2 = d1.add_and_gate("Network security")
	d3 = d2.add_and_gate("Access control")
	d4 = d3.add_defense("Passwords")
	a1 = d4.add_countermeasure(Node("Dictionary attack", NodeType.ATTACK))
	d5 = a1.add_countermeasure(Node("Strong password", NodeType.DEFENSE))
	a2 = d5.add_countermeasure(Gate(GateType.XOR, "Strong password attack", NodeType.ATTACK))
	a2.add_attack("Find note")
	a2.add_attack("Same password, different account")
	d2.add_defense("Firewall")
	d2.add_defense("IDS")
	d6 = d1.add_defense("Physical security")
	a3 = d1.add_countermeasure(Gate(GateType.OR, "Employee attack", NodeType.ATTACK))
	a3.add_attack("Corruption").add_countermeasure(Node("Screening", NodeType.DEFENSE))
	a3.add_attack("Social engineering").add_countermeasure(Node("Sensitivity training", NodeType.DEFENSE))
	a4 = d6.add_countermeasure(Gate(GateType.OR, "Break in", NodeType.ATTACK))
	a5 = a4.add_attack("Back door") \
		.add_countermeasure(Node("Lock", NodeType.DEFENSE)) \
		.add_countermeasure(Gate(GateType.OR, "Defeat lock", NodeType.ATTACK))
	a5.add_attack("Force open")
	a5.add_attack("Acquire keys")
	a6 = a4.add_or_gate("Fire escape")
	a7 = a6.add_attack("Door") \
	    .add_countermeasure(Node("Lock", NodeType.DEFENSE)) \
	    .add_countermeasure(Gate(GateType.OR, "Defeat lock", NodeType.ATTACK))
	a6.add_attack("Window").add_countermeasure(Node("Reinforce", NodeType.DEFENSE))
	a7.add_attack("Force open")
	a7.add_attack("Acquire keys")
	a4.add_attack("Window").add_countermeasure(Node("Reinforce", NodeType.DEFENSE))
	a8 = a4.add_countermeasure(Node("Security Guard", NodeType.DEFENSE)) \
		.add_countermeasure(Gate(GateType.OR, "Defeat guard", NodeType.ATTACK))
	a8.add_attack("Bribe")
	a8.add_attack("Steal keys")
	a9 = a8.add_and_gate("Overpower")
	a9.add_attack("Out-number")
	a9.add_attack("Use weapons")
	a8.add_countermeasure(Node("Video cameras", NodeType.DEFENSE))

	return AttackTree(d1)
