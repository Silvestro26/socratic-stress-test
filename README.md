# Socratic Stress Test

![Tests](https://github.com/Silvestro26/socratic-stress-test/actions/workflows/test.yml/badge.svg)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Python 3.9+](https://img.shields.io/badge/python-3.9+-blue.svg)](https://www.python.org/downloads/)

## Project Description

The **Socratic Stress Test (SST)** is a framework for auditing epistemic reliability of reasoning systems through a structured 7-step methodology inspired by Socratic questioning.

### Key Features

- 🔍 **7-Step Protocol**: Systematic methodology for claim evaluation
- 🏷️ **Three-State Classification**: FACT / HYP (Hypothesis) / UNK (Unknown)
- 🧠 **Three Operating Modes**: 
  - `basic` - Direct questioning
  - `deep-ask` - Maieutic method with human guidance
  - `deep-auto` - Automated self-analysis
- ✅ **Comprehensive Testing**: 77+ unit tests
- 📊 **Confidence Scoring**: 0-100 scale with source and coherence factors

## Installation

```bash
# Clone the repository
git clone https://github.com/Silvestro26/socratic-stress-test.git
cd socratic-stress-test

# Install in development mode
pip install -e .

# Or install dependencies directly
pip install -r requirements.txt
```

## Quick Start

```python
from sst.core.protocol import SSTProtocol

# Create a protocol instance
protocol = SSTProtocol(mode="basic")

# Run the full 7-step protocol
report = protocol.run_full_protocol(
    statement="Water boils at 100°C at sea level.",
    sources=["CRC Handbook of Chemistry", "NIST Database"],
    coherence_score=90.0
)

# Access results
print(f"Classification: {report['full_analysis']['step5']['label']}")
print(f"Confidence: {report['full_analysis']['step6']['confidence']}%")
```

## The 7-Step Protocol

| Step | Name | Description |
|------|------|-------------|
| 1 | Statement Formulation | Clearly articulate the claim |
| 2 | Assumption Extraction | Identify implicit premises |
| 3 | Source Identification | Link to verifiable evidence |
| 4 | Coherence Testing | Check logical consistency |
| 5 | Classification | Assign FACT/HYP/UNK label |
| 6 | Confidence Quantification | Score 0-100 |
| 7 | Reporting | Generate reasoning chain |

## Classification States

| State | Value | Description |
|-------|-------|-------------|
| **FACT** | 1 | High confidence (≥85%) with verified sources |
| **HYP** | 0 | Hypothesis - plausible but needs verification |
| **UNK** | -1 | Unknown - insufficient evidence |

## Operating Modes

### Basic Mode
Direct questioning approach for straightforward claim evaluation.

```python
protocol = SSTProtocol(mode="basic")
```

### Deep-Ask Mode (Maieutic)
Interactive Socratic dialogue with human guidance.

```python
protocol = SSTProtocol(mode="deep-ask")
session = protocol.start_interactive_session("Your claim here")
```

### Deep-Auto Mode
Automated deep analysis without human intervention.

```python
protocol = SSTProtocol(mode="deep-auto")
results = protocol.run_auto_analysis(
    statement="Your claim",
    sources=["Source 1"],
    coherence_score=80.0
)
```

## Project Structure

```
socratic-stress-test/
├── sst/
│   ├── __init__.py
│   ├── core/
│   │   ├── claim.py          # Claim data model
│   │   ├── classification.py # FACT/HYP/UNK state machine
│   │   ├── protocol.py       # 7-step SST protocol
│   │   └── self_test.py      # Coherence & assumption analysis
│   └── prompts/
│       ├── basic.py          # Basic mode templates
│       ├── deep_ask.py       # Maieutic dialogue templates
│       └── deep_auto.py      # Automated analysis templates
├── tests/
│   ├── test_claim.py
│   ├── test_classification.py
│   ├── test_protocol.py
│   ├── test_prompts.py
│   └── test_self_test.py
├── examples/
│   └── run_sst_example.py
├── requirements.txt
├── setup.py
└── LICENSE
```

## Running Tests

```bash
# Run all tests
pytest tests/ -v

# Run with coverage
pytest tests/ -v --cov=sst --cov-report=term-missing
```

## Contributing

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## Acknowledgments

- Inspired by Socratic methodology and epistemic philosophy
- Built for auditing AI reasoning systems