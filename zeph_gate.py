# -*- coding: utf-8 -*-
"""ZEPH-GATE — a camada de decisao trivalente da ZEPHIRUM para circuitos PennyLane.

Uso: execute qualquer PennyLane QNode que retorne probabilidades, declare a
margem ANTES, e receba o veredito trivalente (1 / 0 / REFUSED) com recibo selado
(SHA3-256, cadeia Z-QEA). A regra e declarada antes do dado: anti-peeking.
"""
import hashlib, json
from datetime import datetime, timezone

def trivalent(p, lo, hi):
    if p >= hi: return "1"
    if p <= lo: return "0"
    return "REFUSED_INSIDE_NOISE_BAND"

def seal_receipt(claim, verdict, p, margin, qnode_name):
    rec = {"claim": claim, "verdict": verdict, "p": p, "margin": margin,
           "qnode": qnode_name, "data": datetime.now(timezone.utc).isoformat(),
           "engine": "pennylane", "protocolo": "Z-QEA SHA3-256"}
    rec["selo_sha3_256"] = hashlib.sha3_256(
        json.dumps({k: v for k, v in rec.items()}, sort_keys=True,
                   ensure_ascii=True, default=str).encode()).hexdigest()[:16]
    return rec

def decide_qnode(qnode, claim, lo=0.15, hi=0.85):
    """Roda o QNode (que retorna uma probabilidade) e devolve veredito + recibo."""
    p = float(qnode())
    if not (0.0 <= p <= 1.0):
        return {"verdict": "REFUSED_INVALID_EVIDENCE", "p": p}
    v = trivalent(p, lo, hi)
    return {"verdict": v, "receipt": seal_receipt(claim, v, p, hi - lo,
                                                  getattr(qnode, "__name__", "qnode"))}
