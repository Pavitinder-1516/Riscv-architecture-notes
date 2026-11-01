# Day 31 — Revision of R-Type, I-Type, S/B-Type Instructions

> **Course:** Week 7, Video 1 &nbsp;|&nbsp; **Playlist #31** &nbsp;|&nbsp; [Chip Design with Rashid — RISC-V Architecture Explained](https://www.youtube.com/playlist?list=PL0-xus8sJBCRzZtmL_fLWaohRKuc4j5aH)  
> **Notes source:** video topic + standard RV32I material (to be updated from the transcript)

![Instruction formats](../diagrams/18_instruction_formats.png)

| Format | Has rd? | Has rs1? | Has rs2? | Immediate | Used by |
|---|---|---|---|---|---|
| **R** | ✔ | ✔ | ✔ | none | reg-reg ALU |
| **I** | ✔ | ✔ | ✘ | 12-bit [31:20] | ALU-imm, loads, `jalr`, system |
| **S** | ✘ | ✔ | ✔ | 12-bit split [31:25] + [11:7] | stores |
| **B** | ✘ | ✔ | ✔ | 13-bit (bit 0 = 0) scattered | branches |
| **U** | ✔ | ✘ | ✘ | 20-bit [31:12] | `lui`, `auipc` |
| **J** | ✔ | ✘ | ✘ | 21-bit (bit 0 = 0) scattered | `jal` |

## How to recognise the format from the hex quickly

Look at the **last two hex digits** (they contain opcode bits 6:0 plus `rd[0]` in bit 7):

| Ends with | Opcode | Format |
|---|---|---|
| `…33` / `…B3` | 0110011 | R |
| `…13` / `…93` | 0010011 | I (ALU) |
| `…03` / `…83` | 0000011 | I (load) |
| `…67` / `…E7` | 1100111 | I (jalr) |
| `…23` / `…A3` | 0100011 | S |
| `…63` / `…E3` | 1100011 | B |
| `…37` / `…B7` | 0110111 | U (lui) |
| `…17` / `…97` | 0010111 | U (auipc) |
| `…6F` / `…EF` | 1101111 | J |
| `…73` / `…F3` | 1110011 | system (ecall, ebreak, CSR) |

## Mini quiz from revision

| Machine code | Decoded |
|---|---|
| `0x007302B3` | `add x5, x6, x7` |
| `0xFFF50513` | `addi a0, a0, -1` |
| `0x00512423` | `sw t0, 8(sp)` |
| `0xFE629CE3` | `bne t0, t1, -8` |

---

## Week 7 Key Takeaways

- U-type: 20-bit upper immediate placed as-is; `lui` (absolute) and `auipc` (PC-relative).
- J-type: 21-bit even offset, scrambled, ±1 MiB.
- **Label offset = label address − instruction address**; labels take no space.
- Far jumps/addresses: `auipc` + `jalr`/`addi` with the +0x800 rounding.

## Practice Questions

1. Encode `lui t0, 0xABCDE`.
2. A `jal ra, func` is at `0x0400`, `func` is at `0x0380`. What is the offset? Is bit 31 of the encoding 0 or 1?
3. Encode `jal x0, +8`.
4. How many bytes forward can a single `beq` reach? A `jal`?
5. Why does `auipc` exist if we already have `lui`?

<details><summary>Answers</summary>

1. `0xABCDE2B7` (rd = x5 = 00101 → `0010 1011 0111` = `2B7`).
2. `0x380 − 0x400 = −0x80 = −128`; negative → bit 31 = 1.
3. `0x0080006F`.
4. `beq`: +4094 bytes; `jal`: +1,048,574 bytes (≈ 1 MiB).
5. `auipc` gives addresses relative to where the code is running (position-independent code, far calls); `lui` can only build absolute constants.
</details>

---
[⬅ Day 30](../Day-30-Label-Address-Calculation/README.md) | [Index](../README.md) | [Day 32 ➡](../Day-32-BNE-Backward-Label/README.md)
