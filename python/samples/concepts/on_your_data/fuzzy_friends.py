import asyncio
import logging

from semantic_kernel import Kernel
from semantic_kernel.connectors.ai.chat_completion_client_base import ChatCompletionClientBase
from semantic_kernel.connectors.ai.function_call_behavior import FunctionCallBehavior
from semantic_kernel.connectors.ai.open_ai import AzureChatCompletion
from semantic_kernel.connectors.ai.open_ai.prompt_execution_settings.azure_chat_prompt_execution_settings import (
    AzureChatPromptExecutionSettings,
)
from semantic_kernel.contents.chat_history import ChatHistory
from semantic_kernel.core_plugins.time_plugin import TimePlugin
from semantic_kernel.functions.kernel_arguments import KernelArguments


async def main():
    print("running main")
    # Initialize the kernel
    kernel = Kernel()

    # Add Azure OpenAI chat completion
    kernel.add_service(AzureChatCompletion(
        # deployment_name="your_models_deployment_name",
        # api_key="your_api_key",
        # base_url="your_base_url",
    ))

    # Set the logging level for  semantic_kernel.kernel to DEBUG.
    logging.basicConfig(
        format="[%(asctime)s - %(name)s:%(lineno)d - %(levelname)s] %(message)s",
        datefmt="%Y-%m-%d %H:%M:%S",
    )
    logging.getLogger("kernel").setLevel(logging.DEBUG)

    # Add a plugin (the LightsPlugin class is defined below)
    kernel.add_plugin(
        TimePlugin(),
        plugin_name="timePlugin",
    )

    chat_completion: AzureChatCompletion = kernel.get_service(type=ChatCompletionClientBase)

    # Enable planning
    execution_settings = AzureChatPromptExecutionSettings(tool_choice="auto")
    execution_settings.function_call_behavior = FunctionCallBehavior.EnableFunctions(auto_invoke=True, filters={})

    # Create a history of the conversation
    history = ChatHistory()
    history.add_user_message("Can you help me write an email for my boss?")

    result = (await chat_completion.get_chat_message_contents(
        chat_history=history,
        settings=execution_settings,
        kernel=kernel,
        arguments=KernelArguments(),
    ))[0]

    print(result)

# Run the main function


if __name__ == "__main__":
    asyncio.run(main())
