# Verify secret-bearing claims by count and hash

## Spot a redacted value

- Treat any rendered output that shows a secret, token, or credential placeholder as unproven for the exact value.

- Assume the display layer can replace a secret value with a redaction marker even when the underlying file or log holds the real value.

- Name the claim in one sentence before you verify it, such as whether a token format string is present or absent in a file.

- Read the live file with `muse.read` before you judge a claim about its contents, and do not judge from a summary or an earlier report alone.

## Prove presence or absence with counts and hashes

- Count matches with `grep -c` for the exact pattern and record the count, the file, and the line number.

- Hash the matching line with `sha256sum` and record the hash instead of copying the rendered line into your report.

- Treat a count of zero as absence only after you confirm the pattern, the file path, and the search scope are the ones the claim names.

- Treat a rendered redaction marker as no evidence either way, and never use it to claim a value is present or absent.

- Re-run the count and the hash after any edit, rebase, or checkout, and record the new values beside the old ones.

## Compare two versions without reading the secret

- Compare the count from each version first, and compare the hash of each matching line next.

- Report that the counts match and the hashes match, or report the exact count and hash that differ.

- Verify a claimed fix the same way, by showing the count or hash changed in the direction the fix requires.

- Check the base commit with `git show` when a working tree may hold uncommitted work, and record which commit you checked.

- Keep the secret value out of every report, log, and quote, and carry only counts, hashes, file paths, and line numbers.

## Available connectors

- Use `muse.connector_search` to find other connectors and `muse.skill_search` to find related skills.

- If nothing here fits, look on the web for a maintained API or MCP server and set it up with [Custom Connectors and MCPs](/opt/muse/skills/custom-connector-setup/SKILL.md), or build a custom connector.

## Alternatives for better results

- Read `probe-first` when the claim is about whether something can be done at all, and use its smallest probe to test the mechanism directly.

- Read `verify-before-claiming` when the claim compares two systems or repeats another agent report, and check the primary source before you certify it.

- Ask a reviewer to repeat the count and hash independently when a single wrong reading would change a merge or release decision.
