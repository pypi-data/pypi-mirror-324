from typing import Iterable
from pleenok.model.attack_tree import AttackTree
from pleenok.conversion.process_tree import attack_tree_to_process_tree_string
from pm4py.objects.process_tree.utils.generic import parse as parse_process_tree
import pandas as pd
import pm4py


def attack_successful(attack_tree: AttackTree, attack_log: pd.DataFrame):
	process_tree = parse_process_tree(attack_tree_to_process_tree_string(attack_tree))
	pn, im, fm = pm4py.convert_to_petri_net(process_tree)
	return pm4py.conformance_diagnostics_alignments(attack_log, pn, im, fm)


def closest_tree(attack_trees: Iterable[AttackTree], attack_events: Iterable[str]) -> AttackTree:
	# construct the event log
	events = [['case_1', event, '2021-01-01T00:00:00.000Z'] for event in attack_events]
	df = pd.DataFrame(events, columns=['case_id', 'activity', 'timestamp'])
	attack_log = pm4py.format_dataframe(df, case_id='case_id', activity_key='activity', timestamp_key='timestamp')

	# compare the event log against all attack trees
	best_tree = None
	best_fitness = -1
	for tree in attack_trees:
		alignment = attack_successful(tree, attack_log)
		fitness = alignment[0]['fitness']
		if fitness > best_fitness:
			best_fitness = fitness
			best_tree = tree
	return best_tree
