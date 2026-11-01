# Week 2 examples - run in RARS / Venus / Ripes (RV32I)
        .text
        .globl main
main:
        # --- register basics -------------------------------------------
        addi t1, x0, 10          # t1 = 10
        addi t2, x0, 20          # t2 = 20
        add  t0, t1, t2          # t0 = 30
        sub  t3, t1, t2          # t3 = -10  (0xFFFFFFF6)

        # --- f = (g + h) - (i + j) --------------------------------------
        li   s1, 5               # g
        li   s2, 6               # h
        li   s3, 1               # i
        li   s4, 2               # j
        add  t0, s1, s2
        add  t1, s3, s4
        sub  s0, t0, t1          # s0 = 8

        # --- addi with negative immediate (sign extension) --------------
        addi t4, x0, -5          # t4 = 0xFFFFFFFB

        # --- 32-bit constants with lui + addi ---------------------------
        lui  t5, 0x12345
        addi t5, t5, 0x678       # t5 = 0x12345678

        lui  t6, 0xDEADC         # upper part +1 because 0xEEF has bit 11 set
        addi t6, t6, -0x111      # t6 = 0xDEADBEEF

        li   a0, 0xDEADBEEF      # the pseudo-instruction does the same

        # --- exit (RARS/Venus ecall 10) ----------------------------------
        li   a7, 10
        ecall
