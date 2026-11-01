# Day 03 — C Language to Assembly to Machine Language

> **Course:** Week 2, Video 1 &nbsp;|&nbsp; **Playlist #3** &nbsp;|&nbsp; [Chip Design with Rashid — RISC-V Architecture Explained](https://www.youtube.com/playlist?list=PL0-xus8sJBCRzZtmL_fLWaohRKuc4j5aH)  
> **Notes source:** video topic + standard RV32I material (to be updated from the transcript)

![C to machine flow](../diagrams/02_c_to_machine_flow.png)

| Stage | Tool | Input → Output | Example |
|---|---|---|---|
| Compile | `gcc` / `clang` | `.c` → `.s` (assembly) | `x = y + 5;` → `addi x5, x6, 5` |
| Assemble | `as` | `.s` → `.o` (object, machine code) | `addi x5, x6, 5` → `0x00530293` |
| Link | `ld` | many `.o` + libraries → executable (`.elf`) | resolves labels / addresses |
| Load / run | loader / boot ROM | executable → memory | CPU starts fetching at the entry address |

## Three representations of the same instruction

```
C            :  x = y + 5;                      (x in register x5, y in x6)
Assembly     :  addi x5, x6, 5
Machine code :  000000000101 00110 000 00101 0010011
                imm = 5      rs1=6 f3  rd=5  opcode (OP-IMM)
Hex          :  0x00530293
```

- **Assembly** is a *human-readable* name for each machine instruction — there is (almost) a 1-to-1 mapping.
- **Machine code** is what is actually stored in memory and decoded by the hardware.
- Weeks 6–7 teach how to do this translation by hand.

## Try it yourself

```bash
riscv64-unknown-elf-gcc -march=rv32i -mabi=ilp32 -O1 -S add.c     # produces add.s
riscv64-unknown-elf-gcc -march=rv32i -mabi=ilp32 -O1 -c add.c     # produces add.o
riscv64-unknown-elf-objdump -d add.o                               # assembly + hex side by side
```

---
[⬅ Day 02](../Day-02-RV32I-Just-in-Time-Approach/README.md) | [Index](../README.md) | [Day 04 ➡](../Day-04-What-is-a-Register/README.md)
