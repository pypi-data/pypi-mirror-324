from pathlib import Path
import time
from typing import Tuple, Optional

from wyn_voice.chat import ChatBot, AudioProcessor
from autogen import ConversableAgent
from pydub import AudioSegment
from autogen.coding import LocalCommandLineCodeExecutor


class WynVoiceUltra:
    """
    This class encapsulates all the functionality to run a voice-based conversation
    system with multiple assistants, code execution, and audio input/output. It uses
    the `wyn_voice.chat` module for chat and audio processing, as well as
    `autogen.ConversableAgent` for code execution. The primary usage is to call the
    `run()` method in a Jupyter notebook environment, which will continuously prompt
    the user via voice, and respond back with text and voice output.

    Example:
    -------
    >> bot = WynVoiceUltra(openai_api_key="YOUR_OPENAI_KEY", role="Lifestyle Helper")
    >> bot.run()
    """

    def __init__(self, openai_api_key: str = "KEY_HERE", role: str = "Lifestyle Helper") -> None:
        """
        Initialize the WynVoiceUltra system with an OpenAI API key and a default
        assistant role.

        Parameters
        ----------
        openai_api_key : str
            The OpenAI API key for accessing GPT-based assistants.
        role : str
            A string specifying which assistant role to default to. Possible values
            are "Coding Helper", "Lifestyle Helper", "Therapist", or "Drivethrough".
        """

        # Store parameters
        self.openai_api_key = openai_api_key
        self.role = role

        # Prepare working directory for code execution
        self.work_dir = Path("coding")
        self.work_dir.mkdir(exist_ok=True)

        # Create a local command line code executor
        self.executor = LocalCommandLineCodeExecutor(work_dir=self.work_dir)

        # Create an agent with code executor configuration
        self.code_executor_agent = ConversableAgent(
            "code_executor_agent",
            llm_config=False,  # Turn off LLM for this agent.
            code_execution_config={"executor": self.executor},  # Local command line code executor.
            human_input_mode="NEVER",  # Always take human input for this agent for safety.
        )

        # Define all possible assistants
        self.assistant_v1 = ChatBot(
            api_key=self.openai_api_key,
            protocol=(
                "You are a helpful assistant.\n\n"
                "If user asks you python related question, you will ask question back and clarify it.\n"
                "If all makes sense, you will write the python code for user.\n"
                "If the python code is written from before, ask user whether they want to execute it.\n"
            )
        )
        self.assistant_v2 = ChatBot(
            api_key=self.openai_api_key,
            protocol=(
                "You are a helpful assistant. You are an expert to recommend life style choices."
            )
        )
        self.assistant_v3 = ChatBot(
            api_key=self.openai_api_key,
            protocol=(
                "You are a therapist.\n\n"
                "You are an expert at guiding people through mental health stresses and work situations.\n"
                "You are a good listener and you take the patients (user) complain and try to understand it.\n"
                "When user ask, you may suggest some life style choices to the user based on the user's complain.\n"
            )
        )
        self.assistant_v4 = ChatBot(
            api_key=self.openai_api_key,
            protocol=(
                "You are a McDonald drivethrough service assistant.\n\n"
                "Here's a menu for the day:\n\n"
                "| Item                       | Price  | Calories |\n"
                "|----------------------------|--------|----------|\n"
                "| Big Mac                    | $5.99  | 550      |\n"
                "| Quarter Pounder with Cheese| $6.49  | 750      |\n"
                "| McChicken                  | $3.29  | 400      |\n"
                "| Filet-O-Fish               | $4.99  | 390      |\n"
                "| French Fries (Medium)      | $2.99  | 340      |\n"
                "| Chicken McNuggets (10 pcs) | $5.49  | 480      |\n"
                "| McDouble                   | $2.99  | 390      |\n"
                "| Egg McMuffin               | $3.99  | 300      |\n"
                "| Sausage Biscuit            | $2.79  | 460      |\n"
                "| Apple Pie                  | $1.49  | 240      |\n\n"
                "You are designed to serve the cutomer with the best price and calories combination.\n\n"
                "User will ask you some questions and price and calories.\n\n"
                "Ask user if they are ready to confirm the order.\n\n"
                "If user is ready to confirm the order, write a python code for the order. "
                "The python code saves the order in a csv file.\n"
                "If user is not ready to confirm the order, ask user if there's anything to add.\n"
            )
        )

        # Pick the assistant and audio processor based on the default role
        self.assistant, self.audio_processor = self._set_assistant(self.role)

    def _set_assistant(self, value: str) -> Tuple[ChatBot, AudioProcessor]:
        """
        Internal helper method to select the appropriate assistant and audio processor
        based on the role specified.

        Parameters
        ----------
        value : str
            The role for which assistant and audio processor will be initialized.

        Returns
        -------
        Tuple[ChatBot, AudioProcessor]
            A tuple of ChatBot and AudioProcessor corresponding to the specified role.
        """
        if value == "Coding Helper":
            assistant = self.assistant_v1
        elif value == "Lifestyle Helper":
            assistant = self.assistant_v2
        elif value == "Therapist":
            assistant = self.assistant_v3
        else:
            # Default to "Drivethrough" or any non-specified
            assistant = self.assistant_v4

        audio_processor = AudioProcessor(bot=assistant)
        return assistant, audio_processor

    def run(self) -> None:
        """
        Run the main conversation loop that captures voice input, processes user requests,
        and provides both textual and audio responses. This loop will continue until
        the user says "exit" in their prompt. If the user says "execute", it will attempt
        to run the previously generated code through a local code executor.
        """
        prompt: str = ""
        response: str = ""
        reply: str = ""
        audio_length: float = 0.0

        while "exit" not in prompt.lower():
            # Get voice input from user
            prompt = self.audio_processor.voice_to_text(sec=4)
            print("🤔 User: ", prompt)

            # Check if user wants to execute the code
            if "execute" in prompt.lower():
                message_with_code_block = (
                    f"This is a message with code block.\n{response}"
                )

                # Generate a reply for the given code
                reply = self.code_executor_agent.generate_reply(
                    messages=[{"role": "user", "content": message_with_code_block}]
                )
                print("💻 Executing....")
                print(reply)

                # Generate the assistant's response after execution
                try:
                    response = self.assistant.generate_response(
                        f"""User has provided the prompt: {prompt}
                        And previously we have an answer: {response}

                        Now that the code finished executing. Here's the result: {reply}.

                        Summarize the result and ask for another question or task.
                        """
                    )
                    print("🤖 Bot: ", response)
                except:
                    # In case of an error, re-initialize assistant and try again
                    self.assistant, self.audio_processor = self._set_assistant(self.role)
                    response = self.assistant.generate_response(
                        f"""User has provided the prompt: {prompt}
                        And previously we have an answer: {response}

                        Now that the code finished executing. Here's the result: {reply}.

                        Summarize the result and ask for another question or task.
                        """
                    )
                    print("🤖 Bot: ", response)

            else:
                # Generate the assistant's response
                try:
                    response = self.assistant.generate_response(prompt)
                    print("🤖 Bot: ", response)
                except:
                    # In case of an error, re-initialize assistant and try again
                    self.assistant, self.audio_processor = self._set_assistant(self.role)
                    response = self.assistant.generate_response(prompt)
                    print("🤖 Bot: ", response)

            # If the assistant's response is long or contains code, generate a shorter summary for audio
            if "\n\n```python" in response.lower() or len(response) > 500:
                response_short = self.assistant.generate_response(
                    f"Summarize the following in 1-2 sentences: {response}"
                )
            else:
                response_short = response

            # Convert the assistant's response to audio
            output_file_path = self.audio_processor.text_to_voice(response_short)
            audio = AudioSegment.from_file(output_file_path)
            audio_length = len(audio) / 1000.0 + 1
            print("⏳ Audio lag: ", audio_length)

            # Delay the next iteration based on audio length
            time.sleep(audio_length)
