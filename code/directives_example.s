# Day 38: assembler directives - an example in the same style as the textbook's
# Assemble:  llvm-mc -triple=riscv32 -filetype=obj directives_example.s -o d.o
#            llvm-objdump -t -s -j .data d.o      (see symbol offsets and the bytes)

        .globl main                 # make 'main' visible to the start-up code
        .equ   N, 5                 # N is just a name for 5 (no memory used)

        .data                       # ---- goes to SRAM ----
A:      .word  5, 42, -88, 2, -5, 20, 7   # 7 words = 28 bytes, offsets 0x00-0x1B
str1:   .string "RISC-V"            # 6 chars + '\0' = 7 bytes, offsets 0x1C-0x22
        .align 2                    # 2^2 = 4: skip to the next multiple of 4 (0x24)
B:      .word  0x32A                # offset 0x24 (aligned)
C:      .space 4                    # 4 zero bytes, offset 0x28
D:      .space 1                    # 1 zero byte,  offset 0x2C
        .balign 4                   # same idea as .align 2: pad to 0x30

        .text                       # ---- code: goes to flash ----
main:
        la   t0, A                  # pseudo-instruction: load the address of A
        li   t1, N                  # becomes addi t1, x0, 5
        lw   t2, 8(t0)              # t2 = A[2] = -88
        la   t3, B
        lw   t4, 0(t3)              # t4 = 0x32A (one aligned read)
        sw   t2, 0(t3)              # B = -88
        ret

        .section .rodata            # ---- read-only data: flash, cannot be written ----
str2:   .string "read only"
