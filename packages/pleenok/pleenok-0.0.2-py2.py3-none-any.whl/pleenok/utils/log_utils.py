from typing import Iterable
import pandas as pd
import pm4py
from datetime import datetime, timedelta


def str_to_log(data: Iterable[str]) -> pd.DataFrame:
	events = []
	for case_id, trace in enumerate(data, start=1):
		for idx, activity in enumerate(trace):
			timestamp = datetime.now() + timedelta(seconds=idx)
			events.append([case_id, activity, timestamp])
	df = pd.DataFrame(events, columns=['case_id', 'activity', 'timestamp'])
	return pm4py.format_dataframe(df, case_id='case_id', activity_key='activity', timestamp_key='timestamp')
