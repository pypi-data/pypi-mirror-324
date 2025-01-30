import gradio as gr
import ai_gradio


gr.load(
    name='perplexity:sonar-reasoning',
    src=ai_gradio.registry,
    coder=True
).launch()
