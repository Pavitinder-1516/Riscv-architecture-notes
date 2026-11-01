# Day 04 — What is a Register?

> **Course:** Week 2, Video 2 &nbsp;|&nbsp; **Playlist #4** &nbsp;|&nbsp; [Chip Design with Rashid — RISC-V Architecture Explained](https://www.youtube.com/playlist?list=PL0-xus8sJBCRzZtmL_fLWaohRKuc4j5aH)  
> **Notes source:** video topic + standard RV32I material (to be updated from the transcript)

A **register** is a small, very fast storage location **inside the CPU**, built from flip-flops (D flip-flops clocked together). A 32-bit register = 32 flip-flops sharing a clock and a write-enable.

```
          write enable ──┐
 D[31:0] ──────────────►┌┴──────────────┐
                        │ 32 x D-FF     ├──► Q[31:0]
 clk ──────────────────►└───────────────┘
```

## Why registers?

| Storage | Where | Typical access time | Size |
|---|---|---|---|
| **Registers** | inside the CPU core | < 1 cycle | 32 × 4 B = 128 B |
| Cache (L1) | on chip | 1–4 cycles | KBs |
| Main memory (DRAM) | off chip | 100+ cycles | GBs |

- The ALU can only operate on **registers** (RISC load/store rule).
- Fewer registers → more trips to slow memory. More registers → more bits needed to name them and a bigger, slower register file. **32** is the RISC-V sweet spot: 5 bits name a register (2⁵ = 32).

## The special register `x0`

`x0` is **hard-wired to 0**. Reads always give 0; writes are ignored. It is extremely useful:

| Need | Use x0 |
|---|---|
| load a constant | `addi x5, x0, 42` |
| copy a register | `addi x5, x6, 0`  (pseudo `mv x5, x6`) |
| compare with zero | `beq x5, x0, label` |
| discard a result | `jal x0, label` (jump without saving return address) |
| do nothing | `addi x0, x0, 0` (= `nop`) |

---
[⬅ Day 03](../Day-03-C-to-Assembly-to-Machine-Language/README.md) | [Index](../README.md) | [Day 05 ➡](../Day-05-Register-File/README.md)
