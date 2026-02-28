# 🪵🛒 Lumber Mart

A plugin marketplace for Claude Code that lets you discover and install plugins for enhanced development workflows.

Learn more about Claude Code marketplaces in the [official documentation](https://code.claude.com/docs/en/plugin-marketplaces).

## Available Plugins

| Plugin | Category | Description |
|--------|----------|-------------|
| [circuits](plugins/circuits/) | Hardware | Skills and agents for microcontroller and hardware projects -- timing diagrams, PCB design, and datasheet extraction |
| [specbeads](plugins/specbeads/) | Workflow | Specification-driven development with spec-kit and beads -- task tracking, sync, and automated code/docs/test/spec reviews |
| [skill-creator](plugins/skill-creator/) | Workflow | Guidance and tooling for creating high-quality Claude Code skills with validation and best practices |
| [runbooks](plugins/runbooks/) | Workflow | Operational runbook creation with consistent structure and built-in maintenance feedback loops |

### [circuits](plugins/circuits/)

Skills and agents to help with microcontroller and other hardware projects.

| Component | Type | Description |
|-----------|------|-------------|
| `wavejson` | Skill | Generate WaveJSON timing diagrams and HTML viewers using WaveDrom |
| `circuit-synth` | Skill | Design PCB circuits in Python with KiCad output and component search |
| `datasheet` | Skill | Extract structured information from IC/component datasheets into markdown |
| `datasheet-agent` | Agent | Autonomous agent for datasheet reading and extraction |

### [specbeads](plugins/specbeads/)

Integrates [spec-kit](https://github.com/spec-kit/specify) with [beads](https://github.com/beads-project/beads) for streamlined specification-driven development.

| Component | Type | Description |
|-----------|------|-------------|
| `specbeads:init` | Command | Initialize a repository with spec-kit and beads |
| `specbeads:beadify` | Command | Convert tasks.md into beads (epics for phases, tasks as children) |
| `specbeads:sync` | Command | Bidirectional sync between beads and tasks.md |
| `specbeads:status` | Command | Project progress dashboard with phase status and sync health |
| `specbeads:review-code` | Command | Review code for quality issues, create bug beads for findings |
| `specbeads:review-docs` | Command | Review documentation for completeness and accuracy |
| `specbeads:review-tests` | Command | Review tests for coverage and quality issues |
| `specbeads:review-spec` | Command | Validate implementation against spec-kit artifacts |

### [skill-creator](plugins/skill-creator/)

Guidance and tooling for creating high-quality Claude Code skills with validation and best practices.

| Component | Type | Description |
|-----------|------|-------------|
| `creating-skills` | Skill | End-to-end guide for creating and refining Claude Code skills |

### [runbooks](plugins/runbooks/)

Operational runbook creation with consistent structure and built-in maintenance feedback loops.

| Component | Type | Description |
|-----------|------|-------------|
| `create-runbook` | Skill | Create a new operational runbook from a standard template |

## Usage

### Adding This Marketplace

```bash
# If hosted on GitHub
/plugin marketplace add lumberbarons/lumber-mart

# For local testing
/plugin marketplace add /path/to/lumber-mart
```

### Installing Plugins

```bash
# List available plugins
/plugin list

# Install a plugin
/plugin install circuits@lumber-mart
```

## License

MIT
