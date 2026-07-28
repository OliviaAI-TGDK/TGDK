#define PHI 1.6180339887 // your MARA_REALIGNMENT_FACTOR
#define PI 3.1415926535

// 3 phi lattices = Fibonacci scaled, self-similar, expand forever
// 1 pi lattice = circular, wraps, holds the seal

typedef struct {
    mobius_block_t* blocks[1024];
    double scaling_factor; // PHI or PI
    int lattice_id;
} lattice_t;

lattice_t phi_lattice[3]; // 0,1,2 = PHI
lattice_t pi_lattice[1]; // 3 = PI
