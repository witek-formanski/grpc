"""Calls SayHello 20 times in sequence, then from 20 threads, and times both."""

from concurrent import futures
import logging
import time

import grpc
import helloworld_pb2
import helloworld_pb2_grpc

CALLS = 20


def run():
    with grpc.insecure_channel("localhost:50051") as channel:
        stub = helloworld_pb2_grpc.GreeterStub(channel)

        def say_hello(i):
            request = helloworld_pb2.HelloRequest(name=f"client {i}")
            return stub.SayHello(request, timeout=60).message

        start = time.perf_counter()
        for i in range(CALLS):
            say_hello(i)
        print(f"Sequential: {time.perf_counter() - start:.1f} s")

        start = time.perf_counter()
        with futures.ThreadPoolExecutor(max_workers=20) as executor:
            list(executor.map(say_hello, range(CALLS)))
        print(f"Parallel (20 threads): {time.perf_counter() - start:.1f} s")


if __name__ == "__main__":
    logging.basicConfig()
    run()
