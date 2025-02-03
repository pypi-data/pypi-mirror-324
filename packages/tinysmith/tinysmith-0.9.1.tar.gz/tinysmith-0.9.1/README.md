<p align="center">
  <img src="https://i.imgur.com/vWDUm4E.png" width=256 height=256 />
</p>
<h1 align="center">TinyAgentSmith</h1>

TinyAgentSmith (`tinysmith`) is a tiny, modular multi-agent LLM framework. It is designed to be lightweight and simple to use, while providing a flexible and extensible platform for quickly iterating on multi-agent algorithms.

> Tiny: small, lightweight, and simple.  
> Agent Smith: a smith that forges agents, also a reference to the movie "The Matrix".


## Usage Examples
### New Custom Strategy
The most useful feature of `tinysmith` is the ability to define arbitrary new strategies. The following gives an example of how to define a new toy strategy.

#### 0. Add Logging
In order to see what's going on, you can set up logging. The following code snippet shows how to set up the logger for the `tinysmith` framework together with the adapted Intercode library in this repository, to show the agent's interactions. Use `logger.DEBUG` for a detailed output of what each agent's prompts and responses are.

```python
logger.setLevel(logging.INFO)
intercode_logger = logging.getLogger("intercode")
intercode_logger.setLevel(logging.INFO)
tinysmith_logger = logging.getLogger("tinysmith")
tinysmith_logger.setLevel(logging.INFO)
```

#### 1. Define Agents and Collaboration
We want to define an example toy strategy where two agents communicate: An agent that throws a coin, and a poet agent that writes a poem based on the coin's outcome.

The transition function defines which agent is called under what circumstances. The following transition function give a simple example of how to switch between the agents. The transition function can access the full state object and can be made arbitrarily complex.

```python
def transition(obs, state):
    if state.get_agent_name() == 'init':
        state.set_agent_name('coinflip_agent')
    elif state.get_agent_name() == 'coinflip_agent':
        state.set_agent_name('poet_agent')
        state.set_is_envstep(True)  # The poet's output is always passed to the environment
    elif state.get_agent_name() == 'poet_agent':
        state.set_agent_name('coinflip_agent')
```

The PromptEngineer implementations determine the agent's behavior. The following code snippet shows the implementation of the PromptEngineer for the coinflip and poet agents. 
```python
from tinysmith.orchestrator.prompting import PromptEngineer
from tinysmith.orchestrator.state import State
from tinysmith.orchestrator.utils import signal_error

class CoinflipPE(PromptEngineer):
    def render_prompt(self, obs, hist, state):
        # In order to shape the agent's behavior, create a prompt as a string and append it to the history.
        prompt = 'Flip a coin. Answer only with "heads" or "tails".'
        hist.append(UserMessage(prompt))

    def process_response(self, obs, res, hist, state):
        # The LLMs response can be arbitrarily parsed and processed here. It usually makes sense to store some information in the state object to communicate it to other agents.
        if (('heads' in res.lower() and 'tails' in res.lower()) 
            or ('heads' not in res.lower() and 'tails' not in res.lower())):
            # If the response is not valid, the signale_error helper function can be used to reprompt the agent.
            signal_error(state, 
                         'Invalid flip.', 
                         'Invalid response. Please answer either heads or tails.')
            return ''

        # Store the coinflip result in the agent's namespace in the state object
        coinflip_agent_state = state.get('coinflip') if state.get('coinflip') else {}
        if 'heads' in res.lower(): 
            coinflip_agent_state['flip'] = 'heads'
        else:
            coinflip_agent_state['flip'] = 'tails'
        state.set('coinflip', coinflip_agent_state)

    def reset(self):
        pass

class PoetPE(PromptEngineer):
    def render_prompt(self, obs, hist, state):
        # Other agents' state can be accessed to use information gathered by other agents previously.
        coinflip_agent_state = state.get('coinflip')

        prompt = "Your output will be interpretet by a bash shell. " \
                + "Use the echo command to print your output. " \
                + "Print a happy poem about randomness." \
                + f"Include the coinflip result: {coinflip_agent_state['flip']}."
        hist.append(UserMessage(prompt))

    def process_response(self, obs, res, hist, state):
        return res

    def reset(self):
        pass
```

#### 2. Define the Agents and Orchestrator
Once the strategy is defined, the components are just plugged into the framework objects and can be run.
`tinysmith` provides a selection of LLM adapters (i.e., for https://mistral.ai/, https://openai.com/, and https://groq.com/) in `/llm/adapters.py`. 
Use groq for a free option. Simply replace the `api_key` with the one provided by the respective service.

```python
from tinysmith.agent.agent import Agent
from tinysmith.llm.adapters import UserMessage, GroqAPIAdapter
from tinysmith.orchestrator.orchestrator import Orchestrator

token_usage = {} # This can be used to log the token usage by the LLM.
# Create LLM adapter for the agents
llm = GroqAPIAdapter(
        model='llama3-8b-8192', 
        temperature=1,
        top_p=1,
        token_usage=token_usage,
        api_key='XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX')

# Create the agents with their PromptEngineer and LLM adapter implementations. Their name must match the transition function.
coinflip_agent = Agent('coinflip_agent', CoinflipPE(), llm)
poet_agent = Agent('poet_agent', PoetPE(), llm)

# The state object should be prefilled with all necessary information for the strategy and with meta information.
state = State()
state.set_max_errors(3) # The orchestrator stops if it encounters more than 3 errors in agent executions.
state.set_max_steps(10) # The orchestrator stops after 10 environment steps.

# Assemble all components into the orchestrator
orchestrator = Orchestrator([coinflip_agent, poet_agent], transition, state)
```

#### 3. Run the Orchestrator
Create an environment (e.g. Intercode) and run the orchestrator and the environment in a loop. 

To emulate an environement you could use something like this:
```python
while True:
    print(orchestrator.forward(input("> "), 0))
```

#### Full Example
```python
import logging

from tinysmith.agent.agent import Agent
from tinysmith.llm.adapters import UserMessage, GroqAPIAdapter
from tinysmith.orchestrator.orchestrator import Orchestrator
from tinysmith.orchestrator.prompting import PromptEngineer
from tinysmith.orchestrator.state import State
from tinysmith.orchestrator.utils import signal_error

logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)
tinysmith_logger = logging.getLogger("tinysmith")
tinysmith_logger.setLevel(logging.DEBUG)

class CoinflipPE(PromptEngineer):
    def render_prompt(self, obs, hist, state):
        prompt = 'Flip a coin. Answer only with "heads" or "tails".'
        hist.append(UserMessage(prompt))

    def process_response(self, obs, res, hist, state):
        if (('heads' in res.lower() and 'tails' in res.lower()) 
            or ('heads' not in res.lower() and 'tails' not in res.lower())):
            signal_error(state, 
                         'Invalid flip.', 
                         'Invalid response. Please answer either heads or tails.')
            return ''

        coinflip_agent_state = state.get('coinflip') if state.get('coinflip') else {}
        if 'heads' in res.lower(): 
            coinflip_agent_state['flip'] = 'heads'
        else:
            coinflip_agent_state['flip'] = 'tails'
        state.set('coinflip', coinflip_agent_state)

    def reset(self):
        pass

class PoetPE(PromptEngineer):
    def render_prompt(self, obs, hist, state):
        coinflip_agent_state = state.get('coinflip')

        prompt = "Your output will be interpretet by a bash shell. " \
                + "Use the echo command to print your output. " \
                + "Print a happy poem about randomness." \
                + f"Include the coinflip result: {coinflip_agent_state['flip']}."
        hist.append(UserMessage(prompt))

    def process_response(self, obs, res, hist, state):
        return res

    def reset(self):
        pass

token_usage = {}
llm = GroqAPIAdapter(
        model='llama3-8b-8192', 
        temperature=1,
        top_p=1,
        token_usage=token_usage,
        api_key='XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX')

coinflip_agent = Agent('coinflip_agent', CoinflipPE(), llm)
poet_agent = Agent('poet_agent', PoetPE(), llm)

def transition(obs, state):
    if state.get_agent_name() == 'init':
        state.set_agent_name('coinflip_agent')
    elif state.get_agent_name() == 'coinflip_agent':
        state.set_agent_name('poet_agent')
        state.set_is_envstep(True)
    elif state.get_agent_name() == 'poet_agent':
        state.set_agent_name('coinflip_agent')

state = State()
state.set_max_errors(3)
state.set_max_steps(10)
orchestrator = Orchestrator([coinflip_agent, poet_agent], transition, state)


while True:
    print(orchestrator.forward(input("> "), 0))

```

### Built-In: Planner/Reviewer/Executor Strategy
This is an example of the built-in planner/reviewer/executor strategy. All built-in strategies can be found in `/agent/strategies/`. These strategies are used mainly for experimentation and as a reference for creating custom strategies.

```python
import logging

from tinysmith.agent.agent import Agent
from tinysmith.agent.strategies.planner_reviewer_executor.prompting import (
    ExecutorPromptEngineer,
    PlannerPromptEngineer,
    ReviewerPromptEngineer,
)
from tinysmith.agent.strategies.planner_reviewer_executor.transition import (
    planner_reviewer_executor,
)
from tinysmith.llm.adapters import MistralAPIAdapter, OpenAiAPIAdapter
from tinysmith.orchestrator.orchestrator import Orchestrator
from tinysmith.orchestrator.state import State

# Set up logging to see what's going on
logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)
tinysmith_logger = logging.getLogger("tinysmith")
tinysmith_logger.setLevel(logging.INFO)

# 'Large LLM' Adapter
openai_llm_adapter = OpenAiAPIAdapter(
        model = 'gpt-4',
        temperature = 0,
        top_p = 1,
        token_usage = {},
        api_key = "<API KEY>")

# 'Small LLM' Adapter
mistral_llm_adapter = MistralAPIAdapter(
        model = 'open-mixtral-8x7b',
        temperature = 0,
        top_p = 1,
        token_usage = {},
        api_key = "<API KEY>")


# Agents
planner = Agent(
        name = 'planner',
        prompt_engineer = PlannerPromptEngineer(),
        llm_adapter = mistral_llm_adapter
        )
reviewer = Agent(
        name = 'reviewer',
        prompt_engineer = ReviewerPromptEngineer(),
        llm_adapter = mistral_llm_adapter
        )
executor = Agent(
        name = 'executor',
        prompt_engineer = ExecutorPromptEngineer(),
        llm_adapter = mistral_llm_adapter
        )

# Define the orchestrator state and set all necessary information for your strategy
# For example, the challenge description, and the reviewer's maximum number of rejections
state = State()
state.set_max_errors(3)
state.set('challenge_description', 'The flag is in a hidden file. Have fun!')
state.set('executor', {'max_steps': 10})
state.set('reviewer', {'max_rejects': 1})

# Define the orchestrator with the agents, transition function, and state
orchestrator = Orchestrator(
        agents=[planner, reviewer, executor],
        transition=planner_reviewer_executor,
        state=state)

# === Use the agent in some kind of environment loop. ===
# - BYO environment, e.g InterCode. -

obs = ""
while True:
    print(f"Agent chose the following action: {orchestrator.forward(obs, 0)}")
    obs = input("Play environment. Enter observation: ")
```

### Selfhosted LLM
The easiest way to use a self-hosted LLM, is to run it in an inference engine with a OpenAI compatible API. The `CustomAPIAdapter` class can then be used to connect to the self-hosted LLM. 

1. Follow the steps to set up vLLM with an API server: https://docs.vllm.ai/en/latest/serving/openai_compatible_server.html
    - The vLLM server can run on any local or remote machine 
    - The server must be accessible from the host running `tinysmith`.
2. Connect the `CustomAPIAdapter` to the self-hosted LLM.

The following code snippet shows how to connect to a self-hosted LLM.

```python
llm = CustomAPIAdapter(
        model='NousResearch/Meta-Llama-3-8B-Instruct', 
        temperature=0.5,
        top_p=1,
        token_usage={},
        api_key = "token-abc123",
        base_url='http://localhost:8000/v1')
```
