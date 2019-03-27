from rasa_core.channels.channel import InputChannel
from rasa_core.channels.slack import SlackInput
from rasa_core.agent import Agent
from rasa_core.interpreter import RasaNLUInterpreter
import yaml
# from slack_connector import SlackInput
from rasa_core.utils import EndpointConfig

nlu_interpreter = RasaNLUInterpreter('./models/nlu/default/weathernlu')
action_endpoint = EndpointConfig(url="http://localhost:5055/webhook")
agent = Agent.load('./models/dialogue', interpreter = nlu_interpreter, action_endpoint = action_endpoint)

input_channel = SlackInput(slack_token = 'YiYBQO8sJWAnbF1BPhvQLZNL',#app verification token
                            slack_channel="bot-compare-app" #channel name
                            )

# agent.handle_channel(InputChannel(5004, '/', input_channel))
agent.handle_channels([input_channel], 5004, serve_forever=True)