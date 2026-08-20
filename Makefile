.PHONY: test fuzz tf-validate-templates tflint tfsec iac-scan

test:
	terraform fmt -check -recursive templates
	python .github/scripts/validate_templates.py

fuzz:
	go test ./fuzz -run=^$$ -fuzz=FuzzHCLParse -fuzztime=30s

tf-validate-templates:
	python3 .github/scripts/terraform_validate_templates.py

tflint:
	cd templates && tflint --init && tflint --recursive

tfsec:
	tfsec templates

iac-scan: tflint tfsec

