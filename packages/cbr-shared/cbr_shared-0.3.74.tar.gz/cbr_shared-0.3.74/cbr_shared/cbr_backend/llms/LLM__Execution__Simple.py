from osbot_utils.type_safe.Type_Safe                                   import Type_Safe


URL__LLM__COMPLETION__PROXY                        = "https://osbot-llms.dev.aws.cyber-boardroom.com/chat/completion"

DEFAULT__LLM__COMPLETION__PROXY__SELECTED_PLATFORM = "Mistral (Free)"   # "Groq (Free)"
DEFAULT__LLM__COMPLETION__PROXY__SELECTED_PROVIDER = "Mistral"          # "1. Meta"
DEFAULT__LLM__COMPLETION__PROXY__SELECTED_MODEL    = "pixtral-12b-2409" # "llama-3.2-11b-vision-preview"

# URL__LLM__COMPLETION__PROXY                        = "http://localhost:5001/api/llms/chat/completion"
# DEFAULT__LLM__COMPLETION__PROXY__SELECTED_PLATFORM = 'Ollama (Local)'
# DEFAULT__LLM__COMPLETION__PROXY__SELECTED_PROVIDER = 'Meta'             # "Microsoft"    #
# DEFAULT__LLM__COMPLETION__PROXY__SELECTED_MODEL    = 'llama3.2:latest'  # 'phi3'         #

class LLM__Execution__Simple(Type_Safe):
    selected_platform : str = DEFAULT__LLM__COMPLETION__PROXY__SELECTED_PLATFORM
    selected_provider : str = DEFAULT__LLM__COMPLETION__PROXY__SELECTED_PROVIDER
    selected_model    : str = DEFAULT__LLM__COMPLETION__PROXY__SELECTED_MODEL
    stream            : bool = False
    target_server     : str = URL__LLM__COMPLETION__PROXY

    def execute(self, **kwargs):
        import requests

        llm_chat_completion = self.llm_chat_completion(**kwargs)
        request_body        = llm_chat_completion.json()
        response            = requests.post(self.target_server, json=request_body)
        response_json       = response.json()
        response_text       = ''.join(response_json)
        return response_text

    def llm_chat_completion(self, user_prompt, system_prompts=None, images=None):
        from cbr_shared.schemas.data_models.llm_chat.LLMs__Chat_Completion import LLMs__Chat_Completion

        user_data      = { "selected_platform": self.selected_platform ,
                           "selected_provider": self.selected_provider ,
                           "selected_model"   : self.selected_model    }

        kwargs  = dict(user_prompt    = user_prompt         ,
                       user_data      = user_data           ,
                       stream         = self.stream         )

        if images        :  kwargs['images'        ] = images
        if system_prompts:  kwargs['system_prompts'] = system_prompts

        return LLMs__Chat_Completion(**kwargs)