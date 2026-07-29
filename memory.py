from __future__ import annotations
import math
import time
import random
import threading
from dataclasses import dataclass, field, asdict
from typing import List, Optional, Dict, Any

MEMORY_EXPANSION_SNELL = 4096
MARA_REALIGNMENT_FACTOR = 1.6180339887
PHI = 1.6180339887
PI_L = 3.1415926535
CHAIN_LENGTH = 32
LATTICE_SIZE = 1024
HASH_SIZE = 32

# ----------------------------
# Optional DIMFO hooks (stubs)
# ----------------------------
def dimfo_init() -> None:
    pass

def dimfo_apply_to_lattice(lat: "Lattice", worker_id: int, block: "MobiusBlock") -> None:
    # Keep as a hook for future behavior
    return


def snell_memory_allocate(size: int) -> bytearray:
    adjusted_size = math.ceil(size * MARA_REALIGNMENT_FACTOR)
    return bytearray(adjusted_size)


@dataclass
class TGDKHeader:
    prev_hash: bytes = field(default_factory=lambda: bytes(HASH_SIZE))
    mobius_hash: bytes = field(default_factory=lambda: bytes(HASH_SIZE))
    nonce: int = 0
    inverted: int = 0
    block_number: int = 0


@dataclass
class MobiusBlock:
    data: bytearray = field(default_factory=lambda: bytearray(MEMORY_EXPANSION_SNELL))
    hash: bytearray = field(default_factory=lambda: bytearray(HASH_SIZE))
    prev: Optional["MobiusBlock"] = None
    next: Optional["MobiusBlock"] = None
    inverted: int = 0
    real_size: int = 0
    policy_ratio: float = 1.0
    header: TGDKHeader = field(default_factory=TGDKHeader)


@dataclass
class Lattice:
    entry: Optional[MobiusBlock] = None
    blocks: List[MobiusBlock] = field(default_factory=list)
    count: int = 0
    scaling_factor: float = 1.0
    lattice_id: int = 0
    name: str = ""
    status: str = "Ready"


@dataclass
class CorrugationWorker:
    worker_id: int
    pi_theta: float = 1.0
    pi_old: float = 1.0
    advantage: float = 0.0
    is_pi_worker: bool = False


@dataclass
class TGDKMetrics:
    phi_counts: List[int]
    pi_count: int
    chain_count: int
    sealed_events: int
    policy_clip_violations: int


class TGDKRuntime:
    def __init__(self, seed: Optional[int] = None):
        self.random = random.Random(seed if seed is not None else int(time.time()))
        self.memory_lock = threading.Lock()

        self.phi_lattice = [
            Lattice(scaling_factor=PHI, lattice_id=i, name=f"phi-{i}", status="Ready")
            for i in range(3)
        ]
        self.pi_lattice = [
            Lattice(scaling_factor=PI_L, lattice_id=3, name="pi-0", status="Ready")
        ]

        self.global_chain: List[MobiusBlock] = []
        self.sealed_events = 0
        self.policy_clip_violations = 0

    # ---------- Core logic ----------
    def hash_block(self, prev: Optional[MobiusBlock], curr: MobiusBlock) -> None:
        # FNV-1a style over prev hash + first 256 bytes
        h = 1469598103934665603
        if prev is not None:
            for b in prev.hash:
                h ^= b
                h *= 1099511628211
                h &= 0xFFFFFFFFFFFFFFFF  # constrain to 64-bit

        for i in range(256):
            h ^= curr.data[i]
            h *= 1099511628211
            h &= 0xFFFFFFFFFFFFFFFF

        # zero then copy h + real_size into first 16 bytes
        curr.hash[:] = b"\x00" * HASH_SIZE
        h_bytes = h.to_bytes(8, "little", signed=False)
        rs_bytes = int(curr.real_size).to_bytes(8, "little", signed=False)
        curr.hash[0:8] = h_bytes
        curr.hash[8:16] = rs_bytes

        if prev is not None:
            curr.header.prev_hash = bytes(prev.hash)
        curr.header.block_number = len(self.global_chain)

    def tgdk_seal(self, head: MobiusBlock, tail: MobiusBlock) -> None:
        # Seal on every 8th index after first window
        if len(self.global_chain) % 8 == 0 and len(self.global_chain) > 0:
            tail.inverted = 1
            tail.header.inverted = 1
            tail.header.nonce = self.random.getrandbits(64)

            mobius = bytearray(HASH_SIZE)
            for i in range(HASH_SIZE):
                mobius[i] = (
                    head.data[i % MEMORY_EXPANSION_SNELL]
                    ^ tail.data[i % MEMORY_EXPANSION_SNELL]
                    ^ tail.hash[i]
                )
            tail.header.mobius_hash = bytes(mobius)
            self.sealed_events += 1

    def _create_block(self, clipped_ratio: float) -> MobiusBlock:
        b = MobiusBlock()
        _ = snell_memory_allocate(MEMORY_EXPANSION_SNELL)  # preserves intent from C
        b.real_size = int(MEMORY_EXPANSION_SNELL * MARA_REALIGNMENT_FACTOR)
        b.policy_ratio = clipped_ratio
        for i in range(MEMORY_EXPANSION_SNELL):
            b.data[i] = self.random.randint(0, 255)
        return b

    def _append_chain_block(self, b: MobiusBlock) -> None:
        if self.global_chain:
            prev = self.global_chain[-1]
            self.hash_block(prev, b)
            prev.next = b
            b.prev = prev
        else:
            self.hash_block(None, b)

        if len(self.global_chain) < CHAIN_LENGTH:
            self.global_chain.append(b)
            self.tgdk_seal(self.global_chain[0], b)

    def duo_corrugation_task(self, worker: CorrugationWorker, iterations: int = 20, sleep_enabled: bool = False) -> None:
        for iter_idx in range(iterations):
            worker.pi_theta = 0.8 + self.random.random() * 0.4
            ratio = worker.pi_theta / worker.pi_old if worker.pi_old != 0 else 1.0
            clipped = max(0.8, min(1.2, ratio))

            if clipped < 0.8 or clipped > 1.2:
                self.policy_clip_violations += 1

            with self.memory_lock:
                b = self._create_block(clipped)
                self._append_chain_block(b)

                if not worker.is_pi_worker:
                    lid = worker.worker_id
                    lat = self.phi_lattice[lid]
                    if lat.count < LATTICE_SIZE:
                        lat.status = "Corrugating"
                        lat.blocks.append(b)
                        lat.count += 1
                        b.real_size = int(b.real_size * PHI)

                        # mirror first 128 bytes with tail region
                        for i in range(128):
                            j = MEMORY_EXPANSION_SNELL - 1 - i
                            b.data[i], b.data[j] = b.data[j], b.data[i]
                else:
                    lat = self.pi_lattice[0]
                    dimfo_apply_to_lattice(lat, worker.worker_id, b)
                    if lat.count < LATTICE_SIZE:
                        lat.status = "Corrugating"
                        lat.blocks.append(b)
                        lat.count += 1
                        angle = 2 * PI_L * iter_idx / float(iterationsi == 3))
            for i in range(worker_count)
        ]

        threads = []
        for w in workers:
            t = threading.Thread(target=self.duo_corrugation_task, args=(w, iterations, sleep_enabled), daemon=False)
            threads.append(t)
            t.start()

        for t in threads:
            t.join()

        # Mark lattices sealed at completion
        for lat in self.phi_lattice:
            lat.status = "Sealed"
        self.pi_lattice[0].status = "Sealed"

        return TGDKMetrics(
            phi_counts=[lat.count for lat in self.phi_l).__name__}: {e}",
            duration_ms=now_ms() - start,
        )
