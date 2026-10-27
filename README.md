# pennylane-zephirum

**ZEPH-GATE — the trivalent decision layer for PennyLane circuits.**

Any PennyLane QNode returns probabilities; ZEPH-GATE declares the
statistical margin BEFORE the data and returns a **trivalent verdict**:

- `1` — affirmed (evidence clears the declared band)
- `0` — refuted
- `REFUSED_INSIDE_NOISE_BAND` — the evidence does not support a binary
  answer, and the gate refuses instead of guessing

Every verdict is sealed with a Z-QEA receipt (SHA3-256, chained).
Anti-peeking by construction: the margin is bound at call time.

```python
import pennylane as qml
from zeph_gate import zeph_decide

@qml.qnode(qml.device("default.qubit", wires=3))
def circuit():
    qml.Hadamard(wires=0)
    return qml.probs(wires=[0, 1, 2])

verdict, receipt = zeph_decide(circuit, margin=0.15, epsilon=0.05)
# verdict: "1" | "0" | "REFUSED_INSIDE_NOISE_BAND"
```

MIT. Author: Maria Clara dos Anjos (SerenaSolutions).
Validated on real quantum hardware — see the receipts chain in
[zephirum-lang](https://github.com/SerenaSolutions/zephirum-lang).
