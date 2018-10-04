CXX_FLAGS+=--std=c++11 -Wall
BUILD_DIR=build

default: ${BUILD_DIR}/gobgp-analysis

${BUILD_DIR}/gobgp-analysis: build
	${CXX} ${CXX_FLAGS} -o $@ -I./deps/rapidjson/include -I./src src/*.cc cmd/*.cc

gobgp-analysis-test: ${BUILD_DIR}/gobgp-analysis
	./test/gobgp-analysis-test.sh

${BUILD_DIR}/run-test: build
	${CXX} ${CXX_FLAGS} -o $@ -I./src src/*.cc test/*.cc

run-test: ${BUILD_DIR}/run-test
	${BUILD_DIR}/run-test

build:
	mkdir -p ${BUILD_DIR}

clean:
	rm -rf ${BUILD_DIR}
