import os
from datetime import datetime

from loguru import logger
from pydantic import Field

from plurally.models.env_vars import BaseEnvVars, OpenAiApiKeyRequired
from plurally.models.misc import AudioFile
from plurally.models.node import Node


class Transcript(Node):
    ICON = "openai"

    class EnvVars(BaseEnvVars):
        OPENAI_API_KEY: str = OpenAiApiKeyRequired

    class InitSchema(Node.InitSchema):
        pass

    class InputSchema(Node.InputSchema):
        audio: AudioFile = Field(
            title="Audio",
            description="The audio file",
            json_schema_extra={
                "type-friendly": "Audio",
            },
        )
        # FIXME: Prompt is buggy as hell and completely messes up the transcription
        # do not use it
        # prompt: str = Field(
        #     "",
        #     title="Prompt",
        #     description="The prompt to use for the transcription",
        #     json_schema_extra={
        #         "uiSchema": {"ui:widget": "textarea", "ui:options": {"rows": 10}}
        #     },
        # )

    class OutputSchema(Node.OutputSchema):
        transcript: str = Field(
            description="The extracted transcript from the audio file.",
        )

    def __init__(self, init_inputs: Node.InitSchema):
        self._client = None
        self.model = "whisper-1"
        super().__init__(init_inputs)

    @property
    def client(self):
        global OpenAI
        from openai import OpenAI

        if self._client is None:
            self._client = OpenAI()
        return self._client


    def forward(self, node_inputs: InputSchema):
        logger.debug(f"Transcribing audio {node_inputs.audio.filename}")

        transcription = self.client.audio.transcriptions.create(
            model=self.model,
            file=(node_inputs.audio.filename, node_inputs.audio.content),
        )

        dt_str = datetime.now().strftime("%Y-%m-%d-%H-%M-%S")
        with open(f"{dt_str}.txt", "w") as f:
            f.write(transcription.text)
        
        self.outputs = {"transcript": transcription.text}
