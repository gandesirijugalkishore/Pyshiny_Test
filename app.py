from shiny import App, ui, reactive, Session

# Define the UI
app_ui = ui.page_fillable(
    ui.panel_title("Dynamic Button Interaction"),
    ui.chat_ui("chat"),
    ui.tags.script(
        """
        Shiny.addCustomMessageHandler('bind_event', function(data) {
            let btn = document.getElementById(data.button_id);
            if (btn) {
                btn.onclick = function() {
                    console.log('Button clicked:', data.button_id);
                    Shiny.setInputValue(data.button_id, Math.random(), {priority: 'event'});
                };
            }
        });
        """
    ),
    fillable_mobile=True,
)

def server(input, output, session: Session):
    chat = ui.Chat(id="chat")

    @chat.on_user_submit
    async def _():
        user_message = chat.user_input().strip()
        # button_id = f"simple_button_{user_message.replace(' ', '_')}"
        like_button_id = f"like_button_{user_message.replace(' ', '_')}"
        dislike_button_id = f"dislike_button_{user_message.replace(' ', '_')}"

        await chat.append_message(ui.HTML(f"""
            <button id="{like_button_id}" class="btn btn-success">👍 Like</button>
            <button id="{dislike_button_id}" class="btn btn-danger">👎 Dislike</button>
        """))
         # Dynamically bind the buttons
        await session.send_custom_message("bind_event", {"button_id": like_button_id})
        await session.send_custom_message("bind_event", {"button_id": dislike_button_id})

        # Reactive handler for button clicks
        @reactive.Effect
        @reactive.event(input[like_button_id])
        def handle_click():
            message = f"Button clicked for message: '{user_message}'"
            print(message)
            # Show notification
            ui.notification_show(message, duration=5)

app = App(app_ui, server, debug=True)
