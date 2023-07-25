import ROOT
import math
from array import array


# Function to calculate the magnetic field components Bx, By for a given (x, y) point
def calculate_magnetic_field(x, y, magnitude):
    # Calculate the angle theta of the point (x, y) with respect to the positive x-axis
    theta = math.atan2(y, x)

    # Calculate the magnetic field components Bx, By
    Bx = magnitude * math.cos(theta)
    By = magnitude * math.sin(theta)

    return Bx, By


def create_and_fill_tree(Bfield, rmin, rmax, halflength, z_endcap_min, r_endcap_min, num_points):
    # Create a TTree
    tree = ROOT.TTree("my_magnetic_field_map",
                      "MuColl_10TeV_v0A toroidal magnetic field")

    # Define variables for the branches
    x_mm = array('f', [0])
    y_mm = array('f', [0])
    z_mm = array('f', [0])
    Bx = array('f', [0])
    By = array('f', [0])
    Bz = array('f', [0])

    # x_mm = ROOT.vector('float')()
    # y_mm = ROOT.vector('float')()
    # r_mm = ROOT.vector('float')()
    # z_mm = ROOT.vector('float')()
    # Bx = ROOT.vector('float')()
    # By = ROOT.vector('float')()
    # Bz = ROOT.vector('float')()

    # Add branches to the TTree
    tree.Branch('x_mm', x_mm, 'var/F')
    tree.Branch('y_mm', y_mm, 'var/F')
    # tree.Branch('r_mm', r_mm, 'var/F')
    tree.Branch('z_mm', z_mm, 'var/F')
    tree.Branch('Bx', Bx, 'var/F')
    tree.Branch('By', By, 'var/F')
    tree.Branch('Bz', Bz, 'var/F')

    # Fill the barrel region
    for iz in range(num_points):
        z = (iz * halflength) / num_points

        for ir in range(num_points):
            radius = rmin + ir * (rmax-rmin) / num_points

            for i in range(num_points):
                theta = 2 * math.pi * i / num_points
                x = radius * math.cos(theta)
                y = radius * math.sin(theta)

                x_mm[0] = x
                y_mm[0] = y
                z_mm[0] = z
                Bx_val, By_val = calculate_magnetic_field(x, y, Bfield)
                Bx[0] = Bx_val
                By[0] = By_val
                Bz[0] = 0.0

                tree.Fill()

                # symmetrize around z=0
                x_mm[0] = x
                y_mm[0] = y
                z_mm[0] = -z
                Bx[0] = Bx_val
                By[0] = By_val
                Bz[0] = 0.0

                tree.Fill()

    # Fill the endcap region
    for iz in range(num_points):
        z = z_endcap_min + iz * (halflength-z_endcap_min) / num_points

        for ir in range(num_points-1):  # avoids overlap at rmin
            radius = r_endcap_min + ir * (rmin-r_endcap_min) / num_points

            for i in range(num_points):
                theta = 2 * math.pi * i / num_points
                x = radius * math.cos(theta)
                y = radius * math.sin(theta)

                x_mm[0] = x
                y_mm[0] = y
                z_mm[0] = z
                Bx_val, By_val = calculate_magnetic_field(x, y, Bfield)
                Bx[0] = Bx_val
                By[0] = By_val
                Bz[0] = 0.0

                tree.Fill()

                # symmetrize around z=0
                x_mm[0] = x
                y_mm[0] = y
                z_mm[0] = -z
                Bx[0] = Bx_val
                By[0] = By_val
                Bz[0] = 0.0

                tree.Fill()

    return tree


if __name__ == "__main__":
    # Set the parameters for the cylindrical surface
    rmin = 4100  # min radius [mm]
    rmax = 7600  # max radius [mm]
    halflength = 8000  # Chosen halflength [mm]
    z_endcap_min = 4570  # End of HCal [mm]
    r_endcap_min = 445  # End of nozzle [mm]
    num_points = 100  # Number of points to create (same for x,y,z)
    Bfield = 5  # [T]

    # Create and fill the TTree
    tree = create_and_fill_tree(
        Bfield, rmin, rmax, halflength, z_endcap_min, r_endcap_min, num_points)

    # Create a ROOT file to store the TTree
    output_file = ROOT.TFile("cylindrical_surface_data.root", "RECREATE")
    output_file.cd()

    # Write the TTree to the ROOT file
    tree.Write()

    # Close the ROOT file
    output_file.Close()

    print("TTree has been created and filled with data and saved to 'cylindrical_surface_data.root'.")
