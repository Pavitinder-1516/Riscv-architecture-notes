# Day 09 — Memory Architecture - Why PC+4 Has the Next Word

> **Course:** Week 3, Video 1 &nbsp;|&nbsp; **Playlist #9** &nbsp;|&nbsp; [Chip Design with Rashid — RISC-V Architecture Explained](https://www.youtube.com/playlist?list=PL0-xus8sJBCRzZtmL_fLWaohRKuc4j5aH)  
> **Notes source:** video topic + Rashid's weekly notes + standard RV32I material

![Byte addressable memory](../diagrams/07_memory_byte_addressing_pc.png)

## Key facts

- **Byte-addressable**: every address points to **one byte** (8 bits).
- A **word** is 4 bytes (32 bits). An RV32I instruction is one word.
- So consecutive instructions are at `0x0, 0x4, 0x8, 0xC …` → the next instruction is at **PC + 4**.
- Words are normally **aligned**: their address is a multiple of 4 (the two lowest address bits are `00`).

## The Program Counter (PC)

The PC holds the address of the instruction being executed. Every cycle:

```
instruction = Memory[PC]
if (branch taken or jump)  PC = target
else                       PC = PC + 4
```

The PC is **not** one of `x0–x31`; you cannot write it with `addi`. It changes only through branches and jumps (and traps).

## Memory organisation

| Architecture | Instruction & data memory | Notes |
|---|---|---|
| **Von Neumann** | one shared memory and bus | simpler, but fetch and data access compete |
| **Harvard** | separate instruction and data memories | fetch and load/store in the same cycle — used by most simple RISC-V cores and microcontrollers |

From the programmer's view, RISC-V has a single 32-bit address space (2³² bytes = 4 GiB); code, data, stack and peripherals are just different **regions** of it (more in Week 8).

## Typical program memory layout

```
 high addresses  ┌──────────────┐
                 │    Stack     │  ← sp starts here, grows DOWN
                 │      ↓       │
                 │      ↑       │
                 │    Heap      │  (malloc) grows UP
                 ├──────────────┤
                 │ .bss         │  uninitialised globals (zeroed at start-up)
                 │ .data        │  initialised globals
                 ├──────────────┤
                 │ .text        │  program code (instructions)
 low addresses   └──────────────┘
```

<!-- rashid-notes -->
## 📒 From Rashid's Week 3 notes

> Extra points and worked examples from Rashid's members-only weekly notes ([RISCV_Arch folder](https://drive.google.com/drive/folders/1sIX-rAanGWWkZocAbXNmvW80JbdAEg6P), members only). Written here in my own words; most of his examples come from the reference book *Digital Design and Computer Architecture, RISC-V Edition* (Harris & Harris), chapters 6–7.

![Rashid's memory example](../diagrams/53_rashid_memory_words.png)

- **The register file is faster than memory.** In RISC-V, the arithmetic and logic instructions only work on **registers**. Memory is only touched by loads and stores.
- **Memory is byte-addressable:** every byte has its own address. One **word = 4 bytes**, a **half-word = 2 bytes**.
- So word 0 is at address **0x0**, word 1 at **0x4**, word 2 at **0x8**, word 3 at **0xC**, word 4 at **0x10** — that is why the PC goes up by **4**.
- With a 32-bit address there are 2³² byte addresses: **0x0000_0000 … 0xFFFF_FFFF**.

His sample memory (used again in Day 10):

| Byte address | Word | Data (MSB … LSB) |
|---|---|---|
| 0x10 | word 4 | CD 19 A6 58 |
| 0x0C | word 3 | 40 F3 07 88 |
| 0x08 | word 2 | 01 EE 28 42 |
| 0x04 | word 1 | F2 F1 AC 07 |
| 0x00 | word 0 | AB CD EF 78 |

---
[⬅ Day 08](../Day-08-Week-1-2-Recap/README.md) | [Index](../README.md) | [Day 10 ➡](../Day-10-Load-Word-Store-Word/README.md)
