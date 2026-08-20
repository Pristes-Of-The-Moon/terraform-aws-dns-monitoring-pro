# Contributing

Thanks for your interest in contributing to **terraform-aws-observability-pro**.

This repository is public for transparency and review, but it is read-only for external contributors.

- Pull requests from non-abcxyz members are not accepted and may be automatically closed.
- Changes to this repository are made only by abcxyz maintainers.

Additional notes:

- GitHub Issues are not used for support. Use the abcxyz links below.
- This repository is templates-only; the licensed Terraform module is delivered via abcxyz subscription and requires an active license to download and use.

## External requests

External users may submit the following via the abcxyz Contact form:

- Bug reports
- Feature requests
- Improvement suggestions
- Documentation feedback
- Configuration or behavior questions

Submit via:

- <https://www.abcxyz.com/contact>

### Minimum required information

- Name
- Email
- Description of the request

### Helpful details for faster troubleshooting

Include when relevant:

- AWS account ID, AWS region, and module prefix
- Affected ZoneId values, VPC values, and log group ARN values
- Module version and Terraform version
- CloudWatch alarm or dashboard names (or screenshots) and any recent changes
- Exact error output (copy and paste)

Do not include secrets (access keys, session tokens, private keys, passwords) in any submission.

Security vulnerabilities: follow the instructions in `SECURITY.md` and do not submit sensitive details via public forms.

## abcxyz maintainers

All changes must be made by abcxyz maintainers and merged via pull request.

### Quality and security standards

Before requesting review, ensure the following:

- Formatting is clean (run `terraform fmt -check -recursive templates`).
- Template conventions pass (run `python .github/scripts/validate_templates.py`).
- Template functional validation passes (run `make tf-validate-templates`).
- CI workflows and GitHub Actions remain pinned and least-privilege where possible.
- Changes are small, reviewed, and merged via pull request per repository rules.

References:

- Terraform style and conventions: <https://developer.hashicorp.com/terraform/language/style>
- GitHub Actions security hardening: <https://docs.github.com/en/actions/security-guides/security-hardening-for-github-actions>

### Testing policy

When major functionality is added or changed (templates, validation scripts, or CI behavior), corresponding automated tests or checks must be added or updated.

At a minimum, PRs must pass:

- `make test`
- `make tf-validate-templates`

Optional (when applicable):

- `make fuzz`

### Secure-by-default checklist

For changes that affect templates or defaults, verify:

- No secrets are committed (credentials, tokens, private keys).
- IAM permissions are least-privilege and avoid broad wildcards where practical.
- Public exposure is not enabled by default (only opt-in with clear documentation).
- Logging, retention, and encryption settings are enabled where applicable.
- Inputs are validated and documented; unsafe defaults are avoided.
- GitHub Actions remain pinned (commit SHA) and permissions remain minimal.

## Licensed user technical support

If you are a licensed user and have a technical issue, open a support ticket via:

- My Cases (open or track cases): <https://www.abcxyz.com/cases.html>
- Knowledge Base (known issues and how-to): <https://www.abcxyz.com/knowledge.html>

For faster resolution, include:

- AWS account ID, AWS region, and module prefix
- Affected ZoneId values, VPC values, and log group ARN values
- Module version and Terraform version
- CloudWatch alarm or dashboard names (or screenshots) and any recent changes
- Exact error output (copy and paste)
