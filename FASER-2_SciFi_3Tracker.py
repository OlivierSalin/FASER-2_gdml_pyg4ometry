import pyg4ometry
import numpy as _np

# set the number of polygon points on cylinders to be 2x the 16 default
#pyg4ometry.config.SolidDefaults.Tubs.nslice = 32
#pyg4ometry.config.SolidDefaults.CutTubs.nslice = 32

def SciFiTracker(vis= False):
    reg = pyg4ometry.geant4.Registry()


    d_hor_vert = pyg4ometry.gdml.Constant("d_hor_vert","100",reg,True)
    d_layers = pyg4ometry.gdml.Constant("d_layers","500",reg,True)
    #d_stream = pyg4ometry.gdml.Constant("d_stream","6500",reg,True)

    d1_ds = pyg4ometry.gdml.Constant("d1_ds","7500",reg,True)
    d1_us = pyg4ometry.gdml.Constant("d1_us","17000",reg,True)



    
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

    SciFiLv = SciFiTrackerLayer(reg = reg)
#downstream
    nLayer_ds = 3
    for k in range(0,nLayer_ds):
       SciFi_Trk_ds_vertPV = pyg4ometry.geant4.PhysicalVolume([0,k*_np.pi/180,0],[0,0, d1_ds+k*d_layers], SciFiLv,"SciFi_Trk_ds_vertPV"+str(k),worldLV,reg)
       SciFi_Trk_ds_horizPV = pyg4ometry.geant4.PhysicalVolume([0,_np.pi/2,0],[0,0, d1_ds+k*d_layers+d_hor_vert], SciFiLv,"SciFi_Trk_ds_horizPV"+ str(k),worldLV,reg)


#upstream
    nLayer_us = 3
    for j in range(0,nLayer_us):
       SciFi_Trk_us_vertPV = pyg4ometry.geant4.PhysicalVolume([0,j*_np.pi/180,0],[0,0, d1_us+j*d_layers], SciFiLv,"SciFi_Trk_us_vertPV"+str(j),worldLV,reg)
       SciFi_Trk_us_horizPV = pyg4ometry.geant4.PhysicalVolume([0,_np.pi/2,0],[0,0,d1_ds+j*d_layers +d_hor_vert], SciFiLv,"SciFi_Trk_us_horizPV"+str(j),worldLV,reg)



    # gdml output
    reg.setWorld(worldLV)
    w = pyg4ometry.gdml.Writer()
    w.addDetector(reg)
    w.write("SciFi_3Tracker.gdml")





def SciFiTrackerLayer(reg = None) :
    reg = pyg4ometry.geant4.Registry() if reg is None else reg

    bx = pyg4ometry.gdml.Constant("bx","3500",reg,True)
    by = pyg4ometry.gdml.Constant("by","1500",reg,True)
    bz = pyg4ometry.gdml.Constant("bz","40",reg,True)

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

    SciFi_Trk   = pyg4ometry.geant4.solid.Box("SciFi_Trk", bx, by, bz,reg)
    SciFiLv = pyg4ometry.geant4.LogicalVolume(SciFi_Trk,Fiberm,"SciFiLv",reg)

    return SciFiLv







if __name__ == "__main__":
    SciFiTracker(False)
