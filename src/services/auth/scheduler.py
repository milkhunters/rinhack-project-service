import logging

import grpc
from src.protos.ums_control import ums_control_pb2
from src.protos.ums_control import ums_control_pb2_grpc


async def update_reauth_list(app, config, ums_grps_addr: tuple[str, int]):
    app.state.reauth_session_dict = dict()

    try:

        async with grpc.aio.insecure_channel(f"{ums_grps_addr[0]}:{ums_grps_addr[1]}") as channel:
            stub = ums_control_pb2_grpc.UserManagementStub(channel)
            response = await stub.GetListOfReauth(ums_control_pb2.GetListRequest())

        app.state.reauth_session_dict = {d.key: d.value for d in response.dicts}

    except grpc.RpcError as e:
        logging.error(f"Error: {e}")
