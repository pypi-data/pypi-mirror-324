from pleenok.model.attack_tree import AttackTree
from pleenok.conversion.process_tree import attack_tree_to_process_tree_string
from pm4py.algo.simulation.playout.petri_net import algorithm as simulator
from pm4py.objects.process_tree.utils.generic import parse as parse_process_tree
import pm4py


def simulate(attack_tree: AttackTree, traces: int = 1):
	process_tree = parse_process_tree(attack_tree_to_process_tree_string(attack_tree))
	pn, im, fm = pm4py.convert_to_petri_net(process_tree)
	return simulator.apply(pn, im,
						   variant=simulator.Variants.BASIC_PLAYOUT,
						   parameters={simulator.Variants.BASIC_PLAYOUT.value.Parameters.NO_TRACES: traces})
