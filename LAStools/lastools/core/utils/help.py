"""
descriptions of all the lastools
"""
import os

# ../plugins/LAStools/lastools + /assets/img
paths = {
    "lastools": f"{os.path.split(os.path.split(os.path.dirname(__file__))[0])[0]}/",
    "img": f"{os.path.split(os.path.split(os.path.dirname(__file__))[0])[0]}/assets/img/"
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
                "licence": True,
                "short_help_string": """
                short_help_string
                
                (for pro classes) With this tool you can choose a folder contain multiple input file rather than single file.
                For more details see the README file (Please click on help button).
                """,
                "short_description": 'short_description ("for pro classes" using a folder contain multiple input file)',
                "url_path": 'url_path'
            },
        },
    },

}

descript_processing = {
    "info": {
        "group": 'Preprocessing',
        "group_id": 'preprocessing',
    },
    "items": {
        "las3dpoly": {

            "Las3dPolyRadialDistance": {
                "name": 'Las3dPolyRadialDistance',
                "display_name": 'las3dpoly (Radial Distance)',
                "licence": True,
                "short_help_string": """
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
            """,
                "short_description": 'Modifies points within a certain radial distance of 3D polylines',
                "url_path": 'https://downloads.rapidlasso.de/readme/las3dpoly_README.md'
            },

            "Las3dPolyHorizontalVerticalDistance": {
                "name": 'Las3dPolyHorizontalVerticalDistance',
                "display_name": 'las3dpoly (Horizontal and Vertical Distance)',
                "licence": True,
                "short_help_string": """
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
            """,
                "short_description": 'Modifies points within a certain horizontal and vertical distance of 3D polylines',
                "url_path": 'https://downloads.rapidlasso.de/readme/las3dpoly_README.md'
            }

        },

        "lasintensity": {

            "LasIntensity": {
                "name": 'LasIntensity',
                "display_name": 'lasintensity',
                "licence": True,
                "short_help_string": """
                    ** Description
                    This tool corrects the intensity attenuation due to atmospheric absorption. 
                    Because the light has to travel longer distances for points with large scan angles, these points may be detected with reduced intensities.
                    
                    In order to get a reliant attenuation estimate several parameters are essential:
                    - Scanner height above ground level (AGL) [km]
                    - Scanner wavelength [µm]
                    - Atmospheric visibility range [km]
                    
                    For more details see the README file (Please click on help button).
                """,
                "short_description": 'corrects the intensity attenuation due to atmospheric absorption.',
                "url_path": 'https://downloads.rapidlasso.de/readme/lasintensity_README.md'
            },

            "LasIntensityAttenuationFactor": {
                "name": 'LasIntensityAttenuationFactor',
                "display_name": 'lasintensity (Attenuation Factor)',
                "licence": True,
                "short_help_string": """
                    ** Description
                    This tool corrects the intensity attenuation due to atmospheric absorption. 
                    Because the light has to travel longer distances for points with large scan angles, these points may be detected with reduced intensities.
                
                    In order to get a reliant attenuation estimate several parameters are essential:
                    - Scanner height above ground level (AGL) [km]
                    - Absorption coefficient [km^-1]
                    
                    For more details see the README file (Please click on help button).
                """,
                "short_description": 'corrects the intensity attenuation due to atmospheric absorption.',
                "url_path": 'https://downloads.rapidlasso.de/readme/lasintensity_README.md'

            },
        },

        "lasindex": {

            "LasIndex": {
                "name": 'LasIndex',
                "display_name": 'lasindex',
                "licence": False,
                "short_help_string": """
                    Creates a *.lax file for a given *.las or *.laz file that contains spatial indexing information. When this LAX file is present it will be used to speed up access to the relevant areas of the LAS/LAZ file.                   
                    
                    For more details see the README file (Please click on help button).
                """,
                "short_description": 'Creates an index file (LAX) about a LAS/LAZ file (using a folder contain multiple input file).',
                "url_path": 'https://downloads.rapidlasso.de/readme/lasindex_README.md'
            },

            "LasIndexPro": {
                "name": 'LasIndexPro',
                "display_name": 'lasindex (folder)',
                "licence": False,
                "short_help_string": """
                    Creates a *.lax file for a given *.las or *.laz file that contains spatial indexing information. When this LAX file is present it will be used to speed up access to the relevant areas of the LAS/LAZ file.                   
                    With this tool you can choose a folder contain multiple input file rather than single file.
                    For more details see the README file (Please click on help button).
                """,
                "short_description": 'Creates an index file (LAX) about a LAS/LAZ file (using a folder contain multiple input file).',
                "url_path": 'https://downloads.rapidlasso.de/readme/lasindex_README.md'
            },

        },

        "lasmerge": {
            "LasMerge": {
                "name": 'LasMerge',
                "display_name": 'lasmerge',
                "licence": False,
                "short_help_string": """
                This is a handy tool to merge multiple LiDAR files into one. However, we usually discourage this practice as this can also be achieved on-the-fly with the ‘-merged’ option in any of the other LAStools without creating a second copy on disk. In addition this tools allows splitting larger files into smaller subsets each containing a user-specified number of points. This tool is 100% open source LGPL.
                
                For more details see the README file (Please click on help button).
                """,
                "short_description": 'Merges several LAS or LAZ files.',
                "url_path": 'https://downloads.rapidlasso.de/readme/lasmerge_README.md'
            },

            "LasMergePro": {
                "name": 'LasMergePro',
                "display_name": 'lasmerge (folder)',
                "licence": False,
                "short_help_string": """
                This is a handy tool to merge multiple LiDAR files into one. However, we usually discourage this practice as this can also be achieved on-the-fly with the ‘-merged’ option in any of the other LAStools without creating a second copy on disk. In addition this tools allows splitting larger files into smaller subsets each containing a user-specified number of points. This tool is 100% open source LGPL.
                
                With this tool you can choose a folder contain multiple input file rather than single file.
                For more details see the README file (Please click on help button).
                """,
                "short_description": 'Merges several LAS or LAZ files (using a folder contain multiple input file).',
                "url_path": 'https://downloads.rapidlasso.de/readme/lasmerge_README.md'
            },
        },

        "lasoverage": {

            "LasOverage": {
                "name": 'LasOverage',
                "display_name": 'lasoverage',
                "licence": True,
                "short_help_string": """
                reads LiDAR points of an airborne collect and finds the “overage” points that get covered by more than a single flightline. It either marks these overage points or removes them from the output files. The tool requires that the files either have the flightline information stored for each point in the point source ID field (e.g. for tiles containing overlapping flightlines) or that there are multiple files where each corresponds to a flight line (‘-files_are_flightlines’). It is also required that the scan angle field of each point is properly populated.
                
                For more details see the README file (Please click on help button).
                """,
                "short_description": 'short_description ("for pro classes" using a folder contain multiple input file)',
                "url_path": 'url_path'
            },

            "LasOveragePro": {
                "name": 'LasOveragePro',
                "display_name": 'lasoverage (folder)',
                "licence": True,
                "short_help_string": """
                reads LiDAR points of an airborne collect and finds the “overage” points that get covered by more than a single flightline. It either marks these overage points or removes them from the output files. The tool requires that the files either have the flightline information stored for each point in the point source ID field (e.g. for tiles containing overlapping flightlines) or that there are multiple files where each corresponds to a flight line (‘-files_are_flightlines’). It is also required that the scan angle field of each point is properly populated.

                With this tool you can choose a folder contain multiple input file rather than single file.
                For more details see the README file (Please click on help button).
                """,
                "short_description": 'Find “overage” points of multiple lightlines (using a folder contain multiple input file).',
                "url_path": 'url_path'
            },

        },

        "lasboundary": {

            "LasBoundary": {
                "name": 'LasBoundary',
                "display_name": 'lasboundary',
                "licence": True,
                "short_help_string": """
                reads LIDAR from LAS/LAZ/ASCII files and computes a boundary polygon that encloses the points. By default this is a joint concave hull where “islands of points” are connected by edges that are traversed in each direction once. Optionally a disjoint concave hull is computed with the ‘-disjoint’ flag. This can lead to multiple hulls in case of islands. Note that tiny islands of the size of one or two LIDAR points that are too small to form a triangle will be “lost”. 
                For more details see the README file (Please click on help button).
                """,
                "short_description": 'Computes a boundary polygon that encloses LIDAR points.',
                "url_path": 'https://downloads.rapidlasso.de/readme/lasboundary_README.md'
            },

            "LasBoundaryPro": {
                "name": 'LasBoundaryPro',
                "display_name": 'lasboundary (folder)',
                "licence": True,
                "short_help_string": """
                reads LIDAR from LAS/LAZ/ASCII files and computes a boundary polygon that encloses the points. By default this is a joint concave hull where “islands of points” are connected by edges that are traversed in each direction once. Optionally a disjoint concave hull is computed with the ‘-disjoint’ flag. This can lead to multiple hulls in case of islands. Note that tiny islands of the size of one or two LIDAR points that are too small to form a triangle will be “lost”. 
                With this tool you can choose a folder contain multiple input file rather than single file.
                For more details see the README file (Please click on help button).
                """,
                "short_description": 'Computes a boundary polygon that encloses LIDAR points (using a folder contain multiple input file).',
                "url_path": 'https://downloads.rapidlasso.de/readme/lasboundary_README.md'
            },

        },

        "lasclip": {
            "LasClip": {
                "name": 'LasClip',
                "display_name": 'lasclip',
                "licence": True,
                "short_help_string": """
                    takes as input a LAS/LAZ/TXT file and a SHP/TXT file with one or many polygons (e.g. building footprints or flight lines), clips away all the points that fall outside all polygons (or inside some polygon), and stores the surviving points to the output LAS/LAZ/TXT file. Instead of clipping the points they can also be classified.
                    
                    For more details see the README file (Please click on help button).
                """,
                "short_description": 'Clip LIDAR data by polygons.',
                "url_path": 'https://downloads.rapidlasso.de/readme/lasclip_README.md'
            },
        },

        "lastile": {
            "LasTile": {
                "name": 'LasTile',
                "display_name": 'lastile',
                "licence": True,
                "short_help_string": """
                tiles a potentially very large amount of LAS/LAZ/ASCII points from one  or many files into square non-overlapping tiles of a specified size and save them into LAS or LAZ format. Optionally the tool can also create a small ‘-buffer 10’ around every tile where the parameter 10 specifies the number of units each tile is (temporarily) grown in each direction. It is possible to remove the buffer from a tile by running with ‘-remove_buffer’ option. You may also flag the points that fall into the buffer with the new ‘-flag_as_withheld’ or ‘-flag_as_synthetic’ options. If you spatially index your input files using lasindex you may also run lastile on multiple processors with the ‘-cores 4’ option.

                For more details see the README file (Please click on help button).
                """,
                "short_description": 'Tiles LIDAR points into tiles',
                "url_path": 'https://downloads.rapidlasso.de/readme/lastile_README.md'
            },

            "LasTilePro": {
                "name": 'LasTilePro',
                "display_name": 'lastile (folder)',
                "licence": True,
                "short_help_string": """
                tiles a potentially very large amount of LAS/LAZ/ASCII points from one  or many files into square non-overlapping tiles of a specified size and save them into LAS or LAZ format. Optionally the tool can also create a small ‘-buffer 10’ around every tile where the parameter 10 specifies the number of units each tile is (temporarily) grown in each direction. It is possible to remove the buffer from a tile by running with ‘-remove_buffer’ option. You may also flag the points that fall into the buffer with the new ‘-flag_as_withheld’ or ‘-flag_as_synthetic’ options. If you spatially index your input files using lasindex you may also run lastile on multiple processors with the ‘-cores 4’ option.

                With this tool you can choose a folder contain multiple input file rather than single file.
                For more details see the README file (Please click on help button).
                """,
                "short_description": 'Tiles LIDAR points into tiles (using a folder contain multiple input file)',
                "url_path": 'https://downloads.rapidlasso.de/readme/lastile_README.md'
            },

        },

        "lassplit": {
            "LasSplit": {
                "name": 'LasSplit',
                "display_name": 'lassplit',
                "licence": True,
                "short_help_string": """
                    is a tool that splits LAS or LAZ files into multiple files based on some criteria. By default it splits the points into separate files based on the ‘point source ID’ field that usually contains the flightline ID. 
                    
                    For more details see the README file (Please click on help button).
                """,
                "short_description": 'A tool that splits LAS or LAZ files into multiple files.',
                "url_path": 'https://downloads.rapidlasso.de/readme/lassplit_README.md'
            },
        },

        

    },

}
