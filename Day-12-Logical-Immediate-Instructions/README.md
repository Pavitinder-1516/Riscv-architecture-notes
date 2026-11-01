# Day 12 — Logical Immediate Instructions

> **Course:** Week 3, Video 4 &nbsp;|&nbsp; **Playlist #12** &nbsp;|&nbsp; [Chip Design with Rashid — RISC-V Architecture Explained](https://www.youtube.com/playlist?list=PL0-xus8sJBCRzZtmL_fLWaohRKuc4j5aH)  
> **Notes source:** video topic + standard RV32I material (to be updated from the transcript)

```asm
andi rd, rs1, imm    # rd = rs1 & sign_ext(imm)
ori  rd, rs1, imm
xori rd, rs1, imm
slti  rd, rs1, imm   # signed compare with immediate
sltiu rd, rs1, imm   # unsigned compare (imm is still sign-extended first!)
```

All are **I-type** with a 12-bit **sign-extended** immediate.

## Examples

```asm
andi t0, t1, 0xFF    # t0 = low byte of t1
ori  t0, t0, 0x1     # set bit 0
xori t0, t0, 0x4     # toggle bit 2
andi t0, t0, -2      # -2 = ...11110 → clear bit 0
sltiu t0, t1, 1      # t0 = (t1 == 0)   (pseudo: seqz t0, t1)
```

> ⚠️ Because the immediate is sign-extended, `andi t0, t1, 0x800` actually ANDs with `0xFFFFF800`, not `0x00000800`. For masks wider than 11 bits, build the mask with `lui`/`li` first and use the register form `and`.

---
[⬅ Day 11](../Day-11-Logical-AND-OR-XOR/README.md) | [Index](../README.md) | [Day 13 ➡](../Day-13-Shift-Instructions/README.md)
