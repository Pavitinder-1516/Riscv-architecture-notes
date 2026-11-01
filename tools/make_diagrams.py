#!/usr/bin/env python3
"""Generates every PNG diagram in ../diagrams (matplotlib). Re-run after edits."""
import os
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib.patches import FancyBboxPatch, Rectangle, FancyArrowPatch

OUT = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "diagrams")
os.makedirs(OUT, exist_ok=True)

# palette
C = dict(op="#4C78A8", rd="#F58518", rs1="#54A24B", rs2="#B279A2", f3="#E45756",
         f7="#9D755D", imm="#EECA3B", ink="#1f2937", mute="#6b7280", bg="#f3f4f6",
         blue="#dbeafe", green="#dcfce7", amber="#fef3c7", rose="#ffe4e6",
         violet="#ede9fe", slate="#e5e7eb", teal="#ccfbf1")
plt.rcParams.update({"font.family": "DejaVu Sans", "font.size": 11})


def fig(w, h):
    f, ax = plt.subplots(figsize=(w, h), dpi=150)
    ax.set_xlim(0, w * 10)
    ax.set_ylim(0, h * 10)
    ax.axis("off")
    return f, ax


def save(f, name):
    f.savefig(os.path.join(OUT, name), bbox_inches="tight", facecolor="white", pad_inches=0.15)
    plt.close(f)


def box(ax, x, y, w, h, text, fc=C["blue"], ec=C["ink"], fs=11, bold=False, r=0.8, tc=None):
    ax.add_patch(FancyBboxPatch((x, y), w, h, boxstyle=f"round,pad=0,rounding_size={r}",
                                fc=fc, ec=ec, lw=1.3))
    ax.text(x + w / 2, y + h / 2, text, ha="center", va="center", fontsize=fs,
            weight="bold" if bold else "normal", color=tc or C["ink"], wrap=True)


def arrow(ax, x1, y1, x2, y2, text=None, color=None, fs=9, style="-|>", ls="-", rad=0.0, toff=(0, 1.2)):
    ax.add_patch(FancyArrowPatch((x1, y1), (x2, y2), arrowstyle=style, mutation_scale=14,
                                 color=color or C["ink"], lw=1.4, linestyle=ls,
                                 connectionstyle=f"arc3,rad={rad}"))
    if text:
        ax.text((x1 + x2) / 2 + toff[0], (y1 + y2) / 2 + toff[1], text, ha="center",
                va="center", fontsize=fs, color=C["mute"],
                bbox=dict(fc="white", ec="none", pad=0.5))


def title(ax, t, sub=None):
    xmax = ax.get_xlim()[1]
    ymax = ax.get_ylim()[1]
    ax.text(xmax / 2, ymax - 2, t, ha="center", va="top", fontsize=15, weight="bold", color=C["ink"])
    if sub:
        ax.text(xmax / 2, ymax - 6.2, sub, ha="center", va="top", fontsize=10.5, color=C["mute"])


# ---------------------------------------------------------------- bitfields
def bitfield(ax, x0, y0, width, fields, h=6, show_bits=True, fs=10, label=None):
    """fields: list of (name, nbits, color, value_text or None). MSB first (bit 31 left)."""
    total = sum(f[1] for f in fields)
    unit = width / total
    x = x0
    hi = total - 1
    if label:
        ax.text(x0 - 1.5, y0 + h / 2, label, ha="right", va="center", fontsize=12, weight="bold")
    for name, nb, col, val in fields:
        w = nb * unit
        ax.add_patch(Rectangle((x, y0), w, h, fc=col, ec="white", lw=2, alpha=0.9))
        ax.text(x + w / 2, y0 + h * (0.64 if val else 0.5), name, ha="center", va="center",
                fontsize=fs, color="white", weight="bold")
        if val:
            ax.text(x + w / 2, y0 + h * 0.27, val, ha="center", va="center", fontsize=fs - 1,
                    color="white", family="DejaVu Sans Mono")
        if show_bits:
            lo = hi - nb + 1
            ax.text(x + 0.3, y0 + h + 0.9, str(hi), ha="left", va="bottom", fontsize=8, color=C["mute"])
            if nb > 1:
                ax.text(x + w - 0.3, y0 + h + 0.9, str(lo), ha="right", va="bottom", fontsize=8, color=C["mute"])
            hi = lo - 1
        x += w


def d_formats():
    f, ax = fig(13, 8.6)
    title(ax, "RV32I Instruction Formats (32 bits each)", "Same field = same bit position in every format -> simple, fast decoder")
    I = C["imm"]; A = "#c9a227"
    rows = [
        ("R", [("funct7", 7, C["f7"], None), ("rs2", 5, C["rs2"], None), ("rs1", 5, C["rs1"], None),
               ("funct3", 3, C["f3"], None), ("rd", 5, C["rd"], None), ("opcode", 7, C["op"], None)]),
        ("I", [("imm[11:0]", 12, A, None), ("rs1", 5, C["rs1"], None),
               ("funct3", 3, C["f3"], None), ("rd", 5, C["rd"], None), ("opcode", 7, C["op"], None)]),
        ("S", [("imm[11:5]", 7, A, None), ("rs2", 5, C["rs2"], None), ("rs1", 5, C["rs1"], None),
               ("funct3", 3, C["f3"], None), ("imm[4:0]", 5, A, None), ("opcode", 7, C["op"], None)]),
        ("B", [("imm[12|10:5]", 7, A, None), ("rs2", 5, C["rs2"], None), ("rs1", 5, C["rs1"], None),
               ("funct3", 3, C["f3"], None), ("imm[4:1|11]", 5, A, None), ("opcode", 7, C["op"], None)]),
        ("U", [("imm[31:12]", 20, A, None), ("rd", 5, C["rd"], None), ("opcode", 7, C["op"], None)]),
        ("J", [("imm[20|10:1|11|19:12]", 20, A, None), ("rd", 5, C["rd"], None), ("opcode", 7, C["op"], None)]),
    ]
    desc = ["reg-reg ALU: add, sub, and, or, sll ...",
            "imm ALU, loads, jalr: addi, lw, jalr ...",
            "stores: sb, sh, sw",
            "cond. branches: beq, bne, blt ...",
            "upper imm: lui, auipc",
            "jump: jal"]
    y = 68
    for (lab, flds), d in zip(rows, desc):
        bitfield(ax, 8, y, 88, flds, h=6.5, label=lab)
        ax.text(97.5, y + 3.2, d, ha="left", va="center", fontsize=9.5, color=C["mute"])
        y -= 11.5
    ax.set_xlim(0, 135)
    save(f, "18_instruction_formats.png")


def d_encoding(name, asm, fields, note, fname):
    f, ax = fig(12, 3.6)
    ax.text(60, 33, f"{name}:  {asm}", ha="center", va="top", fontsize=14, weight="bold",
            family="DejaVu Sans Mono")
    bitfield(ax, 4, 12, 112, fields, h=10, fs=10)
    ax.text(60, 5, note, ha="center", va="center", fontsize=10.5, color=C["ink"],
            family="DejaVu Sans Mono")
    save(f, fname)


def d_encodings():
    A = "#c9a227"
    d_encoding("R-type", "add x5, x6, x7", [
        ("funct7", 7, C["f7"], "0000000"), ("rs2=x7", 5, C["rs2"], "00111"), ("rs1=x6", 5, C["rs1"], "00110"),
        ("funct3", 3, C["f3"], "000"), ("rd=x5", 5, C["rd"], "00101"), ("opcode", 7, C["op"], "0110011")],
        "0000 0000 0111 0011 0000 0010 1011 0011  =  0x007302B3", "19_rtype_example.png")
    d_encoding("I-type", "addi a0, a0, -1", [
        ("imm = -1", 12, A, "111111111111"), ("rs1=x10", 5, C["rs1"], "01010"),
        ("funct3", 3, C["f3"], "000"), ("rd=x10", 5, C["rd"], "01010"), ("opcode", 7, C["op"], "0010011")],
        "1111 1111 1111 0101 0000 0101 0001 0011  =  0xFFF50513", "20_itype_example.png")
    d_encoding("S-type", "sw t0, 8(sp)", [
        ("imm[11:5]", 7, A, "0000000"), ("rs2=x5", 5, C["rs2"], "00101"), ("rs1=x2", 5, C["rs1"], "00010"),
        ("funct3", 3, C["f3"], "010"), ("imm[4:0]", 5, A, "01000"), ("opcode", 7, C["op"], "0100011")],
        "offset 8 = 0000000_01000 split 7 | 5  ->  0x00512423", "21_stype_example.png")
    d_encoding("B-type", "bne t0, t1, -12", [
        ("imm[12|10:5]", 7, A, "1 111111"), ("rs2=x6", 5, C["rs2"], "00110"), ("rs1=x5", 5, C["rs1"], "00101"),
        ("funct3", 3, C["f3"], "001"), ("imm[4:1|11]", 5, A, "1010 1"), ("opcode", 7, C["op"], "1100011")],
        "-12 = 1_1111_1111_0100 (13 bits, bit0 dropped)  ->  0xFE629AE3", "22_btype_example.png")
    d_encoding("U-type", "lui a0, 0x12345", [
        ("imm[31:12] = 0x12345", 20, A, "0001 0010 0011 0100 0101"), ("rd=x10", 5, C["rd"], "01010"),
        ("opcode", 7, C["op"], "0110111")],
        "a0 = 0x12345 << 12 = 0x12345000   machine code 0x12345537", "24_utype_example.png")
    d_encoding("J-type", "jal ra, 16", [
        ("imm[20|10:1|11|19:12]", 20, A, "0 0000001000 0 00000000"), ("rd=x1", 5, C["rd"], "00001"),
        ("opcode", 7, C["op"], "1101111")],
        "ra = PC+4 ;  PC = PC + 16     machine code 0x010000EF", "25_jtype_example.png")


def d_imm_scramble(kind):
    f, ax = fig(12, 5.2)
    if kind == "B":
        title(ax, "B-type: how the 13-bit branch offset is scattered", "bit 0 is always 0 (offsets are multiples of 2) so it is not stored")
        imm_bits = list(range(12, 0, -1)) + [0]
        mapping = {31: 12, **{25 + k: 5 + k for k in range(6)}, **{8 + k: 1 + k for k in range(4)}, 7: 11}
        instr_ranges = [(31, 25), (11, 7)]
        fname = "23_btype_imm_bits.png"
    else:
        title(ax, "J-type: how the 21-bit jump offset is scattered", "bit 0 is always 0, giving a range of +/- 1 MiB around PC")
        imm_bits = list(range(20, 0, -1)) + [0]
        mapping = {31: 20, **{21 + k: 1 + k for k in range(10)}, 20: 11, **{12 + k: 12 + k for k in range(8)}}
        instr_ranges = [(31, 12)]
        fname = "26_jtype_imm_bits.png"
    # instruction row (only imm bits)
    ibits = sorted(mapping.keys(), reverse=True)
    n = len(ibits)
    cw = min(5.0, 104 / max(n, len(imm_bits)))
    x0 = 60 - n * cw / 2
    ax.text(x0 - 2, 31, "instruction\nbits", ha="right", va="center", fontsize=9.5, color=C["mute"])
    pos_i = {}
    for k, b in enumerate(ibits):
        x = x0 + k * cw
        ax.add_patch(Rectangle((x, 28), cw, 6, fc=C["op"], ec="white", lw=1.5))
        ax.text(x + cw / 2, 31, str(b), ha="center", va="center", color="white", fontsize=8.5, weight="bold")
        pos_i[b] = x + cw / 2
    # immediate row
    m = len(imm_bits)
    x1 = 60 - m * cw / 2
    ax.text(x1 - 2, 9, "offset\nbits", ha="right", va="center", fontsize=9.5, color=C["mute"])
    pos_m = {}
    for k, b in enumerate(imm_bits):
        x = x1 + k * cw
        fc = "#c9a227" if b != 0 else "#d1d5db"
        ax.add_patch(Rectangle((x, 6), cw, 6, fc=fc, ec="white", lw=1.5))
        ax.text(x + cw / 2, 9, str(b), ha="center", va="center", color="white" if b else C["ink"], fontsize=8.5, weight="bold")
        pos_m[b] = x + cw / 2
    for ib, mb in mapping.items():
        ax.plot([pos_i[ib], pos_m[mb]], [28, 12], color=C["mute"], lw=0.7, alpha=0.8)
    ax.text(pos_m[0], 3.5, "always 0", ha="center", fontsize=8, color=C["mute"])
    save(f, fname)


# ---------------------------------------------------------------- flows
def vflow(name, ttl, steps, w=9, edge_labels=None, sub=None):
    """steps: list of (text, kind) kind in {'start','proc','dec'}"""
    n = len(steps)
    H = n * 9 + 10
    f, ax = fig(w, H / 10)
    title(ax, ttl, sub)
    y = H - 12
    cx = w * 5
    prev = None
    for i, (t, kind) in enumerate(steps):
        fc = {"start": C["green"], "proc": C["blue"], "dec": C["amber"], "end": C["rose"]}[kind]
        bw = w * 10 * 0.8
        box(ax, cx - bw / 2, y - 6, bw, 6, t, fc=fc, fs=10, r=1.5 if kind in ("start", "end") else 0.5)
        if prev is not None:
            lab = edge_labels.get(i) if edge_labels else None
            arrow(ax, cx, prev, cx, y, lab)
        prev = y - 6
        y -= 9
    save(f, name)


def d_compile_flow():
    f, ax = fig(14, 5)
    title(ax, "From C to bits: what happens before the CPU runs your code")
    items = [("C source\nx = y + 5;", C["green"]), ("Compiler\n(gcc / clang)", C["slate"]),
             ("Assembly\naddi x5, x6, 5", C["blue"]), ("Assembler\n(as)", C["slate"]),
             ("Machine code\n0x00530293", C["amber"]), ("CPU\nfetch-decode-execute", C["rose"])]
    x = 2
    for i, (t, c) in enumerate(items):
        box(ax, x, 14, 19.5, 14, t, fc=c, fs=10.5, bold=(i % 2 == 0))
        if i < len(items) - 1:
            arrow(ax, x + 19.5, 21, x + 23.5, 21)
        x += 23.5
    ax.text(70, 7, "high-level  ->  human-readable machine instructions  ->  32-bit binary words stored in memory",
            ha="center", fontsize=10, color=C["mute"])
    save(f, "02_c_to_machine_flow.png")


def d_roadmap():
    f, ax = fig(14, 7.6)
    title(ax, "Course Roadmap - RISC-V Architecture Explained (CPU & Peripherals)")
    weeks = [("Week 1", "Overview,\nRV32I mindset", C["green"]),
             ("Week 2", "C->asm->binary,\nregisters, addi,\nlui", C["green"]),
             ("Week 3", "Memory, PC+4,\nlw/sw, logic,\nshifts, branches", C["blue"]),
             ("Week 4", "jumps, if-else,\nswitch, loops,\narrays, functions", C["blue"]),
             ("Week 5", "stack, caller /\ncallee saved,\npseudo-instr.", C["blue"]),
             ("Week 6", "encoding:\nR, I, S, B\ntypes", C["amber"]),
             ("Week 7", "U/J types,\nlabel offset\ncalculation", C["amber"]),
             ("Week 8", "peripherals,\nmemory map,\ninterrupts", C["rose"]),
             ("Week 9", "exceptions,\ndirectives,\ndebug (JTAG)", C["rose"])]
    for i, (w, t, c) in enumerate(weeks):
        row, col = divmod(i, 5)
        x = 4 + col * 27
        y = 44 - row * 26
        box(ax, x, y, 22, 18, "", fc=c)
        ax.text(x + 11, y + 15, w, ha="center", va="center", weight="bold", fontsize=11)
        ax.text(x + 11, y + 7, t, ha="center", va="center", fontsize=9.3)
        if i < len(weeks) - 1:
            if col < 4:
                arrow(ax, x + 22, y + 9, x + 27, y + 9)
    arrow(ax, 4 + 4 * 27 + 11, 44, 4 + 11, 36, rad=0.0, color=C["mute"], ls="--")
    lg = [("Foundations", C["green"]), ("Assembly programming", C["blue"]),
          ("Machine encoding", C["amber"]), ("SoC / system", C["rose"])]
    for i, (t, c) in enumerate(lg):
        ax.add_patch(Rectangle((20 + i * 26, 2), 3, 3, fc=c, ec=C["ink"]))
        ax.text(24 + i * 26, 3.5, t, va="center", fontsize=9.5)
    save(f, "01_course_roadmap.png")


def d_regfile_table():
    regs = [("x0", "zero", "hard-wired 0", "-"), ("x1", "ra", "return address", "caller"),
            ("x2", "sp", "stack pointer", "callee"), ("x3", "gp", "global pointer", "-"),
            ("x4", "tp", "thread pointer", "-"), ("x5", "t0", "temporary / alt. link", "caller"),
            ("x6", "t1", "temporary", "caller"), ("x7", "t2", "temporary", "caller"),
            ("x8", "s0/fp", "saved / frame pointer", "callee"), ("x9", "s1", "saved", "callee"),
            ("x10", "a0", "arg 0 / return value", "caller"), ("x11", "a1", "arg 1 / return value", "caller"),
            ("x12-17", "a2-a7", "function arguments", "caller"), ("x18-27", "s2-s11", "saved registers", "callee"),
            ("x28-31", "t3-t6", "temporaries", "caller")]
    f, ax = fig(11, 8.4)
    title(ax, "RV32I Integer Register File: 32 x 32-bit registers", "ABI names are just nicknames the assembler understands")
    hdr = ["Register", "ABI name", "Role", "Saved by"]
    xs = [5, 25, 45, 85]
    ws = [20, 20, 40, 20]
    y = 70
    for x, w_, h in zip(xs, ws, hdr):
        ax.add_patch(Rectangle((x, y), w_, 4.6, fc=C["ink"], ec="white"))
        ax.text(x + w_ / 2, y + 2.3, h, ha="center", va="center", color="white", weight="bold", fontsize=10)
    for r in regs:
        y -= 4.6
        fc = {"caller": C["amber"], "callee": C["green"], "-": C["slate"]}[r[3]]
        for x, w_, v in zip(xs, ws, r):
            ax.add_patch(Rectangle((x, y), w_, 4.6, fc=fc, ec="white"))
            ax.text(x + w_ / 2, y + 2.3, v, ha="center", va="center", fontsize=9.8,
                    family="DejaVu Sans Mono" if x < 45 else "DejaVu Sans")
    ax.text(55, y - 4, "green = callee-saved (preserved across calls)    amber = caller-saved (may be clobbered)",
            ha="center", fontsize=9.5, color=C["mute"])
    save(f, "03_register_file_table.png")


def d_regfile_block():
    f, ax = fig(11, 6.2)
    title(ax, "Register File: 2 read ports + 1 write port")
    box(ax, 38, 12, 30, 38, "", fc=C["violet"])
    ax.text(53, 46, "Register File", ha="center", weight="bold", fontsize=12)
    for i, t in enumerate(["x0 = 0", "x1", "x2", "...", "x31"]):
        ax.add_patch(Rectangle((44, 38 - i * 5.2), 18, 4.4, fc="white", ec=C["mute"]))
        ax.text(53, 40.2 - i * 5.2, t, ha="center", va="center", fontsize=9, family="DejaVu Sans Mono")
    ins = [("rs1 (5 bits)", 44, C["rs1"]), ("rs2 (5 bits)", 36, C["rs2"]), ("rd (5 bits)", 26, C["rd"]),
           ("write data (32)", 19, C["imm"]), ("RegWrite, clk", 13.5, C["mute"])]
    for t, y, c in ins:
        arrow(ax, 14, y, 38, y, color=c)
        ax.text(13, y, t, ha="right", va="center", fontsize=9.5, color=c, weight="bold")
    outs = [("read data 1 (32)", 40), ("read data 2 (32)", 26)]
    for t, y in outs:
        arrow(ax, 68, y, 88, y)
        ax.text(89, y, t, ha="left", va="center", fontsize=9.5, weight="bold")
    ax.text(53, 6, "Reads are combinational; the write to rd happens on the clock edge (if RegWrite=1).\nWrites to x0 are ignored - it always reads 0.",
            ha="center", fontsize=9.5, color=C["mute"])
    ax.set_xlim(-8, 120)
    save(f, "04_register_file_block.png")


def cells(ax, x, y, bitsstr, cw=2.2, h=4, fc=C["blue"], hl=None, fs=8.5):
    for i, b in enumerate(bitsstr):
        c = fc
        if hl and i in hl:
            c = hl[i]
        ax.add_patch(Rectangle((x + i * cw, y), cw, h, fc=c, ec="white"))
        ax.text(x + i * cw + cw / 2, y + h / 2, b, ha="center", va="center", fontsize=fs, family="DejaVu Sans Mono")
    return x + len(bitsstr) * cw


def d_sign_ext():
    f, ax = fig(13, 6.6)
    title(ax, "Two's complement & sign extension of a 12-bit immediate", "Copy the sign bit (bit 11) into bits 31..12 so the value stays the same")
    imm_n = "111111111011"  # -5
    imm_p = "000000000101"  # +5
    ax.text(3, 48, "addi t0, t1, -5", fontsize=11, weight="bold", family="DejaVu Sans Mono")
    ax.text(3, 43.5, "12-bit imm:", fontsize=9.5, color=C["mute"])
    cells(ax, 50, 42, imm_n, hl={0: C["rose"]})
    ax.text(3, 37, "sign-extended\nto 32 bits:", fontsize=9.5, color=C["mute"])
    cells(ax, 6 + 18, 35, "1" * 20, cw=2.2, fc=C["rose"])
    cells(ax, 24 + 44, 35, imm_n, fc=C["blue"])
    ax.text(124, 37, "= 0xFFFFFFFB = -5", fontsize=10, va="center")
    ax.text(3, 25, "addi t0, t1, +5", fontsize=11, weight="bold", family="DejaVu Sans Mono")
    ax.text(3, 20.5, "12-bit imm:", fontsize=9.5, color=C["mute"])
    cells(ax, 50, 19, imm_p, hl={0: C["green"]})
    ax.text(3, 14, "sign-extended\nto 32 bits:", fontsize=9.5, color=C["mute"])
    cells(ax, 24, 12, "0" * 20, fc=C["green"])
    cells(ax, 68, 12, imm_p, fc=C["blue"])
    ax.text(124, 14, "= 0x00000005 = +5", fontsize=10, va="center")
    ax.text(70, 4, "Negate in two's complement:  invert all bits, then add 1      5 = 0101  ->  1010 + 1 = 1011 = -5",
            ha="center", fontsize=10, color=C["ink"])
    ax.set_xlim(0, 150)
    save(f, "05_twos_complement_sign_ext.png")


def d_lui_addi():
    f, ax = fig(13, 5.8)
    title(ax, "Building a 32-bit constant:  li t0, 0xDEADBEEF", "lui loads the upper 20 bits, addi adds the lower 12 bits (which are sign-extended!)")
    ax.text(2, 41, "lui t0, 0xDEADC", family="DejaVu Sans Mono", fontsize=10.5, weight="bold")
    bitfield(ax, 40, 38, 96, [("0xDEADC (upper 20)", 20, "#c9a227", None), ("000 (12 zeros)", 12, "#9ca3af", None)], h=5.5, show_bits=False)
    ax.text(140, 40.8, "t0 = 0xDEADC000", va="center", fontsize=10)
    ax.text(2, 28, "addi t0, t0, -0x111", family="DejaVu Sans Mono", fontsize=10.5, weight="bold")
    bitfield(ax, 40, 25, 96, [("sign-extension of 0xEEF (all 1s)", 20, C["f3"], None), ("0xEEF", 12, C["op"], None)], h=5.5, show_bits=False)
    ax.text(140, 27.8, "+ 0xFFFFFEEF", va="center", fontsize=10)
    ax.plot([40, 165], [21.5, 21.5], color=C["ink"], lw=1)
    ax.text(140, 17.5, "t0 = 0xDEADBEEF", va="center", fontsize=11, weight="bold")
    ax.text(85, 8, "Rule: if bit 11 of the low part is 1 (low part >= 0x800), add 1 to the upper part.\n"
            "0xDEADB + 1 = 0xDEADC because addi will effectively subtract 0x1000 when it sign-extends.",
            ha="center", fontsize=9.8, color=C["mute"])
    ax.set_xlim(0, 170)
    save(f, "06_lui_addi.png")


def d_memory_pc():
    f, ax = fig(12, 7.6)
    title(ax, "Byte-addressable memory: why the next instruction is at PC + 4")
    addrs = ["0x0000_0000", "0x0000_0004", "0x0000_0008", "0x0000_000C", "0x0000_0010"]
    instr = ["addi x5, x0, 10", "addi x6, x0, 20", "add  x7, x5, x6", "sw   x7, 0(x8)", "..."]
    y = 58
    for i, (a, t) in enumerate(zip(addrs, instr)):
        ax.text(14, y + 3, a, ha="right", va="center", family="DejaVu Sans Mono", fontsize=9.5)
        for b in range(4):
            ax.add_patch(Rectangle((16 + b * 11, y), 11, 6, fc=C["blue"] if i != 1 else C["amber"], ec="white"))
            ax.text(16 + b * 11 + 5.5, y + 3, f"byte {i*4+b}", ha="center", va="center", fontsize=8)
        ax.text(64, y + 3, t, va="center", family="DejaVu Sans Mono", fontsize=10)
        y -= 8.5
    ax.text(110, 55, "PC = 0x0", fontsize=11, weight="bold", color=C["op"])
    arrow(ax, 109, 56, 92, 61, color=C["op"])
    ax.text(110, 47, "PC = PC + 4", fontsize=11, weight="bold", color=C["rd"])
    arrow(ax, 109, 48, 92, 53, color=C["rd"])
    ax.text(60, 9, "Every address names ONE byte.  Each RV32I instruction is 4 bytes (32 bits),\n"
            "so consecutive instructions are 4 addresses apart.  Instruction addresses are word-aligned (multiple of 4).",
            ha="center", fontsize=9.8, color=C["mute"])
    save(f, "07_memory_byte_addressing_pc.png")


def d_lw_sw():
    f, ax = fig(13, 6.6)
    title(ax, "Load / Store addressing:  effective address = rs1 + sign-extended offset")
    box(ax, 4, 34, 26, 12, "base register\nsp = 0x1000", fc=C["green"])
    box(ax, 4, 16, 26, 12, "offset (12-bit imm)\n+8", fc=C["amber"])
    ax.add_patch(plt.Circle((44, 31), 4.2, fc="white", ec=C["ink"], lw=1.4))
    ax.text(44, 31, "+", ha="center", va="center", fontsize=18)
    arrow(ax, 30, 40, 40, 33)
    arrow(ax, 30, 22, 40, 29)
    arrow(ax, 48.2, 31, 62, 31, "0x1008", toff=(0, 2))
    mem = [("0x1000", ""), ("0x1004", ""), ("0x1008", "0x0000002A"), ("0x100C", "")]
    for i, (a, v) in enumerate(mem):
        y = 46 - i * 8
        ax.add_patch(Rectangle((66, y), 30, 7, fc=C["amber"] if v else C["slate"], ec="white"))
        ax.text(64.5, y + 3.5, a, ha="right", va="center", fontsize=8.5, family="DejaVu Sans Mono")
        ax.text(81, y + 3.5, v, ha="center", va="center", fontsize=9, family="DejaVu Sans Mono")
    box(ax, 110, 38, 26, 9, "lw  t0, 8(sp)\nt0 <- Mem[0x1008]", fc=C["blue"], fs=9.5)
    box(ax, 110, 22, 26, 9, "sw  t0, 8(sp)\nMem[0x1008] <- t0", fc=C["rose"], fs=9.5)
    arrow(ax, 96, 33, 110, 42, color=C["op"])
    arrow(ax, 110, 26, 96, 32, color=C["f3"])
    ax.text(70, 5, "Only loads and stores touch memory (load/store architecture). ALU instructions work on registers only.",
            ha="center", fontsize=9.8, color=C["mute"])
    ax.set_xlim(0, 140)
    save(f, "08_lw_sw_addressing.png")


def d_logic():
    f, ax = fig(12, 6.6)
    title(ax, "Bitwise logic: each bit position is computed independently")
    a = "11001010"
    b = "10100110"
    rows = [("t1 =", a, C["blue"]), ("t2 =", b, C["blue"]),
            ("and t0,t1,t2", "".join(str(int(x) & int(y)) for x, y in zip(a, b)), C["green"]),
            ("or  t0,t1,t2", "".join(str(int(x) | int(y)) for x, y in zip(a, b)), C["amber"]),
            ("xor t0,t1,t2", "".join(str(int(x) ^ int(y)) for x, y in zip(a, b)), C["rose"])]
    y = 50
    for lab, bs, c in rows:
        ax.text(38, y + 2.2, lab, ha="right", va="center", family="DejaVu Sans Mono", fontsize=10.5)
        cells(ax, 40, y, bs, cw=5, h=4.5, fc=c, fs=10)
        y -= 7.5
        if lab == "t2 =":
            ax.plot([38, 82], [y + 5.6, y + 5.6], color=C["ink"], lw=0.8)
    uses = ["AND -> mask / clear bits (keep where mask=1)", "OR  -> set bits", "XOR -> toggle bits; x^x = 0;  xori rd,rs,-1 = NOT"]
    for i, u in enumerate(uses):
        ax.text(88, 34 - i * 6, u, fontsize=9.5, family="DejaVu Sans Mono")
    ax.set_xlim(0, 150)
    save(f, "09_bitwise_logic.png")


def d_shifts():
    f, ax = fig(12, 6.6)
    title(ax, "Shift instructions (shift amount = low 5 bits, 0..31)")
    src = "10110010"
    rows = [("original", src, None),
            ("sll  by 2", src[2:] + "00", {6: C["green"], 7: C["green"]}),
            ("srl  by 2", "00" + src[:-2], {0: C["green"], 1: C["green"]}),
            ("sra  by 2", "11" + src[:-2], {0: C["rose"], 1: C["rose"]})]
    y = 48
    for lab, bs, hl in rows:
        ax.text(30, y + 2.2, lab, ha="right", va="center", family="DejaVu Sans Mono", fontsize=10.5)
        cells(ax, 32, y, bs, cw=5, h=4.5, fc=C["blue"], hl=hl, fs=10)
        y -= 9
    notes = ["sll: fill with 0s from right   = x * 2^n",
             "srl: fill with 0s from left    = unsigned / 2^n",
             "sra: copy sign bit from left   = signed / 2^n (rounds toward -inf)"]
    for i, t in enumerate(notes):
        ax.text(80, 39 - i * 9, t, fontsize=9.5, family="DejaVu Sans Mono", va="center")
    ax.text(60, 6, "Immediate forms: slli, srli, srai.  srai is distinguished from srli by imm[10] (funct7 = 0100000).",
            ha="center", fontsize=9.6, color=C["mute"])
    ax.set_xlim(0, 150)
    save(f, "10_shift_ops.png")


def d_endian():
    f, ax = fig(11, 5.6)
    title(ax, "Little-endian: the least-significant byte goes to the lowest address")
    ax.text(10, 38, "register t0 = 0x12345678", fontsize=11, family="DejaVu Sans Mono", weight="bold")
    for i, b in enumerate(["12", "34", "56", "78"]):
        ax.add_patch(Rectangle((62 + i * 10, 36), 10, 5, fc=C["blue"], ec="white"))
        ax.text(67 + i * 10, 38.5, b, ha="center", va="center", family="DejaVu Sans Mono")
    ax.text(62, 43, "MSB", fontsize=8, color=C["mute"]); ax.text(94, 43, "LSB", fontsize=8, color=C["mute"])
    ax.text(10, 24, "sw t0, 0(a0)   (a0 = 0x2000)", fontsize=10.5, family="DejaVu Sans Mono")
    for i, (a, b) in enumerate(zip(["0x2000", "0x2001", "0x2002", "0x2003"], ["78", "56", "34", "12"])):
        ax.add_patch(Rectangle((20 + i * 18, 10), 18, 6, fc=C["amber"], ec="white"))
        ax.text(29 + i * 18, 13, b, ha="center", va="center", family="DejaVu Sans Mono")
        ax.text(29 + i * 18, 7.5, a, ha="center", va="center", fontsize=8.5, family="DejaVu Sans Mono", color=C["mute"])
    ax.text(100, 13, "lbu t1, 0(a0) -> t1 = 0x78\nlhu t1, 2(a0) -> t1 = 0x1234", fontsize=9.5, family="DejaVu Sans Mono", va="center")
    ax.set_xlim(0, 135)
    save(f, "14_little_endian.png")


def d_function_call():
    f, ax = fig(13, 6.4)
    title(ax, "Function call and return with jal / jalr")
    box(ax, 4, 14, 50, 36, "", fc=C["blue"])
    ax.text(29, 46.5, "caller (main)", ha="center", weight="bold")
    code = ["0x100: li   a0, 3", "0x104: li   a1, 4", "0x108: jal  ra, sum", "0x10C: mv   s0, a0   # <- returns here", "  ..."]
    for i, t in enumerate(code):
        ax.text(7, 41 - i * 5.5, t, family="DejaVu Sans Mono", fontsize=9.5,
                color=C["f3"] if "jal" in t else C["ink"])
    box(ax, 80, 22, 46, 24, "", fc=C["green"])
    ax.text(103, 42.5, "callee (sum)", ha="center", weight="bold")
    code2 = ["0x200: add  a0, a0, a1", "0x204: jalr x0, 0(ra)  # ret"]
    for i, t in enumerate(code2):
        ax.text(83, 36 - i * 6, t, family="DejaVu Sans Mono", fontsize=9.5,
                color=C["f3"] if "jalr" in t else C["ink"])
    arrow(ax, 54, 30, 80, 36, "jal: ra = 0x10C, PC = 0x200", rad=-0.2, toff=(0, 4))
    arrow(ax, 80, 28, 54, 24, "ret: PC = ra = 0x10C", rad=-0.2, toff=(0, -4.5))
    ax.text(65, 5, "Arguments go in a0-a7, return value in a0 (a1).  ret is a pseudo-instruction for jalr x0, 0(ra).",
            ha="center", fontsize=9.8, color=C["mute"])
    ax.set_xlim(0, 130)
    save(f, "15_function_call_jal_jalr.png")


def d_stack():
    f, ax = fig(12, 8.2)
    title(ax, "The stack: grows DOWN toward lower addresses")
    slots = [("0x7FFF_FFF0", "caller's data", C["slate"]),
             ("0x7FFF_FFEC", "ra (saved)", C["amber"]),
             ("0x7FFF_FFE8", "s0 (saved)", C["green"]),
             ("0x7FFF_FFE4", "s1 (saved)", C["green"]),
             ("0x7FFF_FFE0", "local var", C["blue"]),
             ("0x7FFF_FFDC", "(free)", "white"), ("0x7FFF_FFD8", "(free)", "white")]
    y = 62
    for a, t, c in slots:
        ax.add_patch(Rectangle((40, y), 30, 7, fc=c, ec=C["ink"], lw=0.8))
        ax.text(38, y + 3.5, a, ha="right", va="center", family="DejaVu Sans Mono", fontsize=9)
        ax.text(55, y + 3.5, t, ha="center", va="center", fontsize=9.5)
        y -= 7
    ax.text(74, 69 + 3.5 - 7, "<- old sp (on entry)", va="center", fontsize=9.5, color=C["mute"])
    ax.text(74, 69 + 3.5 - 35, "<- new sp = old sp - 16", va="center", fontsize=9.5, weight="bold", color=C["op"])
    ax.annotate("", xy=(20, 18), xytext=(20, 62), arrowprops=dict(arrowstyle="-|>", color=C["f3"], lw=1.6))
    ax.text(17, 38, "stack\ngrows\ndown", ha="right", va="center", fontsize=9.5, color=C["f3"])
    code = ["# prologue", "addi sp, sp, -16", "sw   ra, 12(sp)", "sw   s0,  8(sp)", "sw   s1,  4(sp)",
            "  ... body ...", "# epilogue", "lw   s1,  4(sp)", "lw   s0,  8(sp)", "lw   ra, 12(sp)", "addi sp, sp, 16", "ret"]
    for i, t in enumerate(code):
        ax.text(104, 66 - i * 4.4, t, family="DejaVu Sans Mono", fontsize=9.5,
                color=C["mute"] if t.startswith("#") else C["ink"])
    ax.text(70, 6, "sp must stay 16-byte aligned (RISC-V psABI). Push = decrement sp then store; Pop = load then increment sp.",
            ha="center", fontsize=9.5, color=C["mute"])
    ax.set_xlim(0, 140)
    save(f, "16_stack_frame.png")


def d_caller_callee():
    f, ax = fig(12, 5.8)
    title(ax, "Who saves which register?")
    box(ax, 4, 10, 54, 36, "", fc=C["amber"])
    ax.text(31, 42, "CALLER-saved (temporaries)", ha="center", weight="bold")
    ax.text(31, 26, "ra, t0-t6, a0-a7\n\nCallee may overwrite them freely.\nIf the caller still needs a value\nafter the call, the CALLER saves it\non the stack before 'jal'.",
            ha="center", va="center", fontsize=10)
    box(ax, 64, 10, 54, 36, "", fc=C["green"])
    ax.text(91, 42, "CALLEE-saved (preserved)", ha="center", weight="bold")
    ax.text(91, 26, "sp, s0-s11\n\nMust have the same value after\nthe call as before. If the CALLEE\nwants to use one, it saves it in its\nprologue and restores before 'ret'.",
            ha="center", va="center", fontsize=10)
    ax.text(61, 4, "zero, gp, tp are not allocated by normal functions.", ha="center", fontsize=9.5, color=C["mute"])
    ax.set_xlim(0, 122)
    save(f, "17_caller_callee_saved.png")


def d_label_offset():
    f, ax = fig(12, 7)
    title(ax, "Label address -> PC-relative offset", "offset = address(label) - address(branch/jump instruction)")
    code = [("0x0000", "        li   t0, 0"), ("0x0004", "        li   t1, 5"),
            ("0x0008", "loop:   addi t0, t0, 1"), ("0x000C", "        addi a0, a0, 2"),
            ("0x0010", "        bne  t0, t1, loop"), ("0x0014", "        jal  x0, done"),
            ("0x0018", "        addi a0, a0, 100"), ("0x001C", "done:   nop")]
    y = 55
    ys = {}
    for a, t in code:
        ax.text(8, y, a, family="DejaVu Sans Mono", fontsize=10, color=C["mute"], va="center")
        ax.text(20, y, t, family="DejaVu Sans Mono", fontsize=10.5, va="center",
                color=C["f3"] if ("bne" in t or "jal" in t) else C["ink"])
        ys[a] = y
        y -= 6
    arrow(ax, 64, ys["0x0010"], 64, ys["0x0008"], rad=0.5, color=C["op"])
    ax.text(75, (ys["0x0010"] + ys["0x0008"]) / 2, "0x08 - 0x10 = -8", fontsize=10, color=C["op"], weight="bold", va="center")
    arrow(ax, 60, ys["0x0014"], 60, ys["0x001C"], rad=-0.5, color=C["rd"])
    ax.text(75, (ys["0x0014"] + ys["0x001C"]) / 2, "0x1C - 0x14 = +8", fontsize=10, color=C["rd"], weight="bold", va="center")
    ax.text(60, 4, "Backward label -> negative offset;  forward label -> positive offset.  The assembler fills these in for you.",
            ha="center", fontsize=9.8, color=C["mute"])
    ax.set_xlim(0, 120)
    save(f, "27_label_offset_calc.png")


def d_soc():
    f, ax = fig(13, 7.4)
    title(ax, "A minimal RISC-V SoC: CPU talks to everything through the bus")
    box(ax, 6, 44, 30, 18, "RISC-V CPU core\n(RV32I)\nPC, regfile, ALU,\nCSRs", fc=C["violet"], bold=True, fs=10)
    box(ax, 46, 44, 26, 18, "Interrupt\ncontroller\n(PLIC / CLINT)", fc=C["rose"], fs=10)
    box(ax, 82, 44, 26, 18, "Debug module\n<- JTAG", fc=C["slate"], fs=10)
    ax.add_patch(Rectangle((6, 32), 118, 5, fc=C["ink"]))
    ax.text(65, 34.5, "System bus (address / data / control)  - e.g. AXI, AHB, APB, Wishbone, TileLink", ha="center", va="center", color="white", fontsize=9.5)
    per = [("Instr. memory\n(ROM / Flash)", C["blue"]), ("Data memory\n(SRAM)", C["blue"]), ("GPIO", C["green"]),
           ("UART", C["green"]), ("Timer", C["green"]), ("SPI / I2C", C["green"])]
    for i, (t, c) in enumerate(per):
        x = 6 + i * 20
        box(ax, x, 10, 17, 14, t, fc=c, fs=9)
        arrow(ax, x + 8.5, 32, x + 8.5, 24, style="<|-|>")
    arrow(ax, 21, 44, 21, 37, style="<|-|>")
    arrow(ax, 95, 44, 95, 37, style="<|-|>")
    arrow(ax, 46, 53, 36, 53, "IRQ", toff=(0, 2.2))
    for i in range(2, 6):
        x = 6 + i * 20 + 8.5
    ax.plot([6 + 2 * 20 + 14, 6 + 5 * 20 + 14], [26.5, 26.5], color=C["f3"], lw=1, ls="--")
    ax.plot([59, 59], [26.5, 44], color=C["f3"], lw=1, ls="--")
    ax.text(110, 27.5, "interrupt lines", fontsize=8.5, color=C["f3"])
    ax.set_xlim(0, 130)
    save(f, "28_soc_block.png")


def d_memmap():
    f, ax = fig(11, 8)
    title(ax, "Memory-mapped I/O: one address space for memory AND peripherals", "(example map - real addresses depend on the SoC)")
    regions = [("0x8001_0000", "unused / reserved", C["slate"], 6),
               ("0x8000_0000", "Data RAM (stack, heap, .data, .bss)", C["blue"], 10),
               ("0x1001_3000", "UART  (TXDATA, RXDATA, STATUS)", C["green"], 7),
               ("0x1001_2000", "GPIO  (OUTPUT, INPUT, DIR)", C["green"], 7),
               ("0x0200_0000", "CLINT timer (mtime, mtimecmp)", C["rose"], 7),
               ("0x0000_0000", "Boot ROM / Flash (.text code)", C["amber"], 10)]
    y = 66
    for a, t, c, h in regions:
        ax.add_patch(Rectangle((32, y - h), 44, h, fc=c, ec="white", lw=2))
        ax.text(54, y - h / 2, t, ha="center", va="center", fontsize=9.5)
        ax.text(30, y - h + 0.6, a, ha="right", va="bottom", fontsize=8.5, family="DejaVu Sans Mono")
        y -= h
    ax.text(80, 50, "Writing to a peripheral\nlooks like a normal store:", fontsize=9.5)
    ax.text(80, 38, "li  t0, 0x10012000\nli  t1, 1\nsw  t1, 0(t0)  # LED on\nlw  t2, 4(t0)  # read pins", family="DejaVu Sans Mono", fontsize=9.2)
    ax.text(80, 22, "Peripheral regions must be\nmarked non-cacheable and\naccessed with 'volatile' in C.", fontsize=9.2, color=C["mute"])
    ax.set_xlim(0, 115)
    save(f, "29_memory_map.png")


def d_interrupt12():
    steps = [
        ("1", "Peripheral event (UART byte arrives, timer expires, button press)"),
        ("2", "Device raises its interrupt line -> pending bit set (mip)"),
        ("3", "CPU checks: enabled in mie AND global mstatus.MIE = 1 ?"),
        ("4", "CPU completes the current instruction (precise interrupt)"),
        ("5", "Hardware saves PC of the next instruction into mepc"),
        ("6", "Hardware writes cause into mcause (MSB=1 for interrupt + code)"),
        ("7", "mstatus.MPIE <- MIE,  MIE <- 0 (block nesting),  MPP <- old mode"),
        ("8", "PC <- mtvec (direct: BASE  |  vectored: BASE + 4*cause)"),
        ("9", "ISR prologue: push the registers it will use onto the stack"),
        ("10", "ISR body: service device, CLEAR the interrupt source"),
        ("11", "ISR epilogue: pop the saved registers"),
        ("12", "mret: PC <- mepc,  MIE <- MPIE  -> program resumes"),
    ]
    f, ax = fig(12, 10.4)
    title(ax, "12-step interrupt action flow (RISC-V machine mode)")
    ax.plot([8, 8], [89, 92 - 11 * 7.4 - 2.8], color=C["ink"], lw=1.5, zorder=0)
    y = 92
    for i, (n, t) in enumerate(steps):
        c = C["green"] if i < 3 else (C["amber"] if i < 8 else C["blue"])
        if i == 11:
            c = C["rose"]
        ax.add_patch(plt.Circle((8, y - 2.8), 2.8, fc=C["ink"]))
        ax.text(8, y - 2.8, n, ha="center", va="center", color="white", fontsize=9, weight="bold")
        box(ax, 13, y - 5.6, 100, 5.6, t, fc=c, fs=9.6, r=0.4)
        y -= 7.4
    lg = [("device", C["green"]), ("hardware (automatic)", C["amber"]), ("software ISR", C["blue"]), ("return", C["rose"])]
    for i, (t, c) in enumerate(lg):
        ax.add_patch(Rectangle((14 + i * 26, 0.8), 3, 2.6, fc=c, ec=C["ink"]))
        ax.text(18 + i * 26, 2.1, t, va="center", fontsize=9)
    save(f, "30_interrupt_12_steps.png")


def d_exception():
    f, ax = fig(13, 7.4)
    title(ax, "Exceptions (synchronous traps) vs Interrupts (asynchronous)")
    box(ax, 4, 46, 50, 14, "Exception: caused BY the instruction\nillegal instr., misaligned address,\naccess fault, ecall, ebreak", fc=C["rose"], fs=9.5)
    box(ax, 72, 46, 50, 14, "Interrupt: caused by an outside event\ntimer, software (IPI), external device\n(not related to current instruction)", fc=C["green"], fs=9.5)
    box(ax, 38, 26, 50, 12, "Trap entry (hardware)\nmepc, mcause, mtval, mstatus;  PC <- mtvec", fc=C["amber"], fs=9.5)
    arrow(ax, 29, 46, 50, 38)
    arrow(ax, 97, 46, 76, 38)
    box(ax, 38, 6, 50, 12, "Trap handler (software)\nread mcause -> fix / emulate / report\nmepc += 4 for ecall/ebreak, then mret", fc=C["blue"], fs=9.5)
    arrow(ax, 63, 26, 63, 18)
    ax.text(105, 22, "mepc for an exception =\naddress of the FAULTING\ninstruction itself", fontsize=9, color=C["mute"], ha="center")
    ax.text(18, 22, "mcause MSB:\n1 = interrupt\n0 = exception", fontsize=9, color=C["mute"], ha="center")
    ax.set_xlim(0, 128)
    save(f, "31_exception_flow.png")


def d_alignment():
    f, ax = fig(12, 5.4)
    title(ax, "Alignment: a word should start at an address that is a multiple of 4")
    for r, (lab, start, ok) in enumerate([("aligned word at 0x1004", 4, True), ("misaligned word at 0x1006", 6, False)]):
        y = 30 - r * 15
        ax.text(4, y + 3, lab, fontsize=10, va="center", weight="bold", color="#15803d" if ok else C["f3"])
        for b in range(12):
            addr = b
            inside = start <= addr < start + 4
            ax.add_patch(Rectangle((50 + b * 6, y), 6, 6, fc=(C["green"] if ok else C["rose"]) if inside else C["slate"], ec="white"))
            ax.text(53 + b * 6, y - 1.6, f"0x100{addr:X}", ha="center", fontsize=6, color=C["mute"])
        for wb in range(4):
            ax.plot([50 + wb * 24, 50 + wb * 24], [y - 0.5, y + 6.5], color=C["ink"], lw=1.8)
    ax.text(62, 2.5, ".align 2  /  .balign 4  pads with zeros so the next item starts on a 4-byte boundary",
            ha="center", fontsize=9.8, color=C["mute"], family="DejaVu Sans Mono")
    ax.set_xlim(0, 125)
    save(f, "32_alignment.png")


def d_debug():
    f, ax = fig(14, 5.2)
    title(ax, "On-chip debug chain: GDB -> OpenOCD -> JTAG -> Debug Module -> CPU")
    items = [("GDB\n(break, step,\nprint regs)", C["blue"]), ("OpenOCD\n(GDB server,\nport 3333)", C["green"]),
             ("JTAG adapter\n(USB probe)", C["amber"]), ("DTM + Debug\nModule (DM)\non the SoC", C["rose"]),
             ("RISC-V hart\nhalt / resume,\nGPR / CSR / mem", C["violet"])]
    x = 2
    labels = ["TCP (RSP)", "USB", "TCK TMS\nTDI TDO", "DMI bus"]
    for i, (t, c) in enumerate(items):
        box(ax, x, 12, 20, 20, t, fc=c, fs=9.4)
        if i < len(items) - 1:
            arrow(ax, x + 20, 22, x + 30, 22, style="<|-|>")
            ax.text(x + 25, 26.5, labels[i], ha="center", va="bottom", fontsize=7.8, color=C["mute"])
        x += 30
    ax.text(70, 4, "Host PC (software)                      board / cable                         inside the chip",
            ha="center", fontsize=9.5, color=C["mute"])
    ax.set_xlim(0, 144)
    save(f, "33_debug_chain.png")


def d_isa_overview():
    f, ax = fig(14, 9.2)
    title(ax, "RV32I base: 40 instructions (37 for normal programs + fence, ecall, ebreak)")
    groups = [("Arithmetic", ["add", "sub", "addi", "lui", "auipc"], C["blue"]),
              ("Logical", ["and", "or", "xor", "andi", "ori", "xori"], C["green"]),
              ("Shifts", ["sll", "srl", "sra", "slli", "srli", "srai"], C["teal"]),
              ("Compare", ["slt", "sltu", "slti", "sltiu"], C["violet"]),
              ("Loads", ["lb", "lh", "lw", "lbu", "lhu"], C["amber"]),
              ("Stores", ["sb", "sh", "sw"], C["amber"]),
              ("Branches", ["beq", "bne", "blt", "bge", "bltu", "bgeu"], C["rose"]),
              ("Jumps", ["jal", "jalr"], C["rose"]),
              ("System / sync", ["fence", "ecall", "ebreak"], C["slate"])]
    for i, (g, ins, c) in enumerate(groups):
        row, col = divmod(i, 3)
        x = 4 + col * 46
        y = 62 - row * 24
        box(ax, x, y, 42, 20, "", fc=c)
        ax.text(x + 21, y + 16.5, f"{g} ({len(ins)})", ha="center", weight="bold", fontsize=11)
        ax.text(x + 21, y + 7.5, "  ".join(ins[:3]) + ("\n" + "  ".join(ins[3:]) if len(ins) > 3 else ""),
                ha="center", va="center", family="DejaVu Sans Mono", fontsize=10.5)
    ax.text(70, 4, "5+6+6+4+5+3+6+2+3 = 40", ha="center", fontsize=10, color=C["mute"])
    ax.set_xlim(0, 142)
    save(f, "34_rv32i_instruction_set.png")


def d_cpu_datapath():
    f, ax = fig(14, 6.4)
    title(ax, "Fetch -> Decode -> Execute: the single-cycle RV32I view")
    box(ax, 2, 22, 12, 12, "PC", fc=C["violet"], bold=True)
    box(ax, 20, 18, 20, 20, "Instruction\nMemory", fc=C["blue"])
    box(ax, 46, 18, 20, 20, "Register\nFile\n+ Imm Gen", fc=C["violet"])
    box(ax, 72, 18, 16, 20, "ALU", fc=C["amber"], bold=True)
    box(ax, 94, 18, 20, 20, "Data\nMemory", fc=C["blue"])
    box(ax, 120, 18, 16, 20, "Write\nback\n(rd)", fc=C["green"])
    for x1, x2 in [(14, 20), (40, 46), (66, 72), (88, 94), (114, 120)]:
        arrow(ax, x1, 28, x2, 28)
    box(ax, 2, 44, 12, 8, "+4", fc=C["slate"])
    arrow(ax, 8, 34, 8, 44)
    arrow(ax, 14, 48, 140, 48, style="-", color=C["mute"])
    ax.text(70, 50.5, "next PC = PC + 4  (or branch / jump target)", ha="center", fontsize=9, color=C["mute"])
    box(ax, 46, 2, 42, 10, "Control unit: decodes opcode / funct3 / funct7", fc=C["slate"], fs=9.5)
    arrow(ax, 30, 18, 46, 8, color=C["mute"])
    ax.set_xlim(0, 142)
    save(f, "35_cpu_datapath.png")


def d_cpu_mem_io():
    f, ax = fig(13, 7)
    ax.set_xlim(0, 108)
    title(ax, "The 32-bit system: CPU, memory and I/O", "a single line with a slash and '32' means a bus of 32 wires")
    box(ax, 6, 22, 30, 28, "CPU\n(RV32I)", fc=C["violet"], bold=True, fs=13)
    box(ax, 70, 30, 32, 26, "", fc=C["blue"])
    ax.text(86, 52, "Memory", ha="center", weight="bold", fontsize=12)
    rows = [("location 0", "32-bit data"), ("location 1", "32-bit data"), ("...", "..."), ("location 2^32-1", "32-bit data")]
    for i, (a, d) in enumerate(rows):
        ax.add_patch(Rectangle((84, 45 - i * 4.4), 16, 3.8, fc="white", ec=C["mute"]))
        ax.text(83, 46.9 - i * 4.4, a, ha="right", va="center", fontsize=7.5, family="DejaVu Sans Mono")
        ax.text(92, 46.9 - i * 4.4, d, ha="center", va="center", fontsize=7.5)
    def bus(y, label, both=False):
        arrow(ax, 36, y, 70, y, style="<|-|>" if both else "-|>")
        ax.plot([51, 55], [y - 1.6, y + 1.6], color=C["ink"], lw=1.4)
        ax.text(53, y + 2.6, "32", ha="center", fontsize=9, weight="bold")
        ax.text(53, y - 3.2, label, ha="center", fontsize=9, color=C["mute"])
    bus(44, "address bus")
    bus(32, "data bus (read / write)", both=True)
    ax.text(86, 25.5, "2^32 locations: 0 ... 2^32 - 1", ha="center", fontsize=9.5)
    box(ax, 6, 4, 96, 10, "", fc=C["green"])
    ax.text(54, 11.2, "I/O controllers - the link to the real world", ha="center", weight="bold", fontsize=10)
    ax.text(54, 6.6, "keyboard, mouse (input)    screen via HDMI / VGA (output)    USB / USB-C", ha="center", fontsize=9.5)
    arrow(ax, 21, 22, 21, 14, style="<|-|>")
    ax.set_xlim(0, 108)
    save(f, "36_cpu_memory_io.png")


def d_branch():
    f, ax = fig(11, 6.4)
    title(ax, "Conditional branch:  beq / bne / blt / bge / bltu / bgeu  rs1, rs2, label")
    box(ax, 30, 48, 50, 7, "Fetch branch instruction at PC", fc=C["green"], r=1.5)
    box(ax, 30, 36, 50, 7, "Read rs1 and rs2 from the register file", fc=C["blue"])
    box(ax, 30, 22, 50, 9, "Compare rs1 ? rs2\n(==, !=, < signed, >= signed, < unsigned, >= unsigned)", fc=C["amber"], fs=9.5)
    box(ax, 4, 4, 42, 8, "TAKEN:  PC = PC + offset (label)", fc=C["rose"], fs=10)
    box(ax, 64, 4, 42, 8, "NOT taken:  PC = PC + 4", fc=C["slate"], fs=10)
    arrow(ax, 55, 48, 55, 43); arrow(ax, 55, 36, 55, 31)
    arrow(ax, 45, 22, 25, 12, "true", toff=(-3, 1)); arrow(ax, 65, 22, 85, 12, "false", toff=(3, 1))
    ax.set_xlim(0, 110)
    save(f, "11_branch_flow.png")


if __name__ == "__main__":
    d_roadmap(); d_compile_flow(); d_regfile_table(); d_regfile_block(); d_sign_ext(); d_lui_addi()
    d_memory_pc(); d_lw_sw(); d_logic(); d_shifts(); d_endian(); d_function_call(); d_stack()
    d_caller_callee(); d_formats(); d_encodings(); d_imm_scramble("B"); d_imm_scramble("J")
    d_label_offset(); d_soc(); d_memmap(); d_interrupt12(); d_exception(); d_alignment(); d_debug()
    d_isa_overview(); d_cpu_datapath(); d_cpu_mem_io()
    d_branch()
    vflow("12_if_else_flow.png", "if (a == b) x = 1; else x = 2;  ->  assembly",
          [("bne a0, a1, ELSE      # test the OPPOSITE condition", "dec"),
           ("THEN:  li t0, 1", "proc"), ("j END                # skip the else part", "proc"),
           ("ELSE:  li t0, 2", "proc"), ("END:   ...", "end")], w=10)
    vflow("13_loop_flow.png", "for (i = 0; i < n; i++) sum += i;",
          [("li t0, 0  (i)   ;   li a0, 0  (sum)", "start"),
           ("LOOP: bge t0, a1, DONE     # exit when i >= n", "dec"),
           ("add a0, a0, t0             # body", "proc"),
           ("addi t0, t0, 1             # i++", "proc"),
           ("j LOOP                     # back-edge", "proc"),
           ("DONE: ...", "end")], w=10)
    print("diagrams written to", os.path.abspath(OUT))
