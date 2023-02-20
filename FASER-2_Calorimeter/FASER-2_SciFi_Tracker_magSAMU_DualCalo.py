import pyg4ometry
import numpy as _np
import pyg4ometry.geant4 as g4
import pyg4ometry.gdml as gdml

# set the number of polygon points on cylinders to be 2x the 16 default
#pyg4ometry.config.SolidDefaults.Tubs.nslice = 32
#pyg4ometry.config.SolidDefaults.CutTubs.nslice = 32

def SciFiTracker(vis= False):
    reg = pyg4ometry.geant4.Registry()


    d_hor_vert = pyg4ometry.gdml.Constant("d_hor_vert","100",reg,True)
    d_layers = pyg4ometry.gdml.Constant("d_layers","500",reg,True)
    #d_stream = pyg4ometry.gdml.Constant("d_stream","6500",reg,True)

    d1_us = pyg4ometry.gdml.Constant("d1_us","10000",reg,True)
    d1_ds = pyg4ometry.gdml.Constant("d1_ds","18000",reg,True)



    
    twopi  = pyg4ometry.gdml.Constant("twopi", "2.0*pi", reg)
    halfpi = pyg4ometry.gdml.Constant("halfpi", "0.5*pi", reg)
    offset_angle = pyg4ometry.gdml.Constant("offset_angle","10",reg,True)
    safety = pyg4ometry.gdml.Constant("safety", 1e-3, reg)
    constants = {"twopi" : twopi,
                 "safety": safety,
                 "halfpi": halfpi}



    worldSolid = pyg4ometry.geant4.solid.Box("world_solid",100000,100000,100000,reg,"mm")
    worldLV = pyg4ometry.geant4.LogicalVolume(worldSolid,"G4_Galactic","worldLV",reg)
    

    #tiltAngleRad = pyg4ometry.transformation.deg2rad(tiltAngleDeg)

    #SciFi_Downstream_Av = pyg4ometry.geant4.AssemblyVolume("SciFi_Downstream_Av",reg,True)

    SF_LV = SciFiTrackerLayer(reg = reg)
    SciFiLv_vert_us=SF_LV[0]
    SciFiLv_vert_ds=SF_LV[1]
    SciFiLv_hor=SF_LV[2]
    Fiberm=SF_LV[3]

#upstream
#     nLayer_us = 3
#     for k in range(0,nLayer_us):
#         SciFi_Trk_us_vertPV = pyg4ometry.geant4.PhysicalVolume([0,0,((-1)**k)*_np.pi/180],[0,0, d1_us+k*d_layers], SciFiLv_vert_us,"SciFi_Trk_us_vertPV"+str(k),worldLV,reg)
#         SciFi_Trk_us_horizPV = pyg4ometry.geant4.PhysicalVolume([0,0,0],[0,0, d1_us+k*d_layers+d_hor_vert], SciFiLv_hor,"SciFi_Trk_us_horizPV"+ str(k),worldLV,reg)



# #downstream
#     nLayer_ds = 3
#     for j in range(0,nLayer_ds):
#         SciFi_Trk_ds_vertPV = pyg4ometry.geant4.PhysicalVolume([0,0,((-1)**j)*_np.pi/180],[0,0, d1_ds+j*d_layers], SciFiLv_vert_ds,"SciFi_Trk_ds_vertPV"+str(j),worldLV,reg)
#         SciFi_Trk_ds_horizPV = pyg4ometry.geant4.PhysicalVolume([0,0,0],[0,0, d1_ds+j*d_layers+d_hor_vert], SciFiLv_hor,"SciFi_Trk_ds_horizPV"+ str(j),worldLV,reg)



#Magnet
    # Define the constants
    z_mag = pyg4ometry.gdml.Constant("z_mag", 15000, reg)
    coil_inner_diameter = pyg4ometry.gdml.Constant("coil_inner_diameter", 2350, reg)
    coil_outer_diameter = pyg4ometry.gdml.Constant("coil_outer_diameter", 2710, reg)
    coil_z = pyg4ometry.gdml.Constant("coil_z", 200, reg)
    gap = pyg4ometry.gdml.Constant("gap", 1000, reg)
    yoke_x = pyg4ometry.gdml.Constant("yoke_x", 5000, reg)
    yoke_y = pyg4ometry.gdml.Constant("yoke_y", 800, reg)
    yoke_z = pyg4ometry.gdml.Constant("yoke_z", 4000, reg)
    yoke_side_x = pyg4ometry.gdml.Constant("yoke_side_x", 600, reg)
    yoke_side_y = pyg4ometry.gdml.Constant("yoke_side_y", 1000, reg)
    yoke_side_z = pyg4ometry.gdml.Constant("yoke_side_z", 4000, reg)


    
    # Create the coil cylinder
    nbti = pyg4ometry.geant4.MaterialCompound("nbti", 5.7, 2, reg)
    nbti.set_state("solid")
    nbti.add_material(pyg4ometry.geant4.MaterialPredefined("G4_Sn"), 0.3)
    nbti.add_material(pyg4ometry.geant4.MaterialPredefined("G4_Nb"), 0.7)
    coil_cylinder = pyg4ometry.geant4.solid.Tubs("coil_cylinder", 0, 0.5 * coil_outer_diameter , coil_z , 0, 2 * _np.pi, reg, "mm")


    coil_lv = pyg4ometry.geant4.LogicalVolume(coil_cylinder, "G4_Nb", "coil_lv", reg)
    
    # Create the iron yoke box
    yoke_box_main = pyg4ometry.geant4.solid.Box("yoke_box_main",  yoke_x , yoke_y ,  yoke_z, reg, "mm")
    yoke_main_lv = pyg4ometry.geant4.LogicalVolume(yoke_box_main, "G4_Fe", "yoke_main_lv", reg)

    yoke_box_side = pyg4ometry.geant4.solid.Box("yoke_box_side",  yoke_side_x , yoke_side_y ,  yoke_side_z, reg, "mm")
    yoke_side_lv = pyg4ometry.geant4.LogicalVolume(yoke_box_side, "G4_Fe", "yoke_side_lv", reg)
    
    # Place the coil inside the yoke
    # coil1_pv1 = pyg4ometry.geant4.PhysicalVolume([0.5*_np.pi, 0, 0], [0, 0.5*gap-0.5*coil_z, z_mag], coil_lv, "coil_pv1", worldLV, reg)
    # coil_pv2 = pyg4ometry.geant4.PhysicalVolume([0.5*_np.pi, 0, 0], [0, -0.5*gap+0.5*coil_z, z_mag], coil_lv, "coil_pv2", worldLV, reg)
    # yoke_main_pv1 = pyg4ometry.geant4.PhysicalVolume([0, 0, 0], [0,0.5* (gap+yoke_y), z_mag], yoke_main_lv, "yoke_main_pv1", worldLV, reg)
    # yoke_main_pv2 = pyg4ometry.geant4.PhysicalVolume([0, 0, 0], [0, -0.5*(gap+yoke_y), z_mag], yoke_main_lv, "yoke_main_pv2", worldLV, reg)

    # yoke_side_pv1 = pyg4ometry.geant4.PhysicalVolume([0, 0, 0], [0.5*yoke_x-0.5*yoke_side_x, 0, z_mag], yoke_side_lv, "yoke_side_pv1", worldLV, reg)
    # yoke_side_pv2 = pyg4ometry.geant4.PhysicalVolume([0, 0, 0], [-0.5*yoke_x+0.5*yoke_side_x, 0, z_mag], yoke_side_lv, "yoke_side_pv2", worldLV, reg)

    # #CALO



    #DualCalo
    z_Calo_EM = pyg4ometry.gdml.Constant("z_Calo_EM","21000",reg,True)

    t_diameter=40
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
    tube = g4.solid.Tubs("tube", 0 , tube_outer_diameter / 2, tube_length , 0, 2 * _np.pi, reg, "mm", "rad")
    tube_lv = g4.LogicalVolume(tube, "G4_Cu", "tube_lv", reg)
    tube_hor_lv = g4.LogicalVolume(tube, "G4_Zn", "tube_hor_lv", reg)

    tube_had = g4.solid.Tubs("tube_had", 0 , tube_outer_diameter / 2,Had_Calorimeter_z  , 0, 2 * _np.pi, reg, "mm", "rad")
    
    tube_had_lv = g4.LogicalVolume(tube_had, "G4_Si", "tube_had_lv", reg)
    # tube_pv = g4.PhysicalVolume([0, 0, 0], [0, 0, 0], tube_lv, "tube_pv", worldLV, reg)

    n_tubes_col=int(Calo_x/t_diameter)
    n_rows=int(0.5*EM_calo_z/t_diameter)+1

    # for k in range(n_rows):
    #     for c in range(n_tubes_col):
    #         Tube_vert_PV=pyg4ometry.geant4.PhysicalVolume([_np.pi/2,0,0],[-Calorimeter_x*0.5+c*tube_outer_diameter,0, -0.5*EM_Calorimeter_z +2*k*tube_outer_diameter+z_Calo_EM], tube_lv,"Tube_vert_PV"+ str(k)+","+str(c),worldLV,reg)
    #         Tube_hor_PV=pyg4ometry.geant4.PhysicalVolume([0,_np.pi/2,0],[0,-Calorimeter_x*0.5+c*tube_outer_diameter, -0.5*EM_Calorimeter_z+(2*k+1)*tube_outer_diameter+z_Calo_EM], tube_hor_lv,"Tube_hor_PV"+ str(k)+","+str(c),worldLV,reg)

    n_rows2=int(EM_calo_z/t_diameter)+1        
    for k in range(n_tubes_col):
        for c in range(n_tubes_col):
            Tube_had_PV=pyg4ometry.geant4.PhysicalVolume([0,0,_np.pi/2],[-Calorimeter_x*0.5+c*tube_outer_diameter,-Calorimeter_x*0.5+k*tube_outer_diameter,0.5*tube_outer_diameter+ 0.5*EM_Calorimeter_z+Had_Calorimeter_z*0.5+z_Calo_EM], tube_had_lv,"Tube_had_PV"+ str(k)+","+str(c),worldLV,reg)


    # gdml output
    reg.setWorld(worldLV)
    w = pyg4ometry.gdml.Writer()
    w.addDetector(reg)
    w.write("SciFi_3Trk_mag_Dualcalo.gdml")

    v=None
    if vis :

       # v_c = pyg4ometry.visualisation.VtkViewerColoured(materialVisOptions={"G4_Fe":[0,0,1],nbti:[1,0,1],Fiberm:[0,1,1]})
        v_c = pyg4ometry.visualisation.VtkViewerColoured(materialVisOptions={"G4_Nb":[1,0,0.6],"G4_Fe":[0,0,1],"G4_Cu":[1,0,0],"G4_Zn":[0,0.8,1],"G4_Si":[0.2,0.05,0.0]})
        v_c.addLogicalVolume(worldLV)
        v_c.setOpacity(0.9)
       # v_c.setWireframe(-1)
        v_c.addAxesWidget()
        v_c.exportOBJScene('Calo_had_r20_obj')
        v_c.view()
        # v = pyg4ometry.visualisation.VtkViewer()
        # v.addLogicalVolume(worldLV)
        # v.addAxes(300)
        # v.setOpacity(0.75)
        # v.view()





def SciFiTrackerLayer(reg = None) :
    reg = pyg4ometry.geant4.Registry() if reg is None else reg
    SF_LV=[]
    
    bx_vert_us = pyg4ometry.gdml.Constant("bx_vert_us","3000",reg,True)
    by_vert_us = pyg4ometry.gdml.Constant("by_vert_us","1500",reg,True)
    bz_vert_us = pyg4ometry.gdml.Constant("bz_vert_us","40",reg,True)

    bx_vert_ds = pyg4ometry.gdml.Constant("bx_vert_ds","3500",reg,True)
    by_vert_ds = pyg4ometry.gdml.Constant("by_vert_ds","1500",reg,True)
    bz_vert_ds = pyg4ometry.gdml.Constant("bz_vert_ds","40",reg,True)

    bx_hor = pyg4ometry.gdml.Constant("bx_hor","3700",reg,True)
    by_hor = pyg4ometry.gdml.Constant("by_hor","1000",reg,True)
    bz_hor = pyg4ometry.gdml.Constant("bz_hor","40",reg,True)

    Fiberm = pyg4ometry.geant4.MaterialCompound("Scifiber",1.18,3,reg)
    Corem = pyg4ometry.geant4.MaterialCompound("Core",1.05,2,reg)
    Innerm = pyg4ometry.geant4.MaterialCompound("Innerm",1.19,3,reg)
    Outerm = pyg4ometry.geant4.MaterialCompound("Outerm",1.43,3,reg)
    he = pyg4ometry.geant4.ElementSimple("hydrogen","H",1,1.008)
    ce = pyg4ometry.geant4.ElementSimple("carbon","C",6,12.0096)
    oe = pyg4ometry.geant4.ElementSimple("oxygen","O",8,16.0)
    fluore = pyg4ometry.geant4.ElementSimple("fluor","F",9,19.0)

    Corem.add_element_massfraction(ce, 0.923)
    Corem.add_element_massfraction(he, 0.077)

    Innerm.add_element_massfraction(oe, 0.6059)
    Innerm.add_element_massfraction(ce, 0.3142)
    Innerm.add_element_massfraction(he, 0.0799)

    Outerm.add_element_massfraction(fluore, 0.6628)
    Outerm.add_element_massfraction(ce, 0.2791)
    Outerm.add_element_massfraction(he, 0.0581)

    Fiberm.add_material(Corem, 0.7744)
    Fiberm.add_material(Innerm, 0.1092)
    Fiberm.add_material(Outerm, 0.1164)

    SciFi_Trk_vert_us   = pyg4ometry.geant4.solid.Box("SciFi_Trk_vert_us", bx_vert_us, by_vert_us, bz_vert_us,reg)
    SciFiLv_vert_us = pyg4ometry.geant4.LogicalVolume(SciFi_Trk_vert_us,Fiberm,"SciFiLv_vert_us",reg)
    SF_LV.append(SciFiLv_vert_us)

    SciFi_Trk_vert_ds   = pyg4ometry.geant4.solid.Box("SciFi_Trk_vert_ds", bx_vert_ds, by_vert_ds, bz_vert_ds,reg)
    SciFiLv_vert_ds = pyg4ometry.geant4.LogicalVolume(SciFi_Trk_vert_ds,Fiberm,"SciFiLv_vert_ds",reg)
    SF_LV.append(SciFiLv_vert_ds)

    SciFi_Trk_hor   = pyg4ometry.geant4.solid.Box("SciFi_Trk_hor", bx_hor, by_hor, bz_hor,reg)
    SciFiLv_hor = pyg4ometry.geant4.LogicalVolume(SciFi_Trk_hor,Fiberm,"SciFiLv_hor",reg)
    SF_LV.append(SciFiLv_hor)
    SF_LV.append(Fiberm)
    

    return SF_LV







if __name__ == "__main__":
    SciFiTracker(True)
