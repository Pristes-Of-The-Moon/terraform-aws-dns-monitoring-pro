package fuzz

import "github.com/hashicorp/hcl/v2/hclparse"

// Fuzz target for ClusterFuzzLite/OSS-Fuzz go tooling.
// It expects a byte stream and returns an int.
func FuzzHCLParseCFLite(data []byte) int {
	// Avoid pathological memory usage.
	if len(data) > 1<<20 {
		return -1
	}

	p := hclparse.NewParser()
	// Use a dummy filename; parser only needs bytes + name.
	_, _ = p.ParseHCL(data, "input.hcl")
	return 0
}
