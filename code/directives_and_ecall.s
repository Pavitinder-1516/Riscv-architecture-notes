# Week 9: assembler directives, alignment and ecall (RARS / Venus services)
        .data
msg:    .asciz "Sum = "          # 7 bytes incl. '\0'
        .align 2                 # 2^2 = 4-byte boundary for the words below
nums:   .word  10, 20, 30, 40
count:  .word  4
buf:    .space 16                # 16 zero bytes

        .equ   PRINT_INT, 1
        .equ   PRINT_STR, 4
        .equ   EXIT,      10

        .text
        .globl main
main:
        la   t0, nums
        la   t1, count
        lw   t1, 0(t1)
        li   a1, 0
L:      beqz t1, E
        lw   t2, 0(t0)           # aligned word load
        add  a1, a1, t2
        addi t0, t0, 4
        addi t1, t1, -1
        j    L
E:
        la   a0, msg
        li   a7, PRINT_STR
        ecall                    # print "Sum = "
        mv   a0, a1
        li   a7, PRINT_INT
        ecall                    # print 100
        li   a7, EXIT
        ecall
