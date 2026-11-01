# Day 40 — Complete Course Overview and Roadmap

> **Course:** Week 9, Overview &nbsp;|&nbsp; **Playlist #40** &nbsp;|&nbsp; [Chip Design with Rashid — RISC-V Architecture Explained](https://www.youtube.com/playlist?list=PL0-xus8sJBCRzZtmL_fLWaohRKuc4j5aH)  
> **Notes source:** video topic + standard RV32I material (to be updated from the transcript)

![Course roadmap](../diagrams/01_course_roadmap.png)

## Everything in one picture

| Layer | What you learnt | Weeks |
|---|---|---|
| **Programmer's model** | 32 registers, PC, byte-addressable memory, RV32I's 40 instructions | 1–2 |
| **Assembly programming** | arithmetic, constants, load/store, logic, shifts, branches, loops, arrays, strings, functions, stack, calling convention, pseudo-instructions | 2–5 |
| **Machine code** | R/I/S/B/U/J formats, opcode/funct fields, immediates, label offsets | 6–7 |
| **System / SoC** | peripherals, bus, memory-mapped I/O, interrupts, CSRs, exceptions, directives, alignment, on-chip debug | 8–9 |

## Where to go next (digital IC design path)

1. **Write a single-cycle RV32I core in Verilog/SystemVerilog** — PC, register file, immediate generator, ALU, control unit, data memory. Run the programs from this course on it.
2. **Verify** it: self-checking testbench, compare against Spike, run `riscv-tests` / `riscv-arch-test`.
3. **Pipeline** it (5 stages: IF, ID, EX, MEM, WB) — handle data hazards (forwarding, stalls) and control hazards (branch flush / prediction).
4. **Add extensions**: M (multiply/divide), Zicsr + interrupts, C (compressed).
5. **Build the SoC**: bus (Wishbone/AXI-Lite/APB), GPIO, UART, timer, PLIC; boot ROM; run C code.
6. **Implement**: FPGA prototype, then the open-source ASIC flow — Yosys (synthesis), OpenROAD/OpenLane (place & route), Magic/KLayout, on an open PDK such as SkyWater 130 nm.

---

## Week 9 Key Takeaways

- Exceptions are synchronous traps caused by the instruction; same CSR mechanism as interrupts; `mepc` = faulting instruction; skip `ecall` with `mepc += 4`.
- Directives (`.text .data .word .asciz .align .globl .equ`) instruct the assembler, not the CPU.
- Naturally aligned = address is a multiple of the size; words need address bits `[1:0] = 00`.
- Debug path: GDB ⇄ OpenOCD ⇄ JTAG ⇄ DTM/Debug Module ⇄ hart (halt, step, read/write, breakpoints).

## Practice Questions

1. What is in `mcause` and `mepc` after `lw t0, 2(x0)` faults on a core without misaligned support?
2. Why must an `ecall` handler add 4 to `mepc`?
3. `.data` starts at `0x2000`: `a: .byte 1`, `b: .half 2`, `c: .word 3` with no alignment directives. At what addresses are `b` and `c`? Which are misaligned?
4. What is the difference between `.align 2` and `.balign 2`?
5. Name the four mandatory JTAG signals and the job of OpenOCD.

<details><summary>Answers</summary>

1. `mcause = 4` (load address misaligned), `mepc` = address of that `lw`, `mtval = 0x2`.
2. `mepc` points at the `ecall` itself; without +4 `mret` would execute `ecall` again forever.
3. `b` at `0x2001` (misaligned half), `c` at `0x2003` (misaligned word).
4. In RISC-V GNU as, `.align 2` aligns to 2² = 4 bytes; `.balign 2` aligns to 2 bytes.
5. TCK, TMS, TDI, TDO. OpenOCD is the GDB server that converts GDB commands into JTAG / RISC-V debug-module operations.
</details>

---
[⬅ Day 39](../Day-39-Debug-GDB-OpenOCD-JTAG/README.md) | [Index](../README.md)
