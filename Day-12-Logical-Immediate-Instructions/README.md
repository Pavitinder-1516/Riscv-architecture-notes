# Day 12 — Logical Immediate Instructions

> **Course:** Week 3, Video 4 &nbsp;|&nbsp; **Playlist #12** &nbsp;|&nbsp; [Chip Design with Rashid — RISC-V Architecture Explained](https://www.youtube.com/playlist?list=PL0-xus8sJBCRzZtmL_fLWaohRKuc4j5aH)  
> **Notes source:** video topic + Rashid's weekly notes + standard RV32I material

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

<!-- rashid-notes -->
## 📒 From Rashid's Week 3 notes

> Extra points and worked examples from Rashid's members-only weekly notes ([RISCV_Arch folder](https://drive.google.com/drive/folders/1sIX-rAanGWWkZocAbXNmvW80JbdAEg6P), members only). Written here in my own words; most of his examples come from the reference book *Digital Design and Computer Architecture, RISC-V Edition* (Harris & Harris), chapters 6–7.

**Immediate versions** from his notes:

```asm
andi s6, s0, 0xFF7    # clear bit 3 only
ori  s7, s0, 0x020    # set bit 5
xori s8, s1, -1       # flip every bit  (this is the 'not' pseudo-instruction)
```

**The trick to understand them:** the 12-bit immediate is **sign-extended** first.

- `0xFF7` = `1111 1111 0111` → bit 11 is 1 → becomes **0xFFFFFFF7**. ANDing with it keeps all 32 bits except bit 3. So `andi` can clear a low bit without destroying the upper 20 bits.
- `0x020` → `0x00000020`. ORing with it sets bit 5 and leaves everything else alone.
- `-1` → `0xFFFFFFFF`. XOR with all ones = invert every bit.

Example with s0 = `0x46A1F1B9` (ends in `1011 1001`):

- `andi s6, s0, 0xFF7` → bit 3 (the `1` in `…1001`) is cleared → s6 = **0x46A1F1B1**.

---
[⬅ Day 11](../Day-11-Logical-AND-OR-XOR/README.md) | [Index](../README.md) | [Day 13 ➡](../Day-13-Shift-Instructions/README.md)
