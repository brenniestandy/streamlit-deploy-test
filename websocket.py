import websockets
import pandas as pd
import json

async def fetch():
    uri = "ws://localhost:8765"

    data_compilation = []
    async with websockets.connect(uri) as ws_types:
        cut_off = 0
        print("Connected to server.")

        # Fetch account holder type
        await ws_types.send("holder_type")

        while cut_off != 10:
            try:
                data = await ws_types.recv()
                df_json = json.loads(data)
                df = pd.read_json(df_json, orient="split")
                data_compilation.append(df)
                cut_off += 1

            except websockets.exceptions.ConnectionClosedError:
                print("Connection closed by server.")
                break

    async with websockets.connect(uri) as ws_classifications:
        cut_off = 0
        await ws_classifications.send("classification")

        while cut_off != 100:
            try:
                data = await ws_classifications.recv()
                df_json = json.loads(data)
                df = pd.read_json(df_json, orient="split")
                data_compilation.append(df)
                cut_off += 1

            except websockets.exceptions.ConnectionClosedError:
                print("Connection closed by server.")
                break

    async with websockets.connect(uri) as ws_mediatypes:
        cut_off = 0
        await ws_mediatypes.send("media_types")

        while cut_off != 100:
            try:
                data = await ws_mediatypes.recv()
                df_json = json.loads(data)
                df = pd.read_json(df_json, orient="split")
                data_compilation.append(df)
                cut_off += 1

            except websockets.exceptions.ConnectionClosedError:
                print("Connection closed by server.")
                break

    async with websockets.connect(uri) as ws_mediatypes:
        cut_off = 0
        await ws_mediatypes.send("expiration")

        while cut_off != 100:
            try:
                data = await ws_mediatypes.recv()
                df_json = json.loads(data)
                df = pd.read_json(df_json, orient="split")
                data_compilation.append(df)
                cut_off += 1

            except websockets.exceptions.ConnectionClosedError:
                print("Connection closed by server.")
                break

    result_data = pd.concat(data_compilation)
    return result_data
# asyncio.get_event_loop().run_until_complete(fetch_data())
# loop = asyncio.new_event_loop()
# asyncio.set_event_loop(loop)
# asyncio.get_event_loop().run_until_complete(fetch())
