# Prompt for GPT-4o

Analyze commit and file diffs between the `integration/v0.0.6` branch and the
pull request from
[PR #90](https://github.com/enveng-group/dev_greenova/pull/90). Analysis using
`scripts/pre-merge.fish` script and review log file in
`logs/pre_merge_analysis.log` whether the changes, improve on the current
`Makefile`. Provide recommendations of any changes to keep or dismiss or
improve on in the `Makefile` . Ensure that the only files being changed are
specific to the PR, particularly `Makefile`, and verify that no other files
refactored in `origin/staging:integration/v0.0.6` are being updated.

**Objectives**:

**Context**:

```txt
https://github.com/enveng-group/dev_greenova/pull/90
```

**Tasks**:

**Sources**:

- `Makefile`
- `logs/pre_merge_analysis.log`

**Expectations**: GitHub Copilot can delete and consolidate files where
multiple implementations are found and can be merged into a single file
globally. Always use `use context7` to lookup documentation from the context7
MCP server, which provides access to all project-specific configuration files
and standards. Additional resources such as the github, filesystem, JSON,
context7, sqlite, git, fetch, sequential-thinking, and docker MCP servers have
been activated and are available for use by GitHub Copilot.

**Instructions**:

1. Identify and remove unnecessary or outdated files, code, or documentation
   that no longer serves the project's objectives. Clearly define the task's
   scope to focus only on relevant elements flagged in pre-commit checks.
2. Organize project resources, including tools, code, and documentation, into a
   logical structure. Ensure naming conventions and folder hierarchies are
   consistent, making it easier to locate and work with files.
3. Create stub files (.pyi files) for internal modules that don't have proper
   type information.
4. Add a py.typed marker file to indicate these modules have type information
5. Refactor the code to address issues such as readability, maintainability,
   and technical debt. Implement clean coding practices and resolve any flagged
   issues in the pre-commit output, such as formatting or style violations.
6. Use automated tools like bandit, autopep8, mypy, eslint, djlint,
   markdownlint, ShellCheck, and pylint to enforce coding standards. Validate
   compliance with the project's guidelines and ensure all pre-commit checks
   pass without errors. Iterate running `pre-commit` to check for any remaining
   issues after each change. Do not use the command
   `pre-commit run --all-files`.
7. Ensure that the code is well-documented, with clear explanations of
   functions, classes, and modules. Use docstrings and comments to clarify
   complex logic or important decisions made during development.
8. Test the code thoroughly to ensure it works as intended and meets the
   project's requirements. Write unit tests and integration tests as needed,
   and ensure that all tests pass before finalizing the changes.
9. Iterate until resolved.
