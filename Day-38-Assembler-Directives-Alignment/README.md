# Day 38 — Assembler Directives and 4-Byte Boundary Alignment

> **Course:** Week 9, Video 2 &nbsp;|&nbsp; **Playlist #38** &nbsp;|&nbsp; [Chip Design with Rashid — RISC-V Architecture Explained](https://www.youtube.com/playlist?list=PL0-xus8sJBCRzZtmL_fLWaohRKuc4j5aH)  
> **Notes source:** video topic + standard RV32I material (to be updated from the transcript)

## What is a directive?

An **assembler directive** starts with a dot (`.`). It is an instruction **to the assembler**, not to the CPU — it generates **no machine instruction** by itself. Directives tell the assembler where to put things, reserve/initialise data, define symbols and set alignment.

## The most important directives

| Directive | Meaning | Example |
|---|---|---|
| `.text` | following items go into the **code** section | `.text` |
| `.data` | initialised **data** section | `.data` |
| `.rodata` / `.section .rodata` | read-only data (constants, strings) | |
| `.bss` | zero-initialised data (takes no space in the file) | |
| `.section name` | put following items in a named section | `.section .init` |
| `.globl sym` / `.global` | make a symbol visible to the linker | `.globl main` |
| `.word v, …` | 32-bit value(s) | `arr: .word 1, 2, 3` |
| `.half v` | 16-bit value | `.half 0x1234` |
| `.byte v` | 8-bit value | `.byte 'A', 10` |
| `.ascii "s"` | string, **no** terminator | |
| `.asciz "s"` / `.string "s"` | string **with** `'\0'` | `msg: .asciz "Hi"` |
| `.space n` / `.zero n` | reserve *n* zero bytes | `buf: .space 64` |
| `.align n` | align to **2ⁿ** bytes (RISC-V GNU as) | `.align 2` → 4 bytes |
| `.balign n` | align to **n** bytes | `.balign 4` |
| `.equ name, value` / `.set` | define a constant | `.equ UART, 0x10013000` |
| `.option norvc` | don't use compressed instructions | |

## Example program using directives

```asm
        .data
msg:    .asciz "Hello"          # 6 bytes: H e l l o \0
        .align 2                # pad so the next item is 4-byte aligned
nums:   .word  10, 20, 30, 40
count:  .word  4
buf:    .space 16

        .text
        .globl main
main:
        la   a0, nums
        lw   t0, 0(a0)          # 10 — works because nums is word aligned
        ...
```

Memory layout of `.data` (assuming it starts at `0x1000`):

```
0x1000  'H'  'e'  'l'  'l'
0x1004  'o'  \0   pad  pad      ← .align 2 inserts 2 padding bytes
0x1008  nums[0] = 10            ← aligned to a multiple of 4 ✓
0x100C  nums[1] = 20
...
```

Without `.align 2`, `nums` would start at `0x1006` → a **misaligned** word.

## What does "4-byte boundary aligned" mean?

![Alignment](../diagrams/32_alignment.png)

An object of size *N* bytes is **naturally aligned** if its address is a multiple of *N*:

| Type | Size | Aligned address ends in (hex) | Lowest bits must be |
|---|---|---|---|
| byte | 1 | anything | — |
| half-word | 2 | 0, 2, 4, 6, 8, A, C, E | `…0` |
| word | 4 | **0, 4, 8, C** | **`…00`** |

## Why alignment matters

- A word at an aligned address lies entirely inside one memory word → **one** bus access.
- A misaligned word straddles two memory words → two accesses + shifting in hardware, **or** a misaligned-address **exception** (cause 4/6) on simple cores.
- **Instructions** must be 4-byte aligned in RV32I (2-byte with the C extension). A `jalr` to an odd address has bit 0 cleared automatically; a jump to `…2` without C causes an instruction-address-misaligned exception.
- `mtvec` must be 4-byte aligned (low 2 bits are the MODE field).

## Linker and sections (where directives end up)

The linker script places the sections in the SoC's memory map:

```
MEMORY { ROM (rx) : ORIGIN = 0x00000000, LENGTH = 64K
         RAM (rwx): ORIGIN = 0x80000000, LENGTH = 16K }
SECTIONS { .text : { *(.text*) } > ROM
           .data : { *(.data*) } > RAM AT > ROM
           .bss  : { *(.bss*)  } > RAM }
```

---
[⬅ Day 37](../Day-37-CPU-Exceptions/README.md) | [Index](../README.md) | [Day 39 ➡](../Day-39-Debug-GDB-OpenOCD-JTAG/README.md)
