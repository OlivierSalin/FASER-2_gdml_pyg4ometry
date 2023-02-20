import numpy as np
import pyg4ometry
import pyg4ometry.geant4 as g4
import pyg4ometry.gdml as gdml

def create_calorimeter_dual_readout_geometry():
    # Constants
    reg = pyg4ometry.geant4.Registry()
    world_box = pyg4ometry.geant4.solid.Box("world_box",10000, 10000, 20000, reg, "mm")
    world_lv = pyg4ometry.geant4.LogicalVolume(world_box, "G4_Galactic", "world_lv", reg)

    t_diameter=60
    Calo_x = 2000
    Calo_y = 2000
    EM_calo_z = 370
    Had_Calo_z = 2500
    tube_outer_diameter = gdml.Constant("tube_outer_diameter", t_diameter, reg)
    tube_length = gdml.Constant("tube_length", Calo_x, reg)
    
    Calorimeter_x = gdml.Constant("Calorimeter_x", Calo_x, reg)
    Calorimeter_y = gdml.Constant("Calorimeter_y", Calo_y, reg)
    EM_Calorimeter_z = gdml.Constant("EM_Calorimeter_z", EM_calo_z, reg)
    Had_Calorimeter_z = gdml.Constant("Had_Calorimeter_z", Had_Calo_z, reg)


    Brass = pyg4ometry.geant4.MaterialCompound("Brass", 8.44, 2, reg)
    Brass.add_material(pyg4ometry.geant4.MaterialPredefined("G4_Cu"), 0.3)
    Brass.add_material(pyg4ometry.geant4.MaterialPredefined("G4_Zn"), 0.7)

    # Brass Capillary Tube
    tube = g4.solid.Tubs("tube", 0 , tube_outer_diameter / 2, tube_length , 0, 2 * np.pi, reg, "mm", "rad")
    tube_lv = g4.LogicalVolume(tube, "G4_Cu", "tube_lv", reg)
    tube_hor_lv = g4.LogicalVolume(tube, "G4_Zn", "tube_hor_lv", reg)

    tube_had = g4.solid.Tubs("tube_had", 0 , tube_outer_diameter / 2,Had_Calorimeter_z  , 0, 2 * np.pi, reg, "mm", "rad")
    
    tube_had_lv = g4.LogicalVolume(tube_had, "G4_Si", "tube_had_lv", reg)
    # tube_pv = g4.PhysicalVolume([0, 0, 0], [0, 0, 0], tube_lv, "tube_pv", world_lv, reg)

    n_tubes_col=int(Calo_x/t_diameter)
    n_rows=int(0.5*EM_calo_z/t_diameter)+1

    for k in range(n_rows):
        for c in range(n_tubes_col):
            Tube_vert_PV=pyg4ometry.geant4.PhysicalVolume([np.pi/2,0,0],[-Calorimeter_x*0.5+c*tube_outer_diameter,0, -0.5*EM_Calorimeter_z +2*k*tube_outer_diameter], tube_lv,"Tube_vert_PV"+ str(k)+","+str(c),world_lv,reg)
            Tube_hor_PV=pyg4ometry.geant4.PhysicalVolume([0,np.pi/2,0],[0,-Calorimeter_x*0.5+c*tube_outer_diameter, -0.5*EM_Calorimeter_z+(2*k+1)*tube_outer_diameter], tube_hor_lv,"Tube_hor_PV"+ str(k)+","+str(c),world_lv,reg)

    n_rows2=int(EM_calo_z/t_diameter)+1        
    for k in range(n_tubes_col):
        for c in range(n_tubes_col):
            Tube_had_PV=pyg4ometry.geant4.PhysicalVolume([0,0,np.pi/2],[-Calorimeter_x*0.5+c*tube_outer_diameter,-Calorimeter_x*0.5+k*tube_outer_diameter,0.5*tube_outer_diameter+ 0.5*EM_Calorimeter_z+Had_Calorimeter_z*0.5], tube_had_lv,"Tube_had_PV"+ str(k)+","+str(c),world_lv,reg)
            

    square = pyg4ometry.geant4.solid.Box("square", Calorimeter_x, Calorimeter_y, EM_Calorimeter_z, reg, "mm")
    square_lv = pyg4ometry.geant4.LogicalVolume(square, "G4_Galactic", "square_lv", reg)
    #square_pv=pyg4ometry.geant4.PhysicalVolume([0,0,0],[0,0, 0], square_lv,"square_pv",world_lv,reg)

    reg = pyg4ometry.geant4.Registry()
    reg.setWorld(world_lv)

    # v = pyg4ometry.visualisation.VtkViewer()
    # v.addLogicalVolume(world_lv)
    # v.addAxes(100)
    # v.view()


    # v_c = pyg4ometry.visualisation.VtkViewerColoured(defaultColour="random")
    v_c = pyg4ometry.visualisation.VtkViewerColoured(materialVisOptions={"G4_Cu":[1,0,0],"G4_Zn":[0,0,1],"G4_Si":[0.3,0.3,0.3]})
    v_c.addLogicalVolume(world_lv)
    v_c.setOpacity(0.92)
    #v_c.addAxes(100)
    # v_c.exportOBJScene('FASER2_obj')
    v_c.view()

if __name__ == "__main__":
    create_calorimeter_dual_readout_geometry()

