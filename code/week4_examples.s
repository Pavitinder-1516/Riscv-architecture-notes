# Week 4 examples: if-else, loops, arrays, strings, functions (RV32I)
        .data
arr:    .word 3, 1, 4, 1, 5, 9, 2, 6
msg:    .asciz "hello risc-v"
        .text
        .globl main
main:
        # sum = sum_array(arr, 8)
        la   a0, arr
        li   a1, 8
        jal  ra, sum_array       # a0 = 31
        mv   s0, a0

        # len = strlen(msg)
        la   a0, msg
        jal  ra, strlen          # a0 = 12
        mv   s1, a0

        # toupper(msg)
        la   a0, msg
        jal  ra, toupper         # msg = "HELLO RISC-V"

        # f(10, 20, 3, 7) = (10+20) - (3+7) = 20
        li   a0, 10
        li   a1, 20
        li   a2, 3
        li   a3, 7
        jal  ra, f
        mv   s2, a0

        li   a7, 10
        ecall

# int sum_array(int *a, int n)
sum_array:
        li   t0, 0
L1:     blez a1, E1
        lw   t1, 0(a0)
        add  t0, t0, t1
        addi a0, a0, 4           # pointer to next word
        addi a1, a1, -1
        j    L1
E1:     mv   a0, t0
        ret

# int strlen(char *s)
strlen: mv   t0, a0
L2:     lbu  t1, 0(t0)
        beqz t1, E2
        addi t0, t0, 1
        j    L2
E2:     sub  a0, t0, a0
        ret

# void toupper(char *s)
toupper:
L3:     lbu  t1, 0(a0)
        beqz t1, E3
        li   t2, 'a'
        blt  t1, t2, N3
        li   t2, 'z'
        bgt  t1, t2, N3
        addi t1, t1, -32
        sb   t1, 0(a0)
N3:     addi a0, a0, 1
        j    L3
E3:     ret

# int f(int g, int h, int i, int j)
f:      add  t0, a0, a1
        add  t1, a2, a3
        sub  a0, t0, t1
        ret
