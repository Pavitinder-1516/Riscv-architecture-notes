# Day 17 — Loop Instructions

> **Course:** Week 4, Video 2 &nbsp;|&nbsp; **Playlist #17** &nbsp;|&nbsp; [Chip Design with Rashid — RISC-V Architecture Explained](https://www.youtube.com/playlist?list=PL0-xus8sJBCRzZtmL_fLWaohRKuc4j5aH)  
> **Notes source:** video topic + standard RV32I material (to be updated from the transcript)

There is no special "loop" instruction — a loop is a **branch that goes backwards**.

![Loop flow](../diagrams/13_loop_flow.png)

## for loop

```c
int sum = 0;
for (int i = 0; i < n; i++) sum += i;
```

```asm
# n in a1, sum in a0, i in t0
        li   a0, 0
        li   t0, 0
LOOP:   bge  t0, a1, DONE     # exit test at top
        add  a0, a0, t0       # body
        addi t0, t0, 1        # i++
        j    LOOP
DONE:
```

## while loop

```c
while (x != 0) { x = x >> 1; count++; }
```

```asm
WHILE:  beqz a0, WEND
        srli a0, a0, 1
        addi a1, a1, 1
        j    WHILE
WEND:
```

## do-while (test at the bottom — one branch per iteration)

```asm
LOOP:   add  a0, a0, t0
        addi t0, t0, 1
        blt  t0, a1, LOOP     # loop while i < n
```

Compilers often turn `for`/`while` into this shape (with one check before entry) because it executes one fewer jump per iteration.

## Counting down to zero (very common)

```asm
        li   t0, 10
L:      ...                   # body
        addi t0, t0, -1
        bnez t0, L
```

---
[⬅ Day 16](../Day-16-Jump-If-Else-Switch-Case/README.md) | [Index](../README.md) | [Day 18 ➡](../Day-18-Arrays-ASCII-Bytes-Halfwords/README.md)
