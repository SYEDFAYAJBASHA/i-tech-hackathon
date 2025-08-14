# Gradio interface
interface = gr.Interface(
    fn=process_file,
    inputs=gr.File(label="Upload File"),
    outputs=[gr.Image(label="Masked Output"), gr.Textbox(label="Redaction Log")],
    title="Masking Tool",
    description="Upload your file (.png, .jpg, .jpeg, .pdf, or .txt) to mask sensitive information."
)

interface.launch(share=True)