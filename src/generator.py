from jinja2 import Template
import configparser

# This script applies values in ../config.ini to all configurations

def generate_config(template_path, conky_destination):

    config = configparser.ConfigParser()
    config.read('config.ini')

    try:
        with open(template_path, 'r') as f:
            jinja_template = f.read()
            tm = Template(jinja_template)
            generated_config = tm.render(config=config)

            file = open(conky_destination, 'w')
            file.write(generated_config)

            file.close()

    except Exception as e:
        print('The jinja template was not found at: ' + template_path)


generate_config('src/modules/gmail/template', 'config/conky_gmail')
generate_config('src/modules/gcalendar/template', 'config/conky_gcalendar')
generate_config('src/modules/github/template', 'config/conky_github')
generate_config('src/modules/toggl/template', 'config/conky_toggl')
generate_config('src/modules/weather/template', 'config/conky_weather')
generate_config('src/modules/attendance/template', 'config/conky_attendance')
