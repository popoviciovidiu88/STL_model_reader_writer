import parser
import fileManager
import model
import utilities

if __name__ == '__main__':
    print('main running')
    pars_device = parser.Parser()
    pars_device.parse_command_line()

    data_model = model.DataModel()

    file_manager_device = fileManager.FileManager(pars_device.args.input)

    file_manager_device.read_file(pars_device.args.input, data_model)

    utilities.print_model_header_console(data_model, pars_device.no_merge_flag)
    utilities.print_model_data_console(data_model)

    file_manager_device.write_to_file(pars_device.args.output, pars_device.output_file_type, data_model)
