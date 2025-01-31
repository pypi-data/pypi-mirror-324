import numpy as np
import networkx as nx
from scipy.spatial.distance import canberra
from scipy.special import rel_entr
from sklearn.preprocessing import MinMaxScaler


def euclidean_distance(p1, p2):
    ''' 
    Euclidean distance.

    Args:
      p1 (float): pixel value 1
      p2 (float): pixel value 2

    Returns:
      float: Euclidean distance between p1 and p2
    '''
    return np.sqrt(np.sum((p1 - p2) ** 2))

def minkowski_distance(p1, p2, r):
    ''' 
    Minkowski distance.

    Args:
      p1 (float): pixel value 1
      p2 (float): pixel value 2

    Returns:
      float: Minkowski distance between p1 and p2
    '''
    return np.power(np.sum(np.power(np.abs(p1 - p2), r)), 1/r)

def chebyshev_distance(p1, p2):
    ''' 
    Chebyshev distance.

    Args:
      p1 (float): pixel value 1
      p2 (float): pixel value 2

    Returns:
      float: Chebyshev distance between p1 and p2
    '''
    return np.max(np.abs(p1 - p2))

def jensen_shannon_divergence(X, Y):
    ''' 
    Jensen-Shannon Divergence.

    Args:
      p1 (float): pixel value 1
      p2 (float): pixel value 2

    Returns:
      float: Jensen-Shannon Divergence between p1 and p2
    '''
    M = 0.5 * (X + Y)
    return np.sqrt(np.abs(0.5 * (rel_entr(X, M).sum() + rel_entr(Y, M).sum())))

def gaussian_similarity(a, b, sigma):
  ''' 
  Gaussian similarity.

  Args:
    p1 (float): pixel value 1
    p2 (float): pixel value 2

  Returns:
    float: Gaussian similarity between p1 and p2
  '''
  gaussian_similairity_score = np.exp(-((a - b)**2) / (2 * sigma**2))
  return gaussian_similairity_score

# Canberra Distance
def canberra_distance(X, Y):
    ''' 
    Canberra distance.

    Args:
      p1 (float): pixel value 1
      p2 (float): pixel value 2

    Returns:
      float: Canberra distance between p1 and p2
    '''
    return canberra(X, Y)

def apply_similarity(type,image, x1, y1, x2, y2, sigma=None):
  ''' 
  Apply chosen similarity to image.

  Args:
    type (str): Similarity type name
    image (np.array): input image
    x1 (int): x coordinates pixel 1
    y1 (int): y coordinates pixel 1
    x2 (int): x coordinates pixel 2
    y2 (int): y coordinates pixel 2

  Returns:
    weight (float): Edge weight
  '''
  if type=='Gaussian':
    weight = -1*(1-gaussian_similarity(image[x1,y1],image[x2,y2], sigma))
  elif type=='Euclidean':
    weight = (1-euclidean_distance(image[x1,y1],image[x2,y2]))
  elif type=='Minkowski':
    weight = (1-minkowski_distance(image[x1,y1].reshape(1),image[x2,y2].reshape(1),3))
  elif type=='Chebyshev':
    weight = (1-chebyshev_distance(image[x1,y1].reshape(1),image[x2,y2].reshape(1)))
  elif type=='Jensen':
    weight = (1-jensen_shannon_divergence(np.abs(image[x1,y1]).reshape(1),np.abs(image[x2,y2]).reshape(1)))
  elif type=='Canberra':
    weight = (1-canberra_distance(image[x1,y1].reshape(1),image[x2,y2].reshape(1)))
  return weight



def image_to_grid_graph(gray_img, type = 'Gaussian', sigma = None):
  """
  Convert a grayscale image to a grid graph with Gaussian similarity as edge weights.

  Args:
    gray_img (numpy.ndarray): Grayscale image.
    type (str): Similarity type name
    sigma (float): Parameter for Gaussian similarity.

  Returns:
    list: List of edges with weights for the graph.
  """
  h, w = gray_img.shape  
  if sigma is None and type=='Gaussian': # Calculate std as the data std unless stated otherwise
    data = gray_img.flatten()
    sigma = np.std(data)
  nodes = np.zeros((h*w, 1))
  edges = []
  nx_elist = []
  # Calculate similarity between neighboring pixels
  for i in range(h*w):
    x, y = i//w, i%w
    nodes[i] = gray_img[x,y]
    if x > 0:
      j = (x-1)*w + y
      weight = apply_similarity(type,gray_img, x,y, x-1, y,sigma)
      edges.append((i, j, weight))
      nx_elist.append(((x,y),(x-1,y),np.round(weight,2)))
    if y > 0:
      j = x*w + y-1
      weight = apply_similarity(type,gray_img, x,y, x, y-1,sigma)
      edges.append((i, j, weight))
      nx_elist.append(((x,y),(x,y-1),weight))
  w_list = [e[2] for e in edges]
  # Normalize weights to the [-1,1] domain
  scaler = MinMaxScaler((-1,1))
  w_list_scaled = scaler.fit_transform(np.array(w_list).reshape(-1,1)).flatten()
  normalized_nx_elist = []
  for i in range(len(nx_elist)):
    normalized_nx_elist.append((nx_elist[i][0], nx_elist[i][1], w_list_scaled[i]))
  return normalized_nx_elist


def create_graph(data_small, type = 'Gaussian', sd_prop = 0.3):
  '''
  Function to create the Graph encoding the image, where the edges are calculated using the Gaussian similarity between pixels.
  Here we perform hyperparameter optimization for the stadard deviation, ensuring that  the proportion of the two tails of the weights distribution is around 0.17. 

  Args:
    data_small (np.array): input data
    type (str): Similarity type name

  Returns:
    G (networkx.graph): Graph encoding the image to be segmented.
  '''
  x = data_small.flatten()
  if type=='Gaussian':
    normalized_nx_elist = image_to_grid_graph(data_small, sigma=sd_prop*np.std(x)) 
    G = nx.grid_2d_graph(data_small.shape[0], data_small.shape[1])
    G.add_weighted_edges_from(normalized_nx_elist)
  else: # For other similarity measures there is no hyperparameter search
    normalized_nx_elist = image_to_grid_graph(data_small, type)
    G = nx.grid_2d_graph(data_small.shape[0], data_small.shape[1])
    G.add_weighted_edges_from(normalized_nx_elist)
    std_p =1
  return G
