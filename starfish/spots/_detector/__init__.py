import os
from typing import Type

import click

from starfish.codebook.codebook import Codebook
from starfish.imagestack.imagestack import ImageStack
from starfish.pipeline import AlgorithmBase, PipelineComponent
from starfish.types import Indices
from . import _base
from . import gaussian
from . import pixel_spot_detector
from . import trackpy_local_max_peak_finder


class SpotFinder(PipelineComponent):

    @classmethod
    def _get_algorithm_base_class(cls) -> Type[AlgorithmBase]:
        return _base.SpotFinderAlgorithmBase

    @classmethod
    def _cli_run(cls, ctx, instance):
        output = ctx.obj["output"]
        blobs_stack = ctx.obj["blobs_stack"]
        image_stack = ctx.obj["image_stack"]
        ref_image = ctx.obj["reference_image_from_max_projection"]
        if blobs_stack is not None:
            blobs_stack = ImageStack.from_path_or_url(blobs_stack)  # type: ignore
            blobs_image = blobs_stack.max_proj(Indices.ROUND, Indices.CH)
            #  TODO: this won't work for PixelSpotDectector
            intensities = instance.run(
                image_stack,
                blobs_image=blobs_image,
                reference_image_from_max_projection=ref_image,
            )
        else:
            intensities = instance.run(image_stack)

        # When PixelSpotDetector is used run() returns a tuple
        if isinstance(intensities, tuple):
            intensities = intensities[0]
        intensities.save(output)

    @staticmethod
    @click.group("detect_spots")
    @click.option("-i", "--input", required=True, type=click.Path(exists=True))
    @click.option("-o", "--output", required=True)
    @click.option(
        '--blobs-stack', default=None, required=False, help=(
            'ImageStack that contains the blobs. Will be max-projected across imaging round '
            'and channel to produce the blobs_image'
        )
    )
    @click.option(
        '--reference-image-from-max-projection', default=False, is_flag=True, help=(
            'Construct a reference image by max projecting imaging rounds and channels. Spots '
            'are found in this image and then measured across all images in the input stack.'
        )
    )
    @click.option(
        '--codebook', default=None, required=False, help=(
            'A spaceTx spec-compliant json file that describes a three dimensional tensor '
            'whose values are the expected intensity of a spot for each code in each imaging '
            'round and each color channel.'
        )
    )
    @click.pass_context
    def _cli(ctx, input, output, blobs_stack, reference_image_from_max_projection, codebook):
        print('Detecting Spots ...')
        ctx.obj = dict(
            component=SpotFinder,
            image_stack=ImageStack.from_path_or_url(input),
            output=output,
            blobs_stack=blobs_stack,
            reference_image_from_max_projection=reference_image_from_max_projection,
            codebook=None,
        )

        if codebook is not None:
            ctx.obj["codebook"] = Codebook.from_json(codebook)


SpotFinder._cli_register()
