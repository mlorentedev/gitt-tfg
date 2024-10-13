"""
Name        :   testbench.py
Created on  :   18.10.2017
Designer    :   Manuel Lorente Alman
-------------------------------------------------------------------------------
Description:    General test bench to simulate a CMOS sensor, sweep exposure,
                process all data refering to EMVA1288 and generate a standard
                report.
-------------------------------------------------------------------------------    
"""
#%% Imports
import os
import shutil
from emva1288.camera.dataset_generator import DatasetGenerator
from emva1288.process.parser import ParseEmvaDescriptorFile
from emva1288.process.loader import LoadImageData
from emva1288.process.data import Data1288
from emva1288.process.results import Results1288
from emva1288.process.plotting import Plotting1288
from emva1288 import report

#%% Processing parameters

dir_ = 'K:\\TFG\\3-Code\\src\\Results\\'
fname = 'EMVA1288_Simulation_12Bit'
                            # The output directory where the descriptor file 
                            # and images will be saved. If None, it will create 
                            # a tempory directory that will be deleted (and its 
                            # contents) when the dataset generator object is 
                            # deleted
                            
datagen_flag = 1            # 1 for sensor data simulation. If None, select the
                            # given directory
                            
dataproc_flag = 1           # 1 for sensor data processing and EMVA1288 calcs

#%% Test parameters

steps = 40                  # Number of points to take
L = 5                       # The number of image taken during a spatial test.
version = 15                # SVN config version to add in descriptor file

image_format = 'tiff'       # To Matlab or other image processing softwares

radiance_min = None         # The minimal radiance (in W/cm^2/sr). If None, 
                            # a value above dark illumination will be 
                            # automatically chosen
                            
radiance_max = None         # The maximal radiance (in W/cm^2/sr). If None, a 
                            # value above dark illumination will be 
                            # automatically chosen
                            
exposure_fixed = None      # By default, the points given are for an texp
                            # variation test (if this is None). If a value is 
                            # given to this kwarg, this will be the camera's 
                            # exposure time (in ns) at which the operation 
                            # points will be set for an illumination variation 
                            # test.

#%% Sensor parameters
                            
f_number = 8                # F-number of the light source/camera setup

pixel_area = 25             # The area of one pixel (in um ^ 2)

bit_depth = 12              # Bit depth of the image [8, 10, 12, 14]

width = 640                 # The number of columns in the image

height = 480                # The number of rows in the image

temp = 45,                  # Sensor temperature in degrees Celsius

temp_ref = 25               # Reference temperature (at which the dark current
                            # is equal to the reference dark current)
                            
temp_doubling = 3           # The doubling temperature (at which the dark
                            # current is two times the reference dark
                            # current)
                            
wavelength = 550            # illumination wavelength in nm

qe = None                   # Quantum efficiency for the given wavelength  
                            # (between 0 and 1). If None, a simulated
                            # quantum efficiency is choosen
                            
exposure = 1000000          # Exposure time in ns

exposure_min = 100000       # Minimum exposure time in ns

exposure_max = 500000000    # Maximum exposure time in ns

K = 0.21                    # Overall system gain (in DN/e^-)

K_min = 0.05                # The overall minimal system gain (in DN/e^-)

K_max = 17.                 # The overall maximal system gain (in DN/e^-)

K_steps = 255               # The number of available intermediate overall 
                            # system gains between K_min and K_max
                            
blackoffset = 3             # The dark signal offset for each pixel (in DN)

blackoffset_min = 0         # The min dark signal offset for each pixel (in DN)

blackoffset_max = None      # The max dark signal offset for each pixel (in DN)

blackoffset_steps = 255     # The number of available blackoffsets between the
                            # mimimal and maximal blackoffsets.
                        
dark_current_ref = 5       # The reference dark current used for computing the
                            # total dark current
                            
dark_signal_0 = 20.         # Mean number of electrons generated by the 
                            # electronics (offset)
                            
sigma2_dark_0 = 15.         # Variance of electrons generated by the 
                            # electronics
                            
u_esat = 45000.             # Full well capacity

radiance_factor = 1.        # The factor or an array with the same size of the 
                            # image for modifie the radiance. By default 1 for 
                            # no modification
                            
dsnu = 5                 # DSNU image in DN, array with the same shape of 
                            # the image that is added to every image
                            
prnu = 0.8                 # PRNU image in percentages (1 = 100%), array with 
                            # the same shape of the image. Every image is 
                            # multiplied by it

#%% Report parameters
                            
# Description of the setup
s_standard_version = 3.1    # The EMVA1288 standard version number used  
          
s_ls = 'Led'                # The light source type (e.g. integrating sphere)

s_ls_nonuniform = '0.5%'    # The light source introducing non uniformity
  
# Basic information
b_vendor =  'Electronic \
            Engineering \
            Department'     # The vendor name that manufactures theabc

b_model =  'CMOS Sensor'    # The model of the tested camera

b_data_type =  'Single'     # The label given to the data used for the test

b_sensor_type =  'Area'     # The type of the tested sensor within the camera

b_resolution =  '640x480'   # The camera's resolution

b_pixel_size =  5           # The sensor's pixel size

b_shutter_type =  'Global'  # The shutter type of the sensor

b_max_readout =  '120fps'    # The camera's maximal readout rate

b_interf =  'GigE'   # The camera's interface type

b_qe_plot =  None           # The sensor's quantum efficency plots
 
# Marketing information
m_logo = None               # The path to the logo icon

m_watermark = None          # A text that will be printed on every page of the
                            # report in the background in transparent red.

m_missingplot = None        # The path to a missing plot icon

m_cover_page = None         # The path to a custom cover page for the report

# Operation point
    # bit_depth, gain, black_level, exposure_time, wavelength,
    # temperature, housing_temperature, fpn_correction,
    # summary_only
op_name = 'Config case B'

op_id = 1

op_summary = False
                          
#%% Algorithm

if datagen_flag :
    if dir_ and fname:
        outdir = os.path.join(dir_, fname)
        if os.path.exists(outdir):
            shutil.rmtree(outdir,1)
    else:
        outdir  =  None
    dataset_generator  =  DatasetGenerator(steps = steps,
                                           L = L,
                                           version = version,
                                           image_format = image_format,
                                           outdir = outdir,
                                           radiance_min = radiance_min,
                                           radiance_max = radiance_max,
                                           exposure_fixed = exposure_fixed,
                                           f_number = f_number,
                                           pixel_area = pixel_area,
                                           bit_depth = bit_depth,
                                           width = width,
                                           height = height,
                                           temperature = temp_ref,
                                           temperature_doubling = temp_doubling,
                                           wavelength = wavelength,
                                           qe = qe,
                                           exposure = exposure,
                                           exposure_min = exposure_min,
                                           exposure_max = exposure_max,
                                           K = K,
                                           K_min = K_min,
                                           K_max = K_max,
                                           K_steps = K_steps,
                                           blackoffset = blackoffset,
                                           blackoffset_min = blackoffset_min,
                                           blackoffset_max = blackoffset_max,
                                           blackoffset_steps = blackoffset_steps,
                                           dark_current_ref = dark_current_ref,
                                           dark_signal_0 = dark_signal_0,
                                           sigma2_dark_0 = sigma2_dark_0,
                                           u_esat = u_esat,
                                           radiance_factor = radiance_factor,
                                           dsnu = dsnu,
                                           prnu = prnu
                                            )

if dataproc_flag :
    if datagen_flag :
        imp = dataset_generator.descriptor_path
    else :
        imp = os.path.join(os.path.join(dir_, fname),'EMVA1288descriptor.txt')
    # Parse the descriptor file  
    parser = ParseEmvaDescriptorFile(imp)
    # Load images
    imgs = LoadImageData(parser.images)
    # Process the collected data
    data = Data1288(imgs.data)
    res = Results1288(data.data, pixel_area = pixel_area)
    res.print_results()
    plot = Plotting1288(res)
    plot.plot()
    # Initialize the report with the marketing data
    # Provide a non existent name for the output directory
    myreport = report.Report1288(os.path.join(os.path.join(dir_, fname),\
                                              'Report'),
                                 marketing={'logo': m_logo,
                                            'watermark': m_watermark,
                                            'missingplot': m_missingplot,
                                            'cover_page': m_cover_page
                                            },
                                 setup={'Light source' : s_ls,
                                        'Light source non uniformity' : \
                                        s_ls_nonuniform, 
                                        'Standard version' : s_standard_version    
                                         },
                                 basic= {'vendor': b_vendor,
                                         'model': b_model,
                                         'data_type': b_data_type,
                                         'sensor_type': b_sensor_type,
                                         'resolution': b_resolution,
                                         'pixel_size': b_pixel_size,
                                         'bit_depth': bit_depth,
                                         'shutter_type': b_shutter_type,
                                         'maximum_readout_rate': b_max_readout,
                                         'interface_type': b_interf,
                                         'qe_plot': b_qe_plot
                                         })
 
    op = {'name': op_name,
         'id': op_id,
         'summary_only': op_summary,
         'camera_settings': {'Number of images' : steps,                 
                             'Number of frames' : L,                      
                             'Configuration SVN version' : version,            
                             'Image format' : image_format,       
                             'Radiance minimimum' : radiance_min,                      
                             'Radiance maximum' : radiance_max,                                 
                             'Exposure fixed' : exposure_fixed 
                            }
         }
    
    # Add the operation point to the report
    # we can add as many operation points as we want
    # we pass the emva1288.Data1288 object to extract automatically all 
    # the results and graphics
    myreport.add(op, data.data)
    
    # Generate the latex files
    myreport.latex()