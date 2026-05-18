# Reliability Analysis Report

## 1. Defect Identification

**Type:** Stack-based buffer overflow (CWE-121)
**Location:** `strcpy(buf, v[1])` — line 6
**Root cause:** `strcpy` performs an unbounded copy from attacker-controlled `argv[1]` into a fixed-size 32-byte stack buffer with no length validation.

## 2. Boundary Analysis

| Input size | Result | Reason |
|---|---|---|
| 16 bytes | PASS (exit 0) | Fits within `buf[32]` including NUL terminator |
| 64 bytes | CRASH | Overruns buffer by 32 bytes — corrupts saved frame pointer / return address |
| 128 bytes | CRASH | Severe overflow into stack canary / return address → SIGSEGV or stack-smash abort |

**Failure boundary lies between 32 and 64 bytes.** The exact failure threshold is:

- **Safe:** input length ≤ 31 (plus NUL = 32, fits exactly)
- **Undefined behavior begins at:** input length ≥ 32 (NUL written out-of-bounds)
- **Observable crash typically at:** input length ≥ ~40–48 (depends on compiler padding, stack canary placement, ABI)

The telemetry gap between 16 and 64 should be closed with tests at sizes **31, 32, 33, 40, 48** to confirm the precise boundary.

## 3. Clean Fix

Replace the unbounded copy with a bounded one and validate input length explicitly:

```c
#include <stdio.h>
#include <string.h>

#define BUF_SZ 32

int main(int argc, char *argv[]) {
    char buf[BUF_SZ];

    if (argc < 2) {
        fprintf(stderr, "usage: %s <arg>\n", argv[0]);
        return 1;
    }

    size_t len = strlen(argv[1]);
    if (len >= BUF_SZ) {
        fprintf(stderr, "error: argument too long (%zu >= %d)\n", len, BUF_SZ);
        return 2;
    }

    memcpy(buf, argv[1], len + 1);   /* includes NUL */
    return 0;
}
```

### Why this is clean
- **Explicit bound check** — fails loud and early instead of corrupting the stack.
- **`memcpy` with verified length** — avoids `strncpy`'s well-known pitfall of leaving the destination unterminated when the source equals the buffer size.
- **Distinct exit codes** (1 = usage, 2 = input violation) — improves observability in telemetry.
- **`BUF_SZ` constant** — single source of truth; eliminates magic numbers.

## 4. Recommended Hardening (Defense in Depth)

1. **Compile flags:** `-D_FORTIFY_SOURCE=2 -fstack-protector-strong -Wall -Wextra -Werror`
2. **Static analysis:** `clang --analyze`, Coverity, or CodeQL — would have flagged the `strcpy` immediately.
3. **Fuzzing:** AFL++/libFuzzer with size-progressive inputs to auto-discover boundary regressions.
4. **Sanitizers in CI:** Build a parallel artifact with `-fsanitize=address,undefined` to catch off-by-one cases that don't yet crash.

## 5. Summary
A single unchecked `strcpy` produces deterministic crashes once input exceeds the 32-byte stack buffer. The fix is a length-validated `memcpy` plus a constant-defined buffer size. Combined with FORTIFY, stack protector, and ASan in CI, this class of defect can be prevented from recurring.