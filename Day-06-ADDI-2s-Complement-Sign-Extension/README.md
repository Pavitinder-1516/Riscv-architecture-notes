# Day 06 — Why Assembly? ADDI Instruction, 2's Complement, Sign Extension

> **Course:** Week 2, Video 4 &nbsp;|&nbsp; **Playlist #6** &nbsp;|&nbsp; [Chip Design with Rashid — RISC-V Architecture Explained](https://www.youtube.com/playlist?list=PL0-xus8sJBCRzZtmL_fLWaohRKuc4j5aH)  
> **Notes source:** video topic + standard RV32I material (to be updated from the transcript)

## Why learn assembly at all?

- To understand **what the hardware actually executes** — essential for designing CPUs.
- Debugging (crash dumps, disassembly), performance tuning, boot code, interrupt handlers, drivers.
- Writing the **startup code** of an SoC (set `sp`, clear `.bss`, jump to `main`) — this is always assembly.

## ADDI — add immediate

```asm
addi rd, rs1, imm      # rd = rs1 + sign_extend(imm[11:0])
```

- `imm` is a **12-bit signed** constant inside the instruction.
- Range: **−2048 … +2047**.
- There is **no `subi`** — just use a negative immediate: `addi t0, t0, -1`.

## 2's complement in 30 seconds

For an *n*-bit number, the MSB has weight **−2ⁿ⁻¹**; the rest are positive.

```
4-bit:  1011 = -8 + 0 + 2 + 1 = -5
Range of n bits: -2^(n-1) ... +2^(n-1) - 1
12 bits: -2048 ... +2047        32 bits: -2,147,483,648 ... +2,147,483,647
```

**To negate:** invert all bits, add 1. `5 = 0101 → 1010 + 1 = 1011 = −5`.

## Sign extension

The ALU works on 32 bits, but the immediate has only 12. The hardware **copies bit 11 (the sign bit) into bits 31…12**. This keeps the *value* unchanged.

![Sign extension](../diagrams/05_twos_complement_sign_ext.png)

| 12-bit imm | Sign-extended 32-bit | Value |
|---|---|---|
| `0x005` | `0x00000005` | +5 |
| `0xFFB` | `0xFFFFFFFB` | −5 |
| `0x7FF` | `0x000007FF` | +2047 |
| `0x800` | `0xFFFFF800` | −2048 |

## Useful pseudo-instructions built on ADDI

| Pseudo | Real instruction |
|---|---|
| `li rd, imm` (small) | `addi rd, x0, imm` |
| `mv rd, rs` | `addi rd, rs, 0` |
| `nop` | `addi x0, x0, 0` |

---
[⬅ Day 05](../Day-05-Register-File/README.md) | [Index](../README.md) | [Day 07 ➡](../Day-07-LUI-and-ADDI/README.md)
