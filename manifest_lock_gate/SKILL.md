# Gate manifest and lockfile changes

## Diff the lockfile at its real path

- Find the lockfile where it actually lives before you check any diff.

- Run the diff against that exact path, such as the workspace lockfile under the workspace directory.

- Expect the diff to show exactly the dependency the manifest change adds or changes.

- Treat a diff at a path where no lockfile exists as no check at all, and stop there.

## Build locked on the committed tree

- Run the gates on the committed tree, not on a working tree that the tooling can still change.

- Build with the locked flag, such as a locked Cargo build, so a missing lock entry fails instead of being silently added.

- Check that the tree is clean after the gates finish, with no lockfile changed by the gate run itself.

- Rerun the gates after any lockfile fix, and record the lockfile checksum before and after.

## Report only what the diff proves

- Name the lockfile path and the exact diff lines in the report.

- Say which locked build ran and its exit code.

- Say whether the tree was clean after the gates, in the same report.

- Never claim committed tree state from a gate run that changed the tree.

## Available connectors

- Use `muse.connector_search` to find other connectors and `muse.skill_search` to find related skills.

- If nothing here fits, look on the web for a maintained API or MCP server and set it up with [Custom Connectors and MCPs](/opt/muse/skills/custom-connector-setup/SKILL.md), or build a custom connector.

## Alternatives for better results

- Keep the manifest and lockfile change in one commit so the diff is reviewable as a pair.

- Use the package manager lock command for the ecosystem in use when the locked build flag is not available.
