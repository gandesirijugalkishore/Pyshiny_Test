from shiny import App, ui, reactive, render
import httpx

# Define the user interface
app_ui = ui.page_fluid(
    ui.layout_sidebar(
        ui.sidebar(
            ui.h3("Select Agent"),
            ui.input_select(
                "agent", "Choose an agent to chat with:",
                choices=["PSUMS Agent", "Front Desk Agent"],
                selected="PSUMS Agent"
            ),
            style="height: 100px;"  # Sidebar is static, no scrolling
        ),
        ui.card(
            ui.h3("Chat Area"),
            ui.output_text("selected_agent_heading"),
            ui.chat_ui(id="my_chat"),
            style="overflow-y: auto; height: 100vh; padding: 10px; border: 1px solid #ccc;"
        )
    )
)

# Define the server logic
def server(input, output, session):
    chat_psums = ui.Chat(id="chat_psums")
    chat_frontdesk = ui.Chat(id="chat_frontdesk")
    fastapi_url = "http://127.0.0.1:8000/"  # FastAPI backend URL

    @reactive.Calc
    def current_chat():
        """Switch between chats based on selected agent."""
        if input.agent() == "PSUMS Agent":
            return chat_psums
        else:
            return chat_frontdesk

    @reactive.Effect
    def update_chat():
        """Handle user submissions and provide responses dynamically."""
        current = current_chat()

        @current.on_user_submit
        async def _():
            # Get messages currently in the chat
            messages = current.messages()
            if not messages:
                return
            user_message = messages[-1]["content"]  # Get the last user message

            # Send user message to FastAPI backend and get a response
            async with httpx.AsyncClient() as client:
                response = await client.post(f"{fastapi_url}/process", json={"message": user_message})
                if response.status_code == 200:
                    response_message = response.json().get("reply", "No response from server.")
                    # Append the response into the chat
                    await current.append_message({"role": "system", "content": response_message})
                else:
                    await current.append_message({"role": "system", "content": "Error communicating with backend."})

    @output
    @render.text
    def selected_agent_heading():
        """Display the selected agent."""
        return f"Chatting with {input.agent()}"

# Create the app instance
app = App(app_ui, server)
