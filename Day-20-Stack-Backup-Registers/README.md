# Day 20 — Using the Stack to Back Up Registers During a Function Call

> **Course:** Week 5, Video 1 &nbsp;|&nbsp; **Playlist #20** &nbsp;|&nbsp; [Chip Design with Rashid — RISC-V Architecture Explained](https://www.youtube.com/playlist?list=PL0-xus8sJBCRzZtmL_fLWaohRKuc4j5aH)  
> **Notes source:** video topic + standard RV32I material (to be updated from the transcript)

## The problem

There are only 32 registers, and **every function uses the same registers**. If `main` keeps a value in `s0` and calls `f`, and `f` also uses `s0`, `main`'s value is destroyed. Also, if `f` calls `g`, the `jal` to `g` **overwrites `ra`**, so `f` can no longer return to `main`.

**Solution:** temporarily save registers in memory — on the **stack**.

## What is the stack?

- A region of RAM used as **Last-In-First-Out** storage.
- `sp` (x2) points to the **top** of the stack (the last used word).
- In RISC-V the stack **grows downward** (toward lower addresses).
- The RISC-V ABI requires `sp` to be **16-byte aligned** at function calls.

![Stack frame](../diagrams/16_stack_frame.png)

## Push and pop (no dedicated instructions — use addi + sw/lw)

```asm
# PUSH t0
addi sp, sp, -4      # make room (grow down)
sw   t0, 0(sp)       # store

# POP t0
lw   t0, 0(sp)       # load
addi sp, sp, 4       # free the room
```

Better: allocate the whole **stack frame** once in the **prologue** and free it in the **epilogue**:

```asm
func:
    # ---- prologue ----
    addi sp, sp, -16     # allocate 16 bytes (keeps 16-byte alignment)
    sw   ra, 12(sp)      # save return address
    sw   s0,  8(sp)      # save s0 (we are going to use it)
    # ---- body ----
    ...
    # ---- epilogue ----
    lw   s0,  8(sp)      # restore in reverse
    lw   ra, 12(sp)
    addi sp, sp, 16      # free the frame
    ret
```

## Golden rules

1. Every `addi sp, sp, -N` must be matched by `addi sp, sp, +N` on every return path.
2. Restore registers before `ret`.
3. Never read data below `sp` — it can be overwritten (e.g. by an interrupt handler).

---
[⬅ Day 19](../Day-19-Week-4-Recap/README.md) | [Index](../README.md) | [Day 21 ➡](../Day-21-Stack-Callee-and-Caller/README.md)
