FROM gcr.io/oss-fuzz-base/base-builder-go:v1@sha256:493822179f0e9e79bac385b155b2b1253844ee74fbe5f16c43d0e41851cbcc6f


# Copy your repo into the container.
COPY . $SRC/terraform-aws-observability-pro
WORKDIR $SRC/terraform-aws-observability-pro

# build.sh is executed by OSS-Fuzz/ClusterFuzzLite tooling.
COPY .clusterfuzzlite/build.sh $SRC/build.sh
