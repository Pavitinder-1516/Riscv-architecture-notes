# Day 11 — Logical AND, OR, XOR - All Register Based

> **Course:** Week 3, Video 3 &nbsp;|&nbsp; **Playlist #11** &nbsp;|&nbsp; [Chip Design with Rashid — RISC-V Architecture Explained](https://www.youtube.com/playlist?list=PL0-xus8sJBCRzZtmL_fLWaohRKuc4j5aH)  
> **Notes source:** video topic + Rashid's weekly notes + standard RV32I material

```asm
and rd, rs1, rs2     # rd = rs1 & rs2
or  rd, rs1, rs2     # rd = rs1 | rs2
xor rd, rs1, rs2     # rd = rs1 ^ rs2
```

![Bitwise logic](../diagrams/09_bitwise_logic.png)

## Truth table (per bit)

| a | b | AND | OR | XOR |
|---|---|---|---|---|
| 0 | 0 | 0 | 0 | 0 |
| 0 | 1 | 0 | 1 | 1 |
| 1 | 0 | 0 | 1 | 1 |
| 1 | 1 | 1 | 1 | 0 |

## Why they matter

| Operation | Use |
|---|---|
| **AND** with a mask | *clear* / *extract* bits — `x & 0x0F` keeps the low 4 bits |
| **OR** with a mask | *set* bits — turn an LED bit on in a GPIO register |
| **XOR** with a mask | *toggle* bits — blink an LED; `x ^ x = 0`; compare two values for equality |

## NOT (there is no NOT instruction)

```asm
xori rd, rs, -1      # -1 = all ones → flips every bit   (pseudo: not rd, rs)
```

## Set-less-than (also register based)

```asm
slt  rd, rs1, rs2    # rd = (rs1 < rs2) ? 1 : 0   signed
sltu rd, rs1, rs2    # same, unsigned
```

`sltu rd, x0, rs` → `rd = (rs != 0)` (pseudo `snez`).

<!-- rashid-notes -->
## 📒 From Rashid's Week 3 notes

> Extra points and worked examples from Rashid's members-only weekly notes ([RISCV_Arch folder](https://drive.google.com/drive/folders/1sIX-rAanGWWkZocAbXNmvW80JbdAEg6P), members only). Written here in my own words; most of his examples come from the reference book *Digital Design and Computer Architecture, RISC-V Edition* (Harris & Harris), chapters 6–7.

**What each bitwise instruction is *for*:**

| Instruction | Typical use |
|---|---|
| **AND** | **clearing / masking** bits (keep only the bits where the mask is 1) |
| **OR** | **setting / combining** bits |
| **XOR** | **inverting** bits (XOR with 1 flips a bit) |

**Book Figure 6.1 example** — s1 = `0x46A1F1B7`, s2 = `0xFFFF0000`:

| Instruction | Result |
|---|---|
| `and s3, s1, s2` | **0x46A10000** (upper half kept, lower half cleared) |
| `or  s4, s1, s2` | **0xFFFFF1B7** (upper half forced to 1s) |
| `xor s5, s1, s2` | **0xB95EF1B7** (upper half flipped, lower half unchanged) |

(Checked with Python.)

---
[⬅ Day 10](../Day-10-Load-Word-Store-Word/README.md) | [Index](../README.md) | [Day 12 ➡](../Day-12-Logical-Immediate-Instructions/README.md)
