
# coding: utf-8

# In[16]:


import cv2
from collections import Counter
from sklearn.cluster import KMeans
import webcolors
from PIL import Image
from colormath.color_objects import sRGBColor, LabColor
from colormath.color_conversions import convert_color
from colormath.color_diff import delta_e_cie2000


# In[19]:


class DominantColors:

    CLUSTERS = None
    IMAGE = None
    COLORS = None
    LABELS = None
    
    def __init__(self, image, clusters=3):
        self.CLUSTERS = clusters
        self.IMAGE = image
        
    def dominantColors(self):
    
        # Read image
        img = cv2.imread(self.IMAGE)
        
        #convert to rgb from bgr
        img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
                
        #reshaping to a list of pixels
        img = img.reshape((img.shape[0] * img.shape[1], 3))
        
        #save image after operations
        self.IMAGE = img
        
        #using k-means to cluster pixels
        kmeans = KMeans(n_clusters = self.CLUSTERS)
        kmeans.fit_predict(img)
        
        #the cluster centers are our dominant colors.
        self.COLORS = kmeans.cluster_centers_
        
        #save labels
        self.LABELS = kmeans.labels_
        
        #returning after converting to integer from float
        n = Counter(self.LABELS).most_common(2)
        c = self.COLORS[n[0][0]]
        if closest_colour(c) == 'black':
            n =  n[1][0]
        else :
            n =  n[0][0]
        return self.COLORS.astype(int), n
    
    def rgb_to_hex(self, rgb):
        return '#%02x%02x%02x' % (int(rgb[0]), int(rgb[1]), int(rgb[2]))
    
    def plotClusters(self):
        #plotting 
        fig = plt.figure()
        ax = Axes3D(fig)        
        for label, pix in zip(self.LABELS, self.IMAGE):
            ax.scatter(pix[0], pix[1], pix[2], color = self.rgb_to_hex(self.COLORS[label]))
        plt.show()


# In[20]:


def closest_colour(requested_colour):
    min_colours = {}
    for key, name in webcolors.css3_hex_to_names.items():
        r_c, g_c, b_c = webcolors.hex_to_rgb(key)
        rd = (r_c - requested_colour[0]) ** 2
        gd = (g_c - requested_colour[1]) ** 2
        bd = (b_c - requested_colour[2]) ** 2
        min_colours[(rd + gd + bd)] = name
    return min_colours[min(min_colours.keys())]

def get_colour_name(requested_colour):
    try:
        closest_name = actual_name = webcolors.rgb_to_name(requested_colour)
    except ValueError:
        closest_name = closest_colour(requested_colour)
        actual_name = None
    return actual_name, closest_name


# In[22]:
def createMonocolourImg(colour):
    return Image.new('RGB', (200, 200), color = colour)

def displayColor(img_name, clusters):
    dc = DominantColors(img_name, clusters)
    colors, n = dc.dominantColors()
    
    requested_colour = (colors[n][0], colors[n][1], colors[n][2])
    
    actual_name, closest_name = get_colour_name(requested_colour)

    
    img = createMonocolourImg(requested_colour)
    if(actual_name!=None):
        return actual_name, img, requested_colour
    return closest_name, img, colors


def whichColour(c1,c2,dominants):
    print(dominants)

    bestDelta = 100000000
    bestColor = ""

    c1_rgb = webcolors.name_to_rgb(c1)
    c2_rgb = webcolors.name_to_rgb(c2)
    c1_rgb = sRGBColor(c1_rgb.red, c1_rgb.green, c1_rgb.blue)
    c2_rgb = sRGBColor(c2_rgb.red, c2_rgb.green, c2_rgb.blue)
        

    # Convert from RGB to Lab Color Space
    color1_lab = convert_color(c1_rgb , LabColor);

    # Convert from RGB to Lab Color Space
    color2_lab = convert_color(c2_rgb, LabColor);

    for i in range(len(dominants)):


        rgb = sRGBColor(dominants[i][0], dominants[i][1], dominants[i][2])
        lab = convert_color(rgb, LabColor)
        dominant_color = convert_color(lab, LabColor)
        # Find the color difference
        delta_c1 = delta_e_cie2000(color1_lab, dominant_color);
        delta_c2 = delta_e_cie2000(color2_lab, dominant_color);

        if(bestDelta >= delta_c1):
            bestColor = c1
            bestDelta = delta_c1

        if(bestDelta >= delta_c2):
            bestColor = c2
            bestDelta = delta_c2

    #print("The difference between the 2 colors = " + bestColor +" - "+ str(bestDelta))
    return bestColor




# In[25]:


