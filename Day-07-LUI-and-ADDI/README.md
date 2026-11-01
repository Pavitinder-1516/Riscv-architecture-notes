# Day 07 — Assigning a Register a 32-bit Value with LUI and ADDI

> **Course:** Week 2, Video 5 &nbsp;|&nbsp; **Playlist #7** &nbsp;|&nbsp; [Chip Design with Rashid — RISC-V Architecture Explained](https://www.youtube.com/playlist?list=PL0-xus8sJBCRzZtmL_fLWaohRKuc4j5aH)  
> **Notes source:** video topic + standard RV32I material (to be updated from the transcript)

Problem: an instruction is only 32 bits, so it cannot hold a 32-bit constant *plus* an opcode and a register number. Solution: build it in **two** instructions.

## LUI — Load Upper Immediate

```asm
lui rd, imm20       # rd = imm20 << 12      (lower 12 bits become 0)
```

## Recipe for `li rd, 0xHHHHHLLL`

1. Split the constant into **upper 20 bits** (`H`) and **lower 12 bits** (`L`).
2. `lui rd, H`
3. `addi rd, rd, L`
4. ⚠️ **Correction:** `addi` *sign-extends* `L`. If bit 11 of `L` is 1 (i.e. `L ≥ 0x800`), `addi` effectively subtracts `0x1000`. To compensate, **use `H + 1`** in the `lui`.

## Example 1 — `0x12345678` (no correction needed)

```asm
lui  t0, 0x12345     # t0 = 0x12345000
addi t0, t0, 0x678   # t0 = 0x12345678     (0x678 < 0x800, positive)
```

## Example 2 — `0xDEADBEEF` (correction needed)

![LUI + ADDI](../diagrams/06_lui_addi.png)

```
lower 12 bits = 0xEEF  → bit 11 = 1 → as signed 12-bit = 0xEEF - 0x1000 = -0x111 (-273)
upper 20 bits = 0xDEADB → add 1 → 0xDEADC
```

```asm
lui  t0, 0xDEADC         # t0 = 0xDEADC000
addi t0, t0, -0x111      # t0 = 0xDEADC000 - 0x111 = 0xDEADBEEF ✓
```

The assembler's `li t0, 0xDEADBEEF` pseudo-instruction does exactly this automatically. In GNU assembly you can also write `lui t0, %hi(0xDEADBEEF)` / `addi t0, t0, %lo(0xDEADBEEF)` and it applies the correction for you.

## AUIPC (preview)

`auipc rd, imm20` → `rd = PC + (imm20 << 12)`. Same idea as LUI but relative to the PC — used for position-independent addresses (see Week 7).

---
[⬅ Day 06](../Day-06-ADDI-2s-Complement-Sign-Extension/README.md) | [Index](../README.md) | [Day 08 ➡](../Day-08-Week-1-2-Recap/README.md)
