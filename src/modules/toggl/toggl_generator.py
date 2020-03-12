#! /usr/bin/env python3

def generate_file(data):
    file = """
conky.config = {
    alignment = 'bottom_left',
    background = false,
    border_width = 1,
    
    background = true,
    update_interval = 1,
    double_buffer = true,
    no_buffers = true,

    gap_x = 0,
    gap_y = 0,
    maximum_width = 268,
    minimum_width = 268,
    minimum_height = 200,
    own_window = true,
    own_window_type = 'normal',
    own_window_transparent = true,
    own_window_argb_visual = true,
    own_window_argb_value = 255,
    own_window_hints = 'undecorated,sticky,skip_taskbar,skip_pager,below',
    own_window = true,
    own_window_transparent = true,
    own_window_argb_visual = true,
    own_window_class = 'Conky',
    own_window_type = 'desktop',
    border_inner_margin = 0,
    border_outer_margin = 0,

    draw_shades = false,
    default_shade_color = 'AAAAAA',
    draw_outline = false,
    default_outline_color = 'AAAAAA',
    draw_borders = false,
    draw_graph_borders = false,
    default_graph_width = 20,
    default_graph_height = 80,
    show_graph_scale = false,
    show_graph_range = false,

    use_xft = true,
    xftalpha = 0,
    xftfont = 'Droid Sans:size=8',
    text_buffer_size = 256,
    override_utf8_locale = true,

    short_units = true,
    pad_percents = 2,
    top_name_width = 30,

    default_color = 'FFFFFF',
    color1 = 'FFFFFF',
    color2 = 'FFFFFF',
    color3 = 'FFFFFF',
    color4 = 'FFFFFF',
    color5 = 'DCDCDC',
    color6 = 'FFFFFF',
    color7 = 'FFFFFF',
    color8 = 'FFFFFF'
}

conky.text = [[
    """
    file += "${image src/icons/toggl.png -p 2,2 -s 100x25 -f 86400}"
    file += """
    \\
    """
    file += "${hr 1}"
    file += """
    \\
    """
    if not data:
        file += "${image src/icons/alert.png -p 70,70 -s 100x100 -f 86400}"
    file += "${color white}${font Drois Sans:size=10}${execi 5 python3 src/modules/toggl/toggl.py}"
    file += """
\\
]]
    """
    return file

if __name__ == '__main__':
    print(generate_file([]))
