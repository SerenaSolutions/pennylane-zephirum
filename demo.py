import pennylane as qml
from zeph_gate import decide_qnode

dev = qml.device("default.qubit", wires=1)
@qml.qnode(dev)
def prob_zero():
    return qml.probs(wires=0)   # devolve [p0, p1]
def gate_zero():                # extrai so p0
    return prob_zero()[0]

r = decide_qnode(lambda: 1.0, "o qubit esta em |0> com margem declarada")
print("constante:", r["verdict"], "| selo:", r["receipt"]["selo_sha3_256"])
r2 = decide_qnode(lambda: gate_zero() * 0.0 + 0.5, "caso cinzento declarado")
print("cinzento:", r2["verdict"])
