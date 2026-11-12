# Decode external JSON batches per item

## Mirror the upstream decoder first

- Read the upstream decoder before you write your own decoder.

- Record how it splits the batch and how it handles one bad item.

- Record how it advances its offset or cursor after a bad item.

- Treat a review claim of parity as unproven until the upstream code above is on record.

## Decode each item alone

- Decode the batch envelope into raw items first, with one raw value per item.

- Decode each raw item in its own step and keep the good items when one item fails.

- Skip a bad item and continue with the next item instead of failing the whole batch.

- Advance the offset from the best effort item id of a bad item when the upstream decoder does that.

## Treat null as absent

- Give every non optional field a default for absent values.

- Treat an explicit null the same way you treat an absent field.

- Add a null arm for fields that arrive as null in real traffic, such as a file id inside a document.

- Keep wrong type errors visible in a per item test instead of letting them fail the batch silently.

## Prove it with poisoned fixtures

- Build one fixture per poison shape, with one bad item beside good items.

- Cover a wrong type field, an explicit null field, and a null nested object.

- Assert that the good items still arrive and the offset still advances.

- Rename a test when its name no longer matches what it proves, so a later reader does not trust a misleading name.

## Available connectors

- Use `muse.connector_search` to find other connectors and `muse.skill_search` to find related skills.

- If nothing here fits, look on the web for a maintained API or MCP server and set it up with [Custom Connectors and MCPs](/opt/muse/skills/custom-connector-setup/SKILL.md), or build a custom connector.

## Alternatives for better results

- Read the upstream library source for the exact decode loop instead of guessing from its public docs.

- Ask the reviewer to name the upstream function they checked before they certify parity.
