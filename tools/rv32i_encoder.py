#!/usr/bin/env python3
"""
rv32i_encoder.py - a tiny, readable RV32I instruction encoder for learning.

Usage:
    python3 rv32i_encoder.py "add x5, x6, x7"
    python3 rv32i_encoder.py "addi t0, t1, -5"
    python3 rv32i_encoder.py "sw t0, 8(sp)"
    python3 rv32i_encoder.py "beq a0, a1, -8"      # branch offset in bytes
    python3 rv32i_encoder.py "lui a0, 0x12345"
    python3 rv32i_encoder.py "jal ra, 2048"

It prints the binary split into the instruction-format fields and the hex
machine code, so you can check your hand-encoding from Weeks 6 and 7.
"""
import re
import sys

ABI = {
    "zero": 0, "ra": 1, "sp": 2, "gp": 3, "tp": 4, "t0": 5, "t1": 6, "t2": 7,
    "s0": 8, "fp": 8, "s1": 9, "a0": 10, "a1": 11, "a2": 12, "a3": 13, "a4": 14,
    "a5": 15, "a6": 16, "a7": 17, "s2": 18, "s3": 19, "s4": 20, "s5": 21,
    "s6": 22, "s7": 23, "s8": 24, "s9": 25, "s10": 26, "s11": 27, "t3": 28,
    "t4": 29, "t5": 30, "t6": 31,
}

# name: (format, opcode, funct3, funct7)
OPS = {
    # R-type
    "add": ("R", 0b0110011, 0b000, 0b0000000), "sub": ("R", 0b0110011, 0b000, 0b0100000),
    "sll": ("R", 0b0110011, 0b001, 0b0000000), "slt": ("R", 0b0110011, 0b010, 0b0000000),
    "sltu": ("R", 0b0110011, 0b011, 0b0000000), "xor": ("R", 0b0110011, 0b100, 0b0000000),
    "srl": ("R", 0b0110011, 0b101, 0b0000000), "sra": ("R", 0b0110011, 0b101, 0b0100000),
    "or": ("R", 0b0110011, 0b110, 0b0000000), "and": ("R", 0b0110011, 0b111, 0b0000000),
    # I-type ALU
    "addi": ("I", 0b0010011, 0b000, None), "slti": ("I", 0b0010011, 0b010, None),
    "sltiu": ("I", 0b0010011, 0b011, None), "xori": ("I", 0b0010011, 0b100, None),
    "ori": ("I", 0b0010011, 0b110, None), "andi": ("I", 0b0010011, 0b111, None),
    "slli": ("IS", 0b0010011, 0b001, 0b0000000), "srli": ("IS", 0b0010011, 0b101, 0b0000000),
    "srai": ("IS", 0b0010011, 0b101, 0b0100000),
    # loads (I-type)
    "lb": ("L", 0b0000011, 0b000, None), "lh": ("L", 0b0000011, 0b001, None),
    "lw": ("L", 0b0000011, 0b010, None), "lbu": ("L", 0b0000011, 0b100, None),
    "lhu": ("L", 0b0000011, 0b101, None),
    "jalr": ("L", 0b1100111, 0b000, None),
    # stores (S-type)
    "sb": ("S", 0b0100011, 0b000, None), "sh": ("S", 0b0100011, 0b001, None),
    "sw": ("S", 0b0100011, 0b010, None),
    # branches (B-type)
    "beq": ("B", 0b1100011, 0b000, None), "bne": ("B", 0b1100011, 0b001, None),
    "blt": ("B", 0b1100011, 0b100, None), "bge": ("B", 0b1100011, 0b101, None),
    "bltu": ("B", 0b1100011, 0b110, None), "bgeu": ("B", 0b1100011, 0b111, None),
    # U / J
    "lui": ("U", 0b0110111, None, None), "auipc": ("U", 0b0010111, None, None),
    "jal": ("J", 0b1101111, None, None),
}


def reg(tok):
    tok = tok.strip()
    if tok in ABI:
        return ABI[tok]
    m = re.fullmatch(r"x(\d+)", tok)
    if m and 0 <= int(m.group(1)) < 32:
        return int(m.group(1))
    raise ValueError(f"bad register: {tok}")


def imm(tok):
    return int(tok.strip(), 0)


def bits(v, n):
    return format(v & ((1 << n) - 1), f"0{n}b")


def encode(line):
    line = line.split("#")[0].strip()
    name, _, rest = line.partition(" ")
    name = name.lower()
    args = [a.strip() for a in rest.split(",")] if rest else []
    fmt, opc, f3, f7 = OPS[name]

    if fmt == "R":
        rd, rs1, rs2 = map(reg, args)
        word = (f7 << 25) | (rs2 << 20) | (rs1 << 15) | (f3 << 12) | (rd << 7) | opc
        fields = [("funct7", bits(f7, 7)), ("rs2", bits(rs2, 5)), ("rs1", bits(rs1, 5)),
                  ("funct3", bits(f3, 3)), ("rd", bits(rd, 5)), ("opcode", bits(opc, 7))]
    elif fmt in ("I", "IS"):
        rd, rs1, i = reg(args[0]), reg(args[1]), imm(args[2])
        if fmt == "IS":
            i = (f7 << 5) | (i & 0x1F)
        assert -2048 <= i <= 4095, "12-bit immediate out of range"
        word = ((i & 0xFFF) << 20) | (rs1 << 15) | (f3 << 12) | (rd << 7) | opc
        fields = [("imm[11:0]", bits(i, 12)), ("rs1", bits(rs1, 5)), ("funct3", bits(f3, 3)),
                  ("rd", bits(rd, 5)), ("opcode", bits(opc, 7))]
    elif fmt == "L":  # rd, off(rs1)
        rd = reg(args[0])
        off, base = re.fullmatch(r"(-?\w*)\((\w+)\)", args[1].replace(" ", "")).groups()
        i, rs1 = imm(off or "0"), reg(base)
        word = ((i & 0xFFF) << 20) | (rs1 << 15) | (f3 << 12) | (rd << 7) | opc
        fields = [("imm[11:0]", bits(i, 12)), ("rs1", bits(rs1, 5)), ("funct3", bits(f3, 3)),
                  ("rd", bits(rd, 5)), ("opcode", bits(opc, 7))]
    elif fmt == "S":  # rs2, off(rs1)
        rs2 = reg(args[0])
        off, base = re.fullmatch(r"(-?\w*)\((\w+)\)", args[1].replace(" ", "")).groups()
        i, rs1 = imm(off or "0"), reg(base)
        hi, lo = (i >> 5) & 0x7F, i & 0x1F
        word = (hi << 25) | (rs2 << 20) | (rs1 << 15) | (f3 << 12) | (lo << 7) | opc
        fields = [("imm[11:5]", bits(hi, 7)), ("rs2", bits(rs2, 5)), ("rs1", bits(rs1, 5)),
                  ("funct3", bits(f3, 3)), ("imm[4:0]", bits(lo, 5)), ("opcode", bits(opc, 7))]
    elif fmt == "B":
        rs1, rs2, i = reg(args[0]), reg(args[1]), imm(args[2])
        assert i % 2 == 0, "branch offset must be even"
        b12, b11 = (i >> 12) & 1, (i >> 11) & 1
        b10_5, b4_1 = (i >> 5) & 0x3F, (i >> 1) & 0xF
        word = (b12 << 31) | (b10_5 << 25) | (rs2 << 20) | (rs1 << 15) | (f3 << 12) | \
               (b4_1 << 8) | (b11 << 7) | opc
        fields = [("imm[12]", str(b12)), ("imm[10:5]", bits(b10_5, 6)), ("rs2", bits(rs2, 5)),
                  ("rs1", bits(rs1, 5)), ("funct3", bits(f3, 3)), ("imm[4:1]", bits(b4_1, 4)),
                  ("imm[11]", str(b11)), ("opcode", bits(opc, 7))]
    elif fmt == "U":
        rd, i = reg(args[0]), imm(args[1])
        word = ((i & 0xFFFFF) << 12) | (rd << 7) | opc
        fields = [("imm[31:12]", bits(i, 20)), ("rd", bits(rd, 5)), ("opcode", bits(opc, 7))]
    elif fmt == "J":
        rd, i = reg(args[0]), imm(args[1])
        assert i % 2 == 0, "jump offset must be even"
        b20, b10_1 = (i >> 20) & 1, (i >> 1) & 0x3FF
        b11, b19_12 = (i >> 11) & 1, (i >> 12) & 0xFF
        word = (b20 << 31) | (b10_1 << 21) | (b11 << 20) | (b19_12 << 12) | (rd << 7) | opc
        fields = [("imm[20]", str(b20)), ("imm[10:1]", bits(b10_1, 10)), ("imm[11]", str(b11)),
                  ("imm[19:12]", bits(b19_12, 8)), ("rd", bits(rd, 5)), ("opcode", bits(opc, 7))]
    return word & 0xFFFFFFFF, {"L": "I", "IS": "I"}.get(fmt, fmt), fields


if __name__ == "__main__":
    if len(sys.argv) < 2:
        print(__doc__)
        sys.exit(0)
    for ins in sys.argv[1:]:
        w, fmt, fields = encode(ins)
        print(f"{ins:28s} -> 0x{w:08X}   ({fmt}-type)")
        print("   " + " | ".join(f"{n}={v}" for n, v in fields))
