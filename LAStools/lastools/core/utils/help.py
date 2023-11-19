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
                "licence": False,
                "short_help_string": """
                short_help_string
                """,
                "short_description": 'short_description',
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
                """,
                "short_description": 'corrects the intensity attenuation due to atmospheric absorption.',
                "url_path": 'https://downloads.rapidlasso.de/readme/lasintensity_README.md'

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
                For more details see the README file (Please click on help button).
                """,
                "short_description": 'Computes a boundary polygon that encloses LIDAR points.',
                "url_path": 'https://downloads.rapidlasso.de/readme/lasboundary_README.md'
            },

        },

        "lasindex": {

            "LasIndex": {
                "name": 'LasIndex',
                "display_name": 'lasindex',
                "licence": False,
                "short_help_string": """
                    Creates a *.lax file for a given *.las or *.laz file that contains spatial indexing information. When this LAX file is present it will be used to speed up access to the relevant areas of the LAS/LAZ file whenever a spatial queries of the type
    
                    -inside_tile ll_x ll_y size  
                    -inside_circle center_x center_y radius  
                    -inside_rectangle min_x min_y max_x max_y  (or simply -inside)  
                    
                    appears in the command line of any LAStools invocation. This acceleration is also available to users of the LASlib API. The LASreader class has three new functions called
                    
                    BOOL inside_tile(F32 ll_x, F32 ll_y, F32 size);  
                    BOOL inside_circle(F64 center_x, F64 center_y, F64 radius);  
                    BOOL inside_rectangle(F64 min_x, F64 min_y, F64 max_x, F64 max_y);  
                    
                    if any of these functions is called the LASreader will only return the points that fall inside the specified region and use - when available - the spatial indexing information in the LAX file created by lasindex.
                """,
                "short_description": 'Creates an index file (LAX) about a LAS/LAZ file (using multi file inside a folder).',
                "url_path": 'https://downloads.rapidlasso.de/readme/lasindex_README.md'
            },

            "LasIndexPro": {
                "name": 'LasIndexPro',
                "display_name": 'lasindex (folder)',
                "licence": False,
                "short_help_string": """
                    Creates a *.lax file for a given *.las or *.laz file that contains spatial indexing information. When this LAX file is present it will be used to speed up access to the relevant areas of the LAS/LAZ file whenever a spatial queries of the type
    
                    -inside_tile ll_x ll_y size  
                    -inside_circle center_x center_y radius  
                    -inside_rectangle min_x min_y max_x max_y  (or simply -inside)  
                    
                    appears in the command line of any LAStools invocation. This acceleration is also available to users of the LASlib API. The LASreader class has three new functions called
                    
                    BOOL inside_tile(F32 ll_x, F32 ll_y, F32 size);  
                    BOOL inside_circle(F64 center_x, F64 center_y, F64 radius);  
                    BOOL inside_rectangle(F64 min_x, F64 min_y, F64 max_x, F64 max_y);  
                    
                    if any of these functions is called the LASreader will only return the points that fall inside the specified region and use - when available - the spatial indexing information in the LAX file created by lasindex.
                """,
                "short_description": 'Creates an index file (LAX) about a LAS/LAZ file (using multi file inside a folder).',
                "url_path": 'https://downloads.rapidlasso.de/readme/lasindex_README.md'
            },

        },
    },

}
