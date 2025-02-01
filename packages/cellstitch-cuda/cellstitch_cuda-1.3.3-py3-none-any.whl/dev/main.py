import tifffile
from cellstitch_cuda.pipeline import cellstitch_cuda
from cellstitch_cuda.interpolate import full_interpolate

img = r"E:\1_DATA\Rheenen\tvl_jr\SP8\2024Nov22_SI_1mg_1year_3D_2D-merge\Villus_crops\2024Nov22_SI_1mg_1year_3D_2D-merge-1-1\output.tif"

cellstitch_cuda(img, output_masks=True, verbose=True, seg_mode="nuclei_cells", interpolation=True, n_jobs=-1)

# masks = tifffile.imread(r"E:\1_DATA\Rheenen\tvl_jr\3d stitching\raw4-small\cellstitch_masks.tif")
#
# masks = full_interpolate(masks, anisotropy=4, n_jobs=-1, verbose=True)
#
# tifffile.imwrite(r"E:\1_DATA\Rheenen\tvl_jr\3d stitching\raw4-small\cellstitch_masks_interpolated.tif", masks)
