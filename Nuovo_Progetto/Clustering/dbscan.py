"""
Questo file contiene l'implementazione di DBSCAN, algoritmo di clustering.
"""

import sys
sys.path.append('../')
import numpy as np 
from Util.matrix_functions import extract_neighborhood,extract_sub_matrix,binarize_matrix



def __expand_cluster(current_cluster_label,point,neighbors,clusters,visited_points,points_class,points_labels,eps,min_pts):
    clusters[current_cluster_label].append(point)
    points_labels[point] = current_cluster_label

    for point_neigh in neighbors[point]:
        if visited_points[point_neigh] == 0:
            visited_points[point_neigh] = 1
            neighs = neighbors[point_neigh]
            if points_class[point_neigh] == 'core':
                for n in neighs:
                    neighbors[point].append(n)
            if points_labels[point_neigh] == -1:
                points_labels[point_neigh] = current_cluster_label
                clusters[current_cluster_label].append(point_neigh)



def DBSCAN(M,points_dict,eps,min_pts):
    """
    DBSCAN è un algoritmo di clustering basato su densità.
    Data lo stato attuale dell'ambiente, rappresentato tramite matrice,
    suddivide gli agenti in vari clusters. 
    I parametri principali dell'algoritmo sono:
        - eps : Raggio del vicinato da utilizzare
        - min_pts : Numero minimo di agenti che devono essere presenti nel vicinato, compreso l'agente su cui è centrato il vicinato,
                    affinché l'agente possa essere classificato come un CORE point.
    """
    current_cluster_label = -1

    visited_points = {}

    points_class = {}
    points_label = {}
    clusters = {}
    neighbors = {}
    
    for point,position in points_dict.items():
        
        visited_points[point] = 0
        points_label[point] = -1

        neighbors[point] = []

        M_neigh = extract_neighborhood(M,eps,position[0],position[1])
        n_points = 1

        for row in M_neigh:
            for element in row:
                if element > 0:
                    neighbors[point].append(element)
                    n_points += 1
        
        if n_points >= min_pts:
            points_class[point] = 'core'
        else:
            points_class[point] = 'noise'
 
    for point in visited_points.keys():
        if visited_points[point] == 0:
            visited_points[point] = 1
            if points_class[point] == 'core':
                current_cluster_label += 1
                clusters[current_cluster_label] = []
                __expand_cluster(current_cluster_label, point,neighbors,clusters,visited_points,points_class,points_label, eps,min_pts)
              
    
    for point in points_label.keys():
        if points_label[point] == -1:
            current_cluster_label += 1
            points_label[point] == current_cluster_label
            clusters[current_cluster_label] = [point]

    mean_cluster_size = 0
    n_clusters = 0
    for p in clusters:
        mean_cluster_size += len(clusters[p])
        n_clusters += 1

    mean_cluster_size /= n_clusters
    
    return clusters,np.around(mean_cluster_size,3)
  





