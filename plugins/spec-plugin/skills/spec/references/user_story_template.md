# User Story Index Template

Use this template when adding entries to `specs/user-stories.md`. This file serves as a lightweight index linking to full specs.

**Progressive Disclosure**: `user-stories.md` is a scannable index. Full user story details live in each feature's `overview.md` where implementation context is needed.

## Template Structure

```markdown
### [Feature Name] ([Status])

**Epic**: [Epic Name]
**Status**: [Design Phase | In Progress | Complete | On Hold]
**Priority**: [High | Medium | Low]

**User Need**: As a [user type], I want to [action] so that [benefit].

**Full Spec**: [Feature Overview](feature-name/overview.md)
```

## Filling Guidelines

- **Status**: Design Phase (planning), In Progress (building), Complete (shipped), On Hold (deferred)
- **Priority**: Based on user impact and business value
- **User Need**: One-line summary in "As a [who], I want [what], so that [why]" format
- **Full Spec**: Link to the overview.md containing full details

Keep index entries minimal - detailed use cases, success criteria, and architecture components belong in overview.md.

## Example

```markdown
### Smart Product Scanner (In Progress)

**Epic**: Mobile Shopping Experience
**Status**: In Progress
**Priority**: High

**User Need**: As a shopper, I want to scan a product and instantly see personalized recommendations based on my purchase history, so I can make confident buying decisions in-store.

**Full Spec**: [Smart Product Scanner](product-scanner/overview.md)
```
