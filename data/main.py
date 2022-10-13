#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import logging
import base64
import json
import os.path

from socket_server import SocketServer
from systemd.journal import JournaldLogHandler


def main():
    logger = logging.getLogger("FakeMCServer")
    logger.setLevel(logging.INFO)
    console_handler = logging.StreamHandler()
    console_handler.setLevel(logging.INFO)
    journal_handler = JournaldLogHandler()
    journal_handler.setLevel(logging.INFO)
    formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
    console_handler.setFormatter(formatter)
    journal_handler.setFormatter(formatter)
    logger.addHandler(console_handler)
    logger.addHandler(journal_handler)
    if os.path.exists("standby.json"):
        logger.info("Loading configuration...")
        with open("standby.json", 'r', encoding='windows-1255') as file:
            configuration = json.load(file,)

        ip = configuration["ip"]
        port = configuration["port"]
        motd = configuration["motd"]["first_line"] + "\n" + configuration["motd"]["second_line"]
        version_text = configuration["version_text"]
        samples = configuration["samples"]
        show_hostname = configuration["show_hostname_if_available"]

        player_max = configuration.get("player_max", 0)
        player_online = configuration.get("player_online", 0)
        protocol = configuration.get("protocol", 2)
        kick_message = "\n".join(configuration["kick_message"])

        if not os.path.exists(configuration["server_icon"]):
            logger.warning("Server icon doesn't exists - submitting none...")
            server_icon = None
        else:
            with open(configuration["server_icon"], 'rb') as image:
                server_icon = "data:image/png;base64," + base64.b64encode(image.read()).decode()
        server = None
        try:
            logger.info("Setting up server...")
            server = SocketServer(ip, port, motd, version_text, kick_message, samples, server_icon, logger, show_hostname, player_max, player_online, protocol)
            server.start()
        except KeyboardInterrupt:
            logger.info("Shutting down server...")
            server.close()
            logger.info("Done. Thanks for using FakeMCServer!")
            exit(0)
        except Exception as e:
            logger.exception(e)
    else:
        logger.warning("No configuration file found. Creating standby.json...")
        configuration = {
            "ip": "0.0.0.0",
            "port": 25565,
            "protocol": 2,
            "motd": {
                "first_line": "§4Maintenance!",
                "second_line": "§aCheck example.com for more information!",
            },
            "version_text": "§4Maintenance",
            "kick_message": ["§bSorry", "", "§aThis server is offline!"],
            "server_icon": "server_icon.png",
            "samples": ["§bexample.com", "", "§4Maintenance"],
            "show_hostname_if_available": True,
            "show_ip_if_hostname_available": True,
            "player_max": 0,
            "player_online": 0,
        }

        with open("standby.json", 'w', encoding='windows-1255') as file:
            json.dump(configuration, file, sort_keys=True, indent=4, ensure_ascii=False)
        logger.info("Please adjust the settings in the standby.json!")
        exit(1)


if __name__ == '__main__':
    main()
