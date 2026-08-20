# TFLint configuration for Terraform templates in this repository.
# Docs: https://github.com/terraform-linters/tflint

plugin "aws" {
  enabled = true
  version = "0.33.0"
  source  = "github.com/terraform-linters/tflint-ruleset-aws"
}

config {
  # Keep output readable in CI.
  format = "compact"
}

# You can selectively disable noisy rules here if needed.
# rule "terraform_required_version" {
#   enabled = false
# }
