# Autonomous System Reliability Harness (Mythos Pattern)

A closed-loop security automation harness that bridges probabilistic AI reasoning with deterministic operating system infrastructure. This repository sets up a self-contained pipeline that provisions an ephemeral Linux sandbox, compiles an instrumentation target, hits it with an escalating geometric input matrix, traps hardware/OS faults natively, and streams real-time telemetry back to an LLM loop for vulnerability synthesis.

## System Architecture

The harness orchestrates an automated validation loop that isolates runtime execution from host machines:

1. **Infrastructure Layer:** Leverages the official E2B Python SDK to spin up isolated, secure Firecracker MicroVM sandboxes on demand.
2. **Compilation Matrix:** Injects a parameterized, vulnerable C program directly into the virtual filesystem and compiles it natively with standard stack protections disabled (`-fno-stack-protector`).
3. **Telemetry Capture:** Feeds the binary geometric data strings (16, 64, and 128 bytes). It utilizes a specialized Python exception wrapper to absorb system crashes (`CommandExitException`), recording raw operating system exit status signatures.
4. **Reasoning Synthesis:** Packs the verified file system source code along with live execution logs into a data array, driving an advanced analytical report generation loop via frontier models.

---

## Getting Started

### 1. Prerequisites & Environment Setup

Ensure you have [Conda](https://docs.conda.io/en/latest/) installed on your machine. Create and activate the synchronized runtime environment using the provided configuration file:

```bash
# Clone the repository
git clone [https://github.com/your-username/mythos-reliability-harness.git](https://github.com/your-username/mythos-reliability-harness.git)
cd mythos-reliability-harness

# Provision the conda environment
conda env create -f environment.yaml
conda activate mythos-analysis
```

### 2. Export API Credentials

The harness automatically picks up authentication keys from your active system environment. Export your E2B and Anthropic credentials before starting the runtime loop:

```bash
export E2B_API_KEY="your-e2b-api-key"
export ANTHROPIC_API_KEY="your-anthropic-api-key"
```

### 3. Run the Evaluation Suite

Execute the main automation suite to spin up the sandbox, run the test matrix, and compile your local markdown report:

```bash
python harness.py
```

To review or visualize additional head-to-head benchmarking statistics generated across historical execution matrices, execute the pandas tracking reporter:

```bash
python analyze_results.py
```

---

## Sample Telemetry & Inferred Boundaries

During standard execution loops, the harness captures distinct phase metrics:

| Input Buffer | Operation Status | OS Exit Code | Inferred Frame State |
|--------------|------------------|--------------|----------------------|
| 16 Bytes     | `PASS`           | `0`          | Inside 32-Byte Allocation Frame |
| 64 Bytes     | `CRASH`          | `-1`         | Stack Frame Overrun / Return Memory Corruption |
| 128 Bytes    | `CRASH`          | `-1`         | Out-of-Bounds Memory Invalidation |

The final generated asset (`mythos_report.md`) breaks down the core structural flaws of the target logic, substituting hazardous bounded operations like legacy `strncpy` for production-grade validation patterns:

```c
size_t len = strlen(argv[1]);
if (len >= BUF_SZ) {
    fprintf(stderr, "error: argument too long (%zu >= %d)\n", len, BUF_SZ);
    return 2;
}
memcpy(buf, argv[1], len + 1); // Bounded memory copy inclusive of NUL termination
```

---

## Project Structure

```text
├── environment.yaml       # Conda environment specifications
├── harness.py             # Active closed-loop SDK automation harness
├── analyze_results.py     # Metrics processing and analytical charting tool
├── targets.json           # Definitions metadata for targeted repositories
└── mythos_report.md       # Final generated architectural stability analysis (Output)
```

## License

This project is open-source and available under the MIT License. Educational testing resources contained herein are restricted to authorized infrastructure evaluations and security discovery exploration loops.
