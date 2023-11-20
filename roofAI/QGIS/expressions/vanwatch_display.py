from qgis.core import *
from qgis.gui import *

@qgsfunction(args='auto', group='Custom', referenced_columns=[])
def vanwatch_display(object_name, cameras, feature, parent):
    """
    Produce display text for a vanwatch mapid.
    
    vanwatch_display(
        layer_property(@layer,'name'),
        "cameras"
    )
    """
    url_prefix = "https://kamangir-public.s3.ca-central-1.amazonaws.com"

    image_name_list = [url.split("/")[-1].split(".")[0] for url in cameras.split(",")]
    
    url_list = ["{}/{}/{}-inference.jpg".format(
        url_prefix,
        object_name,
        image_name,
        ) for image_name in image_name_list]
    
    image_tag_list = [f"<img src=\"{url}\">" for url in url_list]
    
    return "\n".join(["<table border=\"1\">",
    "    <tr>"]+
    [f"        <td>{image_tag}</td>" for image_tag in image_tag_list]+
    ["    </tr>",
    "</table>"])
