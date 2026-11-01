# Week 6/7 encoding examples.
# Assemble and compare with the hand encodings in the notes:
#   riscv64-unknown-elf-as -march=rv32i -mabi=ilp32 encoding_examples.s -o enc.o
#   riscv64-unknown-elf-objdump -d enc.o
# Or check one instruction at a time:  python3 ../../tools/rv32i_encoder.py "add x5, x6, x7"
        .text
        .option norvc
start:
        add  x5, x6, x7          # 0x007302B3  R
        sub  t2, t0, t1          # 0x406283B3  R
        addi a0, a0, -1          # 0xFFF50513  I
        lw   a0, 12(s0)          # 0x00C42503  I (load)
        srai t0, t1, 3           # 0x40335293  I (shift)
        sw   t0, 8(sp)           # 0x00512423  S
        li   t0, 0               #             (0x00000293)
        li   t1, 5               #             (0x00500313)
loop:   addi t0, t0, 1           # address 0x20 here; bne at 0x28 -> offset 0x20-0x28 = -8
        addi a0, a0, 2
        bne  t0, t1, loop        # 0xFE629CE3  B  offset -8
        jal  x0, done            # 0x0080006F  J  offset +8
        addi a0, a0, 100
done:   lui  a0, 0x12345         # 0x12345537  U
        jalr x0, 0(ra)           # 0x00008067  ret
