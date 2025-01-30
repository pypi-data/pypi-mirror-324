from cbr_shared.cbr_backend.llm_chat.models.Model__LLM_Chat__Config             import Model__LLM_Chat__Config
from cbr_shared.cbr_backend.llm_chat.models.Model__LLM_Chat__Feedback__Summary  import Model__LLM_Chat__Feedback__Summary
from cbr_shared.cbr_backend.llm_chat.models.Model__LLM_Chat__Message            import Model__LLM_Chat__Message
from cbr_shared.cbr_backend.llm_chat.models.Model__LLM_Chat__Provider__Setup    import Model__LLM_Chat__Provider__Setup
from cbr_shared.cbr_backend.llm_chat.models.Model__LLM_Chat__Response__Metadata import Model__LLM_Chat__Response__Metadata
from cbr_shared.cbr_backend.llm_chat.models.Model__LLM_Chat                     import Model__LLM_Chat
from cbr_shared.cbr_backend.llm_chat.models.Model__LLM_Chat__User__Feedback     import Model__LLM_Chat__User__Feedback
from osbot_utils.type_safe.Type_Safe                                               import Type_Safe
from osbot_utils.helpers.Random_Guid                                            import Random_Guid
from osbot_utils.utils.Misc                                                     import random_text

class Temp__LLM_Chat__Data(Type_Safe):

    def provider_setup(self):
        return Model__LLM_Chat__Provider__Setup(name        = random_text('provider')  ,
                                                temperature = 0.7                      ,
                                                model      = random_text('model')      ,
                                                api_version= "2024-03"                 ,
                                                description= random_text('description'),
                                                is_active  = True                      )

    def response_metadata(self):
        return Model__LLM_Chat__Response__Metadata(finish_reason = "stop",tokens_used = 128)

    def user_feedback(self):
        return Model__LLM_Chat__User__Feedback(rating        = 1                     ,
                                               is_bookmarked = True                  ,
                                               is_flagged    = False                 ,
                                               comment       = random_text('comment'))

    def feedback_summary(self):
        return Model__LLM_Chat__Feedback__Summary(  total    = 15,
                                                    positive = 1 ,
                                                    negative = 2 ,
                                                    neutral  = 3 ,
                                                    block    = 4 ,
                                                    bookmark = 5 )

    def message(self, role="user"):
        return Model__LLM_Chat__Message(role             = role                    ,
                                        content          = random_text('content'  ),
                                        response_metadata= self.response_metadata(),
                                        user_feedback    = self.user_feedback()    )

    def config(self):
        return Model__LLM_Chat__Config(max_tokens = 2048,
                                       stream     = True,
                                       seed       = 42  )

    def llm_chat(self):
        message             = self.message()
        message_id          = message.message_id

        provider            = self.provider_setup()
        provider_id         = provider.provider_id
        message.provider_id = provider_id

        providers           = { provider_id: provider }
        messages            = { message_id: message   }
        active_branch       = [ message_id]
        token_usage         = { provider_id: 128 }

        return Model__LLM_Chat(active_branch    = active_branch          ,
                               chat_id          = Random_Guid()          ,
                               config           = self.config()          ,
                               feedback_summary = self.feedback_summary(),
                               messages         = messages               ,
                               token_usage      = token_usage            ,
                               providers        = providers              )