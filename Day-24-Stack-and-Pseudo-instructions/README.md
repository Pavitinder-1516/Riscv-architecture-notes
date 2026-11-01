# Day 24 — Further Use of Stack, Pseudo-instructions

> **Course:** Week 5, Video 4 &nbsp;|&nbsp; **Playlist #24** &nbsp;|&nbsp; [Chip Design with Rashid — RISC-V Architecture Explained](https://www.youtube.com/playlist?list=PL0-xus8sJBCRzZtmL_fLWaohRKuc4j5aH)  
> **Notes source:** video topic + standard RV32I material (to be updated from the transcript)

## Other uses of the stack

| Use | How |
|---|---|
| Local arrays / structs | allocate space in the frame: `addi sp, sp, -32`, use `0(sp)…28(sp)` |
| Arguments 9+ | caller places them at `0(sp)`, `4(sp)` … |
| Spilling | when a function runs out of registers it saves values to the stack |
| Frame pointer | `s0`/`fp` can point to the start of the frame for easier debugging |
| Interrupt handlers | save *all* registers they touch (Week 8) |

## Local array example

```c
void f() { int buf[4] = {1, 2, 3, 4}; ... }
```

```asm
f:  addi sp, sp, -16
    li   t0, 1
    sw   t0, 0(sp)          # buf[0]
    li   t0, 2
    sw   t0, 4(sp)          # buf[1]
    li   t0, 3
    sw   t0, 8(sp)
    li   t0, 4
    sw   t0, 12(sp)
    ...
    addi sp, sp, 16
    ret
```

## Pseudo-instructions — the complete everyday list

A **pseudo-instruction** is assembler shorthand; the CPU never sees it — the assembler expands it into one or more real instructions.

| Pseudo | Expands to | Meaning |
|---|---|---|
| `nop` | `addi x0, x0, 0` | do nothing |
| `li rd, imm` | `addi` or `lui`+`addi` | load immediate |
| `la rd, symbol` | `auipc rd, %pcrel_hi(sym)` + `addi rd, rd, %pcrel_lo` | load address |
| `mv rd, rs` | `addi rd, rs, 0` | copy |
| `not rd, rs` | `xori rd, rs, -1` | bitwise NOT |
| `neg rd, rs` | `sub rd, x0, rs` | negate |
| `seqz rd, rs` | `sltiu rd, rs, 1` | rd = (rs == 0) |
| `snez rd, rs` | `sltu rd, x0, rs` | rd = (rs != 0) |
| `sltz rd, rs` | `slt rd, rs, x0` | rd = (rs < 0) |
| `sgtz rd, rs` | `slt rd, x0, rs` | rd = (rs > 0) |
| `beqz / bnez rs, L` | `beq / bne rs, x0, L` | |
| `blez / bgez / bltz / bgtz` | compare with x0 | |
| `bgt / ble / bgtu / bleu a, b, L` | swapped `blt / bge / bltu / bgeu` | |
| `j L` | `jal x0, L` | jump |
| `jal L` | `jal ra, L` | call (near) |
| `jr rs` | `jalr x0, 0(rs)` | jump register |
| `jalr rs` | `jalr ra, 0(rs)` | call via register |
| `ret` | `jalr x0, 0(ra)` | return |
| `call L` | `auipc ra, hi` + `jalr ra, lo(ra)` | call (far) |
| `tail L` | `auipc t1, hi` + `jalr x0, lo(t1)` | tail call |

---
[⬅ Day 23](../Day-23-Functions-Case-I-II/README.md) | [Index](../README.md) | [Day 25 ➡](../Day-25-All-40-Base-Instructions/README.md)
