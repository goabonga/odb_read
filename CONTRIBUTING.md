# Contributing

## Getting Started

1. Fork the repository on GitHub
2. Clone your fork:

```bash
git clone git@github.com:<your-username>/odb-tui.git
cd odb-tui
make install-dev
```

## Workflow

1. Create a branch from `main`
2. Make your changes
3. Run checks: `make check`
4. Push to your fork
5. Open a pull request targeting `main` on the original repository

## Commit Messages

This project uses [Conventional Commits](https://www.conventionalcommits.org/):

```
feat: add new feature
fix: resolve bug
docs: update documentation
style: formatting, no code change
refactor: restructure without behavior change
test: add or update tests
chore: maintenance tasks
```

Use `cz commit` for interactive commit or write the message manually.

## Code Quality

All pull requests must pass:

- **Lint**: `make lint` (ruff)
- **Type check**: `make typecheck` (mypy)
- **Tests**: `make test` (pytest)

Or run everything at once: `make check`

## Pull Requests

- Keep PRs focused on a single change
- Update tests for new features or bug fixes
- Ensure CI passes before requesting review

## License

By contributing, you agree that your contributions will be licensed under the [MIT License](LICENSE).
