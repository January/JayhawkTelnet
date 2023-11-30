import asyncio
import os
import sys
import telnetlib3

async def handler(reader, writer):
    client_ip = writer.get_extra_info('peername')[0]
    writer.write(f"Hello and welcome, {client_ip}!")
    writer.write(f"\r\nYou've reached JayhawkTelnet, the internet's #1 telnet-based source of KU sports info.")
    writer.write(f"\r\nMade by Drew Fink. Rock Chalk!")
    writer.close()

try:
    loop = asyncio.get_event_loop()
    coro = telnetlib3.create_server(port=23, shell=handler)
    print("JayhawkTelnet running.")
    telnet_server = loop.run_until_complete(coro)
    loop.run_until_complete(telnet_server.wait_closed())
except KeyboardInterrupt:
    try:
        print("Quitting JayhawkTelnet.")
        sys.exit(0)
    except SystemExit:
        os._exit(0)