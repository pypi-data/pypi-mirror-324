import scanpy as sc
import matplotlib.pyplot as plt
from matplotlib.colors import ListedColormap

def kde_results(adata_tmp, score_name, plot_masks=True, plot_enrichment=True, if_filtered=False, figsize=(10, 10), spot_size=50):
    """
    Plot binary_mask and mask on the first row, enrichment scores on the second row.

    Parameters
    ----------
    adata_tmp : AnnData
        AnnData object containing the data and masks.
    score_name : str
        The gene or feature name used for plotting enrichment scores.
    plot_masks : bool, optional (default=True)
        Whether to plot binary_mask and mask.
    plot_enrichment : bool, optional (default=True)
        Whether to plot the enrichment score.
    if_filtered : bool, optional (default=False)
        If True and 'filtered_coords' exists, both original and filtered enrichment scores will be plotted.
    figsize : tuple, optional (default=(10, 10))
        Size of the figure.
    spot_size : int, optional (default=50)
        Size of the points in spatial plots.
    """

    num_rows = 2 
    num_cols = 2 

    fig, axes = plt.subplots(num_rows, num_cols, figsize=figsize)

    if num_rows == 1:
        axes = [axes]  
    elif num_cols == 1:
        axes = [[ax] for ax in axes]  

    if plot_enrichment:
        if if_filtered and 'filtered_coords' in adata_tmp.obs:
            filtered_adata = adata_tmp[adata_tmp.obs['filtered_coords']]
            
            sc.pl.spatial(adata_tmp, color=score_name, ax=axes[1][0], show=False, spot_size=spot_size)
            axes[0][0].set_title("Original Enrichment Score")

            sc.pl.spatial(filtered_adata, color=score_name, ax=axes[1][1], show=False, spot_size=spot_size)
            axes[0][1].set_title("Filtered Enrichment Score")
        else:
            sc.pl.spatial(adata_tmp, color=score_name, ax=axes[1][0], show=False, spot_size=spot_size)
            axes[0][0].set_title("Enrichment Score")
            axes[0][1].axis("off")

    if plot_masks:
        if "binary_mask" not in adata_tmp.obsm or "mask" not in adata_tmp.obsm:
            raise ValueError("binary_mask or mask is not stored in adata_tmp.obsm!")

        binary_mask = adata_tmp.obsm["binary_mask"]
        mask = adata_tmp.obsm["mask"]

        axes[1][0].matshow(binary_mask, cmap=ListedColormap(['silver', 'indianred']))
        axes[1][0].set_title("Binary Mask")

        axes[1][1].matshow(mask, cmap=ListedColormap(['silver', 'indianred']))
        axes[1][1].set_title("Mask")

    plt.tight_layout()
    plt.show()
