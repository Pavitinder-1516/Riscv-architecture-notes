# Day 10 — Load Word and Store Word Instructions

> **Course:** Week 3, Video 2 &nbsp;|&nbsp; **Playlist #10** &nbsp;|&nbsp; [Chip Design with Rashid — RISC-V Architecture Explained](https://www.youtube.com/playlist?list=PL0-xus8sJBCRzZtmL_fLWaohRKuc4j5aH)  
> **Notes source:** video topic + Rashid's weekly notes + standard RV32I material

```asm
lw  rd,  offset(rs1)     # rd          = Memory32[rs1 + sign_ext(offset)]
sw  rs2, offset(rs1)     # Memory32[rs1 + sign_ext(offset)] = rs2
```

![Load store addressing](../diagrams/08_lw_sw_addressing.png)

- **Effective address = base register + 12-bit signed offset** (−2048 … +2047).
- `lw` is an **I-type** instruction; `sw` is **S-type** (it has no `rd` — it writes memory, not a register).
- RISC-V is a **load/store architecture**: to add two numbers in memory you must load both, add, then store.

## Example — `A[3] = A[1] + h`

`A` is an array of 32-bit ints whose base address is in `s0`; `h` is in `s1`.
Element `i` is at byte offset `4 × i`.

```asm
lw   t0, 4(s0)       # t0 = A[1]          (offset 1*4)
add  t0, t0, s1      # t0 = A[1] + h
sw   t0, 12(s0)      # A[3] = t0          (offset 3*4)
```

## Example — swap two memory words

```asm
# swap(*p, *q); p in a0, q in a1
lw   t0, 0(a0)
lw   t1, 0(a1)
sw   t1, 0(a0)
sw   t0, 0(a1)
```

> ⚠️ **Common mistake:** using index `i` directly as the offset. For words, the byte offset is `i × 4` (`slli t0, i, 2`).

<!-- rashid-notes -->
## 📒 From Rashid's Week 3 notes

> Extra points and worked examples from Rashid's members-only weekly notes ([RISCV_Arch folder](https://drive.google.com/drive/folders/1sIX-rAanGWWkZocAbXNmvW80JbdAEg6P), members only). Written here in my own words; most of his examples come from the reference book *Digital Design and Computer Architecture, RISC-V Edition* (Harris & Harris), chapters 6–7.

**`lw` = load a word from memory into a register.** High-level `a = mem[2]` (word 2).

```asm
lw s7, 8(zero)        # address = 8 + 0 = 0x8  → s7 = 0x01EE2842
```

`8(zero)` is **offset + base register**: offset 8, base = `zero` (0). Word 2 lives at byte address 2 × 4 = **8**.

**`sw` = store a word.** High-level `mem[5] = 42`.

```asm
addi t3, zero, 42     # t3 = 42 = 0x0000002A
sw   t3, 20(zero)     # address = 20 = 0x14 (word 5) → mem[0x14] = 0x0000002A
```

> ✏️ **Small correction:** on the board 42 is written as `101000` / `0x28` — that is **40**. 42 = `101010` = **0x2A**. The address part (word 5 → byte 20 = 0x14) is right.

Verified encodings: `lw s7, 8(zero)` = **0x00802B83**, `sw t3, 20(zero)` = **0x01C02A23**.

---
[⬅ Day 09](../Day-09-Memory-Architecture-PC-plus-4/README.md) | [Index](../README.md) | [Day 11 ➡](../Day-11-Logical-AND-OR-XOR/README.md)
