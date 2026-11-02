# Day 04 — What is a Register?

> **Course:** Week 2, Video 2 &nbsp;|&nbsp; **Playlist #4** &nbsp;|&nbsp; [Chip Design with Rashid — RISC-V Architecture Explained](https://www.youtube.com/playlist?list=PL0-xus8sJBCRzZtmL_fLWaohRKuc4j5aH)  
> **Notes source:** video topic + Rashid's weekly notes + standard RV32I material

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

<!-- rashid-notes -->
## 📒 From Rashid's Week 1,2 notes

> Extra points and worked examples from Rashid's members-only weekly notes ([RISCV_Arch folder](https://drive.google.com/drive/folders/1sIX-rAanGWWkZocAbXNmvW80JbdAEg6P), members only). Written here in my own words; most of his examples come from the reference book *Digital Design and Computer Architecture, RISC-V Edition* (Harris & Harris), chapters 6–7.

**"Revise registers"** — he points to his *Sequential Logic Design* series: Topic 01 (SR latch, D latch), Topic 02 (latch vs flip-flop), Topic 03 (flip-flops).

**Basic cells** come in two kinds:

- **Combinational:** AND, NAND, OR, NOR, INV …
- **Sequential:** LATCH, FLIP-FLOP

**A one-bit register** = a D flip-flop with **D, Q, EN, RESET, CLK**. Q only changes at the clock edge.

**Worked example — clock frequency:** if the clock edges come every 10 ns (0, 10 ns, 20 ns …) then

f = 1 / T = 1 / (10 × 10⁻⁹ s) = **100 MHz**.

In the timing sketch, D changes in the middle of a cycle, but Q only picks up the new value at the **next rising edge** (10 ns, 20 ns …).

**Every cell is judged on 4 things:** 1) functionality, 2) timing (delay), 3) power, 4) area — the famous **PPA** plus correctness.

His last sketch on this page: **flip-flop → adder → flip-flop**. That is the basic shape of every CPU pipeline — logic sandwiched between registers.

---
[⬅ Day 03](../Day-03-C-to-Assembly-to-Machine-Language/README.md) | [Index](../README.md) | [Day 05 ➡](../Day-05-Register-File/README.md)
