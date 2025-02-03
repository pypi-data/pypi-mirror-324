from Communist.logging_config import setup_logging

setup_logging()

from Communist.agent.prompts import SystemPrompt as SystemPrompt
from Communist.agent.service import Agent as Agent
from Communist.agent.views import ActionModel as ActionModel
from Communist.agent.views import ActionResult as ActionResult
from Communist.agent.views import AgentHistoryList as AgentHistoryList
from Communist.browser.browser import Browser as Browser
from Communist.agent.views import FireflinkNLP as FireflinkNLP
from Communist.browser.browser import BrowserConfig as BrowserConfig
from Communist.controller.service import Controller as Controller
from Communist.dom.service import DomService as DomService

__all__ = [
	'Agent',
	'Browser',
	'BrowserConfig',
	'Controller',
	'DomService',
	'SystemPrompt',
	'ActionResult',
	'ActionModel',
	'AgentHistoryList',
 	'FireflinkNLP'
]
