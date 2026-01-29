# circuits

A Claude Code plugin with skills and agents for microcontroller and other hardware projects.

## Overview

This plugin provides tools for hardware development workflows:
- **Timing diagram generation** from signal descriptions using WaveJSON/WaveDrom
- **PCB circuit design** using Python and KiCad with AI assistance
- **Datasheet extraction** from component PDFs and URLs into structured markdown

## Skills

| Skill | Description |
|-------|-------------|
| `wavejson` | Generate WaveJSON timing diagrams and standalone HTML viewers using WaveDrom |
| `circuit-synth` | Design PCB circuits in Python with KiCad output, component search, and manufacturing-ready exports |
| `datasheet` | Extract structured information from IC/component datasheets (PDF or URL) into markdown summaries |

### wavejson

Generate timing diagrams for digital signals using WaveJSON format and create standalone HTML viewers rendered with WaveDrom.

**Features:**
- Generate WaveJSON format timing diagrams
- Create standalone HTML viewers with WaveDrom rendering
- Support for clock signals, data buses, control signals, and protocol sequences
- Built-in templates for common patterns (SPI, I2C, setup/hold timing)
- Quick reference documentation included

**Usage:**
```
Ask Claude to generate a timing diagram for your protocol or signal sequence.
The skill produces WaveJSON and optionally an HTML viewer file.
```

### circuit-synth

Create and design PCB circuits using Python and KiCad with AI assistance. Generate circuits from natural language descriptions, existing documentation, or templates.

**Requirements:** Python 3.12+, `circuit-synth` package, optionally `reportlab`

**Features:**
- Define circuits in Python instead of GUI clicking
- Generate professional KiCad output (.kicad_pro, .kicad_sch, .kicad_pcb)
- AI-accelerated design from natural language descriptions
- Convert hardware documentation and pinouts into formal schematics
- Search components with real-time stock and pricing (JLCPCB, DigiKey, Mouser)
- Pre-built manufacturing-ready patterns (buck/boost converters, LDO regulators, etc.)
- Generate manufacturing outputs (BOM, Gerbers, PDF schematics)
- Hierarchical design with modular subcircuits
- Version control friendly (text-based definitions)

**Usage:**
```
Ask Claude to design a circuit, and it will create a Python project
using circuit-synth that generates KiCad-compatible output files.
```

### datasheet

Extract structured information from integrated circuit and component datasheets (PDF files or URLs) and generate comprehensive markdown summaries.

**Features:**
- Extract from both local PDF files and URLs
- Goal-oriented output in two sections: Circuit Design Information and Microcontroller Code Information
- 100% accurate pinout tables with voltage levels and active HIGH/LOW indication
- Complete timing specifications with units and conditions
- Saves to standardized `datasheets/` directory
- Source fidelity -- only extracts information present in the provided datasheet

**Usage:**
```
Provide Claude with a datasheet PDF path or URL and ask it to extract
the component information. Output goes to datasheets/<component>.md.
```

## Agents

| Agent | Description |
|-------|-------------|
| `datasheet-agent` | Autonomous agent that reads and extracts structured data from component datasheets |

The `datasheet-agent` is a specialized subagent used by the `datasheet` skill. It runs a 6-step extraction workflow: receive input, read/analyze the datasheet, extract goal-oriented sections, generate markdown, verify completeness, and provide a summary.
