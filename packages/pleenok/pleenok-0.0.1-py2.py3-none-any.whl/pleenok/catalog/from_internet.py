from pleenok.model.attack_tree import AttackTree, Gate, GateType


def defcon_risk() -> AttackTree:
	# From https://images.squarespace-cdn.com/content/v1/654fa95a9084f270bbe850ea/18a7b21d-2704-4fe4-ad10-6ed53fb7e4b7/Screenshot+2024-08-03+at+12.34.46%E2%80%AFPM.png
	at2 = Gate(GateType.OR, "Defcon Risk")
	at2_1 = at2.add_gate(GateType.OR, "Steal property")
	at2_11 = at2_1.add_gate(GateType.OR, "Obtain from us")
	at2_11.add_attack("Pickpocketing")
	at2_111 = at2_11.add_gate(GateType.OR, "Obtain laptop")
	at2_111.add_attack("Left unattended")
	at2_111.add_attack("Forceful robbery")
	at2_12 = at2_1.add_gate(GateType.OR, "Obtain from room")
	at2_121 = at2_12.add_gate(GateType.AND, "Use blocked door")
	at2_121.add_attack("Find property")
	at2_121.add_attack("Does not close all the way")
	at2_122 = at2_12.add_gate(GateType.AND, "Steal from blocked door")
	at2_1221 = at2_122.add_gate(GateType.OR, "Find way into room")
	at2_1221.add_attack("Staff attack")
	at2_1221.add_attack("Lost keycard")
	at2_122.add_attack("Find property")
	at2_2 = at2.add_gate(GateType.OR, "Steal data")
	at2_2.add_attack("Steal from computer")
	at2_2.add_attack("Steal from phone")
	at2_3 = at2.add_gate(GateType.OR, "Bodily harm")
	at2_3.add_attack("Targetted attack")
	at2_3.add_attack("Mass attack")
	return AttackTree(at2)


def amezana_1() -> AttackTree:
	# From https://www.amenaza.com/attack-tree-what-are.php
	at = Gate(GateType.AND, "Physically damage cooling pumps")
	at.add_attack("Gather information")
	or1 = at.add_or_gate("Compromise perimeter security")
	or2 = at.add_or_gate("Sabotage pump and/or coolant pipes")
	or2.add_attack("Cause electrical damage")
	or2.add_attack("Blow up pumps")
	or11 = or1.add_or_gate("Place authorized insider in plant")
	or1.add_attack("Force entry")
	or11.add_attack("Blackmail intimidate existing, cleared employee")
	or111 = or11.add_sequence_and_gate("Insert sympathiser into plant")
	or111.add_attack("Create trained agent")
	or111.add_attack("Apply for employment")
	or111.add_attack("Pass screening procedure")
	return AttackTree(at)
