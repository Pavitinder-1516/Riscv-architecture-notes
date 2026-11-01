# Week 3 examples: load/store, logic, shifts, branches (RV32I)
        .data
A:      .word 5, 10, 15, 20, 25
        .text
        .globl main
main:
        la   s0, A               # base address of A
        li   s1, 100             # h

        # A[3] = A[1] + h
        lw   t0, 4(s0)
        add  t0, t0, s1
        sw   t0, 12(s0)          # A[3] = 110

        # logic
        li   t1, 0xCA            # 1100 1010
        li   t2, 0xA6            # 1010 0110
        and  t3, t1, t2          # 0x82
        or   t4, t1, t2          # 0xEE
        xor  t5, t1, t2          # 0x6C
        xori t6, t1, -1          # NOT t1

        # shifts: a0 * 10 = (a0 << 3) + (a0 << 1)
        li   a0, 7
        slli t0, a0, 3
        slli t1, a0, 1
        add  a1, t0, t1          # a1 = 70
        li   t2, -64
        srai t3, t2, 2           # -16 (sign kept)
        srli t4, t2, 2           # large positive number

        # branch: a2 = max(a0, a1)
        mv   a2, a0
        bge  a0, a1, DONE
        mv   a2, a1
DONE:
        li   a7, 10
        ecall
