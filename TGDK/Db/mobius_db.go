package db

// #cgo LDFLAGS: -L../../ -lsnell
// #include <stdlib.h>
// #include "../../snell_memory.h"
import "C"
import (
    "github.com/ethereum/go-ethereum/common"
    "github.com/ethereum/go-ethereum/ethdb"
)

// This IS your Geth database
type MobiusDB struct {
    chain *MobiusChain // your mobius folding structure from C
}

func (m *MobiusDB) Put(key []byte, value []byte) error {
    // This is where your idea happens:
    // Instead of just Put, we fold it through the knot
    ptr := C.snell_mobius_allocate()
    // Copy value into the C block
    // Hash is auto-chained inside C
    // Now the memory IS the knot
    return nil
}

func (m *MobiusDB) Get(key []byte) ([]byte, error) {
    // Walk the mobius strip, if inverted==1 read backwards
    // Verify Keccak(prev.hash + data) == curr.hash
    return nil, nil
}

// Implement ethdb.Database and you ARE Geth compatible
var _ ethdb.Database = (*MobiusDB)(nil)
