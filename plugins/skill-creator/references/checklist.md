# Quality Checklist

Run through this checklist before considering a skill complete.

## Metadata

- [ ] `name` is short, descriptive, and conveys what the skill does
- [ ] `name` is lowercase, hyphens and digits only, no leading/trailing/consecutive hyphens
- [ ] `name` is 64 characters or fewer
- [ ] `name` matches the directory name exactly
- [ ] `description` uses third-person voice
- [ ] `description` includes trigger phrases covering all major use cases
- [ ] `description` is 80–1024 characters
- [ ] `description` contains no angle brackets
- [ ] No extra frontmatter fields beyond `name` and `description` (unless `argument-hint`, `disable-model-invocation`, `user-invocable`, `allowed-tools`, `model`, `context`, `agent`, or `hooks` are needed)

## Structure

- [ ] SKILL.md body is under 500 lines
- [ ] All reference files are linked from SKILL.md with clear "when to read" guidance
- [ ] References are one level deep (no reference-to-reference chains)
- [ ] No extraneous files (README.md, CHANGELOG.md, etc. inside the skill)
- [ ] Unused scaffolded directories and example files are deleted
- [ ] File paths use forward slashes only (no backslashes)

## Content Quality

- [ ] Body uses imperative form for instructions
- [ ] Only includes information Claude doesn't already know
- [ ] Concrete examples are preferred over abstract explanations
- [ ] Terminology is consistent throughout (no synonyms for the same concept)
- [ ] No time-sensitive information (version numbers, dates, volatile URLs)
- [ ] "When to use" information is in the description, not the body
- [ ] Progressive disclosure is applied — details are in references, not inline
- [ ] Callout blocks highlight critical information (`> [!NOTE]`, `> [!CAUTION]`, `> [!IMPORTANT]`)
- [ ] No over-explaining of concepts Claude already understands

## Scripts

- [ ] Each script solves a complete problem (no placeholder logic)
- [ ] No magic numbers or unexplained constants
- [ ] Scripts have been tested by actually running them
- [ ] Scripts produce verifiable intermediate outputs where appropriate
- [ ] Scripts have zero or minimal external dependencies
- [ ] Script names describe what they do (`validate_fields.py`, not `helper.py`)

## Testing

- [ ] Skill has been tested on representative real tasks
- [ ] Claude navigates reference files as intended (no unexpected paths)
- [ ] Output matches expected format
- [ ] Skill triggers reliably from natural user prompts matching the description
- [ ] Skill does NOT trigger on unrelated prompts
- [ ] Validation script passes clean
