.PHONY: verify

verify:
	python3 tools/synthetic_network_canary.py --check
