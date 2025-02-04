# Need to configure Python to use the SNAP-Python (snappy) interface(https://senbox.atlassian.net/wiki/spaces/SNAP/pages/50855941/Configure+Python+to+use+the+SNAP-Python+snappy+interface)
# Read in unzipped Sentinel-1 GRD products (EW and IW modes)

##questo codice dà il risultato stesso di SNAP
import sys
from os.path import dirname, basename, join
#snap_path= 'C:\\Users\\vitto\\.snap\\snap-python'


import datetime
import time
import sys



import os, gc

import geopandas as gpd

def do_apply_orbit_file(source):
    from esa_snappy import GPF
    from esa_snappy import HashMap
    print('\tApply orbit file...') 
    parameters = HashMap()
    parameters.put('Apply-Orbit-File', True)
    output = GPF.createProduct('Apply-Orbit-File', parameters, source)
    return output


def do_thermal_noise_removal(source):
    from esa_snappy import GPF
    from esa_snappy import HashMap
    print('\tThermal noise removal...')
    parameters = HashMap()
    parameters.put('removeThermalNoise', True)
    output = GPF.createProduct('ThermalNoiseRemoval', parameters, source)
    return output


def do_calibration(source, polarization, pols):
    print('\tCalibration...')
    from esa_snappy import GPF
    from esa_snappy import HashMap   
    parameters = HashMap()
    parameters.put('outputSigmaBand', True)
    if polarization == 'DH':
        parameters.put('sourceBands', 'Intensity_HH,Intensity_HV')
    elif polarization == 'DV':
        parameters.put('sourceBands', 'Intensity_VH,Intensity_VV')
    elif polarization == 'SH' or polarization == 'HH':
        parameters.put('sourceBands', 'Intensity_HH')
    elif polarization == 'SV':
        parameters.put('sourceBands', 'Intensity_VV')
    else:
        print("different polarization!")
    parameters.put('selectedPolarisations', pols)
    parameters.put('outputImageScaleInDb', False)
    output = GPF.createProduct("Calibration", parameters, source)
    return output

def do_speckle_filtering(source):
    from esa_snappy import GPF
    from esa_snappy import HashMap
    print('\tSpeckle filtering...')
    parameters = HashMap()
    parameters.put('filter', 'Refined Lee')
    parameters.put('SizeX', 5)
    parameters.put('SizeY', 5)
    output = GPF.createProduct('Speckle-Filter', parameters, source)
    return output


def do_flip(source, orbit):
    from esa_snappy import GPF
    from esa_snappy import HashMap
    if orbit == "ASCENDING":
        flipType = 'Vertical'
    elif orbit == "DESCENDING":
        flipType = "Horizontal"
    print('\tFlipping...')
    parameters = HashMap()
    parameters.put('flipType', flipType)
    output = GPF.createProduct('Flip', parameters, source)
    return output


def do_terrain_correction(source, proj, downsample):
    from esa_snappy import GPF
    from esa_snappy import HashMap
    print('\tTerrain correction...')
    parameters = HashMap()
    parameters.put('demName', 'SRTM 1Sec HGT')
    parameters.put('imgResamplingMethod', 'BILINEAR_INTERPOLATION')
    # parameters.put('mapProjection', proj)       # Uncomment this line if need to convert to UTM/WGS84, default is WGS84
    parameters.put('saveProjectedLocalIncidenceAngle', True)
    parameters.put('saveSelectedSourceBand', True)
    if downsample == 1:                      # downsample: 1 -- need downsample to 40m, 0 -- no need to downsample
        parameters.put('pixelSpacingInMeter', 40.0)
    output = GPF.createProduct('Terrain-Correction', parameters, source)
    return output

def do_subset(source, wkt):
    from esa_snappy import GPF
    from esa_snappy import HashMap
    print('\tSubsetting...')
    parameters = HashMap()
    parameters.put('geoRegion', wkt)
    output = GPF.createProduct('Subset', parameters, source)
    return output

def s1_preprocessing(in_image_path, output_path, wkt):
    """
    Preprocessing Sentinel-1 raw data, performs following preprocessing
    1. Apply orbit file
    2. Thermal noise removal
    3. Calibration
    4. Speckle filtering
    5. Subset

    Parameters:
        in_image_path (str): Path to the raw Sentinel-1 image.
        output_path (str): Directory to save preprocessed image.
        wkt (str): Polygon in wkt format to clip over ROI.
    
    Returns:
        Path of preprocessed image
    """
    from esa_snappy import ProductIO
    gc.enable()
    gc.collect()
    sentinel_1 = ProductIO.readProduct(in_image_path)
    # Get orbit direction
    orbit_direction = sentinel_1.getMetadataRoot().getElement('Abstracted_Metadata').getAttributeString('PASS')
    
    loopstarttime=str(datetime.datetime.now())
    print('Start time:', loopstarttime)
    start_time = time.time()
    in_image_bn = basename(in_image_path)
    
    ## Extract mode, product type, and polarizations from filename
    modestamp = in_image_bn.split("_")[1]
    productstamp = in_image_bn.split("_")[2]
    polstamp = in_image_bn.split("_")[3]
    polarization = polstamp[2:4]
    if polarization == 'DV':
        pols = 'VH,VV'
    elif polarization == 'DH':
        pols = 'HH,HV'
    elif polarization == 'SH' or polarization == 'HH':
        pols = 'HH'
    elif polarization == 'SV':
        pols = 'VV'
    else:
        print("Polarization error!")
    ## Start preprocessing:
    applyorbit = do_apply_orbit_file(sentinel_1)
    thermaremoved = do_thermal_noise_removal(applyorbit)
    calibrated = do_calibration(thermaremoved, polarization, pols)
    down_filtered = do_speckle_filtering(calibrated)
    subset = do_subset(down_filtered, wkt)
    flipped = do_flip(subset, orbit_direction)
    del applyorbit
    del thermaremoved
    del calibrated
    del down_filtered
    del subset

    out_image_bn = in_image_bn.replace('.zip', '')
    out_image_bn = out_image_bn.replace('.SAFE', '')
    out_image_path = join(output_path, out_image_bn)
    print("Writing...")
    ProductIO.writeProduct(flipped, out_image_path, 'BEAM-DIMAP') #crea il .data
    ProductIO.writeProduct(flipped, out_image_path, 'GeoTIFF')
    del flipped
    print('Processing Done.')
    sentinel_1.dispose()
    sentinel_1.closeIO()
    print("--- %s seconds ---" % (time.time() - start_time))
    return out_image_path


def do_dem_assisted_coregistration(master_path, slave_path, dem_name='SRTM 1Sec HGT'):
    """
    Perform DEM-assisted co-registration of Sentinel-1 images using SNAP's Python API (Snappy).

    Parameters:
        master_path (str): Path to the master Sentinel-1 image.
        slave_path (str): Path to the slave Sentinel-1 image.
        dem_name (str): DEM to use for terrain correction (default is 'SRTM 1Sec HGT').
    
    Returns:
        Coregistrated stack image
    """
    from esa_snappy import GPF
    from esa_snappy import HashMap
    from esa_snappy import ProductIO
    # Load master and slave products
    master = ProductIO.readProduct(f"{master_path}.dim")
    slave = ProductIO.readProduct(f"{slave_path}.dim")
    
    # Set up co-registration parameters
    parameters = HashMap()
    parameters.put('demName', dem_name)
    parameters.put('demResamplingMethod', 'BILINEAR_INTERPOLATION')
    parameters.put('resamplingType', 'BILINEAR_INTERPOLATION')
    parameters.put('tileExtensionPercent', '100')
    parameters.put('maskOutAreaWithoutElevation', True)
    parameters.put('outputRangeAzimuthOffset', False)
    
    # Create a product combining master and slave
    master_slave = HashMap()
    master_slave.put('Master', master)
    master_slave.put('Slave', slave)
    
    # Perform co-registration
    output = GPF.createProduct('DEM-Assisted-Coregistration', parameters, master_slave)    

    return output


def do_offset_tracking(sourcePrd, custom_parameters):
    """
    Perform DEM-assisted co-registration of Sentinel-1 images using SNAP's Python API (Snappy).

    Parameters:
        master_path (str): Path to the master Sentinel-1 image.
        slave_path (str): Path to the slave Sentinel-1 image.
        dem_name (str): DEM to use for terrain correction (default is 'SRTM 1Sec HGT').
    
    Returns:
        None: Saves the co-registered product to the specified output path.
    """
    from esa_snappy import GPF
    from esa_snappy import HashMap
    # Set up co-registration parameters
    DEFAULT_PARAMETERS = {
    'gridAzimuthSpacing': '8',
    'gridRangeSpacing': '8',
    'registrationWindowWidth': '64',
    'registrationWindowHeight': '64',
    'xCorrThreshold': '0.1',
    'registrationOversampling': '32',
    'averageBoxSize': '3',
    'maxVelocity': '2',
    'radius': '5',
    'resamplingType': 'BILINEAR_INTERPOLATION'
}
    # Usa i parametri di default o quelli personalizzati
    parameters = HashMap()
    params = custom_parameters if custom_parameters else DEFAULT_PARAMETERS

    for key, value in params.items():
        parameters.put(key, value)

    source = HashMap()
    source.put('sourceProduct', sourcePrd)
    
    # Perform co-registration
    velocity = GPF.createProduct('Offset-Tracking', parameters, source)
    return velocity

# Run the function
def process_glacier_velocity(reference_image_path,secondary_image_path,outpath, shp_path, snap_path,offset_parameters):
    # Path to reference (master) and secondary (slave) sentinel-1 images and output directory
    from esa_snappy import ProductIO
    from esa_snappy import HashMap
    import os, gc
    from esa_snappy import GPF
  
   

    # Creates outpath if doesn't exist
    if not os.path.exists(outpath):
        os.makedirs(outpath)
    ## UTM projection parameters
    proj = '''PROJCS["WGS 84 / UTM zone 32N",
    GEOGCS["WGS 84",
        DATUM["WGS_1984",
            SPHEROID["WGS 84",6378137,298.257223563,
                AUTHORITY["EPSG","7030"]],
            AUTHORITY["EPSG","6326"]],
        PRIMEM["Greenwich",0,
            AUTHORITY["EPSG","8901"]],
        UNIT["degree",0.0174532925199433,
            AUTHORITY["EPSG","9122"]],
        AUTHORITY["EPSG","4326"]],
    PROJECTION["Transverse_Mercator"],
    PARAMETER["latitude_of_origin",0],
    PARAMETER["central_meridian",9],
    PARAMETER["scale_factor",0.9996],
    PARAMETER["false_easting",500000],
    PARAMETER["false_northing",0],
    UNIT["metre",1,
        AUTHORITY["EPSG","9001"]],
    AXIS["Easting",EAST],
    AXIS["Northing",NORTH],
    AUTHORITY["EPSG","32632"]]
    '''
    # Path of the Region of Interest
    
    # Read polyon, creates buffer over AOI and take that as wkt
    gdf = gpd.read_file(shp_path)
    #wkt = gdf.buffer(0.025).to_wkt()[0]
    wkt = gdf.buffer(0.008).to_wkt()[0]
    # Get the input images date in yyyymmdd format from file name
    # This part assumes, name of the file is same as downloaded from Copernicus website
    reference_yyyymmdd = basename(reference_image_path).split('_')[4][:8]
    secondary_yyyymmdd = basename(secondary_image_path).split('_')[4][:8]
    # Preprocessing of both the S1 images
    reference_image_path = s1_preprocessing(reference_image_path, outpath, wkt)
    secondary_image_path = s1_preprocessing(secondary_image_path, outpath, wkt)
    # Coregistration of two images 
    coregistered = do_dem_assisted_coregistration(reference_image_path, secondary_image_path)
    # Velocity using offset tracking
    velocity = do_offset_tracking(coregistered, offset_parameters)
    # Terrain correction
    tercorrected = do_terrain_correction(velocity, proj, 0)
    # Save terrain corrected velocity iamge
    velBn = f"{reference_yyyymmdd}_{secondary_yyyymmdd}_Stack_Vel_Tc"
    velPath = join(outpath, velBn)
    ProductIO.writeProduct(tercorrected, velPath, 'GeoTIFF')
        

if __name__== "__main__":
    main()