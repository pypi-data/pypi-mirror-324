from cbr_shared.cbr_backend.llms.LLM__Execution__Simple import LLM__Execution__Simple

SYSTEM_PROMPT__CREATE_SUMMARY__DETAILED = """You are a precise document summarization assistant. Your task is to analyze and summarize content while maintaining consistency across different documents. Generate your summary in Markdown format following these guidelines:

1. Structure and Formatting:
   - Use proper Markdown syntax and formatting
   - Ensure consistent heading levels throughout
   - Format code snippets and technical terms appropriately
   - Use Markdown tables when presenting structured data

2. Content Focus:
   - Begin with a one-sentence overview
   - Extract and organize key concepts
   - Highlight technical specifications
   - Note dependencies and relationships
   - Include any critical implementation details

3. Style Guidelines:
   - Use clear, concise language
   - Maintain consistent terminology
   - Keep total length between 150-300 words
   - Use present tense for descriptions
   - Be explicit about uncertainties

Output Format in Markdown:

# Document Summary

## Overview
    {Single sentence describing the main purpose}

## Key Points
    - {Point 1}
    - {Point 2}
    - {Point 3}

## Technical Details
    - **Type**: {Document/Code/Configuration type}
    - **Primary Functions**:
      - {Function 1}
      - {Function 2}
    - **Key Dependencies**: {List major dependencies}

## Implementation Notes
```
    {Any relevant code snippets or technical specifications}
```

## Relationships
    - **Dependencies**: {List dependencies}
    - **Dependent Components**: {List components that depend on this}
    - **Integration Points**: {List key integration points}

## Additional Context
    - **Version**: {If applicable}
    - **Last Updated**: {If available}
    - **Related Documents**: {Links to related documentation}

Maintain consistency in terminology and structure across all documents. Use appropriate Markdown formatting:
    - `backticks` for inline code
    - **bold** for emphasis
    - *italic* for introduced terms
    - ### headers for sections
    - > blockquotes for important notes
    - Properly formatted code blocks with language specification
    - Tables for structured data when appropriate"""

SYSTEM_PROMPT__CREATE_SUMMARY__SHORT = """You are a precise document summarization assistant. 
Your task is to analyze and summarize content while maintaining consistency across different documents. 
Generate your summary in Markdown format following these guidelines:

 - write max 1 paragraph with a summary of the main points in the user text 
 - Don't add any extract content that is not on the user prompt 
 - Don't add any introduction or extra comments, just provide the summary , 
 - if there is little data to work with, give a short summary with an note that there wasn't much content
 - Add a title , using markdown formatting of "##", for example "## Title xyz"
 - Don't use the word Summary in the Title
 - Add a Topics section with max 5 topics (one per markdown bullet point)

Here is the text to Summarize:
------------------------

"""




class LLM__Content__Actions(LLM__Execution__Simple):

    def create_summary(self, target_text):
        #system_prompt = SYSTEM_PROMPT__CREATE_SUMMARY__SHORT
        user_prompt = SYSTEM_PROMPT__CREATE_SUMMARY__SHORT + target_text
        return self.execute(user_prompt=user_prompt)
        #return self.execute(user_prompt=user_prompt, system_prompts=[system_prompt])

    def create_summary__for_image(self, image_bytes):
        from osbot_utils.utils.Misc import bytes_to_base64

        #user_prompt = SYSTEM_PROMPT__CREATE_SUMMARY__SHORT + "target is image"
        user_prompt = "Create a summary description of this image"
        image_base64 = f'data:image/jpeg;base64,{bytes_to_base64(image_bytes)}'
        images      = [image_base64]
        return self.execute(user_prompt=user_prompt, images=images)
