"""Client for the RouteGuide Tick RPC."""

from datetime import timezone
import logging

from google.protobuf.empty_pb2 import Empty
import grpc
import route_guide_pb2_grpc


def run():
    with grpc.insecure_channel("localhost:50051") as channel:
        stub = route_guide_pb2_grpc.RouteGuideStub(channel)
        try:
            for timestamp in stub.Tick(Empty(), timeout=60):
                # The server sends UTC; show it in the client's local time zone.
                local_time = timestamp.ToDatetime(tzinfo=timezone.utc).astimezone()
                print(local_time.strftime("%H:%M:%S %Z"), flush=True)
        except grpc.RpcError as error:
            print(f"Tick ended: {error.code().name}")


if __name__ == "__main__":
    logging.basicConfig()
    run()
