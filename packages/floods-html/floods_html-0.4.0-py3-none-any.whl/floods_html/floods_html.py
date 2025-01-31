from floods_html import json_format as jf


def json_to_html(input, svg_location=""):
    """
    Converts a flooding JSON object to flooding HTML object.

    Parameters
    ----------
    input : str or dict or FHJSON
        Input JSON object.
    svg_location='': str
        Location of the SVG files.

    Returns
    -------
    html_output : List[str]
        List of HTML strings for each entry in the JSON object.

    """
    if type(input) is str:
        pydantic_data_object = jf.FHJSON.model_validate_json(input)
    elif type(input) is dict:
        pydantic_data_object = jf.FHJSON(**input)
    elif isinstance(input, jf.FHJSON):
        pydantic_data_object = input
    else:
        raise ValueError("Invalid input type. Must be either a JSON string, JSON object, or a FHJSON class instance.")
    html_output = []
    for entry in pydantic_data_object.data:
        html_entry = entry_to_html(entry, svg_location)
        html_output.append(html_entry)
    return html_output


def entry_to_html(entry, svg_location):
    if entry.type == "table":
        return table_to_html(entry.data)
    elif entry.type == "svg_figure":
        return svg_figure_to_html(entry.data, svg_location)
    else:
        raise ValueError("Unknown entry type: {}".format(entry.type))


def table_to_html(json):
    html_template = "<{html_tag}{html_options}>{value}</{html_tag}>"

    def html_options_to_str(x):
        return "".join(
            [
                " {0}={1}".format(k, v if type(v) is str else '"' + "".join([f"{a}:{b};" for a, b in v.items()]) + '"')
                for k, v in x.items()
            ]
        )

    table_row_str = ""
    for table_row in json.headers.data:
        table_entry_str = ""
        for header_entry in table_row.data:
            table_entry_str += html_template.format(
                html_tag="th", html_options=html_options_to_str(header_entry.html_options), value=header_entry.value
            )
        table_row_str += html_template.format(
            html_tag="tr", html_options=html_options_to_str(table_row.html_options), value=table_entry_str
        )
    table_header_str = html_template.format(
        html_tag="thead", html_options=html_options_to_str(json.headers.html_options), value=table_row_str
    )

    table_row_str = ""
    for table_row in json.rows.data:
        table_entry_str = ""
        for table_entry in table_row.data:
            table_entry_str += html_template.format(
                html_tag="td", html_options=html_options_to_str(table_entry.html_options), value=table_entry.value
            )
        table_row_str += html_template.format(
            html_tag="tr", html_options=html_options_to_str(table_row.html_options), value=table_entry_str
        )
    table_body_str = html_template.format(
        html_tag="tbody", html_options=html_options_to_str(json.rows.html_options), value=table_row_str
    )

    table_str = html_template.format(
        html_tag="table", html_options=html_options_to_str(json.html_options), value=table_header_str + table_body_str
    )

    title_str = html_template.format(html_tag="h3", html_options="", value=json.title)

    return title_str + table_str


def svg_figure_to_html(json, svg_location):
    svg_file = svg_location + json.filename

    if svg_file[:4] == "http":
        figure_html_template = """
            <span>
                <h4>{title}</h4>
                <img src={imgname}/>
            </span>
        """

        figure_html = figure_html_template.format(
            title=json.title,
            imgname=svg_file,
        )
    else:
        figure_html_template = """
        <div>
            <span>
                <h4>{title}</h4>
                {svg}
            </span>
        </div>
        """

        svg_contents = open(svg_file, "r").read()

        figure_html = figure_html_template.format(
            title=json.title,
            svg=svg_contents,
        )

    return figure_html
