# Day 18 — Arrays, ASCII Characters, Load/Store Bytes and Half-Words

> **Course:** Week 4, Video 3 &nbsp;|&nbsp; **Playlist #18** &nbsp;|&nbsp; [Chip Design with Rashid — RISC-V Architecture Explained](https://www.youtube.com/playlist?list=PL0-xus8sJBCRzZtmL_fLWaohRKuc4j5aH)  
> **Notes source:** video topic + Rashid's weekly notes + standard RV32I material

## All load/store sizes

| Instruction | Size | Extension to 32 bits | Format |
|---|---|---|---|
| `lb rd, off(rs1)` | byte | **sign**-extend | I |
| `lbu rd, off(rs1)` | byte | **zero**-extend | I |
| `lh rd, off(rs1)` | half (16 b) | sign-extend | I |
| `lhu rd, off(rs1)` | half | zero-extend | I |
| `lw rd, off(rs1)` | word | — | I |
| `sb rs2, off(rs1)` | stores low 8 bits | — | S |
| `sh rs2, off(rs1)` | stores low 16 bits | — | S |
| `sw rs2, off(rs1)` | stores 32 bits | — | S |

There is no `sbu`/`shu` — stores just write the low bits, so sign does not matter.

```
memory byte = 0xF0
lb  → 0xFFFFFFF0  (-16)
lbu → 0x000000F0  (240)
```

## Little-endian

![Little endian](../diagrams/14_little_endian.png)

RISC-V stores the **least significant byte at the lowest address**.

## Array element addresses

| Element type | Size | Address of `A[i]` |
|---|---|---|
| `char` | 1 | `base + i` |
| `short` | 2 | `base + 2i` |
| `int` | 4 | `base + 4i` |

## ASCII characters

A `char` is a 1-byte code. Useful values:

| Char | Hex | Dec |
|---|---|---|
| `'\0'` (string end) | 0x00 | 0 |
| `'0'` … `'9'` | 0x30 … 0x39 | 48 … 57 |
| `'A'` … `'Z'` | 0x41 … 0x5A | 65 … 90 |
| `'a'` … `'z'` | 0x61 … 0x7A | 97 … 122 |
| space | 0x20 | 32 |

Upper ↔ lower case differ only in **bit 5** (0x20). Digit value = `char − '0'`.

## Example — string length (`strlen`)

```asm
# a0 = address of string; returns length in a0
strlen: mv   t0, a0            # t0 = pointer
LOOP:   lbu  t1, 0(t0)         # load one character
        beqz t1, DONE          # stop at '\0'
        addi t0, t0, 1         # next byte (char = 1 byte)
        j    LOOP
DONE:   sub  a0, t0, a0        # length = end - start
        ret
```

## Example — convert a string to upper case

```asm
# a0 = address of string
toupper:
LOOP:   lbu  t1, 0(a0)
        beqz t1, DONE
        li   t2, 'a'
        blt  t1, t2, NEXT      # below 'a' → not lowercase
        li   t2, 'z'
        bgt  t1, t2, NEXT      # above 'z' → not lowercase
        addi t1, t1, -32       # 'a' - 'A' = 32 (or: andi t1, t1, 0xDF)
        sb   t1, 0(a0)
NEXT:   addi a0, a0, 1
        j    LOOP
DONE:   ret
```

## Example — sum of an int array

```asm
# a0 = &A[0], a1 = n ; returns sum in a0
sum_array:
        li   t0, 0             # sum
        li   t1, 0             # i
L:      bge  t1, a1, E
        slli t2, t1, 2         # i*4
        add  t2, a0, t2        # &A[i]
        lw   t3, 0(t2)
        add  t0, t0, t3
        addi t1, t1, 1
        j    L
E:      mv   a0, t0
        ret
```

(A faster version increments a pointer by 4 instead of recomputing `i*4`.)

<!-- rashid-notes -->
## 📒 From Rashid's Week 4 notes

> Extra points and worked examples from Rashid's members-only weekly notes ([RISCV_Arch folder](https://drive.google.com/drive/folders/1sIX-rAanGWWkZocAbXNmvW80JbdAEg6P), members only). Written here in my own words; most of his examples come from the reference book *Digital Design and Computer Architecture, RISC-V Edition* (Harris & Harris), chapters 6–7.

**Arrays** = "store the contents at **sequential addresses** in memory" — they keep the data together. In his memory picture `scores[0]` is word 0 (address 0x0), `scores[1]` is at 0x4, `scores[2]` at 0x8 …

**Code Example 6.21 — `scores[i] = scores[i] + 10` for 200 entries** (s0 = base address, s1 = i):

```asm
      addi s1, zero, 0      # i = 0
      addi t2, zero, 200    # t2 = 200
for:  bge  s1, t2, done     # i >= 200? exit
      slli t0, s1, 2        # t0 = i * 4   (byte offset)
      add  t0, t0, s0       # address of scores[i] = base + i*4
      lw   t1, 0(t0)        # t1 = scores[i]
      addi t1, t1, 10
      sw   t1, 0(t0)        # scores[i] = t1
      addi s1, s1, 1        # i++
      j    for
done:
```

**ASCII** = American Standard Code for Information Interchange, an **8-bit** code. Printable characters run 0x20 … 0x7E → **95** of them ('A' = 0x41, 'a' = 0x61 — lowercase is uppercase + 32).

**Byte loads/stores** (book Figure 6.5, memory word = `F7 8C 42 03`, s4 points to it):

| Instruction | Result |
|---|---|
| `lbu s1, 2(s4)` | s1 = **0x0000008C** (zero-extended) |
| `lb  s2, 3(s4)` | s2 = **0xFFFFFFF7** (sign-extended: F7 has its top bit set) |
| `sb  s3, 1(s4)` | stores the **low byte** of s3 (0x9B) into byte 1 |

**Strings** end with a **null byte 0x00** — "Hello!" is `48 65 6C 6C 6F 21 00` (7 bytes).

**Example 6.2 — make a 10-char array upper-case** (subtract 32 from each char; s0 = base, s1 = i):

```asm
      addi s1, zero, 0
      addi t0, zero, 10
for:  bge  s1, t0, done
      add  t1, s1, s0       # address = base + i   (bytes, so NO *4)
      lbu  s2, 0(t1)
      addi s2, s2, -32
      sb   s2, 0(t1)
      addi s1, s1, 1
      j    for
done:
```

**Half-words:** `lh` (load half, sign-extended), `lhu` (zero-extended), `sh` (store half) — 16 bits.

---
[⬅ Day 17](../Day-17-Loops/README.md) | [Index](../README.md) | [Day 19 ➡](../Day-19-Week-4-Recap/README.md)
