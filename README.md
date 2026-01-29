# 🪵🛒 Lumber Mart

A plugin marketplace for Claude Code that lets you discover and install plugins for enhanced development workflows.

Learn more about Claude Code marketplaces in the [official documentation](https://code.claude.com/docs/en/plugin-marketplaces).

## Available Plugins

### circuits-plugin

### wavejson skill

Generate WaveJSON timing diagrams for digital signals and create HTML viewers to display them using WaveDrom. Perfect for hardware development, protocol analysis, and documenting signal timing in embedded systems projects.

**Features:**
- Generate WaveJSON format timing diagrams
- Create standalone HTML viewers with WaveDrom rendering
- Support for clock signals, data buses, control signals, and protocol sequences
- Built-in templates for common patterns (SPI, I2C, setup/hold timing, etc.)
- Quick reference documentation included

### circuit-synth skill

Create and design PCB circuits using Python and KiCad with AI assistance. Generate circuits from natural language descriptions, existing documentation, or templates. Search components, manage BOMs, and produce manufacturing-ready outputs.

**Features:**
- Define circuits in Python instead of GUI clicking
- Generate professional KiCad output (.kicad_pro, .kicad_sch, .kicad_pcb)
- AI-accelerated design workflows from natural language descriptions
- Convert hardware documentation/pinouts into formal schematics
- Search components with real-time stock and pricing (JLCPCB, DigiKey, Mouser)
- Pre-built manufacturing-ready patterns (buck/boost converters, LDO regulators, etc.)
- Generate manufacturing outputs (BOM, Gerbers, PDF schematics)
- Hierarchical design with modular subcircuits
- Version control friendly (text-based definitions)

### datasheet skill

Extract structured information from integrated circuit and component datasheets (PDF files or URLs) and generate comprehensive markdown summaries. Perfect for documenting components, creating reference materials for hardware projects, and building AI-consumable component libraries.

**Features:**
- Extract from both PDF files and URLs
- Structured 6-section format: General Info, Pinout, Usage, Electrical Characteristics, Package Info, Application Examples
- 100% accurate pinout tables with voltage levels and active HIGH/LOW indication
- Complete timing specifications with units and conditions
- Electrical characteristics tables with min/typ/max values
- Package variant documentation
- Human and AI-readable markdown output
- Save to standardized datasheets/ directory
- Source fidelity - only extracts from provided datasheet

### specbeads

Integrates [spec-kit](https://github.com/spec-kit/specify) with [beads](https://github.com/beads-project/beads) for streamlined specification-driven development. Convert spec-kit tasks into trackable beads, keep them synchronized, and run automated reviews that create beads for issues found.

**Features:**
- Initialize repos with both spec-kit and beads configuration
- Convert tasks.md phase/task breakdowns into beads (epics and child tasks)
- Bidirectional sync between beads and tasks.md
- Project progress dashboard with phase status and sync health
- Code review for quality issues (code smells, security, error handling)
- Documentation review for completeness and accuracy
- Test review for coverage, isolation, and output validation
- Spec conformance review against spec.md, plan.md, and constitution.md
- All review commands support `--dry-run` to preview findings without creating beads

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
/plugin install circuits-plugin@lumber-mart
```

## License

MIT
