import json
from difflib import SequenceMatcher

from .import_utils import ignore_transformers_warnings

with ignore_transformers_warnings():
    from transformers import PreTrainedTokenizer

from functools import cache

from jinja2.exceptions import TemplateError
from transformers import logging as transformers_logging

from ..utils.hf_hub_utils import _has_file
from ..utils.import_utils import ignore_transformers_warnings

with ignore_transformers_warnings():
    from transformers import AutoConfig, AutoTokenizer


class HFChatPromptTemplateResponse:
    def __init__(self, name: str):
        self.name = name

    def __repr__(self):  # pragma: no cover
        return self.name


COULD_NOT_DETECT = HFChatPromptTemplateResponse("COULD_NOT_DETECT")


@cache
def _chat_prompt_template_and_system_prompt_from_tokenizer(
    model_name: str, revision: None | str = None
) -> None | tuple[str, None | HFChatPromptTemplateResponse | str]:
    from ..llms._chat_prompt_templates import (
        SYSTEM_PROMPTS,
        _model_name_to_system_prompt_type,
    )

    # Check if the model exists on HF Hub
    if _has_file(
        repo_id=model_name,
        filename="tokenizer_config.json",
        repo_type="model",
        revision=revision,
    ):
        config = AutoConfig.from_pretrained(model_name, revision=revision)
        is_encoder_decoder = (
            hasattr(config, "is_encoder_decoder") and config.is_encoder_decoder
        )
        transformers_logging_verbosity = transformers_logging.get_verbosity()
        transformers_logging.set_verbosity(transformers_logging.CRITICAL)
        tokenizer = AutoTokenizer.from_pretrained(model_name, revision=revision)

        # Check if the tokenizer has a chat template
        if not is_encoder_decoder and tokenizer.chat_template:
            tokenizer.use_default_system_prompt = False
            system_var = "{{system_prompt}}"
            user_var = "{{prompt}}"
            assistant_var = "{{response}}"
            system_message = {"role": "system", "content": system_var}
            user_message = {"role": "user", "content": user_var}
            assistant_message = {"role": "assistant", "content": assistant_var}
            system_chat = [system_message, user_message]
            chat = [user_message]

            # Check if the chat template supports system prompts
            tokenizer.use_default_system_prompt = False
            try:
                without_assistant_message_in_template = tokenizer.apply_chat_template(
                    system_chat, tokenize=False, add_generation_prompt=True
                )
                with_assistant_message_in_template = tokenizer.apply_chat_template(
                    system_chat + [assistant_message],
                    tokenize=False,
                    add_generation_prompt=True,
                )
                assistant_message_in_template = (
                    with_assistant_message_in_template.replace(
                        without_assistant_message_in_template, ""
                    ).lstrip()
                )
                chat_prompt_template = with_assistant_message_in_template.replace(
                    assistant_message_in_template, ""
                )
                assert system_var in chat_prompt_template
                pre_system = chat_prompt_template[
                    : chat_prompt_template.index(system_var)
                ]
                post_system = chat_prompt_template[
                    chat_prompt_template.index(system_var) + len(system_var) :
                ]
                tokenizer.use_default_system_prompt = True
                chat_prompt_template_with_default_system = (
                    tokenizer.apply_chat_template(
                        chat, tokenize=False, add_generation_prompt=True
                    )
                )
                tokenizer.use_default_system_prompt = False
                if (
                    pre_system not in chat_prompt_template_with_default_system
                    or post_system not in chat_prompt_template_with_default_system
                ):
                    assert (
                        _model_name_to_system_prompt_type(model_name) in SYSTEM_PROMPTS
                    )
                    system_prompt = COULD_NOT_DETECT
                else:
                    system_prompt = chat_prompt_template_with_default_system.replace(
                        pre_system, ""
                    ).replace(post_system, "")
            except (TemplateError, AssertionError):
                without_assistant_message_in_template = tokenizer.apply_chat_template(
                    chat, tokenize=False, add_generation_prompt=True
                )
                with_assistant_message_in_template = tokenizer.apply_chat_template(
                    chat + [assistant_message],
                    tokenize=False,
                    add_generation_prompt=True,
                )
                assistant_message_in_template = (
                    with_assistant_message_in_template.replace(
                        without_assistant_message_in_template, ""
                    ).lstrip()
                )
                chat_prompt_template = with_assistant_message_in_template.replace(
                    assistant_message_in_template, ""
                )
                system_prompt = None

            # Strip special tokens
            special_tokens = tokenizer.decode(tokenizer.encode(""))
            if chat_prompt_template.startswith(special_tokens):
                chat_prompt_template = chat_prompt_template.replace(
                    special_tokens, "", 1
                )

            # Return the chat prompt template and system prompt
            transformers_logging.set_verbosity(transformers_logging_verbosity)
            return chat_prompt_template, system_prompt

    return None


def set_hf_chat_template(
    tokenizer: PreTrainedTokenizer, chat_prompt_template: str, system_prompt: None | str
):
    tokenizer.use_default_system_prompt = False
    if "[/INST]" in chat_prompt_template:
        space_after_inst_end = " " if "[/INST] " in chat_prompt_template else ""
        if "<</SYS>>" in chat_prompt_template:
            tokenizer.chat_template = (
                "{% if messages[0]['role'] == 'system' %}{% set loop_messages ="
                " messages[1:] %}{% set system_message = messages[0]['content'] %}"
                "{% else %}{% set loop_messages = messages %}{% set system_message = "
                f"{json.dumps(system_prompt)}"
                " %}{% endif %}{% for message in loop_messages %}{% if (message['role']"
                " == 'user') != (loop.index0 % 2 == 0) %}{{ raise_exception('Conversation"
                " roles must alternate user/assistant/user/assistant/...') }}{% endif %}"
                "{% if loop.index0 == 0 and system_message != false %}{% set content"
                " = '<<SYS>>\\n' + system_message + '\\n<</SYS>>\\n\\n' +"
                " message['content'] %}{% else %}{% set content = message['content'] %}"
                "{% endif %}{% if message['role'] == 'user' %}{{ bos_token + '[INST] ' "
                f"+ content + ' [/INST]{space_after_inst_end}'"
                " }}{% elif message['role'] == 'assistant'"
                " %}{{ content + eos_token }}{% endif %}{% endfor %}"
            )
        else:
            tokenizer.chat_template = (
                "{% set loop_messages = messages %}{% set system_message = false %}"
                "{% for message in loop_messages %}{% if (message['role'] == 'user')"
                " != (loop.index0 % 2 == 0) %}{{ raise_exception('Conversation roles"
                " must alternate user/assistant/user/assistant/...') }}{% endif %}"
                "{% if loop.index0 == 0 and system_message != false %}{% set content = "
                "'<<SYS>>\\n' + system_message + '\\n<</SYS>>\\n\\n' + "
                "message['content'] %}{% else %}{% set content = message['content'] %}"
                "{% endif %}{% if message['role'] == 'user' %}{{ bos_token + '[INST] ' "
                f"+ content + ' [/INST]{space_after_inst_end}'"
                " }}{% elif message['role'] == 'assistant'"
                " %}{{ content + eos_token }}{% endif %}{% endfor %}"
            )
        return
    has_bos_token = len(tokenizer.decode(tokenizer.encode(""))) > 0
    eos_token = tokenizer.eos_token
    has_system_prompt = "{{system_prompt}}" in chat_prompt_template
    if has_system_prompt:
        chat_template = """
        {{ pre_chat }}
        {% for message in messages %}
            {% if loop.first and message["role"] != "system" %}
                {{ pre_system + default_system + post_system }}
            {% endif %}
            {% if message["role"] == "system" %}
                {{ pre_system + message["content"] + post_system }}
            {% elif message["role"] == "user" %}
                {{ pre_user + message["content"] + post_user }}
            {% elif message["role"] == "assistant" %}
                {{ pre_asst  + message["content"] }}{{ eos_token }}
            {% endif %}
            {% if loop.last and add_generation_prompt %}
                {{ pre_asst }}
            {% endif %}
        {% endfor %}
        """.strip()
    else:
        chat_template = """
        {{ pre_chat }}
        {% for message in messages %}
            {% if message["role"] == "user" %}
                {{ pre_user + message["content"] + post_user }}
            {% elif message["role"] == "assistant" %}
                {{ pre_asst  + message["content"] }}{{ eos_token }}
            {% endif %}
            {% if loop.last and add_generation_prompt %}
                {{ pre_asst }}
            {% endif %}
        {% endfor %}
        """.strip()

    pre_prompt = chat_prompt_template.split("{{prompt}}")[0]
    post_prompt = chat_prompt_template.split("{{prompt}}")[1]
    post_prompt_match = chat_prompt_template.split("{{prompt}}")[1]
    while True:
        match = SequenceMatcher(
            None, pre_prompt, post_prompt_match
        ).find_longest_match()
        if match.b == 0:
            break
        else:
            post_prompt_match = post_prompt_match[:-1]

    match_a = (
        pre_prompt.rindex(pre_prompt[match.a : match.a + match.size])
        if has_system_prompt
        else match.a
    )
    separator = pre_prompt[match_a : match_a + match.size]
    if has_system_prompt:
        pre_system, post_system = pre_prompt[:match_a].split("{{system_prompt}}")
        if separator in pre_system:
            pre_chat = pre_system[: pre_system.rindex(separator)]
            pre_system = (
                separator + pre_system[pre_system.rindex(separator) + len(separator) :]
            )
        else:
            pre_chat = ""
        if separator.startswith(eos_token):
            separator = separator.replace(eos_token, "", 1)
            post_user = eos_token
            post_system = eos_token + post_system
        else:
            post_user = ""
    else:
        pre_chat = pre_prompt[:match_a]
        if separator.startswith(eos_token):
            separator = separator.replace(eos_token, "", 1)
            if len(pre_chat) > 0:
                pre_chat += eos_token
            post_user = eos_token
        else:
            post_user = ""
    pre_user = separator + pre_prompt[match_a + match.size :]
    pre_asst = separator + post_prompt[match.b + match.size :]
    if has_system_prompt:
        chat_template = (
            chat_template.replace("pre_system", json.dumps(pre_system))
            .replace("post_system", json.dumps(post_system))
            .replace("default_system", json.dumps(system_prompt))
        )
    chat_template = (
        chat_template.replace("pre_chat", json.dumps(pre_chat))
        .replace("pre_user", json.dumps(pre_user))
        .replace("post_user", json.dumps(post_user))
        .replace("pre_asst", json.dumps(pre_asst))
    )
    chat_template = ("{{ bos_token }}" if has_bos_token else "") + "".join(
        [line.lstrip() for line in chat_template.split("\n")]
    )
    tokenizer.chat_template = chat_template
