from setuptools import setup, find_packages
from torch.utils.cpp_extension import BuildExtension, CUDAExtension

setup(
    name='deep_hough',
    version='0.1.0',
    packages=find_packages(),
    requires=[
      "torch"
    ],
    ext_modules=[
        CUDAExtension('deep_hough', [
            'deep_hough_cuda.cpp',
            'deep_hough_cuda_kernel.cu',
        ],
        extra_compile_args={'cxx': ['-g'], 'nvcc': ['-arch=sm_60']})
    ],
    cmdclass={
        'build_ext': BuildExtension
    })
