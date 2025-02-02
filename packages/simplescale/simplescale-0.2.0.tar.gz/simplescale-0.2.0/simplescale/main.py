"""main module implements a simple scaler using ESRGan and Gradio.
"""

import gradio as gr

from . import _image
from . import _model


def dimensions(image):
  if image is None:
    return ''

  dims = _image.dimensions(image)
  return f'{dims[0]} x {dims[1]}'


def upscale(image, model, denoise, scale, enhance):
  if image is None:
    return None, ''

  image, dims = _model.upscale(image, model, denoise, scale, enhance)
  return image, f'{dims[0]} x {dims[1]}'


def run():
  with gr.Blocks(title='Simple Scale', theme=gr.themes.Base()) as app:
    with gr.Sidebar(label='Options', open=False):
      gr.Markdown('**Options**')
      gr.Markdown('---')
      model = gr.Dropdown(label='Model',
                          choices=[
                            _model.RealESRGAN_x4plus,
                            _model.RealESRNet_x4plus,
                            _model.RealESRGAN_x4plus_anime_6B,
                            _model.RealESRGAN_x2plus,
                            _model.RealESR_General_x4_v3
                          ],
                          value='RealESR_General_x4_v3')
      denoise = gr.Slider(label='Denoise Strength',
                          minimum=0, maximum=1, step=0.1,
                          value=1)
      scale = gr.Slider(label='Scale Factor',
                        minimum=1, maximum=6, step=1,
                        value=2)
      enhance = gr.Checkbox(label='Face Enhancement')
    with gr.Row():
      with gr.Group():
        image = gr.Image(label='Original', show_label=True,
                         container=True,
                         type='pil', sources=['upload'])
        dims = gr.Textbox(label='Dimensions', show_label=False,
                          container=False,
                          interactive=False)
      with gr.Group():
        scaled_image = gr.Image(label='Scaled', show_label=True,
                                container=True,
                                type='pil', sources=['upload'])
        scaled_dims = gr.Textbox(label='Scaled Dimensions', show_label=False,
                                 container=False,
                                 interactive=False)
    with gr.Row():
      button = gr.Button('Upscale')

    image.change(fn=dimensions, inputs=image, outputs=dims)
    button.click(fn=upscale,
                 inputs=[image, model, denoise, scale, enhance],
                 outputs=[scaled_image, scaled_dims])

    app.launch(share=True, debug=True, inline=False)


if __name__ == '__main__':
  run()
