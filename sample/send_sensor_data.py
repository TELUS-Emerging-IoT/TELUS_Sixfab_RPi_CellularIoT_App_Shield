# -------------------------------------------------------------------------
# Copyright (c) Microsoft Corporation. All rights reserved.
# Licensed under the MIT License. See License.txt in the project root for
# license information.
# --------------------------------------------------------------------------

import os
import asyncio
import uuid
import time
from cellulariot import cellulariot
from azure.iot.device.aio import IoTHubDeviceClient
from azure.iot.device import Message

async def main():
    # The connection string for a device should never be stored in code. For the sake of simplicity we're using an environment variable here.
    conn_str = os.getenv("IOTHUB_DEVICE_CONNECTION_STRING")

    # The client object is used to interact with your Azure IoT hub.
    device_client = IoTHubDeviceClient.create_from_connection_string(conn_str)

    # Connect the client.
    await device_client.connect()

    node = cellulariot.CellularIoTApp()
    node.setupGPIO()

    node.disable()
    time.sleep(1)
    node.enable()

    async def sensor_data():
        msg = Message("Acceleration: "+str(node.readAccel())+"; "+"Humidity: " + str(node.readHum())+"; "+"Temperature: " + str(node.readTemp())+"; "+"Lux: " + str(node.readLux())+"; "+"ADC1: " + str(node.readAdc(0))+"; "+"ADC2: " + str(node.readAdc(1))+"; "+"ADC3: " + str(node.readAdc(2))+"; "+"ADC4: " + str(node.readAdc(3)))
        msg.message_id = uuid.uuid4()
        msg.correlation_id = "correlation-1234"
        await device_client.send_message(msg)
    
    count = 0
    while(True):
        await sensor_data()
        print("#"+str(count)+" sent data")
        count = count+1
        time.sleep(1)

    # finally, disconnect
    # await device_client.disconnect()

if __name__ == "__main__":
    asyncio.run(main())

    # If using Python 3.6 or below, use the following code instead of asyncio.run(main()):
    # loop = asyncio.get_event_loop()
    # loop.run_until_complete(main())
    # loop.close()

