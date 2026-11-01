# Day 08 — Week 1 & 2 Recap

> **Course:** Week 2, Recap &nbsp;|&nbsp; **Playlist #8** &nbsp;|&nbsp; [Chip Design with Rashid — RISC-V Architecture Explained](https://www.youtube.com/playlist?list=PL0-xus8sJBCRzZtmL_fLWaohRKuc4j5aH)  
> **Notes source:** video topic + standard RV32I material (to be updated from the transcript)

| Concept | Remember |
|---|---|
| RV32I | 32 regs × 32 bits, 32-bit instructions, 40 instructions |
| `x0` | always 0 |
| Register file | 2 read ports, 1 write port; ABI names |
| `add / sub` | register-register |
| `addi` | 12-bit signed immediate, sign-extended, −2048…2047 |
| 2's complement | invert + 1; MSB has negative weight |
| `lui + addi` | build any 32-bit constant; add 1 to upper part when low ≥ 0x800 |

---

## Week 2 Key Takeaways

- C → (compiler) → assembly → (assembler) → machine code → (linker) → executable.
- Registers are the CPU's fastest storage; the ALU works only on registers.
- Immediates are sign-extended — this matters for `addi`, loads, stores, branches.
- Any 32-bit constant = `lui` + `addi` (with the +1 correction).

## Practice Questions

1. What is the 32-bit sign-extended value of the 12-bit immediate `0x9AB`?
2. Write instructions for `t0 = 0x0000_1800`.
3. Write instructions for `a0 = -1` and `a1 = 0x8000_0000`.
4. Why can't RISC-V have a 32-bit immediate in one instruction?
5. Translate `a = b - c + 100` (a in s0, b in s1, c in s2).

<details><summary>Answers</summary>

1. Bit 11 of `0x9AB` is 1 → `0xFFFFF9AB` (= −1621).
2. Low 12 = `0x800` → bit 11 = 1 → `lui t0, 0x2` ; `addi t0, t0, -2048` → `0x2000 − 0x800 = 0x1800`.
3. `addi a0, x0, -1` ; `lui a1, 0x80000`.
4. The instruction is 32 bits and must also contain an opcode and a register number.
5. `sub s0, s1, s2` ; `addi s0, s0, 100`.
</details>

---
[⬅ Day 07](../Day-07-LUI-and-ADDI/README.md) | [Index](../README.md) | [Day 09 ➡](../Day-09-Memory-Architecture-PC-plus-4/README.md)
