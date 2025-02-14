from shiny import App, ui, reactive, render
from google.cloud import bigquery
from google.genai import Client
from google.genai.types import GenerateContentConfig

BIGQUERY_DATASET_ID = "thelook_ecommerce"
MODEL_ID = "gemini-1.5-pro"
LOCATION = "us-central1"

app_ui = ui.page_fillable(
    ui.panel_title("SQL Talk with BigQuery (Mock UI)"),
    ui.markdown(
        """
        ## Sample Questions
        - What is the total revenue for the last quarter?
        - How many users signed up in the last month?
        - What are the top 5 products by sales?
        """
    ),
    ui.chat_ui("chat"),
    fillable_mobile=True,
)

welcome = ui.markdown(
    """
    Ask me about information in the database...
    """
)

def server(input, output, session):
    chat = ui.Chat(id="chat", messages=[welcome])
    client = Client()

    @chat.on_user_submit
    async def _():
        user_prompt = chat.user_input()

        if user_prompt: # Check for empty input
            await chat.append_message({"author": "user", "content": user_prompt})

            prompt = user_prompt + """
                Please give a concise, high-level summary followed by detail in
                plain language about where the information in your response is
                coming from in the database. Only use information that you learn
                from BigQuery, do not make up information.
                """

            response = client.generate_content(
                model=MODEL_ID,
                config=GenerateContentConfig(temperature=0),
                prompt=prompt
            )

            gemini_response = response.candidates[0].content

            await chat.append_message({"author": "ai", "content": gemini_response})
            chat.clear_user_input()  # Clear input box

app = App(app_ui, server)