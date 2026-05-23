/**
 * study/CS50/memory_pointers.c
 * 
 * Runnable reference code demonstrating memory pointers in C.
 * Matches CS50 Week 4 Memory concepts.
 */
#include <stdio.h>

// A helper function to demonstrate passing pointers by reference.
// By taking pointer arguments (int*), we can modify the original variables.
void swap(int *a, int *b) {
    int temp = *a; // Retrieve the value stored at address 'a' and hold it in temp
    *a = *b;       // Copy the value at address 'b' to the address 'a'
    *b = temp;     // Copy the temp value to the address 'b'
}

int main(void) {
    // 1. Basic Variable & Pointer Declaration
    int x = 50;
    int *p = &x; // 'p' stores the address of 'x' (p points to x)

    printf("=== Basic Pointer Operations ===\n");
    printf("Value of x: %d\n", x);
    printf("Address of x (&x): %p\n", (void*)&x);
    printf("Value stored in pointer p: %p\n", (void*)p);
    printf("Address of pointer p itself (&p): %p\n", (void*)&p);
    printf("Dereferenced value (*p): %d\n\n", *p);

    // 2. Modifying values via pointers
    *p = 100; // Overwrite the value at the address stored in p
    printf("=== After Modifying via Pointer (*p = 100) ===\n");
    printf("Value of x is now: %d (changed through pointer)\n\n", x);

    // 3. Pointer Arithmetic & Arrays
    int numbers[] = {10, 20, 30};
    int *arr_ptr = numbers; // An array name decays to a pointer to its first element

    printf("=== Pointer Arithmetic & Arrays ===\n");
    // These two print statements are functionally identical
    printf("First element: %d (via numbers[0])\n", numbers[0]);
    printf("First element: %d (via *arr_ptr)\n", *arr_ptr);
    
    // Move pointer to the next integer (adds sizeof(int) bytes to address)
    arr_ptr++; 
    printf("Second element: %d (via *(arr_ptr + 1) offset)\n", *arr_ptr);
    printf("Third element: %d (via *(numbers + 2) notation)\n\n", *(numbers + 2));

    // 4. Pass-by-Reference Demonstration
    int num1 = 10;
    int num2 = 99;
    printf("=== Pass-by-Reference (swap) ===\n");
    printf("Before swap: num1 = %d, num2 = %d\n", num1, num2);
    swap(&num1, &num2); // Pass addresses of num1 and num2
    printf("After swap:  num1 = %d, num2 = %d\n", num1, num2);

    return 0;
}
