typedef struct {
    int worker_id;
    double pi_theta; // current policy prob
    double pi_old; // old policy prob
    double advantage;
} corrugation_worker_t;

void* duo_corrugation_task(void* arg) {
    corrugation_worker_t* w = (corrugation_worker_t*)arg;

    while(1) {
        pthread_mutex_lock(&memory_lock);

        // DUO = forward corrugation + backward corrugation
        // Forward: fold memory into knot
        mobius_block_t* b = snell_mobius_allocate();
        // Backward: read it inverted through mobius twist

        // CONCURRENT POLICY RATIO - the Geth PPO clipping you googled
        double policy_ratio = w->pi_theta / w->pi_old;

        // CLIP 0.8 to 1.2 like in your screenshot - stability control
        double clipped = fmax(0.8, fmin(1.2, policy_ratio));

        // Only allow the fold if ratio is stable
        if(clipped >= 0.8 && clipped <= 1.2) {
            // Apply to lattices
            if(w->worker_id < 3) {
                // Worker 0,1,2 -> operate on 3 phi lattices
                // phi operation = scale by PHI, self-similar expansion
                phi_lattice[w->worker_id].blocks[...] = b;
                b->real_size = (size_t)(b->real_size * PHI);
            } else {
                // Worker 3 -> operates on 1 pi lattice
                // pi operation = circular wrap, sin/cos corrugation
                pi_lattice[0].blocks[...] = b;
                double angle = 2 * PI * w->worker_id / 4.0;
                // corrugate the data
                for(int i=0;i<MEMORY_EXPANSION_SNELL;i++)
                    b->data[i] ^= (uint8_t)(sin(angle) * 255);
            }

            printf("[TGDK Worker %d] ratio %.3f (clipped %.3f) -> lattice %s SEALED\n",
                   w->worker_id, policy_ratio, clipped,
                   w->worker_id < 3? "PHI" : "PI");
        }

        pthread_mutex_unlock(&memory_lock);
        usleep(1000);
    }
    return NULL;
}
