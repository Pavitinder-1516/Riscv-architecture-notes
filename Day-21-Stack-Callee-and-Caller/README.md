# Day 21 — Usage of the Stack by a Function that is Callee and Caller

> **Course:** Week 5, Video 3 &nbsp;|&nbsp; **Playlist #21** &nbsp;|&nbsp; [Chip Design with Rashid — RISC-V Architecture Explained](https://www.youtube.com/playlist?list=PL0-xus8sJBCRzZtmL_fLWaohRKuc4j5aH)  
> **Notes source:** video topic + standard RV32I material (to be updated from the transcript)

A **non-leaf** function is called by someone (*callee*) and itself calls someone (*caller*). It **must** save `ra`, because its own `jal` will overwrite it.

## Example — `sumsq(a, b) = sq(a) + sq(b)`

```c
int sq(int x)          { return x * x; }     // leaf (uses mul from M-ext, or a shift-add routine)
int sumsq(int a, int b){ return sq(a) + sq(b); }
```

```asm
sumsq:
    addi sp, sp, -16
    sw   ra, 12(sp)        # we call sq → ra will be overwritten
    sw   s0,  8(sp)        # we need s0, s1 → callee-saved → save them
    sw   s1,  4(sp)

    mv   s1, a1            # keep b safe across the first call (a1 is caller-saved!)
    jal  ra, sq            # a0 = sq(a)
    mv   s0, a0            # keep the result safe across the second call
    mv   a0, s1
    jal  ra, sq            # a0 = sq(b)
    add  a0, s0, a0        # result

    lw   s1,  4(sp)
    lw   s0,  8(sp)
    lw   ra, 12(sp)
    addi sp, sp, 16
    ret
```

## Recursion — factorial

```c
int fact(int n) { if (n <= 1) return 1; return n * fact(n - 1); }
```

```asm
fact:
    addi sp, sp, -16
    sw   ra, 12(sp)
    sw   s0,  8(sp)
    mv   s0, a0             # save n
    li   t0, 1
    bgt  a0, t0, RECURSE
    li   a0, 1              # base case
    j    FACT_END
RECURSE:
    addi a0, a0, -1
    jal  ra, fact           # a0 = fact(n-1)
    mul  a0, s0, a0         # needs M extension; in pure RV32I call a multiply routine
FACT_END:
    lw   s0,  8(sp)
    lw   ra, 12(sp)
    addi sp, sp, 16
    ret
```

Each recursive call creates **its own stack frame** holding its own `ra` and `n`:

```
            ┌───────────────┐ high
fact(3)     │ ra→main, s0   │
            ├───────────────┤
fact(2)     │ ra→fact, s0=3 │
            ├───────────────┤
fact(1)     │ ra→fact, s0=2 │ ← sp at the deepest point
            └───────────────┘ low
```

---
[⬅ Day 20](../Day-20-Stack-Backup-Registers/README.md) | [Index](../README.md) | [Day 22 ➡](../Day-22-Caller-vs-Callee-Saved/README.md)
