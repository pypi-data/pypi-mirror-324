"""_model module provides a wrapper around ESRGan.
"""

import os

import cv2
import numpy as np
from basicsr.archs.rrdbnet_arch import RRDBNet
from basicsr.utils.download_util import load_file_from_url
from gfpgan import GFPGANer
from realesrgan import RealESRGANer
from realesrgan.archs.srvgg_arch import SRVGGNetCompact

from . import _image


RealESRGAN_x4plus = 'RealESRGAN_x4plus'
RealESRNet_x4plus = 'RealESRNet_x4plus'
RealESRGAN_x4plus_anime_6B = 'RealESRGAN_x4plus_anime_6B'
RealESRGAN_x2plus = 'RealESRGAN_x2plus'
RealESR_General_x4_v3 = 'RealESR_General_x4_v3'

models = {
  RealESRGAN_x4plus: {
    'model': RRDBNet(num_in_ch=3, num_out_ch=3, num_feat=64, num_block=23, num_grow_ch=32, scale=4),
    'scale': 4,
    'urls': ['https://github.com/xinntao/Real-ESRGAN/releases/download/v0.1.0/RealESRGAN_x4plus.pth']
  },
  RealESRNet_x4plus: {
    'model': RRDBNet(num_in_ch=3, num_out_ch=3, num_feat=64, num_block=23, num_grow_ch=32, scale=4),
    'scale': 4,
    'urls': ['https://github.com/xinntao/Real-ESRGAN/releases/download/v0.1.1/RealESRNet_x4plus.pth']
  },
  RealESRGAN_x4plus_anime_6B: {
    'model': RRDBNet(num_in_ch=3, num_out_ch=3, num_feat=64, num_block=6, num_grow_ch=32, scale=4),
    'scale': 4,
    'urls': ['https://github.com/xinntao/Real-ESRGAN/releases/download/v0.2.2.4/RealESRGAN_x4plus_anime_6B.pth']
  },
  RealESRGAN_x2plus: {
    'model': RRDBNet(num_in_ch=3, num_out_ch=3, num_feat=64, num_block=23, num_grow_ch=32, scale=2),
    'scale': 2,
    'urls': ['https://github.com/xinntao/Real-ESRGAN/releases/download/v0.2.1/RealESRGAN_x2plus.pth']
  },
  RealESR_General_x4_v3: {
    'model': SRVGGNetCompact(num_in_ch=3, num_out_ch=3, num_feat=64, num_conv=32, upscale=4, act_type='prelu'),
    'scale': 4,
    'urls': [
      'https://github.com/xinntao/Real-ESRGAN/releases/download/v0.2.5.0/realesr-general-wdn-x4v3.pth',
      'https://github.com/xinntao/Real-ESRGAN/releases/download/v0.2.5.0/realesr-general-x4v3.pth'
    ]
  }
}


def upscale(image, model_name, denoise, scale, enhance):
  if model_name == RealESRGAN_x4plus:
    model = RRDBNet(num_in_ch=3, num_out_ch=3, num_feat=64, num_block=23, num_grow_ch=32, scale=4)
    model_scale = 4
    model_urls = ['https://github.com/xinntao/Real-ESRGAN/releases/download/v0.1.0/RealESRGAN_x4plus.pth']
  elif model_name == RealESRNet_x4plus:
    model = RRDBNet(num_in_ch=3, num_out_ch=3, num_feat=64, num_block=23, num_grow_ch=32, scale=4)
    model_scale = 4
    model_urls = ['https://github.com/xinntao/Real-ESRGAN/releases/download/v0.1.1/RealESRNet_x4plus.pth']
  elif model_name == RealESRGAN_x4plus_anime_6B:
    model = RRDBNet(num_in_ch=3, num_out_ch=3, num_feat=64, num_block=6, num_grow_ch=32, scale=4)
    model_scale = 4
    model_urls = ['https://github.com/xinntao/Real-ESRGAN/releases/download/v0.2.2.4/RealESRGAN_x4plus_anime_6B.pth']
  elif model_name == RealESRGAN_x2plus:
    model = RRDBNet(num_in_ch=3, num_out_ch=3, num_feat=64, num_block=23, num_grow_ch=32, scale=2)
    model_scale = 2
    model_urls = ['https://github.com/xinntao/Real-ESRGAN/releases/download/v0.2.1/RealESRGAN_x2plus.pth']
  elif model_name == RealESR_General_x4_v3:
    model = SRVGGNetCompact(num_in_ch=3, num_out_ch=3, num_feat=64, num_conv=32, upscale=4, act_type='prelu')
    model_scale = 4
    model_urls = [
        'https://github.com/xinntao/Real-ESRGAN/releases/download/v0.2.5.0/realesr-general-wdn-x4v3.pth',
        'https://github.com/xinntao/Real-ESRGAN/releases/download/v0.2.5.0/realesr-general-x4v3.pth'
    ]

  model = models[model_name]
  model_path = os.path.join('weights', model_name + '.pth')
  if not os.path.isfile(model_path):
    root_dir = os.path.dirname('/content')
    for url in model['urls']:
      model_path = load_file_from_url(
        url=url, model_dir=os.path.join(root_dir, 'weights'), progress=True, file_name=None)

  dni_weight = None
  if model_name == RealESR_General_x4_v3 and denoise != 1:
    wdn_model_path = model_path.replace('realesr-general-x4v3', 'realesr-general-wdn-x4v3')
    model_path = [model_path, wdn_model_path]
    dni_weight = [denoise, 1 - denoise]

  upsampler = RealESRGANer(
      scale=model['scale'],
      model_path=model_path,
      dni_weight=dni_weight,
      model=model['model'],
      tile=0,
      tile_pad=10,
      pre_pad=10,
      half=False,
      gpu_id=None
  )

  cv_image = np.array(image)
  image = cv2.cvtColor(cv_image, cv2.COLOR_RGBA2BGRA)

  if enhance:
    enhancer = GFPGANer(
      model_path='https://github.com/TencentARC/GFPGAN/releases/download/v1.3.0/GFPGANv1.3.pth',
      upscale=scale,
      arch='clean',
      channel_multiplier=2,
      bg_upsampler=upsampler)
    _, _, image = enhancer.enhance(image,
                                   has_aligned=False,
                                   only_center_face=False,
                                   paste_back=True)
  else:
    image, _ = upsampler.enhance(image, outscale=scale)

  image = cv2.cvtColor(image, cv2.COLOR_BGRA2RGBA)
  return image, _image.dimensions(image)
