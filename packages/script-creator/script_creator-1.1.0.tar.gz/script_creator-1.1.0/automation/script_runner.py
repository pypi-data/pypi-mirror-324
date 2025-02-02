# your_app/script_runner.py
import asyncio
from channels.layers import get_channel_layer

async def run_script(session_id, script_path):
    """
    Runs a Python script and streams output to a WebSocket group.
    """
    channel_layer = get_channel_layer()
    group_name = f"session_{session_id}"

    process = await asyncio.create_subprocess_exec(
        'python', script_path,
        stdout=asyncio.subprocess.PIPE,
        stderr=asyncio.subprocess.PIPE
    )
    print(process)
    print('python' , script_path)
    while True:
        line = await process.stdout.readline()
        if not line:
            break
        # Send real-time data to the WebSocket group
        await channel_layer.group_send(
            group_name,
            {
                "type": "send_session_data",
                "data": line.decode('utf-8'),
            }
        )