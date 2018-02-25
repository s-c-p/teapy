from tea import *
from tea.msgFactory import msgType
from tea.switch_case import switch

msgType('Inc', [], 'vsra', globals())
msgType('Dec', [], '2sra', globals())

y = Dec()

def f(x):
	with switch(x, locals(), globals()) as (case, default):
		@case(Inc)
		def _():
			return "+"
		@case(Dec)
		def _():
			return "-"
		@default
		def _():
			return "ha ha"
	return locals()['switch_case_result']

assert f(Inc) == "ha ha"
assert f(Inc()) == "+"
assert f(Dec()) == "-"

