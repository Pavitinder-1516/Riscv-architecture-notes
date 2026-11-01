# Day 15 — Week 3 Recap

> **Course:** Week 3, Recap &nbsp;|&nbsp; **Playlist #15** &nbsp;|&nbsp; [Chip Design with Rashid — RISC-V Architecture Explained](https://www.youtube.com/playlist?list=PL0-xus8sJBCRzZtmL_fLWaohRKuc4j5aH)  
> **Notes source:** video topic + standard RV32I material (to be updated from the transcript)

| Group | Instructions | Format |
|---|---|---|
| Memory | `lw`, `sw` | I, S |
| Logic | `and or xor`, `andi ori xori` | R, I |
| Compare | `slt sltu slti sltiu` | R, I |
| Shift | `sll srl sra`, `slli srli srai` | R, I |
| Branch | `beq bne blt bge bltu bgeu` | B |

---

## Week 3 Key Takeaways

- Memory is byte-addressed → next instruction at PC + 4; word `i` of an array is at offset `4i`.
- Address = base + sign-extended 12-bit offset.
- AND clears, OR sets, XOR toggles bits; NOT = `xori rd, rs, -1`.
- Shifts give ×2ⁿ / ÷2ⁿ; `sra` keeps the sign.
- Branches are PC-relative; choose signed (`blt/bge`) or unsigned (`bltu/bgeu`) carefully.

## Practice Questions

1. `s0 = 0x1000`. What address does `lw t0, -8(s0)` read?
2. Write code to clear bits 3 and 4 of `a0`.
3. `t0 = 0x80000000`. What is `t0` after `srai t0, t0, 4`? After `srli t0, t0, 4`?
4. Write `if (a0 > a1) a2 = 1;` using only real (non-pseudo) instructions.
5. Compute `t0 = a0 * 5` without a multiply instruction.

<details><summary>Answers</summary>

1. `0x1000 − 8 = 0x0FF8`.
2. `andi a0, a0, -25` (−25 = `...1110 0111`, bits 3 and 4 cleared).
3. `srai` → `0xF8000000`; `srli` → `0x08000000`.
4. `bge a1, a0, skip` ; `addi a2, x0, 1` ; `skip:` (a0 > a1 ⇔ !(a1 ≥ a0)).
5. `slli t0, a0, 2` ; `add t0, t0, a0`.
</details>

---
[⬅ Day 14](../Day-14-Conditional-Branches/README.md) | [Index](../README.md) | [Day 16 ➡](../Day-16-Jump-If-Else-Switch-Case/README.md)
