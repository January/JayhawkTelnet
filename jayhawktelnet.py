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

    MENS_CBB_WINS = ""
    MENS_CBB_LOSSES = ""
    MENS_CBB_CONF_WINS = ""
    MENS_CBB_CONF_LOSSES = ""
    MENS_CBB_RECENT_GAME = ""
    MENS_CBB_SCHEDULE = ""

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

            mens_cbb_stats = ESPNAPIManager.UpdateMensCBBStats()
            JayhawkTelnet.MENS_CBB_WINS = mens_cbb_stats['wins']
            JayhawkTelnet.MENS_CBB_LOSSES = mens_cbb_stats['losses']
            JayhawkTelnet.MENS_CBB_CONF_WINS = mens_cbb_stats['conf_wins']
            JayhawkTelnet.MENS_CBB_CONF_LOSSES = mens_cbb_stats['conf_losses']
            JayhawkTelnet.MENS_CBB_RECENT_GAME = mens_cbb_stats['last_game']
            JayhawkTelnet.MENS_CBB_SCHEDULE = ESPNAPIManager.MensCBBSchedule()

            await asyncio.sleep(500)

    async def handler(reader, writer):
        client_ip = writer.get_extra_info('peername')[0]
        writer.write(f"Hello and welcome, {client_ip}!")
        writer.write(f"\r\nYou've reached JayhawkTelnet, the internet's #1 telnet-based source of KU sports info.")
        writer.write(f"\r\nMade by Drew Fink. Rock Chalk!")
        writer.write(f"\r\n\r\nFootball stats:\r\n------------------------")
        writer.write(f"\r\nRecord: {JayhawkTelnet.CFB_WINS}-{JayhawkTelnet.CFB_LOSSES}")
        writer.write(f"\r\nConference record: {JayhawkTelnet.CFB_CONF_WINS}-{JayhawkTelnet.CFB_CONF_LOSSES}")
        writer.write(f"\r\nLast game: {JayhawkTelnet.CFB_RECENT_GAME}")
        writer.write(f'\r\nUse command "football" for the full football schedule.')
        writer.write(f"\r\n\r\nMen's basketball stats:\r\n------------------------")
        writer.write(f"\r\nRecord: {JayhawkTelnet.MENS_CBB_WINS}-{JayhawkTelnet.MENS_CBB_LOSSES}")
        writer.write(f"\r\nConference record: {JayhawkTelnet.MENS_CBB_CONF_WINS}-{JayhawkTelnet.MENS_CBB_CONF_LOSSES}")
        writer.write(f"\r\nLast game: {JayhawkTelnet.MENS_CBB_RECENT_GAME}")
        writer.write(f'\r\nUse command "mensbb" for the full men\'s basketball schedule.')
        command = ""
        while True:
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
                    case "mbasketball":
                        writer.write("\r\n")
                        for game in JayhawkTelnet.MENS_CBB_SCHEDULE:
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
    telnet_server = loop.run_until_complete(coro)
    loop.run_until_complete(telnet_server.wait_closed())
except KeyboardInterrupt:
    try:
        print("Quitting JayhawkTelnet.")
        sys.exit(0)
    except SystemExit:
        os._exit(0)