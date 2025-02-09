# Optimism Monorepo Contributing Guide

## What to Contribute

Welcome to the **Optimism Monorepo Contributing Guide**! If you're reading this, you might be interested in contributing to the **Optimism Monorepo**. Before diving into the specifics of this repository, take a moment to explore some of the different ways you can contribute:

- **Report issues**: A great bug report is detailed and provides clear steps for reproducing the issue. Developers will appreciate well-written reports!
  - **IMPORTANT**: If you believe your report impacts the security of this repository, refer to the official **Security Policy** document.
- **Fix issues**: Look for issues tagged with `D-good-first-issue` or `S-confirmed`.
- **Improve documentation**: Help enhance the **Optimism Developer Docs** by fixing typos, adding missing sections, or improving explanations.
- **Engage in protocol design discussions**: Join the conversations within the **OP Stack Specs** repository.

## Code of Conduct

All interactions within this repository are subject to a **Code of Conduct** adapted from the **Contributor Covenant**.

## Development Quick Start

### Software Dependencies

| Dependency         | Version | Version Check Command      |
|-------------------|---------|---------------------------|
| `git`            | ^2      | `git --version`          |
| `go`             | ^1.21   | `go version`             |
| `node`           | ^20     | `node --version`         |
| `nvm`            | ^0.39   | `nvm --version`          |
| `just`           | ^1.34.0 | `just --version`         |
| `foundry`        | ^0.2.0  | `forge --version`        |
| `make`           | ^3      | `make --version`         |
| `jq`             | ^1.6    | `jq --version`           |
| `direnv`         | ^2      | `direnv --version`       |
| `docker`         | ^24     | `docker --version`       |
| `docker compose` | ^2.23   | `docker compose version` |

### Notes on Specific Dependencies

#### Node.js
Make sure to use the version specified in `.nvmrc`. You can use **nvm** to manage multiple versions of Node.js and automatically switch to the correct version when working on this repository.

#### Foundry
**Foundry** is updated frequently and may introduce breaking changes. This repository pins a specific version in `versions.json`. Use the command:

```sh
just update-foundry
```

to ensure your version matches the one used in CI.

#### Direnv
**Direnv** loads environment variables from `.envrc` automatically. After installing `direnv`, make sure it is hooked into your shell by following the guide on the **direnv website**. Restart your terminal or reload your config file for the changes to take effect.

#### Docker Compose
Docker Desktop includes **docker compose** by default. If you're on Linux or not using Docker Desktop, you may need to install the **Compose plugin** separately.

## Setting Up

Clone the repository and navigate to it:

```sh
git clone git@github.com:ethereum-optimism/optimism.git
cd optimism
```

## Building the Monorepo

Before proceeding, ensure all required dependencies are installed. **Foundry** is required to build the smart contracts. Refer to the section on **Foundry** above for setup instructions.

To install dependencies and build all packages:

```sh
make build
```

⚠️ **Note:** Packages built on one branch may not be compatible with those on a different branch. Always **rebuild** the monorepo after switching branches.

## Running Tests

### Solidity Unit Tests
```sh
cd packages/contracts-bedrock
just test
```

### Go Unit Tests
Navigate to the package you want to test and run:

```sh
go test ./...
```

### End-to-End (E2E) Tests
For E2E tests, refer to the documentation.

### Contract Static Analysis
We use **slither** for static analysis. Ensure **Python 3.x** is installed, then run:

```sh
cd packages/contracts-bedrock
pip3 install slither-analyzer
just slither
```

## Labels
Labels help categorize issues and pull requests. Here are some key labels:

- **`A-<category>`**: Defines the general area of the issue/PR.
- **`C-<category>`**: Provides contextual information about the type of change.
- **`M-<category>`**: Adds metadata about process-related aspects of the issue/PR.
- **`D-<level>`**: Indicates the difficulty level of an implementation.
- **`S-<status>`**: Specifies the current status of an issue/PR.

You can filter issues labeled **`M-community`** to find those available for external contributions:  
🔗 [Community Issues](https://github.com/ethereum-optimism/optimism/labels/M-community)

For easy-to-fix issues, check **`D-good-first-issue`**:  
🔗 [Good First Issues](https://github.com/ethereum-optimism/optimism/labels/D-good-first-issue)

## Modifying Labels
If you alter or delete labels, be aware that:

- **Mergify bot** uses labels for automation. Ensure you update the **Mergify configuration**.
- If modifying **`S-stale`**, update the **close-stale workflow**.
- If modifying **`M-dependabot`**, update the **Dependabot config**.
- Saved label filters on project boards will **not automatically update**.

## Workflow for Pull Requests

🚨 **Before making major changes, open an issue** to discuss your proposal. This increases the chances of your PR being merged.

### PR Guidelines
- **Smaller PRs** are easier to review and merge.
- **Fork the repository**:
  - Use the `develop` branch for non-breaking changes.
  - Use the `release/X.X.X` branch for upcoming releases.
- **Ensure proper test coverage** for new features.
- **Follow the Conventional Commits format** for commit messages.
- **Mark PRs as 'draft'** until they are ready for review.
- **Provide a clear PR description** to help reviewers understand the changes.
- **Add comments in the 'Files Changed' tab** to clarify key parts of your PR.

## Response Time
We aim to provide a **meaningful response within 2 business days** for external contributions.

## Keeping a Clean Git History

We use **git rebase** to maintain a clean commit history. Learn more here:
🔗 [Git Rebase Tutorial](https://www.atlassian.com/git/tutorials/rewriting-history/git-rebase)

---

📢 **You're now ready to contribute!** 🚀 Follow this guide, and you'll be on your way to making a meaningful impact on Optimism.

