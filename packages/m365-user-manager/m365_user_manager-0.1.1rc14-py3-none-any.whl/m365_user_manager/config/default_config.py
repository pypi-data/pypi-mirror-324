#!/usr/bin/env python
# -*- coding: utf-8 -*-
# ./m365_user_manager/config/default_config.py

from cw_rpa_unified_logger import LoggerType, LoggerConfig
from typing import Optional

def logging_config(discord_webhook_url: Optional[str] = None) -> LoggerConfig:
  if discord_webhook_url:
      return LoggerConfig(
          discord_webhook_url=discord_webhook_url,
          enabled_loggers={LoggerType.LOCAL, LoggerType.DISCORD, LoggerType.ASIO},
          logger_name="M365UserManager"
      )
  else:
      return LoggerConfig(
          enabled_loggers={LoggerType.LOCAL, LoggerType.ASIO},
          logger_name="M365UserManager"
      )