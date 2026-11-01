# Day 30 — Recap of Jumps and How LABEL Address is Calculated

> **Course:** Week 7, Video 3 &nbsp;|&nbsp; **Playlist #30** &nbsp;|&nbsp; [Chip Design with Rashid — RISC-V Architecture Explained](https://www.youtube.com/playlist?list=PL0-xus8sJBCRzZtmL_fLWaohRKuc4j5aH)  
> **Notes source:** video topic + standard RV32I material (to be updated from the transcript)

This is the most important practical skill of the encoding weeks.

![Label offset calculation](../diagrams/27_label_offset_calc.png)

## Step 1 — the assembler assigns addresses

The assembler walks through the program; each instruction takes 4 bytes. Labels do **not** take space — a label is just a **name for the address of the next instruction**.

```asm
0x0000          li   t0, 0
0x0004          li   t1, 5
0x0008  loop:   addi t0, t0, 1         # loop  = 0x0008
0x000C          addi a0, a0, 2
0x0010          bne  t0, t1, loop
0x0014          jal  x0, done
0x0018          addi a0, a0, 100       # skipped
0x001C  done:   nop                    # done  = 0x001C
```

> ⚠️ A pseudo-instruction that expands into **two** instructions (`li` with a big constant, `la`, `call`) takes **8 bytes** — count it twice when computing addresses by hand!

## Step 2 — offset = target − current PC

| Instruction | At | Target | Offset | Machine code |
|---|---|---|---|---|
| `bne t0, t1, loop` | 0x10 | 0x08 | **−8** | `0xFE629CE3` |
| `jal x0, done` | 0x14 | 0x1C | **+8** | `0x0080006F` |

- The offset is relative to the address of the **branch/jump itself** (not PC+4 as on some other ISAs).
- Backward → negative; forward → positive.

## Step 3 — why PC-relative?

1. **Position independence**: the code works wherever it is loaded in memory.
2. **Smaller immediates**: most branches go only a few instructions away.

## Jumping farther than ±1 MiB, or to an absolute address

Use **`auipc` + `jalr`** (the `call` pseudo-instruction):

```
target = 0x1234_5678,   current PC = 0x0000_1000
offset = 0x1234_4678
hi     = (offset + 0x800) >> 12 = 0x12344      ← +0x800 = the same sign correction as lui/addi!
lo     = offset - (hi << 12)   = 0x678
```

```asm
auipc ra, 0x12344          # ra = 0x1000 + 0x12344000 = 0x12345000
jalr  ra, 0x678(ra)        # PC = 0x12345678 ; ra = return address
```

Together they reach **any** address in the 32-bit space (±2 GiB from PC).

## Loading a label's address: `la`

```asm
la a0, msg     →   auipc a0, %pcrel_hi(msg)
                   addi  a0, a0, %pcrel_lo(msg)
```

## Summary of jump-type instructions

| Instruction | Target | Range | Saves return? |
|---|---|---|---|
| `beq…bgeu` | PC + imm13 | ±4 KiB | no |
| `jal rd, L` | PC + imm21 | ±1 MiB | yes, in rd |
| `jalr rd, imm(rs1)` | rs1 + imm12 | anywhere (register) | yes, in rd |
| `auipc` + `jalr` | PC + 32-bit | ±2 GiB | yes |

---
[⬅ Day 29](../Day-29-U-J-Type-Encoding/README.md) | [Index](../README.md) | [Day 31 ➡](../Day-31-Revision-R-I-S-B/README.md)
