# Security Policy

## Reporting a Vulnerability

If you discover a security vulnerability, please do not open a public GitHub issue.

Report it privately using one of the following channels:

- Email (preferred): [support@abcxyz.com](mailto:support@abcxyz.com)
- Web form: <https://www.abcxyz.com/contact>
- GitHub Security Advisories (if enabled): Use the repository’s "Report a vulnerability" button under the Security tab

Do not include secrets (access keys, session tokens, private keys, passwords) in any report or proof of concept.

### What to include

To help us triage quickly, please include:

- Description of the issue
- Impact (what could happen)
- Steps to reproduce (proof of concept if available)
- Affected versions, files, or paths
- Any suggested fix or patch (optional)

For Terraform and AWS-related reports (when applicable), include:

- AWS account ID and region
- Module prefix (if used)
- Affected ZoneId values, VPC values, and log group ARN values (if applicable)
- Module version and Terraform version
- Relevant CloudWatch alarm or dashboard names (or screenshots)
- Exact error output (copy and paste)

## Disclosure Process and Timeline

We follow coordinated vulnerability disclosure.

### Severity targets

We aim to meet the following targets when feasible:

- Critical: acknowledge within 1 business day, provide a fix or mitigation within 7 days
- High: acknowledge within 3 business days, provide a fix or mitigation within 30 days
- Medium: provide a fix or mitigation within 60 days

### Updates

If an issue requires upstream coordination or is complex, we will provide status updates at least weekly until resolution.

## Supported Versions

Security fixes are provided for:

- The latest released version
- Recent minor versions where feasible

## Scope

This repository contains Terraform infrastructure templates (no runtime service). Security issues may include:

- Credential exposure risk
- Insecure defaults
- IAM policies with overly broad permissions
- Supply chain risks in CI tooling

## Safe Harbor

We support good-faith security research. If you follow this policy and avoid privacy violations, data destruction, and service disruption, we will not pursue legal action for your report.
