# -*- coding: utf-8 -*-
"""
descriptions of all the lastools
"""

import os
from pathlib import Path

# html format templates
# <b>bold</b>
# <i>italic</i>
# <small>small</small>
# <sub>sub</sub>
# <sup>sup</sup>
# <font style="color:DodgerBlue;">DodgerBlue</font>
# <font style="color:#CD5C5C;">IndianRed</font>
# <font style="color:#DAA520;">GoldenRod</font>
# <font style="color:#9400D3;">DarkViolet</font>
# <font style="color:#8B008B;">DarkMagenta</font>
# <font style="color:#006400;">DarkGreen</font>


# ../plugins/LAStools/lastools + /assets/img
paths = {
    "lastools": f"{os.path.split(os.path.split(os.path.dirname(__file__))[0])[0]}/",
    "img": f"{Path(os.path.split(os.path.split(os.path.dirname(__file__))[0])[0]).as_posix()}/assets/img/",
}

licence = {
    "c": {
        "descript": 'This tool is <a href="https://rapidlasso.de/license">licensed</a>, but free to test with pointclouds up to 3 mio points.',
        "path": "lic_com.png",
    },
    "o": {"descript": "This tool is open source and free to use.", "path": "lic_opensource.png"},
    "f": {"descript": "This tool is free to use.", "path": "lic_free.png"},
}


def readme_url(lastool):
    return f"https://downloads.rapidlasso.de/html/{lastool}_README.html"


def readme_link(lastool):
    return f"<a href={readme_url(lastool)}>README file</a>"


# general help text below every individual tool help
def help_string_help(lastool, lic):
    return f"""
      <h3>Help</h3>
      Use the predefined arguments in the plugin gui or add additional command line arguments.
      See the {readme_link(lastool)} to get informations about all available arguments or click the help button.
      <h3>Links</h3>
      See <a href="https://rapidlasso.de">rapidlasso webpage</a> for further informations.
      See the <a href="https://rapidlasso.de/lastools-as-qgis-plugin">LAStools QGIS page</a> for informations about this plugin.
      <h3>Licence Info</h3>
      <img source="file:///{paths['img']}{licence[lic]['path']}" width="16" height="16"> {licence[lic]["descript"]}
      """


# groups
lasgroup_info = {
    1: {"group": "1. Data Compression (LAZ)", "group_id": "data_compression"},
    2: {"group": "2. Data Convert (Import / Export)", "group_id": "data_convert"},
    3: {"group": "3. Preprocessing", "group_id": "preprocessing"},
    4: {"group": "4. Classification & Filtering", "group_id": "classification_filtering"},
    5: {"group": "5. DSM/DTM Generation & Production", "group_id": "dsm_dtm_generation_production"},
    6: {"group": "6. Quality Control & Information", "group_id": "quality_control_information"},
    7: {"group": "7. Publishing", "group_id": "publishing"},
    8: {"group": "8. Visualization & Colorization", "group_id": "visualization_colorization"},
    9: {"group": "9. Pipelines & Samples", "group_id": "pipelines"},
}

fop = '<font style="color:#CD5C5C;">'
foe = '<font style="color:#9400D3;">'
fcc = "</font>"


def txt_args(lastool):
    return f"{fop}additional command line arguments:{fcc} optional arguments, see {readme_link(lastool)} or examples."


txt_folder = "Setup for multiple files in a directory instead of single files."
txt_verbose = f"{fop}verbose:{fcc} verbose output (print extra information)."
txt_64bit = f"{fop}64bit:{fcc} run the 64bit version of the tool (recommended)."
txt_inlazfile = f"{fop}input LAS/LAZ file:{fcc} input file to be processed."
txt_inlazother = f"{fop}other input LAS/LAZ file:{fcc} input file against which is compared."
txt_inlazdir = f"{fop}input directory:{fcc} directory of LAS/LAZ files to be processed."
txt_inshpfile = f"{fop}input polygon(s):{fcc} input shapefile to be processed."
txt_inpolyfile = f"{fop}input polyline(s)/polygons SHP/CSV file:{fcc} input file to match against."
txt_cores = f"{fop}number of cores:{fcc} process multiple inputs on multiple tasks in parallel."
txt_step = f"{fop}step size / pixel size:{fcc} size of input dimension per output pixel."
txt_pixel_attrib = f"{fop}attribute:{fcc} attribute to use to calculate output pixel."
txt_pixel_method = f"{fop}method:{fcc} method to calculate output pixel color."
txt_replace_z = f"{fop}replace z:{fcc} replace the z coordinate with the calculated height above ground."
txt_canopy = f"""
{fop}square plot size:{fcc} size of input dimension per output voxel.
{fop}height cutoff / breast height:{fcc} no metrics are calculated below this height.
{fop}create...:{fcc} select metric to be created.
{fop}count rasters:{fcc} optional individual count raster.
{fop}density rasters:{fcc} optional individual density raster.
"""
txt_tile = f"""
{fop}tile size:{fcc} Tile size should be according to your resolution. One target tile should not exceed the size of 10 million points.
{fop}buffer around each tile:{fcc} Set a buffer around each tile to avoid border artifacts wher points are triangulated.
"""
txt_boundary = f"""
{fop}concavity:{fcc} granularity for grow concavities inwards
{fop}interior holes:{fcc} find internal holes and output hole polygoons (-holes)
{fop}disjoint polygon:{fcc} allow polygon to fragment for point clusters farther than concavity apart (-disjoint)
{fop}produce labels:{fcc} label outputs with file name, bounding box, number of points, etc ... (-labels)
"""
txt_resolution = f"""
{fop}resolution of x and y coordinate:{fcc} set input scale of x and y values
{fop}resolution of z coordinate:{fcc} set z scale
"""
txt_filter = f"""
{fop}filter:{fcc} predefined filters to select
"""
txt_filter_value = f"""
{txt_filter}
{fop}value for filter:{fcc} optional parameter for selected filter
"""
txt_proj = f"""
{fop}source projection:{fcc} predefined projections to select
{fop}source EPSG code:{fcc} epsg code if source projection is EPSG
{fop}source utm zone:{fcc} utm zone if source projection is utm
{fop}source state plane code:{fcc} sp code if source projection is sp
{fop}target ...:{fcc} target projection settings
"""
txt_transform = f"""
{fop}transform:{fcc} predefined transform operations
{fop}value for transform:{fcc} optional parameters for selected transformation
"""
head_console_examples = """
<h3>Console Examples</h3>
This are LAStool command line examples. Arguments can be set by the parameters of the plugin or by the additional command line arguments field.
"""
txt_parse = f"""
{fop}parse string tokens{fcc} (see REAME file for full list)<br>x : [x] coordinate<br>y : [y] coordinate<br>z : [z] coordinate<br>t : gps [t]ime<br>R : RGB [R]ed channel<br>G : RGB [G]reen channel<br>B : RGB [B]lue channel<br>I : N[I]R channel (LAS 1.4|8)<br>s : [s]kip a string or a number that we don't care about<br>i : [i]ntensity<br>a : scan [a]ngle<br>n : [n]umber of returns of that given pulse<br>r : number of [r]eturn<br>h : with[h]eld flag<br>k : [k]eypoint flag<br>g : synthetic fla[g]<br>o : [o]verlap flag (LAS 1.4|6-8)<br>l : scanner channe[l] (LAS 1.4|6-8)<br>c : [c]lassification<br>u : [u]ser data<br>p : [p]oint source ID<br>e : [e]dge of flight line flag<br>d : [d]irection of scan flag<br>0-9 : additional attributes / extra bytes (0..9)<br>(13) : additional attributes / extra bytes (10+)
"""
txt_laszip_intro = "Compresses and uncompresses LiDAR data stored in binary LAS format (1.0 - 1.4) in a completely lossless manner to the compressed LAZ format."
txt_laszip_outro = "Default output is the same file than the input file but with oposite file ending: A file.laz will be converted to file.las just as vice versa."
txt_las2las_intro = """
las2las is the "swiss-army knife" of LiDAR file processing. It can convert, filter, transform, subset, repair, scale, translate, zero, clamp, compress, initialize, reproject, georeference,... LAS or LAZ files in numerous ways. The tool is 100% open source LGPL.<br>Sometimes it is not neccessary to use las2las prior other LAStools, because most arguments can be used by the other tools as well.
"""
txt_las2las_filter = "las2las with parameters to filter pointclouds"
txt_las2las_trans = "las2las with parameters to translate pointclouds"
txt_las2las_project = "las2las with parameters to change projection and georeferencing"
txt_las2txt_short = (
    "converts binary LAS or LAZ files to human readable ASCII text format using a user specific parse argument"
)
txt_las2txt_intro = f"""
{txt_las2txt_short}.<br>This can be used to modify lidar data external and convert them back to LAS/LAZ using txt2las.
"""
txt_txt2las_short = "Converts ASCII files to binary LAS or compressed LAZ file"
txt_txt2las_intro = f"""{txt_txt2las_short}.<br>Use the parse string to define the ascii content or use the column headers in the file."""
txt_e572las_short = "Converts 3D point files in E57 format to binary LAS/LAZ format"
txt_e572las_intro = f"""{txt_e572las_short}.<br>By default all scans contained in the E57 file are merged into one output with all invalid points being omitted. The points of different scans are given different point source IDs so that the information which points belong to one scan is preserved.  It's possible to request '-split_scans' and '-include_invalid' to put points from different scans into separate files and/or to include invalid points as well.<br>Sample data can be found at <a href="http://www.libe57.org/data.html">libe57.org</a>.
By default the tool will apply transformations and/or rotations that it find stored in the pose of each scan. You can ask the tool not to apply those with '-no_pose'. To selevtively suppress only transformation or rotation use '-no_transformation' or '-no_rotation'<br>This tool does not support multiple file input. Batch conversion can be done using a batch file like
{fop}:: convert all *.e57 files to *.laz<br>for %%f in (*.e57) do if not exist %%~nf.laz e572las -i %%f -olaz{fcc}
"""
txt_las2shp_short = "Converts LIDAR from LAS/LAZ/ASCII to ESRI’s Shapefile format by grouping consecutive points into MultiPointZ records"
txt_shp2las_short = "Converts from points from ESRI’s Shapefile to LAS/LAZ/ASCII format, given the input, contains Points or MultiPoints"
txt_lasplanes_short = "Finds sufficiently planar patches of LAS/LAZ points"
txt_shp2las_short = "Converts from points from ESRI’s Shapefile to LAS/LAZ/ASCII format, given the input, contains Points or MultiPoints"
txt_las3dpoly_rad_short = "Modifies points within a certain radial distance of 3D polylines"
txt_las3dpoly_xy_short = "Modifies points within a certain horizontal and vertical distance of 3D polylines"
txt_las3dpoly_intro = """
This tool modifies points within a certain distance of polylines. As an input take, for example, a LAS/LAZ/TXT file and a SHP/TXT file with one or many polylines (e.g. powerlines) by specify a radial distance to the 3D polygon. Affected points can be classified, clipped, or flagged.<br>The input SHP/TXT file must contain clean polygons or polylines that are free of self-intersections, duplicate points, and/or overlaps and they must all form closed loops (e.g. the last and first point should be identical).
An input 'line.csv' may look like-10,0,0<br>10,0,0<br>0,0,0<br>0,-10,0<br>0,10,0"""
txt_lasdistance_short = "Classifies, flags, or remove points within a specified distance of polygonal segments"
txt_lasdistance_intro = """
The distance is calculated on a grid with a spacing of 0.5 meters by default. With '-step_xy 1.0' the granularity of this grid can be adjusted up or down."""
txt_lasintensity_short = "corrects the intensity attenuation due to atmospheric absorption"
txt_lasintensity_intro = f"""
{txt_lasintensity_short}.
This tool corrects the intensity attenuation due to atmospheric absorption.<br>Because the light has to travel longer distances for points with large scan angles, these points may be detected with reduced intensities.
In order to get a reliant attenuation estimate several parameters are essential:<br>- Scanner height above ground level (AGL) [km]<br>- Scanner wavelength [µm]<br>- Atmospheric visibility range [km].
"""
txt_lasindex_short = "Creates an index file (*.lax) about a LAS/LAZ file"
txt_index_intro = f"""
{txt_lasindex_short}. The file contains spatial indexing information. When this LAX file is present it will be used to speed up access to the relevant areas of the LAS/LAZ file.
"""
txt_lasprobe_short = (
    "Probes the elevation of the LIDAR for a given x and y location and reports it to a text file or to stdout"
)
txt_merge_short = "Merge multiple LiDAR files into one"
txt_merge_intro = """
This is a handy tool to merge multiple LiDAR files into one. However, we usually discourage this practice as this can also be achieved on-the-fly with the ‘-merged’ option in any of the other LAStools without creating a second copy on disk. In addition this tools allows splitting larger files into smaller subsets each containing a user-specified number of points.
"""
txt_lasoverage_short = "Finds “overage” points that get covered by more than a single flightline"
txt_lasoverage_intro = """
Reads LiDAR points of an airborne collect and finds the “overage” points that get covered by more than a single flightline. It either marks these overage points or removes them from the output files. The tool requires that the files either have the flightline information stored for each point in the point source ID field (e.g. for tiles containing overlapping flightlines) or that there are multiple files where each corresponds to a flight line (‘-files_are_flightlines’). It is also required that the scan angle field of each point is properly populated.
"""
txt_lasboundary_short = "Computes a boundary polygon that encloses LIDAR points"
txt_lasboundary_intro = f"""{txt_lasboundary_short}.
Reads LIDAR from LAS/LAZ/ASCII files and computes a boundary polygon that encloses the points. By default this is a joint concave hull where “islands of points” are connected by edges that are traversed in each direction once. Optionally a disjoint concave hull is computed with the ‘-disjoint’ flag. This can lead to multiple hulls in case of islands. Note that tiny islands of the size of one or two LIDAR points that are too small to form a triangle will be “lost”."""
txt_lasclip_short = "Clip LIDAR data by polygons"
txt_lasreturn_short = "Reports geometric returns statistics and repairs ‘number of returns’ field"
txt_lasreturn_intro = """Reports geometric return statistics for multi-return pulses and repairs the 'number of returns' field based on GPS times. Note that input files need (currently) to be sorted based on their GPS time stamp. It can also compute the 3D distance (or gaps) between subsequent returns of the same pulse. It can also check for missing or duplicate returns per laser shot and create output files where the problematic groups of returns are marked."""
txt_lassort_short = "Sorts LIDAR data by elevation, gps_time or point_source"
txt_lassort_intro = """sorts the points of a LAS file into z-order arranged cells of a square quad tree and saves them into LAS or LAZ format. This is useful to bucket together returns from different swaths or to merge first and last returns that were stored in separate files.For standard LAS/LAZ files one simply chooses a -bucket_size to specify the resolution of finest quad tree cell. A bucket size of, for example, 5 creates 5x5 unit buckets. The z-order traversal of the quad tree creates implicit "finalization tags" that can later be used for streaming processing.<br>For LAS/LAZ files that are part of a tiling that was created with lastile it is beneficial to specify the resolution via the number of -levels of subtiling this tile. This has the advantage that both the tiling and the subtiling can be used during streaming processing.<br>Another option is -average to coarsen the resolution of the quadtree until the average number of points per cell is as specified.<br>The square quad tree used by lassort can (eventually) be exploited by "streaming TIN" generation code to seamlessly Delaunay triangulate large LAS/LAZ files (or large amounts of LAS/LAZ tiles) in a highly memory-efficient fashion. For that purpose, lassort either adds (or updates) a small VLR to the header the generated LAS/LAZ file.<br>Large amounts of LAS data should first be sorted into tiles with lastile - which operates out-of-core - because lassort does its bucket sort in memory.<br>Alternatively lassort can sort a LAS/LAZ file in GPS time order or in a point source ID order (or first sort by point source IDs and then by time)."""
txt_lastile_short = "Tiles LIDAR points into tiles"
txt_lastile_intro = """Tiles a potentially very large amount of LAS/LAZ/ASCII points from one  or many files into square non-overlapping tiles of a specified size and save them into LAS or LAZ format. Optionally the tool can also create a small ‘-buffer 10’ around every tile where the parameter 10 specifies the number of units each tile is (temporarily) grown in each direction. It is possible to remove the buffer from a tile by running with ‘-remove_buffer’ option. You may also flag the points that fall into the buffer with the new ‘-flag_as_withheld’ or ‘-flag_as_synthetic’ options. If you spatially index your input files using lasindex you may also run lastile on multiple processors with the ‘-cores 4’ option."""
txt_lassplit_short = "Splits LAS or LAZ files into multiple files"
txt_lassplit_intro = f"""{txt_lassplit_short} based on some criteria. By default it splits the points into separate files based on the ‘point source ID’ field that usually contains the flightline ID."""
txt_lasnoise_short = "Flags or removes noise points in LAS or LAZ files"
txt_lasnoise_intro = f"""{txt_lasnoise_short}. The tool looks for isolated points according to certain criteria that can be modified via ‘-step 3’ and ‘-isolated 3’ as needed. The default for step is 4 and for isolated is 5. It is possible to specify the xy and the z size of the 27 cells separately with ‘-step_xy 2’ and ‘-step_z 0.3’ which would create cells of size 2 by 2 by 0.3 units.
The tool tries to find points that have only few other points in their surrounding 3 by 3 by 3 grid of cells with the cell the respective point falls into being in the center. The size of each of the 27 cells is set with the ‘-step 5’ parameter. The maximal number of few other points in the 3 by 3 by 3 grid still designating a point as isolated is set with ‘-isolated 6’.
By default the noise points are given the classification code 7 (low or high noise). Using the ‘-remove_noise’ flag will instead remove them from the output file. Alternatively with the ‘-classify_as 31’ switch a different classification code can be selected. Another option is the ‘-flag_as_withheld’ switch which sets the withheld flag on the points identified as noise."""
txt_lasdiff_short = (
    "Compares the LIDAR data of two LAS/LAZ/ASCII files and reports whether they are identical or different"
)
txt_lasground_short = "Tool for bare-earth extraction"
txt_lasground_intro = f"""{txt_lasground_short}: It classifies the LiDAR points into ground points (class = 2) and non-ground points (class = 1). The tools works very well in natural environments such as mountains, forests, fields, hills, and even steep terrain but also gives excellent results in towns or cities."""
txt_lasgroundnew_short = "This is a redesigned tool for bare-earth extraction"
txt_lasgroundnew_intro = f"""{txt_lasgroundnew_short}. It classifies LIDAR points into ground points (class = 2) and non-ground points (class = 1). This is a totally redesigned version of lasground that handles complicated terrain much better where there are steep mountains nearby urban areas with many buildings."""
txt_lasclassify_short = "Classify buildings and high vegetation"
txt_lasclassify_intro = f"""{txt_lasclassify_short} (i.e. trees) in LAS/LAZ files. This tool requires that the bare-earth points have already been identified (e.g. with lasground) and that the elevation of each point above the ground was already computed with lasheight."""
txt_lasthin_short = "A simple LIDAR thinning algorithm"
txt_lasthin_intro = f"""{txt_lasthin_short} for LAS/LAZ/ASCII. It places a uniform grid over the points and within each grid cell keeps only the point with the lowest (or ‘-highest’) Z coordinate a -random’ point per cell or the most ‘-central’ one. When keeping ‘-random’ points you can in addition specify a ‘-seed 232’ for the random generator. Instead of removing the thinned out points from the output file you can also flag them with ‘-flag_as_withheld’ or ‘-flag_as_keypoint’. Then you can use the standard ‘-drop_withheld’ or ‘-keep_withheld’ filters to get either the thinned points or their complement.    """
txt_las2dem_short = "Triangulates LIDAR points from LAS/LAZ to TIN and DEM"
txt_las2dem_intro = f"""{txt_las2dem_short}. Triangulates LIDAR points from the LAS/LAZ format (or some ASCII format) into a temporary TIN and then rasters the TIN to create a DEM. The tool can either raster the ‘-elevation’, the ‘-slope’, the ‘-intensity’, the ‘-rgb’ values, or a ‘-hillshade’ or ‘-gray’ or ‘-false’ coloring. The output is either in BIL, ASC, IMG, FLT, XYZ, DTM, TIF, PNG or JPG format."""
txt_las2iso_short = "Extracts elevation contours to SHP/KML/WKT/TXT format"
txt_las2iso_intro = f"""{txt_las2iso_short}. The tool reads LIDAR points from LAS/LAZ/ASCII (or rasters from ASC/BIL/DTM format) and extracts a set of particular elevation contours in SHP/KML/WKT/TXT format. The user may specify to extract contours every 5 meters or only for individual elevation values. The contours can be smoothed or simplified on demand and hydro breaklines can be specified as well. las2iso can handle files up to about 20 mio. points."""
txt_lasgrid_short = "Raster huge LiDAR collections into grids by elevation, intensity or many other parameters"
txt_lasgrid_intro = f"""{txt_lasgrid_short}. The most important parameter ‘-step n’ specifies the n x n area that of LiDAR points that are gridded on one raster cell (or pixel). The output is either in BIL, ASC, IMG, TIF, PNG, JPG, XYZ, FLT, or DTM format. The tool can raster the ‘-elevation’ or the ‘-intensity’ of each point and stores the ‘-lowest’ or the ‘-highest’, the ‘-average’, or the standard deviation ‘-stddev’. Other gridding options are ‘-scan_angle_abs’, ‘-counter’, ‘-counter_16bit’, ‘-counter_32bit’, ‘-user_data’, ‘-point_source’, and others."""
txt_lasheight_short = "Computes the height of each point above the ground"
txt_lasheight_intro = f"""{txt_lasheight_short}. This assumes that grounds points have already been ground-classified (with standard classification 2 or selected with ‘-class 31’ or ‘-classification 8’) so they can be identified to construct a ground TIN. The ground points can also be in an separate file ‘-ground_points ground.las’ or ‘-ground_points dtm.csv -parse ssxyz’. By default the resulting heights are quantized, scaled with a factor of 10, clamped into an unsigned char between 0 and 255, and stored in the “user data” field of each point. Optional other target fields can be defined."""
txt_lasheight_class = "Extra parameters to classify by height above ground."
txt_lascanopy_short = "Computes common forestry metrics from height-normalized LiDAR point clouds"
txt_lascanopy_intro = f"""{txt_lascanopy_short}. It can compute canopy density or canopy cover (or gap fractions), height or intensity percentiles, averages, minima, maxima, kurtosis, skewness, standard deviation, and many more."""
txt_lascolor_short = "Colors LiDAR points based on imagery that is usually an ortho-photo"
txt_lascolor_intro = f"""{txt_lascolor_short}. The tool computes into which pixel a LAS point is falling and then sets the RGB values accordingly. Currently only the TIF format is supported. The world coordinates need to be either in GeoTIFF tags or in an accompanying *.tfw file."""
txt_blast2dem_short = "Rasters billions of LiDAR points via a streaming TIN to elevation, intensity, slope, or RGB grid"
txt_blast2dem_intro = f"""{txt_blast2dem_short}. blast2dem is almost identical to las2dem except that it can process much much larger inputs. While las2dem operates in-core and is therefore limited to a maximum of around 20 million points, blast2dem utilizes unique “streaming TIN” technology and can seamlessly process up to 2 billion points. This tool is part of the BLAST extension of LAStools.
"""
txt_blast2iso_short = "Contours billions of LiDAR points via a streaming TIN to isolines in KML or SHP format"
txt_blast2iso_intro = f"""{txt_blast2iso_short}. blast2iso is almost identical to las2iso except that it can extract elevation contours from much much larger inputs. While las2iso operates in-core and is therefore limited to a maximum of around 20 million points, blast2iso utilizes unique “streaming TIN” technology and can seamlessly process up to 2 billion points. This tool is part of the BLAST extension of LAStools."""
txt_lasinfo_short = "Report all content of a LAS/LAZ file header"
txt_lasinfo_intro = f"""{txt_lasinfo_short}. This is a handy tool report the contents of the header, the VLRs, and a short summary of the min and max values of the points for LAS/LAZ files. The tool warns when there is a difference between the header information and the point content for counters and bounding box extent."""
txt_lasoverlap_short = "Computes the flight line overlap and alignment of LIDAR points"
txt_lasoverlap_intro = f"""{txt_lasoverlap_short}. Reads LIDAR points from LAS/LAZ or ASCII files and computes the flight line overlap and/or the vertical and horizontal alignment. The output rasters can either be a color coded visual illustration of the level of overlap or the differences or the actual values and can be either in BIL, ASC, IMG, FLT, XYZ, DTM, TIF, PNG or JPG format."""
txt_lascontrol_short = "Computes the elevation of LiDAR data at specific x/y control points"
txt_lascontrol_intro = f"""{txt_lascontrol_short}. Reports the difference in respect to the control point elevation. The tool reads LiDAR in LAS/LAZ/ASCII format, triangulates the relevant points around the control points into a TIN."""
txt_lasduplicate_short = "Removes duplicate LiDAR points with identical x,y and optionally z coordinates"
txt_lasduplicate_intro = f"""{txt_lasduplicate_short}. In the default mode those are xy-duplicate points that have identical x and y coordinates. The first point survives, all subsequent duplicates are removed. It is also possible to keep the lowest points amongst all xy-duplicates via '-lowest_z'.
It is also possible to remove only xyz-duplicates points that have all x, y and z coordinates identical via '-unique_xyz'.
Another option is to identify '-nearby 0.005' points into one so that multiple returns within a specified distance become a single return. Given all pairs of points p1 and p2 (with p1 being before p2 in the file), point p2 will not be part of the output if these three conditions on their quantized coordinates are true
1. |p1.qx - p2.qx| <= 1
2. |p1.qy - p2.qy| <= 1
3. |p1.qz - p2.qz| <= 1
after quantizing them as follows based on the '-nearby d' value
  p1.qx = round(p1.x / d)     p2.qx = round(p2.x / d)
  p1.qy = round(p1.y / d)     p2.qy = round(p2.y / d)
  p1.qz = round(p1.z / d)     p2.qz = round(p2.z / d)
The special option '-single_returns' was added particularly to reconstruct the single versus multiple return information for the (unfortunate) case that the LiDAR points were delivered in two separate files with some points appearing in both. These LiDAR points may be split into all first return and all last returns or into all first returns and all ground returns. See the example below how to deal with this case correctly.<br>The removed points can also be recorded to a LAZ file with the option '-record_removed'."""
txt_lasprecision_short = "Finds the actual precision of LiDAR points and allows to correct the scaling if necessary"
txt_lasprecision_intro = f"""{txt_lasprecision_short}. Reads LIDAR data in the LAS/LAZ format and computes statistics that tell us whether the precision "advertised" in the header is really in the data."""
txt_lasvalidate_short = "Determine if LAS files conform to the ASPRS LAS specifications"
txt_lasvalidate_intro = """A simple tool to validate whether a single or a folder of LAS or LAZ files conform to the LAS specification of the ASPRS."""
txt_lasoptimize_short = "Optimize, compress and spatially index LiDAR files before distribution"
txt_lasoptimize_intro = f"""{txt_lasoptimize_short}.
Optimizes LiDAR stored in binary LAS or LAZ format (1.0 - 1.4) for better compression and spatial coherency. Especially useful prior to distributing LiDAR via data portals to lower bandwidth and storage but also accelerate subsequent exploitation.<br>In the default setting the tool will do the following:<br>- remove fluff in coordinate resolution (i.e. when all X, Y, or Z coordinates are multiples of 10, 100, or 1000).<br>- remove any additional padding in the LAS header or before the point block<br>- set nicely rounded offsets in the LAS header<br>- zero the contents of the user data field<br>- turn (sufficiently small) EVLRs into VLRs (LAS 1.4 only)<br>- rearrange points for better compression and spatial indexing<br>Arguments allows turning off the options."""
txt_lascopy_short = "Copies selected point attributes from a reference file to a target file"
txt_lascopy_intro = f"""{txt_lascopy_short}.
Merging the data is done by a match key. The key is GPS time and return number by default but can be also other or a combination of fields.
See the -match... arguments.<br>By default the selected attributes of the source points are copied to all target points if the two share the exact same combination of key values.
Selecting attributes to be copied is done by adding one or more '-copy_...' arguments. If no selection is made the classifications are copied.
By default the points from the target file that have no match in the source file remain unchanged unless the option '-zero' is used that set the selected attributes to 0 instead.
A simpler copy can be activated with option '-unmatched' which does not check for identical GPS-time and return number but simply copies the requested attribute in the order the point are in."""
txt_laspublish_short = "Creates a LiDAR portal for 3D visualization (and optionally also for downloading) of LAS and LAZ files in any modern Web browser"
txt_laspublish_intro = (
    f'{txt_laspublish_short} using the <a href="https://github.com/potree/potree">WebGL Potree</a> from Markus Schuetz.'
)
txt_lasview_short = "Simple and fast LiDAR visualization tool"
txt_lasview_intro = f"""
{txt_lasview_short} that has a number of neat little tricks that may surprise you. It can also edit the classification of the points as well as delete them.<br>As an optional viewer see <a href="https://rapidlasso.de/laslook">laslook</a>, the new GUI workbench for LAStools.
"""
txt_lasvoxel_short = "Computes various voxelizations for LiDAR point clouds"

# tools
lastool_info = {
    "LasZip": {
        "disp": "laszip (file)",
        "help": f"""
{txt_laszip_intro}
<h3>Parameters</h3>
{txt_inlazfile}
{txt_args("laszip")}
See <a href="https://downloads.rapidlasso.de/readme/lasindex_README.md">lasindex</a> about index files (*.lax).
{txt_verbose}
{txt_64bit}
{txt_laszip_outro}
{head_console_examples}
    {foe}laszip lake.las{fcc}<br>compresses LAS file "lake.las" to an lossless packed LAZ file overwriting any existing file.
    {foe}laszip lake.laz{fcc}<br>decompresses LAS file "lake.las" to an uncompressed LAS file overwriting any existing file.
""",
        "desc": f"{txt_laszip_intro}",
    },
    "LasZipPro": {
        "disp": "laszip (folder)",
        "help": f"""
{txt_laszip_intro}
{txt_folder}
<h3>Parameters</h3>
{txt_inlazdir}
{txt_args("laszip")}
See <a href="https://downloads.rapidlasso.de/readme/lasindex_README.md">lasindex</a> about index files (*.lax).
{txt_cores}
{txt_verbose}
{txt_64bit}
{txt_laszip_outro}
{head_console_examples}
    {foe}laszip *.las{fcc}<br>compresses all LAS files in the current folder overwriting any existing file.
    {foe}laszip *.laz{fcc}<br>decompresses all LAZ files in the current folder overwriting any existing file.
""",
        "desc": f"{txt_laszip_intro}",
    },
    "Las2LasFilter": {
        "disp": "las2las - filter (file)",
        "help": f"""
{txt_las2las_intro}
{txt_las2las_filter}.
<h3>Parameters</h3>
{txt_inlazfile}
{txt_filter_value}
{txt_args("las2las")}
{txt_verbose}
{txt_64bit}
{head_console_examples}
    {foe}las2las -i in.las -o out.las -keep_z 10 100{fcc}<br>keeps points of in.las whose double-precision elevations falls inside the range 10 to 100 and stores these points to out.las.
    {foe}las2las -i in.las -o out.laz -drop_return 1{fcc}<br>drops all points of in.las that are designated first returns by the value in their return_number field and stores surviving points compressed to out.laz.
    {foe}las2las -i in.laz -o out.las -drop_scan_angle_above 15{fcc}<br>drops all points of compressed in.laz whose scan angle is above 15 or below -15 and stores surviving points compressed to out.laz.
    {foe}las2las -i in.las -o out.las -drop_intensity_below 1000 -remove_padding{fcc}<br>drops all points of in.las whose intensity is below 1000 and stores surviving points to out.las. In addition any additional user data after the LAS header or after the VLR block are stripped from the file.
    {foe}las2las -i in.laz -o out.laz -last_only{fcc}<br>extracts all last return points from compressed in.laz and stores them compressed to out.laz.
    {foe}las2las -i in.las -o out.las -keep_class 2 -keep_class 3{fcc}<br>{foe}las2las -i in.las -o out.las -keep_class 2 3{fcc}<br>extracts all points classfied as 2 or 3 from in.las and stores them to out.las.
    {foe}las2las -i in.las -o out.las -keep_XY 63025000 483450000 63050000 483475000{fcc}<br>similar to '-keep_xy' but uses the integer values point.X and point.Y that the points are stored with for the checks (and not the double precision floating point coordinates they represent). drops all the points of in.las that have point.X<63025000 or point.Y<483450000 or point.X>63050000 or point.Y>483475000 and stores surviving points to out.las (use lasinfo.exe to see the range of point.Z and point.Y).
    {foe}las2las -i in.las -o out.las -keep_Z 1000 4000{fcc}<br>similar to '-keep_z' but uses the integer values point.Z that the points are stored with for the checks (and not the double-precision floating point coordinates they represent). drops all the points of in.las that have point.Z<1000 or point.Z>4000 and stores all surviving points to out.las (use lasinfo.exe to see the range of point.Z).
        """,
        "desc": f"{txt_las2las_filter}",
    },
    "Las2LasProFilter": {
        "disp": "las2las - filter (folder)",
        "help": f"""
{txt_las2las_intro}
{txt_las2las_filter}.
{txt_folder}
<h3>Parameters</h3>
{txt_inlazdir}
{txt_filter_value}
{txt_args("las2las")}
{txt_cores}
{txt_verbose}
{txt_64bit}
{head_console_examples}
    {foe}las2las -i *.las -o *.las -keep_z 10 100{fcc}<br>copy all input files to an output file but keep only z values between 10 and 100.
        """,
        "desc": f"{txt_las2las_filter}",
    },
    "Las2LasProject": {
        "disp": "las2las - projection (file)",
        "help": f"""
{txt_las2las_intro}
{txt_las2las_project}.
<h3>Parameters</h3>
{txt_inlazfile}
{txt_proj}
{txt_args("las2las")}
{txt_verbose}
{txt_64bit}
{head_console_examples}
    {foe}las2las -i in.laz -target_epsg 2972 -o out.laz{fcc}<br>copy file and add the given epsg georeferencing to the target.
        """,
        "desc": f"{txt_las2las_project}",
    },
    "Las2LasProProject": {
        "disp": "las2las - projection (folder)",
        "help": f"""
{txt_las2las_intro}
{txt_las2las_project}.
{txt_folder}
<h3>Parameters</h3>
{txt_inlazdir}
{txt_proj}
{txt_args("las2las")}
{txt_cores}
{txt_verbose}
{txt_64bit}
{head_console_examples}
    {foe}las2las -i *.laz -target_epsg 2972 -odir out -olaz{fcc}<br>copy all input files and add the given epsg georeferencing to the target files.
                """,
        "desc": f"{txt_las2las_project}",
    },
    "Las2LasTransform": {
        "disp": "las2las - transform (file)",
        "help": f"""
{txt_las2las_intro}
{txt_las2las_trans}.
<h3>Parameters</h3>
{txt_inlazfile}
{txt_transform}
{txt_args("las2las")}
{txt_verbose}
{txt_64bit}
{head_console_examples}
{foe}las2las -i in.laz -translate_xyz 1 2 3 -o out.laz{fcc}<br>translate point coordinates by 1 2 3 units.
{foe}las2las -i in.laz -rotate_xy 90 50 6000 -o out.laz{fcc}<br>rotate all points by 90 degrees around the z axis center at 50 6000.{foe}las2las -i in.las -o out.las -scale_rgb_up{fcc}<br>multiplies all rgb values in the file with 256. this is used to scale the rgb values from standard unsigned char range (0 ... 255) to the unsigned short range (0 ... 65535) used in the LAS format.
{foe}las2las -i in.laz -o out.laz -scale_rgb_down{fcc}<br>does the opposite with compressed input and output files""",
        "desc": f"{txt_las2las_trans}",
    },
    "Las2LasProTransform": {
        "disp": "las2las - transform (folder)",
        "help": f"""
{txt_las2las_intro}
{txt_las2las_trans}.
{txt_folder}
<h3>Parameters</h3>
{txt_inlazdir}
{txt_transform}
{txt_args("las2las")}
{txt_cores}
{txt_verbose}
{txt_64bit}
{head_console_examples}
{foe}las2las -i *.laz -translate_xyz 1 2 3 -odir out -olaz{fcc}<br>translate point coordinates of all input files by 1 2 3 units and save the result to the 'out' directory as compressed LAZ files.
{foe}las2las -i *.laz -rotate_xy 90 50 6000 -odir out -olaz{fcc}<br>rotate the points of all input files by 90 degrees around the z axis center at 50 6000 and save the result to the 'out' directory as compressed LAZ files.""",
        "desc": f"{txt_las2las_trans}",
    },
    "Las2Shp": {
        "disp": "las2shp",
        "help": f"""
{txt_las2shp_short}.
<h3>Parameters</h3>
{txt_inlazfile}
{fop}use PointZ instead of MultiPointZ:{fcc} Create PointZ records instead of MultiPointZ records (-single_points).
{fop}number of points per record:{fcc} Set argument "-record" value.
{txt_args("las2shp")}
{txt_verbose}
{txt_64bit}
{head_console_examples}
{foe}las2shp -i lidar.laz -o shapefile.shp -record 2048{fcc}<br>converts the LAZ file 'lidar.las' to ESRI's Shapefile 'shapefile.shp' using MultiPointZ records containing 2048 points each.
{foe}las2shp -lof file_list.txt -merged -o lidar.shp -record 2048{fcc}<br>converts the contents of all LAS files listed in 'file_list.txt' to ESRI's Shapefile format 'lidar.shp' using MultiPointZ records containing 2048 points each.""",
        "desc": f"{txt_las2shp_short}",
    },
    "LasPlanes": {
        "disp": "lasplanes",
        "help": f"""Finds sufficiently planar patches of LAS/LAZ points fulfilling a number of user-defineable criteria that are output as simple polygons to SHP or RIEGL's PEF format. The tool was originally designed for generating tie planes to match the point clouds of a mobile scan that suffer from errors in the GPS trajectory to accurate terrestrial scans using clean planar patches that are "seen" without obstruction by both scanners.<br>The algorithm divides the input into cells that are n by n by n units big. It then performs an eigen value decomposition of the covariance matrix of the points in each cell that has more than the minimal number of points. The three eigenvalues have to pass the small_eigen_max, middle_eigen_min, eigen_ratio_smallest, and eigen_ratio_largest criteria. And the plane of points must be sufficiently thin and formed by sufficiently many points after removing no more than a certain percentage of them. Then a polygon with a maximal number of points enclosing a subset of the points is formed that is checked for having a minimal size and a maximal off-planar standard deviation. The surviving planes are output (optionally only if they are sufficiently far from another).
<h3>Parameters</h3>
{txt_inlazfile}
{txt_args("lasplanes")}
{txt_verbose}
{txt_64bit}
{head_console_examples}
{foe}lasplanes64 -i terrestrial_scan.laz -o planes.pef{fcc}<br>finds all planar patches in the file 'terrestrial_scan.laz' and stores the result in RIEGL's PEF format
{foe}lasplanes64 -i terrestrial_scan.laz -o planes.shp{fcc}<br>same as above but outputting the SHP format""",
        "desc": f"{txt_lasplanes_short}",
    },
    "Las2txt": {
        "disp": "las2txt (file)",
        "help": f"""
{txt_las2txt_intro}
<h3>Parameters</h3>
{txt_inlazfile}
{txt_parse}
{fop}write column description:{fcc} write a header line to the output containing the column description (this enables to omit -parse during import using txt2las)
{txt_args("las2txt")}
{txt_verbose}
{txt_64bit}
{head_console_examples}
    {foe}las2txt64 -i in.laz -o out.txt -parse xyzit{fcc}<br>converts in.laz to text by placing the x, y, and z coordinate of each point as the 1st, 2nd, and 3rd entries, the intensity as the 4th entry, and the gps_time as the 5th entry of each line.
            """,
        "desc": f"{txt_las2txt_short}",
    },
    "Las2txtPro": {
        "disp": "las2txt (folder)",
        "help": f"""
{txt_las2txt_intro}
{txt_folder}
<h3>Parameters</h3>
{txt_inlazdir}
{txt_parse}
{fop}write column description:{fcc} write a header line to the output containing the column description (this enables to omit -parse during import using txt2las)
{txt_args("las2txt")}
{txt_cores}
{txt_verbose}
{txt_64bit}
{head_console_examples}
{foe}las2txt64 -i *.laz -odir output -parse xyzit{fcc}<br>converts all LAZ files in the directory to plain text using the given parse logic.
    """,
        "desc": f"{txt_las2txt_short}",
    },
    "Shp2Las": {
        "disp": "shp2las",
        "help": f"""
{txt_shp2las_short}.<br>Expected input are in shape type [1,11,21,8,18,28].
<h3>Parameters</h3>
{txt_inshpfile}
{txt_resolution}
{fop}resolution of x and y coordinate:{fcc} set input scale to quantize points
{fop}resolution of z coordinate:{fcc} set z scale to quantize points
{txt_args("shp2las")}
{txt_verbose}
{head_console_examples}
    {foe}shp2las -set_scale 0.001 0.001 0.001 -i lidar.shp -o lidar.las{fcc}<br>converts 'lidar.shp' to the LAS file 'lidar.las' with the specified scale
                """,
        "desc": f"{txt_shp2las_short}",
    },
    "Txt2Las": {
        "disp": "txt2las (file)",
        "help": f"""
{txt_txt2las_intro}
<h3>Parameters</h3>
{txt_inlazfile}
{txt_parse}
{txt_resolution}
{txt_proj}
{txt_args("txt2las")}
{txt_verbose}
{txt_64bit}
{head_console_examples}
    {foe}txt2las -i file.txt -o out.laz{fcc}<br>read the textfile and convert it to a LAZ file. Expect the first row as column headers to identify the target field.
    {foe}txt2las -i file.txt -o out.laz -parse xyzai -scale_scan_angle 57.3 -scale_intensity 65535{fcc}<br>read the textfile with x y z scan angle (multiplied by 57.3; radian to angle) and the 5th entry as the intensity and multiplies it by 65535 (converts range [0.0 .. 1.0] to range [0 .. 65535]. Output as compressed LAZ file.
        """,
        "desc": f"{txt_txt2las_short}",
    },
    "Txt2LasPro": {
        "disp": "txt2las (folder)",
        "help": f"""
{txt_las2txt_intro}
{txt_folder}
<h3>Parameters</h3>
{txt_inlazdir}
{txt_parse}
{txt_resolution}
{txt_proj}
{txt_args("txt2las")}
{txt_cores}
{txt_verbose}
{txt_64bit}
{head_console_examples}
    {foe}txt2las -skip 3 -i *.txt.gz -odir out -olaz -parse txyzsa -sp83 OH_N{fcc}<br>converts all gzipped ASCII files and uses the 1st entry of each line as the gps time, the 3rd, 4th, and 5th entry as the x, y, and z coordinate of each point, and the 6th entry as the scan angle. It skips the first three lines of the ASCII data file and adds projection info for state plane ohio north with nad83.
        """,
        "desc": f"{txt_txt2las_short}",
    },
    "e572las": {
        "disp": "e572las",
        "help": f"""
{txt_e572las_intro}
<h3>Parameters</h3>
{txt_inlazfile}
{txt_args("e572las")}
{txt_verbose}
{txt_64bit}
{head_console_examples}
    {foe}e572las -i file.txt -o out.laz{fcc}<br>read the textfile and convert it to a LAZ file. Expect the first row as column headers to identify the target field.
    {foe}e572las -i file.txt -o out.laz -parse xyzai -scale_scan_angle 57.3 -scale_intensity 65535{fcc}<br>read the textfile with x y z scan angle (multiplied by 57.3; radian to angle) and the 5th entry as the intensity and multiplies it by 65535 (converts range [0.0 .. 1.0] to range [0 .. 65535]. Output as compressed LAZ file.
        """,
        "desc": f"{txt_e572las_short}",
    },
    "LasOptimize": {
        "disp": "lasoptimize",
        "help": f"""
{txt_lasoptimize_intro}
<h3>Parameters</h3>
{txt_inlazfile}
{txt_args("lasoptimize")}
{txt_verbose}
{txt_64bit}
{head_console_examples}
    {foe}lasoptimize64 -i final\*.laz -odir optimized{fcc}<br>optimizes all LAZ files in the 'final' folder to the 'optimized' folder while over-writing any existing file.
    {foe}lasoptimize64 -i final\*.laz -scanner_channel_in_point_source_ID -odir optimized{fcc}<br>optimizes all LAZ files in the 'final' folder to the 'optimized' folder while over-writing any existing file. The files are from a multi-beam system and the scanner channel is encoded into the flightline number that is stored in the 'pount source ID' field of each point.""",
        "desc": f"{txt_lasoptimize_short}",
    },
    "LasCopy": {
        "disp": "lascopy",
        "help": f"""
{txt_lascopy_intro}
<h3>Parameters</h3>
{txt_inlazfile}
{fop}merge...:{fcc} set merge attributes
{fop}copy...:{fcc} set copy attributes
{fop}zero target if not found in source:{fcc} set target copy field to zero if not found in source data
{fop}copy attributes by point order:{fcc} copy attributes from source to target by point order (no attribute matching)
More merge and copy arguments see README file.
{txt_args("lascopy")}
{txt_verbose}
{txt_64bit}
{head_console_examples}
{foe}lascopy64 -i source.laz -i target.laz -o result.laz{fcc}<br>Copies all classifications from source.laz to target.laz where gps time and return number matches.
{foe}lascopy64 -i source.laz -i target.laz -o result.laz -match_point_source_id{fcc}<br>Copies all classifications from source.laz to target.laz where gps time and point_source_id matches.
{foe}lascopy64 -i source.laz -i target.laz -o result.laz -match_xy 0.5 -elevation -zero{fcc}<br>Copies all z-values from source.laz to target.laz where a matching point within 0.5 units in source exists. Set all other z-values to 0.""",
        "desc": f"{txt_lascopy_short}",
    },
    "Las3dPolyHorizontalVerticalDistance": {
        "disp": "las3dpoly (horizontal and vertical distance)",
        "help": f"""
{txt_las3dpoly_xy_short}
{txt_las3dpoly_intro}
<h3>Parameters</h3>
{txt_inlazfile}
{txt_inpolyfile}
{fop}vertical distance:{fcc} Vertical distance to polygon to match points
{fop}horizontal distance:{fcc} Horizontal distance to polygon to match points
{txt_args("las3dpoly")}
{txt_verbose}
{txt_64bit}
{head_console_examples}
{foe}las3dpoly -i in.laz -poly line.csv -distance 10 20 -o out.laz -remove_points{fcc}<br>clip away all points of in.laz which are less than 10 units vertically and 20 units horizontal from the line specified by line.csv""",
        "desc": f"{txt_las3dpoly_xy_short}",
    },
    "Las3dPolyRadialDistance": {
        "disp": "las3dpoly (Radial Distance)",
        "help": f"""
{txt_las3dpoly_rad_short}
{txt_las3dpoly_intro}
<h3>Parameters</h3>
{txt_inlazfile}
{fop}radial distance:{fcc} radial distance to polygon to match points
{txt_args("las3dpoly")}
{txt_verbose}
{txt_64bit}
{head_console_examples}
    {foe}las3dpoly -i in.laz -poly line.shp -o out.laz -distance 10 -classify_as 13 -v{fcc}<br>classify all points within the result file as class 13 if they are within radial distance=10 to the line specified by line.shp and list a verbose report of what has been done.
                """,
        "desc": f"{txt_las3dpoly_rad_short}",
    },
    "LasDistance": {
        "disp": "lasdistance",
        "help": f"""
{txt_lasdistance_short}
{txt_lasdistance_intro}
<h3>Parameters</h3>
{txt_inlazfile}
{fop}poly:{fcc} use this file as source for polygonal segments
{fop}distance_xy:{fcc} use distance from polygons to classify, flag or remove points
{fop}classify_as:{fcc} classify points within distance as this class instead of clip away
{txt_args("lasdistance")}
{txt_verbose}
{txt_64bit}
{head_console_examples}
{foe}lasdistance64 -i in.laz -poly breaklines.shp -o out.laz{fcc}
{foe}lasdistance64 -i in.laz -poly breaklines.shp -distance_xy 5.0 -o out.laz{fcc}
{foe}lasdistance64 -i in.laz -poly breaklines.shp -distance_xy 0.5 -classify_as 6 -o out.laz{fcc}""",
        "desc": f"{txt_lasdistance_short}",
    },
    "LasBoundary": {
        "disp": "lasboundary (file)",
        "help": f"""
{txt_lasboundary_intro}
<h3>Parameters</h3>
{txt_inlazfile}
{txt_filter}
{txt_boundary}
{txt_args("lasboundary")}
{txt_verbose}
{txt_64bit}
{head_console_examples}
{foe}lasboundary -i lidar1.laz lidar2.laz -merged -o lidar_boundary.shp{fcc}<br>computes the boundary of the data created from merging 'lidar1.laz' and 'lidar2.laz' and stores the result to 'lidar_boundary.shp'.
                """,
        "desc": f"{txt_lasboundary_short}",
    },
    "LasBoundaryPro": {
        "disp": "lasboundary (folder)",
        "help": f"""
{txt_lasboundary_intro}
{txt_folder}
<h3>Parameters</h3>
{txt_inlazdir}
{txt_filter}
{txt_boundary}
{txt_args("lasboundary")}
{txt_cores}
{txt_verbose}
{txt_64bit}
{head_console_examples}
{foe}lasboundary -i *.laz -merged -o lidar_boundary.shp{fcc}<br>computes the boundary of all LAZ files in the directory and stores the result to 'lidar_boundary.shp'.
                """,
        "desc": f"{txt_lasboundary_short}",
    },
    "LasClip": {
        "disp": "lasclip",
        "help": f"""
{txt_lasclip_short}
Takes as input a LAS/LAZ/TXT file and a SHP/TXT file with one or many polygons (e.g. building footprints or flight lines), clips away all the points that fall outside all polygons (or inside some polygon), and stores the surviving points to the output LAS/LAZ/TXT file. Instead of clipping the points they can also be classified.
<h3>Parameters</h3>
{txt_inlazfile}
{txt_inshpfile}
{fop}interior:{fcc} clip points INSIDE the polygons
{txt_args("lasclip")}
{txt_verbose}
{txt_64bit}
{head_console_examples}
    {foe}lasclip -i *.laz -poly polygon.shp -v -olaz{fcc}<br>clips all the LAS files matching "*.laz" against the polygon(s) in  "polygon.shp" and stores each result to a LAS file called "*_1.laz".
                """,
        "desc": f"{txt_lasclip_short}",
    },
    "LasReturn": {
        "disp": "lasreturn (file)",
        "help": f"""
{txt_lasreturn_intro}
<h3>Parameters</h3>
{txt_inlazfile}
{fop}print histogram about returns:{fcc} print histogram about missing or duplicate returns
{fop}adds attribute 'gap to next return':{fcc} adds an attribute 'gap to next return' as "extra bytes" and stores the 3D distance from the current to the next return of the same pulse for all pulses that have multiple returns
{fop}repair invalid number of returns:{fcc} repair invalid number of return values
{fop}skip incomplete returns:{fcc} skip incomplete returns
{txt_args("lasreturn")}
{txt_verbose}
{txt_64bit}
{head_console_examples}
{foe}lasreturn64 -i lidar.laz -repair_number_of_returns -odix _repaired -olaz{fcc}<br>the 'number of returns' field of every point is set to the highest return number that is found for each set of returns with the same unique GPS time stamp. assumes sorted input (use lassort -gps_time).
{foe}lasreturn64 -i lidar.laz -compute_gap_to_next_return -odix _gaps -olaz{fcc}<br>adds an additional per point attribute called 'gap to next return [m]' as "extra bytes". it stores the 3D distance from the current to the next return of the same pulse for all pulses that have multiple return in the file. returns belonging to the same pulse are identified via their matching GPS time stamps. the computation assumes sorted input and will exit if this is not the case (use lassort -gps_time).
{foe}lasreturn64 -i lidar.laz -histo return_distance 0.1{fcc}<br>computes the distances between all subsequent returns from the same pulse and prints a histogram with bin size 0.1 meter. assumes sorted input (use lassort -gps_time).
{foe}lasreturn64 -i lidar.laz -histo return_distance 0.1 0.0 4.99{fcc}<br>same as before but limits the histogram to the range rfrom 0 to 5""",
        "desc": f"{txt_lasreturn_short}",
    },
    "LasReturnPro": {
        "disp": "lasreturn (folder)",
        "help": f"""
{txt_lasreturn_intro}
<h3>Parameters</h3>
{txt_inlazfile}
{fop}print histogram about returns:{fcc} print histogram about missing or duplicate returns
{fop}adds attribute 'gap to next return':{fcc} adds an attribute 'gap to next return' as "extra bytes" and stores the 3D distance from the current to the next return of the same pulse for all pulses that have multiple returns
{fop}repair invalid number of returns:{fcc} repair invalid number of return values
{fop}skip incomplete returns:{fcc} skip incomplete returns
{txt_args("lasreturn")}
{txt_verbose}
{txt_64bit}
{head_console_examples}
{foe}lasreturn64 -i *.laz -repair_number_of_returns -odir repaired -olaz{fcc}<br>the 'number of returns' field of every point in every file is set to the highest return number that is found for each set of returns with the same unique GPS time stamp. assumes sorted input (use lassort -gps_time).""",
        "desc": f"{txt_lasreturn_short}",
    },
    "LasSort": {
        "disp": "lassort (file)",
        "help": f"""
{txt_lassort_intro}
<h3>Parameters</h3>
{txt_inlazfile}
{txt_args("lassort")}
{txt_verbose}
{txt_64bit}
{head_console_examples}
{foe}lassort64 *.laz{fcc}<br>z-orders all LAZ files with a default bucket size.""",
        "desc": "txt_lassort_short",
    },
    "LasSortPro": {
        "disp": "lassort (folder)",
        "help": f"""
{txt_lassort_intro}
{txt_folder}
<h3>Parameters</h3>
{txt_inlazdir}
{txt_args("lassort")}
{txt_cores}
{txt_verbose}
{txt_64bit}
{head_console_examples}
{foe}lassort64 flight1*.las flight2*.las -gps_time{fcc}<br>sorts all LAS files by their GPS time
{foe}lassort64 *.las -olaz -point_source{fcc}<br>sorts all LAS files by their point source ID and stores them compressed""",
        "desc": "txt_lassort_short",
    },
    "LasDiff": {
        "disp": "lasdiff",
        "help": f"""
{txt_lasdiff_short}
<h3>Parameters</h3>
{txt_inlazfile}
{txt_inlazother}
{txt_args("lasdiff")}
{txt_verbose}
{txt_64bit}
{head_console_examples}
{foe}lasdiff -i a.laz -i b.laz -o diff.laz{fcc}<br>compare the 2 input files and create a difference file as output.
                """,
        "desc": f"{txt_lasdiff_short}",
    },
    "LasIndex": {
        "disp": "lasindex (file)",
        "help": f"""
{txt_index_intro}
<h3>Parameters</h3>
{txt_inlazfile}
{txt_args("lasindex")}
{txt_verbose}
{txt_64bit}
{head_console_examples}
    {foe}lasindex -i in.laz{fcc}<br>creates a spatial indexing file called 'in.lax' that need to be in the same folder as the file 'in.laz' to be useful. If you modify the spatial location, the number of points, or their order in the file then you need to recreate the LAX file.
    {foe}lasindex -i in.laz -append{fcc}<br>same as above but append the index to the LAZ file (only LAZ files).
                """,
        "desc": "txt_lasindex_short",
    },
    "LasIndexPro": {
        "disp": "lasindex (folder)",
        "help": f"""
{txt_index_intro}
{txt_folder}
<h3>Parameters</h3>
{txt_inlazdir}
{txt_args("lasindex")}
{txt_cores}
{txt_verbose}
{txt_64bit}
{head_console_examples}
    {foe}lasindex -i *.laz -dont_reindex{fcc}<br>creates a spatial indexing file for all LAZ files that do not yet have a LAX file yet.
                """,
        "desc": "txt_lasindex_short",
    },
    "LasProbe": {
        "disp": "lasprobe",
        "help": f"""
{txt_lasprobe_short}.
The tool reads LIDAR in LAS/LAZ/ASCII format, triangulates the relevant points into a TIN. For classified data sets containing a mix of ground and vegetation/building points it is imperative to specify the points which should be used for this calclation (i.e. usually '-keep_class 2' or '-keep_class 2 8').<br>The tool collects all LiDAR points that are within 'step' meters of the probed location. This can be changed with the '-step 2' parameter which would shrink this circle to a radius to 2 meters.<br>If the LiDAR is spatially indexed (i.e. a *.lax file exists) this collection of points will be accelerated significanly. For repeat probing running lasindex before lasprobe is recommended.
The output report defaults to stdout unless you specify an output file with '-o report.txt'. Standard output is only the z (elevation) value, unless you add '-xyz' to the command line so that all coordinates will be written.
<h3>Parameters</h3>
{txt_inlazfile}
{foe}probe at x pos{fcc}: x position of probe
{foe}probe at y pos{fcc}: y position of probe
{foe}step radius{fcc}: step radius to catch points at probe location
{foe}output xyz value{fcc}: output xyz value instead of only elevation value
{foe}Result file{fcc}: write result into this file (stdout otherwise)
{txt_args("lasprobe")}
{txt_verbose}
{txt_64bit}
{head_console_examples}
{foe}lasprobe64 -i ..\data\fusa.laz -probe 277760.00 6122260 52.14{fcc}<br>probes all LiDAR points including buildings, wires and vegetation and outputs the computed elevation "52.14" to stdout
{foe}lasprobe64 -i ..\data\fusa.laz -probe 277760.00 6122260 -o mist.txt{fcc}<br>probes all LiDAR points including buildings, wires and vegetation and outputs the computed elevation "52.14" to text file 'mist.txt'""",
        "desc": "txt_lasprobe_short",
    },
    "LasIntensity": {
        "disp": "lasintensity",
        "help": f"""
        {txt_lasintensity_intro}
<h3>Parameters</h3>
{txt_inlazfile}
{fop}scanner altitude in [km]:{fcc} Argument '-scanner_height'
{fop}atmospheric visibility range in [km]:{fcc} Argument '-av'
{fop}laser wavelength in [µm]:{fcc} Argument '-w'
{txt_args("lasintensity")}
{txt_verbose}
{txt_64bit}
                """,
        "desc": f"{txt_lasintensity_short}",
    },
    "LasIntensityAttenuationFactor": {
        "disp": "lasintensity (attenuation factor)",
        "help": f"""
        {txt_lasintensity_intro}
<h3>Parameters</h3>
{txt_inlazfile}
{fop}scanner altitude in [km]:{fcc} Argument '-scanner_height'
{fop}attenuation coefficient in [km^-1]:{fcc} Argument '-a'
{txt_args("lasintensity")}
{txt_verbose}
{txt_64bit}
                """,
        "desc": f"{txt_lasintensity_short}",
    },
    "LasMerge": {
        "disp": "lasmerge (file)",
        "help": f"""
{txt_merge_intro}
<h3>Parameters</h3>
{txt_inlazfile}
{fop}2nd file...:{fcc} Other files to merge.
{txt_args("lasmerge")}
{txt_verbose}
{txt_64bit}
{head_console_examples}
    {foe}lasmerge -i big.txt -iparse xyzt -o out000.laz -split 500000000{fcc}<br>split the text file big.txt that could, for example, contain 25 billion points into several compressed output LAZ files that contain 500 million points each that are called out000.laz, out001.laz, out002.laz, out003.laz, ...
                """,
        "desc": f"{txt_merge_short}",
    },
    "LasMergePro": {
        "disp": "lasmerge (folder)",
        "help": f"""
{txt_merge_intro}
{txt_folder}
<h3>Parameters</h3>
{txt_inlazdir}
{txt_args("lasmerge")}
{txt_cores}
{txt_verbose}
{txt_64bit}
{head_console_examples}
    {foe}lasmerge -i *.las -o out0000.laz -split 1000000000{fcc}<br>merge all *.las files into one and then split it into several output files that contain one billion points each and that are called out0000.las, out0001.las, out0002.las, out0003.las, ...
                """,
        "desc": f"{txt_merge_short}",
    },
    "LasNoise": {
        "disp": "lasnoise (file)",
        "help": f"""
{txt_lasnoise_intro}
<h3>Parameters</h3>
{txt_inlazfile}
{txt_args("lasnoise")}
{txt_verbose}
{txt_64bit}
{head_console_examples}
    {foe}lasnoise -i lidar.las -remove_noise -ignore_class 2 -o lidar_without_noise.laz{fcc}<br>removes all points - except those classified as 2 (ground) - that have only 5 or fewer other points in their surrounding 3 by 3 by 3 grid (with the respective point in the center cell) where each cell is 4 by 4 by 4 meters in size.
                """,
        "desc": f"{txt_lasnoise_intro}",
    },
    "LasNoisePro": {
        "disp": "lasnoise (folder)",
        "help": f"""
{txt_lasnoise_intro}
{txt_folder}
<h3>Parameters</h3>
{txt_inlazdir}
{txt_args("lasnoise")}
{txt_cores}
{txt_verbose}
{txt_64bit}
{head_console_examples}
    {foe}lasnoise -i tiles\*.laz -step 2 -isolated 3 -odix _denoised -olaz -cores 6 -cpu64{fcc}<br>classifies all points that have only 3 or fewer other points in their surrounding 3 by 3 by 3 grid (with the respective point in the center cell) where each cell is 2 by 2 by 2 meters in size as classification code 7 (default).
                """,
        "desc": f"{txt_lasnoise_intro}",
    },
    "LasOverage": {
        "disp": "lasoverage (file)",
        "help": f"""
{txt_lasoverage_intro}
<h3>Parameters</h3>
{txt_inlazfile}
{txt_args("lasoverage")}
{txt_verbose}
{txt_64bit}
{head_console_examples}
    {foe}lasoverage -i tile.las -step 2 -o tile_overage.laz{fcc}<br>finds the overlap points and classifies them as 12 for a LAS tile with a point spacing of around 1.0 meters. For this to work, the LiDAR points in the LAS file have their point source ID populated with the flight line number. The output is also compressed.
                """,
        "desc": f"{txt_lasoverage_short}",
    },
    "LasOveragePro": {
        "disp": "lasoverage (folder)",
        "help": f"""
{txt_lasoverage_intro}
{txt_folder}
<h3>Parameters</h3>
{txt_inlazdir}
{txt_args("lasoverage")}
{txt_cores}
{txt_verbose}
{txt_64bit}
{head_console_examples}
    {foe}lasoverage -i tiles\tile_*.laz -step 2 -recover_flightlines -flag_as_withheld -cores 4 -odix _flagged -olaz{fcc}<br>finds the overlap points and classifies them as 12 for all LAZ input files with a point spacing of around 1.0 meters.<br>Try to reconstruct flightline information in an initial pass over the points by looking for continuous intervals of GPS time stamps and by operating on 4 cores.
                """,
        "desc": f"{txt_lasoverage_short}",
    },
    "LasSplit": {
        "disp": "lassplit",
        "help": f"""
{txt_lassplit_intro}
<h3>Parameters</h3>
{txt_inlazfile}
{txt_args("lassplit")}
{txt_verbose}
{txt_64bit}
                """,
        "desc": f"{txt_lassplit_short}",
    },
    "LasTile": {
        "disp": "lastile (file)",
        "help": f"""
{txt_lastile_intro}
<h3>Parameters</h3>
{txt_inlazfile}
{txt_tile}
{txt_args("lastile")}
{txt_verbose}
{txt_64bit}
{head_console_examples}
    {foe}lastile -i large.laz -tile_size 500 -buffer 10 -reversible -o tile.laz{fcc}<br>{foe}lastile -i tile_*.laz -reverse_tiling -o large_reversed.laz{fcc}
tiles file 'large.laz' with tile size 500 and buffer 10 in reversible mode. the second command removes all buffer points, reconstructs the original point order, and stored the result as 'large_reversed.laz'.
                """,
        "desc": f"{txt_lastile_short}",
    },
    "LasTilePro": {
        "disp": "lastile (folder)",
        "help": f"""
{txt_lastile_intro}
{txt_folder}
<h3>Parameters</h3>
{txt_inlazdir}
{txt_tile}
{txt_args("lastile")}
{txt_cores}
{txt_verbose}
{txt_64bit}
{head_console_examples}
    {foe}lasindex -i *.laz -cores 8{fcc}<br>lastile -i *.laz -files_are_flightlines -buffer 25 -o tiles\tile.laz -cores 4 spatially indexes all compressed LAZ files and then tiles them on 4 cores using the default tile size of 1000 and a buffer of 25 while setting the point source ID of each point to the file number it is from.
""",
        "desc": f"{txt_lastile_short}",
    },
    "LasClassify": {
        "disp": "lasclassify (file)",
        "help": f"""
{txt_lasclassify_intro}
<h3>Parameters</h3>
{txt_inlazfile}
{txt_args("lasclassify")}
{txt_verbose}
{txt_64bit}
{head_console_examples}
    {foe}lasground -i lidar.laz -o lidar_with_bare_earth.laz -city{fcc}
    {foe}lasheight -i lidar_with_bare_earth.laz -o lidar_with_heights.laz{fcc}
    {foe}lasclassify -i lidar_with_heights.laz -o lidar_classified.laz{fcc}<br>finds the ground points with lasground, computes the height of each point with lasheight, and classifies buildings and high vegetation with the default settings.
                """,
        "desc": f"{txt_lasclassify_short}",
    },
    "LasClassifyPro": {
        "disp": "lasclassify (folder)",
        "help": f"""
{txt_lasclassify_intro}
{txt_folder}
<h3>Parameters</h3>
{txt_inlazdir}
{txt_args("lasclassify")}
{txt_cores}
{txt_verbose}
{txt_64bit}
{head_console_examples}
    {foe}lasclassify -i *.laz{fcc}<br>classifies all LAZ files with the default settings (the LAZ files need to already have ground points classified and point heigths computed).
                """,
        "desc": f"{txt_lasclassify_short}",
    },
    "LasGround": {
        "disp": "lasground (file)",
        "help": f"""
{txt_lasground_intro}
<h3>Parameters</h3>
{txt_inlazfile}
{txt_args("lasground")}
{txt_verbose}
{txt_64bit}
{head_console_examples}
    {foe}lasground -i terrain.laz -o classified_terrain.laz -all_returns{fcc}<br>classifies a terrain considering all points - not just the last returns (as is the default behavior).
                """,
        "desc": f"{txt_lasground_short}",
    },
    "LasGroundPro": {
        "disp": "lasground (folder)",
        "help": f"""
{txt_lasground_intro}
{txt_folder}
<h3>Parameters</h3>
{txt_inlazdir}
{txt_args("lasground")}
{txt_cores}
{txt_verbose}
{txt_64bit}
{head_console_examples}
    {foe}lasground -i *.laz -odir ground -all_returns{fcc}<br>classifies a terrain considering all points - not just the last returns (as is the default behavior).
                """,
        "desc": f"{txt_lasground_short}",
    },
    "LasGroundNew": {
        "disp": "lasground_new (file)",
        "help": f"""
{txt_lasgroundnew_intro}
<h3>Parameters</h3>
{txt_inlazfile}
{txt_args("lasground_new")}
{txt_verbose}
{txt_64bit}
{head_console_examples}
    {foe}lasground_new -i terrain.laz -o classified_terrain.laz -feet -elevation_feet{fcc}<br>classifies a terrain where both horizontal and vertical units are in feet instead of in meters (which is assumed by default unless there is projection information in the LAS file saying otherwise).
                """,
        "desc": f"{txt_lasgroundnew_short}",
    },
    "LasGroundProNew": {
        "disp": "lasground_new (folder)",
        "help": f"""
{txt_lasgroundnew_intro}
{txt_folder}
<h3>Parameters</h3>
{txt_inlazdir}
{txt_args("lasground_new")}
{txt_cores}
{txt_verbose}
{txt_64bit}
{head_console_examples}
    {foe}lasground_new -i raw\*.laz -town -odir ground -olaz -cores 8 -cpu64{fcc}<br>classifies all LAZ files from the 'raw' folder with finer spacing to allowing only smaller buildings and other man-made structures to be removed on multiple cores and stores the result in the 'ground' folder (that must exist).
                """,
        "desc": f"{txt_lasgroundnew_short}",
    },
    "LasThin": {
        "disp": "lasthin (file)",
        "help": f"""
{txt_lasthin_intro}
<h3>Parameters</h3>
{txt_inlazfile}
{txt_args("lasthin")}
{txt_verbose}
{txt_64bit}
{head_console_examples}
    {foe}lasthin -i in.laz -o out.las{fcc}<br>does pointcloud thinning with the grid spacing default of 1 unit and keeps the lowest point per grid cell
                """,
        "desc": f"{txt_lasthin_short}",
    },
    "LasThinPro": {
        "disp": "lasthin (folder)",
        "help": f"""
{txt_lasthin_intro}
{txt_folder}
<h3>Parameters</h3>
{txt_inlazdir}
{txt_args("lasthin")}
{txt_cores}
{txt_verbose}
{txt_64bit}
{head_console_examples}
    {foe}lasthin -i *.las -odix _thinned{fcc}<br>thins all LAS files with the grid spacing default of 1 unit and keeps the lowest point per grid cell and forms output file names by adding appendix '_thinned' to the input file names.
                """,
        "desc": f"{txt_lasthin_short}",
    },
    "Blast2Dem": {
        "disp": "blast2dem (file)",
        "help": f"""
{txt_blast2dem_intro}
<h3>Parameters</h3>
{txt_inlazfile}
{txt_filter}
{txt_step}
{txt_pixel_attrib}
{txt_pixel_method}
{txt_args("blast2dem")}
{txt_verbose}
{txt_64bit}
{head_console_examples}
    {foe}blast2dem -i huge.laz -o dem.asc -step 2 -keep_class 2{fcc}<br>creates a temporary TIN from all points in the LAS file 'huge.laz' that are classified as ground, rasters the elevation values of the resulting TIN onto a grid with step size 2, and stores the resulting DEM in ASC format.
                """,
        "desc": f"{txt_blast2dem_short}",
    },
    "Blast2DemPro": {
        "disp": "blast2dem (folder)",
        "help": f"""
{txt_blast2dem_intro}
{txt_folder}
<h3>Parameters</h3>
{txt_inlazdir}
{txt_filter}
{txt_step}
{txt_pixel_attrib}
{txt_pixel_method}
{txt_args("blast2dem")}
{txt_cores}
{txt_verbose}
{txt_64bit}
{head_console_examples}
    {foe}blast2dem -i *.laz -opng -utm 17T -step 2.5 -hillshade{fcc}<br>rasters the hillside-shaded elevations of all LAZ files with step size 2.5 and stores the resulting DEM in PNG format and with it a KML file that geo-references each PNG in GE with UTM zone 17T.
                """,
        "desc": f"{txt_blast2dem_short}",
    },
    "Blast2Iso": {
        "disp": "blast2iso (file)",
        "help": f"""
{txt_blast2iso_intro}
<h3>Parameters</h3>
{txt_inlazfile}
{txt_args("blast2iso")}
{txt_verbose}
{txt_64bit}
                """,
        "desc": f"{txt_blast2iso_short}",
    },
    "Blast2IsoPro": {
        "disp": "blast2iso (folder)",
        "help": f"""
{txt_blast2iso_intro}
{txt_folder}
<h3>Parameters</h3>
{txt_inlazdir}
{txt_args("blast2iso")}
{txt_cores}
{txt_verbose}
{txt_64bit}
                """,
        "desc": f"{txt_blast2iso_short}",
    },
    "Las2Dem": {
        "disp": "las2dem (file)",
        "help": f"""
{txt_las2dem_intro}
<h3>Parameters</h3>
{txt_inlazfile}
{txt_filter}
{txt_step}
{txt_pixel_attrib}
{txt_pixel_method}
{txt_args("las2dem")}
{txt_verbose}
{txt_64bit}
{head_console_examples}
    {foe}las2dem -lof lidar_files.txt -merged -o dem.bil -last_only{fcc}<br>creates a temporary TIN from all last returns of all files listed in the text file 'lidar_files.txt', rasters the elevation values of each TIN facet onto a grid with step size 1 and stores the resulting DEM in BIL format with 32 bit floating-point precision.
                """,
        "desc": f"{txt_las2dem_intro}",
    },
    "Las2DemPro": {
        "disp": "las2dem (folder)",
        "help": f"""
{txt_las2dem_intro}
{txt_folder}
<h3>Parameters</h3>
{txt_inlazdir}
{txt_filter}
{txt_step}
{txt_pixel_attrib}
{txt_pixel_method}
{txt_args("las2dem")}
{txt_cores}
{txt_verbose}
{txt_64bit}
{head_console_examples}
    {foe}las2dem -i *.laz -opng -utm 17T -step 2.5 -hillshade{fcc}<br>rasters the hillside-shaded elevations of all LAZ files *.laz with step size 2.5 and stores the resulting DEM in PNG format and with it a KML file that geo-references each PNG in GE with UTM zone 17T.
                """,
        "desc": f"{txt_las2dem_intro}",
    },
    "Las2Iso": {
        "disp": "las2iso",
        "help": f"""
{txt_las2iso_intro}
<h3>Parameters</h3>
{txt_inlazfile}
{txt_args("las2iso")}
{txt_verbose}
{txt_64bit}
                """,
        "desc": f"{txt_las2iso_short}",
    },
    "LasCanopy": {
        "disp": "lascanopy (file)",
        "help": f"""
{txt_lascanopy_intro}
<h3>Parameters</h3>
{txt_inlazfile}
{txt_canopy}
{txt_args("lascanopy")}
{txt_verbose}
{txt_64bit}
{head_console_examples}
    {foe}lascanopy -i in.laz -min -max -avg{fcc}<br>for the input laz file and for all height above 1.37 it computes the minimum, maximum, and average value from all points that fall into cells of size 20 by 20 and stores the resulting grid in ASC format using the endings '_min.asc', '_max.asc', '_avg.asc'.
                """,
        "desc": f"{txt_lascanopy_short}",
    },
    "LasCanopyPro": {
        "disp": "lascanopy (folder)",
        "help": f"""
{txt_lascanopy_intro}
{txt_folder}
<h3>Parameters</h3>
{txt_inlazdir}
{txt_canopy}
{txt_args("lascanopy")}
{txt_cores}
{txt_verbose}
{txt_64bit}
{head_console_examples}
    {foe}lascanopy -i *.las -min -max -avg{fcc}<br>for each *.las files and for all height above 1.37 it computes the minimum, maximum, and average value from all points that fall into cells of size 20 by 20 and stores the resulting grid in ASC format using the endings '_min.asc', '_max.asc', '_avg.asc'.
                """,
        "desc": f"{txt_lascanopy_short}",
    },
    "LasGrid": {
        "disp": "lasgrid (file)",
        "help": f"""
{txt_lasgrid_intro}
<h3>Parameters</h3>
{txt_inlazfile}
{txt_filter}
{txt_step}
{txt_pixel_attrib}
{txt_pixel_method}
{txt_args("lasgrid")}
{txt_verbose}
{txt_64bit}
{head_console_examples}
    {foe}lasgrid -v -i lidar.las -o dem.asc -step 2 -average{fcc}<br>rasters the average elevations from all points that fall into cells of size 2 by 2 units and stores the resulting grid in ASC format.
                """,
        "desc": f"{txt_lasgrid_intro}",
    },
    "LasGridPro": {
        "disp": "lasgrid (folder)",
        "help": f"""
{txt_lasgrid_intro}
{txt_folder}
<h3>Parameters</h3>
{txt_inlazdir}
{txt_filter}
{txt_step}
{txt_pixel_attrib}
{txt_pixel_method}
{txt_args("lasgrid")}
{txt_cores}
{txt_verbose}
{txt_64bit}
{head_console_examples}
    {foe}lasgrid -i *.las -opng -step 5 -false -sp83 OH_N{fcc}<br>rasters for each *.las files the lowest elevation of all points that fall into cells of size 5 by 5, stores the resulting grid in PNG format using false coloring, and creates a KML file that maps the PNG to state plane NAD83 of Northern Ohio.
                """,
        "desc": f"{txt_lasgrid_intro}",
    },
    "LasHeight": {
        "disp": "lasheight (file)",
        "help": f"""
{txt_lasheight_intro}
<h3>Parameters</h3>
{txt_inlazfile}
{txt_replace_z}
{txt_args("lasheight")}
{txt_verbose}
{txt_64bit}
{head_console_examples}
    {foe}lasheight -i lidar.laz -o brush.laz -drop_below 1.0 -drop_above 3.0{fcc}<br>calculate the height above ground, save the height in the user data field and kepps only those points who are between 1 and 3 units above the ground.
                """,
        "desc": f"{txt_lasheight_short}",
    },
    "LasHeightPro": {
        "disp": "lasheight (folder)",
        "help": f"""
{txt_lasheight_intro}
{txt_folder}
<h3>Parameters</h3>
{txt_inlazdir}
{txt_replace_z}
{txt_args("lasheight")}
{txt_cores}
{txt_verbose}
{txt_64bit}
{head_console_examples}
    {foe}lasheight -i *.laz -odir brush -drop_below 1.0 -drop_above 3.0{fcc}<br>calculate the height above ground for all files, save the height in the user data field and kepps only those points who are between 1 and 3 units above the ground.
                """,
        "desc": f"{txt_lasheight_short}",
    },
    "LasHeightClassify": {
        "disp": "lasheight classify (file)",
        "help": f"""
{txt_lasheight_intro}
{txt_lasheight_class}
<h3>Parameters</h3>
{txt_inlazfile}
{txt_replace_z}
{txt_args("lasheight")}
{txt_verbose}
{txt_64bit}
                """,
        "desc": f"{txt_lasheight_short}",
    },
    "LasHeightProClassify": {
        "disp": "lasheight classify (folder)",
        "help": f"""
{txt_lasheight_intro}
{txt_lasheight_class}
{txt_folder}
<h3>Parameters</h3>
{txt_inlazdir}
{txt_replace_z}
{txt_args("lasheight")}
{txt_cores}
{txt_verbose}
{txt_64bit}
                """,
        "desc": f"{txt_lasheight_short}",
    },
    "LasControl": {
        "disp": "lascontrol",
        "help": f"""
        {txt_lascontrol_intro}
<h3>Parameters</h3>
{txt_inlazfile}
{txt_args("lascontrol")}
{txt_verbose}
{txt_64bit}
{head_console_examples}
    {foe}lascontrol -i *.laz -cp cp.csv -cp_out report.txt -keep_class 2 8 -adjust_z -odix _adjusted{fcc}<br>assumes the x/y/z coordinates of the control points are stored as the 1nd/2nd/3rd entry on each line of the 'cp.csv' file and only points with ground and keypoint classification (class 2 or 8) are used to construct the reference TIN. all LAZ files that match '*.laz' get merged on the fly into one to construct the reference TIN. the output is written to the file 'report.txt' and the average error is used to adjust the z coordinate of all LAZ files that are then written to files with the same name and appendix '_adjusted'.
                """,
        "desc": f"{txt_lascontrol_short}",
    },
    "LasDuplicate": {
        "disp": "lasduplicate (file)",
        "help": f"""{txt_lasduplicate_intro}
<h3>Parameters</h3>
{txt_inlazfile}
{txt_args("lasduplicate")}
{txt_verbose}
{txt_64bit}
{head_console_examples}
{foe}lasduplicate64 -i in.laz -nearby 0.005 -o out.laz{fcc}<br>removes all duplicates and nearby points from fulfilling the criteria desribed above from the LAZ file 'in.laz' and stores the result to the LAZ file 'out.laz'.""",
        "desc": f"{txt_lasduplicate_short}",
    },
    "LasDuplicatePro": {
        "disp": "lasduplicate (folder)",
        "help": f"""{txt_lasduplicate_intro}
<h3>Parameters</h3>
{txt_inlazfile}
{txt_args("lasduplicate")}
{txt_verbose}
{txt_64bit}
{head_console_examples}
{foe}lasduplicate64 -i *.las -olaz{fcc}<br>removes all duplicates from all LAS file matching '*.las' and stores each result to a corresponding LAZ file '*.laz'.
{foe}lasduplicate64 -i *.las -olaz -lowest_z{fcc}<br>same as above but keeps the duplicate with the lowest z coordinate.""",
        "desc": f"{txt_lasduplicate_short}",
    },
    "LasPrecision": {
        "disp": "lasprecision",
        "help": f"""
        {txt_lasprecision_intro}
<h3>Parameters</h3>
{txt_inlazfile}
{txt_args("lasprecision")}
{txt_verbose}
{txt_64bit}
{head_console_examples}
    {foe}lasprecision64 -i in.laz -all{fcc}<br>original scale factors: 0.001 0.001 0.001<br>loading first 8146178 of 8146178 points<br>X differences<br>          0 :    7822346   0<br>         10 :     323326   0.01<br>         20 :        500   0.02<br>         30 :          5   0.03
Y differences<br>          0 :    7533456   0<br>         10 :     609382   0.01<br>         20 :       3303   0.02<br>         30 :         36   0.03
Z differences<br>          0 :    8124512   0<br>         10 :      21175   0.01<br>         20 :        346   0.02<br>         30 :         75   0.03<br>         40 :         23   0.04<br>         50 :          7   0.05<br>         60 :          4   0.06<br>...
This example analyzes all raw integer coordinates of "in.laz" into three separate arrays, sort each array in ascending sorted orders, compute the difference between all neighboring values and output a histogram in textural form. These histograms provide information about the original scale factors and if they are inflated/missleading. Here there is no millimeter precision (=> 0.001) in the data, even if the scale factor tells so. All x, and y, or, z values are either 10, 20, 30, 40, or other multiple of 10 units spaced apart.<br>Hence the true precision is only centimeters (=> 0.01).<br>The scale in the header is set to millimeter - this makes compression inefficient.""",
        "desc": f"{txt_lasprecision_short}",
    },
    "LasInfo": {
        "disp": "lasinfo (file)",
        "help": f"""
{txt_lasinfo_intro}
<h3>Parameters</h3>
{txt_inlazfile}
{txt_args("lasinfo")}
{txt_verbose}
{txt_64bit}
{head_console_examples}
    {foe}lasinfo -i lidar.las{fcc}<br>reports the basic information of the given file to the console.
    {foe}lasinfo -i lidar.las -nc{fcc}<br>reports a very fast header information of the given file to the console.
                """,
        "desc": f"{txt_lasinfo_short}",
    },
    "LasInfoPro": {
        "disp": "lasinfo (folder)",
        "help": f"""
{txt_lasinfo_intro}
{txt_folder}
<h3>Parameters</h3>
{txt_inlazdir}
{txt_args("lasinfo")}
{txt_cores}
{txt_verbose}
{txt_64bit}
{head_console_examples}
  {foe}lasinfo -i *.laz -no_vlrs -nc -otxt{fcc}<br>create a textfile to each LAZ file containing the header information without point parsing and VLR information.
  {foe}lasinfo -i *.laz -no_vlrs -nc -stdout > all.txt
create ONE textfile with all LAZ file header information.
                """,
        "desc": f"{txt_lasinfo_short}",
    },
    "LasOverlap": {
        "disp": "lasoverlap (file)",
        "help": f"""
{txt_lasoverlap_intro}
<h3>Parameters</h3>
{txt_inlazfile}
{txt_filter}
{txt_args("lasoverlap")}
{txt_verbose}
{txt_64bit}
{head_console_examples}
    {foe}lasoverlap -i tile.las -step 2 -o overlap.png{fcc}<br>creates an overlap raster as well as a difference raster with a step of 2 units. For this, it is necessary that the LiDAR points in the LAS file have their point source ID populated with the flight line ID. The overlap raster uses the default color ramp which maps overlap counts from 0 to 5 to a different colors. The difference raster uses the default color ramp that maps blue to -2.5, white to 0, and red to 2.5. The default output is PNG.
                """,
        "desc": f"{txt_lasoverlap_short}",
    },
    "LasOverlapPro": {
        "disp": "lasoverlap (folder)",
        "help": f"""
{txt_lasoverlap_intro}
{txt_folder}
<h3>Parameters</h3>
{txt_inlazdir}
{txt_filter}
{txt_args("lasoverlap")}
{txt_cores}
{txt_verbose}
{txt_64bit}
{head_console_examples}
    {foe}lasoverlap -i LDR*.las -files_are_flightlines -step 3 -min_diff 0.1 -max_diff 0.4 -o overlap.png{fcc}<br>merges all the files "LDR*.las" while assigning the points of each file a unique point source ID (aka flight line number), and then creates an overlap raster as well as a difference raster with a step of 3 units. The overlap raster uses the default range of 5 overlaps lines for the color ramp. The difference raster uses '-min_diff 0.1' and '-max_diff 0.4' which maps the range (-0.4 ... -0.1) to (blue ... white) and the range (0.1 ... 0.4) to (white ... red). The range (-0.1 ... 0.1) is mapped to white.
                """,
        "desc": f"{txt_lasoverlap_short}",
    },
    "LasValidate": {
        "disp": "lasvalidate (file)",
        "help": f"""
{txt_lasvalidate_intro}
<h3>Parameters</h3>
{txt_inlazfile}
{txt_args("lasvalidate")}
                """,
        "desc": f"{txt_lasvalidate_short}",
    },
    "LasValidatePro": {
        "disp": "lasvalidate (folder)",
        "help": f"""
{txt_lasvalidate_intro}
{txt_folder}
<h3>Parameters</h3>
{txt_inlazdir}
{txt_args("lasvalidate")}
                """,
        "desc": f"{txt_lasvalidate_short}",
    },
    "LasPublish": {
        "disp": "laspublish (file)",
        "help": f"""
{txt_laspublish_intro}
<h3>Parameters</h3>
{txt_inlazfile}
{txt_args("laspublish")}
{txt_verbose}
{head_console_examples}
    {foe}laspublish -i lidar.laz -odir portal_dir -o portal.html -olaz{fcc}<br>creates a directory called "./portal_dir" containing an HTML file called "portal.html" that allows exploring the LiDAR points from the file "lidar.laz" once the directory is moved into Web space.
                """,
        "desc": f"{txt_laspublish_short}",
    },
    "LasPublishPro": {
        "disp": "laspublish (folder)",
        "help": f"""
{txt_laspublish_intro}
{txt_folder}
<h3>Parameters</h3>
{txt_inlazdir}
{txt_args("laspublish")}
{txt_verbose}
{head_console_examples}
    {foe}laspublish -i tiles_final/*.laz -odir portal_dir -o portal.html -olaz{fcc}<br>creates a directory called './portal_dir' containing an HTML file called 'portal.html' that allows exploring the LiDAR points from the directory 'tiles_final' once the directory is moved into Web space.
                """,
        "desc": f"{txt_laspublish_short}",
    },
    "LasColor": {
        "disp": "lascolor",
        "help": f"""
{txt_lascolor_intro}
<h3>Parameters</h3>
{txt_inlazfile}
{fop}input ortho:{fcc} input file as georeferenced TIF file.
{txt_args("lascolor")}
{txt_verbose}
{txt_64bit}
                """,
        "desc": f"{txt_lascolor_short}",
    },
    "LasView": {
        "disp": "lasview (file)",
        "help": f"""
{txt_lasview_intro}
<h3>Parameters</h3>
{txt_inlazfile}
{txt_args("lasview")}
{txt_verbose}
                """,
        "desc": f"{txt_lasview_short}",
    },
    "LasViewPro": {
        "disp": "lasview (folder)",
        "help": f"""
{txt_lasview_intro}
{txt_folder}
<h3>Parameters</h3>
{txt_inlazdir}
{txt_args("lasview")}
{txt_verbose}
                """,
        "desc": f"{txt_lasview_short}",
    },
    "LasVoxel": {
        "disp": "lasvoxel",
        "help": f"""This tool computes a voxelization of points. You can specify the xy and the z size of the voxel cells separately with '-step_xy 2' and '-step_z 0.3' which would create cells of size 2 by 2 by 0.3 units or use uniform sized cells of '-step 0.5'. For voxels that are infinite in z direction use option '-step_z_infinite'. The number of returns falling into a voxel is stored as the intensity value of the points in the resulting LAS/LAZ file.<br>By adding '-compute_mean_xyz' to the command line lasvoxel uses the average x, y, z coordinate of all points falling into a voxel instead of the center of the voxel.<br>By adding '-empty_voxels' to the command line lasvoxel will also report all empty voxels that fall within the 3D bounding box but give them an intensity value of zero.
<h3>Parameters</h3>
{txt_inlazfile}
{fop}grid size:{fcc} use a [n]x[n]x[n] uniform grid for finding isolated points  (-step [n])
{fop}maximum point count per voxel:{fcc} optional define maximum point count [n] per voxel  (-max_count [n])
{fop}compute averaged coordinate each voxel:{fcc} compute averaged coordinate for output voxels  (-compute_mean_xyz)
{fop}output voxels without returns as intensity zero:{fcc} also output voxels without returns but give them intensity of zero  (-empty_voxels)
{fop}store voxel IDs into "intensity":{fcc} store computed voxel IDs into "intensity" field  (-store_IDs_in_intensity)
{fop}store voxel IDs into "point source":{fcc} store computed voxel IDs into "point source" field  (-store_IDs_in_point_source)
{txt_args("lasvoxel")}
{txt_verbose}
{txt_64bit}
{head_console_examples}
{foe}lasvoxel64 -v -i ..\data\france.laz -step 1 -odix _mist -olaz{fcc}<br>voxelizing all points with voxel size of 1, append ""_mist"" extension and save as LAZ file""",
        "desc": f"{txt_lasvoxel_short}",
    },
    "FlightLinesToCHMFirstReturn": {
        "disp": "Flightlines to CHM - first return",
        "help": """
                    Create a canopy height model with first return only
                """,
        "desc": "Create a canopy height model with first return only",
    },
    "FlightLinesToCHMHighestReturn": {
        "disp": "Flightlines to CHM - highest return",
        "help": """
                    Create a canopy height model with highest return only
                """,
        "desc": "Create a canopy height model with highest return only",
    },
    "FlightLinesToCHMSpikeFree": {
        "disp": "Flightlines to CHM - spike free",
        "help": """
                    Create a canopy height model with spike free option
                """,
        "desc": "Create a canopy height model with spike free option",
    },
    "FlightLinesToDTMandDSMFirstReturn": {
        "disp": "FlightLines to DTM & DSM - first return",
        "help": """
                     Create a digital terrain model and digital surface model out of lidar data files using the first return only
                """,
        "desc": "Create a digital terrain model and digital surface model out of lidar data files using the first return only",
    },
    "FlightLinesToDTMandDSMSpikeFree": {
        "disp": "FlightLines to DTM & DSM - spike free",
        "help": """
                    Create a digital terrain model and digital surface model with spike free option
                """,
        "desc": "Create a digital terrain model and digital surface model with spike free option",
    },
    "FlightLinesToMergedCHMFirstReturn": {
        "disp": "FlightLines to merged CHM - first return",
        "help": """
                    Create a merged canopy height model out of lidar data files using the first return only
                """,
        "desc": "Create a merged canopy height model out of lidar data files using the first return only",
    },
    "FlightLinesToMergedCHMHighestReturn": {
        "disp": "FlightLines to merged CHM - highest return",
        "help": """
                    Create a merged canopy height model out of lidar data files with highest return
                """,
        "desc": "Create a merged canopy height model out of lidar data files with highest return",
    },
    "FlightLinesToMergedCHMPitFree": {
        "disp": "FlightLines to merged CHM - pit free",
        "help": """
                    Create a pit free merged canopy height model out of lidar data files
                """,
        "desc": "Create a pit free merged canopy height model out of lidar data files",
    },
    "FlightLinesToMergedCHMSpikeFree": {
        "disp": "FlightLines to merged CHM - spike free",
        "help": """
                    Create a canopy height model out of lidar data files which are optional in flightlines
                """,
        "desc": "Create a canopy height model out of lidar data files which are optional in flightlines",
    },
    "HugeFileClassify": {
        "disp": "Huge file - classify",
        "help": """
                    Do a classification for huge lidar data files
                """,
        "desc": "Do a classification for huge lidar data files",
    },
    "HugeFileGroundClassify": {
        "disp": "Huge file - ground classify",
        "help": """
                    Do a ground classification for huge lidar data files
                """,
        "desc": "Do a ground classification for huge lidar data files",
    },
    "HugeFileNormalize": {
        "disp": "Huge file - normalize",
        "help": """
                    Normalize huge lidar data files
                """,
        "desc": "Normalize huge lidar data files",
    },
}
