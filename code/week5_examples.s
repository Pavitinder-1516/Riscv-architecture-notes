# Week 5 examples: stack frames, non-leaf functions, recursion (pure RV32I - no mul)
        .text
        .globl main
main:
        li   a0, 5
        jal  ra, fact            # a0 = 120
        mv   s0, a0

        li   a0, 3
        li   a1, 4
        jal  ra, sumsq           # a0 = 9 + 16 = 25
        mv   s1, a0

        li   a7, 10
        ecall

# int mul(int a, int b) - shift-and-add multiply (leaf, unsigned-style loop)
mul:    li   t0, 0
ML:     beqz a1, ME
        andi t1, a1, 1
        beqz t1, MS
        add  t0, t0, a0
MS:     slli a0, a0, 1
        srli a1, a1, 1
        j    ML
ME:     mv   a0, t0
        ret

# int sq(int x) { return x*x; }   - non-leaf because it calls mul
sq:     addi sp, sp, -16
        sw   ra, 12(sp)
        mv   a1, a0
        jal  ra, mul
        lw   ra, 12(sp)
        addi sp, sp, 16
        ret

# int sumsq(int a, int b) { return sq(a) + sq(b); }
sumsq:  addi sp, sp, -16
        sw   ra, 12(sp)
        sw   s0,  8(sp)
        sw   s1,  4(sp)
        mv   s1, a1              # keep b across the call
        jal  ra, sq
        mv   s0, a0              # keep sq(a) across the call
        mv   a0, s1
        jal  ra, sq
        add  a0, s0, a0
        lw   s1,  4(sp)
        lw   s0,  8(sp)
        lw   ra, 12(sp)
        addi sp, sp, 16
        ret

# int fact(int n) { return n <= 1 ? 1 : n * fact(n-1); }
fact:   addi sp, sp, -16
        sw   ra, 12(sp)
        sw   s0,  8(sp)
        mv   s0, a0
        li   t0, 1
        bgt  a0, t0, REC
        li   a0, 1
        j    FEND
REC:    addi a0, a0, -1
        jal  ra, fact            # a0 = fact(n-1)
        mv   a1, s0
        jal  ra, mul             # a0 = fact(n-1) * n
FEND:   lw   s0,  8(sp)
        lw   ra, 12(sp)
        addi sp, sp, 16
        ret
