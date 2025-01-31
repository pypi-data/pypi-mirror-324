import torch
import numpy as np
import faiss
import hdbscan

from typing import Union
from .utils import Clusters, max_n_subvectors

def faiss_kmeans(x, d, k):
    kmeans= faiss.Kmeans(d, k, seed= 42)
    x_np= x.cpu().numpy()
    kmeans.train(x_np)
    return kmeans.centroids #(k, d) 

def faiss_knn(x, m, d, k):
    x_np= x.numpy()
    
    nlist= m//39
    if nlist == 0:
        index= faiss.IndexHNSWFlat(d, m)
    else:
        coarse_quantizer= faiss.IndexFlatL2(d)
        if d >= 1024 or m > 10000:
            index= faiss.IndexIVFPQ(
                coarse_quantizer, d, nlist, max_n_subvectors(d), 8
            )
        else:
            index= faiss.IndexIVFFlat(
                coarse_quantizer, d, nlist
            )
        index.train(x_np)
        
    index.add(x_np)
    distances, neighbors= index.search(x_np, k)
    distances_torch = torch.tensor(distances, device=x.device, dtype= x.dtype)
    neighbors_torch = torch.tensor(neighbors, device=x.device, dtype= torch.long)
    return distances_torch, neighbors_torch

def hdbscan_cpu(x):
    clusterer= hdbscan.HDBSCAN()
    x_np= x.numpy()
    labels= clusterer.fit_predict(x_np)
    labels_torch= torch.tensor(labels)
    return labels_torch

def orbit_algorithm(
    entities: torch.Tensor,
    targets: Union[torch.tensor, int],
    pull_strength: float,
    sim_threshold: float,
)-> Clusters:
    """
        stay in orbit, or be lost in space
    """
    m, d= entities.shape

    if isinstance(targets, int):
        targets= faiss_kmeans(entities, d, targets)
        targets= torch.tensor(targets, dtype= entities.dtype)

    targets= targets.to(entities.dtype)
    if targets.dim() == 1:
        targets= targets.unsqueeze(0)
    n, _= targets.shape

    k_core= min( int(np.log(m + n)),  15)
    knn_dist, _= faiss_knn(entities, m, d, k_core + 1)
    core_dist= knn_dist[: , k_core]
    l2_dist= torch.cdist(entities, targets, p=2)  
    core_dist_normalized= (core_dist - core_dist.min() )/ (core_dist.max() - core_dist.min() + 1e-6)
    l2_dist_normalized= l2_dist/ (l2_dist.max() + 1e-6)

    distance_penalty= torch.exp(- core_dist_normalized.unsqueeze(-1))/(1 + l2_dist_normalized)

    entities_normalized= entities/ (entities.norm(dim= -1, keepdim= True) + 1e-6)
    targets_normalized= targets/ (targets.norm(dim= -1, keepdim= True) + 1e-6) 
    similarity= (entities_normalized @ targets_normalized.transpose(-2, -1))
    similarity_adjusted= similarity*distance_penalty

    indices= torch.argmax(similarity_adjusted, dim= -1)

    pull_strength_adjusted= pull_strength*distance_penalty
    pull_strength_adjusted= pull_strength_adjusted.gather(-1, indices.unsqueeze(-1))
    entities_pulled= (1 - pull_strength_adjusted) * entities\
                        + pull_strength_adjusted* targets[indices]

    sim_mask= similarity_adjusted.gather(-1, indices.unsqueeze(-1)).squeeze(-1) >= sim_threshold
    sim_indices= sim_mask.nonzero(as_tuple= True)[0]
    entities_pruned= entities_pulled[sim_mask]
    data_for_clustering= torch.concat([entities_pruned, targets], dim=0)
    labels= hdbscan_cpu(data_for_clustering)

    new_m= entities_pruned.size(0)
    entity_labels = labels[:new_m]
    target_labels= labels[new_m:]
    label_mask= torch.isin(entity_labels, target_labels)
    remaining_indices = sim_indices[label_mask.nonzero(as_tuple=True)[0]]
    _, corrected_labels= torch.unique(entity_labels[label_mask], sorted= True, return_inverse= True)

    return Clusters(
        entities= entities[remaining_indices].cpu().numpy(),
        indices= remaining_indices.cpu().numpy(),
        labels= corrected_labels.cpu().numpy(),
        centroids= targets.cpu().numpy()
    )