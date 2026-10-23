import verity_x3p
import numpy as np
import pyvista as pv

def load_x3p(file_path):
    surface = verity_x3p.read_x3p(file_path)#read file path inputed by user

    return surface


def show_metadata(surface):
    print("--- Surface Metadata ---")
    print("X points:", surface.nx)
    print("Y points:", surface.ny)
    print("X increment:", surface.increment_x)
    print("Y increment:", surface.increment_y)
    print("Z type:", surface.z_type)
    print("Feature type:", surface.feature_type)
    print("Creator:", surface.creator)
    print("Manufacturer:", surface.manufacturer)
    print("Comment:", surface.comment)
    print("Revision:", surface.revision)

def plot_x3p(surface, z_scale=1):

    data = surface.data
    display_data = data * z_scale #adjust z_scale

    ny, nx = data.shape # (1024,7040)
    dx = surface.increment_x #increment values
    dy = surface.increment_y

    x = np.arange(nx) * dx #create evenly spaced 1D array, mult by dx to form physical values
    y = np.arange(ny) * dy

    X, Y = np.meshgrid(x, y) #determine (Xij,Yij,Zij)

    grid = pv.StructuredGrid(X, Y, display_data)

    plotter = pv.Plotter()
    outline = grid.outline()

    plotter.add_mesh(
        grid,#contain surface geo(look above)
        scalars=data.ravel(order="F"),#values for coloring using Fortran ordering
        cmap="viridis",#color map
        show_edges=False,#dont show ever outline
        scalar_bar_args={"title": "Surface Height"}#color height bar
    )
    
      
    def update_z_scale(value):
      new_z = data * value #updated zval. in ner array
      grid.points[:, 2] = new_z.ravel(order="F")#[every point, column]
  
      
      #use 8 points to continuously update the box outline
      outline.points[0:4,2] = new_z.min()#bottom 4 points since shape is (8,3)
      outline.points[4:8,2] = new_z.max()#top 4 points
      plotter.remove_bounds_axes()
      plotter.show_bounds(mesh=grid,xtitle="X(m)",
      ytitle="Y(m)",ztitle="Z(scaled)",
      fmt="%.0e")
      

    plotter.add_slider_widget(
    update_z_scale,#call back function 
    rng=[1, 50],#slider scale(can be adjusted of course)
    value=z_scale,
    title="Z Scale",pointa=(.95,.3),pointb=(0.95,0.9)
    )

    plotter.add_mesh(
        outline,#8 corner points and lines
        color="black",
        line_width=2
    )

    plotter.add_axes(
        xlabel="X",
        ylabel="Y",
        zlabel="Z"
    )
    plotter.show_bounds(xtitle="X(m)",
    ytitle="Y(m)",ztitle="Z(scaled)",fmt="%.0e")
    plotter.add_text("Surface Visualization",
    position='upper_edge')
    plot = plotter.show()
    return plot
    
def view_x3p(file_path, metadata=False, plot=True, z_scale=1):
    surface = load_x3p(file_path)

    if metadata == True:
        show_metadata(surface)

    if plot == True:
        plot_x3p(surface, z_scale=z_scale)
    
  
  
