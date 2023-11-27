"""
descriptions of all the lastools
"""
import os

# ../plugins/LAStools/lastools + /assets/img
paths = {
    "lastools": f"{os.path.split(os.path.split(os.path.dirname(__file__))[0])[0]}/",
    "img": f"{os.path.split(os.path.split(os.path.dirname(__file__))[0])[0]}/assets/img/"
}

icon_help_text = """
** Licence Info\n
"""

licence = {
    "c": {
        "descript": '[c] Closed source tool (licensed)',
        "path": 'lic_com.png'
    },
    "o": {
        "descript": '[o] Open source tool',
        "path": 'lic_opensource.png'
    },
    "f": {
        "descript": '[f] Free tool',
        "path": 'lic_free.png'
    },
}

descript_template = {
    "info": {
        "group": 'group name',
        "group_id": 'group id',
    },
    "items": {
        "tool_name_1": {
            "tool_class_name_1": {
                "name": 'name',
                "display_name": 'display_name',
                "licence_icon_path": licence["c"]["path"],
                "short_help_string": f"""
                short_help_string
                
                (for pro classes) With this tool you can choose a folder contain multiple input file rather than single file.
                For more details see the README file (Please click on help button).
                {icon_help_text}{licence["c"]["descript"]}
                """,
                "short_description": 'short_description ("for pro classes" using a folder contain multiple input file)',
                "url_path": 'url_path'
            },
        },
    },
}


descript_data_compression = {
    "info": {
        "group": '1. Data Compression',
        "group_id": 'data_compression',
    },
    "items": {
        "laszip": {

            "LasZip": {
                "name": 'LasZip',
                "display_name": 'laszip',
                "licence_icon_path": licence["o"]["path"],
                "short_help_string": f"""
                    Compresses and uncompresses LiDAR data stored in binary LAS

                    For more details see the README file (Please click on help button).
                {icon_help_text}{licence["o"]["descript"]}
                """,
                "short_description": 'Compresses LAS files',
                "url_path": 'https://downloads.rapidlasso.de/readme/laszip_README.md'
            },

            "LasZipPro": {
                "name": 'LasZipPro',
                "display_name": 'laszip (folder)',
                "licence_icon_path": licence["o"]["path"],
                "short_help_string": f"""
                    format (1.0 - 1.4) in a completely lossless manner to the

                    With this tool you can choose a folder contain multiple input file rather than single file.
                    For more details see the README file (Please click on help button).
                {icon_help_text}{licence["o"]["descript"]}
                """,
                "short_description": 'Compresses LAS files (using a folder contain multiple input file)',
                "url_path": 'https://downloads.rapidlasso.de/readme/laszip_README.md'
            },

        },
    },
}

descript_data_convert = {
    "info": {
        "group": '2. Data Convert (Import / Export)',
        "group_id": 'data_convert',
    },
    "items": {

        "las2txt": {
            "Las2txt": {
                "name": 'Las2txt',
                "display_name": 'las2txt',
                "licence_icon_path": licence["o"]["path"],
                "short_help_string": f"""
                    A simple open source tool licensed LGPL 2.1 that converts binary LAS or LAZ files to human readable ASCII text format. Below is an example command line that converts one LAZ file to text by placing the x, y, and z coordinate of each point as the 1st, 2nd, and 3rd entries, the intensity as the 4th entry, and the gps_time as the 5th entry of each line. 
                    
                    For more details see the README file (Please click on help button).
                {icon_help_text}{licence["o"]["descript"]}
                """,
                "short_description": 'Converts binary LAS or LAZ files to human-readable ASCII text format.',
                "url_path": 'https://downloads.rapidlasso.de/readme/las2txt_README.md'
            },

            "Las2txtPro": {
                "name": 'Las2txtPro',
                "display_name": 'las2txt (folder)',
                "licence_icon_path": licence["o"]["path"],
                "short_help_string": f"""
                    A simple open source tool licensed LGPL 2.1 that converts binary LAS or LAZ files to human readable ASCII text format. Below is an example command line that converts one LAZ file to text by placing the x, y, and z coordinate of each point as the 1st, 2nd, and 3rd entries, the intensity as the 4th entry, and the gps_time as the 5th entry of each line. 
                    
                    With this tool you can choose a folder contain multiple input file rather than single file.
                    For more details see the README file (Please click on help button).
                {icon_help_text}{licence["o"]["descript"]}
                """,
                "short_description": 'Converts binary LAS or LAZ files to human-readable ASCII text format (using a folder contain multiple input file).',
                "url_path": 'https://downloads.rapidlasso.de/readme/las2txt_README.md'
            },
        },

        "txt2las": {
            "Txt2Las": {
                "name": 'Txt2Las',
                "display_name": 'txt2las',
                "licence_icon_path": licence["o"]["path"],
                "short_help_string": f"""
                    This handy tool converts from points from bloated ASCII to binary LAS or compressed LAZ file. When you send us a support request for this tool please include a few lines (around 20 to 50) of your ASCII text representation as well the command lines (aka parse strings)
    
                    For more details see the README file (Please click on help button).
                {icon_help_text}{licence["o"]["descript"]}
                """,
                "short_description": 'Converts from ASCII to binary LAS or compressed LAZ file.',
                "url_path": 'https://downloads.rapidlasso.de/readme/txt2las_README.md'
            },
            "Txt2LasPro": {
                "name": 'Txt2LasPro',
                "display_name": 'txt2las (folder)',
                "licence_icon_path": licence["o"]["path"],
                "short_help_string": f"""
                    This handy tool converts from points from bloated ASCII to binary LAS or compressed LAZ file. When you send us a support request for this tool please include a few lines (around 20 to 50) of your ASCII text representation as well the command lines (aka parse strings)
    
                    With this tool you can choose a folder contain multiple input file rather than single file.
                    For more details see the README file (Please click on help button).
                {icon_help_text}{licence["o"]["descript"]}
                """,
                "short_description": 'Converts from ASCII to binary LAS or compressed LAZ file (using a folder contain multiple input file)',
                "url_path": 'https://downloads.rapidlasso.de/readme/txt2las_README.md'
            },
        },

        "las2las": {

            "Las2LasFilter": {
                "name": 'Las2LasFilter',
                "display_name": 'las2las - filter',
                "licence_icon_path": licence["o"]["path"],
                "short_help_string": f"""
                This tool is the “swiss-army knife” of LiDAR file processing. It can convert, filter, transform, subset, repair, scale, translate, zero, clamp, compress, initialize, … LAS or LAZ files in numerous ways. This tool is 100% open source LGPL.
                
                For more details see the README file (Please click on help button).
                {icon_help_text}{licence["o"]["descript"]}
                """,
                "short_description": 'Extracts last returns, clips, subsamples, translates, etc.',
                "url_path": 'https://downloads.rapidlasso.de/readme/las2las_README.md'
            },

            "Las2LasProject": {
                "name": 'Las2LasProject',
                "display_name": 'las2las - project',
                "licence_icon_path": licence["o"]["path"],
                "short_help_string": f"""
                This tool is the “swiss-army knife” of LiDAR file processing. It can convert, filter, transform, subset, repair, scale, translate, zero, clamp, compress, initialize, … LAS or LAZ files in numerous ways. This tool is 100% open source LGPL.
                
                For more details see the README file (Please click on help button).
                {icon_help_text}{licence["o"]["descript"]}
                """,
                "short_description": 'Extracts last returns, clips, subsamples, translates, etc.',
                "url_path": 'https://downloads.rapidlasso.de/readme/las2las_README.md'
            },

            "Las2LasTransform": {
                "name": 'Las2LasTransform',
                "display_name": 'las2las - transform',
                "licence_icon_path": licence["o"]["path"],
                "short_help_string": f"""
                This tool is the “swiss-army knife” of LiDAR file processing. It can convert, filter, transform, subset, repair, scale, translate, zero, clamp, compress, initialize, … LAS or LAZ files in numerous ways. This tool is 100% open source LGPL.
                
                For more details see the README file (Please click on help button).
                {icon_help_text}{licence["o"]["descript"]}
                """,
                "short_description": 'Extracts last returns, clips, subsamples, translates, etc.',
                "url_path": 'https://downloads.rapidlasso.de/readme/las2las_README.md'
            },

            "Las2LasProFilter": {
                "name": 'Las2LasProFilter',
                "display_name": 'las2las - filter (folder)',
                "licence_icon_path": licence["o"]["path"],
                "short_help_string": f"""
                This tool is the “swiss-army knife” of LiDAR file processing. It can convert, filter, transform, subset, repair, scale, translate, zero, clamp, compress, initialize, … LAS or LAZ files in numerous ways. This tool is 100% open source LGPL.
                
                With this tool you can choose a folder contain multiple input file rather than single file.
                For more details see the README file (Please click on help button).
                {icon_help_text}{licence["o"]["descript"]}
                """,
                "short_description": 'Extracts last returns, clips, subsamples, translates, etc. (using a folder contain multiple input file)',
                "url_path": 'https://downloads.rapidlasso.de/readme/las2las_README.md'
            },

            "Las2LasProProject": {
                "name": 'Las2LasProProject',
                "display_name": 'las2las - project (folder)',
                "licence_icon_path": licence["o"]["path"],
                "short_help_string": f"""
                This tool is the “swiss-army knife” of LiDAR file processing. It can convert, filter, transform, subset, repair, scale, translate, zero, clamp, compress, initialize, … LAS or LAZ files in numerous ways. This tool is 100% open source LGPL.
                
                With this tool you can choose a folder contain multiple input file rather than single file.
                For more details see the README file (Please click on help button).
                {icon_help_text}{licence["o"]["descript"]}
                """,
                "short_description": 'Extracts last returns, clips, subsamples, translates, etc. (using a folder contain multiple input file)',
                "url_path": 'https://downloads.rapidlasso.de/readme/las2las_README.md'
            },

            "Las2LasProTransform": {
                "name": 'Las2LasProTransform',
                "display_name": 'las2las - transform (folder)',
                "licence_icon_path": licence["o"]["path"],
                "short_help_string": f"""
                This tool is the “swiss-army knife” of LiDAR file processing. It can convert, filter, transform, subset, repair, scale, translate, zero, clamp, compress, initialize, … LAS or LAZ files in numerous ways. This tool is 100% open source LGPL.
                
                With this tool you can choose a folder contain multiple input file rather than single file.
                For more details see the README file (Please click on help button).
                {icon_help_text}{licence["o"]["descript"]}
                """,
                "short_description": 'Extracts last returns, clips, subsamples, translates, etc. (using a folder contain multiple input file)',
                "url_path": 'https://downloads.rapidlasso.de/readme/las2las_README.md'
            },

        },

        "las2shp": {
            "Las2Shp": {
                "name": 'Las2Shp',
                "display_name": 'las2shp',
                "licence_icon_path": licence["c"]["path"],
                "short_help_string": f"""
                converts LIDAR from LAS/LAZ/ASCII to ESRI’s Shapefile format by grouping consecutive points into MultiPointZ records. The default size is 1024. It can be changed with ‘-record 2048’. If you want to use PointZ records instead you need to add ‘-single_points’ to the command line.
                
                For more details see the README file (Please click on help button).
                {icon_help_text}{licence["c"]["descript"]}
                """,
                "short_description": 'Converts LIDAR from LAS/LAZ/ASCII to ESRI’s Shapefile format by grouping consecutive points into MultiPointZ records.',
                "url_path": 'https://downloads.rapidlasso.de/readme/las2shp_README.md'
            },
        },

        "shp2las": {
            "Shp2Las": {
                "name": 'Shp2Las',
                "display_name": 'shp2las',
                "licence_icon_path": licence["c"]["path"],
                "short_help_string": f"""
                    Converts from points from ESRI’s Shapefile to LAS/LAZ/ASCII format given the input contains Points or MultiPoints (that is any of the shape types 1,11,21,8,18,28).
                    
                    For more details see the README file (Please click on help button).
                {icon_help_text}{licence["c"]["descript"]}
                """,
                "short_description": 'Converts from points from ESRI’s Shapefile to LAS/LAZ/ASCII format, given the input, contains Points or MultiPoints.',
                "url_path": 'https://downloads.rapidlasso.de/readme/shp2las_README.md'
            },
        },

    },
}

descript_processing = {
    "info": {
        "group": '3. Preprocessing',
        "group_id": 'preprocessing',
    },
    "items": {
        "las3dpoly": {

            "Las3dPolyRadialDistance": {
                "name": 'Las3dPolyRadialDistance',
                "display_name": 'las3dpoly (Radial Distance)',
                "licence_icon_path": licence["c"]["path"],
                "short_help_string": f"""
                This tool modifies points within a certain distance of polylines. As an input take, for example, a LAS/LAZ/TXT file and a SHP/TXT file with one or many polylines (e.g. powerlines) by specify a radial distance to the 3D polygon
    
                Affected points can be classified, clipped, or flagged.
                
                The input SHP/TXT file must contain clean polygons or polylines that are free of self-intersections, duplicate points, and/or overlaps and they must all form closed loops (e.g. the last and first point should be identical).
                
                ** Note
                   
                line.csv may look like
                
                -10,0,0
                10,0,0
                0,0,0
                0,-10,0
                0,10,0
                
                For more details see the README file (Please click on help button).
                {icon_help_text}{licence["c"]["descript"]}
                """,
                "short_description": 'Modifies points within a certain radial distance of 3D polylines',
                "url_path": 'https://downloads.rapidlasso.de/readme/las3dpoly_README.md'
            },

            "Las3dPolyHorizontalVerticalDistance": {
                "name": 'Las3dPolyHorizontalVerticalDistance',
                "display_name": 'las3dpoly (Horizontal and Vertical Distance)',
                "licence_icon_path": licence["c"]["path"],
                "short_help_string": f"""
                ** Description
                This tool modifies points within a certain distance of polylines. As an input take, for example, a LAS/LAZ/TXT file and a SHP/TXT file with one or many polylines (e.g. powerlines) by specify a horizontal and vertical distance to the 3D polygon
            
                Affected points can be classified, clipped, or flagged.
            
                The input SHP/TXT file must contain clean polygons or polylines that are free of self-intersections, duplicate points, and/or overlaps and they must all form closed loops (e.g. the last and first point should be identical).
            
                ** Note
            
                line.csv may look like
            
                -10,0,0
                10,0,0
                0,0,0
                0,-10,0
                0,10,0
                
                For more details see the README file (Please click on help button).
                {icon_help_text}{licence["c"]["descript"]}
                """,
                "short_description": 'Modifies points within a certain horizontal and vertical distance of 3D polylines',
                "url_path": 'https://downloads.rapidlasso.de/readme/las3dpoly_README.md'
            }

        },

        "lasintensity": {

            "LasIntensity": {
                "name": 'LasIntensity',
                "display_name": 'lasintensity',
                "licence_icon_path": licence["c"]["path"],
                "short_help_string": f"""
                    ** Description
                    This tool corrects the intensity attenuation due to atmospheric absorption. 
                    Because the light has to travel longer distances for points with large scan angles, these points may be detected with reduced intensities.
                    
                    In order to get a reliant attenuation estimate several parameters are essential:
                    - Scanner height above ground level (AGL) [km]
                    - Scanner wavelength [µm]
                    - Atmospheric visibility range [km]
                    
                    For more details see the README file (Please click on help button).
                {icon_help_text}{licence["c"]["descript"]}
                """,
                "short_description": 'corrects the intensity attenuation due to atmospheric absorption.',
                "url_path": 'https://downloads.rapidlasso.de/readme/lasintensity_README.md'
            },

            "LasIntensityAttenuationFactor": {
                "name": 'LasIntensityAttenuationFactor',
                "display_name": 'lasintensity (Attenuation Factor)',
                "licence_icon_path": licence["c"]["path"],
                "short_help_string": f"""
                    ** Description
                    This tool corrects the intensity attenuation due to atmospheric absorption. 
                    Because the light has to travel longer distances for points with large scan angles, these points may be detected with reduced intensities.
                
                    In order to get a reliant attenuation estimate several parameters are essential:
                    - Scanner height above ground level (AGL) [km]
                    - Absorption coefficient [km^-1]
                    
                    For more details see the README file (Please click on help button).
                {icon_help_text}{licence["c"]["descript"]}
                """,
                "short_description": 'corrects the intensity attenuation due to atmospheric absorption.',
                "url_path": 'https://downloads.rapidlasso.de/readme/lasintensity_README.md'

            },
        },

        "lasindex": {

            "LasIndex": {
                "name": 'LasIndex',
                "display_name": 'lasindex',
                "licence_icon_path": licence["o"]["path"],
                "short_help_string": f"""
                    Creates a *.lax file for a given *.las or *.laz file that contains spatial indexing information. When this LAX file is present it will be used to speed up access to the relevant areas of the LAS/LAZ file.                   
                    
                    For more details see the README file (Please click on help button).
                {icon_help_text}{licence["o"]["descript"]}
                """,
                "short_description": 'Creates an index file (LAX) about a LAS/LAZ file (using a folder contain multiple input file).',
                "url_path": 'https://downloads.rapidlasso.de/readme/lasindex_README.md'
            },

            "LasIndexPro": {
                "name": 'LasIndexPro',
                "display_name": 'lasindex (folder)',
                "licence_icon_path": licence["o"]["path"],
                "short_help_string": f"""
                    Creates a *.lax file for a given *.las or *.laz file that contains spatial indexing information. When this LAX file is present it will be used to speed up access to the relevant areas of the LAS/LAZ file.                   
                    With this tool you can choose a folder contain multiple input file rather than single file.
                    For more details see the README file (Please click on help button).
                {icon_help_text}{licence["o"]["descript"]}
                """,
                "short_description": 'Creates an index file (LAX) about a LAS/LAZ file (using a folder contain multiple input file).',
                "url_path": 'https://downloads.rapidlasso.de/readme/lasindex_README.md'
            },

        },

        "lasmerge": {
            "LasMerge": {
                "name": 'LasMerge',
                "display_name": 'lasmerge',
                "licence_icon_path": licence["o"]["path"],
                "short_help_string": f"""
                This is a handy tool to merge multiple LiDAR files into one. However, we usually discourage this practice as this can also be achieved on-the-fly with the ‘-merged’ option in any of the other LAStools without creating a second copy on disk. In addition this tools allows splitting larger files into smaller subsets each containing a user-specified number of points. This tool is 100% open source LGPL.
                
                For more details see the README file (Please click on help button).
                {icon_help_text}{licence["o"]["descript"]}
                """,
                "short_description": 'Merges several LAS or LAZ files.',
                "url_path": 'https://downloads.rapidlasso.de/readme/lasmerge_README.md'
            },

            "LasMergePro": {
                "name": 'LasMergePro',
                "display_name": 'lasmerge (folder)',
                "licence_icon_path": licence["o"]["path"],
                "short_help_string": f"""
                This is a handy tool to merge multiple LiDAR files into one. However, we usually discourage this practice as this can also be achieved on-the-fly with the ‘-merged’ option in any of the other LAStools without creating a second copy on disk. In addition this tools allows splitting larger files into smaller subsets each containing a user-specified number of points. This tool is 100% open source LGPL.
                
                With this tool you can choose a folder contain multiple input file rather than single file.
                For more details see the README file (Please click on help button).
                {icon_help_text}{licence["o"]["descript"]}
                """,
                "short_description": 'Merges several LAS or LAZ files (using a folder contain multiple input file).',
                "url_path": 'https://downloads.rapidlasso.de/readme/lasmerge_README.md'
            },
        },

        "lasoverage": {

            "LasOverage": {
                "name": 'LasOverage',
                "display_name": 'lasoverage',
                "licence_icon_path": licence["c"]["path"],
                "short_help_string": f"""
                reads LiDAR points of an airborne collect and finds the “overage” points that get covered by more than a single flightline. It either marks these overage points or removes them from the output files. The tool requires that the files either have the flightline information stored for each point in the point source ID field (e.g. for tiles containing overlapping flightlines) or that there are multiple files where each corresponds to a flight line (‘-files_are_flightlines’). It is also required that the scan angle field of each point is properly populated.
                
                For more details see the README file (Please click on help button).
                {icon_help_text}{licence["c"]["descript"]}
                """,
                "short_description": 'short_description ("for pro classes" using a folder contain multiple input file)',
                "url_path": 'url_path'
            },

            "LasOveragePro": {
                "name": 'LasOveragePro',
                "display_name": 'lasoverage (folder)',
                "licence_icon_path": licence["c"]["path"],
                "short_help_string": f"""
                reads LiDAR points of an airborne collect and finds the “overage” points that get covered by more than a single flightline. It either marks these overage points or removes them from the output files. The tool requires that the files either have the flightline information stored for each point in the point source ID field (e.g. for tiles containing overlapping flightlines) or that there are multiple files where each corresponds to a flight line (‘-files_are_flightlines’). It is also required that the scan angle field of each point is properly populated.

                With this tool you can choose a folder contain multiple input file rather than single file.
                For more details see the README file (Please click on help button).
                {icon_help_text}{licence["c"]["descript"]}
                """,
                "short_description": 'Find “overage” points of multiple lightlines (using a folder contain multiple input file).',
                "url_path": 'url_path'
            },

        },

        "lasboundary": {

            "LasBoundary": {
                "name": 'LasBoundary',
                "display_name": 'lasboundary',
                "licence_icon_path": licence["c"]["path"],
                "short_help_string": f"""
                reads LIDAR from LAS/LAZ/ASCII files and computes a boundary polygon that encloses the points. By default this is a joint concave hull where “islands of points” are connected by edges that are traversed in each direction once. Optionally a disjoint concave hull is computed with the ‘-disjoint’ flag. This can lead to multiple hulls in case of islands. Note that tiny islands of the size of one or two LIDAR points that are too small to form a triangle will be “lost”. 
                For more details see the README file (Please click on help button).
                {icon_help_text}{licence["c"]["descript"]}
                """,
                "short_description": 'Computes a boundary polygon that encloses LIDAR points.',
                "url_path": 'https://downloads.rapidlasso.de/readme/lasboundary_README.md'
            },

            "LasBoundaryPro": {
                "name": 'LasBoundaryPro',
                "display_name": 'lasboundary (folder)',
                "licence_icon_path": licence["c"]["path"],
                "short_help_string": f"""
                reads LIDAR from LAS/LAZ/ASCII files and computes a boundary polygon that encloses the points. By default this is a joint concave hull where “islands of points” are connected by edges that are traversed in each direction once. Optionally a disjoint concave hull is computed with the ‘-disjoint’ flag. This can lead to multiple hulls in case of islands. Note that tiny islands of the size of one or two LIDAR points that are too small to form a triangle will be “lost”. 
                With this tool you can choose a folder contain multiple input file rather than single file.
                For more details see the README file (Please click on help button).
                {icon_help_text}{licence["c"]["descript"]}
                """,
                "short_description": 'Computes a boundary polygon that encloses LIDAR points (using a folder contain multiple input file).',
                "url_path": 'https://downloads.rapidlasso.de/readme/lasboundary_README.md'
            },

        },

        "lasclip": {
            "LasClip": {
                "name": 'LasClip',
                "display_name": 'lasclip',
                "licence_icon_path": licence["c"]["path"],
                "short_help_string": f"""
                    takes as input a LAS/LAZ/TXT file and a SHP/TXT file with one or many polygons (e.g. building footprints or flight lines), clips away all the points that fall outside all polygons (or inside some polygon), and stores the surviving points to the output LAS/LAZ/TXT file. Instead of clipping the points they can also be classified.
                    
                    For more details see the README file (Please click on help button).
                {icon_help_text}{licence["c"]["descript"]}
                """,
                "short_description": 'Clip LIDAR data by polygons.',
                "url_path": 'https://downloads.rapidlasso.de/readme/lasclip_README.md'
            },
        },

        "lastile": {
            "LasTile": {
                "name": 'LasTile',
                "display_name": 'lastile',
                "licence_icon_path": licence["c"]["path"],
                "short_help_string": f"""
                tiles a potentially very large amount of LAS/LAZ/ASCII points from one  or many files into square non-overlapping tiles of a specified size and save them into LAS or LAZ format. Optionally the tool can also create a small ‘-buffer 10’ around every tile where the parameter 10 specifies the number of units each tile is (temporarily) grown in each direction. It is possible to remove the buffer from a tile by running with ‘-remove_buffer’ option. You may also flag the points that fall into the buffer with the new ‘-flag_as_withheld’ or ‘-flag_as_synthetic’ options. If you spatially index your input files using lasindex you may also run lastile on multiple processors with the ‘-cores 4’ option.

                For more details see the README file (Please click on help button).
                {icon_help_text}{licence["c"]["descript"]}
                """,
                "short_description": 'Tiles LIDAR points into tiles',
                "url_path": 'https://downloads.rapidlasso.de/readme/lastile_README.md'
            },

            "LasTilePro": {
                "name": 'LasTilePro',
                "display_name": 'lastile (folder)',
                "licence_icon_path": licence["c"]["path"],
                "short_help_string": f"""
                tiles a potentially very large amount of LAS/LAZ/ASCII points from one  or many files into square non-overlapping tiles of a specified size and save them into LAS or LAZ format. Optionally the tool can also create a small ‘-buffer 10’ around every tile where the parameter 10 specifies the number of units each tile is (temporarily) grown in each direction. It is possible to remove the buffer from a tile by running with ‘-remove_buffer’ option. You may also flag the points that fall into the buffer with the new ‘-flag_as_withheld’ or ‘-flag_as_synthetic’ options. If you spatially index your input files using lasindex you may also run lastile on multiple processors with the ‘-cores 4’ option.

                With this tool you can choose a folder contain multiple input file rather than single file.
                For more details see the README file (Please click on help button).
                {icon_help_text}{licence["c"]["descript"]}
                """,
                "short_description": 'Tiles LIDAR points into tiles (using a folder contain multiple input file)',
                "url_path": 'https://downloads.rapidlasso.de/readme/lastile_README.md'
            },

        },

        "lassplit": {
            "LasSplit": {
                "name": 'LasSplit',
                "display_name": 'lassplit',
                "licence_icon_path": licence["c"]["path"],
                "short_help_string": f"""
                    is a tool that splits LAS or LAZ files into multiple files based on some criteria. By default it splits the points into separate files based on the ‘point source ID’ field that usually contains the flightline ID. 
                    
                    For more details see the README file (Please click on help button).
                {icon_help_text}{licence["c"]["descript"]}
                """,
                "short_description": 'A tool that splits LAS or LAZ files into multiple files.',
                "url_path": 'https://downloads.rapidlasso.de/readme/lassplit_README.md'
            },
        },

        "lasnoise": {

            "LasNoise": {
                "name": 'LasNoise',
                "display_name": 'lasnoise',
                "licence_icon_path": licence["c"]["path"],
                "short_help_string": f"""
                    This tool flags or removes noise points in LAS/LAZ/BIN/ASCII files. The tool looks for isolated points according to certain criteria that can be modified via ‘-step 3’ and ‘-isolated 3’ as needed. The default for step is 4 and for isolated is 5. It is possible to specify the xy and the z size of the 27 cells separately with ‘-step_xy 2’ and ‘-step_z 0.3’ which would create cells of size 2 by 2 by 0.3 units.
    
                    The tool tries to find points that have only few other points in their surrounding 3 by 3 by 3 grid of cells with the cell the respective point falls into being in the center. The size of each of the 27 cells is set with the ‘-step 5’ parameter. The maximal number of few other points in the 3 by 3 by 3 grid still designating a point as isolated is set with ‘-isolated 6’.
                    
                    By default the noise points are given the classification code 7 (low or high noise). Using the ‘-remove_noise’ flag will instead remove them from the output file. Alternatively with the ‘-classify_as 31’ switch a different classification code can be selected. Another option is the ‘-flag_as_withheld’ switch which sets the withheld flag on the points identified as noise.
                    
                    For more details see the README file (Please click on help button).
                {icon_help_text}{licence["c"]["descript"]}
                """,
                "short_description": 'Flags or removes noise points in LAS or LAZ files.',
                "url_path": 'https://downloads.rapidlasso.de/readme/lasnoise_README.md'
            },

            "LasNoisePro": {
                "name": 'LasNoisePro',
                "display_name": 'lasnoise (folder)',
                "licence_icon_path": licence["c"]["path"],
                "short_help_string": f"""
                    This tool flags or removes noise points in LAS/LAZ/BIN/ASCII files. The tool looks for isolated points according to certain criteria that can be modified via ‘-step 3’ and ‘-isolated 3’ as needed. The default for step is 4 and for isolated is 5. It is possible to specify the xy and the z size of the 27 cells separately with ‘-step_xy 2’ and ‘-step_z 0.3’ which would create cells of size 2 by 2 by 0.3 units.
        
                    The tool tries to find points that have only few other points in their surrounding 3 by 3 by 3 grid of cells with the cell the respective point falls into being in the center. The size of each of the 27 cells is set with the ‘-step 5’ parameter. The maximal number of few other points in the 3 by 3 by 3 grid still designating a point as isolated is set with ‘-isolated 6’.
                    
                    By default the noise points are given the classification code 7 (low or high noise). Using the ‘-remove_noise’ flag will instead remove them from the output file. Alternatively with the ‘-classify_as 31’ switch a different classification code can be selected. Another option is the ‘-flag_as_withheld’ switch which sets the withheld flag on the points identified as noise.
                        
                    With this tool you can choose a folder contain multiple input file rather than single file.
                    For more details see the README file (Please click on help button).
                {icon_help_text}{licence["c"]["descript"]}
                """,
                "short_description": 'Flags or removes noise points in LAS or LAZ files (using a folder contain multiple input file).',
                "url_path": 'https://downloads.rapidlasso.de/readme/lasnoise_README.md'
            },

        },

        "lasdiff": {
            "LasDiff": {
                "name": 'LasDiff',
                "display_name": 'lasdiff',
                "licence_icon_path": licence["c"]["path"],
                "short_help_string": f"""
                    compares the LIDAR data of two LAS/LAZ/ASCII files and reports whether they are identical or whether they are different.
                    
                    For more details see the README file (Please click on help button).
                {icon_help_text}{licence["c"]["descript"]}
                """,
                "short_description": 'Compares the LIDAR data of two LAS/LAZ/ASCII files and reports whether they are identical or different.',
                "url_path": 'https://downloads.rapidlasso.de/readme/lasdiff_README.md'
            },
        },
    },

}

descript_classification_filtering = {
    "info": {
        "group": '4. Classification & Filtering',
        "group_id": 'classification_filtering',
    },
    "items": {

        "lasground": {
            "LasGround": {
                "name": 'LasGround',
                "display_name": 'lasground',
                "licence_icon_path": licence["c"]["path"],
                "short_help_string": f"""
                    is a tool for bare-earth extraction: it classifies the LiDAR points into ground points (class = 2) and non-ground points (class = 1). The tools works very well in natural environments such as mountains, forests, fields, hills, and even steep terrain but also gives excellent results in towns or cities. 
                    
                    For more details see the README file (Please click on help button).
                {icon_help_text}{licence["c"]["descript"]}
                """,
                "short_description": 'Tool for bare-earth extraction.',
                "url_path": 'https://downloads.rapidlasso.de/readme/lasground_README.md'
            },
            "LasGroundPro": {
                "name": 'LasGroundPro',
                "display_name": 'lasground (folder)',
                "licence_icon_path": licence["c"]["path"],
                "short_help_string": f"""
                    is a tool for bare-earth extraction: it classifies the LiDAR points into ground points (class = 2) and non-ground points (class = 1). The tools works very well in natural environments such as mountains, forests, fields, hills, and even steep terrain but also gives excellent results in towns or cities. 
                    
                    With this tool you can choose a folder contain multiple input file rather than single file.
                    For more details see the README file (Please click on help button).
                {icon_help_text}{licence["c"]["descript"]}
                """,
                "short_description": 'Tool for bare-earth extraction (using a folder contain multiple input file).',
                "url_path": 'https://downloads.rapidlasso.de/readme/lasground_README.md'
            },
        },

        "lasground_new": {
            "LasGroundNew": {
                "name": 'LasGroundNew',
                "display_name": 'lasground_new',
                "licence_icon_path": licence["c"]["path"],
                "short_help_string": f"""
                    This is a tool for bare-earth extraction: it classifies LIDAR points into ground points (class = 2) and non-ground points (class = 1). This is a totally redesigned version of lasground that handles complicated terrain much better where there are steep mountains nearby urban areas with many buildings.
                    
                    For more details see the README file (Please click on help button).
                {icon_help_text}{licence["c"]["descript"]}
                """,
                "short_description": 'This is a tool for bare-earth extraction—a redesigned version of lasground..',
                "url_path": 'https://downloads.rapidlasso.de/readme/lasground_README.md'
            },
            "LasGroundProNew": {
                "name": 'LasGroundProNew',
                "display_name": 'lasground_new (folder)',
                "licence_icon_path": licence["c"]["path"],
                "short_help_string": f"""
                    This is a tool for bare-earth extraction: it classifies LIDAR points into ground points (class = 2) and non-ground points (class = 1). This is a totally redesigned version of lasground that handles complicated terrain much better where there are steep mountains nearby urban areas with many buildings.

                    With this tool you can choose a folder contain multiple input file rather than single file.
                    For more details see the README file (Please click on help button).
                {icon_help_text}{licence["c"]["descript"]}
                """,
                "short_description": 'This is a tool for bare-earth extraction—a redesigned version of lasground. (using a folder contain multiple input file).',
                "url_path": 'https://downloads.rapidlasso.de/readme/lasground_README.md'
            },
        },

        "lasclassify": {

            "LasClassify": {
                "name": 'LasClassify',
                "display_name": 'lasclassify',
                "licence_icon_path": licence["c"]["path"],
                "short_help_string": f"""
                    is a tool to classify buildings and high vegetation (i.e. trees) in LAS/LAZ files. This tool requires that the bare-earth points have already been identified (e.g. with lasground) and that the elevation of each point above the ground was already computed with lasheight (which stores a coarse height value in the ‘user_data’ field of each point)
    
                    For more details see the README file (Please click on help button).
                {icon_help_text}{licence["c"]["descript"]}
                """,
                "short_description": 'Classify buildings and high vegetation',
                "url_path": 'https://downloads.rapidlasso.de/readme/lasclassify_README.md'
            },

            "LasClassifyPro": {
                "name": 'LasClassifyPro',
                "display_name": 'lasclassify (folder)',
                "licence_icon_path": licence["c"]["path"],
                "short_help_string": f"""
                    is a tool to classify buildings and high vegetation (i.e. trees) in LAS/LAZ files. This tool requires that the bare-earth points have already been identified (e.g. with lasground) and that the elevation of each point above the ground was already computed with lasheight (which stores a coarse height value in the ‘user_data’ field of each point)
    
                    With this tool you can choose a folder contain multiple input file rather than single file.
                    For more details see the README file (Please click on help button).
                {icon_help_text}{licence["c"]["descript"]}
                """,
                "short_description": 'Classify buildings and high vegetation (using a folder contain multiple input file)',
                "url_path": 'https://downloads.rapidlasso.de/readme/lasclassify_README.md'
            },

        },

        "lasthin": {

            "LasThin": {
                "name": 'LasThin',
                "display_name": 'lasthin',
                "licence_icon_path": licence["c"]["path"],
                "short_help_string": f"""
                    A simple LiDAR thinning algorithm for LAS/LAZ/ASCII. It places a uniform grid over the points and within each grid cell keeps only the point with the lowest (or ‘-highest’) Z coordinate a -random’ point per cell or the most ‘-central’ one. When keeping ‘-random’ points you can in addition specify a ‘-seed 232’ for the random generator. Instead of removing the thinned out points from the output file you can also flag them with ‘-flag_as_withheld’ or ‘-flag_as_keypoint’. Then you can use the standard ‘-drop_withheld’ or ‘-keep_withheld’ filters to get either the thinned points or their complement.
                    
                    For more details see the README file (Please click on help button).
                {icon_help_text}{licence["c"]["descript"]}
                """,
                "short_description": 'A simple LIDAR thinning algorithm',
                "url_path": 'https://downloads.rapidlasso.de/readme/lasthin_README.md'
            },

            "LasThinPro": {
                "name": 'LasThinPro',
                "display_name": 'lasthin (folder)',
                "licence_icon_path": licence["c"]["path"],
                "short_help_string": f"""
                    A simple LiDAR thinning algorithm for LAS/LAZ/ASCII. It places a uniform grid over the points and within each grid cell keeps only the point with the lowest (or ‘-highest’) Z coordinate a -random’ point per cell or the most ‘-central’ one. When keeping ‘-random’ points you can in addition specify a ‘-seed 232’ for the random generator. Instead of removing the thinned out points from the output file you can also flag them with ‘-flag_as_withheld’ or ‘-flag_as_keypoint’. Then you can use the standard ‘-drop_withheld’ or ‘-keep_withheld’ filters to get either the thinned points or their complement.
    
                    With this tool you can choose a folder contain multiple input file rather than single file.
                For more details see the README file (Please click on help button).
                {icon_help_text}{licence["c"]["descript"]}
                """,
                "short_description": 'A simple LIDAR thinning algorithm (using a folder contain multiple input file)',
                "url_path": 'https://downloads.rapidlasso.de/readme/lasthin_README.md'
            },
        },

    },
}

descript_dsm_dtm_generation_production = {
    "info": {
        "group": '5. DSM/DTM Generation & Production',
        "group_id": 'dsm_dtm_generation_production',
    },
    "items": {
        "las2dem": {

            "Las2Dem": {
                "name": 'Las2Dem',
                "display_name": 'las2dem',
                "licence_icon_path": licence["c"]["path"],
                "short_help_string": f"""
                    is a tool that triangulates LIDAR points from the LAS/LAZ format (or some ASCII format) into a temporary TIN and then rasters the TIN to create a DEM. The tool can either raster the ‘-elevation’, the ‘-slope’, the ‘-intensity’, the ‘-rgb’ values, or a ‘-hillshade’ or ‘-gray’ or ‘-false’ coloring. The output is either in BIL, ASC, IMG, FLT, XYZ, DTM, TIF, PNG or JPG format. 
    
                    For more details see the README file (Please click on help button).
                {icon_help_text}{licence["c"]["descript"]}
                """,
                "short_description": 'Triangulates LIDAR points from LAS/LAZ to TIN and DEM.',
                "url_path": 'https://downloads.rapidlasso.de/readme/las2dem_README.md'
            },

            "Las2DemPro": {
                "name": 'Las2DemPro',
                "display_name": 'las2dem (folder)',
                "licence_icon_path": licence["c"]["path"],
                "short_help_string": f"""
                    is a tool that triangulates LIDAR points from the LAS/LAZ format (or some ASCII format) into a temporary TIN and then rasters the TIN to create a DEM. The tool can either raster the ‘-elevation’, the ‘-slope’, the ‘-intensity’, the ‘-rgb’ values, or a ‘-hillshade’ or ‘-gray’ or ‘-false’ coloring. The output is either in BIL, ASC, IMG, FLT, XYZ, DTM, TIF, PNG or JPG format. 
    
                    With this tool you can choose a folder contain multiple input file rather than single file.
                For more details see the README file (Please click on help button).
                {icon_help_text}{licence["c"]["descript"]}
                """,
                "short_description": 'Triangulates LIDAR points from LAS/LAZ to TIN and DEM (using a folder contain multiple input file)',
                "url_path": 'https://downloads.rapidlasso.de/readme/las2dem_README.md'
            },
        },

        "las2iso": {
            "Las2Iso": {
                "name": 'Las2Iso',
                "display_name": 'las2iso',
                "licence_icon_path": licence["c"]["path"],
                "short_help_string": f"""
                    is a tool that reads LIDAR points from LAS/LAZ/ASCII (or rasters from ASC/BIL/DTM format) and extracts a set of particular elevation contours in SHP/KML/WKT/TXT format. The user may specify to extract contours every 5 meters or only for individual elevation values. The contours can be smoothed or simplified on demand and hydro breaklines can be specified as well. las2iso can handle files up to about 20 mio. points. 
    
                    For more details see the README file (Please click on help button).
                {icon_help_text}{licence["c"]["descript"]}
                """,
                "short_description": 'Extracts elevation contours to SHP/KML/WKT/TXT format',
                "url_path": 'https://downloads.rapidlasso.de/readme/las2iso_README.md'
            },
        },

        "lasgrid": {
            "LasGrid": {
                "name": 'LasGrid',
                "display_name": 'lasgrid',
                "licence_icon_path": licence["c"]["path"],
                "short_help_string": f"""
                is a tool that reads LIDAR from LAS/LAZ/ASCII and grids them onto a raster. The most important parameter ‘-step n’ specifies the n x n area that of LiDAR points that are gridded on one raster cell (or pixel). The output is either in BIL, ASC, IMG, TIF, PNG, JPG, XYZ, FLT, or DTM format. The tool can raster the ‘-elevation’ or the ‘-intensity’ of each point and stores the ‘-lowest’ or the ‘-highest’, the ‘-average’, or the standard deviation ‘-stddev’. Other gridding options are ‘-scan_angle_abs’, ‘-counter’, ‘-counter_16bit’, ‘-counter_32bit’, ‘-user_data’, ‘-point_source’, and others. 

                For more details see the README file (Please click on help button).
                {icon_help_text}{licence["c"]["descript"]}
                """,
                "short_description": 'Grid LIDAR onto a raster',
                "url_path": 'https://downloads.rapidlasso.de/readme/lasgrid_README.md'
            },

            "LasGridPro": {
                "name": 'LasGridPro',
                "display_name": 'lasgrid (folder)',
                "licence_icon_path": licence["c"]["path"],
                "short_help_string": f"""
                    is a tool that reads LIDAR from LAS/LAZ/ASCII and grids them onto a raster. The most important parameter ‘-step n’ specifies the n x n area that of LiDAR points that are gridded on one raster cell (or pixel). The output is either in BIL, ASC, IMG, TIF, PNG, JPG, XYZ, FLT, or DTM format. The tool can raster the ‘-elevation’ or the ‘-intensity’ of each point and stores the ‘-lowest’ or the ‘-highest’, the ‘-average’, or the standard deviation ‘-stddev’. Other gridding options are ‘-scan_angle_abs’, ‘-counter’, ‘-counter_16bit’, ‘-counter_32bit’, ‘-user_data’, ‘-point_source’, and others. 
    
                    With this tool you can choose a folder contain multiple input file rather than single file.
                    For more details see the README file (Please click on help button).
                {icon_help_text}{licence["c"]["descript"]}
                """,
                "short_description": 'Grid LIDAR onto a raster (using a folder contain multiple input file)',
                "url_path": 'https://downloads.rapidlasso.de/readme/lasgrid_README.md'
            },
        },

        "lasheight": {
            "LasHeight": {
                "name": 'LasHeight',
                "display_name": 'lasheight',
                "licence_icon_path": licence["c"]["path"],
                "short_help_string": f"""
                    computes the height of each point above the ground. This assumes that grounds points have already been ground-classified (with standard classification 2 or selected with ‘-class 31’ or ‘-classification 8’) so they can be identified to construct a ground TIN. The ground points can also be in an separate file ‘-ground_points ground.las’ or ‘-ground_points dtm.csv -parse ssxyz’. By default the resulting heights are quantized, scaled with a factor of 10, clamped into an unsigned char between 0 and 255, and stored in the “user data” field of each point.
    
                    For more details see the README file (Please click on help button).
                {icon_help_text}{licence["c"]["descript"]}
                """,
                "short_description": 'Computes the height of each point above the ground',
                "url_path": 'https://downloads.rapidlasso.de/readme/lasheight_README.md'
            },

            "LasHeightClassify": {
                "name": 'LasHeightClassify',
                "display_name": 'lasheight - classify',
                "licence_icon_path": licence["c"]["path"],
                "short_help_string": f"""
                    computes the height of each point above the ground. This assumes that grounds points have already been ground-classified (with standard classification 2 or selected with ‘-class 31’ or ‘-classification 8’) so they can be identified to construct a ground TIN. The ground points can also be in an separate file ‘-ground_points ground.las’ or ‘-ground_points dtm.csv -parse ssxyz’. By default the resulting heights are quantized, scaled with a factor of 10, clamped into an unsigned char between 0 and 255, and stored in the “user data” field of each point.
    
                    For more details see the README file (Please click on help button).
                {icon_help_text}{licence["c"]["descript"]}
                """,
                "short_description": 'Computes the height of each point above the ground',
                "url_path": 'https://downloads.rapidlasso.de/readme/lasheight_README.md'
            },

            "LasHeightPro": {
                "name": 'LasHeightPro',
                "display_name": 'lasheight (folder)',
                "licence_icon_path": licence["c"]["path"],
                "short_help_string": f"""
                    computes the height of each point above the ground. This assumes that grounds points have already been ground-classified (with standard classification 2 or selected with ‘-class 31’ or ‘-classification 8’) so they can be identified to construct a ground TIN. The ground points can also be in an separate file ‘-ground_points ground.las’ or ‘-ground_points dtm.csv -parse ssxyz’. By default the resulting heights are quantized, scaled with a factor of 10, clamped into an unsigned char between 0 and 255, and stored in the “user data” field of each point.
    
                    With this tool you can choose a folder contain multiple input file rather than single file.
                    For more details see the README file (Please click on help button).
                {icon_help_text}{licence["c"]["descript"]}
                """,
                "short_description": 'Computes the height of each point above the ground (using a folder contain multiple input file)',
                "url_path": 'https://downloads.rapidlasso.de/readme/lasheight_README.md'
            },

            "LasHeightProClassify": {
                "name": 'LasHeightProClassify',
                "display_name": 'lasheight - classify (folder)',
                "licence_icon_path": licence["c"]["path"],
                "short_help_string": f"""
                    computes the height of each point above the ground. This assumes that grounds points have already been ground-classified (with standard classification 2 or selected with ‘-class 31’ or ‘-classification 8’) so they can be identified to construct a ground TIN. The ground points can also be in an separate file ‘-ground_points ground.las’ or ‘-ground_points dtm.csv -parse ssxyz’. By default the resulting heights are quantized, scaled with a factor of 10, clamped into an unsigned char between 0 and 255, and stored in the “user data” field of each point.
    
                    With this tool you can choose a folder contain multiple input file rather than single file.
                    For more details see the README file (Please click on help button).
                {icon_help_text}{licence["c"]["descript"]}
                """,
                "short_description": 'Computes the height of each point above the ground (using a folder contain multiple input file)',
                "url_path": 'https://downloads.rapidlasso.de/readme/lasheight_README.md'
            },
        },

        "lascanopy": {
            "LasCanopy": {
                "name": 'LasCanopy',
                "display_name": 'lascanopy',
                "licence_icon_path": licence["c"]["path"],
                "short_help_string": f"""
                    is a tool that computes common forestry metrics from height-normalized LiDAR point clouds. It can compute canopy density or canopy cover (or gap fractions), height or intensity percentiles, averages, minima, maxima, kurtosis, skewness, standard deviation, and many more
    
                    For more details see the README file (Please click on help button).
                {icon_help_text}{licence["c"]["descript"]}
                """,
                "short_description": 'Computes common forestry metrics from height-normalized LiDAR point clouds',
                "url_path": 'https://downloads.rapidlasso.de/readme/lascanopy_README.md'
            },

            "LasCanopyPro": {
                "name": 'LasCanopyPro',
                "display_name": 'lascanopy (folder)',
                "licence_icon_path": licence["c"]["path"],
                "short_help_string": f"""
                    is a tool that computes common forestry metrics from height-normalized LiDAR point clouds. It can compute canopy density or canopy cover (or gap fractions), height or intensity percentiles, averages, minima, maxima, kurtosis, skewness, standard deviation, and many more
    
                    With this tool you can choose a folder contain multiple input file rather than single file.
                    For more details see the README file (Please click on help button).
                {icon_help_text}{licence["c"]["descript"]}
                """,
                "short_description": 'Computes common forestry metrics from height-normalized LiDAR point clouds ("using a folder contain multiple input file)',
                "url_path": 'https://downloads.rapidlasso.de/readme/lascanopy_README.md'
            },
        },

        "blast2dem": {
            "Blast2Dem": {
                "name": 'Blast2Dem',
                "display_name": 'blast2dem',
                "licence_icon_path": licence["c"]["path"],
                "short_help_string": f"""
                is almost identical to las2dem except that it can process much much larger inputs. While las2dem operates in-core and is therefore limited to a maximum of around 20 million points, blast2dem utilizes unique “streaming TIN” technology and can seamlessly process up to 2 billion points. This tool is part of the BLAST extension of LAStools. 

                For more details see the README file (Please click on help button).
                {icon_help_text}{licence["c"]["descript"]}
                """,
                "short_description": 'Rasters billions of LiDAR points via a streaming TIN to elevation, intensity, slope, or RGB grid.',
                "url_path": 'https://downloads.rapidlasso.de/readme/blast2dem_README.md'
            },
            "Blast2DemPro": {
                "name": 'Blast2DemPro',
                "display_name": 'blast2dem (folder)',
                "licence_icon_path": licence["c"]["path"],
                "short_help_string": f"""
                is almost identical to las2dem except that it can process much much larger inputs. While las2dem operates in-core and is therefore limited to a maximum of around 20 million points, blast2dem utilizes unique “streaming TIN” technology and can seamlessly process up to 2 billion points. This tool is part of the BLAST extension of LAStools. 

                With this tool you can choose a folder contain multiple input file rather than single file.
                For more details see the README file (Please click on help button).
                {icon_help_text}{licence["c"]["descript"]}
                """,
                "short_description": 'Rasters billions of LiDAR points via a streaming TIN to elevation, intensity, slope, or RGB grid (using a folder contain multiple input file)',
                "url_path": 'https://downloads.rapidlasso.de/readme/blast2dem_README.md'
            },
        },

        "blast2iso": {
            "Blast2Iso": {
                "name": 'Blast2Iso',
                "display_name": 'blast2iso',
                "licence_icon_path": licence["c"]["path"],
                "short_help_string": f"""
                    is almost identical to las2iso except that it can extract elevation contours from much much larger inputs. While las2iso operates in-core and is therefore limited to a maximum of around 20 million points, blast2iso utilizes unique “streaming TIN” technology and can seamlessly process up to 2 billion points. This tool is part of the BLAST extension of LAStools.
    
                    For more details see the README file (Please click on help button).
                {icon_help_text}{licence["c"]["descript"]}
                """,
                "short_description": 'Contours billions of LiDAR points via a streaming TIN to isolines in KML or SHP format. ',
                "url_path": 'https://downloads.rapidlasso.de/blast2iso_README.txt'
            },
            "Blast2IsoPro": {
                "name": 'Blast2IsoPro',
                "display_name": 'blast2iso (folder)',
                "licence_icon_path": licence["c"]["path"],
                "short_help_string": f"""
                    is almost identical to las2iso except that it can extract elevation contours from much much larger inputs. While las2iso operates in-core and is therefore limited to a maximum of around 20 million points, blast2iso utilizes unique “streaming TIN” technology and can seamlessly process up to 2 billion points. This tool is part of the BLAST extension of LAStools.
    
                    With this tool you can choose a folder contain multiple input file rather than single file.
                    For more details see the README file (Please click on help button).
                {icon_help_text}{licence["c"]["descript"]}
                """,
                "short_description": 'Contours billions of LiDAR points via a streaming TIN to isolines in KML or SHP format. (using a folder contain multiple input file)',
                "url_path": 'https://downloads.rapidlasso.de/blast2iso_README.txt'
            },
        },
    },
}

descript_quality_control_information = {
    "info": {
        "group": '6. Quality Control & Information',
        "group_id": 'quality_control_information',
    },
    "items": {
        "lasinfo": {
            "LasInfo": {
                "name": 'LasInfo',
                "display_name": 'lasinfo',
                "licence_icon_path": licence["o"]["path"],
                "short_help_string": f"""
                This is a handy tool to report the contents of the header, the VLRs, and a short summary of the min and max values of the points for LAS/LAZ files. The tool warns when there is a difference between the header information and the point content for counters and bounding box extent. 

                For more details see the README file (Please click on help button).
                {icon_help_text}{licence["o"]["descript"]}
                """,
                "short_description": 'Report content of a LAS/LAZ file header',
                "url_path": 'https://downloads.rapidlasso.de/readme/lasinfo_README.md'
            },

            "LasInfoPro": {
                "name": 'LasInfoPro',
                "display_name": 'lasinfo (folder)',
                "licence_icon_path": licence["o"]["path"],
                "short_help_string": f"""
                This is a handy tool to report the contents of the header, the VLRs, and a short summary of the min and max values of the points for LAS/LAZ files. The tool warns when there is a difference between the header information and the point content for counters and bounding box extent. 
                
                With this tool you can choose a folder contain multiple input file rather than single file.
                For more details see the README file (Please click on help button).
                {icon_help_text}{licence["o"]["descript"]}
                """,
                "short_description": 'Report content of a LAS/LAZ file header (using a folder contain multiple input file)',
                "url_path": 'https://downloads.rapidlasso.de/readme/lasinfo_README.md'
            },
        },

        "lasoverlap": {
            "LasOverlap": {
                "name": 'LasOverlap',
                "display_name": 'lasoverlap',
                "licence_icon_path": licence["c"]["path"],
                "short_help_string": f"""
                is a tool that reads LIDAR points from LAS/LAZ or ASCII files and computes the flight line overlap and / or the vertical and horizontal alignment. The output rasters can either be a color coded visual illustration of the level of overlap or the differences or the actual values and can be either in BIL, ASC, IMG, FLT, XYZ, DTM, TIF, PNG or JPG format.

                For more details see the README file (Please click on help button).
                {icon_help_text}{licence["c"]["descript"]}
                """,
                "short_description": 'Computes the flight line overlap and alignment of LIDAR points.',
                "url_path": 'https://downloads.rapidlasso.de/readme/lasoverlap_README.md'
            },
            "LasOverlapPro": {
                "name": 'LasOverlapPro',
                "display_name": 'lasoverlap (folder)',
                "licence_icon_path": licence["c"]["path"],
                "short_help_string": f"""
                is a tool that reads LIDAR points from LAS/LAZ or ASCII files and computes the flight line overlap and / or the vertical and horizontal alignment. The output rasters can either be a color coded visual illustration of the level of overlap or the differences or the actual values and can be either in BIL, ASC, IMG, FLT, XYZ, DTM, TIF, PNG or JPG format.

                With this tool you can choose a folder contain multiple input file rather than single file.
                For more details see the README file (Please click on help button).
                {icon_help_text}{licence["c"]["descript"]}
                """,
                "short_description": 'Computes the flight line overlap and alignment of LIDAR points (using a folder contain multiple input file)',
                "url_path": 'https://downloads.rapidlasso.de/readme/lasoverlap_README.md'

            },
        },

        "lascontrol": {
            "LasControl": {
                "name": 'LasControl',
                "display_name": 'lascontrol',
                "licence_icon_path": licence["c"]["path"],
                "short_help_string": f"""
                    computes the elevation of the LiDAR at certain x and y control point locations and reports the difference in respect to the control point elevation. The tool reads LiDAR in LAS/LAZ/ASCII format, triangulates the relevant points around the control points into a TIN.
    
                    For more details see the README file (Please click on help button).
                {icon_help_text}{licence["c"]["descript"]}
                """,
                "short_description": 'Computes the elevation of LiDAR data at specific points.',
                "url_path": 'https://rapidlasso.de/lascontrol/'
            },
        },

        "lasvalidate": {

            "LasValidate": {
                "name": 'LasValidate',
                "display_name": 'lasvalidate',
                "licence_icon_path": licence["o"]["path"],
                "short_help_string": f"""
                    A simple open source tool with LGPL 2.1 license to validate whether a single or a folder of LAS or LAZ files conform to the LAS specification of the ASPRS.
    
                    For more details see the README file (Please click on help button).
                {icon_help_text}{licence["o"]["descript"]}
                """,
                "short_description": 'Determine if LAS files conform to the ASPRS LAS specifications.',
                "url_path": 'https://downloads.rapidlasso.de/readme/lasvalidate_README.md'
            },

            "LasValidatePro": {
                "name": 'LasValidatePro',
                "display_name": 'lasvalidate (folder)',
                "licence_icon_path": licence["o"]["path"],
                "short_help_string": f"""
                    A simple open source tool with LGPL 2.1 license to validate whether a single or a folder of LAS or LAZ files conform to the LAS specification of the ASPRS.
    
                    With this tool you can choose a folder contain multiple input file rather than single file.
                    For more details see the README file (Please click on help button).
                {icon_help_text}{licence["o"]["descript"]}
                """,
                "short_description": 'Determine if LAS files conform to the ASPRS LAS specifications (using a folder contain multiple input file)',
                "url_path": 'https://downloads.rapidlasso.de/readme/lasvalidate_README.md'
            },
        },
    },
}

descript_publishing = {
    "info": {
        "group": '7. Publishing',
        "group_id": 'publishing',
    },
    "items": {
        "laspublish": {

            "LasPublish": {
                "name": 'LasPublish',
                "display_name": 'laspublish',
                "licence_icon_path": licence["c"]["path"],
                "short_help_string": f"""
                    Creates a LiDAR portal for 3D visualization (and optionally also for downloading) of LAS and LAZ files in any modern Web browser using the WebGL Potree from Markus Schuetz
    
                    For more details see the README file (Please click on help button).
                {icon_help_text}{licence["c"]["descript"]}
                """,
                "short_description": 'Creates a LiDAR portal for 3D visualization (and optionally also for downloading) of LAS and LAZ files in any modern Web browser.',
                "url_path": 'https://downloads.rapidlasso.de/readme/laspublish_README.md'
            },

            "LasPublishPro": {
                "name": 'LasPublishPro',
                "display_name": 'laspublish (folder)',
                "licence_icon_path": licence["c"]["path"],
                "short_help_string": f"""
                    Creates a LiDAR portal for 3D visualization (and optionally also for downloading) of LAS and LAZ files in any modern Web browser using the WebGL Potree from Markus Schuetz
    
                    With this tool you can choose a folder contain multiple input file rather than single file.
                    For more details see the README file (Please click on help button).
                {icon_help_text}{licence["c"]["descript"]}
                """,
                "short_description": 'Creates a LiDAR portal for 3D visualization (and optionally also for downloading) of LAS and LAZ files in any modern Web browser. (using a folder contain multiple input file)',
                "url_path": 'https://downloads.rapidlasso.de/readme/laspublish_README.md'
            },
        },
    },
}

descript_visualization_colorization = {
    "info": {
        "group": '8. Visualization & Colorization',
        "group_id": 'visualization_colorization',
    },
    "items": {

        "lasview": {
            "LasView": {
                "name": 'LasView',
                "display_name": 'lasview',
                "licence_icon_path": licence["c"]["path"],
                "short_help_string": f"""
                    is a simple yet fast LiDAR visualization tool that has a number of neat little tricks that may surprise you. It can also edit the classification of the points as well as delete them
    
                    For more details see the README file (Please click on help button).
                {icon_help_text}{licence["c"]["descript"]}
                """,
                "short_description": 'Simple and fast LiDAR visualization tool.',
                "url_path": 'https://downloads.rapidlasso.de/readme/lasview_README.md'
            },

            "LasViewPro": {
                "name": 'LasViewPro',
                "display_name": 'lasview (folder)',
                "licence_icon_path": licence["c"]["path"],
                "short_help_string": f"""
                    is a simple yet fast LiDAR visualization tool that has a number of neat little tricks that may surprise you. It can also edit the classification of the points as well as delete them
    
                    With this tool you can choose a folder contain multiple input file rather than single file.
                    For more details see the README file (Please click on help button).
                {icon_help_text}{licence["c"]["descript"]}
                """,
                "short_description": 'Simple and fast LiDAR visualization tool. (using a folder contain multiple input file)',
                "url_path": 'https://downloads.rapidlasso.de/readme/lasview_README.md'
            },
        },

        "lascolor": {
            "LasColor": {
                "name": 'LasColor',
                "display_name": 'lascolor',
                "licence_icon_path": licence["c"]["path"],
                "short_help_string": f"""
                    is a simple yet fast LiDAR visualization tool that has a number of neat little tricks that may surprise you. It can also edit the classification of the points as well as delete them.
    
                    For more details see the README file (Please click on help button).
                {icon_help_text}{licence["c"]["descript"]}
                """,
                "short_description": 'Colorize LIDAR points using an external image.',
                "url_path": 'https://downloads.rapidlasso.de/readme/lasview_README.md'
            },
        },
    },
}

descript_pipelines = {
    "info": {
        "group": '9. Pipelines',
        "group_id": 'pipelines',
    },
    "items": {
        "flightlines2chm": {

            "FlightLinesToCHMFirstReturn": {
                "name": 'FlightLinesToCHMFirstReturn',
                "display_name": 'Flightlines to CHM - first return',
                "licence_icon_path": licence["c"]["path"],
                "short_help_string": f"""
                    Create a canopy height model with first return only
                {icon_help_text}{licence["c"]["descript"]}
                """,
                "short_description": 'Create a canopy height model with first return only',
                "url_path": 'https://rapidlasso.de/product-overview/'
            },

            "FlightLinesToCHMHighestReturn": {
                "name": 'FlightLinesToCHMHighestReturn',
                "display_name": 'Flightlines to CHM - highest return',
                "licence_icon_path": licence["c"]["path"],
                "short_help_string": f"""
                    Create a canopy height model with highest return only
                {icon_help_text}{licence["c"]["descript"]}
                """,
                "short_description": 'Create a canopy height model with highest return only',
                "url_path": 'https://rapidlasso.de/product-overview/'
            },

            "FlightLinesToCHMSpikeFree": {
                "name": 'FlightLinesToCHMSpikeFree',
                "display_name": 'Flightlines to CHM - spike free',
                "licence_icon_path": licence["c"]["path"],
                "short_help_string": f"""
                    Create a canopy height model with spike free option
                {icon_help_text}{licence["c"]["descript"]}
                """,
                "short_description": 'Create a canopy height model with spike free option',
                "url_path": 'https://rapidlasso.de/product-overview/'
            },

        },

        "flightlines2dtmdsm": {
            "FlightLinesToDTMandDSMFirstReturn": {
                "name": 'FlightLinesToDTMandDSMFirstReturn',
                "display_name": 'FlightLines to DTM & DSM - first return',
                "licence_icon_path": licence["c"]["path"],
                "short_help_string": f"""
                     Create a digital terrain model and digital surface model out of lidar data files using the first return only
                {icon_help_text}{licence["c"]["descript"]}
                """,
                "short_description": 'Create a digital terrain model and digital surface model out of lidar data files using the first return only',
                "url_path": 'https://rapidlasso.de/product-overview/'
            },
            "FlightLinesToDTMandDSMSpikeFree": {
                "name": 'FlightLinesToDTMandDSMSpikeFree',
                "display_name": 'FlightLines to DTM & DSM - spike free',
                "licence_icon_path": licence["c"]["path"],
                "short_help_string": f"""
                    Create a digital terrain model and digital surface model with spike free option
                {icon_help_text}{licence["c"]["descript"]}
                """,
                "short_description": 'Create a digital terrain model and digital surface model with spike free option',
                "url_path": 'https://rapidlasso.de/product-overview/'
            },

        },

        "flightlines2mergedchm": {
            "FlightLinesToMergedCHMFirstReturn": {
                "name": 'FlightLinesToMergedCHMFirstReturn',
                "display_name": 'FlightLines to merged CHM - first return',
                "licence_icon_path": licence["c"]["path"],
                "short_help_string": f"""
                    Create a merged canopy height model out of lidar data files using the first return only
                {icon_help_text}{licence["c"]["descript"]}
                """,
                "short_description": 'Create a merged canopy height model out of lidar data files using the first return only',
                "url_path": 'https://rapidlasso.de/product-overview/'
            },

            "FlightLinesToMergedCHMHighestReturn": {
                "name": 'FlightLinesToMergedCHMHighestReturn',
                "display_name": 'FlightLines to merged CHM - highest return',
                "licence_icon_path": licence["c"]["path"],
                "short_help_string": f"""
                    Create a merged canopy height model out of lidar data files with highest return
                {icon_help_text}{licence["c"]["descript"]}
                """,
                "short_description": 'Create a merged canopy height model out of lidar data files with highest return',
                "url_path": 'https://rapidlasso.de/product-overview/'
            },

            "FlightLinesToMergedCHMPitFree": {
                "name": 'FlightLinesToMergedCHMPitFree',
                "display_name": 'FlightLines to merged CHM - pit free',
                "licence_icon_path": licence["c"]["path"],
                "short_help_string": f"""
                    Create a pit free merged canopy height model out of lidar data files
                {icon_help_text}{licence["c"]["descript"]}
                """,
                "short_description": 'Create a pit free merged canopy height model out of lidar data files',
                "url_path": 'https://rapidlasso.de/product-overview/'
            },

            "FlightLinesToMergedCHMSpikeFree": {
                "name": 'FlightLinesToMergedCHMSpikeFree',
                "display_name": 'FlightLines to merged CHM - spike free',
                "licence_icon_path": licence["c"]["path"],
                "short_help_string": f"""
                    Create a canopy height model out of lidar data files which are optional in flightlines
                {icon_help_text}{licence["c"]["descript"]}
                """,
                "short_description": 'Create a canopy height model out of lidar data files which are optional in flightlines',
                "url_path": 'https://rapidlasso.de/product-overview/'
            },
        },

        "hugefile": {
            "HugeFileClassify": {
                "name": 'HugeFileClassify',
                "display_name": 'Huge file - classify',
                "licence_icon_path": licence["c"]["path"],
                "short_help_string": f"""
                    Do a classification for huge lidar data files
                {icon_help_text}{licence["c"]["descript"]}
                """,
                "short_description": 'Do a classification for huge lidar data files',
                "url_path": 'https://rapidlasso.de/product-overview/'
            },
            "HugeFileGroundClassify": {
                "name": 'HugeFileGroundClassify',
                "display_name": 'Huge file - ground classify',
                "licence_icon_path": licence["c"]["path"],
                "short_help_string": f"""
                    Do a ground classification for huge lidar data files
                {icon_help_text}{licence["c"]["descript"]}
                """,
                "short_description": 'Do a ground classification for huge lidar data files',
                "url_path": 'https://rapidlasso.de/product-overview/'
            },
            "HugeFileNormalize": {
                "name": 'HugeFileNormalize',
                "display_name": 'Huge file - normalize',
                "licence_icon_path": licence["c"]["path"],
                "short_help_string": f"""
                    Normalize huge lidar data files
                {icon_help_text}{licence["c"]["descript"]}
                """,
                "short_description": 'Normalize huge lidar data files',
                "url_path": 'https://rapidlasso.de/product-overview/'
            },
        },
    },
}
