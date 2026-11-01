# Day 19 — Week 4 Recap - If-Else, Case, For, While, Arrays, Function

> **Course:** Week 4, Recap &nbsp;|&nbsp; **Playlist #19** &nbsp;|&nbsp; [Chip Design with Rashid — RISC-V Architecture Explained](https://www.youtube.com/playlist?list=PL0-xus8sJBCRzZtmL_fLWaohRKuc4j5aH)  
> **Notes source:** video topic + standard RV32I material (to be updated from the transcript)

| C construct | Assembly pattern |
|---|---|
| `if` | branch on opposite condition over the then-block |
| `if-else` | opposite branch to ELSE + `j END` at end of then-block |
| `switch` | compare chain or jump table + `jr` |
| `for` / `while` | test at top + `j` back, or test at bottom (do-while) |
| array `A[i]` | `base + i × size`, `slli` for the multiply |
| string | `lbu` until `'\0'` |
| function | args `a0–a7`, `jal ra`, result `a0`, `ret` |

---
[⬅ Day 18](../Day-18-Arrays-ASCII-Bytes-Halfwords/README.md) | [Index](../README.md) | [Day 20 ➡](../Day-20-Stack-Backup-Registers/README.md)
