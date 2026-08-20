package fuzz

import "testing"

func FuzzHCLParse(f *testing.F) {
	f.Add([]byte(`variable "x" { type = string }`))
	f.Add([]byte(`resource "aws_s3_bucket" "b" { bucket = "test" }`))

	f.Fuzz(func(t *testing.T, data []byte) {
		if len(data) > 1<<20 { // 1MB
			return
		}
		ParseHCL(data)
	})
}
