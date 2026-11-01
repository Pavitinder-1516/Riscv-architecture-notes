# Day 36 — 12-Step Interrupt Action Flow - Part 2/2

> **Course:** Week 8, Video 3 &nbsp;|&nbsp; **Playlist #36** &nbsp;|&nbsp; [Chip Design with Rashid — RISC-V Architecture Explained](https://www.youtube.com/playlist?list=PL0-xus8sJBCRzZtmL_fLWaohRKuc4j5aH)  
> **Notes source:** video topic + standard RV32I material (to be updated from the transcript)

![12 step interrupt flow](../diagrams/30_interrupt_12_steps.png)

**Part 2 — the software handler and the return (steps 9–12)**

9. **Prologue** — the Interrupt Service Routine (ISR) saves every register it will use (the interrupted code did not expect them to change!) on the stack.
10. **Service the device** — read `mcause` to find the source (and for external interrupts, *claim* the ID from the PLIC), do the work (read the UART byte, toggle the LED, re-arm the timer…) and **clear the interrupt source** — otherwise it is still pending and fires again immediately.
11. **Epilogue** — restore the saved registers, free the stack space.
12. **`mret`** — hardware does: `PC ← mepc`, `MIE ← MPIE`, privilege ← `MPP`. The interrupted program continues exactly where it stopped, unaware anything happened.

## Code — setting up and handling a timer interrupt

```asm
.equ MTIMECMP, 0x02004000      # CLINT addresses (SiFive / QEMU 'virt' convention)
.equ MTIME,    0x0200BFF8

init:
    la    t0, trap_handler
    csrw  mtvec, t0            # direct mode (low 2 bits = 0, handler 4-byte aligned)
    jal   ra, set_next_tick    # program the first timer compare
    li    t0, (1 << 7)
    csrs  mie, t0              # enable machine timer interrupt (MTIE)
    csrsi mstatus, (1 << 3)    # global enable (MIE)
main_loop:
    wfi                        # sleep until an interrupt
    j     main_loop

set_next_tick:                 # mtimecmp = mtime + 1,000,000
    li    t0, MTIME
    lw    t1, 0(t0)
    li    t2, 1000000
    add   t1, t1, t2
    li    t0, MTIMECMP
    sw    t1, 0(t0)            # (64-bit registers simplified to low word here)
    ret

.align 2
trap_handler:
    addi  sp, sp, -16          # step 9: save what we use
    sw    ra, 12(sp)
    sw    t0,  8(sp)
    sw    t1,  4(sp)
    sw    t2,  0(sp)

    csrr  t0, mcause           # step 10: which trap?
    bgez  t0, not_interrupt    # bit 31 = 0 → exception (Week 9)
    jal   ra, set_next_tick    # writing mtimecmp clears the timer interrupt
    # ... toggle an LED, count ticks, etc. ...
not_interrupt:
    lw    t2,  0(sp)           # step 11: restore
    lw    t1,  4(sp)
    lw    t0,  8(sp)
    lw    ra, 12(sp)
    addi  sp, sp, 16
    mret                       # step 12: return
```

## Interrupt latency

The time from the event (step 1) to the first useful instruction of the handler (step 10). It includes finishing the current instruction, the pipeline flush, and the register saving in the prologue. *Vectored* mode cuts latency because the handler doesn't have to decode `mcause` first.

---

## Week 8 Key Takeaways

- Peripherals hang off the system bus; the CPU reaches them with ordinary `lw`/`sw` at **memory-mapped addresses**.
- Use read-modify-write and `volatile`; MMIO has side effects and must not be cached.
- Polling = simple but wastes CPU; interrupts = efficient but need CSRs and a handler.
- **Interrupt flow:** event → `mip` → enabled? → finish instr → `mepc`, `mcause`, `mstatus` → `PC = mtvec` → save → service + clear → restore → `mret`.

## Practice Questions

1. Why doesn't RISC-V need `in`/`out` instructions?
2. Write code to toggle bit 0 of a GPIO output register at `0x10012000`.
3. An interrupt is pending in `mip` but nothing happens. Name two possible reasons.
4. What would happen if the ISR forgot to clear the interrupt source?
5. What three things does `mret` do?

<details><summary>Answers</summary>

1. Peripheral registers are mapped into the memory address space; `lw`/`sw` reach them.
2. `li t0, 0x10012000` ; `lw t1, 0(t0)` ; `xori t1, t1, 1` ; `sw t1, 0(t0)`.
3. The source is disabled in `mie`, or `mstatus.MIE = 0` (e.g. we are already inside a handler).
4. After `mret` the interrupt is still pending → the CPU immediately traps again → infinite loop of interrupts.
5. `PC ← mepc`, `mstatus.MIE ← MPIE`, privilege ← `MPP`.
</details>

---
[⬅ Day 35](../Day-35-Interrupt-Flow-Part-1/README.md) | [Index](../README.md) | [Day 37 ➡](../Day-37-CPU-Exceptions/README.md)
