# Crossplane development tools

* [xprin test suites](xprin-test-suites.md) - Run repeatable local Composition render tests with declarative assertions.
* [Pin the Crossplane version in xprin runs](xprin-crossplane-version.md) - Pin the Crossplane image tag for render and validation with `--crossplane-version`, available since xprin v0.3.0.
* [xprin Crossplane CLI tier detection](xprin-crossplane-cli-tiers.md) - How xprin, since v0.3.0, chooses the validate subcommand and render flags for the installed Crossplane CLI.
* [Export xprin test artifacts](xprin-test-artifacts-export.md) - Keep a persistent copy of every test case's inputs and outputs with `xprin test --artifacts-dir`, available since xprin v0.3.0.
* [Regenerate xprin golden files](xprin-update-goldens.md) - Write current render output to diff and dyff expected files with `xprin update-goldens`, available since xprin v0.3.0.
