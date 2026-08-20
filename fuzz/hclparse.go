package fuzz

import "github.com/hashicorp/hcl/v2/hclparse"

func ParseHCL(data []byte) {
	p := hclparse.NewParser()
	_, _ = p.ParseHCL(data, "fuzz.tf")
}
