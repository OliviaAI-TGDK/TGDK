#include <stdint.h>

#define CHAIN_LENGTH 8 // must be even for mobius twist

typedef struct mobius_block {
    uint8_t data[MEMORY_EXPANSION_SNELL];
    uint8_t hash[32]; // keccak256 like Geth
    struct mobius_block *prev;
    struct mobius_block *next;
    int inverted; // 0 = normal, 1 = mobius flipped
    size_t real_size;
} mobius_block_t;

typedef struct {
    mobius_block_t *entry; // head of the strip
    pthread_mutex_t lock;
    int count;
} mobius_chain_t;

mobius_chain_t g_chain;

// Simple keccak placeholder - swap for real keccak256 from libkeccak
void hash_block(mobius_block_t *prev, mobius_block_t *curr) {
    // in Geth: Keccak256(prev.hash + curr.data)
    // for tonight, use a fast hash. Replace with real keccak later
    uint64_t h = 1469598103934665603ULL;
    for(int i=0;i<32 && prev;i++) h ^= prev->hash[i];
    for(int i=0;i<MEMORY_EXPANSION_SNELL;i++) h ^= curr->data[i];
    memset(curr->hash, 0, 32);
    memcpy(curr->hash, &h, sizeof(h));
}

mobius_block_t* snell_mobius_allocate() {
    pthread_mutex_lock(&g_chain.lock);

    mobius_block_t *b = snell_memory_allocate(sizeof(mobius_block_t));
    b->real_size = MEMORY_EXPANSION_SNELL * MARA_REALIGNMENT_FACTOR;
    b->inverted = 0;

    if(g_chain.entry == NULL) {
        g_chain.entry = b;
        b->prev = b;
        b->next = b;
    } else {
        // sew into the knot
        mobius_block_t *tail = g_chain.entry->prev;
        b->prev = tail;
        b->next = g_chain.entry;
        tail->next = b;
        g_chain.entry->prev = b;
        hash_block(tail, b);
    }

    g_chain.count++;

    // MOBIUS FOLD: when we complete a loop, flip the read direction
    if(g_chain.count == CHAIN_LENGTH) {
        g_chain.entry->prev->inverted = 1; // the twist in the strip
        g_chain.entry->prev->next = g_chain.entry; // it folds through itself
        printf("[MOBIUS] Chain folded, knot sealed. Count=%d\n", g_chain.count);
    }

    pthread_mutex_unlock(&g_chain.lock);
    return b;
}
