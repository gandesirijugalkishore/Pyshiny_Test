import os
import subprocess
import time
from shiny import App, ui, reactive
import mesop as me

# ==============================================
# Mesop App
# ==============================================
@me.page(path="/mesop")
def mesop_app():
    me.text("Hello from Mesop!")
    me.button("Click Me", on_click=lambda: me.text("Button clicked!"))

# ==============================================
# PyShiny App
# ==============================================
# Define the UI for the Shiny app
app_ui = ui.page_fluid(
    ui.h1("PyShiny App with Embedded Mesop App"),
    ui.p("This is a PyShiny app running a Mesop app inside an iframe."),
    # Use ui.HTML to create a custom iframe
    ui.HTML('<iframe src="/mesop" height="400px" width="100%"></iframe>'),
    ui.input_slider("slider", "Slider", min=0, max=100, value=50),
    ui.output_text("slider_value")
)

# Define the server logic for the Shiny app
def server(input, output, session):
    @reactive.Calc
    def slider_value():
        return f"Slider value: {input.slider()}"

    @output
    @ui.render_text
    def slider_value():
        return slider_value()

# ==============================================
# Run Both Apps Together
# ==============================================
if __name__ == "__main__":
    # Start the Mesop app in a separate process
    mesop_process = subprocess.Popen(["mesop", "run", __file__])

    # Give the Mesop app some time to start
    time.sleep(2)

    # Run the PyShiny app
    app = App(app_ui, server)
    app.run()

    # Terminate the Mesop process when the PyShiny app exits
    mesop_process.terminate()