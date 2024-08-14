.PHONY: lint
lint:
	black .

.PHONY: test
test: lint
ifdef test_name
	pytest tests/unit_tests -v -k $(test_name)
else
	pytest tests/unit_tests
endif

.PHONY: test-integration
test-integration: lint
ifdef test_name
	pytest tests/integration_tests -v -k $(test_name)
else
	pytest tests/integration_tests
endif