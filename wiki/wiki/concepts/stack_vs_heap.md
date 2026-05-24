---
title: "Concept: Memory Allocation (Stack vs Heap)"
category: "concept"
tags: [memory-management, cpp, stack, heap]
sources: [ "[cpp_oop_basics.txt](file:///E:/AIOS/AIS-OS/wiki/raw/cpp_oop_basics.txt)" ]
last_updated: 2026-05-23
---

# Memory Allocation: Stack vs Heap

In systems programming languages like [C++](file:///E:/AIOS/AIS-OS/wiki/wiki/entities/cpp_language.md), memory for objects can be allocated in two primary regions: the **Stack** and the **Heap**.

## Stack Allocation
Stack allocation is the default allocation method when declaring variables inside functions.
- **Syntax**: `Box myBox;`
- **Lifecycle**: Managed automatically. The block of memory is pushed onto the stack frame when entered and popped off (deallocated) when the scope ends.
- **Speed**: Very fast, as allocation is just moving the stack pointer.
- **Size**: Typically limited stack size, which can lead to stack overflow if overly large objects or deep recursion is used.

## Heap Allocation
Heap allocation is used when object lifecycles need to persist beyond the scope of their creation, or when sizes are dynamic.
- **Syntax**: `Box* myBox = new Box();`
- **Lifecycle**: Managed manually. The developer must call `delete` to free the allocated memory. Failure to do so leads to **memory leaks**.
- **Speed**: Slower than stack allocation because it requires finding a block of free memory on the heap.
- **Size**: Scalable and limited only by available system memory.

---
*Derived from:* [Source: C++ OOP & Memory Basics](file:///E:/AIOS/AIS-OS/wiki/wiki/sources/cpp_oop_basics.md)
