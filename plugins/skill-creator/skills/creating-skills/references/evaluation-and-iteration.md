# Evaluation and Iteration

Strategies for testing skills, measuring their effectiveness, and improving them systematically.

## Evaluation-Driven Development

Rather than writing a complete skill and hoping it works, use an iterative approach driven by evaluations:

### The Cycle

1. **Identify gaps**: What does Claude struggle with without the skill? Collect concrete examples of failures or inefficiencies.
2. **Create evaluations**: Turn those examples into test cases with expected outcomes. Each eval is a prompt + the desired behavior.
3. **Baseline**: Run the evals without the skill to measure the starting point. Note where Claude already succeeds — those areas don't need skill content.
4. **Write minimal instructions**: Add only the content needed to address the gaps. Start with the smallest effective addition.
5. **Run evals again**: Measure improvement. If a gap persists, analyze why and add targeted content.
6. **Iterate**: Repeat steps 4–5 until evals pass reliably.

### Principles

- **Minimal additions**: Each iteration should add the smallest amount of content that closes a specific gap. Resist the urge to add "nice to have" content that isn't driven by a failing eval.
- **One change at a time**: When iterating, change one thing and re-evaluate. Multiple simultaneous changes make it hard to attribute improvements.
- **Remove what doesn't help**: If content doesn't improve eval results, remove it. Unnecessary content wastes context.

### Example

Building a `sql-optimizer` skill:

1. **Gap**: Claude rewrites queries but doesn't check execution plans
2. **Eval**: "Optimize this slow query" → should include EXPLAIN analysis
3. **Baseline**: Claude skips EXPLAIN in 4/5 test cases
4. **Addition**: Add "Always run EXPLAIN ANALYZE before and after optimization"
5. **Result**: Claude now includes EXPLAIN in 5/5 cases
6. **Next gap**: Claude doesn't consider index usage → add index analysis step

## The Claude A/B Pattern

A powerful technique for iterating on skills: use one Claude instance to create the skill, and a separate instance to test it.

### How It Works

1. **Claude A** (the author): Creates or modifies the skill based on requirements and eval feedback
2. **Claude B** (the tester): Uses the skill on real tasks with no prior context about the skill's internals
3. **Observe**: Watch how Claude B navigates the skill. Note where it struggles, misinterprets instructions, or produces unexpected output.
4. **Feed back**: Report observations to Claude A for targeted improvements

### Why Two Instances

- Claude A has deep context about the skill's intent, which can mask ambiguities
- Claude B approaches the skill fresh, revealing unclear instructions, missing context, and wrong assumptions
- This mimics how the skill will actually be used in production

### What to Watch For

- Does Claude B find and use the right reference files?
- Does Claude B follow the workflow in the intended order?
- Does Claude B understand when to apply conditional logic?
- Does Claude B produce output matching the expected format?
- Does Claude B know when the skill should *not* apply?

## Testing Across Models

Skills should work across Claude model tiers. Different models have different strengths:

### Model Considerations

| Model | Characteristics | Testing Focus |
|-------|----------------|---------------|
| **Opus** | Strongest reasoning, follows nuanced instructions | Test that the skill isn't over-specifying things Opus would figure out on its own |
| **Sonnet** | Good balance of capability and speed | Primary testing target — most common in production |
| **Haiku** | Fastest, most concise | Test that instructions are explicit enough for a model with less reasoning depth |

### Cross-Model Testing Strategy

1. **Write for Sonnet**: Calibrate the level of detail for Sonnet as the baseline
2. **Test with Haiku**: If Haiku struggles, the instructions may need more explicit guidance for critical steps. Add it selectively — don't dumb down the whole skill.
3. **Test with Opus**: If Opus is ignoring instructions or producing unnecessarily verbose output, the skill may be over-constraining. Ensure the skill doesn't fight the model's natural strengths.

### Common Cross-Model Issues

- **Haiku-specific**: May skip multi-step reasoning, miss implicit connections between sections, or take shortcuts in conditional workflows. Make critical decision points explicit.
- **Opus-specific**: May over-elaborate when the skill gives flexible guidance. If concise output is important, specify length constraints explicitly.

## Observing Skill Navigation

When testing a skill, pay attention to *how* Claude navigates it, not just the final output.

### Signs of Good Skill Design

- Claude reads SKILL.md and immediately knows which reference files to load (if any)
- Claude follows the workflow without backtracking
- Claude applies conditional logic correctly on the first pass
- Claude produces output matching the expected format without re-prompting

### Signs of Problems

- **Unexpected paths**: Claude reads reference files in an unexpected order, or reads files it shouldn't need. This suggests unclear navigation guidance in SKILL.md.
- **Missed connections**: Claude doesn't find a reference file that would have helped. This suggests the reference isn't clearly linked from SKILL.md.
- **Ignored content**: Claude skips over a section that was written to be important. This suggests the section doesn't look important enough — consider callout blocks or restructuring.
- **Repeated context loading**: Claude re-reads the same file multiple times. This suggests the information wasn't in the expected location within the file.
