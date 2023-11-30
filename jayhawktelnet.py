import asyncio
from espn_api_manager import ESPNAPIManager
import os
import sys
import telnetlib3

class JayhawkTelnet:
    CFB_WINS = ""
    CFB_LOSSES = ""
    CFB_CONF_WINS = ""
    CFB_CONF_LOSSES = ""
    CFB_RECENT_GAME = ""
    CFB_SCHEDULE = ""

    # Update stats every few minutes so people can't basically spam ESPN with requests
    async def update_stats():
        while True:
            cfb_stats = ESPNAPIManager.UpdateCFBStats()
            JayhawkTelnet.CFB_WINS = cfb_stats['wins']
            JayhawkTelnet.CFB_LOSSES = cfb_stats['losses']
            JayhawkTelnet.CFB_CONF_WINS = cfb_stats['conf_wins']
            JayhawkTelnet.CFB_CONF_LOSSES = cfb_stats['conf_losses']
            JayhawkTelnet.CFB_RECENT_GAME = cfb_stats['last_game']
            JayhawkTelnet.CFB_SCHEDULE = ESPNAPIManager.CFBSchedule()
            await asyncio.sleep(500)

    async def handler(reader, writer):
        client_ip = writer.get_extra_info('peername')[0]
        writer.write(f"Hello and welcome, {client_ip}!")
        writer.write(f"\r\nYou've reached JayhawkTelnet, the internet's #1 telnet-based source of KU sports info.")
        writer.write(f"\r\nMade by Drew Fink. Rock Chalk!")
        writer.write(f"\r\nFootball stats:\r\n------------------------")
        writer.write(f"\r\nRecord: {JayhawkTelnet.CFB_WINS}-{JayhawkTelnet.CFB_LOSSES}")
        writer.write(f"\r\nConference record: {JayhawkTelnet.CFB_CONF_WINS}-{JayhawkTelnet.CFB_CONF_LOSSES}")
        writer.write(f"\r\nLast game: {JayhawkTelnet.CFB_RECENT_GAME}")
        writer.write(f'\r\nUse command "football" for the full football schedule.')
        command = ""
        while True:
            # Act like we're reading a username
            user_input = await reader.read(1)
            if not user_input:
                break
            # Command sent
            elif '\r' in user_input:
                match command:
                    case "football":
                        writer.write("\r\n")
                        for game in JayhawkTelnet.CFB_SCHEDULE:
                            writer.write(f"\r\n{game}")
                        writer.close()
                    case default:
                        writer.write("\r\nInvalid input. Please reconnect and try again.")
                        writer.close()
            else:
                command += user_input
                writer.write(user_input)
        writer.close()

try:
    loop = asyncio.get_event_loop()
    coro = telnetlib3.create_server(port=23, shell=JayhawkTelnet.handler, timeout=120)
    loop.create_task(JayhawkTelnet.update_stats())
    print("JayhawkTelnet running.")
    ESPNAPIManager.CFBSchedule()
    telnet_server = loop.run_until_complete(coro)
    loop.run_until_complete(telnet_server.wait_closed())
except KeyboardInterrupt:
    try:
        print("Quitting JayhawkTelnet.")
        sys.exit(0)
    except SystemExit:
        os._exit(0)