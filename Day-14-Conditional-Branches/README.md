# Day 14 — Branch Instructions - Conditional

> **Course:** Week 3, Video 6 &nbsp;|&nbsp; **Playlist #14** &nbsp;|&nbsp; [Chip Design with Rashid — RISC-V Architecture Explained](https://www.youtube.com/playlist?list=PL0-xus8sJBCRzZtmL_fLWaohRKuc4j5aH)  
> **Notes source:** video topic + standard RV32I material (to be updated from the transcript)

```asm
beq  rs1, rs2, label   # if (rs1 == rs2) goto label
bne  rs1, rs2, label   # if (rs1 != rs2)
blt  rs1, rs2, label   # if (rs1 <  rs2)  signed
bge  rs1, rs2, label   # if (rs1 >= rs2)  signed
bltu rs1, rs2, label   # if (rs1 <  rs2)  unsigned
bgeu rs1, rs2, label   # if (rs1 >= rs2)  unsigned
```

![Branch flow](../diagrams/11_branch_flow.png)

- **Taken** → `PC = PC + offset`; **not taken** → `PC = PC + 4`.
- The target is **PC-relative**: the instruction stores the *distance* to the label, not its absolute address (B-type, ±4 KiB range — Week 6).
- Branches compare two **registers**; to compare with a constant, load it into a register first (or use `x0` for zero).

## Signed vs unsigned matters

```
t0 = 0xFFFFFFFF, t1 = 1
blt  t0, t1, L   → taken      (-1 < 1)
bltu t0, t1, L   → NOT taken  (4,294,967,295 > 1)
```

## Pseudo-branches (assembler swaps operands for you)

| Pseudo | Real |
|---|---|
| `beqz rs, L` | `beq rs, x0, L` |
| `bnez rs, L` | `bne rs, x0, L` |
| `bgt a, b, L` | `blt b, a, L` |
| `ble a, b, L` | `bge b, a, L` |
| `bgtu / bleu` | `bltu / bgeu` with swapped operands |
| `bltz / bgez / blez / bgtz` | compare with x0 |

---
[⬅ Day 13](../Day-13-Shift-Instructions/README.md) | [Index](../README.md) | [Day 15 ➡](../Day-15-Week-3-Recap/README.md)
