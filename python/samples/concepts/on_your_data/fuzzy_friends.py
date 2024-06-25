import asyncio

from samples.concepts.on_your_data.email_plugin import EmailPlugin
from semantic_kernel import Kernel
from semantic_kernel.contents.chat_history import ChatHistory
from semantic_kernel.connectors.ai.open_ai import AzureChatCompletion
from semantic_kernel.connectors.ai.function_call_behavior import FunctionCallBehavior
from semantic_kernel.connectors.ai.chat_completion_client_base import ChatCompletionClientBase
from semantic_kernel.connectors.ai.open_ai.prompt_execution_settings.azure_chat_prompt_execution_settings import (
    AzureChatPromptExecutionSettings,
)
from semantic_kernel.functions.kernel_arguments import KernelArguments

async def main():
    # Initialize the kernel
    kernel = Kernel()

    # Add Azure OpenAI chat completion
    kernel.add_service(AzureChatCompletion(
    ))

    # Add a plugin
    kernel.add_plugin(
        EmailPlugin(),
        plugin_name="Email",
    )

    chat_completion : AzureChatCompletion = kernel.get_service(type=ChatCompletionClientBase)

    # Enable planning
    execution_settings = AzureChatPromptExecutionSettings(tool_choice="auto")
    execution_settings.function_call_behavior = FunctionCallBehavior.EnableFunctions(auto_invoke=True, filters={})

    # Create a history of the conversation
    history = ChatHistory()

    # Start the conversation
    while True:
        # Get user input
        user_input = input("User > ")
        history.add_user_message(user_input)

        # Get the response from the AI
        result = (await chat_completion.get_chat_message_contents(
            chat_history=history,
            settings=execution_settings,
            kernel=kernel,
            arguments=KernelArguments(),
        ))[0]

        # Print the response
        print("Assistant > " + str(result))
        history.add_assistant_message(str(result))

# Run the main function
if __name__ == "__main__":
    asyncio.run(main())
